from xarizmi.candlestick import Candlestick
from xarizmi.mctools.candlestick import generate_random_candlestick


class TestCandlestickRandomGenerator:

    def test_generate_random_candlestick(self) -> None:
        candlestick = generate_random_candlestick()
        assert isinstance(candlestick, Candlestick)
