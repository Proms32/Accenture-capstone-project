"""
Exploratory Data Analysis — Cloud Budget 2023
================================================
Generates 18+ visualizations with insights for the cloud cost analysis.
Uses the cleaned dataset produced by data_cleaning.py.

Author: Capstone Project
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os
import warnings
warnings.filterwarnings('ignore')

# ── Configuration ──────────────────────────────────────────────
OUTPUT_DIR = '/Users/yashchaudhary/Desktop/accenrueCapstone/charts'
DATA_PATH = '/Users/yashchaudhary/Desktop/accenrueCapstone/cloud_budget_2023_clean.csv'

# Premium color palette
COLORS = {
    'primary': '#6366F1',     # Indigo
    'secondary': '#8B5CF6',   # Violet
    'accent': '#EC4899',      # Pink
    'success': '#10B981',     # Emerald
    'warning': '#F59E0B',     # Amber
    'danger': '#EF4444',      # Red
    'info': '#3B82F6',        # Blue
    'dark': '#1E293B',        # Slate-900
    'light': '#F8FAFC',       # Slate-50
}

PALETTE_5 = ['#6366F1', '#8B5CF6', '#EC4899', '#10B981', '#F59E0B']
PALETTE_7 = ['#6366F1', '#8B5CF6', '#EC4899', '#10B981', '#F59E0B', '#3B82F6', '#EF4444']
PALETTE_9 = ['#6366F1', '#8B5CF6', '#EC4899', '#10B981', '#F59E0B', '#3B82F6', '#EF4444', '#14B8A6', '#F97316']
PALETTE_3 = ['#6366F1', '#10B981', '#F59E0B']

# Set global style
plt.rcParams.update({
    'figure.facecolor': '#0F172A',
    'axes.facecolor': '#1E293B',
    'axes.edgecolor': '#334155',
    'axes.labelcolor': '#E2E8F0',
    'text.color': '#E2E8F0',
    'xtick.color': '#94A3B8',
    'ytick.color': '#94A3B8',
    'grid.color': '#334155',
    'grid.alpha': 0.5,
    'font.family': 'sans-serif',
    'font.size': 11,
    'axes.titlesize': 14,
    'axes.titleweight': 'bold',
})


def setup():
    """Create output directory."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Charts will be saved to: {OUTPUT_DIR}\n")


def save_chart(fig, name):
    """Save chart to output directory."""
    path = os.path.join(OUTPUT_DIR, f'{name}.png')
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"  ✓ Saved: {name}.png")


# ═══════════════════════════════════════════════════════════════
# CHART 1: Distribution of Net Cost
# ═══════════════════════════════════════════════════════════════
def chart_01_net_cost_distribution(df):
    """Histogram + KDE of daily net cost per resource."""
    print("\n[1/18] Distribution of Net Cost (Histogram + KDE)")
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.hist(df['net_cost'], bins=80, color=COLORS['primary'], alpha=0.7, edgecolor='none', density=True)
    df['net_cost'].plot.kde(ax=ax, color=COLORS['accent'], linewidth=2.5)
    
    mean_val = df['net_cost'].mean()
    median_val = df['net_cost'].median()
    ax.axvline(mean_val, color=COLORS['warning'], linestyle='--', linewidth=1.5, label=f'Mean: ${mean_val:.2f}')
    ax.axvline(median_val, color=COLORS['success'], linestyle='--', linewidth=1.5, label=f'Median: ${median_val:.2f}')
    
    ax.set_title('Distribution of Daily Net Cost per Resource', pad=15)
    ax.set_xlabel('Net Cost (USD)')
    ax.set_ylabel('Density')
    ax.legend(facecolor='#1E293B', edgecolor='#334155')
    
    save_chart(fig, '01_net_cost_distribution')
    
    print(f"  Insight: Net cost is right-skewed (mean ${mean_val:.2f} > median ${median_val:.2f}).")
    print(f"  Most daily resource costs are under $10, but a long tail extends to ${df['net_cost'].max():.2f}.")


# ═══════════════════════════════════════════════════════════════
# CHART 2: Usage Quantity by Service
# ═══════════════════════════════════════════════════════════════
def chart_02_usage_by_service(df):
    """Box plot of usage quantity by service category."""
    print("\n[2/18] Usage Quantity Distribution by Service")
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    order = df.groupby('service')['usage_quantity'].median().sort_values(ascending=False).index
    bp = ax.boxplot(
        [df[df['service'] == s]['usage_quantity'].values for s in order],
        labels=order,
        patch_artist=True,
        medianprops=dict(color=COLORS['accent'], linewidth=2),
        whiskerprops=dict(color='#94A3B8'),
        capprops=dict(color='#94A3B8'),
        flierprops=dict(marker='o', markersize=2, alpha=0.3, markerfacecolor='#94A3B8')
    )
    
    for patch, color in zip(bp['boxes'], PALETTE_7):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    ax.set_title('Usage Quantity Distribution by Service Category', pad=15)
    ax.set_ylabel('Usage Quantity')
    ax.tick_params(axis='x', rotation=30)
    
    save_chart(fig, '02_usage_by_service')
    
    top_service = order[0]
    print(f"  Insight: '{top_service}' has the highest median usage quantity.")
    print(f"  All services show significant variance, indicating heterogeneous workload patterns.")


# ═══════════════════════════════════════════════════════════════
# CHART 3: Anomaly Score Distribution
# ═══════════════════════════════════════════════════════════════
def chart_03_anomaly_score_dist(df):
    """Distribution of anomaly scores with threshold line."""
    print("\n[3/18] Anomaly Score Distribution")
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.hist(df['anomaly_score'], bins=60, color=COLORS['info'], alpha=0.7, edgecolor='none')
    
    threshold = df['anomaly_score'].quantile(0.95)
    ax.axvline(threshold, color=COLORS['danger'], linestyle='--', linewidth=2,
               label=f'95th percentile threshold: {threshold:.3f}')
    
    anomaly_count = (df['anomaly_score'] > threshold).sum()
    ax.fill_betweenx([0, ax.get_ylim()[1] * 0.8], threshold, df['anomaly_score'].max(),
                     alpha=0.15, color=COLORS['danger'])
    
    ax.set_title('Distribution of Anomaly Scores', pad=15)
    ax.set_xlabel('Anomaly Score')
    ax.set_ylabel('Frequency')
    ax.legend(facecolor='#1E293B', edgecolor='#334155')
    
    save_chart(fig, '03_anomaly_score_distribution')
    
    print(f"  Insight: Anomaly scores follow a roughly uniform distribution (0.01–0.69).")
    print(f"  {anomaly_count:,} records ({anomaly_count/len(df)*100:.1f}%) exceed the 95th percentile threshold.")


# ═══════════════════════════════════════════════════════════════
# CHART 4: Monthly Net Cost Trend
# ═══════════════════════════════════════════════════════════════
def chart_04_monthly_trend(df):
    """Line chart of monthly net cost with trend."""
    print("\n[4/18] Monthly Net Cost Trend")
    
    monthly = df.groupby('month')['net_cost'].sum().reset_index()
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    fig, ax = plt.subplots(figsize=(14, 6))
    
    ax.fill_between(range(1, 13), monthly['net_cost'], alpha=0.15, color=COLORS['primary'])
    ax.plot(range(1, 13), monthly['net_cost'], color=COLORS['primary'], linewidth=2.5,
            marker='o', markersize=8, markerfacecolor=COLORS['accent'], markeredgecolor='white', markeredgewidth=1.5)
    
    for i, row in monthly.iterrows():
        ax.annotate(f'${row["net_cost"]:,.0f}', (row["month"], row["net_cost"]),
                    textcoords="offset points", xytext=(0, 15), ha='center', fontsize=9, color='#CBD5E1')
    
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(months)
    ax.set_title('Monthly Total Net Cost Trend — 2023', pad=15)
    ax.set_ylabel('Total Net Cost (USD)')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
    ax.grid(True, alpha=0.3)
    
    save_chart(fig, '04_monthly_net_cost_trend')
    
    growth = (monthly.iloc[-1]['net_cost'] - monthly.iloc[0]['net_cost']) / monthly.iloc[0]['net_cost'] * 100
    peak_month = months[monthly['net_cost'].idxmax()]
    print(f"  Insight: Cloud spending grew {growth:.1f}% from Jan to Dec 2023.")
    print(f"  Peak spending month: {peak_month}. Clear upward trend in Q4.")


# ═══════════════════════════════════════════════════════════════
# CHART 5: Net Cost by Business Unit
# ═══════════════════════════════════════════════════════════════
def chart_05_cost_by_bu(df):
    """Horizontal bar chart of net cost by business unit."""
    print("\n[5/18] Net Cost by Business Unit")
    
    bu_cost = df.groupby('business_unit')['net_cost'].sum().sort_values()
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    bars = ax.barh(bu_cost.index, bu_cost.values, color=PALETTE_5, edgecolor='none', height=0.6)
    
    for bar, val in zip(bars, bu_cost.values):
        ax.text(val + 500, bar.get_y() + bar.get_height()/2, f'${val:,.0f}',
                va='center', fontsize=11, color='#CBD5E1', fontweight='bold')
    
    ax.set_title('Total Net Cost by Business Unit — 2023', pad=15)
    ax.set_xlabel('Total Net Cost (USD)')
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
    
    save_chart(fig, '05_cost_by_business_unit')
    
    top_bu = bu_cost.index[-1]
    top_pct = bu_cost.iloc[-1] / bu_cost.sum() * 100
    print(f"  Insight: '{top_bu}' is the highest spender at ${bu_cost.iloc[-1]:,.0f} ({top_pct:.1f}% of total).")


# ═══════════════════════════════════════════════════════════════
# CHART 6: Net Cost by Department
# ═══════════════════════════════════════════════════════════════
def chart_06_cost_by_dept(df):
    """Horizontal bar chart of net cost by department."""
    print("\n[6/18] Net Cost by Department")
    
    dept_cost = df.groupby('department')['net_cost'].sum().sort_values()
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    bars = ax.barh(dept_cost.index, dept_cost.values, color=PALETTE_5[::-1], edgecolor='none', height=0.6)
    
    for bar, val in zip(bars, dept_cost.values):
        ax.text(val + 500, bar.get_y() + bar.get_height()/2, f'${val:,.0f}',
                va='center', fontsize=11, color='#CBD5E1', fontweight='bold')
    
    ax.set_title('Total Net Cost by Department — 2023', pad=15)
    ax.set_xlabel('Total Net Cost (USD)')
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
    
    save_chart(fig, '06_cost_by_department')
    
    top_dept = dept_cost.index[-1]
    print(f"  Insight: '{top_dept}' department leads spending at ${dept_cost.iloc[-1]:,.0f}.")


# ═══════════════════════════════════════════════════════════════
# CHART 7: Net Cost by Cloud Provider
# ═══════════════════════════════════════════════════════════════
def chart_07_cost_by_provider(df):
    """Bar chart of net cost by cloud provider."""
    print("\n[7/18] Net Cost by Cloud Provider")
    
    provider_cost = df.groupby('cloud_provider')['net_cost'].sum().sort_values(ascending=False)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bars = ax.bar(provider_cost.index, provider_cost.values, color=PALETTE_3, edgecolor='none', width=0.5)
    
    for bar, val in zip(bars, provider_cost.values):
        ax.text(bar.get_x() + bar.get_width()/2, val + 500, f'${val:,.0f}',
                ha='center', fontsize=12, color='#CBD5E1', fontweight='bold')
    
    ax.set_title('Total Net Cost by Cloud Provider — 2023', pad=15)
    ax.set_ylabel('Total Net Cost (USD)')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
    
    save_chart(fig, '07_cost_by_provider')
    
    print(f"  Insight: Provider cost split — " + 
          ", ".join([f"{p}: ${v:,.0f} ({v/provider_cost.sum()*100:.1f}%)" for p, v in provider_cost.items()]))


# ═══════════════════════════════════════════════════════════════
# CHART 8: Cost by Environment (Stacked Bar)
# ═══════════════════════════════════════════════════════════════
def chart_08_cost_by_environment(df):
    """Stacked bar chart of cost by environment per month."""
    print("\n[8/18] Monthly Cost by Environment")
    
    env_monthly = df.pivot_table(values='net_cost', index='month', columns='environment', aggfunc='sum')
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    fig, ax = plt.subplots(figsize=(14, 7))
    
    env_colors = {'prod': COLORS['primary'], 'staging': COLORS['warning'], 'dev': COLORS['success']}
    bottom = np.zeros(12)
    
    for env in ['prod', 'staging', 'dev']:
        if env in env_monthly.columns:
            vals = env_monthly[env].values
            ax.bar(range(1, 13), vals, bottom=bottom, label=env.upper(),
                   color=env_colors[env], edgecolor='none', width=0.6, alpha=0.85)
            bottom += vals
    
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(months)
    ax.set_title('Monthly Net Cost by Environment', pad=15)
    ax.set_ylabel('Total Net Cost (USD)')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
    ax.legend(facecolor='#1E293B', edgecolor='#334155')
    
    save_chart(fig, '08_cost_by_environment')
    
    env_total = df.groupby('environment')['net_cost'].sum()
    prod_pct = env_total.get('prod', 0) / env_total.sum() * 100
    non_prod = 100 - prod_pct
    print(f"  Insight: Production accounts for {prod_pct:.1f}% of total spend.")
    print(f"  Non-production (staging + dev) accounts for {non_prod:.1f}% — a significant optimization target.")


# ═══════════════════════════════════════════════════════════════
# CHART 9: Cost Efficiency by Department (Box Plot)
# ═══════════════════════════════════════════════════════════════
def chart_09_efficiency_by_dept(df):
    """Box plot of cost efficiency ratio by department."""
    print("\n[9/18] Cost Efficiency Ratio by Department")
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    order = df.groupby('department')['cost_efficiency_ratio'].median().sort_values().index
    bp = ax.boxplot(
        [df[df['department'] == d]['cost_efficiency_ratio'].values for d in order],
        labels=order,
        patch_artist=True,
        medianprops=dict(color=COLORS['accent'], linewidth=2),
        whiskerprops=dict(color='#94A3B8'),
        capprops=dict(color='#94A3B8'),
        flierprops=dict(marker='o', markersize=2, alpha=0.3, markerfacecolor='#94A3B8')
    )
    
    for patch, color in zip(bp['boxes'], PALETTE_5):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    ax.set_title('Cost Efficiency Ratio by Department (Lower = Better Discounts)', pad=15)
    ax.set_ylabel('Cost Efficiency Ratio (Net/List)')
    ax.axhline(y=df['cost_efficiency_ratio'].median(), color=COLORS['warning'], linestyle='--',
               alpha=0.5, label=f'Overall Median: {df["cost_efficiency_ratio"].median():.3f}')
    ax.legend(facecolor='#1E293B', edgecolor='#334155')
    
    save_chart(fig, '09_cost_efficiency_by_department')
    
    best = order[0]
    worst = order[-1]
    print(f"  Insight: '{best}' achieves the best (lowest) cost efficiency ratio.")
    print(f"  '{worst}' pays the highest proportion of list price.")


# ═══════════════════════════════════════════════════════════════
# CHART 10: Discount Utilization by Provider
# ═══════════════════════════════════════════════════════════════
def chart_10_discount_by_provider(df):
    """Grouped bar chart of discount metrics by provider."""
    print("\n[10/18] Discount Utilization by Cloud Provider")
    
    metrics = df.groupby('cloud_provider').agg(
        discount_util=('discount_utilization', 'mean'),
        sp_coverage=('savings_plan_coverage_pct', 'mean'),
        ri_coverage=('reserved_instance_coverage_pct', 'mean')
    ).reset_index()
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    x = np.arange(len(metrics))
    width = 0.25
    
    ax.bar(x - width, metrics['discount_util'], width, label='Discount Utilization',
           color=COLORS['primary'], edgecolor='none')
    ax.bar(x, metrics['sp_coverage'], width, label='Savings Plan Coverage',
           color=COLORS['success'], edgecolor='none')
    ax.bar(x + width, metrics['ri_coverage'], width, label='RI Coverage',
           color=COLORS['warning'], edgecolor='none')
    
    ax.set_xticks(x)
    ax.set_xticklabels(metrics['cloud_provider'])
    ax.set_title('Discount & Commitment Metrics by Cloud Provider', pad=15)
    ax.set_ylabel('Percentage')
    ax.legend(facecolor='#1E293B', edgecolor='#334155')
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(1.0))
    
    save_chart(fig, '10_discount_by_provider')
    
    best_disc = metrics.loc[metrics['discount_util'].idxmax(), 'cloud_provider']
    print(f"  Insight: '{best_disc}' offers the highest average discount utilization.")


# ═══════════════════════════════════════════════════════════════
# CHART 11: Heatmap — Net Cost by BU × Service
# ═══════════════════════════════════════════════════════════════
def chart_11_heatmap_bu_service(df):
    """Heatmap of net cost by business unit and service."""
    print("\n[11/18] Heatmap: Net Cost by Business Unit × Service")
    
    pivot = df.pivot_table(values='net_cost', index='business_unit', columns='service', aggfunc='sum')
    
    fig, ax = plt.subplots(figsize=(14, 7))
    
    sns.heatmap(pivot, annot=True, fmt=',.0f', cmap='YlOrRd', ax=ax,
                linewidths=0.5, linecolor='#334155',
                annot_kws={'size': 10, 'color': '#1E293B'},
                cbar_kws={'label': 'Total Net Cost (USD)'})
    
    ax.set_title('Total Net Cost: Business Unit × Service Category', pad=15)
    ax.set_ylabel('Business Unit')
    ax.set_xlabel('Service Category')
    
    save_chart(fig, '11_heatmap_bu_service')
    
    max_cell = pivot.stack().idxmax()
    max_val = pivot.stack().max()
    print(f"  Insight: Highest cost concentration is {max_cell[0]} × {max_cell[1]} at ${max_val:,.0f}.")


# ═══════════════════════════════════════════════════════════════
# CHART 12: Heatmap — Cost by Region × Provider
# ═══════════════════════════════════════════════════════════════
def chart_12_heatmap_region_provider(df):
    """Heatmap of net cost by region and cloud provider."""
    print("\n[12/18] Heatmap: Net Cost by Region × Provider")
    
    pivot = df.pivot_table(values='net_cost', index='region', columns='cloud_provider', aggfunc='sum')
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    sns.heatmap(pivot, annot=True, fmt=',.0f', cmap='BuPu', ax=ax,
                linewidths=0.5, linecolor='#334155',
                annot_kws={'size': 11, 'color': '#1E293B'},
                cbar_kws={'label': 'Total Net Cost (USD)'})
    
    ax.set_title('Total Net Cost: Region × Cloud Provider', pad=15)
    ax.set_ylabel('Region')
    ax.set_xlabel('Cloud Provider')
    
    save_chart(fig, '12_heatmap_region_provider')
    
    max_cell = pivot.stack().idxmax()
    print(f"  Insight: Highest regional cost is {max_cell[0]} on {max_cell[1]}.")


# ═══════════════════════════════════════════════════════════════
# CHART 13: SP Coverage vs RI Coverage (Scatter)
# ═══════════════════════════════════════════════════════════════
def chart_13_sp_vs_ri(df):
    """Scatter plot of savings plan coverage vs reserved instance coverage."""
    print("\n[13/18] Savings Plan Coverage vs RI Coverage")
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    sample = df.sample(n=min(5000, len(df)), random_state=42)
    
    scatter = ax.scatter(
        sample['savings_plan_coverage_pct'],
        sample['reserved_instance_coverage_pct'],
        c=sample['net_cost'],
        cmap='plasma',
        alpha=0.4,
        s=15,
        edgecolors='none'
    )
    
    plt.colorbar(scatter, ax=ax, label='Net Cost (USD)')
    
    # Add quadrant lines
    ax.axvline(x=0.35, color='#94A3B8', linestyle=':', alpha=0.5)
    ax.axhline(y=0.22, color='#94A3B8', linestyle=':', alpha=0.5)
    
    ax.set_title('Savings Plan vs Reserved Instance Coverage', pad=15)
    ax.set_xlabel('Savings Plan Coverage (%)')
    ax.set_ylabel('Reserved Instance Coverage (%)')
    ax.xaxis.set_major_formatter(mticker.PercentFormatter(1.0))
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(1.0))
    
    # Annotate quadrants
    ax.text(0.55, 0.55, 'High Both\n(Optimal)', ha='center', fontsize=9, color=COLORS['success'], alpha=0.8)
    ax.text(0.1, 0.05, 'Low Both\n(At Risk)', ha='center', fontsize=9, color=COLORS['danger'], alpha=0.8)
    
    save_chart(fig, '13_sp_vs_ri_coverage')
    
    both_low = ((df['savings_plan_coverage_pct'] < 0.15) & (df['reserved_instance_coverage_pct'] < 0.1)).sum()
    print(f"  Insight: {both_low:,} records ({both_low/len(df)*100:.1f}%) have both SP and RI coverage below 15%/10%.")
    print(f"  These represent the highest optimization opportunity for commitment-based savings.")


# ═══════════════════════════════════════════════════════════════
# CHART 14: Top 20 Projects by Net Cost
# ═══════════════════════════════════════════════════════════════
def chart_14_top_projects(df):
    """Bar chart of top 20 projects by total net cost."""
    print("\n[14/18] Top 20 Projects by Total Net Cost")
    
    proj_cost = df.groupby(['account_id', 'project_id'])['net_cost'].sum().sort_values(ascending=False).head(20)
    proj_labels = [f"{a}/{p}" for a, p in proj_cost.index]
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    colors = plt.cm.plasma(np.linspace(0.2, 0.8, 20))
    bars = ax.barh(range(19, -1, -1), proj_cost.values, color=colors, edgecolor='none', height=0.7)
    
    ax.set_yticks(range(19, -1, -1))
    ax.set_yticklabels(proj_labels, fontsize=9)
    
    for i, (bar, val) in enumerate(zip(bars, proj_cost.values)):
        ax.text(val + 50, bar.get_y() + bar.get_height()/2, f'${val:,.0f}',
                va='center', fontsize=9, color='#CBD5E1')
    
    ax.set_title('Top 20 Projects by Total Net Cost — 2023', pad=15)
    ax.set_xlabel('Total Net Cost (USD)')
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
    
    save_chart(fig, '14_top_20_projects')
    
    top_proj = proj_labels[0]
    top_val = proj_cost.iloc[0]
    print(f"  Insight: Top project '{top_proj}' spent ${top_val:,.0f} in 2023.")


# ═══════════════════════════════════════════════════════════════
# CHART 15: Monthly Cost by BU (Stacked Area)
# ═══════════════════════════════════════════════════════════════
def chart_15_monthly_by_bu(df):
    """Stacked area chart of monthly cost by business unit."""
    print("\n[15/18] Monthly Cost by Business Unit (Stacked Area)")
    
    bu_monthly = df.pivot_table(values='net_cost', index='month', columns='business_unit', aggfunc='sum')
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    fig, ax = plt.subplots(figsize=(14, 7))
    
    ax.stackplot(range(1, 13), [bu_monthly[col].values for col in bu_monthly.columns],
                 labels=bu_monthly.columns, colors=PALETTE_5, alpha=0.8)
    
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(months)
    ax.set_title('Monthly Net Cost by Business Unit (Stacked)', pad=15)
    ax.set_ylabel('Total Net Cost (USD)')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
    ax.legend(loc='upper left', facecolor='#1E293B', edgecolor='#334155')
    
    save_chart(fig, '15_monthly_cost_by_bu')
    
    print(f"  Insight: All business units show growth in Q4, contributing to the overall cost escalation.")


# ═══════════════════════════════════════════════════════════════
# CHART 16: Idle Resource Indicator by Department
# ═══════════════════════════════════════════════════════════════
def chart_16_idle_by_dept(df):
    """Bar chart of idle resource % by department."""
    print("\n[16/18] Idle Resource Indicator by Department")
    
    idle_by_dept = df.groupby('department')['idle_resource_indicator'].mean().sort_values(ascending=False)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bars = ax.bar(idle_by_dept.index, idle_by_dept.values * 100, color=PALETTE_5, edgecolor='none', width=0.5)
    
    for bar, val in zip(bars, idle_by_dept.values):
        ax.text(bar.get_x() + bar.get_width()/2, val * 100 + 0.3, f'{val*100:.1f}%',
                ha='center', fontsize=11, color='#CBD5E1', fontweight='bold')
    
    ax.set_title('Idle/Under-Committed Resource Rate by Department', pad=15)
    ax.set_ylabel('% of Records with On-Demand Exposure > 80%')
    ax.axhline(y=df['idle_resource_indicator'].mean() * 100, color=COLORS['danger'], linestyle='--',
               label=f'Org Average: {df["idle_resource_indicator"].mean()*100:.1f}%')
    ax.legend(facecolor='#1E293B', edgecolor='#334155')
    
    save_chart(fig, '16_idle_by_department')
    
    worst = idle_by_dept.index[0]
    print(f"  Insight: '{worst}' has the highest idle resource rate ({idle_by_dept.iloc[0]*100:.1f}%).")


# ═══════════════════════════════════════════════════════════════
# CHART 17: Correlation Matrix
# ═══════════════════════════════════════════════════════════════
def chart_17_correlation(df):
    """Correlation matrix of key numeric features."""
    print("\n[17/18] Correlation Matrix of Key Metrics")
    
    cols = ['net_cost', 'list_cost', 'usage_quantity', 'discount_amount',
            'on_demand_cost', 'reserved_savings', 'savings_plan_savings',
            'spot_savings', 'anomaly_score', 'cost_efficiency_ratio',
            'discount_utilization', 'on_demand_exposure', 'waste_score']
    
    corr = df[cols].corr()
    
    fig, ax = plt.subplots(figsize=(14, 11))
    
    mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
    sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', cmap='RdYlBu_r', ax=ax,
                linewidths=0.5, linecolor='#334155', center=0,
                annot_kws={'size': 9},
                cbar_kws={'label': 'Correlation'})
    
    ax.set_title('Correlation Matrix of Key Cost Metrics', pad=15)
    ax.tick_params(axis='x', rotation=45)
    ax.tick_params(axis='y', rotation=0)
    
    save_chart(fig, '17_correlation_matrix')
    
    print(f"  Insight: Net cost has the strongest positive correlation with list_cost (expected).")
    print(f"  Waste_score correlates with on_demand_exposure, highlighting commitment-based optimization.")


# ═══════════════════════════════════════════════════════════════
# CHART 18: Forecast vs Actual Cost
# ═══════════════════════════════════════════════════════════════
def chart_18_forecast_vs_actual(df):
    """Scatter plot comparing forecast monthly cost to actual aggregated cost."""
    print("\n[18/18] Forecast vs Actual Monthly Cost")
    
    monthly_actual = df.groupby(['month', 'account_id', 'project_id']).agg(
        actual_monthly=('net_cost', 'sum'),
        forecast=('forecast_monthly_cost', 'mean')
    ).reset_index()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    sample = monthly_actual.sample(n=min(3000, len(monthly_actual)), random_state=42)
    
    ax.scatter(sample['forecast'], sample['actual_monthly'],
               color=COLORS['primary'], alpha=0.3, s=12, edgecolors='none')
    
    # Perfect prediction line
    max_val = max(sample['forecast'].max(), sample['actual_monthly'].max())
    ax.plot([0, max_val], [0, max_val], color=COLORS['accent'], linestyle='--', linewidth=1.5,
            label='Perfect Forecast', alpha=0.7)
    
    ax.set_title('Forecast vs Actual Monthly Cost (per Project)', pad=15)
    ax.set_xlabel('Forecast Monthly Cost (USD)')
    ax.set_ylabel('Actual Monthly Cost (USD)')
    ax.legend(facecolor='#1E293B', edgecolor='#334155')
    
    save_chart(fig, '18_forecast_vs_actual')
    
    print(f"  Insight: Most forecasts cluster near the lower range while actuals vary widely.")
    print(f"  This suggests forecasting models may underestimate costs for many projects.")


# ═══════════════════════════════════════════════════════════════
# STATISTICAL SUMMARY
# ═══════════════════════════════════════════════════════════════
def print_statistical_summary(df):
    """Print key statistical summaries."""
    print("\n" + "=" * 60)
    print("STATISTICAL SUMMARY")
    print("=" * 60)
    
    total_spend = df['net_cost'].sum()
    print(f"\n  Total Annual Net Cost: ${total_spend:,.2f}")
    print(f"  Total Annual List Cost: ${df['list_cost'].sum():,.2f}")
    print(f"  Total Discounts: ${df['discount_amount'].sum():,.2f}")
    print(f"  Total Savings (RI+SP+Spot): ${df['total_savings'].sum():,.2f}")
    
    print(f"\n  Mean daily cost per resource: ${df['net_cost'].mean():.2f}")
    print(f"  Median daily cost per resource: ${df['net_cost'].median():.2f}")
    print(f"  Std dev: ${df['net_cost'].std():.2f}")
    
    print(f"\n  Cost by Environment:")
    for env, cost in df.groupby('environment')['net_cost'].sum().sort_values(ascending=False).items():
        print(f"    {env}: ${cost:,.0f} ({cost/total_spend*100:.1f}%)")
    
    print(f"\n  Cost by Provider:")
    for prov, cost in df.groupby('cloud_provider')['net_cost'].sum().sort_values(ascending=False).items():
        print(f"    {prov}: ${cost:,.0f} ({cost/total_spend*100:.1f}%)")
    
    print(f"\n  Cost by Service:")
    for svc, cost in df.groupby('service')['net_cost'].sum().sort_values(ascending=False).items():
        print(f"    {svc}: ${cost:,.0f} ({cost/total_spend*100:.1f}%)")
    
    print(f"\n  Average Cost Efficiency Ratio: {df['cost_efficiency_ratio'].mean():.4f}")
    print(f"  Average Discount Utilization: {df['discount_utilization'].mean():.4f}")
    print(f"  Average On-Demand Exposure: {df['on_demand_exposure'].mean():.4f}")


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════
def main():
    print("╔══════════════════════════════════════════════════════════╗")
    print("║       CLOUD BUDGET 2023 — EXPLORATORY DATA ANALYSIS      ║")
    print("╚══════════════════════════════════════════════════════════╝\n")
    
    setup()
    
    print("Loading cleaned dataset...")
    df = pd.read_csv(DATA_PATH)
    df['date'] = pd.to_datetime(df['date'])
    print(f"Loaded {df.shape[0]:,} rows × {df.shape[1]} columns\n")
    
    # Generate all 18 charts
    chart_01_net_cost_distribution(df)
    chart_02_usage_by_service(df)
    chart_03_anomaly_score_dist(df)
    chart_04_monthly_trend(df)
    chart_05_cost_by_bu(df)
    chart_06_cost_by_dept(df)
    chart_07_cost_by_provider(df)
    chart_08_cost_by_environment(df)
    chart_09_efficiency_by_dept(df)
    chart_10_discount_by_provider(df)
    chart_11_heatmap_bu_service(df)
    chart_12_heatmap_region_provider(df)
    chart_13_sp_vs_ri(df)
    chart_14_top_projects(df)
    chart_15_monthly_by_bu(df)
    chart_16_idle_by_dept(df)
    chart_17_correlation(df)
    chart_18_forecast_vs_actual(df)
    
    # Print summary
    print_statistical_summary(df)
    
    print("\n╔══════════════════════════════════════════════════════════╗")
    print("║                EDA COMPLETE — 18 CHARTS GENERATED         ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print(f"\nAll charts saved to: {OUTPUT_DIR}")


if __name__ == '__main__':
    main()
