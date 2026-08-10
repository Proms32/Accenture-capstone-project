# Cloud Budget 2023 — Capstone Project Implementation Plan

A technology company is experiencing rising cloud bills and wants to identify avoidable spending. This project analyzes VM usage, storage consumption, compute hours, idle resource reports, department ownership, billing tags, and monthly cost data across AWS, Azure, and GCP.

---

## Dataset Overview (Profiling Results)

| Property | Value |
|---|---|
| **Rows** | 54,751 (header + 54,750 records) |
| **Columns** | 40 |
| **Date Range** | 2023-01-01 → 2023-12-31 |
| **Cloud Providers** | AWS, Azure, GCP |
| **Environments** | prod, staging, dev |
| **Business Units** | Finance, Marketing, HR, Engineering, Sales |
| **Departments** | Mobile, BI, DataPlatform, Security, WebApps |
| **Regions** | us-west-2, us-east-1, ap-south-1, eu-west-1, eu-central-1, ap-southeast-1 |
| **Services** | Serverless, Container, Database, Compute, Storage, Analytics, Networking |
| **Resource Types** | VM, RDS, NoSQL, ObjectStorage, BlockStorage, LoadBalancer, LambdaFunction, KubernetesCluster, DataWarehouse |
| **Accounts** | 10 (acct-001 through acct-010) |
| **Projects** | 15 per account (project-001 through project-015) |
| **Duplicates** | 0 |
| **Missing Values** | 0 (all columns fully populated) |
| **Currency** | USD only |
| **Total Annual Net Cost** | ~$407,980 |

---

## Proposed Changes

### 1. Business Understanding (10%)

#### [NEW] [business_understanding.md](file:///Users/yashchaudhary/Desktop/accenrueCapstone/business_understanding.md)
- 1–2 page problem statement document
- Business context: rising cloud costs, multi-cloud sprawl, departmental ownership gaps
- Stakeholder needs: Finance leaders need cost accountability; Engineering leaders need optimization targets
- Key business questions:
  1. Which departments/business units are the biggest cloud spenders?
  2. Are there idle or underutilized resources consuming budget?
  3. Where are the largest cost-optimization opportunities (reserved instances, savings plans)?
  4. Are there abnormal cost spikes that indicate waste or misconfiguration?
  5. How do costs vary across environments (prod vs staging vs dev)?
  6. Which cloud provider delivers the best cost-efficiency for each service type?
- Measurable outcomes: Identify ≥ 20% of spend as optimizable, rank departments by waste ratio

---

### 2. Data Understanding (10%)

#### [NEW] [data_understanding.md](file:///Users/yashchaudhary/Desktop/accenrueCapstone/data_understanding.md)
- Comprehensive data dictionary for all 40 columns
- Explanation of billing dimensions: list_cost → discounts → net_cost flow
- Tag structure analysis (team, bu, env, provider, service)
- Key KPIs to engineer:
  - **Cost Efficiency Ratio** = net_cost / list_cost
  - **Discount Utilization** = discount_amount / list_cost
  - **Savings Plan Effectiveness** = savings_plan_savings / net_cost
  - **Reserved Instance ROI** = reserved_savings / net_cost
  - **Idle Resource Score** = on_demand_cost / net_cost (high ratio = poor commitment coverage)
  - **Budget Headroom** = budget_amount − forecast_monthly_cost
  - **Cost per Usage Unit** = net_cost / usage_quantity

---

### 3. Data Quality Assessment (15%)

#### [NEW] [data_quality_report.md](file:///Users/yashchaudhary/Desktop/accenrueCapstone/data_quality_report.md)

Issues identified during profiling:

| Issue | Count/Details | Impact | Resolution |
|---|---|---|---|
| No null values | 0 missing across all columns | None | N/A |
| No duplicates | 0 duplicates | None | N/A |
| `budget_status` single value | All "under" — no variance | Low analytical value | Document; use budget_utilization_pct instead |
| `is_anomaly` single value | All 0 — never flagged | Needs re-engineering | Derive anomaly flag from anomaly_score threshold |
| `forecast_monthly_cost` outliers | Max 959.98 vs median 12.97 | Skews aggregations | Cap/flag outliers using IQR method |
| `on_demand_cost` zeros | Some rows have 0.0 | May indicate full RI/SP coverage or data gap | Investigate & document |
| Tags are denormalized | Semicolon-delimited string | Hard to filter/group | Parse into separate columns |
| `spot_savings` mostly zero | ~75% are 0.0 | Limited spot adoption | Document as finding |
| `date` is string type | Not datetime | Can't do time-series ops | Convert to datetime |
| Cost variance columns | 7d and 30d have negative values | Expected (cost decreases) | Validate range ±50% |

---

### 4. Data Cleaning & Preprocessing (15%)

#### [NEW] [data_cleaning.py](file:///Users/yashchaudhary/Desktop/accenrueCapstone/data_cleaning.py)

Steps:
1. **Parse date** → proper datetime; extract quarter, week_of_year
2. **Parse tags** → extract into `tag_team`, `tag_bu`, `tag_env`, `tag_provider`, `tag_service` columns
3. **Validate tag consistency** → cross-check `tag_bu` vs `business_unit`, `tag_env` vs `environment`
4. **Standardize resource names** → ensure consistent casing/naming
5. **Derive anomaly flag** → `is_anomaly_derived = anomaly_score > threshold` (e.g., 95th percentile)
6. **Handle outliers** → flag forecast_monthly_cost outliers (IQR method); don't remove, flag for analysis
7. **Engineer KPI features**:
   - `cost_efficiency_ratio` = net_cost / list_cost
   - `discount_utilization` = discount_amount / list_cost
   - `savings_plan_effectiveness` = savings_plan_savings / net_cost
   - `ri_effectiveness` = reserved_savings / net_cost
   - `idle_resource_indicator` = 1 if on_demand_cost / net_cost > 0.8 (high on-demand = no commitment)
   - `cost_per_unit` = net_cost / usage_quantity
   - `quarter` = derived from month
   - `is_weekend` = derived from day_of_week
8. **Export** clean dataset as `cloud_budget_2023_clean.csv`

#### [NEW] [cloud_budget_2023_clean.csv](file:///Users/yashchaudhary/Desktop/accenrueCapstone/cloud_budget_2023_clean.csv)

---

### 5. Exploratory Data Analysis (20%)

#### [NEW] [eda_analysis.py](file:///Users/yashchaudhary/Desktop/accenrueCapstone/eda_analysis.py)

**15+ visualizations planned:**

| # | Type | Visualization | Business Question |
|---|---|---|---|
| 1 | Univariate | Distribution of net_cost (histogram + KDE) | What's the typical daily resource cost? |
| 2 | Univariate | Distribution of usage_quantity by service | Which services consume the most resources? |
| 3 | Univariate | Distribution of anomaly_score | How spread are anomaly risks? |
| 4 | Bivariate | Monthly net_cost trend (line chart) | Is spending trending up? |
| 5 | Bivariate | Net cost by business_unit (bar chart) | Who spends the most? |
| 6 | Bivariate | Net cost by department (bar chart) | Which teams drive costs? |
| 7 | Bivariate | Net cost by cloud_provider (bar chart) | Which provider is most expensive? |
| 8 | Bivariate | Net cost by environment (stacked bar) | How much goes to non-prod? |
| 9 | Bivariate | Cost efficiency ratio by department (box plot) | Who gets worst value for money? |
| 10 | Bivariate | Discount utilization by provider (grouped bar) | Which provider gives best discounts? |
| 11 | Multivariate | Heatmap: net_cost by business_unit × service | Where do costs concentrate? |
| 12 | Multivariate | Cost by region × provider (heatmap) | Regional cost patterns |
| 13 | Multivariate | Savings plan coverage vs RI coverage (scatter) | Commitment strategy gaps |
| 14 | Bivariate | Top 20 projects by total net_cost | Which projects are most expensive? |
| 15 | Time-series | Monthly cost by business_unit (stacked area) | Spending trends by team |
| 16 | Bivariate | Idle resource indicator distribution by dept | Which dept has most idle resources? |
| 17 | Multivariate | Correlation matrix of all numeric KPIs | How do metrics relate? |
| 18 | Bivariate | Forecast vs actual cost comparison | Forecasting accuracy |

#### [NEW] [eda_report.md](file:///Users/yashchaudhary/Desktop/accenrueCapstone/eda_report.md)
- Chart + written insight for each visualization
- Statistical summaries (mean, median, std, percentiles)
- Correlation analysis

---

### 6. Business Insights (10%)

#### [NEW] [business_insights.md](file:///Users/yashchaudhary/Desktop/accenrueCapstone/business_insights.md)
- Evidence-based insights connecting data patterns to business meaning
- Prioritized by business impact (estimated savings potential)
- Key areas: idle resources, commitment coverage gaps, environment waste, department comparisons, cost spike root causes

---

### 7. Dashboard Development (15%)

#### [NEW] [dashboard.py](file:///Users/yashchaudhary/Desktop/accenrueCapstone/dashboard.py)
- **Streamlit** interactive dashboard
- Features:
  - KPI cards: Total Spend, Avg Daily Cost, Savings Rate, Discount Rate, Idle Resource %
  - Filters: Date range, Cloud Provider, Business Unit, Department, Environment, Region, Service
  - Monthly cost trend chart
  - Department/BU comparison charts
  - Provider cost breakdown
  - Top wasteful projects table
  - Cost efficiency leaderboard
  - Anomaly detection view (high anomaly_score resources)
  - Drill-down by clicking on elements

---

### 8. Recommendations (5%)

#### [NEW] [recommendations.md](file:///Users/yashchaudhary/Desktop/accenrueCapstone/recommendations.md)
- Summary table: Recommendation | Data Evidence | Expected Benefit
- Actionable items mapped to specific findings
- Priority ranking (Quick wins vs strategic changes)

---

## User Review Required

> [!IMPORTANT]
> **Dashboard tool choice**: The plan uses **Streamlit** for the dashboard (Python-native, easy to run locally). If you prefer **Power BI** or **Tableau** instead, let me know and I'll adjust.

> [!IMPORTANT]
> **Output format**: The plan creates standalone Python scripts (`.py` files) for data cleaning and EDA, plus Markdown reports for documentation. If you'd prefer **Jupyter Notebooks** (`.ipynb`) for the analysis portions, let me know.

## Open Questions

1. **Anomaly threshold**: The `is_anomaly` column is always 0 and `anomaly_score` ranges 0.01–0.69. Should I define anomalies at the 95th percentile (score > 0.58), or do you have a specific threshold in mind?

2. **Dashboard deployment**: Should the Streamlit dashboard be runnable locally only, or would you like me to set up deployment instructions (e.g., Streamlit Cloud)?

3. **Report format**: Should the deliverable documents (business_understanding, data_quality_report, etc.) be Markdown files, or would you prefer PDFs/Word docs?

---

## Verification Plan

### Automated Tests
- Run `python3 data_cleaning.py` and verify clean CSV has no nulls in derived columns
- Run `python3 eda_analysis.py` and verify all 18 charts are generated as PNG files
- Run `streamlit run dashboard.py` and verify dashboard loads with all filters working

### Manual Verification
- Validate that KPI calculations match manual spot-checks on raw data
- Confirm all 15+ visualizations have accompanying written insights
- Verify dashboard interactivity (filters, drill-downs)
- Cross-check business recommendations against EDA findings
