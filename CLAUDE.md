# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Xarizmi (read Khwarizmi) is a Python library for technical analysis in financial markets. It provides tools for candlestick charting, technical indicators (OBV, etc.), fundamental analysis, Monte Carlo tools, portfolio management, and database persistence for market data.

## Commands

Tasks are namespaced under `code.*` via the `tasks/` package (invoke).

### Run tests
```bash
invoke code.test
# Single test file or by name (run pytest directly):
pytest -vv tests/test_candlestick.py
pytest -vv tests/ -k "test_name"
```

### Lint / format
```bash
invoke code.autoformat   # ruff format + ruff check --fix + black
invoke code.check        # check formatting without fixing (CI-safe)
invoke code.mypy         # mypy type checking
invoke code.ty           # ty type checking (faster alternative)
```

### CI (runs everything)
```bash
invoke code.ci           # autoformat → check → ty → mypy → complexity → test
```

### Coverage
```bash
invoke code.coverage          # pytest --cov + HTML report
invoke code.coverage-open     # same, then opens report in browser
invoke code.coverage-xml      # generates XML report
invoke code.coverage-score    # prints single coverage % to stdout
```

### Code quality extras
```bash
invoke code.complexity    # cyclomatic complexity via radon
invoke code.deadcode      # unused code via vulture
invoke code.docstrings    # docstring coverage via interrogate
invoke code.typecov       # type annotation coverage via mypy HTML report
invoke code.duplication   # copy-paste detection via pylint
invoke code.security      # bandit + pip-audit
invoke code.osv-scan      # OSV-Scanner on uv.lock
invoke code.licenses      # dependency license check via pip-licenses
```

### Docs
```bash
invoke code.docs          # build MkDocs site
invoke code.docs-serve    # serve docs locally with live reload
```

### Cleanup
```bash
invoke code.clean         # remove __pycache__, .mypy_cache, htmlcov, etc.
```

### Build & deploy
```bash
python setup.py sdist bdist_wheel
python -m twine upload dist/*
```

## Code Style

- **Formatter**: `ruff format` + `black` (run together via `invoke code.autoformat`)
- **Linter**: `ruff check` replaces flake8/isort/autoflake
- **mypy strict mode** with `pydantic.mypy` plugin; typings stubs in `typings/`
- `xarizmi/db/admin_tools/` is excluded from mypy

## Architecture

### Core data model
`xarizmi/candlestick.py` — Central module. `Candlestick` (Pydantic `BaseModel`) holds OHLCV data plus optional `symbol`, `datetime`, `exchange`. `CandlestickChart` wraps a list of `Candlestick` and provides analysis methods (support/resistance detection, plotting via `mplfinance`). All models use `model_validate()` for construction from dicts.

### Package structure
- `xarizmi/candlestick.py` — `Candlestick`, `CandlestickChart`, `CandlestickList`
- `xarizmi/config.py` — Singleton `Config` object (accessed via `from xarizmi.config import config`). Holds `DOJINESS_THRESHOLD` and `DATABASE_URL`. DB URL defaults to `postgresql://postgres:1@localhost/xarizmi`. Use `reset_config()` in tests.
- `xarizmi/enums.py` — `IntervalTypeEnum` (e.g. `"1day"`, `"1month"`), `SideEnum`, `OrderStatusEnum`
- `xarizmi/models/` — Pydantic models: `Symbol`, `Currency`, `Exchange`, `Portfolio`, `Orders`, `Actors`
- `xarizmi/ta/` — Technical indicators; currently `obv.py` (`OBVIndicator` wraps TA-Lib's OBV via `talib.abstract`)
- `xarizmi/db/` — SQLAlchemy ORM layer: `models/` (DB schema), `actions/` (CRUD), `mappers/` (ORM↔Pydantic), `client.py` (session context manager), `alembic/` (migrations)
- `xarizmi/opendata/` — Data clients; `yahoo_finance.py` (`YahooFinanceDailyDataClient`) downloads via `yfinance` and returns `CandlestickChart`
- `xarizmi/mctools/` — Monte Carlo / random candlestick generators
- `xarizmi/fundamentals/` — Fundamental analysis models (`Fundamentals`, DCF, IRR, time value of money, cash flow)
- `xarizmi/utils/` — `extremums.py` (local min/max detection), `math.py`, `numbers.py`, `datetools.py`, `plot/` (matplotlib wrappers)

### Symbol model
`Symbol` has `base_currency`, `quote_currency`, `fee_currency` (all `Currency` models with a `.name` string field) and optional `exchange`. Use `Symbol.build(base_currency="BTC", quote_currency="USDT", fee_currency="USDT")` as the factory.

### DB layer
Config must be updated before using DB: `config.DATABASE_URL = "postgresql://..."`. The `session_scope()` context manager in `xarizmi/db/client.py` handles commit/rollback. Alembic migrations live in `xarizmi/db/alembic/`.

### Indicator pattern
Indicators take a `CandlestickChart`, call `.compute()` to populate `indicator_data: list[float]`, then optionally `.plot()`. They rely on TA-Lib (`talib.abstract`), which requires native installation (use conda if pip fails: `conda install -c conda-forge ta-lib`).

### Tests
`tests/conftest.py` provides a `btc_usdt_monthly_data` session-scoped fixture (raw list of dicts). Tests use `CandlestickChart.model_validate({"candles": btc_usdt_monthly_data})` to build charts.
