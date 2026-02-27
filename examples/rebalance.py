"""Portfolio rebalancing example.

Scenario
--------
You hold three crypto assets but your allocation has drifted far from your
target.  The rebalance() function tells you exactly what to buy and sell
(in USD market value) to restore the target weights.

Current portfolio (total ~$130,000):
  BTC  $90,000  (69%)   target → 50%   → overweight, sell
  ETH  $30,000  (23%)   target → 30%   → slightly underweight, buy
  SOL  $10,000   (8%)   target → 20%   → underweight, buy

Run
---
    uv run example_rebalance.py
"""

import datetime

from xarizmi.models.portfolio import Portfolio, PortfolioItem
from xarizmi.models.rebalance import (
    PortfolioAllocation,
    PortfolioAllocationItem,
    rebalance,
)
from xarizmi.models.symbol import Symbol

# ── 1. Build the current portfolio snapshot ───────────────────────────────────

now = datetime.datetime(2024, 11, 26)

btc = Symbol.build(base_currency="BTC", quote_currency="USD",
                   fee_currency="USD", exchange="BINANCE")
eth = Symbol.build(base_currency="ETH", quote_currency="USD",
                   fee_currency="USD", exchange="BINANCE")
sol = Symbol.build(base_currency="SOL", quote_currency="USD",
                   fee_currency="USD", exchange="BINANCE")

portfolio = Portfolio(
    items=[
        PortfolioItem(symbol=btc, market_value=90_000, quantity=0.9,  datetime=now),
        PortfolioItem(symbol=eth, market_value=30_000, quantity=10.0, datetime=now),
        PortfolioItem(symbol=sol, market_value=10_000, quantity=62.5, datetime=now),
    ]
)

# ── 2. Define target weights (must sum to 1.0) ────────────────────────────────

target = PortfolioAllocation(
    items=[
        PortfolioAllocationItem(symbol=btc, weight=0.50),
        PortfolioAllocationItem(symbol=eth, weight=0.30),
        PortfolioAllocationItem(symbol=sol, weight=0.20),
    ]
)

# ── 3. Compute rebalancing actions ────────────────────────────────────────────

result = rebalance(portfolio, target)

# ── 4. Print report ───────────────────────────────────────────────────────────

print(f"Total portfolio value: ${result.total_value:>12,.0f}")
print()

header = f"{'Symbol':<10} {'Current':>12} {'Current%':>9} {'Target%':>8} {'Delta':>12} {'Action'}"
print(header)
print("-" * len(header))

for item in sorted(result.items, key=lambda i: i.symbol.to_string()):
    action = ""
    if item.delta_market_value > 1:
        action = "BUY"
    elif item.delta_market_value < -1:
        action = "SELL"
    else:
        action = "HOLD"

    print(
        f"{item.symbol.to_string():<10}"
        f" ${item.current_market_value:>11,.0f}"
        f" {item.current_weight * 100:>8.1f}%"
        f" {item.target_weight * 100:>7.1f}%"
        f" {item.delta_market_value:>+12,.0f}"
        f"  {action}"
    )

print()
print("── Orders ───────────────────────────────────")
for item in result.to_sell():
    print(f"  SELL {item.symbol.to_string():<8}  ${-item.delta_market_value:>10,.0f}")
for item in result.to_buy():
    print(f"  BUY  {item.symbol.to_string():<8}  ${item.delta_market_value:>10,.0f}")
