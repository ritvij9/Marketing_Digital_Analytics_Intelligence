# Marketing & Digital Analytics Intelligence
## Business Findings and Recommendations

**Analysis period:** 1–7 January 2021  
**Data source:** Google Analytics 4 public ecommerce sample dataset  
**Analysis grain:** Sessions, using the available session identifier  
**Status:** Observational analysis; recommendations require further validation

---

## 1. Executive Summary

This analysis examines session activity, ecommerce funnel-event coverage, and conversion rates across acquisition categories in the GA4 public ecommerce sample.

The local extract contains 245,209 event records and 26,331 distinct session keys. Across these sessions, 136 sessions contained at least one purchase event, giving an observed session conversion rate of approximately **0.52%**.

Observed conversion rates vary across acquisition categories. However, the available acquisition fields represent **first-user traffic-source information**, not verified session-level attribution or causal marketing impact. The dataset also lacks marketing spend, so return on ad spend (ROAS), customer acquisition cost (CAC), and budget efficiency cannot be calculated reliably.

The strongest immediate business opportunity is therefore to improve measurement quality and investigate unusual conversion patterns before making channel-allocation decisions.

## 2. Key Findings

### Finding 1 — Overall session conversion is low in the observed sample

| Metric | Observed result |
|---|---:|
| Event records | 245,209 |
| Distinct session keys | 26,331 |
| Sessions containing a purchase event | 136 |
| Sessions without a purchase event | 26,195 |
| Session conversion rate | 0.5165% |

**Interpretation:** Approximately 5.2 sessions per 1,000 contained a purchase event.

This is a descriptive benchmark for the selected seven-day sample. It should not automatically be treated as the site's long-term conversion baseline or compared with external benchmarks without matching definitions, traffic mix, and observation windows.

### Finding 2 — Funnel-event coverage identifies areas for investigation

| Event | Sessions containing the event |
|---|---:|
| page_view | 24,998 |
| view_item | 3,944 |
| add_to_cart | 803 |
| begin_checkout | 301 |
| add_shipping_info | 301 |
| add_payment_info | 192 |
| purchase | 136 |

These counts measure sessions containing each event. They are **not a validated sequential funnel**: the current analysis does not establish that every session progressed through the stages in the displayed order.

**Business implication:** Cart, checkout, shipping, and payment behaviour deserve further investigation. Before quantifying stage-level abandonment, build a session-event sequence model with explicit ordering, eligibility, and time-window rules.

### Finding 3 — Google organic and direct have similar observed conversion rates

| First-user acquisition category | Sessions | Converting sessions | Conversion rate | 95% Wilson CI |
|---|---:|---:|---:|---:|
| google / organic / (organic) | 8,620 | 43 | 0.499% | 0.371–0.671% |
| (direct) / (none) / (direct) | 6,168 | 32 | 0.519% | 0.368–0.731% |

The observed rates are close, and the confidence intervals overlap substantially.

**Business implication:** This evidence does not justify reallocating resources between these categories. Further comparisons should use validated session-attribution fields, consistent reporting windows, and a clearly defined comparison method.

### Finding 4 — A data-deleted category has an elevated observed rate

| Metric | Result |
|---|---:|
| Sessions | 1,159 |
| Converting sessions | 20 |
| Conversion rate | 1.726% |
| 95% Wilson CI | 1.120–2.650% |

This category has a higher observed conversion rate than the overall sample. However, its label indicates that the underlying acquisition information is unavailable or deleted.

**Business implication:** Treat this as a measurement-investigation lead, not as a high-performing marketing channel. Investigate why this category exists and whether the underlying traffic can be identified legitimately.

### Finding 5 — Some small categories produce highly uncertain rates

The category `(data deleted) / (data deleted) / <Other>` contains only 25 sessions and one converting session. Its observed conversion rate is 4.0%, but its 95% Wilson confidence interval is approximately 0.71–19.54%.

Another category contains 16 sessions and no converting sessions; its 95% interval extends to approximately 19.36%.

These wide intervals show why ranking acquisition categories by observed conversion rate alone can be misleading.

The 200-session threshold used in the analysis is a screening heuristic. It does not guarantee adequate statistical power or establish statistical significance.

### Finding 6 — Marketing efficiency cannot be evaluated from the current data

The available extract does not contain marketing spend or cost at a suitable channel/campaign grain.

Consequently, this analysis cannot reliably calculate:

- Return on ad spend (ROAS)
- Customer acquisition cost (CAC)
- Cost per click or cost per acquisition
- Incremental revenue attributable to marketing
- The marginal return from increasing or reducing a budget

Purchase events and revenue fields can support transaction-level validation, but observed revenue alone does not establish channel profitability or incremental marketing impact.

## 3. Recommended Actions

### Priority 1 — Investigate acquisition measurement quality

**Evidence:** Acquisition categories include data-deleted and other placeholder values. Event-level acquisition parameters also varied within some sessions in the diagnostic analysis.

**Action:** Document the provenance and intended meaning of each acquisition field. Inspect tracking implementation and available GA4 traffic-source dimensions before selecting a session-attribution model.

**Risk:** Incorrect attribution can lead to misallocated budgets and misleading performance comparisons.

**Success measure:** A documented attribution definition, field-coverage report, and reconciliation between source data and the selected analytical model.

### Priority 2 — Build a validated sequential funnel

**Evidence:** Current event-presence counts show substantially fewer sessions containing `add_to_cart` than `view_item`, but the current output does not establish sequential progression.

**Action:** Build session-level event sequences, validate event timestamps and ordering, define stage eligibility, and calculate stage-to-stage conversion using explicit denominators.

**Success measure:** Reconciled stage counts, validated event-order rules, and documented stage-level conversion rates.

### Priority 3 — Validate purchase and revenue metrics

**Evidence:** The source-level validation found 144 purchase events, 138 events with an event-parameter transaction ID, and 136 distinct event-parameter transaction IDs. The event value and ecommerce purchase-revenue sums both equalled USD 7,982 in the checked extract.

**Action:** Investigate the purchase events missing transaction IDs and repeated transaction identifiers. Distinguish repeated events from genuinely separate orders before applying any deduplication rule.

**Success measure:** A documented purchase-count and revenue reconciliation with explicit treatment of missing and repeated identifiers.

### Priority 4 — Connect spend data before evaluating budget efficiency

**Evidence:** Marketing cost is not available in the current dataset.

**Action:** Identify a legitimate source for campaign spend, clicks, and impressions. Confirm join keys, reporting windows, currency, and aggregation grain before joining costs to conversion or revenue data.

**Success measure:** Reconciled cost and outcome metrics at a defensible channel/campaign grain.

### Priority 5 — Plan a controlled experiment for causal questions

**Evidence:** The current analysis is observational and does not contain validated randomized experiment assignments.

**Action:** If the business wants to know whether a marketing intervention causes incremental conversions, define a controlled experiment with a prespecified outcome, randomization unit, sample-size calculation, observation window, and analysis plan.

**Success measure:** A documented experiment proposal with measurable outcomes and a defensible method for estimating treatment effects.

## 4. Statistical Interpretation

The confidence intervals in this report are 95% Wilson intervals for individual observed conversion proportions.

They describe uncertainty in each category's observed conversion rate under the interval method's assumptions. They are not, by themselves, formal tests of differences between categories.

The overall conversion rate includes the categories being compared, so comparisons against that overall rate are not independent. Overlapping intervals are also not a substitute for a properly designed comparison test.

No causal lift, budget optimization, or statistically significant channel ranking is claimed.

## 5. Limitations

1. The observation window covers only seven days in January 2021.
2. The data comes from a public GA4 sample and may not represent a live business's current traffic.
3. The acquisition fields used here describe first-user traffic source, not verified session-level attribution.
4. Placeholder categories such as `<Other>` and `(data deleted)` limit business interpretability.
5. The event-presence summary is not yet a validated sequential funnel.
6. Marketing spend is unavailable, preventing reliable ROAS and CAC analysis.
7. The analysis does not establish causal effects or incremental conversions.
8. Small conversion counts produce wide confidence intervals, limiting ranking and decision-making.

## 6. Decision Summary

| Decision area | Current recommendation | Evidence status |
|---|---|---|
| Shift budget between organic and direct | Do not recommend a shift based on these results | Insufficient evidence |
| Investigate data-deleted acquisition traffic | Prioritize measurement investigation | Descriptive signal |
| Quantify funnel abandonment | Build a validated sequential funnel first | Current counts are insufficient |
| Evaluate ROAS and CAC | Obtain and validate spend data first | Not calculable from current extract |
| Claim incremental marketing impact | Design a controlled experiment | Not established |
| Use conversion confidence intervals | Retain as uncertainty reporting | Implemented and tested |

## 7. Conclusion

The current analysis establishes a reproducible descriptive baseline and identifies measurement and funnel questions that merit further work.

Its principal business value is not declaring a winning channel. It is showing which conclusions the available data supports, which conclusions remain uncertain, and what additional measurement is required to make defensible marketing decisions.