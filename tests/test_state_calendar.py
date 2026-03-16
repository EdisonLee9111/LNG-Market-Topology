"""Tests for state_calendar.py — institutional constraint tracking."""

import pytest
from datetime import date
from pathlib import Path

from src.constraint.state_calendar import (
    ActiveConstraint,
    get_active_constraints,
    days_to_next_deadline,
    is_constraint_window_active,
    load_players,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

CONFIG_DIR = Path(__file__).resolve().parent.parent / "config"


@pytest.fixture(scope="module")
def players():
    return load_players(CONFIG_DIR / "players.yaml")


# ===========================================================================
# JERA — Fiscal year ends 03-31, Q4 fiscal = Jan-Mar
# ===========================================================================

class TestJERA:

    def test_q4_fiscal_active_in_february(self, players):
        """Mid-Feb is squarely in JERA's Q4 fiscal window (Jan-Mar)."""
        actives = get_active_constraints("JERA", date(2024, 2, 15), players)
        types = [a.constraint_type for a in actives]
        assert "ToP_deadline" in types
        assert "IFRS_time_lag" in types  # always-on structural constraint

    def test_q4_fiscal_days_remaining(self, players):
        """On 2024-02-15, ToP deadline window ends 2024-03-31 → 45 days."""
        actives = get_active_constraints("JERA", date(2024, 2, 15), players)
        top = next(a for a in actives if a.constraint_type == "ToP_deadline")
        assert top.days_remaining == 45

    def test_q4_fiscal_critical_near_end(self, players):
        """Within 30 days of window end → severity = critical."""
        actives = get_active_constraints("JERA", date(2024, 3, 10), players)
        top = next(a for a in actives if a.constraint_type == "ToP_deadline")
        assert top.severity == "critical"
        assert top.days_remaining == 21

    def test_no_top_in_july(self, players):
        """July is outside JERA's Q4 fiscal window."""
        actives = get_active_constraints("JERA", date(2024, 7, 15), players)
        types = [a.constraint_type for a in actives]
        assert "ToP_deadline" not in types

    def test_ifrs_always_on(self, players):
        """IFRS_time_lag is a structural constraint, active year-round."""
        for month in [1, 4, 7, 10]:
            actives = get_active_constraints("JERA", date(2024, month, 15), players)
            assert any(a.constraint_type == "IFRS_time_lag" for a in actives)

    def test_days_to_deadline_in_q4(self, players):
        """In Q4, nearest deadline should be ≤ days to FYE (03-31)."""
        d = days_to_next_deadline("JERA", date(2024, 2, 15), players)
        # FYE is 03-31, ToP window also ends 03-31 → 45 days
        assert d == 45

    def test_days_to_deadline_outside_q4(self, players):
        """Outside Q4, deadline = next fiscal year end."""
        d = days_to_next_deadline("JERA", date(2024, 7, 15), players)
        # Next FYE = 2025-03-31
        expected = (date(2025, 3, 31) - date(2024, 7, 15)).days
        assert d == expected


# ===========================================================================
# KOGAS — UGBA inventory floor, winter = Nov-Mar
# ===========================================================================

class TestKOGAS:

    def test_ugba_critical_in_winter(self, players):
        """UGBA should be critical during winter months."""
        actives = get_active_constraints("KOGAS", date(2026, 1, 15), players)
        ugba = next(a for a in actives if a.constraint_type == "UGBA_inventory_floor")
        assert ugba.severity == "critical"

    def test_ugba_critical_in_march(self, players):
        """March is still winter (Nov-Mar range)."""
        actives = get_active_constraints("KOGAS", date(2026, 3, 10), players)
        ugba = next(a for a in actives if a.constraint_type == "UGBA_inventory_floor")
        assert ugba.severity == "critical"

    def test_ugba_approaching_in_september(self, players):
        """September is ~60 days before Nov 1 → approaching."""
        actives = get_active_constraints("KOGAS", date(2026, 9, 15), players)
        ugba = next(a for a in actives if a.constraint_type == "UGBA_inventory_floor")
        assert ugba.severity == "approaching"

    def test_ugba_active_in_summer(self, players):
        """June is far from winter — still monitored, severity = active."""
        actives = get_active_constraints("KOGAS", date(2026, 6, 15), players)
        ugba = next(a for a in actives if a.constraint_type == "UGBA_inventory_floor")
        assert ugba.severity == "active"

    def test_price_inversion_always_on(self, players):
        """price_inversion is structural, active year-round."""
        actives = get_active_constraints("KOGAS", date(2026, 6, 15), players)
        assert any(a.constraint_type == "price_inversion" for a in actives)

    def test_days_to_deadline_winter(self, players):
        """In winter, nearest deadline may be UGBA winter end (Mar 31)."""
        d = days_to_next_deadline("KOGAS", date(2026, 1, 15), players)
        # UGBA winter ends March 31, FYE is Dec 31
        # Winter end = Mar 31, 2026 → 75 days away
        # FYE = Dec 31, 2026 → 350 days away
        assert d == 75


# ===========================================================================
# Chinese SOEs — NDRC winter mandate (Nov-Mar)
# ===========================================================================

class TestChineseSOEs:

    @pytest.mark.parametrize("player", ["CNOOC", "Sinopec", "CNPC"])
    def test_ndrc_active_in_december(self, players, player):
        actives = get_active_constraints(player, date(2025, 12, 15), players)
        types = [a.constraint_type for a in actives]
        assert "NDRC_winter_mandate" in types

    @pytest.mark.parametrize("player", ["CNOOC", "Sinopec", "CNPC"])
    def test_ndrc_inactive_in_june(self, players, player):
        actives = get_active_constraints(player, date(2025, 6, 15), players)
        types = [a.constraint_type for a in actives]
        assert "NDRC_winter_mandate" not in types

    @pytest.mark.parametrize("player", ["CNOOC", "Sinopec", "CNPC"])
    def test_residential_priority_always_on(self, players, player):
        actives = get_active_constraints(player, date(2025, 6, 15), players)
        assert any(a.constraint_type == "residential_priority" for a in actives)


# ===========================================================================
# is_constraint_window_active — convenience API
# ===========================================================================

class TestIsWindowActive:

    def test_jera_top_in_window(self, players):
        assert is_constraint_window_active("JERA", date(2024, 2, 1), "ToP_deadline", players)

    def test_jera_top_out_of_window(self, players):
        assert not is_constraint_window_active("JERA", date(2024, 7, 1), "ToP_deadline", players)

    def test_kogas_ugba_always_true(self, players):
        """UGBA is always monitored, so always 'active'."""
        assert is_constraint_window_active("KOGAS", date(2024, 7, 1), "UGBA_inventory_floor", players)

    def test_nonexistent_constraint(self, players):
        assert not is_constraint_window_active("JERA", date(2024, 2, 1), "nonexistent", players)


# ===========================================================================
# Edge cases
# ===========================================================================

class TestEdgeCases:

    def test_jan_1_jera_in_q4(self, players):
        """Jan 1 should be inside JERA's Q4 fiscal (Jan-Mar)."""
        assert is_constraint_window_active("JERA", date(2024, 1, 1), "ToP_deadline", players)

    def test_mar_31_jera_last_day(self, players):
        """Mar 31 is the last day of JERA's Q4 — still active, 0 days remaining."""
        actives = get_active_constraints("JERA", date(2024, 3, 31), players)
        top = next(a for a in actives if a.constraint_type == "ToP_deadline")
        assert top.days_remaining == 0

    def test_apr_1_jera_outside(self, players):
        """Apr 1 is outside JERA Q4."""
        assert not is_constraint_window_active("JERA", date(2024, 4, 1), "ToP_deadline", players)

    def test_year_boundary_ndrc(self, players):
        """Nov-Mar wraps around year boundary. Nov 2025 and Feb 2026 both active."""
        assert is_constraint_window_active("CNOOC", date(2025, 11, 15), "NDRC_winter_mandate", players)
        assert is_constraint_window_active("CNOOC", date(2026, 2, 15), "NDRC_winter_mandate", players)
