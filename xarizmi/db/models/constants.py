from enum import StrEnum


class TableNamesEnum(StrEnum):
    EXCHANGE = "xarizmi_exchange"
    CURRENCY = "xarizmi_currency"
    PORTFOLIO = "xarizmi_portfolio"
    PORTFOLIO_ITEM = "xarizmi_portfolio_item"
    SYMBOL = "xarizmi_symbol"
    CANDLESTICK = "xarizmi_candlestick"
    ORDER = "xarizmi_order"
    ACTOR = "xarizmi_actor"
    PORTFOLIO_ALLOCATION = "xarizmi_portfolio_allocation"
    PORTFOLIO_ALLOCATION_ITEM = "xarizmi_portfolio_allocation_item"
    REBALANCE_RESULT = "xarizmi_rebalance_result"
    REBALANCE_ITEM = "xarizmi_rebalance_item"
