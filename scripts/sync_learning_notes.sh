#!/usr/bin/env bash
set -euo pipefail

project_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
vault_root="${1:-/home/tanbnz/Documents/notes/resume}"

cp "$project_root/learning/01-backtesting-fundamentals.md" \
    "$vault_root/Skills/Backtesting Fundamentals.md"
cp "$project_root/learning/02-returns-and-accounting.md" \
    "$vault_root/Skills/Returns and Portfolio Accounting.md"
cp "$project_root/learning/03-biases-and-validation.md" \
    "$vault_root/Skills/Backtest Biases and Validation.md"
cp "$project_root/learning/04-risk-and-performance.md" \
    "$vault_root/Skills/Risk and Performance Metrics.md"
cp "$project_root/learning/05-costs-and-execution.md" \
    "$vault_root/Skills/Trading Costs and Execution.md"
cp "$project_root/learning/06-strategy-plugin-architecture.md" \
    "$vault_root/Skills/Strategy Plugin Architecture.md"
cp "$project_root/learning/07-factor-research.md" \
    "$vault_root/Skills/Factor Research.md"
cp "$project_root/learning/08-paper-trading.md" \
    "$vault_root/Skills/Paper Trading Systems.md"
cp "$project_root/learning/INTERVIEW-DRILL.md" \
    "$vault_root/Projects/Quant Portfolio Interview Drill.md"

echo "Synced quant notes into the vault's existing Projects and Skills folders"
