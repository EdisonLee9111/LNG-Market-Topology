"""
Cross-layer data contracts for LNG-Market-Topology.

All modules communicate exclusively through these dataclasses.
This file is the single source of truth for inter-layer data structures.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Tuple


# =============================================================================
# Constraint Layer Outputs
# =============================================================================

@dataclass
class ConstraintState:
    """Output of the constraint layer for a given player at a given date.

    Combines institutional calendar state with topological exposure assessment.
    """
    player: str
    date: datetime
    active_constraints: List[str]       # ["ToP_deadline", "UGBA_redline", ...]
    exposure_score: float               # 0.0-1.0, volume through disrupted node / total
    buffer_score: float                 # 0.0-1.0, composite of alternatives
    constraint_class: str               # "binding" | "induced" | "buffered"
    feasible_routes: List[str] = field(default_factory=list)
    days_to_deadline: Optional[int] = None


# =============================================================================
# Signal Layer Outputs
# =============================================================================

@dataclass
class RationalBaseline:
    """The profit-maximizing flow pattern for a given route at current prices."""
    route_id: str
    netback_spread: float               # $/MMBtu
    optimal_destination: str
    total_voyage_cost: float            # USD
    break_even_wait_days: float         # W value (canal queue threshold)


@dataclass
class ShadowPriceResult:
    """Quantifies the implied cost of a hidden constraint driving observed behavior.

    Dual-mode:
    - route_deviation: cost(actual_route) - cost(optimal_route)
    - price_premium: (spot - contract_baseline) * volume
    """
    cargo_id: str
    mode: str                           # "route_deviation" | "price_premium"
    shadow_price_usd: float
    implied_constraint_cost: float      # $/MMBtu equivalent
    attribution_signal: str             # "institutional" | "strategic" | "ambiguous"


@dataclass
class DeviationSignal:
    """A detected deviation from the rational baseline."""
    timestamp: datetime
    signal_type: str                    # "route_shift" | "speed_anomaly" | "spread_residual"
    magnitude: float
    direction: str                      # "tightening" | "loosening"


# =============================================================================
# Inference Layer Outputs
# =============================================================================

@dataclass
class BehaviorPosterior:
    """Posterior probability distribution over behavioral hypotheses for a player.

    Note: This is structured expert judgment using probabilistic logic for
    consistency, not a data-driven statistical model. See README for full
    methodological disclaimer.
    """
    player: str
    timestamp: datetime
    hypotheses: Dict[str, float]        # {"restocking": 0.6, "distressed": 0.3, ...}
    posterior_entropy: float
    dominant_hypothesis: str
    inference_pass: str                 # "first" | "second"


# =============================================================================
# Upstream Project Interfaces (mock/adapter)
# =============================================================================

@dataclass
class ArbitrageMonitorOutput:
    """Interface to Global-LNG-Arbitrage-Monitor outputs."""
    route_id: str
    netback_spread: float
    shipping_cost: float
    monte_carlo_ci_95: Tuple[float, float] = (0.0, 0.0)


@dataclass
class EventStudyOutput:
    """Interface to Structural-Event-Study-Framework outputs."""
    timestamp: datetime
    hotelling_t2: float
    is_significant: bool
    channels_affected: List[str] = field(default_factory=list)


@dataclass
class AlphaFeedOutput:
    """Interface to LNG-Alpha-Feed outputs."""
    timestamp: datetime
    public_explanation_exists: bool
    event_tags: List[str] = field(default_factory=list)
    temporal_lag_hours: float = 0.0     # break timestamp - first public report
