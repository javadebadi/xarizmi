# Xarizmi
Xarizmi (read Khwarizmi) project is an educational project that contains tools for technical analysis in Python.


## Installation
```bash
pip install xarizmi
```
If you encounter error in installation use Anaconda and then install ta-lib using:
`bash
conda install -c conda-forge ta-lib
`
and then install other packages.

## Example

### Build Candlestick
```python
from xarizmi.candlestick import Candlestick
c = Candlestick(
    **{
        "open": 2,
        "low": 1,
        "high": 4,
        "close": 3,
    }
)
```


### Portfolio Rebalancing

```python
import datetime
from xarizmi.models.portfolio import Portfolio, PortfolioItem
from xarizmi.models.rebalance import (
    PortfolioAllocation, PortfolioAllocationItem, rebalance
)
from xarizmi.models.symbol import Symbol

now = datetime.datetime(2024, 11, 26)
btc = Symbol.build("BTC", "USD", "USD", "BINANCE")
eth = Symbol.build("ETH", "USD", "USD", "BINANCE")
sol = Symbol.build("SOL", "USD", "USD", "BINANCE")

# Current holdings
portfolio = Portfolio(items=[
    PortfolioItem(symbol=btc, market_value=90_000, quantity=0.9,  datetime=now),
    PortfolioItem(symbol=eth, market_value=30_000, quantity=10.0, datetime=now),
    PortfolioItem(symbol=sol, market_value=10_000, quantity=62.5, datetime=now),
])

# Desired allocation
target = PortfolioAllocation(items=[
    PortfolioAllocationItem(symbol=btc, weight=0.50),
    PortfolioAllocationItem(symbol=eth, weight=0.30),
    PortfolioAllocationItem(symbol=sol, weight=0.20),
])

result = rebalance(portfolio, target)

for item in result.to_sell():
    print(f"SELL {item.symbol.to_string()}: ${-item.delta_market_value:,.0f}")
# SELL BTC-USD: $25,000

for item in result.to_buy():
    print(f"BUY  {item.symbol.to_string()}: ${item.delta_market_value:,.0f}")
# BUY  ETH-USD: $9,000
# BUY  SOL-USD: $16,000
```

See [`examples/rebalance.py`](examples/rebalance.py) for the full runnable script.

### Indicators
### OBV Indicator
```python
from xarizmi.candlestick import CandlestickChart
from xarizmi.ta.obv import OBVIndicator

# assuming btc_usdt_monthly_data is defined (similar to tests/conftest.py)
c = CandlestickChart.model_validate({"candles": btc_usdt_monthly_data})

obv_indicator = OBVIndicator(candlestick_chart=c, volume='amount')
obv_indicator.compute()
print(obv_indicator.indicator_data)
obv_indicator.plot()
```


