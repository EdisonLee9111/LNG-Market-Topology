"""
Shadow Price Engine — Quantifies implied cost of hidden constraints.

Dual-mode:
- Route Deviation Mode (First Pass): cost(actual) - cost(optimal)
- Price Premium Mode (Second Pass): (spot - contract_baseline) * volume
"""
