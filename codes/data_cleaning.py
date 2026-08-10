"""
Data Cleaning & Preprocessing — Cloud Budget 2023
===================================================
This script loads the raw dataset, performs all cleaning and preprocessing steps,
engineers derived features and KPIs, and exports a clean CSV for analysis.

Author: Capstone Project
Date: 2023 Cloud Cost Analysis
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')


def load_data(filepath):
    """Load the raw dataset."""
    print("=" * 60)
    print("STEP 1: Loading raw data")
    print("=" * 60)
    df = pd.read_csv(filepath)
    print(f"  Loaded {df.shape[0]:,} rows × {df.shape[1]} columns")
    print(f"  Memory usage: {df.memory_usage(deep=True).sum() / 1e6:.1f} MB")
    return df


def convert_dates(df):
    """Convert date string to datetime and extract calendar features."""
    print("\n" + "=" * 60)
    print("STEP 2: Date conversion & calendar feature extraction")
    print("=" * 60)
    
    df['date'] = pd.to_datetime(df['date'])
    df['quarter'] = df['date'].dt.quarter
    df['week_of_year'] = df['date'].dt.isocalendar().week.astype(int)
    df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
    df['month_name'] = df['date'].dt.month_name()
    
    print(f"  Date range: {df['date'].min().date()} → {df['date'].max().date()}")
    print(f"  Quarters: {sorted(df['quarter'].unique())}")
    print(f"  Weekend records: {df['is_weekend'].sum():,} ({df['is_weekend'].mean()*100:.1f}%)")
    return df


def parse_tags(df):
    """Parse semicolon-delimited tags into separate columns."""
    print("\n" + "=" * 60)
    print("STEP 3: Parsing billing tags")
    print("=" * 60)
    
    def extract_tag(tag_string, key):
        """Extract a specific key's value from a tag string."""
        if pd.isna(tag_string):
            return np.nan
        for pair in tag_string.split(';'):
            if '=' in pair:
                k, v = pair.split('=', 1)
                if k.strip() == key:
                    return v.strip()
        return np.nan
    
    tag_keys = ['team', 'bu', 'env', 'provider', 'service']
    for key in tag_keys:
        col_name = f'tag_{key}'
        df[col_name] = df['tags'].apply(lambda x: extract_tag(x, key))
        non_null = df[col_name].notna().sum()
        print(f"  Extracted '{key}' → {col_name}: {non_null:,} values ({non_null/len(df)*100:.1f}%)")
    
    return df


def validate_tag_consistency(df):
    """Cross-validate parsed tags against existing columns."""
    print("\n" + "=" * 60)
    print("STEP 4: Tag consistency validation")
    print("=" * 60)
    
    checks = [
        ('tag_team', 'department', 'Team vs Department'),
        ('tag_bu', 'business_unit', 'BU tag vs Business Unit'),
        ('tag_env', 'environment', 'Env tag vs Environment'),
        ('tag_provider', 'cloud_provider', 'Provider tag vs Cloud Provider'),
        ('tag_service', 'service', 'Service tag vs Service'),
    ]
    
    all_consistent = True
    for tag_col, main_col, label in checks:
        mismatches = (df[tag_col] != df[main_col]).sum()
        status = "✓ CONSISTENT" if mismatches == 0 else f"✗ {mismatches:,} MISMATCHES"
        print(f"  {label}: {status}")
        if mismatches > 0:
            all_consistent = False
            # Show sample mismatches
            mismatch_df = df[df[tag_col] != df[main_col]][[tag_col, main_col]].head(5)
            print(f"    Sample mismatches:\n{mismatch_df.to_string()}")
    
    if all_consistent:
        print("\n  ✓ All tags are consistent with main columns.")
    
    return df


def standardize_categories(df):
    """Standardize categorical values (casing, naming)."""
    print("\n" + "=" * 60)
    print("STEP 5: Standardizing categories")
    print("=" * 60)
    
    cat_columns = ['cloud_provider', 'environment', 'business_unit', 'department',
                   'region', 'service', 'resource_type', 'currency']
    
    for col in cat_columns:
        original_uniques = df[col].nunique()
        # Strip whitespace
        df[col] = df[col].str.strip()
        new_uniques = df[col].nunique()
        change = "no change" if original_uniques == new_uniques else f"reduced {original_uniques} → {new_uniques}"
        print(f"  {col}: {new_uniques} unique values ({change})")
    
    return df


def engineer_anomaly_flag(df):
    """Re-engineer anomaly flag from anomaly_score."""
    print("\n" + "=" * 60)
    print("STEP 6: Engineering anomaly detection")
    print("=" * 60)
    
    threshold_95 = df['anomaly_score'].quantile(0.95)
    df['is_anomaly_derived'] = (df['anomaly_score'] > threshold_95).astype(int)
    
    anomaly_count = df['is_anomaly_derived'].sum()
    print(f"  Anomaly score 95th percentile threshold: {threshold_95:.4f}")
    print(f"  Records flagged as anomalous: {anomaly_count:,} ({anomaly_count/len(df)*100:.1f}%)")
    print(f"  Original is_anomaly column: always 0 (all {len(df):,} records)")
    
    return df


def flag_outliers(df):
    """Flag outliers in forecast_monthly_cost using IQR method."""
    print("\n" + "=" * 60)
    print("STEP 7: Flagging forecast outliers")
    print("=" * 60)
    
    Q1 = df['forecast_monthly_cost'].quantile(0.25)
    Q3 = df['forecast_monthly_cost'].quantile(0.75)
    IQR = Q3 - Q1
    upper_bound = Q3 + 1.5 * IQR
    
    df['is_forecast_outlier'] = (df['forecast_monthly_cost'] > upper_bound).astype(int)
    outlier_count = df['is_forecast_outlier'].sum()
    
    print(f"  IQR: {IQR:.2f}")
    print(f"  Upper bound (Q3 + 1.5×IQR): {upper_bound:.2f}")
    print(f"  Records flagged as forecast outliers: {outlier_count:,} ({outlier_count/len(df)*100:.1f}%)")
    
    return df


def engineer_kpis(df):
    """Create derived KPI columns for analysis."""
    print("\n" + "=" * 60)
    print("STEP 8: Engineering cost-efficiency KPIs")
    print("=" * 60)
    
    # Cost Efficiency Ratio (lower = better discounts)
    df['cost_efficiency_ratio'] = df['net_cost'] / df['list_cost']
    print(f"  cost_efficiency_ratio: mean={df['cost_efficiency_ratio'].mean():.4f}")
    
    # Discount Utilization Rate (higher = better)
    df['discount_utilization'] = df['discount_amount'] / df['list_cost']
    print(f"  discount_utilization: mean={df['discount_utilization'].mean():.4f}")
    
    # Savings Plan Effectiveness
    df['sp_effectiveness'] = np.where(
        df['net_cost'] > 0,
        df['savings_plan_savings'] / df['net_cost'],
        0
    )
    print(f"  sp_effectiveness: mean={df['sp_effectiveness'].mean():.4f}")
    
    # Reserved Instance Effectiveness
    df['ri_effectiveness'] = np.where(
        df['net_cost'] > 0,
        df['reserved_savings'] / df['net_cost'],
        0
    )
    print(f"  ri_effectiveness: mean={df['ri_effectiveness'].mean():.4f}")
    
    # On-Demand Exposure (higher = more exposed to full pricing)
    df['on_demand_exposure'] = np.where(
        df['net_cost'] > 0,
        df['on_demand_cost'] / df['net_cost'],
        0
    )
    print(f"  on_demand_exposure: mean={df['on_demand_exposure'].mean():.4f}")
    
    # Idle Resource Indicator (high on-demand exposure with low commitment)
    df['idle_resource_indicator'] = (df['on_demand_exposure'] > 0.8).astype(int)
    idle_count = df['idle_resource_indicator'].sum()
    print(f"  idle_resource_indicator: {idle_count:,} records ({idle_count/len(df)*100:.1f}%) flagged as idle/under-committed")
    
    # Cost Per Usage Unit
    df['cost_per_unit'] = np.where(
        df['usage_quantity'] > 0,
        df['net_cost'] / df['usage_quantity'],
        0
    )
    print(f"  cost_per_unit: mean={df['cost_per_unit'].mean():.4f}")
    
    # Total Commitment Coverage
    df['total_commitment_coverage'] = df['savings_plan_coverage_pct'] + df['reserved_instance_coverage_pct']
    print(f"  total_commitment_coverage: mean={df['total_commitment_coverage'].mean():.4f}")
    
    # Savings Ratio (total savings as % of list cost)
    df['total_savings'] = df['reserved_savings'] + df['savings_plan_savings'] + df['spot_savings']
    df['savings_ratio'] = np.where(
        df['list_cost'] > 0,
        df['total_savings'] / df['list_cost'],
        0
    )
    print(f"  savings_ratio: mean={df['savings_ratio'].mean():.4f}")
    
    # Waste Score (composite: high on-demand exposure + low commitment + high cost)
    df['waste_score'] = (
        df['on_demand_exposure'] * 0.4 +
        (1 - df['total_commitment_coverage'].clip(0, 1)) * 0.3 +
        df['cost_efficiency_ratio'] * 0.3
    )
    print(f"  waste_score: mean={df['waste_score'].mean():.4f}")
    
    return df


def compute_monthly_budget_utilization(df):
    """Compute meaningful monthly budget utilization."""
    print("\n" + "=" * 60)
    print("STEP 9: Computing monthly budget utilization")
    print("=" * 60)
    
    monthly_costs = df.groupby(['month', 'account_id', 'project_id']).agg(
        monthly_net_cost=('net_cost', 'sum'),
        budget_amount=('budget_amount', 'first')
    ).reset_index()
    
    monthly_costs['monthly_budget_util'] = monthly_costs['monthly_net_cost'] / monthly_costs['budget_amount']
    
    over_budget = (monthly_costs['monthly_budget_util'] > 1).sum()
    print(f"  Project-months over budget: {over_budget} / {len(monthly_costs)}")
    print(f"  Mean monthly utilization: {monthly_costs['monthly_budget_util'].mean():.4f}")
    print(f"  Max monthly utilization: {monthly_costs['monthly_budget_util'].max():.4f}")
    
    # Merge back a monthly utilization flag
    monthly_util_map = monthly_costs.groupby(['month', 'account_id', 'project_id'])['monthly_budget_util'].first()
    df = df.merge(
        monthly_costs[['month', 'account_id', 'project_id', 'monthly_budget_util']],
        on=['month', 'account_id', 'project_id'],
        how='left'
    )
    
    return df


def final_summary(df):
    """Print final dataset summary."""
    print("\n" + "=" * 60)
    print("FINAL SUMMARY")
    print("=" * 60)
    print(f"  Final shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
    print(f"  New columns added: {df.shape[1] - 40}")
    print(f"  Memory usage: {df.memory_usage(deep=True).sum() / 1e6:.1f} MB")
    
    new_cols = [c for c in df.columns if c not in [
        'date','year','month','day','day_of_week','is_month_start','is_month_end',
        'cloud_provider','account_id','project_id','environment','business_unit',
        'department','cost_center','region','service','resource_type','usage_quantity',
        'usage_unit','list_cost','savings_plan_coverage_pct','reserved_instance_coverage_pct',
        'discount_rate_pct','discount_amount','net_cost','on_demand_cost','reserved_savings',
        'savings_plan_savings','spot_savings','amortized_cost','forecast_monthly_cost',
        'budget_amount','budget_utilization_pct','budget_status','cost_variance_7d_pct',
        'cost_variance_30d_pct','anomaly_score','is_anomaly','currency','tags'
    ]]
    print(f"\n  New columns:")
    for col in new_cols:
        print(f"    - {col}")
    
    print(f"\n  Null check (new columns only):")
    for col in new_cols:
        null_count = df[col].isnull().sum()
        print(f"    {col}: {null_count} nulls")
    
    return df


def main():
    """Main cleaning pipeline."""
    print("╔══════════════════════════════════════════════════════════╗")
    print("║     CLOUD BUDGET 2023 — DATA CLEANING & PREPROCESSING   ║")
    print("╚══════════════════════════════════════════════════════════╝\n")
    
    # Pipeline
    input_path = '/Users/yashchaudhary/Desktop/accenrueCapstone/cloud_budget_2023_dataset.csv'
    output_path = '/Users/yashchaudhary/Desktop/accenrueCapstone/cloud_budget_2023_clean.csv'
    
    df = load_data(input_path)
    df = convert_dates(df)
    df = parse_tags(df)
    df = validate_tag_consistency(df)
    df = standardize_categories(df)
    df = engineer_anomaly_flag(df)
    df = flag_outliers(df)
    df = engineer_kpis(df)
    df = compute_monthly_budget_utilization(df)
    df = final_summary(df)
    
    # Export
    print(f"\n  Exporting clean dataset to: {output_path}")
    df.to_csv(output_path, index=False)
    print(f"  ✓ Export complete. File size: {pd.io.common.file_exists(output_path)}")
    
    print("\n╔══════════════════════════════════════════════════════════╗")
    print("║              CLEANING PIPELINE COMPLETE                  ║")
    print("╚══════════════════════════════════════════════════════════╝")
    
    return df


if __name__ == '__main__':
    df = main()
