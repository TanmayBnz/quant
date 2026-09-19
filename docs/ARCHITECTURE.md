# Architecture

## Design principles

- **Make time explicit.** Strategies produce targets from information available at a
  close; the engine delays those targets before applying returns.
- **Keep research reproducible.** Synthetic data and fixed seeds make the default demo
  independent of third-party APIs.
- **Separate decisions from accounting.** Strategies decide desired exposure; the
  backtester owns returns, turnover, costs, and equity.
- **Earn abstractions.** The first engine is deliberately single-asset. Multi-asset
  accounting will be added when the factor lab supplies concrete requirements.
- **Treat the UI as a client.** Financial calculations live in `quant_core`, not inside
  Streamlit scripts.
- **Keep strategies outside the engine.** Trusted files in `strategies/` implement one
  small contract and are discovered dynamically. Their dataclass metadata drives the UI.
- **Isolate batch failures.** One bad symbol should not erase valid results for the rest
  of a multi-ticker experiment.

## Current data flow

```text
strategies/*.py ──discovery──► selected strategy + parameter metadata
                                      │
ticker list ──data adapter──► {ticker: price frame}
                                      │
                       independent batch runs
                                      │
                     strategy.generate_targets()
                                      │ targets observed at each close
                                      ▼
                           one-row execution delay
                                      │ held position
                                      ▼
                    asset return × position − turnover costs
                                      │
                         ┌────────────┴────────────┐
                         ▼                         ▼
              per-ticker detail         cross-ticker comparison
```

## Known simplifications

- One asset per individual run and one close price per bar; batch mode compares runs but
  does not yet construct a combined multi-asset portfolio
- Fractional exposure from -1 to +1
- No dividends, borrow fees, financing costs, taxes, or corporate actions
- Linear cost model and unlimited liquidity
- No intraday orders or partial fills

These constraints are public and tested where possible. Later milestones should
replace them one at a time rather than silently implying market realism.
