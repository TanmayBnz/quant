---
type: skill
category: backend
level: working
tracks: [quant, swe]
evidence: ["[[Strategy Backtesting Engine]]"]
keywords: [plugin architecture, Python dataclasses, dynamic imports, strategy pattern, metadata]
---
# Strategy plug-in architecture

## Separation of responsibilities

- `Strategy.generate_targets` expresses the market hypothesis.
- `quant_core.backtest` owns timing, positions, turnover, costs, and capital.
- `quant_core.strategy_loader` discovers trusted local strategy classes.
- Streamlit reads parameter metadata and generates controls.

This prevents each strategy from reimplementing accounting and makes comparisons use the
same assumptions.

## Why dataclasses

Dataclasses make parameters explicit, immutable, inspectable, and easy to construct from
UI values. `strategy_parameter(...)` attaches labels and numeric bounds as field metadata
without importing Streamlit into strategy code.

## Discovery

The loader imports each public `.py` file in `strategies/`, finds locally defined
subclasses of `Strategy`, validates their identifiers and dataclass parameters, and
rejects duplicates. Files beginning with `_` are ignored, so `_template.py` is safe to
copy from.

## Security boundary

Plug-ins are executable Python, not a sandboxed formula language. The folder must contain
trusted local code. Supporting arbitrary user-submitted Python on a public server would
require process isolation or a restricted strategy DSL.

## How to add one

1. Copy `strategies/_template.py`.
2. Choose a unique `strategy_id`.
3. Declare parameters with defaults and bounds.
4. Return an aligned target series in `[-1, 1]`.
5. Test warm-up behavior, timing, bounds, and edge cases.

## Design trade-off

Dynamic discovery improves extension and removes the app registry, but failures move to
runtime. Loader validation and tests compensate for that cost.
