"""Trend-following baseline using a fast and slow moving average."""

from dataclasses import dataclass
from typing import ClassVar

import pandas as pd

from quant_core.data import validate_prices
from quant_core.strategies import Strategy, strategy_parameter


@dataclass(frozen=True)
class MovingAverageCrossover(Strategy):
    strategy_id: ClassVar[str] = "moving_average"
    display_name: ClassVar[str] = "Moving-average crossover"
    description: ClassVar[str] = "Trend following: long above the slow average, short below it."

    fast_window: int = strategy_parameter(
        20,
        label="Fast window",
        min_value=2,
        max_value=100,
        step=1,
    )
    slow_window: int = strategy_parameter(
        60,
        label="Slow window",
        min_value=3,
        max_value=300,
        step=1,
    )

    def __post_init__(self) -> None:
        if self.slow_window <= self.fast_window:
            raise ValueError("slow_window must be greater than fast_window")

    def generate_targets(self, prices: pd.DataFrame) -> pd.Series:
        clean_prices = validate_prices(prices)
        fast = clean_prices["close"].rolling(self.fast_window).mean()
        slow = clean_prices["close"].rolling(self.slow_window).mean()
        target = pd.Series(0.0, index=clean_prices.index, name="target")
        target.loc[fast > slow] = 1.0
        target.loc[fast < slow] = -1.0
        return target
