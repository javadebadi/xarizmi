from sqlalchemy.orm import Session

from ..models import Exchange


def upsert_exchange(exchange_name: str, session: Session) -> Exchange:
    """Creates exchange in db or returns it if it already exists"""
    exchange = Exchange(name=exchange_name)
    session.merge(exchange)
    session.flush()
    return exchange


def bulk_upsert_exchanges(
    exchange_names: list[str], session: Session
) -> list[Exchange]:
    exchanges = [
        Exchange(name=exchange_name) for exchange_name in exchange_names
    ]
    for exchange in exchanges:
        session.merge(exchange)
        session.flush()
    return exchanges
