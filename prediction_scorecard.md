# LNG-Market-Topology Prediction Scorecard

**Created**: 2026-03-13
**Last updated**: 2026-03-13
**Verification window**: Through 2026-05-15 (JERA FY2025 earnings season)
**Repository**: Commit timestamps serve as immutable proof of inference dates.

---

## Classification Key

| Tag | Label | Definition |
|:---|:---|:---|
| **(F)** | Framework-derived inference | Conclusion that follows from the constraint model's logic chain (physical topology + institutional calendar + shadow price engine). Valid regardless of when the analysis was conducted—the inference is a structural output of the model, not an observation. |
| **(E)** | Informed extrapolation | Projection based on data points already observable at the time of analysis. The direction was already indicated by early market signals; the framework provides structure but not independent discovery. |
| **(O)** | Observation | Fact already confirmed at the time of writing. Included for completeness and to honestly distinguish from genuine inferences. |

---

## Part A: Layer 1 Backtest Results (2023.7 — 2024.3)

Historical backtesting against fully resolved data. These are retrospective validations—the framework's constraint logic is applied to events whose outcomes are already known.

| ID | Framework Inference | Actual Outcome | Verdict |
|:---|:---|:---|:---|
| A1 | Panama Canal draft restrictions (44 ft minimum) should NOT be the primary cause of the 66% LNG transit plunge—systemic uncertainty (JIT disruption, auction cost unpredictability) is the dominant driver. | Confirmed. LNG vessels draw 36-39.5 ft, well under the 44 ft limit. Transit collapse driven by slot uncertainty, $4M auction fees, and BOG timing risk (ACP Analysts 2024). | ✅ Confirmed |
| A2 | US-to-Asia cargoes will massively reroute via Cape of Good Hope as Panama queue costs exceed the break-even threshold (~$850k/voyage penalty). | 94% of US-Asia LNG rerouted via Cape by Q3 2024 (Data Insights 2024). | ✅ Confirmed |
| A3 | Despite 15-day longer voyages, US LNG exports to Asia will NOT decline—buyers will accept "voyage inflation" to meet ToP obligations. | US-Asia exports increased 22% to 29 MT (Energy Desk 2024). | ✅ Confirmed |
| A4 | JKM-TTF spread will widen precisely enough to compensate for incremental Cape route costs—acting as rational price compensation. | JKM-TTF spread expanded from $0.6 to $1.3/MMBtu, matching Cape route incremental cost (Data Insights 2024). | ✅ Confirmed |
| A5 | H1 2024 freight rates will remain suppressed despite massive rerouting—new vessel deliveries (60+ ships) will absorb incremental ton-mile demand. | Spark25S/30S hovered at $20k-$70k/day in H1 2024, far below crisis expectations (Data Insights 2024). | ✅ Confirmed |
| A6 | When the vessel delivery buffer is exhausted, freight rates will spike violently as underlying tightness is exposed. | Q4 2024: Spark30S surged to $182k/day driven by European congestion + floating storage arbitrage (Data Insights 2024). | ✅ Confirmed |
| A7 | JERA and KOGAS will engage in physical cargo swaps as the unique mathematical solution to the intersection of their constraint sets (JERA: excess near-term, deficit long-term; KOGAS: deficit near-term, supply en route). | JERA-KOGAS MOU signed April 2023; physical swap execution confirmed during constraint period (Energy Desk 2024). | ✅ Confirmed |
| A8 | Japanese utilities will set resale records by exploiting structural long-term surplus during constrained periods. | Japan resold a record 38.25 MT overseas in FY2023, equivalent to 37% of domestic consumption (Energy Desk 2024). | ✅ Confirmed |

**Layer 1 Summary**: 8/8 inferences confirmed. The constraint reasoning framework correctly identified the dominant behavioral drivers in the Panama Canal single-bottleneck scenario.

---

## Part B: Layer 2 Framework Application (post 2026.2.28)

Inferences generated in early March 2026 by transferring the Layer 1 constraint reasoning logic to the Hormuz multi-bottleneck crisis. Classified by epistemic status at time of analysis.

### JERA (Second Pass / Induced Binding)

| ID | Inference | Classification | Status (2026.3.13) | Verification Source |
|:---|:---|:---|:---|:---|
| B1 | Standard procurement channels remain intact; JERA avoids distressed spot market. May hold position or act as net reseller if US FOB / Australian flexible volumes allow arbitrage. | **(F)** Constraint model: Intact physical supply + elevated JKM → hold/resale capacity rather than distressed procurement | ⏳ Pending | JKM spot vs. long-term contract pricing; JERA procurement disclosures |
| B2 | Activation of JERA-KOGAS physical swap mechanism, but on highly asymmetric terms favoring JERA's surplus position | **(F)** Layer 1 validated behavior transferred to new constraint configuration with altered bargaining power | ⏳ Pending | Cargo tracking (Kpler/SynMax); JERA-KOGAS public statements |
| B3 | METI may proactively coordinate inter-utility reallocation to support highly exposed Asian buyers; JERA participates as surplus holder | **(F)** Institutional calendar: Supply cutoff driven regulatory intervention | ⏳ Pending | METI press releases; Japanese energy press |
| B4 | First-pass distressed procurement (e.g., KOGAS) forces JKM >$22.50. (Note: JKM elevation was already observable; the framework's independent contribution is attributing the surge mechanism to first-pass distressed procurement rather than speculative premium.) | **(F)** Internal market clearing mechanism driven by First Pass players | ✅ Observed (pre-existing) | Platts JKM assessment |
| B5 | Negishi terminal inventory drawdown only exceeds seasonal norm IF severe oil price spike ($100+ Brent) triggers domestic gas-to-power switching | **(F)** Conditional inference; JERA's physical supply routes are unaffected by Hormuz | ⏳ Pending | METI weekly petroleum statistics |
| B6 | Localized marginal spot premium costs appearing in FY2025/2026 earnings, but lacking systemic IFRS time-lag losses | **(F)** Institutional calendar: procurement cost recognition limited to marginal spot volumes | ⏳ Pending May 2026 | JERA annual report (expected May 2026) |

### KOGAS (First Pass / Direct Binding)

| ID | Inference | Classification | Status (2026.3.13) | Verification Source |
|:---|:---|:---|:---|:---|
| B7 | Price-insensitive spot procurement triggered by UGBA legal floor proximity | **(F)** Institutional constraint: UGBA Article 10-10 → behavioral override of price rationality | ⏳ Pending | KOGAS procurement data; Korean energy press |
| B8 | Acceptance of asymmetric terms in JERA swap arrangements | **(F)** Constraint intersection: KOGAS direct physical deficit vs JERA induced pricing → asymmetric cooperative behavior | ⏳ Pending | Bilateral trade flow data |
| B9 | Acceleration of 70% FOB domestic-carrier mandate | **(E)** Policy signals already visible at time of analysis | ✅ Enacted (MOF/MOTIE) | Strategy Group 2024 report |
| B10 | KOGAS inventory days approach 37-day UGBA statutory threshold | **(F)** Physical drawdown model: post-winter nadir + direct supply cutoff | ⏳ Pending | KOGAS monthly inventory reports |
| B11 | MOTIE activates elevated energy emergency protocols | **(F)** Institutional trigger: UGBA 7-day consecutive violation → mandatory protocol activation | ⏳ Pending | MOTIE official announcements |

### Chinese SOEs (Buffered First Pass)

| ID | Inference | Classification | Status (2026.3.13) | Verification Source |
|:---|:---|:---|:---|:---|
| B12 | Structurally lower urgency than Japan/Korea; limited distressed spot participation | **(F)** Diversification structure: pipeline + domestic + storage buffers → lower single-node failure exposure | ⏳ Pending | Chinese SOE procurement patterns; spot market data |
| B13 | Primary response via pipeline maximization (Power of Siberia, Central Asia) + storage drawdown | **(F)** Physical topology: alternative supply edges available in Chinese subgraph | ⏳ Pending | Pipeline flow data (IEF/CNPC disclosures) |
| B14 | Limited, targeted industrial gas rationing with residential supply preserved | **(F)** NDRC institutional logic: residential stability mandate overrides industrial efficiency | ⏳ Pending | Chinese provincial energy reports; media monitoring |
| B15 | Q1 profit margin compression for CNOOC/Sinopec/CNPC without distress debt issuance | **(F)** Cost absorption model: SOEs absorb elevated procurement costs to maintain domestic price stability | ⏳ Pending Q1 reports | SOE quarterly earnings (expected April-May 2026) |

### Part B Summary

| Classification | Count | Confirmed | Pending | Disconfirmed |
|:---|:---|:---|:---|:---|
| **(F)** Framework-derived | 13 | 0 | 13 | 0 |
| **(E)** Informed extrapolation | 2 | 2 | 0 | 0 |
| **Total** | 15 | 2 | 13 | 0 |

**Note on the two confirmed (E) items**: JKM >$22.50 and the 70% FOB mandate were already observable at the time of analysis. Their inclusion demonstrates that the framework's output aligns with real-world developments, but they should not be counted as independent validations of predictive power. The 13 pending **(F)** items represent the genuine test of framework portability.

---

## Part C: Forward Predictions (from 2026.3.13)

**These predictions are genuinely forward-looking.** They are committed to this repository on March 13, 2026—18 days before JERA's fiscal year-end and weeks before Q1 earnings season. The git commit timestamp is the immutable record of their creation date.

All items below are classified **(F)** Framework-derived—they follow from the constraint model's logic chain applied to current conditions.

### JERA (Verification window: 2026.3.31 — 2026.5.15)

| ID | Prediction | Verification Deadline | Verification Source | Status |
|:---|:---|:---|:---|:---|
| C1 | Conditional: IF Brent crude sustains >$100 causing domestic gas-to-power switching, Negishi drawdown will exceed normal seasonal usage. If Brent drops below $90, drawdown stays normal | 2026.4.7 (next METI weekly release after FY-end) | METI Weekly Petroleum Statistics (石油統計速報) | ⏳ |
| C2 | JERA FY2025 annual report will show time-lag IFRS procurement losses heavily concentrated in marginal spot trades rather than systemic portfolio failure — estimated impact scaled down to ¥[TBD] billion | 2026.5.15 (earnings release) | JERA Integrated Report / IR presentation | ⏳ |

### KOGAS (Verification window: 2026.3.31 — 2026.5.15)

| ID | Prediction | Verification Deadline | Verification Source | Status |
|:---|:---|:---|:---|:---|
| C4 | KOGAS March-end inventory will fall to within ±2 days of the 37-day UGBA statutory threshold (i.e., between 35-39 days) | 2026.4.15 (monthly inventory disclosure) | KOGAS monthly operations report; Korean Gas Union statistics | ⏳ |
| C5 | KOGAS Q1 2026 uncollected receivables (미수금) will increase by >30% year-over-year, driven by the price inversion spread | 2026.5.15 (Q1 earnings) | KOGAS quarterly financial statements | ⏳ |
| C6 | MOTIE will formally activate Stage 2 or higher energy emergency protocols before March 31, OR KOGAS will publicly disclose emergency procurement measures | 2026.3.31 | MOTIE official announcements; Korean energy press | ⏳ |

### Chinese SOEs (Verification window: 2026.4.30)

| ID | Prediction | Verification Deadline | Verification Source | Status |
|:---|:---|:---|:---|:---|
| C7 | March 2026: no large-scale residential natural gas supply disruption in China (limited industrial rationing does not count) | 2026.4.15 | Chinese provincial government reports; NDRC announcements; media monitoring | ⏳ |
| C8 | CNOOC, Sinopec, CNPC Q1 2026 upstream profit margins will compress by >5 percentage points year-over-year, but no distress-level debt issuance will occur | 2026.5.15 (Q1 earnings) | SOE quarterly earnings; bond issuance records | ⏳ |

### Market-wide (Verification window: 2026.3.31)

| ID | Prediction | Verification Deadline | Verification Source | Status |
|:---|:---|:---|:---|:---|
| C9 | JKM closing price on March 31, 2026 will remain above $20/MMBtu (crisis premium sustained through JERA fiscal year-end) | 2026.3.31 | Platts JKM daily assessment | ⏳ |
| C10 | Spark25S/30S weekly average will remain above $150,000/day for the duration of March 2026 | 2026.3.31 | Spark Commodities weekly index | ⏳ |

### Part C Summary

| Category | Count | Earliest Verification | Latest Verification |
|:---|:---|:---|:---|
| JERA | 2 | 2026.3.31 | 2026.5.15 |
| KOGAS | 3 | 2026.3.31 | 2026.5.15 |
| Chinese SOEs | 2 | 2026.4.15 | 2026.5.15 |
| Market-wide | 2 | 2026.3.31 | 2026.3.31 |
| **Total** | **9** | **2026.3.31** | **2026.5.15** |

---

## Verification Protocol

1. **Weekly updates**: This scorecard will be updated weekly until 2026.3.31, then monthly through earnings season.
2. **Status values**: ✅ Confirmed | ⚠️ Partially confirmed | ❌ Disconfirmed | ⏳ Pending
3. **Evidence standard**: Each status change must cite a specific public data source with date.
4. **Honesty commitment**: Disconfirmed predictions will be analyzed for root cause—was the framework logic wrong, or was the input data wrong? Both outcomes generate learning value.

---

## Epistemic Position Statement

**Layer 1** (Part A) is a genuine historical backtest. The framework's constraint reasoning logic was applied to fully resolved data from the 2023-2024 Panama Canal drought. 8/8 inferences were confirmed.

**Layer 2** (Part B) is a real-time framework application, not a prediction exercise. The analysis was conducted in early March 2026, after the Hormuz crisis was already underway. Its value lies in demonstrating that the constraint reasoning logic built for a single-bottleneck canal scenario could be transferred to a structurally different multi-bottleneck crisis within days and produce falsifiable inferences. Two items classified as **(E)** were already observable and should not be counted as independent validations.

**Forward Predictions** (Part C) are genuinely prospective. They were committed to this repository on 2026-03-13 and will be verified against public data as it becomes available. These represent the framework's first true forward prediction track record.

The combined evidence structure—historical backtest (Layer 1) + framework portability demonstration (Layer 2) + forward predictions (Part C)—provides a three-tier validation of the LNG-Market-Topology framework's analytical utility.
