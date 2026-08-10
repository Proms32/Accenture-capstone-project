# Data Understanding — Cloud Budget 2023 Dataset

## 1. Dataset Overview

| Property | Value |
|---|---|
| **Source File** | `cloud_budget_2023_dataset.csv` |
| **Total Records** | 54,750 |
| **Total Columns** | 40 |
| **Date Range** | January 1, 2023 – December 31, 2023 (full calendar year) |
| **Granularity** | Daily resource-level billing records |
| **File Size** | ~18 MB |
| **Currency** | USD (single currency) |
| **Duplicates** | 0 |
| **Missing Values** | 0 (all columns fully populated) |

Each row represents one day's billing record for a specific resource within a specific project, account, and cloud provider.

## 2. Data Dictionary

### 2.1 Date & Calendar Dimensions

| Column | Type | Description | Example |
|---|---|---|---|
| `date` | string | Full date of the billing record (YYYY-MM-DD) | 2023-01-01 |
| `year` | int | Year extracted from date | 2023 |
| `month` | int | Month number (1–12) | 1 |
| `day` | int | Day of month (1–31) | 1 |
| `day_of_week` | int | Day of week (0=Monday, 6=Sunday) | 6 |
| `is_month_start` | int | Binary flag: 1 if first day of month | 1 |
| `is_month_end` | int | Binary flag: 1 if last day of month | 0 |

### 2.2 Organizational Dimensions

| Column | Type | Unique Values | Description | Values |
|---|---|---|---|---|
| `cloud_provider` | string | 3 | Cloud service provider | AWS, Azure, GCP |
| `account_id` | string | 10 | Cloud account identifier | acct-001 to acct-010 |
| `project_id` | string | 15 | Project identifier within an account | project-001 to project-015 |
| `environment` | string | 3 | Deployment environment | prod, staging, dev |
| `business_unit` | string | 5 | Business unit owning the resource | Finance, Marketing, HR, Engineering, Sales |
| `department` | string | 5 | Department/team within the business unit | Mobile, BI, DataPlatform, Security, WebApps |
| `cost_center` | string | 10 | Accounting cost center code | CC-1001 to CC-1010 |
| `region` | string | 6 | Cloud data center region | us-west-2, us-east-1, ap-south-1, eu-west-1, eu-central-1, ap-southeast-1 |

### 2.3 Service & Resource Dimensions

| Column | Type | Unique Values | Description | Values |
|---|---|---|---|---|
| `service` | string | 7 | Cloud service category | Serverless, Container, Database, Compute, Storage, Analytics, Networking |
| `resource_type` | string | 9 | Specific resource type | VM, RDS, NoSQL, ObjectStorage, BlockStorage, LoadBalancer, LambdaFunction, KubernetesCluster, DataWarehouse |

### 2.4 Usage Metrics

| Column | Type | Description | Range |
|---|---|---|---|
| `usage_quantity` | float | Amount of resource consumed | 2.32 – 285.35 |
| `usage_unit` | string | Unit of measurement for usage | vCPU-hours, GB-month, DB-hours, request-million, container-hours, query-hours, GB |

### 2.5 Cost Metrics (Core Billing Flow)

The cost flow follows: **List Cost → Discounts → Net Cost**

| Column | Type | Description | Range |
|---|---|---|---|
| `list_cost` | float | Full on-demand/list price before any discounts | $0.20 – $42.69 |
| `savings_plan_coverage_pct` | float | % of usage covered by Savings Plans | 0.00 – 0.70 |
| `reserved_instance_coverage_pct` | float | % of usage covered by Reserved Instances | 0.00 – 0.60 |
| `discount_rate_pct` | float | Overall discount rate applied | 0.05 – 0.40 |
| `discount_amount` | float | Total dollar discount applied | $0.01 – $16.71 |
| `net_cost` | float | **Final cost after all discounts** (primary cost metric) | $0.14 – $38.01 |
| `on_demand_cost` | float | Portion paid at on-demand rates (no commitment) | $0.00 – $31.84 |
| `reserved_savings` | float | Savings from Reserved Instances | $0.00 – $6.02 |
| `savings_plan_savings` | float | Savings from Savings Plans | $0.00 – $7.42 |
| `spot_savings` | float | Savings from Spot/Preemptible instances | $0.00 – $3.60 (75% are zero) |
| `amortized_cost` | float | Cost with upfront payments spread over time | $0.14 – $34.76 |

### 2.6 Budget & Forecasting

| Column | Type | Description | Range |
|---|---|---|---|
| `forecast_monthly_cost` | float | Projected monthly cost for this resource | $0.17 – $959.98 |
| `budget_amount` | float | Allocated monthly budget for this resource | $6,800 – $60,000 |
| `budget_utilization_pct` | float | % of budget consumed | 0.00 – 0.04 (very low) |
| `budget_status` | string | Budget status indicator | Always "under" (single value) |

### 2.7 Anomaly & Variance Detection

| Column | Type | Description | Range |
|---|---|---|---|
| `cost_variance_7d_pct` | float | 7-day cost variance percentage | -0.25 to 0.35 |
| `cost_variance_30d_pct` | float | 30-day cost variance percentage | -0.40 to 0.50 |
| `anomaly_score` | float | Computed anomaly score (higher = more anomalous) | 0.01 – 0.69 |
| `is_anomaly` | int | Binary anomaly flag | Always 0 (never flagged) |

### 2.8 Metadata

| Column | Type | Description | Example |
|---|---|---|---|
| `currency` | string | Currency code | Always "USD" |
| `tags` | string | Semicolon-delimited resource tags | team=Mobile;bu=Finance;env=staging;provider=AWS;service=Serverless |

**Tag keys present**: `team`, `bu`, `env`, `provider`, `service`

## 3. Relationships & Cross-References

- **Tags ↔ Columns**: The `tags` field contains redundant information that maps to existing columns (`team` → `department`, `bu` → `business_unit`, `env` → `environment`, `provider` → `cloud_provider`, `service` → `service`). This provides cross-validation opportunity.
- **Account ↔ Project**: Each of the 10 accounts has 15 projects (150 total account-project combinations).
- **Cost Flow**: `list_cost` − `discount_amount` ≈ `net_cost` (primary financial metric).
- **Savings Breakdown**: `reserved_savings` + `savings_plan_savings` + `spot_savings` ≈ portion of total savings from commitments.

## 4. Target KPIs for Analysis

| KPI | Formula | Business Purpose |
|---|---|---|
| **Cost Efficiency Ratio** | net_cost / list_cost | Lower = better discounts; measures overall cost optimization |
| **Discount Utilization Rate** | discount_amount / list_cost | Higher = better at leveraging available discounts |
| **Savings Plan Effectiveness** | savings_plan_savings / net_cost | Contribution of Savings Plans to total cost reduction |
| **RI Effectiveness** | reserved_savings / net_cost | Contribution of Reserved Instances to cost reduction |
| **On-Demand Exposure** | on_demand_cost / net_cost | Higher = more exposed to full pricing; poor commitment coverage |
| **Cost per Usage Unit** | net_cost / usage_quantity | Unit economics; enables cross-service comparison |
| **Budget Headroom** | budget_amount − forecast_monthly_cost | How much budget remains; negative = over budget |
| **Monthly Spend Growth** | (month_n − month_n-1) / month_n-1 | Month-over-month cost trend |

## 5. Analytical Dimensions

The dataset enables analysis across these dimensions:

1. **Time**: Daily, weekly, monthly, quarterly trends
2. **Organization**: Business unit → Department → Cost center hierarchy
3. **Infrastructure**: Cloud provider → Service → Resource type
4. **Environment**: Production vs. staging vs. development
5. **Geography**: 6 cloud regions across US, Europe, and Asia-Pacific
6. **Financial**: Cost breakdown, discounts, commitments, forecasts, budgets
