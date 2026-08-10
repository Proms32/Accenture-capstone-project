# Business Insights Report — Cloud Budget 2023

## Overview

This report translates the data patterns identified in the Exploratory Data Analysis into actionable business insights. Each insight is prioritized by estimated business impact and supported by specific data evidence.

---

## Insight 1: The Company Is Losing $90,380/Year to Non-Production Environments

**Priority: HIGH | Estimated Annual Savings: $45,000–$63,000**

**Pattern**: Staging and development environments account for **22.2% of total cloud spend** ($66,783 staging + $23,597 dev = $90,380). While some non-production spend is necessary for testing and development, industry benchmarks suggest non-production should typically consume 10–15% of total cloud spend.

**Evidence**:
- Staging alone consumes **16.4%** of total spend — higher than the typical 8–10% benchmark.
- Dev environments run 24/7 despite likely being used only during business hours (8–12 hours/day).
- Weekend spending patterns show no significant reduction for non-production resources (28.8% of records are weekends, proportionally equal to weekday records).

**Business Impact**: If staging environments were shut down outside business hours (saving ~60% of staging costs) and dev environments followed a similar schedule, the company could save **$45,000–$63,000 annually** — representing 11–15% of total spend.

**Root Cause**: Lack of automated scheduling policies for non-production resource lifecycle management.

---

## Insight 2: Low Commitment Coverage Creates $40,000+ in Avoidable On-Demand Costs

**Priority: HIGH | Estimated Annual Savings: $40,000–$55,000**

**Pattern**: The average total commitment coverage (Savings Plans + Reserved Instances) is only **54.1%**, meaning nearly half of all usage is charged at full on-demand rates. Additionally, **8.4% of resource records have both SP and RI coverage below 15%/10%**, representing complete exposure to premium pricing.

**Evidence**:
- Average on-demand exposure is **46.5%** — nearly half of all costs come from uncommitted resources.
- Reserved savings contribute only **4.96%** of net cost on average.
- Savings Plan savings contribute only **6.4%** of net cost on average.
- Total commitment savings (RI + SP + Spot) are $53,604 — just 10.2% of list cost.

**Business Impact**: Increasing commitment coverage from 54% to 75% (a realistic 21-point improvement) for production workloads could save **$40,000–$55,000 annually** at typical 25–30% commitment discounts.

**Root Cause**: Decentralized commitment purchasing across departments with no centralized FinOps governance.

---

## Insight 3: Q4 Spending Surge Signals Resource Accumulation Without Cleanup

**Priority: HIGH | Estimated Annual Savings: $15,000–$20,000**

**Pattern**: Monthly spending increased sharply in Q4: October ($32,675) → November ($40,588, +24.2%) → December ($41,402, +2.0%). This represents a **38.5% increase from January to December**, far exceeding typical organic growth.

**Evidence**:
- All 5 business units show synchronized Q4 growth (Chart 15).
- The spike is not driven by a single department or provider.
- No corresponding increase in `usage_quantity` proportional to cost increase, suggesting price escalation or resource sprawl rather than workload growth.

**Business Impact**: The Q4 spike adds approximately $15,000–$20,000 in extra monthly costs. If resources created in Q4 are not decommissioned post-project, this elevated baseline carries into the next fiscal year, compounding the cost problem.

**Root Cause**: Year-end project sprints create resources that are not decommissioned after projects conclude. Absence of resource lifecycle policies and automated cleanup triggers.

---

## Insight 4: Spot Instance Adoption Is Nearly Zero — Missing 20–60% Savings on Eligible Workloads

**Priority: MEDIUM | Estimated Annual Savings: $10,000–$25,000**

**Pattern**: **75% of resource records show $0 in spot savings**, indicating near-zero adoption of spot/preemptible instances across the organization. Spot instances can provide 20–60% cost savings for fault-tolerant workloads.

**Evidence**:
- Only 25% of records show any spot savings, and even those are minimal ($0–$3.60 per record).
- Container workloads (15.3% of spend, $62,484) and Serverless workloads (11.3%, $46,086) are strong spot candidates.
- Batch analytics workloads (18.9% of spend, $77,120) could partially run on spot instances.

**Business Impact**: If just 20% of eligible workloads (Container + portions of Compute/Analytics) were migrated to spot instances, the company could save **$10,000–$25,000 annually** at a 30% average discount.

**Root Cause**: Engineering teams may lack tooling or confidence in spot instance reliability. No organizational incentive or playbook for spot adoption.

---

## Insight 5: All Departments Have Similar Waste Profiles — Systemic Problem

**Priority: MEDIUM | Strategic Importance: HIGH**

**Pattern**: Unlike typical organizations where one or two departments drive most waste, all five departments and all five business units show nearly identical spending patterns ($78K–$83K range), cost efficiency ratios, and idle resource rates (~11%).

**Evidence**:
- Department spending range: $78,597 (BI) to $82,711 (Mobile) — only 5% variance.
- Business unit spending range: $78,729 (Engineering) to $82,745 (Finance) — only 5% variance.
- Idle resource rates: 10.7% (lowest) to 11.8% (highest) — minimal variance.
- Cost efficiency ratio distributions are nearly identical across departments (Chart 9).

**Business Impact**: This finding means that targeted department-level interventions will have limited impact. The company needs **organization-wide policy changes** — centralized commitment purchasing, standardized resource lifecycle policies, and unified FinOps governance.

**Root Cause**: Uniform infrastructure provisioning patterns across teams suggest shared templates, scripts, or default configurations that embed waste into every deployment.

---

## Insight 6: Forecasting Accuracy Is Poor — Budget Planning Is Undermined

**Priority: MEDIUM | Estimated Impact: Improved Planning Accuracy**

**Pattern**: The `forecast_monthly_cost` values diverge significantly from actual costs. The forecast column shows extreme outliers (max $959.98 vs. median $12.97), and the forecast-vs-actual scatter plot shows weak correlation. Additionally, `budget_utilization_pct` is always below 4%, and `budget_status` is always "under" — suggesting budgets are set at granularities that don't match actual cost patterns.

**Evidence**:
- Forecast outliers: 5,775 records (10.5%) flagged as forecast outliers.
- Budget utilization is always below 4% (daily cost vs. monthly budget comparison).
- Zero records ever exceeded their budget allocation.
- No correlation between forecast direction and actual cost trends.

**Business Impact**: Poor forecasting means finance teams cannot plan infrastructure budgets accurately. Over-budgeting wastes capital allocation, while under-budgeting creates surprise cost escalations.

**Root Cause**: Forecast models may not incorporate seasonal trends, commitment coverage changes, or resource lifecycle patterns.

---

## Insight 7: AWS Costs 3–10% More Than Comparable Azure/GCP Deployments

**Priority: LOW–MEDIUM | Estimated Annual Savings: $5,000–$10,000**

**Pattern**: AWS accounts for **35.1%** of total spend despite supporting a similar workload share as Azure (32.9%) and GCP (32.0%). The cost premium is consistent across services and regions.

**Evidence**:
- AWS: $143,329 (35.1%) — higher by $9K–$13K compared to other providers.
- GCP shows the highest average discount utilization (Chart 10).
- The AWS cost premium persists even after normalizing for usage quantity.

**Business Impact**: Evaluating workload placement across providers for cost-optimal deployment could save **$5,000–$10,000 annually**. Some workloads may benefit from migration to the most cost-effective provider for that specific service type.

**Root Cause**: Historical provider preferences, vendor lock-in, or different pricing tiers across providers.

---

## Insight 8: 11.3% of Resource-Days Show Idle/Under-Committed Patterns

**Priority: MEDIUM | Estimated Annual Savings: $8,000–$15,000**

**Pattern**: Approximately **6,203 resource-day records (11.3%)** have on-demand exposure exceeding 80%, indicating resources running without meaningful commitment coverage. These are either truly idle (running but unused) or deployed without cost optimization.

**Evidence**:
- WebApps department has the highest idle rate (11.8%), BI the lowest (10.7%).
- Idle resources span all providers and regions proportionally.
- Idle resources in staging and dev environments are particularly wasteful.

**Business Impact**: Identifying and right-sizing or terminating idle resources could save **$8,000–$15,000 annually**. Even a 50% reduction in idle resource-days would yield meaningful savings.

**Root Cause**: Lack of automated idle resource detection and alerting. No accountability mechanism for un-tagged or unmonitored resources.

---

## Insight Priority Matrix

| Priority | Insight | Estimated Savings | Effort | Quick Win? |
|---|---|---|---|---|
| **P1** | Non-production scheduling | $45K–$63K | Medium | Yes |
| **P1** | Increase commitment coverage | $40K–$55K | Medium | No |
| **P1** | Q4 resource cleanup | $15K–$20K | Low | Yes |
| **P2** | Spot instance adoption | $10K–$25K | High | No |
| **P2** | Idle resource detection | $8K–$15K | Medium | Yes |
| **P2** | Improve forecasting | Planning accuracy | High | No |
| **P2** | Systemic FinOps governance | Foundation for all above | High | No |
| **P3** | Multi-cloud cost arbitrage | $5K–$10K | High | No |

**Total Estimated Annual Savings Potential: $123,000–$188,000 (30–46% of current spend)**
