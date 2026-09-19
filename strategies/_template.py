"""Copy this file to ``strategies/my_strategy.py`` and remove the leading underscore."""

from dataclasses import dataclass
from typing import ClassVar

import pandas as pd

from quant_core.data import validate_prices
from quant_core.strategies import Strategy, strategy_parameter


@dataclass(frozen=True)
class MyStrategy(Strategy):
    strategy_id: ClassVar[str] = "my_strategy"
    display_name: ClassVar[str] = "My strategy"
    description: ClassVar[str] = "Explain the market hypothesis in one sentence."

    lookback: int = strategy_parameter(
        20,
        label="Lookback",
        min_value=2,
        max_value=252,
        step=1,
        help="Number of trading days used by the signal.",
    )

    def generate_targets(self, prices: pd.DataFrame) -> pd.Series:
        clean_prices = validate_prices(prices)
        signal_input = clean_prices["close"].pct_change(self.lookback)

        target = pd.Series(0.0, index=clean_prices.index, name="target")
        target.loc[signal_input > 0] = 1.0
        target.loc[signal_input < 0] = -1.0
        return target
