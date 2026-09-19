"""A buy-and-hold control strategy."""

from dataclasses import dataclass
from typing import ClassVar

import pandas as pd

from quant_core.data import validate_prices
from quant_core.strategies import Strategy


@dataclass(frozen=True)
class BuyAndHold(Strategy):
    strategy_id: ClassVar[str] = "buy_and_hold"
    display_name: ClassVar[str] = "Buy and hold"
    description: ClassVar[str] = "Always long; useful as an engine and cost-model control."

    def generate_targets(self, prices: pd.DataFrame) -> pd.Series:
        clean_prices = validate_prices(prices)
        return pd.Series(1.0, index=clean_prices.index, name="target")
