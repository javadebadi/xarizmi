from pydantic import BaseModel, field_validator, model_validator

from xarizmi.utils.math import divide_with_no_zero_division_error

from .portfolio import Portfolio
from .symbol import Symbol


class PortfolioAllocationItem(BaseModel):
    symbol: Symbol
    weight: float  # fraction of total portfolio value, 0.0–1.0

    @field_validator("weight")
    @classmethod
    def weight_must_be_non_negative(cls, v: float) -> float:
        if v < 0:
            raise ValueError(f"weight must be >= 0, got {v}")
        return v


class PortfolioAllocation(BaseModel):
    items: list[PortfolioAllocationItem]

    @model_validator(mode="after")
    def validate_allocation(self) -> "PortfolioAllocation":
        if not self.items:
            raise ValueError("PortfolioAllocation cannot be empty")
        total = sum(item.weight for item in self.items)
        if abs(total - 1.0) > 1e-9:
            raise ValueError(f"Weights must sum to 1.0, got {total:.10f}")
        return self

    def __getitem__(self, symbol: Symbol) -> float:
        """Return target weight for symbol; 0.0 if not in allocation."""
        items = [i for i in self.items if i.symbol == symbol]
        return items[0].weight if items else 0.0


class RebalanceItem(BaseModel):
    symbol: Symbol
    current_weight: float
    target_weight: float
    current_market_value: float
    target_market_value: float
    delta_market_value: float  # positive → buy, negative → sell


class RebalanceResult(BaseModel):
    items: list[RebalanceItem]
    total_value: float

    def to_buy(self) -> list[RebalanceItem]:
        """Items where market value must increase (buy)."""
        return [i for i in self.items if i.delta_market_value > 0]

    def to_sell(self) -> list[RebalanceItem]:
        """Items where market value must decrease (sell)."""
        return [i for i in self.items if i.delta_market_value < 0]

    def __getitem__(self, symbol: Symbol) -> RebalanceItem:
        items = [i for i in self.items if i.symbol == symbol]
        if items:
            return items[0]
        return RebalanceItem(
            symbol=symbol,
            current_weight=0.0,
            target_weight=0.0,
            current_market_value=0.0,
            target_market_value=0.0,
            delta_market_value=0.0,
        )


def rebalance(
    portfolio: Portfolio, target: PortfolioAllocation
) -> RebalanceResult:
    """Return what to buy/sell to move portfolio toward target allocation.

    Parameters
    ----------
    portfolio:
        Current holdings snapshot. All items must share the same datetime.
    target:
        Desired weight per symbol as a fraction of total portfolio value.
        Weights must sum to exactly 1.0.
        Symbols not listed in ``target`` are treated as 0% weight (full sell).

    Returns
    -------
    RebalanceResult
        Per-symbol ``delta_market_value``:
        - positive → buy (underweight)
        - negative → sell (overweight)

    Example
    -------
    >>> import datetime
    >>> from xarizmi.models.portfolio import Portfolio, PortfolioItem
    >>> from xarizmi.models.rebalance import (
    ...     PortfolioAllocation, PortfolioAllocationItem, rebalance
    ... )
    >>> from xarizmi.models.symbol import Symbol
    >>>
    >>> now = datetime.datetime(2024, 11, 26)
    >>> btc = Symbol.build("BTC", "USD", "USD", "BINANCE")
    >>> eth = Symbol.build("ETH", "USD", "USD", "BINANCE")
    >>>
    >>> portfolio = Portfolio(items=[
    ...     PortfolioItem(
    ...         symbol=btc,
    ...         market_value=80_000,
    ...         quantity=1,
    ...         datetime=now,
    ...        ),
    ...     PortfolioItem(
    ...         symbol=eth,
    ...         market_value=20_000,
    ...         quantity=6,
    ...         datetime=now,
    ...     ),
    ... ])
    >>>
    >>> target = PortfolioAllocation(items=[
    ...     PortfolioAllocationItem(symbol=btc, weight=0.5),
    ...     PortfolioAllocationItem(symbol=eth, weight=0.5),
    ... ])
    >>>
    >>> result = rebalance(portfolio, target)
    >>> for item in result.to_sell():
    ...     print(
    ...     f"SELL {item.symbol.to_string()}: ${-item.delta_market_value:,.0f}"
    ...     )
    SELL BTC-USD: $30,000
    >>> for item in result.to_buy():
    ...     print(
    ...     f"BUY  {item.symbol.to_string()}: ${item.delta_market_value:,.0f}"
    ...     )
    BUY  ETH-USD: $30,000
    """
    total_value = sum(item.market_value for item in portfolio.items)

    all_symbols = set(
        [item.symbol for item in portfolio.items]
        + [item.symbol for item in target.items]
    )

    items = []
    for symbol in all_symbols:
        current_mv = portfolio[symbol].market_value
        current_weight = divide_with_no_zero_division_error(
            current_mv, total_value
        )
        target_weight = target[symbol]
        target_mv = total_value * target_weight
        delta_mv = target_mv - current_mv
        items.append(
            RebalanceItem(
                symbol=symbol,
                current_weight=current_weight,
                target_weight=target_weight,
                current_market_value=current_mv,
                target_market_value=target_mv,
                delta_market_value=delta_mv,
            )
        )

    return RebalanceResult(items=items, total_value=total_value)
