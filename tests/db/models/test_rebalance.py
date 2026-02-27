import pytest

from xarizmi.db.models.rebalance import (
    PortfolioAllocation,
    PortfolioAllocationItem,
    RebalanceItem,
    RebalanceResult,
)
from xarizmi.models.rebalance import (
    PortfolioAllocation as PyPortfolioAllocation,
)
from xarizmi.models.rebalance import (
    PortfolioAllocationItem as PyPortfolioAllocationItem,
)
from xarizmi.models.rebalance import RebalanceItem as PyRebalanceItem
from xarizmi.models.rebalance import RebalanceResult as PyRebalanceResult
from xarizmi.models.symbol import Symbol as PySymbol


@pytest.fixture
def py_allocation(db_symbol, db_eth_symbol) -> PyPortfolioAllocation:  # type: ignore[no-untyped-def]
    return PyPortfolioAllocation(
        items=[
            PyPortfolioAllocationItem(
                symbol=PySymbol.build("BTC", "USD", "USD", "BINANCE"),
                weight=0.6,
            ),
            PyPortfolioAllocationItem(
                symbol=PySymbol.build("ETH", "USD", "USD", "BINANCE"),
                weight=0.4,
            ),
        ]
    )


class TestPortfolioAllocationFromPydantic:
    def test_creates_db_object(self, py_allocation) -> None:  # type: ignore[no-untyped-def]
        db_alloc = PortfolioAllocation.from_pydantic(py_allocation)
        assert isinstance(db_alloc, PortfolioAllocation)


class TestPortfolioAllocationItemFromPydantic:
    def test_weight_is_set(self, db_symbol) -> None:  # type: ignore[no-untyped-def]
        py_item = PyPortfolioAllocationItem(
            symbol=PySymbol.build("BTC", "USD", "USD", "BINANCE"),
            weight=0.6,
        )
        db_item = PortfolioAllocationItem.from_pydantic(
            py_item, symbol_id=db_symbol.id, allocation_id=1
        )
        assert db_item.weight == 0.6

    def test_symbol_id_fk_is_set(self, db_symbol) -> None:  # type: ignore[no-untyped-def]
        py_item = PyPortfolioAllocationItem(
            symbol=PySymbol.build("BTC", "USD", "USD", "BINANCE"),
            weight=0.5,
        )
        db_item = PortfolioAllocationItem.from_pydantic(
            py_item, symbol_id=db_symbol.id, allocation_id=1
        )
        assert db_item.symbol_id == db_symbol.id

    def test_allocation_id_fk_is_set(self, db_symbol) -> None:  # type: ignore[no-untyped-def]
        py_item = PyPortfolioAllocationItem(
            symbol=PySymbol.build("BTC", "USD", "USD", "BINANCE"),
            weight=0.5,
        )
        db_item = PortfolioAllocationItem.from_pydantic(
            py_item, symbol_id=db_symbol.id, allocation_id=42
        )
        assert db_item.allocation_id == 42


class TestPortfolioAllocationItemToPydantic:
    def test_returns_pydantic_item(self, session, db_symbol) -> None:  # type: ignore[no-untyped-def]
        db_alloc = PortfolioAllocation()
        session.add(db_alloc)
        session.flush()

        db_item = PortfolioAllocationItem(
            allocation_id=db_alloc.id,
            symbol_id=db_symbol.id,
            weight=0.7,
        )
        session.add(db_item)
        session.flush()

        fetched = session.get(PortfolioAllocationItem, db_item.id)
        assert fetched is not None
        result = fetched.to_pydantic()
        assert isinstance(result, PyPortfolioAllocationItem)

    def test_weight_matches(self, session, db_symbol) -> None:  # type: ignore[no-untyped-def]
        db_alloc = PortfolioAllocation()
        session.add(db_alloc)
        session.flush()

        db_item = PortfolioAllocationItem(
            allocation_id=db_alloc.id,
            symbol_id=db_symbol.id,
            weight=0.35,
        )
        session.add(db_item)
        session.flush()

        fetched = session.get(PortfolioAllocationItem, db_item.id)
        assert fetched is not None
        assert fetched.to_pydantic().weight == 0.35

    def test_symbol_loaded_via_relationship(self, session, db_symbol) -> None:  # type: ignore[no-untyped-def]
        # The symbol FK is the DB link; to_pydantic() uses the relationship
        # to reconstruct the full pydantic Symbol.
        db_alloc = PortfolioAllocation()
        session.add(db_alloc)
        session.flush()

        db_item = PortfolioAllocationItem(
            allocation_id=db_alloc.id,
            symbol_id=db_symbol.id,
            weight=1.0,
        )
        session.add(db_item)
        session.flush()

        fetched = session.get(PortfolioAllocationItem, db_item.id)
        assert fetched is not None
        result = fetched.to_pydantic()
        assert result.symbol.base_currency.name == "BTC"


class TestPortfolioAllocationToPydantic:
    def test_round_trip_with_items(
        self, session, db_symbol, db_eth_symbol
    ) -> None:  # type: ignore[no-untyped-def]
        db_alloc = PortfolioAllocation()
        session.add(db_alloc)
        session.flush()

        session.add_all(
            [
                PortfolioAllocationItem(
                    allocation_id=db_alloc.id,
                    symbol_id=db_symbol.id,
                    weight=0.6,
                ),
                PortfolioAllocationItem(
                    allocation_id=db_alloc.id,
                    symbol_id=db_eth_symbol.id,
                    weight=0.4,
                ),
            ]
        )
        session.flush()

        fetched = session.get(PortfolioAllocation, db_alloc.id)
        assert fetched is not None
        result = fetched.to_pydantic()
        assert isinstance(result, PyPortfolioAllocation)
        assert len(result.items) == 2

    def test_allocation_fk_relationship(self, session, db_symbol) -> None:  # type: ignore[no-untyped-def]
        # PortfolioAllocationItem has FK allocation_id → PortfolioAllocation.id
        db_alloc = PortfolioAllocation()
        session.add(db_alloc)
        session.flush()

        db_item = PortfolioAllocationItem(
            allocation_id=db_alloc.id,
            symbol_id=db_symbol.id,
            weight=1.0,
        )
        session.add(db_item)
        session.flush()

        fetched_item = session.get(PortfolioAllocationItem, db_item.id)
        assert fetched_item is not None
        assert fetched_item.allocation_id == db_alloc.id


class TestRebalanceResultFromPydantic:
    def test_total_value_is_set(self) -> None:
        py_result = PyRebalanceResult(items=[], total_value=100_000.0)
        db_result = RebalanceResult.from_pydantic(py_result)
        assert db_result.total_value == 100_000.0


class TestRebalanceItemFromPydantic:
    def test_fields_are_set(self, db_symbol) -> None:  # type: ignore[no-untyped-def]
        py_item = PyRebalanceItem(
            symbol=PySymbol.build("BTC", "USD", "USD", "BINANCE"),
            current_weight=0.8,
            target_weight=0.5,
            current_market_value=80_000.0,
            target_market_value=50_000.0,
            delta_market_value=-30_000.0,
        )
        db_item = RebalanceItem.from_pydantic(
            py_item, symbol_id=db_symbol.id, result_id=1
        )
        assert db_item.current_weight == 0.8
        assert db_item.target_weight == 0.5
        assert db_item.current_market_value == 80_000.0
        assert db_item.target_market_value == 50_000.0
        assert db_item.delta_market_value == -30_000.0

    def test_symbol_id_fk_is_set(self, db_symbol) -> None:  # type: ignore[no-untyped-def]
        py_item = PyRebalanceItem(
            symbol=PySymbol.build("BTC", "USD", "USD", "BINANCE"),
            current_weight=0.5,
            target_weight=0.5,
            current_market_value=50_000.0,
            target_market_value=50_000.0,
            delta_market_value=0.0,
        )
        db_item = RebalanceItem.from_pydantic(
            py_item, symbol_id=db_symbol.id, result_id=99
        )
        assert db_item.symbol_id == db_symbol.id
        assert db_item.result_id == 99


class TestRebalanceItemToPydantic:
    def test_fields_match_after_db_round_trip(
        self, session, db_symbol
    ) -> None:  # type: ignore[no-untyped-def]
        db_result = RebalanceResult(total_value=100_000.0)
        session.add(db_result)
        session.flush()

        db_item = RebalanceItem(
            result_id=db_result.id,
            symbol_id=db_symbol.id,
            current_weight=0.8,
            target_weight=0.5,
            current_market_value=80_000.0,
            target_market_value=50_000.0,
            delta_market_value=-30_000.0,
        )
        session.add(db_item)
        session.flush()

        fetched = session.get(RebalanceItem, db_item.id)
        assert fetched is not None
        result = fetched.to_pydantic()
        assert isinstance(result, PyRebalanceItem)
        assert result.current_weight == 0.8
        assert result.target_weight == 0.5
        assert result.delta_market_value == -30_000.0

    def test_symbol_loaded_via_relationship(self, session, db_symbol) -> None:  # type: ignore[no-untyped-def]
        # symbol FK links to Symbol table; to_pydantic() navigates relationship
        db_result = RebalanceResult(total_value=50_000.0)
        session.add(db_result)
        session.flush()

        db_item = RebalanceItem(
            result_id=db_result.id,
            symbol_id=db_symbol.id,
            current_weight=1.0,
            target_weight=0.5,
            current_market_value=50_000.0,
            target_market_value=25_000.0,
            delta_market_value=-25_000.0,
        )
        session.add(db_item)
        session.flush()

        fetched = session.get(RebalanceItem, db_item.id)
        assert fetched is not None
        result = fetched.to_pydantic()
        assert result.symbol.base_currency.name == "BTC"


class TestRebalanceResultToPydantic:
    def test_round_trip_with_items(
        self, session, db_symbol, db_eth_symbol
    ) -> None:  # type: ignore[no-untyped-def]
        db_result = RebalanceResult(total_value=100_000.0)
        session.add(db_result)
        session.flush()

        session.add_all(
            [
                RebalanceItem(
                    result_id=db_result.id,
                    symbol_id=db_symbol.id,
                    current_weight=0.8,
                    target_weight=0.5,
                    current_market_value=80_000.0,
                    target_market_value=50_000.0,
                    delta_market_value=-30_000.0,
                ),
                RebalanceItem(
                    result_id=db_result.id,
                    symbol_id=db_eth_symbol.id,
                    current_weight=0.2,
                    target_weight=0.5,
                    current_market_value=20_000.0,
                    target_market_value=50_000.0,
                    delta_market_value=30_000.0,
                ),
            ]
        )
        session.flush()

        fetched = session.get(RebalanceResult, db_result.id)
        assert fetched is not None
        result = fetched.to_pydantic()
        assert isinstance(result, PyRebalanceResult)
        assert result.total_value == 100_000.0
        assert len(result.items) == 2

    def test_result_fk_relationship(self, session, db_symbol) -> None:  # type: ignore[no-untyped-def]
        # RebalanceItem has FK result_id → RebalanceResult.id
        db_result = RebalanceResult(total_value=10_000.0)
        session.add(db_result)
        session.flush()

        db_item = RebalanceItem(
            result_id=db_result.id,
            symbol_id=db_symbol.id,
            current_weight=1.0,
            target_weight=1.0,
            current_market_value=10_000.0,
            target_market_value=10_000.0,
            delta_market_value=0.0,
        )
        session.add(db_item)
        session.flush()

        fetched_item = session.get(RebalanceItem, db_item.id)
        assert fetched_item is not None
        assert fetched_item.result_id == db_result.id
