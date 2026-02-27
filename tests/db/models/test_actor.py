from xarizmi.db.models.actor import (
    Actor,
    ExchangeActor,
    InvestorActor,
    TraderActor,
)
from xarizmi.models.actors import Actor as PyActor
from xarizmi.models.actors import ExchangeActor as PyExchangeActor
from xarizmi.models.actors import InvestorActor as PyInvestorActor
from xarizmi.models.actors import TraderActor as PyTraderActor


class TestActorFromPydantic:
    def test_asset_is_set(self) -> None:
        py_actor = PyActor(asset=1_000.0)
        db_actor = Actor.from_pydantic(py_actor)
        assert db_actor.asset == 1_000.0

    def test_zero_asset(self) -> None:
        db_actor = Actor.from_pydantic(PyActor(asset=0.0))
        assert db_actor.asset == 0.0


class TestActorToPydantic:
    def test_returns_py_actor(self) -> None:
        db_actor = Actor(asset=500.0, actor_type="actor")
        result = db_actor.to_pydantic()
        assert isinstance(result, PyActor)

    def test_asset_matches(self) -> None:
        db_actor = Actor(asset=250.0, actor_type="actor")
        result = db_actor.to_pydantic()
        assert result.asset == 250.0


class TestActorRoundTrip:
    def test_round_trip_through_db(self, session) -> None:  # type: ignore[no-untyped-def]
        py_actor = PyActor(asset=9_999.0)
        db_actor = Actor.from_pydantic(py_actor)
        db_actor.actor_type = "actor"
        session.add(db_actor)
        session.flush()

        fetched = session.get(Actor, db_actor.id)
        assert fetched is not None
        result = fetched.to_pydantic()
        assert result.asset == 9_999.0


class TestExchangeActorFromPydantic:
    def test_asset_is_set(self) -> None:
        py_actor = PyExchangeActor(asset=1e10)
        db_actor = ExchangeActor.from_pydantic(py_actor)
        assert db_actor.asset == 1e10

    def test_polymorphic_identity_is_set(self) -> None:
        py_actor = PyExchangeActor(asset=1e10)
        db_actor = ExchangeActor.from_pydantic(py_actor)
        assert db_actor.actor_type == "exchange_actor"


class TestExchangeActorToPydantic:
    def test_returns_py_exchange_actor(self) -> None:
        db_actor = ExchangeActor(asset=1e10, actor_type="exchange_actor")
        result = db_actor.to_pydantic()
        assert isinstance(result, PyExchangeActor)

    def test_asset_matches(self) -> None:
        db_actor = ExchangeActor(asset=5e9, actor_type="exchange_actor")
        result = db_actor.to_pydantic()
        assert result.asset == 5e9


class TestExchangeActorRoundTrip:
    def test_round_trip_through_db(self, session) -> None:  # type: ignore[no-untyped-def]
        py_actor = PyExchangeActor(asset=1e10)
        session.add(ExchangeActor.from_pydantic(py_actor))
        session.flush()

        fetched = session.query(ExchangeActor).first()
        assert fetched is not None
        result = fetched.to_pydantic()
        assert isinstance(result, PyExchangeActor)
        assert result.asset == 1e10

    def test_polymorphic_identity_stored(self, session) -> None:  # type: ignore[no-untyped-def]
        # Single-table inheritance: actor_type discriminator is
        # "exchange_actor"
        session.add(ExchangeActor.from_pydantic(PyExchangeActor(asset=1.0)))
        session.flush()

        row = session.query(Actor).first()
        assert row is not None
        assert row.actor_type == "exchange_actor"
        assert isinstance(row, ExchangeActor)


class TestTraderActorFromPydantic:
    def test_asset_is_set(self) -> None:
        db_actor = TraderActor.from_pydantic(PyTraderActor(asset=50_000.0))
        assert db_actor.asset == 50_000.0

    def test_polymorphic_identity_is_set(self) -> None:
        db_actor = TraderActor.from_pydantic(PyTraderActor(asset=50_000.0))
        assert db_actor.actor_type == "trader_actor"


class TestTraderActorToPydantic:
    def test_returns_py_trader_actor(self) -> None:
        db_actor = TraderActor(asset=100.0, actor_type="trader_actor")
        assert isinstance(db_actor.to_pydantic(), PyTraderActor)

    def test_round_trip_through_db(self, session) -> None:  # type: ignore[no-untyped-def]
        session.add(TraderActor.from_pydantic(PyTraderActor(asset=1_234.0)))
        session.flush()

        fetched = session.query(TraderActor).first()
        assert fetched is not None
        result = fetched.to_pydantic()
        assert isinstance(result, PyTraderActor)
        assert result.asset == 1_234.0


class TestInvestorActorFromPydantic:
    def test_asset_is_set(self) -> None:
        db_actor = InvestorActor.from_pydantic(
            PyInvestorActor(asset=200_000.0)
        )
        assert db_actor.asset == 200_000.0

    def test_polymorphic_identity_is_set(self) -> None:
        db_actor = InvestorActor.from_pydantic(PyInvestorActor(asset=1.0))
        assert db_actor.actor_type == "investor_actor"


class TestInvestorActorToPydantic:
    def test_returns_py_investor_actor(self) -> None:
        db_actor = InvestorActor(asset=300.0, actor_type="investor_actor")
        assert isinstance(db_actor.to_pydantic(), PyInvestorActor)

    def test_round_trip_through_db(self, session) -> None:  # type: ignore[no-untyped-def]
        session.add(
            InvestorActor.from_pydantic(PyInvestorActor(asset=5_000.0))
        )
        session.flush()

        fetched = session.query(InvestorActor).first()
        assert fetched is not None
        result = fetched.to_pydantic()
        assert isinstance(result, PyInvestorActor)
        assert result.asset == 5_000.0


class TestActorPolymorphism:
    def test_all_subtypes_stored_in_single_table(self, session) -> None:  # type: ignore[no-untyped-def]
        # All actor variants share the same table (single-table inheritance)
        session.add_all(
            [
                ExchangeActor.from_pydantic(PyExchangeActor(asset=1.0)),
                TraderActor.from_pydantic(PyTraderActor(asset=2.0)),
                InvestorActor.from_pydantic(PyInvestorActor(asset=3.0)),
            ]
        )
        session.flush()

        all_actors = session.query(Actor).all()
        assert len(all_actors) == 3
        types = {type(a) for a in all_actors}
        assert ExchangeActor in types
        assert TraderActor in types
        assert InvestorActor in types

    def test_query_by_subtype_filters_correctly(self, session) -> None:  # type: ignore[no-untyped-def]
        session.add_all(
            [
                ExchangeActor.from_pydantic(PyExchangeActor(asset=10.0)),
                TraderActor.from_pydantic(PyTraderActor(asset=20.0)),
            ]
        )
        session.flush()

        exchange_actors = session.query(ExchangeActor).all()
        assert len(exchange_actors) == 1
        assert exchange_actors[0].actor_type == "exchange_actor"

        trader_actors = session.query(TraderActor).all()
        assert len(trader_actors) == 1
        assert trader_actors[0].actor_type == "trader_actor"
