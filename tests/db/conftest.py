import datetime
from collections.abc import Iterator

import pytest
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

from xarizmi.db.models import Base
from xarizmi.db.models.exchange import Exchange
from xarizmi.db.models.symbol import Symbol


@pytest.fixture
def engine() -> Iterator[Engine]:
    eng = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(eng)
    yield eng
    eng.dispose()


@pytest.fixture
def session(engine: Engine) -> Iterator[Session]:
    with Session(engine) as sess:
        yield sess


@pytest.fixture
def db_exchange(session: Session) -> Exchange:
    exc = Exchange(name="BINANCE")
    session.add(exc)
    session.flush()
    return exc


@pytest.fixture
def db_symbol(session: Session, db_exchange: Exchange) -> Symbol:
    sym = Symbol(
        base_currency="BTC",
        quote_currency="USD",
        fee_currency="USD",
        exchange_name=db_exchange.name,
    )
    session.add(sym)
    session.flush()
    session.refresh(sym)
    return sym


@pytest.fixture
def db_eth_symbol(session: Session, db_exchange: Exchange) -> Symbol:
    sym = Symbol(
        base_currency="ETH",
        quote_currency="USD",
        fee_currency="USD",
        exchange_name=db_exchange.name,
    )
    session.add(sym)
    session.flush()
    session.refresh(sym)
    return sym


@pytest.fixture
def snapshot_dt() -> datetime.datetime:
    return datetime.datetime(2024, 11, 26, 12, 0, 0)
