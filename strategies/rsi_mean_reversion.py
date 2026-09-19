"""A simple RSI threshold strategy for studying mean reversion."""

from dataclasses import dataclass
from typing import ClassVar

import pandas as pd

from quant_core.data import validate_prices
from quant_core.strategies import Strategy, strategy_parameter


@dataclass(frozen=True)
class RsiMeanReversion(Strategy):
    strategy_id: ClassVar[str] = "rsi_mean_reversion"
    display_name: ClassVar[str] = "RSI mean reversion"
    description: ClassVar[str] = "Long oversold observations and short overbought observations."

    lookback: int = strategy_parameter(
        14,
        label="RSI lookback",
        min_value=2,
        max_value=100,
        step=1,
    )
    lower_threshold: float = strategy_parameter(
        30.0,
        label="Oversold threshold",
        min_value=1.0,
        max_value=49.0,
        step=1.0,
    )
    upper_threshold: float = strategy_parameter(
        70.0,
        label="Overbought threshold",
        min_value=51.0,
        max_value=99.0,
        step=1.0,
    )

    def __post_init__(self) -> None:
        if self.lower_threshold >= self.upper_threshold:
            raise ValueError("lower_threshold must be below upper_threshold")

    def generate_targets(self, prices: pd.DataFrame) -> pd.Series:
        clean_prices = validate_prices(prices)
        change = clean_prices["close"].diff()
        average_gain = change.clip(lower=0).rolling(self.lookback).mean()
        average_loss = -change.clip(upper=0).rolling(self.lookback).mean()
        relative_strength = average_gain / average_loss
        rsi = 100 - (100 / (1 + relative_strength))
        rsi = rsi.mask((average_loss == 0) & (average_gain > 0), 100.0)
        rsi = rsi.mask((average_gain == 0) & (average_loss > 0), 0.0)
        rsi = rsi.mask((average_gain == 0) & (average_loss == 0), 50.0)

        target = pd.Series(0.0, index=clean_prices.index, name="target")
        target.loc[rsi < self.lower_threshold] = 1.0
        target.loc[rsi > self.upper_threshold] = -1.0
        return target
