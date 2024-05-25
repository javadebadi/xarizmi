import numpy as np

from xarizmi.candlestick import Candlestick


def generate_random_candlestick() -> Candlestick:
    nums = np.random.random(4)
    nums.sort()
    return Candlestick(
        close=nums[2],
        open=nums[1],
        low=nums[0],
        high=nums[4],
    )
