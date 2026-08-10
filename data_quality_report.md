# Data Quality Assessment Report — Cloud Budget 2023

## 1. Assessment Summary

| Metric | Value |
|---|---|
| **Total Records Assessed** | 54,750 |
| **Total Columns** | 40 |
| **Overall Data Completeness** | 100% (no missing values) |
| **Duplicate Records** | 0 |
| **Issues Identified** | 10 |
| **Critical Issues** | 2 |
| **Moderate Issues** | 4 |
| **Low/Informational Issues** | 4 |

---

## 2. Detailed Issue Register

### Issue 1: `date` Column Stored as String (MODERATE)

| Attribute | Detail |
|---|---|
| **Column** | `date` |
| **Issue** | Date values stored as string type, not datetime |
| **Record Count** | All 54,750 records |
| **Impact** | Cannot perform time-series operations, date arithmetic, or proper chronological sorting without conversion |
| **Resolution** | Convert to `datetime64` type during preprocessing. Extract additional features: `quarter`, `week_of_year`, `is_weekend` |

### Issue 2: `is_anomaly` Column Has Zero Variance (CRITICAL)

| Attribute | Detail |
|---|---|
| **Column** | `is_anomaly` |
| **Issue** | All 54,750 values are `0` — the anomaly flag was never triggered |
| **Record Count** | 54,750 (100%) |
| **Impact** | Column provides no analytical value as-is. Cannot use it to identify cost anomalies. Despite having `anomaly_score` values ranging from 0.011 to 0.688, no record was ever flagged as anomalous. This suggests either a threshold configuration error in the source system or a data generation issue. |
| **Resolution** | Engineer a new `is_anomaly_derived` column using the `anomaly_score` with a threshold at the 95th percentile (score > 0.58). This will flag ~5% of records (~2,738 records) as anomalous for analysis. |

### Issue 3: `budget_status` Column Has Zero Variance (CRITICAL)

| Attribute | Detail |
|---|---|
| **Column** | `budget_status` |
| **Issue** | All 54,750 values are `"under"` — no resource ever exceeded its budget |
| **Record Count** | 54,750 (100%) |
| **Impact** | Column has no analytical utility. Combined with very low `budget_utilization_pct` (max 0.035), this suggests budgets may be set at a granularity that makes daily comparisons meaningless (e.g., budget_amount is monthly but compared against daily costs). |
| **Resolution** | Do not use `budget_status` for analysis. Instead, compute monthly aggregated budget utilization by summing daily `net_cost` per resource-month and comparing against `budget_amount`. |

### Issue 4: Tags Column is Denormalized (MODERATE)

| Attribute | Detail |
|---|---|
| **Column** | `tags` |
| **Issue** | Tags are stored as a single semicolon-delimited string (e.g., `team=Mobile;bu=Finance;env=staging;provider=AWS;service=Serverless`) instead of separate queryable columns |
| **Record Count** | All 54,750 records |
| **Impact** | Cannot directly filter, group, or analyze by individual tag keys without parsing. Makes cross-validation with existing columns difficult. |
| **Resolution** | Parse tags into separate columns: `tag_team`, `tag_bu`, `tag_env`, `tag_provider`, `tag_service`. Then cross-validate against existing columns (`department`, `business_unit`, `environment`, `cloud_provider`, `service`). |

### Issue 5: `forecast_monthly_cost` Contains Extreme Outliers (MODERATE)

| Attribute | Detail |
|---|---|
| **Column** | `forecast_monthly_cost` |
| **Issue** | Extreme right skew with outliers. Median = $12.97, Mean = $29.86, Max = $959.98. Records with forecast > $100: 3,203 (5.9%). Records > $500: 158 (0.3%). Records > $900: 2. |
| **Record Count** | 3,203 potential outliers (>$100) |
| **Impact** | Outliers skew mean calculations and forecasting accuracy assessments. However, some high forecasts may be legitimate (e.g., high-usage production resources). |
| **Resolution** | Flag outliers using IQR method (Q3 + 1.5 × IQR). Do NOT remove — keep for analysis but add `is_forecast_outlier` flag for separate treatment. |

### Issue 6: `spot_savings` Predominantly Zero (MODERATE)

| Attribute | Detail |
|---|---|
| **Column** | `spot_savings` |
| **Issue** | 75th percentile is $0.00, meaning at least 75% of records show no spot instance savings at all |
| **Record Count** | ~41,063 records with spot_savings = 0 (75%) |
| **Impact** | Indicates very low adoption of spot/preemptible instances across the organization. While this is a valid business finding, it limits the utility of this column for comparative analysis. |
| **Resolution** | Document as a key business finding (spot instance under-adoption). Use for identifying specific services/departments that DO use spot instances as best-practice examples. |

### Issue 7: `on_demand_cost` Contains Zero Values (LOW)

| Attribute | Detail |
|---|---|
| **Column** | `on_demand_cost` |
| **Issue** | Some records have `on_demand_cost = 0.0`, meaning entire usage was covered by commitments (RIs/SPs) |
| **Record Count** | ~548 records |
| **Impact** | These are actually positive indicators (full commitment coverage). Not a data quality issue but needs documentation to avoid confusion. |
| **Resolution** | No remediation needed. Document that $0 on-demand cost indicates full RI/SP coverage — a best-practice scenario. |

### Issue 8: `budget_utilization_pct` Extremely Low Values (LOW)

| Attribute | Detail |
|---|---|
| **Column** | `budget_utilization_pct` |
| **Issue** | Max value is 0.0354 (3.5%). This is because daily costs are compared against monthly budgets. |
| **Record Count** | All records |
| **Impact** | The metric is misleading at daily granularity. A 3.5% daily utilization could actually represent ~100% monthly utilization. |
| **Resolution** | Recalculate at monthly level: aggregate daily `net_cost` per project-month and divide by `budget_amount` to get meaningful monthly budget utilization. |

### Issue 9: Inconsistent Usage Units Across Services (LOW)

| Attribute | Detail |
|---|---|
| **Column** | `usage_unit` |
| **Issue** | Seven different units used: vCPU-hours, GB-month, DB-hours, request-million, container-hours, query-hours, GB. This makes cross-service usage comparisons impossible on raw quantities. |
| **Record Count** | All records |
| **Impact** | Cannot compare usage_quantity across different service types directly. |
| **Resolution** | Use `cost_per_unit` (net_cost / usage_quantity) as the normalized comparison metric instead of raw usage_quantity. Group analyses by usage_unit when comparing raw quantities. |

### Issue 10: `currency` Column Has Zero Variance (INFORMATIONAL)

| Attribute | Detail |
|---|---|
| **Column** | `currency` |
| **Issue** | All values are "USD" |
| **Record Count** | All records |
| **Impact** | No analytical value but confirms no currency conversion issues. |
| **Resolution** | Drop from analysis. No action needed. |

---

## 3. Data Quality Score

| Dimension | Score | Notes |
|---|---|---|
| **Completeness** | 10/10 | No missing values in any column |
| **Uniqueness** | 10/10 | No duplicate records |
| **Consistency** | 7/10 | Tags need parsing; budget metrics need re-aggregation |
| **Validity** | 8/10 | Two zero-variance columns (is_anomaly, budget_status); outliers in forecast |
| **Timeliness** | 10/10 | Full 365-day coverage for 2023 |
| **Accuracy** | 9/10 | Cost flow (list_cost - discount = net_cost) generally holds |
| **Overall** | 9/10 | High-quality dataset with minor structural issues |

---

## 4. Remediation Priority Matrix

| Priority | Issue | Effort | Impact |
|---|---|---|---|
| **P1** | Parse tags into separate columns | Medium | High — enables tag-based analysis |
| **P1** | Re-engineer anomaly flag from anomaly_score | Low | High — enables anomaly detection |
| **P1** | Convert date to datetime | Low | High — enables time-series analysis |
| **P2** | Recalculate budget utilization at monthly level | Medium | Medium — meaningful budget tracking |
| **P2** | Flag forecast outliers | Low | Medium — accurate forecasting |
| **P3** | Document zero-variance columns | Low | Low — report completeness |
| **P3** | Document spot_savings under-adoption | Low | Low — business insight |
