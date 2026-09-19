# Writing a strategy

The dashboard discovers every `Strategy` subclass in public `.py` files in this folder.
No engine or app registry needs editing.

1. Copy `_template.py` to a new filename without a leading underscore.
2. Give the class a unique `strategy_id`, a display name, and a one-sentence hypothesis.
3. Add dataclass fields with `strategy_parameter(...)`; the dashboard creates their
   controls automatically.
4. Implement `generate_targets(prices)` and return a `pandas.Series` indexed exactly
   like `prices`, with every value between `-1` and `1`.
5. Add deterministic unit tests for the signal logic.

## Timing contract

`generate_targets` receives data through the current close and returns the exposure it
wants next. The engine shifts the target by one row before applying returns. Do not shift
again inside a strategy or it will trade one day later than intended.

## Target meaning

- `1.0`: fully long
- `0.0`: cash
- `-1.0`: fully short
- Values in between: fractional exposure

Strategy files are imported as executable Python. Only place trusted local code here.
