# Business Understanding — Cloud Cost Optimization Analysis

## 1. Business Context

A mid-to-large technology company operates a multi-cloud infrastructure spanning **AWS, Azure, and Google Cloud Platform (GCP)**. The company's cloud footprint serves five business units — Finance, Marketing, HR, Engineering, and Sales — each running workloads across production, staging, and development environments.

Over the course of 2023, the company observed a **steady escalation in cloud spending**, with monthly net costs rising from approximately **$29,900 in January to $41,400 in December** — a **38.5% increase** within a single fiscal year. Leadership suspects that a significant portion of this growth is **avoidable**, driven by idle resources, poor commitment coverage, non-production environment sprawl, and inconsistent cost governance across departments.

The Chief Financial Officer (CFO) and VP of Engineering have jointly commissioned this analysis to identify actionable opportunities for cost reduction without compromising operational capabilities.

## 2. Stakeholder Needs

| Stakeholder | Role | Primary Need |
|---|---|---|
| **CFO / Finance Team** | Budget owners | Visibility into departmental cost accountability; identify budget overruns and forecast accuracy |
| **VP of Engineering** | Infrastructure owner | Pinpoint idle/underutilized resources; optimize commitment coverage (RIs, Savings Plans) |
| **Department Heads** | Team leads (Mobile, BI, DataPlatform, Security, WebApps) | Understand their team's cloud consumption relative to peers; justify spend |
| **Cloud FinOps Team** | Cost governance | Standardized KPIs for cost efficiency; anomaly detection for unusual spikes |
| **CTO** | Strategic decision-maker | Multi-cloud cost comparison to inform provider strategy |

## 3. Project Objectives and Scope

### Objectives
1. **Quantify avoidable cloud spending** by identifying idle resources, underutilized commitments, and non-production environment waste.
2. **Build cost-efficiency KPIs** that enable ongoing monitoring of cloud financial health.
3. **Compare departmental and business-unit spending** to establish accountability and benchmarking.
4. **Detect abnormal cost spikes** and their root causes.
5. **Deliver an executive dashboard** that empowers finance and engineering leaders to locate waste and prioritize optimization.

### Scope
- **In scope**: Analysis of daily cloud billing records for all of 2023 (54,750 records across 10 accounts, 15 projects, 3 providers, 7 service categories, and 9 resource types).
- **Out of scope**: Real-time monitoring system implementation; contract renegotiation with cloud providers; application-level performance optimization.

## 4. Key Business Questions

| # | Business Question | Analysis Approach |
|---|---|---|
| 1 | **Which departments and business units are the largest cloud spenders?** | Aggregate net_cost by business_unit and department; rank by total and per-unit cost |
| 2 | **How much of the total spend goes to non-production environments (staging/dev)?** | Segment costs by environment; calculate non-prod as % of total |
| 3 | **Are there idle or underutilized resources?** | Analyze on_demand_cost ratio, low usage_quantity with high cost, spot_savings = 0 patterns |
| 4 | **What is the company's commitment coverage (RIs + Savings Plans)?** | Evaluate savings_plan_coverage_pct and reserved_instance_coverage_pct distributions |
| 5 | **Where are the biggest discount optimization opportunities?** | Compare discount_rate_pct across providers, services, and departments |
| 6 | **Are there abnormal monthly cost spikes?** | Time-series analysis of monthly trends; anomaly scoring; forecast vs actual comparison |
| 7 | **Which cloud provider delivers the best cost-efficiency per service type?** | Cross-tabulate net_cost/usage_quantity by provider and service |
| 8 | **How accurate are cost forecasts?** | Compare forecast_monthly_cost to actual net_cost aggregations |
| 9 | **Which projects consume the most budget relative to their allocation?** | Rank projects by budget_utilization_pct and absolute net_cost |
| 10 | **What is the regional cost distribution?** | Analyze cost by region to identify geographic optimization opportunities |

## 5. Measurable Data Analysis Outcomes

1. **Identify ≥ 15% of total annual spend** (~$61,000+) as potentially optimizable through specific recommendations.
2. **Rank all 5 business units** and **5 departments** by cost-efficiency KPIs with statistical backing.
3. **Flag the top 10 most wasteful resource-project combinations** with quantified savings potential.
4. **Detect and explain** any months with cost growth exceeding 10% month-over-month.
5. **Deliver a live interactive dashboard** with ≥ 5 filter dimensions enabling self-service exploration by finance and engineering leaders.
6. **Provide ≥ 8 actionable, data-backed recommendations** with estimated business impact.
