# Quant portfolio interview review

These notes explain the decisions implemented—or deliberately deferred—in this
repository. They are written for active recall before interviews, not as a textbook.

## Current backtester

1. [Backtesting fundamentals](01-backtesting-fundamentals.md)
2. [Returns and portfolio accounting](02-returns-and-accounting.md)
3. [Biases and validation](03-biases-and-validation.md)
4. [Risk and performance metrics](04-risk-and-performance.md)
5. [Costs and execution](05-costs-and-execution.md)
6. [Strategy plug-in architecture](06-strategy-plugin-architecture.md)

## Upcoming projects

7. [Factor research and portfolio construction](07-factor-research.md)
8. [Paper trading and production risk](08-paper-trading.md)

## Fast preparation

- [Interview drill](INTERVIEW-DRILL.md)
- Read the implementation beside the notes: `src/quant_core/`, `strategies/`, and
  `tests/` are intentionally small enough to discuss line by line.

Each note distinguishes **implemented now** from **planned** so the resume never implies
features that do not exist.
