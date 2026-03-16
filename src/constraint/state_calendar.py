"""
State Calendar — Institutional constraint tracking by player and date.

Input: config/players.yaml, current date
Output: ActiveConstraint list, days-to-deadline, window status

Maps each player's fiscal calendar and regulatory constraints onto a timeline
so downstream modules know *when* institutional pressure is active.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from typing import Dict, List, Optional

import yaml


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class ActiveConstraint:
    """A single institutional constraint that is currently active for a player."""
    constraint_type: str          # e.g. "ToP_deadline", "UGBA_inventory_floor"
    days_remaining: Optional[int] # days until the constraint window closes (None if always-on)
    severity: str                 # "critical" | "active" | "approaching"
    details: Dict                 # original YAML payload for downstream use


# ---------------------------------------------------------------------------
# Window logic helpers
# ---------------------------------------------------------------------------

_MONTH_ABBR = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}


def _parse_fiscal_year_end(fye_str: str) -> tuple[int, int]:
    """Parse 'MM-DD' → (month, day)."""
    parts = fye_str.split("-")
    return int(parts[0]), int(parts[1])


def _fiscal_year_end_date(fye_month: int, fye_day: int, ref: date) -> date:
    """Return the *next* fiscal-year-end date on or after ``ref``."""
    candidate = date(ref.year, fye_month, fye_day)
    if candidate < ref:
        candidate = date(ref.year + 1, fye_month, fye_day)
    return candidate


def _parse_month_range(window_str: str) -> tuple[int, int]:
    """Parse window specs like 'Nov-Mar' → (11, 3)."""
    parts = window_str.split("-")
    start = _MONTH_ABBR[parts[0].strip().lower()[:3]]
    end = _MONTH_ABBR[parts[1].strip().lower()[:3]]
    return start, end


def _month_in_range(month: int, start: int, end: int) -> bool:
    """Check whether *month* falls inside [start, end], wrapping around Dec→Jan."""
    if start <= end:
        return start <= month <= end
    # wraps around year boundary (e.g. Nov-Mar → 11,12,1,2,3)
    return month >= start or month <= end


def _window_end_date(start_month: int, end_month: int, ref: date) -> date:
    """Last day of the window's end-month that is on or after *ref*."""
    import calendar
    # Determine the year for the window end
    if start_month <= end_month:
        # Same calendar year
        end_year = ref.year
    else:
        # Wraps around: if we're in the start-side (>=start_month), end is next year
        end_year = ref.year + 1 if ref.month >= start_month else ref.year

    last_day = calendar.monthrange(end_year, end_month)[1]
    candidate = date(end_year, end_month, last_day)
    if candidate < ref:
        # Already past this cycle — advance by one year
        end_year += 1
        last_day = calendar.monthrange(end_year, end_month)[1]
        candidate = date(end_year, end_month, last_day)
    return candidate


def _resolve_q4_fiscal(fye_month: int, fye_day: int) -> tuple[int, int]:
    """Q4 of a fiscal year = the 3 months ending on fiscal-year-end month.

    E.g. FYE 03-31 → Q4 = Jan, Feb, Mar → (1, 3)
    """
    end = fye_month
    start = (fye_month - 3) % 12 + 1
    return start, end


# ---------------------------------------------------------------------------
# Player config loader
# ---------------------------------------------------------------------------

def load_players(players_path: str | Path) -> Dict:
    """Load and return the players YAML as a dict."""
    with open(players_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# ---------------------------------------------------------------------------
# Core public API
# ---------------------------------------------------------------------------

def get_active_constraints(
    player_name: str,
    query_date: date,
    players: Dict,
) -> List[ActiveConstraint]:
    """Return all institutional constraints active for *player_name* on *query_date*.

    Parameters
    ----------
    player_name : str
        Key in players dict (e.g. "KOGAS", "JERA").
    query_date : date
        The date to evaluate.
    players : dict
        Parsed players.yaml content.

    Returns
    -------
    List[ActiveConstraint]
        May be empty if no constraints are active on that date.
    """
    player = players[player_name]
    fye_month, fye_day = _parse_fiscal_year_end(player["fiscal_year_end"])
    constraints_cfg = player.get("institutional_constraints", [])

    active: List[ActiveConstraint] = []

    for cfg in constraints_cfg:
        ctype = cfg["type"]

        # ---- Always-on constraints (no window) ----
        if "window" not in cfg and ctype not in ("UGBA_inventory_floor",):
            # Constraints like "price_inversion", "residential_priority" are
            # structural — always active.
            active.append(ActiveConstraint(
                constraint_type=ctype,
                days_remaining=None,
                severity="active",
                details=dict(cfg),
            ))
            continue

        # ---- UGBA inventory floor (always monitored, severity changes) ----
        if ctype == "UGBA_inventory_floor":
            # UGBA is always technically active but severity depends on
            # proximity to winter heating season (Nov-Mar in Korea).
            winter_start, winter_end = 11, 3
            in_winter = _month_in_range(query_date.month, winter_start, winter_end)
            # Approaching = within 60 days of winter start
            nov1 = date(query_date.year, 11, 1)
            if nov1 < query_date:
                nov1 = date(query_date.year + 1, 11, 1)
            days_to_winter = (nov1 - query_date).days

            if in_winter:
                severity = "critical"
                end = _window_end_date(winter_start, winter_end, query_date)
                days_rem = (end - query_date).days
            elif days_to_winter <= 60:
                severity = "approaching"
                days_rem = days_to_winter
            else:
                severity = "active"  # monitored daily year-round per YAML
                days_rem = days_to_winter

            active.append(ActiveConstraint(
                constraint_type=ctype,
                days_remaining=days_rem,
                severity=severity,
                details=dict(cfg),
            ))
            continue

        # ---- Window-based constraints ----
        window_str = cfg["window"]

        if window_str == "Q4_fiscal":
            start_m, end_m = _resolve_q4_fiscal(fye_month, fye_day)
        else:
            start_m, end_m = _parse_month_range(window_str)

        if _month_in_range(query_date.month, start_m, end_m):
            end_date = _window_end_date(start_m, end_m, query_date)
            days_rem = (end_date - query_date).days

            severity = "critical" if days_rem <= 30 else "active"

            active.append(ActiveConstraint(
                constraint_type=ctype,
                days_remaining=days_rem,
                severity=severity,
                details=dict(cfg),
            ))

    return active


def days_to_next_deadline(
    player_name: str,
    query_date: date,
    players: Dict,
) -> int:
    """Return the number of days until the player's next hard deadline.

    The primary deadline is the fiscal-year-end. If the player has windowed
    constraints that end sooner, the earliest of those is returned instead.
    """
    player = players[player_name]
    fye_month, fye_day = _parse_fiscal_year_end(player["fiscal_year_end"])

    # Fiscal year end is the baseline deadline
    fye_date = _fiscal_year_end_date(fye_month, fye_day, query_date)
    nearest = (fye_date - query_date).days

    # Check if any active windowed constraint ends sooner
    for ac in get_active_constraints(player_name, query_date, players):
        if ac.days_remaining is not None and ac.days_remaining < nearest:
            nearest = ac.days_remaining

    return nearest


def is_constraint_window_active(
    player_name: str,
    query_date: date,
    constraint_type: str,
    players: Dict,
) -> bool:
    """Check whether a specific constraint type is active on *query_date*."""
    actives = get_active_constraints(player_name, query_date, players)
    return any(ac.constraint_type == constraint_type for ac in actives)
