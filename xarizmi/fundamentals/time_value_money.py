"""A module to calculate time value of money
"""


def time_value_money(
    impatience_to_consume: float,
    inflation: float,
    risk: float,
) -> float:
    """Calculates time value of money.

    Parameters
    ----------
    impatience_to_consume : float
        Impatience to consume is the rate of exchange between future
        consumption and curent consumption. The other name for this in
        finance is "pure rate of interest".
        For example, a person might have 2 percent (0.02) Impatience to
        consume which means that he or she expects 2 percent reward in order
        to not consume and invest instead.

    inflation : float
        The inflation as defined in ecomony which is general progressive
        increase in prices of goods and services in an economy.

    risk : float
        The amount of risk which exists in an investement.


    Returns
    -------
    float
        Returns the time value of money.


    Example
    -------
    >>> round(time_value_money(0.02,0.03,0),4)
    0.0506

    """
    return (1 + impatience_to_consume) * (1 + inflation) * (1 + risk) - 1


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
