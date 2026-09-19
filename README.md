# Quant Portfolio

A small end-to-end quantitative research platform built as three connected projects:

1. **Backtesting engine** — bias-aware signal execution, portfolio accounting, costs,
   benchmarks, risk metrics, and an interactive strategy explorer.
2. **Factor research lab** — cross-sectional factor testing, portfolio construction,
   walk-forward validation, and tear sheets.
3. **Paper-trading risk monitor** — scheduled signals, simulated execution, persistent
   state, P&L attribution, and operational health checks.

The repository intentionally starts small. Correct timing, reproducible experiments,
and clear assumptions matter more than a large feature list.

## Current milestone

Milestone 1 provides:

- A reusable `quant_core` package
- A trusted local strategy plug-in folder with automatic discovery
- Buy-and-hold, moving-average, and RSI mean-reversion examples
- Independent batch tests across multiple ticker symbols
- Deterministic sample data and optional Yahoo Finance adjusted closes
- A single-asset backtest with commissions and slippage
- Equity, benchmark, turnover, and drawdown series
- CAGR, volatility, Sharpe, Sortino, max drawdown, and exposure metrics
- Deterministic synthetic data for offline demos and tests
- A working Streamlit backtester
- Skeleton applications for factor research and paper-trading risk

The original prototype remains at `backtester/backtester.py` as a learning reference.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
streamlit run apps/backtester/app.py
```

The default demo does not download market data. It generates deterministic synthetic
prices for several ticker labels, so it works offline and produces reproducible results.
Switch the dashboard to Yahoo Finance to test real adjusted daily histories.

## Add a strategy

Copy `strategies/_template.py` to a public Python filename, then implement its
`generate_targets` method. The dashboard discovers it automatically and creates controls
for fields declared with `strategy_parameter(...)`; neither the engine nor the app needs
a manual registry update. See [`strategies/README.md`](strategies/README.md) for the full
contract.

## Accounting convention

A strategy observes closing prices through date `t`. Its target is shifted by one row,
so the new position earns the close-to-close return ending on `t + 1`. Trading cost is
charged when exposure changes. This convention prevents a signal from using today's
close and also earning today's return.

This is a research model, not an exchange simulator. It currently assumes fractional
positions, unlimited liquidity, and one close-to-close fill per day.

## Applications

```bash
streamlit run apps/backtester/app.py
streamlit run apps/factor_lab/app.py
streamlit run apps/risk_monitor/app.py
```

See [the roadmap](docs/ROADMAP.md) and [architecture notes](docs/ARCHITECTURE.md) for
the planned progression. The interview-oriented explanations live in
[`learning/`](learning/README.md).

The repository is the source of truth for those learning notes. To refresh the Obsidian
inventory without creating new top-level vault folders, run:

```bash
./scripts/sync_learning_notes.sh /home/tanbnz/Documents/notes/resume
```

The script writes topic notes directly into the vault's existing `Skills/` folder and
the spoken interview drill directly into its existing `Projects/` folder.

## Disclaimer

This project is for education and research. It is not investment advice and must not
be used to place real trades without independent validation and appropriate controls.
