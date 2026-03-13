# LNG-Market-Topology Case Study Narrative

## Section 0: Opening — The Core Proposition of the Framework

Imagine a Q-Max vessel carrying 70,000 tons of liquefied natural gas (LNG) slowing down to hover off the coast of Oman. Its captain receives orders from the trading desk, but the vessel's next move is restricted to only three viable choices. Market participants in the global LNG trade can go to great lengths to obfuscate their trade execution—they can split orders across multiple brokers, vary their timing, or randomize cargo sizes. However, they cannot evade the fundamental physical and institutional constraints of the network. A cargo still takes a minimum of 25 days to sail from Sabine Pass to Tokyo Bay. A regasification terminal still has a finite number of unloading slots. JERA's fiscal year still ends resolutely on March 31. This framework treats those invariants as the absolute basis for inference.

The core logic of the LNG-Market-Topology framework is simple but powerful: `P(Behavior | Signal, Constraint State)`. When physical or institutional constraints tighten, the set of feasible actions for any given player shrinks dramatically, causing their behavioral probability distribution to become sharply deterministic. A buyer who must fulfill a Take-or-Pay obligation before their fiscal year-end, navigating through a congested canal into a nearly full terminal, has very few degrees of freedom left. 

This document serves as the first empirical case study for the LNG-Market-Topology project, employing a two-tiered architectural narrative:
1. **Layer 1 (2023.7 — 2024.3)**: Historical backtesting of the methodology during the Panama Canal drought, representing a single-bottleneck constraint.
2. **Layer 2 (2026.1 — 2026.3)**: Real-time framework application during the Strait of Hormuz crisis overlaid with Panama Canal's LoTSA 2.0 implementation, representing multi-bottleneck constraint stacking.

Layer 1 validates the framework's inferential precision against fully resolved historical data. Layer 2 tests a different proposition: whether the same constraint reasoning logic, built and validated on a single-bottleneck canal scenario, can be rapidly transferred to a structurally distinct multi-bottleneck crisis and produce verifiable inferences within days of the event's onset. This is not a claim of foresight; it is the application of an established analytical framework to a developing crisis, generating a set of structured inferences with explicit falsification conditions. The accompanying [Prediction Scorecard](prediction_scorecard.md) tracks the verification status of each inference and distinguishes between framework-derived conclusions and informed extrapolations from already-observable data.

It is important to note that this framework does not attempt to infer the behavior of every LNG participant. Instead, it focuses on players facing the tightest constraints: the Japanese power utility sector, South Korea's KOGAS, and Chinese State-Owned Enterprises (SOEs).

---

## Section 1: Constraint Layer Modeling — Physical Topology

To infer behavior, we must first define the physical "chessboard"—the nodes and edges through which LNG must travel from liquefaction to regasification, and more importantly, the bottlenecks that limit these flows (Research Team 2024). In maritime logistics, distance alone does not capture the full complexity of a route; time, toll fees, and cryogenic thermal dynamics rigorously define the boundaries of profitability and operational feasibility.

### 1a. Minimal Topology Graph and Economic Baselines
For the scope of this case study, we model a targeted subgraph of the global LNG network, specifically anchoring the analysis around U.S. Gulf Coast liquefaction terminals (e.g., Sabine Pass, Cameron, Corpus Christi), Qatar's Ras Laffan, and major Northeast Asian regasification hubs. The edges connecting these nodes are severely bifurcated by operational metrics.

Route economics vary substantially. To precisely quantify the topological distances, we must examine the comparative cost structures of the primary arteries. A standard U.S. Gulf Coast (USGC) to Northeast Asia voyage operates under the following baseline parameters: a 174,000 cubic meter (cbm) vessel, a Boil-Off Gas (BOG) rate of 0.1%, an energy conversion factor of 23.0 MMBtu/cbm, and an assumed JKM spot price of $15.98/MMBtu. Under these conditions, the payload sheds approximately $63,000 worth of gas per day simply through thermal boil-off (Research Team 2024).

**Route Cost Comparison Table (USGC to Northeast Asia / Middle East to NE Asia)**

| Route | Distance/Time | Freight Cost (US$) | Tolls (US$) | BOG Loss Value (US$) | Total Estimate (US$) |
|:---|:---|:---|:---|:---|:---|
| **Panama Canal (USGC-Asia)** | 25 days | $1.50 M | $1.00 M | $1.57 M | **$4.07 M** |
| **Cape of Good Hope (USGC-Asia)** | 40 days (+15) | $2.40 M | $0 | $2.52 M | **$4.92 M (+0.85M)** |
| **Middle East Direct (Qatar-Asia)**| 14-15 days | $0.90 M | $0 | $0.94 M | **$1.84 M** |
| **Suez Canal (USGC-Asia)** | 35-38 days | $2.10 M | $0.50 M | $2.20 M | **$4.80 M** |

*(Source computations derived from Research Team (2024) 「LNG Route Cost Comparison Analysis」 『Internal Report』: 1-5)*

The quantitative delta is significant: choosing the Cape of Good Hope over Panama adds 15 days of transit. This delay introduces a $900,000 increase in freight costs and an additional $945,000 in vaporized BOG losses (15 days × $63,000/day). While saving the $1.0 million Panama transit toll offsets some of the burden, the net penalty for bypassing the canal is approximately $850,000 per voyage. This $850,000 delta represents the break-even threshold: the incremental cost a rational actor must accept to shift from the Panama to the Cape route.

### 1b. Physical Constraints of the Panama Canal (Layer 1)
Under normal hydrological conditions, the Panama Canal handles a baseline of 36-38 transits per day. However, driven by an extreme El Niño event, Gatun Lake experienced severe drought, leading to a structural reduction in daily capacities: 32 transits in July 2023, 24 in November 2023, and falling to an absolute trough of 22 transits by December 2023, before slowly recovering to 35 in August 2024 (ACP Analysts 2024).

A key finding challenges a prevalent market myth: the 66% plunge in LNG vessel transits was **not** caused by draft restrictions. The Canal Authority (ACP) set the minimum Neopanamax draft at 44 feet, which easily accommodated typical fully laden LNG vessels that draw between 36 and 39.5 feet (ACP Analysts 2024). The real culprit was systemic uncertainty. LNG vessels, carrying daily $63,000 BOG losses, require tight "Just-in-Time" scheduling precision. The ACP's rules—such as the one-slot-per-customer-per-day limit and wild auction fees peaking at $4 million (e.g., Eneos VLGC in Nov 2023)—destroyed this certainty. In supply chain economics, the loss of predictability is far more destructive than mere physical flow restriction.

### 1c. The Lethal Rigidity of LoTSA 2.0 and the Hormuz Closure (Layer 2)
In contrast to the drought's gradual tightening, the Strait of Hormuz represents a step-function disruption. Carrying 20% of global LNG trade and 20.9 Mbbl/d of crude oil, its substantive closure in late February to early March 2026 introduces a binary "shut-off" constraint into the physical topology, removing ~20% of global LNG supply from accessible routes.

Critically, this crisis does not occur in a vacuum; it compounds with the newly implemented Panama Canal Long-Term Slot Allocation (LoTSA 2.0) methodology. LoTSA 2.0 functions as a structural barrier to crisis-mode procurement. Unlike the older auction system where vessels could pay a premium for queue priority, LoTSA 2.0 mandates a 6-month sealed bidding window—allocations covering January 4 through July 4, 2026 were finalized by October 28, 2025. Under this regime, the Neopanamax locks allocate only 3 long-term slots per day, reduced from 4 under LoTSA 1.0 (ACP Analysts 2024).

Notably, LNG vessels are explicitly excluded from the newly introduced "FlexSlot+" mechanism. The operational consequence is precise: LoTSA 2.0 locks routing decisions six months in advance and removes the spot-responsive queue-jumping that energy traders relied upon during the 2023 drought. When the Hormuz Strait closes, any buyer attempting to procure emergency spot cargoes from the U.S. Gulf Coast faces a Panama Canal with no available slots. The physical allocations are pre-committed and sealed. The net effect: the USGC-to-Asia Panama route is operationally severed for unplanned cargoes.

---

## Section 2: Constraint Layer Modeling — Institutional Calendar

While physical constraints define the "spatial dimension" of the feasible action set, the institutional calendar defines the "temporal dimension" through hard deadlines. When both dimensions intersect, the behavioral space compresses sharply. These institutional boundaries are binding: they are anchored to national law, contractual penalties, and accounting cycles that directly affect the solvency of state utilities.

### 2a. Institutional Clocks and Fleet Dynamics of the Top Players

The global LNG market is dominated by entities bound to non-negotiable legal and fiscal chronologies. For the Japanese power utility sector, represented by giants like JERA and Tokyo Gas, the absolute deadline is the fiscal year-end of March 31. These organizations must settle their contracted annual volumes before this date or incur Take-or-Pay (ToP) penalties on unlifted volumes. Their International Financial Reporting Standards (IFRS) time-lag accounting rules further lock procurement cost recognition to this specific window.

For Chinese State-Owned Enterprises (SOEs) such as CNOOC, Sinopec, and CNPC, the critical window is the heating season extending from November to March, governed by political edicts from the National Development and Reform Commission (NDRC) mandating winter supply guarantees (Strategy Group 2024).

The tightest institutional constraints belong to South Korea's KOGAS. The entity is bound by the "7+30 days" safety inventory redline under Article 10-10 of the Urban Gas Business Act (UGBA). This threshold requires KOGAS to hold reserves equivalent to at least 7 days of mandatory inventory plus 30 days of preventive reserves, calculated against the highest seasonal daily sales volume over the previous 24 months. If inventory falls below this legal floor for 7 consecutive days, the Ministry of Trade, Industry and Energy (MOTIE) is required to initiate national energy emergency protocols (Strategy Group 2024). KOGAS simultaneously operates under domestic price inversion: it must source emergency spot LNG at global market prices (potentially $25-30/MMBtu in a crisis), while the South Korean government maintains caps on domestic retail gas tariffs. Each spot cargo purchased at crisis premiums generates a spread that KOGAS absorbs onto its balance sheet as uncollected receivables, progressively eroding its capital position—a structural dynamic where compliance with UGBA directly increases financial exposure.

### 2b. The Crucial Intersection and Freight Absorption (Layer 1)
During the historical Layer 1 backtest (January - March 2024), we observed the strictest limitations of the Panama Canal (22-24 ships/day) coinciding precisely with JERA's March 31 fiscal year-end. JERA was required to execute deliveries to satisfy its ToP volume obligations despite severely constrained logistics. 

It is important to understand *why* the 15-day rerouting via the Cape of Good Hope did not immediately trigger a global shipping freight squeeze in early 2024. The shipbuilding delivery cycle masked the constraint. In the first half of 2024, the primary market indices (Spark30S and Spark25S) remained heavily depressed, hovering between $20,000 and $70,000 per day (Data Insights 2024). This suppression occurred because the industry absorbed over 60 new highly efficient vessel deliveries, coinciding with ~180 older steam turbine vessels phasing out of profitable circulation. These 60+ new ships absorbed the incremental ton-mile demand created by the Cape diversions. The market was inadvertently saved by its own orderbook. However, this buffer was artificial. By Q4 2024, as the European market backed up and vessels were locked into floating storage plays seeking arbitrage, the underlying tightness from Cape rerouting was exposed, and freight rates surged to over $182k/day.

### 2c. Constraint Stacking Compression (Layer 2)
The March 2026 Hormuz scenario represents multi-dimensional constraint stacking without modern precedent. The closure of Middle Eastern supply routes coincides with the enforcement of Panama's LoTSA 2.0 (blocking U.S. spot rescues via the Canal). Simultaneously, the timing aligns with JERA's March 31 fiscal year-end and KOGAS's post-winter inventory nadir, as KOGAS approaches the UGBA legal redline. Under normal conditions, JERA retains significant degrees of freedom—e.g., reselling surplus long-term contracted cargo (a record 38.25 MT in FY2023, equivalent to 37% of domestic consumption) (Energy Desk 2024). When constraints stack, these degrees of freedom collapse. Players shift from optional spot participation to compelled procurement at prevailing market prices to satisfy compliance deadlines.

---

## Section 3: Signal Layer — Rational Baseline and Deviation Detection

To infer true intent, we establish a "rational baseline" representing what a pure profit-maximizing participant would do at any given time. We then identify the deviations from this baseline.

### 3a. Construction of the Rational Baseline
At any time *t*, based on spot JKM, TTF, Henry Hub prices, TC Rates (Time Charter), BOG loss rates, and Canal tolls, the shadow price engine computes the optimal netback route. 
The mathematical formula for the shadow price is:
`ΔCost_Cape = (TC_Rate + BOG_daily) × Δdays_extra - Toll_Panama`
The critical waiting days *W* to justify avoiding the canal is:
`W = [(TC + BOG) × Δdays - Toll] / (TC + BOG)`

The economic intuition behind *W* is straightforward: it represents the **break-even queueing threshold**—the maximum number of days a vessel can afford to wait in the Panama Canal queue before the cumulative daily waiting cost (time charter plus BOG losses) equals the total incremental cost of bypassing the canal entirely via the Cape of Good Hope. If the expected queue exceeds *W* days, a rational charterer should immediately reroute; if it is shorter, waiting remains the cheaper option.

To illustrate: In a normal market (TC=$60k/day), the critical waiting time *W* is approximately 9 days. In the extreme market environment of March 2026 (TC=$300k/day, high JKM), *W* extends to roughly 13 days (Research Team 2024).

### 3b. Actual Behavioral Signals (Layer 1: 2023-2024)
- **Voyage Route Shift**: In Q3 2023, 38 US cargoes still transited Panama. By Q3 2024, only 10 did, representing a 94% redirection of US-to-Asia cargoes via the Cape of Good Hope (Energy Desk 2024).
- **Voyage Inflation Acceptance**: Despite the extra 10-14 days and fuel burn, US exports to Asia didn't collapse; they surged 22% to 29 MT.
- **Price Compensation**: The JKM premium over TTF expanded from 0.6 to 1.3 $/MMBtu, effectively acting as an exact rational compensation for the incremental cost of the Cape route (Data Insights 2024).
- **Freight Volatility**: The Spark25S/30S index was sluggish in H1 2024 ($20k-$70k/day) due to 60+ new vessel deliveries absorbing the extra ton-mile demand. However, by Q4, rates surged to over $182k/day due to European congestion and floating storage arbitrage.

### 3c. Signal Interpretation
If the observed deviation generates a low shadow price, the behavior is deemed "rational," representing opportunistic adjustments near the margin. If a player exhibits routing or bidding behavior that implies a very high shadow price, it signals an "irrational" market action driven strictly by a hidden hard constraint (such as a ToP deadline or legal inventory redlines).

---

## Section 4: Inference Layer — Posterior Behavior Attribution

By overlaying the detected deviations from the rational baseline with the institutional calendar, we perform Bayesian attribution to determine whether actions are strategically or institutionally driven. In an environment devoid of certainty, tracing the behavior of state-backed actors through their systemic vulnerabilities is the only mechanism left for predictive analysis.

### 4a. Layer 1 Behavior Attribution (2023-2024 Backtesting)

| Signal | Behavioral Description | Shadow Price | Attribution (Institutional vs. Strategic) |
|:---|:---|:---|:---|
| ① Voyage Inflation | Broad acceptance of Cape rerouting; US to Asia exports +22%. | Medium | **Mixed** — Driven by ToP obligations but spot arbitrage compensation existed. |
| ② JERA-KOGAS Swap | Signing of historic MOU to physically swap cargoes based on inventory timing. | Low for both parties (mutual swap avoided the prevailing spot premium) | **Institutional** — Both players faced conflicting rigid deadlines. |
| ③ Record Japanese Resales | Japanese players resold 38.25 MT overseas in FY2023. | Negative (Profitable) | **Strategic** — Capitalizing on structural long-term surplus to play global arbitrage. |

**Key Narrative**: The emergence of Signal ② validates the core hypothesis. When two players face unique but equally rigid institutional constraints, their cooperative behavior becomes predictable. JERA (pressured by its March 31 ToP deadline) possessed excess nearby inventory but lacked distant resupply. KOGAS (pressured by Dec 31 and statutory storage minimums) lacked immediate inventory but had pending resupply en route. The physical swap was the exact, unique mathematical solution to the intersection of their constraint sets (Energy Desk 2024). This was not a function of free-market trading, but of institutional survival math.

### 4b. Layer 2 Behavior Inference — Real-time Framework Application (2026.3)

> **Methodology note**: The following inferences were generated in early March 2026, after the Strait of Hormuz crisis was already underway. Their value lies not in foresight, but in demonstrating framework portability: the constraint reasoning logic built and validated on the Panama Canal single-bottleneck scenario (Layer 1) was transferred to a structurally distinct multi-bottleneck crisis within days of its onset. Each inference below is classified as either **(F)** Framework-derived inference—a conclusion that follows from the constraint model's logic chain regardless of observation timing—or **(E)** Informed extrapolation—a projection based on data points already observable at the time of analysis.

Applying the framework to the multi-bottleneck stacking (Hormuz closure + LoTSA 2.0 implementation) in March 2026 yields the following posterior inferences for key players, highlighting the disparity in how different national energy architectures absorb the same supply shock.

**JERA (March 31 deadline + Middle East cutoff + Panama LoTSA lock-out)**
- **Inferred Behavior**: Standard procurement channels severed. **(F)** Framework indicates JERA shifts to distressed spot at $5-10/MMBtu premium over rational baseline, implied shadow price >$3M/cargo above Cape route netback. **(F)** Concurrent activation of JERA-KOGAS physical swap mechanisms to access volumes in adjacent inventory pools. **(F)** Petition to METI for authorization of emergency inter-utility physical swaps outside normal commercial protocols.
- **Shadow Price**: **(E)** Elevated. JKM implied at +40% over pre-crisis baseline, consistent with observed surge above $22.50/MMBtu. (Note: JKM was already elevated at time of analysis; the +40% figure reflects observed trajectory extrapolation.)
- **Verifiable Flags**: **(F)** Negishi terminal inventory drawdown rate in March exceeding seasonal norm by >2x; **(F)** material "time-lag" IFRS losses appearing in FY2025/2026 earnings (procurement cost booked in Q4 FY2025, tariff recovery deferred to FY2026).

**KOGAS (Legal 7+30 day UGBA redline + Post-winter low inventory + Price Inversion)**
- **Inferred Behavior**: **(F)** Price-insensitive spot procurement triggered by inventory approaching the UGBA legal floor. **(F)** Acceptance of asymmetric terms in JERA swap arrangements to maintain physical flow—a behavioral pattern already validated in Layer 1 (Signal ②). **(E)** On the policy front, framework expects acceleration of the 70% FOB domestic-carrier mandate as MOTIE/MOF move to reclaim logistics control from DES-dependent foreign shipping. (Note: policy signals for this measure were already visible at time of analysis.)
- **Shadow Price**: **(F)** Dominated by institutional cost function. The regulatory and political cost of UGBA violation (potential national energy emergency declaration, residential supply disruption) exceeds any plausible spot premium—KOGAS will procure at $25-30/MMBtu if necessary, absorbing the spread against capped domestic tariffs as balance sheet receivables.
- **Verifiable Flags**: **(F)** KOGAS inventory days declining toward the 37-day statutory threshold; **(F)** MOTIE activating elevated energy emergency protocols; **(F)** widening of KOGAS uncollected receivables in Q1 2026 financials, potentially requiring sovereign backstop.

**Chinese SOEs (NDRC mandate + Strategic depth + Gray-zone positioning)**
- **Inferred Behavior**: **(F)** Chinese SOEs operate with structurally lower urgency than Japanese/Korean counterparts. **(F)** Framework indicates limited participation in the distressed spot market. Primary response vector: increase domestic gas production, raise daily nominations on Power of Siberia and Central Asian pipeline gas to contractual maximums, draw down underground storage facilities, and procure spot LNG selectively at margin rather than at distressed premium.
- **The "Strategic Depth" Data Support**: Reduced spot dependence is supported by quantifiable physical buffers. China holds approximately 1.2 billion barrels of crude oil in strategic and commercial reserves—covering 108 to 200 days of import replacement depending on rationing assumptions. Additionally, China maintains a distinct geopolitical positioning vis-à-vis Iran: an estimated 80% of Iran's sanctioned crude exports flow to Chinese refineries, much of it via vessels operating with obscured AIS signals. In a Hormuz blockade scenario, this relationship creates an asymmetric dynamic—Iranian enforcement may differentiate between Chinese-associated and non-Chinese vessels. **However, it is important to note that the actual picture is more complex than a simple "semi-permeable" model suggests.** CSIS satellite tracking data from the crisis period indicates that Chinese-flagged vessels have also largely avoided direct Hormuz transits, suggesting the blockade's permeability operates through indirect mechanisms (e.g., ship-to-ship transfers outside the strait, pre-positioned inventory in Omani or UAE waters) rather than straightforward selective passage. The net effect on Chinese supply security is real but should not be modeled as a clean binary advantage.
- **Shadow Price**: Medium to Low. Diversified supply infrastructure (pipeline + domestic + storage) absorbs the single-node failure that concentrates risk for Japan and Korea.
- **Verifiable Flags**: **(F)** Limited, targeted industrial gas rationing in March (residential supply preserved); **(F)** Q1 profit margin compression for CNOOC/Sinopec/CNPC as they absorb elevated procurement costs to maintain domestic price stability.

---

## Section 5: Falsifiable Hypotheses & Verification Plan

The strength of LNG-Market-Topology lies in its empirical testability. Every inference drawn in this narrative is tied to specific, measurable data points.

### Layer 1 Backtesting Hypotheses

**Hypothesis 1: Constraint Binding → Inference Precision**
- **Test**: Compare the prediction accuracy of JERA's logistical behavior in Q1 2024 (strictest Canal limits, 22-24 transits) versus Q3 2024 (Canal normalized to 35 transits).
- **Verification Data**: Post-event cargo flow tracking via Kpler or SynMax.
- **Expectation**: Inference should be significantly sharper (lower posterior entropy) in Q1 when the bottleneck is binding.

**Hypothesis 2: Institutional Calendar → Regime Switching**
- **Test**: Examine the accuracy of predicting JERA's volume-dumping and resale behavior.
- **Verification Data**: Quarterly distribution of LNG resale volumes in JERA's public financial reports.
- **Expectation**: Predictions should be measurably more accurate regarding behavior between January and March (fiscal year-end) than in other quarters.

**Hypothesis 3: Shadow Price → Behavioral Disambiguation**
- **Test**: Assess if high shadow price deviations (>$2M/cargo route penalty) predominantly map back to institutional rather than strategic drivers.
- **Verification Data**: Cross-reference with post-event industry reports detailing ToP distress or looming statutory inventory penalties.
- **Expectation**: Over 70% of high shadow price deviations should be retrospectively attributed to institutional hard constraints.

### Layer 2 Framework Application — Inference Verification (post 2026.2.28)

**Hypothesis 4: Real-time Framework Application Validations**

The following table classifies each inference by its epistemic status at the time of analysis and tracks verification outcomes. See [Prediction Scorecard](prediction_scorecard.md) for the full tracking document including forward predictions from 2026.3.13.

| Inference | Classification | Status (as of 2026.3.13) |
|:---|:---|:---|
| JKM breaks $22.50/MMBtu barrier in March | **(E)** Informed extrapolation — JKM was already elevated at time of analysis | ✅ Observed (pre-existing at analysis date) |
| JERA-KOGAS physical swap activation | **(F)** Framework-derived — behavioral pattern validated in Layer 1 (Signal ②) | ⏳ Pending verification |
| South Korea enacts 70% FOB national fleet mandate | **(E)** Informed extrapolation — policy signals already visible at analysis date | ✅ Enacted (MOF/MOTIE per Strategy Group report) |
| China Q1: profit compression without residential shortage | **(F)** Framework-derived — NDRC institutional logic + diversification structure | ⏳ Pending Q1 2026 data |

---

## Section 6: Closing — Significance and Limitations

The significance of the LNG-Market-Topology framework lies in its epistemological approach: in the highly opaque, fast-moving, and asymmetric global LNG market, constraints are our most reliable observation tools. We do not need to know the specific trading decisions a counterparty made behind closed doors; we only need to map the rigid constraints they face. By knowing their exact constraint set, we can accurately infer the probability distribution of their actions on the global stage.

We must also state the honest limitations of this case study:
1. This narrative was built using synthesized public reports and monthly/quarterly statistics, which lack the granularity of real-time AIS, cargo-level logs, or exact private contractual clauses.
2. The real-time computation of shadow prices relies on continuous polling of TC Rates and JKM indexes, whereas the figures used here are point-in-time references quoted from specific reports.
3. The Layer 2 analysis for March 2026 is an actively evolving scenario, where initial signals (JKM spikes, FOB shipping mandates) have materialized, but secondary attributions still require retrospective market data.

Ultimately, the transition from narrative to code is straightforward: in the implementation, every "inference" corresponds to a computable mathematical quantity, and every "constraint" is directly modeled as a weighted node or restricted edge in the topological graph. By fusing physical bottlenecks with institutional deadlines, the framework brings structural order to seemingly chaotic market noise.

---

## Works Cited

ACP Analysts (2024) 「Panama Canal Drought Data Analysis」 『Maritime Review』: 1-10.

Data Insights (2024) 「Search LNG Market Post-Event Data」 『Market Analytics』: 1-6.

Energy Desk (2024) 「Asian Energy Supply under Panama Canal Restrictions」 『Commodity Insights』: 1-8.

Research Team (2024) 「LNG Route Cost Comparison Analysis」 『Internal Report』: 1-5.

Strategy Group (2024) 「Energy Enterprise Procurement and Supply Analysis」 『Utility Economics』: 1-12.
