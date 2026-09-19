"""Interactive multi-ticker front end for the backtesting engine."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from quant_core import (
    BacktestConfig,
    download_yfinance_prices,
    generate_sample_universe,
    run_batch_backtest,
)
from quant_core.strategies import StrategyParameter, strategy_parameters
from quant_core.strategy_loader import discover_strategy_classes

PROJECT_ROOT = Path(__file__).resolve().parents[2]
STRATEGY_DIRECTORY = PROJECT_ROOT / "strategies"
POPULAR_TICKERS = ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "SPY", "QQQ"]


@st.cache_data(ttl="6h", max_entries=24, show_spinner=False)
def load_market_data(tickers: tuple[str, ...], period: str):
    return download_yfinance_prices(tickers, period=period)


@st.cache_data(max_entries=48, show_spinner=False)
def load_sample_data(tickers: tuple[str, ...], periods: int, seed: int):
    return generate_sample_universe(tickers, periods=periods, seed=seed)


def render_parameter_widget(parameter: StrategyParameter, strategy_id: str):
    key = f"strategy_{strategy_id}_{parameter.name}"
    if parameter.value_type is bool:
        return st.toggle(parameter.label, value=parameter.default, key=key, help=parameter.help)
    if parameter.value_type in (int, float):
        return st.number_input(
            parameter.label,
            min_value=parameter.min_value,
            max_value=parameter.max_value,
            value=parameter.default,
            step=parameter.step,
            key=key,
            help=parameter.help,
        )
    return st.text_input(
        parameter.label,
        value=str(parameter.default),
        key=key,
        help=parameter.help,
    )


st.set_page_config(
    page_title="Quant backtester",
    page_icon=":material/candlestick_chart:",
    layout="wide",
)
st.title("Multi-ticker strategy backtester")
st.caption(
    "Compare one transparent strategy across several instruments with delayed execution "
    "and explicit trading costs."
)

strategy_classes = discover_strategy_classes(STRATEGY_DIRECTORY)

with st.sidebar:
    st.header("Experiment")
    data_source = st.segmented_control(
        "Data source",
        ["Synthetic", "Yahoo Finance"],
        default="Synthetic",
        key="data_source",
    )
    selected_tickers = st.multiselect(
        "Tickers",
        POPULAR_TICKERS,
        default=["AAPL", "MSFT", "NVDA"],
        accept_new_options=True,
        max_selections=12,
        select_all=False,
        placeholder="Choose or type ticker symbols",
        key="tickers",
        help="Each ticker is tested independently with the same strategy and costs.",
    )

    if data_source == "Yahoo Finance":
        market_period = st.selectbox(
            "History",
            ["1y", "2y", "5y", "10y", "max"],
            index=2,
            key="market_period",
        )
        periods = 0
        seed = 0
    else:
        periods = st.slider("Business days", 252, 2_500, 756, 21, key="sample_periods")
        seed = int(st.number_input("Synthetic-data seed", min_value=0, value=7, step=1, key="seed"))
        market_period = ""

    st.divider()
    strategy_id = st.selectbox(
        "Strategy",
        list(strategy_classes),
        format_func=lambda item: strategy_classes[item].display_name,
        key="strategy_id",
    )
    strategy_type = strategy_classes[strategy_id]
    st.caption(strategy_type.description)
    parameter_values = {
        parameter.name: render_parameter_widget(parameter, strategy_id)
        for parameter in strategy_parameters(strategy_type)
    }

    st.divider()
    commission = st.number_input("Commission (bps)", 0.0, 50.0, 1.0, 0.5, key="commission")
    slippage = st.number_input("Slippage (bps)", 0.0, 50.0, 2.0, 0.5, key="slippage")

if not selected_tickers:
    st.warning("Select at least one ticker to run the experiment.")
    st.stop()

tickers = tuple(
    dict.fromkeys(ticker.strip().upper() for ticker in selected_tickers if ticker.strip())
)

try:
    strategy = strategy_type(**parameter_values)
except (TypeError, ValueError) as exc:
    st.error(f"Invalid strategy configuration: {exc}")
    st.stop()

config = BacktestConfig(commission_bps=commission, slippage_bps=slippage)

if data_source == "Yahoo Finance":
    data_slot = st.container()
    with data_slot.skeleton():
        loaded = load_market_data(tickers, market_period)
    prices_by_ticker = loaded.prices
    data_errors = loaded.errors
else:
    prices_by_ticker = load_sample_data(tickers, periods, seed)
    data_errors = {}

if data_errors:
    with st.expander(
        f"Data unavailable for {len(data_errors)} ticker(s)", icon=":material/warning:"
    ):
        for ticker, message in data_errors.items():
            st.markdown(f"- **{ticker}:** {message}")

if not prices_by_ticker:
    st.error("No usable price histories were returned.")
    st.stop()

batch = run_batch_backtest(prices_by_ticker, strategy, config)
if batch.failures:
    with st.expander(f"Backtest failed for {len(batch.failures)} ticker(s)"):
        for ticker, message in batch.failures.items():
            st.markdown(f"- **{ticker}:** {message}")

if not batch.results:
    st.error("Every backtest failed. Review the strategy parameters and price histories.")
    st.stop()

summary = batch.comparison_frame()
st.subheader("Cross-ticker comparison")
st.dataframe(
    summary.reset_index(),
    hide_index=True,
    column_config={
        "ticker": st.column_config.TextColumn("Ticker", pinned=True),
        "total_return": st.column_config.NumberColumn("Strategy return", format="percent"),
        "benchmark_return": st.column_config.NumberColumn("Buy-and-hold", format="percent"),
        "excess_return": st.column_config.NumberColumn("Excess return", format="percent"),
        "annualized_return": st.column_config.NumberColumn("CAGR", format="percent"),
        "annualized_volatility": st.column_config.NumberColumn("Volatility", format="percent"),
        "sharpe_ratio": st.column_config.NumberColumn("Sharpe", format="%.2f"),
        "sortino_ratio": st.column_config.NumberColumn("Sortino", format="%.2f"),
        "max_drawdown": st.column_config.NumberColumn("Max drawdown", format="percent"),
        "average_abs_exposure": st.column_config.NumberColumn("Avg. exposure", format="percent"),
        "total_turnover": st.column_config.NumberColumn("Turnover", format="%.1f×"),
        "observations": st.column_config.NumberColumn("Rows", format="%d"),
    },
    width="stretch",
    key="comparison_table",
)

normalized_equity = pd.concat(
    {
        ticker: result.history["equity"] / config.initial_capital
        for ticker, result in batch.results.items()
    },
    axis=1,
)
with st.container(border=True):
    st.subheader("Strategy growth by ticker")
    st.line_chart(normalized_equity, y_label="Growth of $1")

selected_ticker = st.selectbox(
    "Inspect ticker",
    list(batch.results),
    key="inspected_ticker",
)
result = batch.results[selected_ticker]
metrics = result.metrics

with st.container(horizontal=True):
    st.metric(
        "Total return",
        metrics["total_return"],
        format="percent",
        border=True,
        icon=":material/trending_up:",
    )
    st.metric("CAGR", metrics["annualized_return"], format="percent", border=True)
    st.metric("Sharpe", metrics["sharpe_ratio"], format="%.2f", border=True)
    st.metric(
        "Max drawdown",
        metrics["max_drawdown"],
        format="percent",
        border=True,
        icon=":material/trending_down:",
    )
    st.metric("Turnover", f"{metrics['total_turnover']:.1f}×", border=True)

left, right = st.columns(2)
with left:
    with st.container(border=True):
        st.subheader(f"{selected_ticker}: strategy vs. benchmark")
        st.line_chart(result.history[["equity", "benchmark_equity"]], y_label="Portfolio value")
with right:
    with st.container(border=True):
        st.subheader("Position and drawdown")
        st.line_chart(result.history[["position", "drawdown"]])

with st.expander("Inspect backtest history"):
    st.dataframe(result.history.tail(250), width="stretch", key="backtest_history")

st.info(
    "A target observed at today's close is shifted before it earns returns. Strategy files "
    "belong in `strategies/`; adding one does not require changing this dashboard."
)
