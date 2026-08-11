"""
Cloud Budget 2023 — Executive Dashboard
=========================================
Interactive Streamlit dashboard for cloud cost analysis.

Run with: streamlit run dashboard.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path

# ── Page Config ────────────────────────────────────────────────
st.set_page_config(
    page_title="Cloud Cost Optimizer — 2023",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ─────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Global */
    .stApp {
        background: linear-gradient(135deg, #0F172A 0%, #1E1B4B 50%, #0F172A 100%);
        font-family: 'Inter', sans-serif;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: rgba(30, 27, 75, 0.95) !important;
        border-right: 1px solid rgba(99, 102, 241, 0.2);
    }

    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown label {
        color: #CBD5E1 !important;
    }

    /* KPI Cards */
    .kpi-card {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 16px;
        padding: 20px 24px;
        backdrop-filter: blur(10px);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(99, 102, 241, 0.15);
    }

    .kpi-value {
        font-size: 28px;
        font-weight: 700;
        background: linear-gradient(135deg, #818CF8, #C084FC);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 4px;
    }

    .kpi-label {
        font-size: 13px;
        color: #94A3B8;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .kpi-delta-pos {
        color: #F87171;
        font-size: 12px;
        font-weight: 600;
    }

    .kpi-delta-neg {
        color: #34D399;
        font-size: 12px;
        font-weight: 600;
    }

    /* Section headers */
    .section-header {
        font-size: 20px;
        font-weight: 600;
        color: #E2E8F0;
        margin: 32px 0 16px 0;
        padding-bottom: 8px;
        border-bottom: 2px solid rgba(99, 102, 241, 0.3);
    }

    /* Title */
    .dashboard-title {
        font-size: 32px;
        font-weight: 700;
        background: linear-gradient(135deg, #818CF8, #C084FC, #F472B6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 4px;
    }

    .dashboard-subtitle {
        font-size: 14px;
        color: #94A3B8;
        margin-bottom: 24px;
    }

    /* Metric styling */
    div[data-testid="stMetric"] {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 12px;
        padding: 16px;
    }

    div[data-testid="stMetric"] label {
        color: #94A3B8 !important;
    }

    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #E2E8F0 !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 8px;
        color: #CBD5E1;
        padding: 8px 16px;
    }

    .stTabs [aria-selected="true"] {
        background: rgba(99, 102, 241, 0.2) !important;
        border-color: #6366F1 !important;
    }

    /* Table styling */
    .stDataFrame {
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 12px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)


# ── Data Loading ───────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "dataset" / "cloud_budget_2023_clean.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df['date'] = pd.to_datetime(df['date'])
    return df

df = load_data()

# ── Plotly Theme ───────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(30,41,59,0.5)',
    font=dict(family='Inter', color='#CBD5E1', size=12),
    margin=dict(l=40, r=40, t=60, b=40),
    xaxis=dict(gridcolor='rgba(51,65,85,0.5)', zerolinecolor='rgba(51,65,85,0.5)'),
    yaxis=dict(gridcolor='rgba(51,65,85,0.5)', zerolinecolor='rgba(51,65,85,0.5)'),
    colorway=['#818CF8', '#C084FC', '#F472B6', '#34D399', '#FBBF24', '#60A5FA', '#F87171', '#2DD4BF', '#FB923C'],
)


# ── Sidebar Filters ────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ☁️ Filters")
    st.markdown("---")

    # Date range
    date_range = st.date_input(
        "📅 Date Range",
        value=(df['date'].min().date(), df['date'].max().date()),
        min_value=df['date'].min().date(),
        max_value=df['date'].max().date()
    )

    # Cloud Provider
    providers = st.multiselect(
        "🌐 Cloud Provider",
        options=sorted(df['cloud_provider'].unique()),
        default=sorted(df['cloud_provider'].unique())
    )

    # Business Unit
    bus = st.multiselect(
        "🏢 Business Unit",
        options=sorted(df['business_unit'].unique()),
        default=sorted(df['business_unit'].unique())
    )

    # Department
    depts = st.multiselect(
        "👥 Department",
        options=sorted(df['department'].unique()),
        default=sorted(df['department'].unique())
    )

    # Environment
    envs = st.multiselect(
        "⚙️ Environment",
        options=sorted(df['environment'].unique()),
        default=sorted(df['environment'].unique())
    )

    # Region
    regions = st.multiselect(
        "🌍 Region",
        options=sorted(df['region'].unique()),
        default=sorted(df['region'].unique())
    )

    # Service
    services = st.multiselect(
        "🛠️ Service",
        options=sorted(df['service'].unique()),
        default=sorted(df['service'].unique())
    )

    st.markdown("---")
    st.markdown("*Data: Jan–Dec 2023*")
    st.markdown("*54,750 billing records*")


# ── Apply Filters ──────────────────────────────────────────────
mask = (
    (df['date'].dt.date >= date_range[0]) &
    (df['date'].dt.date <= date_range[1]) &
    (df['cloud_provider'].isin(providers)) &
    (df['business_unit'].isin(bus)) &
    (df['department'].isin(depts)) &
    (df['environment'].isin(envs)) &
    (df['region'].isin(regions)) &
    (df['service'].isin(services))
)
filtered = df[mask]


# ── Title ──────────────────────────────────────────────────────
st.markdown('<div class="dashboard-title">☁️ Cloud Cost Optimizer Dashboard</div>', unsafe_allow_html=True)
st.markdown(f'<div class="dashboard-subtitle">Analyzing {len(filtered):,} records | {filtered["date"].min().strftime("%b %d")} – {filtered["date"].max().strftime("%b %d, %Y")}</div>', unsafe_allow_html=True)


# ── KPI Cards ──────────────────────────────────────────────────
total_spend = filtered['net_cost'].sum()
total_list = filtered['list_cost'].sum()
total_discount = filtered['discount_amount'].sum()
avg_efficiency = filtered['cost_efficiency_ratio'].mean()
idle_pct = filtered['idle_resource_indicator'].mean() * 100
total_savings = filtered['total_savings'].sum()
savings_rate = (total_discount / total_list * 100) if total_list > 0 else 0
anomaly_count = filtered['is_anomaly_derived'].sum()

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">${total_spend:,.0f}</div>
        <div class="kpi-label">Total Net Cost</div>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">${total_discount:,.0f}</div>
        <div class="kpi-label">Total Discounts</div>
    </div>""", unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{savings_rate:.1f}%</div>
        <div class="kpi-label">Savings Rate</div>
    </div>""", unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{avg_efficiency:.1%}</div>
        <div class="kpi-label">Cost Efficiency</div>
    </div>""", unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{idle_pct:.1f}%</div>
        <div class="kpi-label">Idle Resource Rate</div>
    </div>""", unsafe_allow_html=True)

with col6:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{anomaly_count:,}</div>
        <div class="kpi-label">Anomalies Detected</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Tabs ───────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Cost Trends", "🏢 Department Analysis", "☁️ Provider Breakdown",
    "🔍 Waste Detection", "📊 Detailed Data"
])


# ── TAB 1: Cost Trends ────────────────────────────────────────
with tab1:
    st.markdown('<div class="section-header">Monthly Cost Trend</div>', unsafe_allow_html=True)

    monthly = filtered.groupby(filtered['date'].dt.to_period('M')).agg(
        net_cost=('net_cost', 'sum'),
        list_cost=('list_cost', 'sum'),
        discount_amount=('discount_amount', 'sum')
    ).reset_index()
    monthly['date'] = monthly['date'].dt.to_timestamp()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly['date'], y=monthly['net_cost'],
        mode='lines+markers', name='Net Cost',
        line=dict(color='#818CF8', width=3),
        marker=dict(size=8, color='#C084FC'),
        fill='tozeroy', fillcolor='rgba(129,140,248,0.1)'
    ))
    fig.add_trace(go.Scatter(
        x=monthly['date'], y=monthly['list_cost'],
        mode='lines+markers', name='List Cost',
        line=dict(color='#F472B6', width=2, dash='dash'),
        marker=dict(size=6)
    ))
    fig.update_layout(**PLOTLY_LAYOUT, height=400, title='Monthly Cost: Net vs List Price')
    fig.update_yaxes(title='Cost (USD)')
    st.plotly_chart(fig, use_container_width=True)

    # Cost by environment over time
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-header">Cost by Environment</div>', unsafe_allow_html=True)
        env_monthly = filtered.groupby([filtered['date'].dt.to_period('M'), 'environment'])['net_cost'].sum().reset_index()
        env_monthly['date'] = env_monthly['date'].dt.to_timestamp()
        fig_env = px.area(env_monthly, x='date', y='net_cost', color='environment',
                         color_discrete_sequence=['#818CF8', '#FBBF24', '#34D399'])
        fig_env.update_layout(**PLOTLY_LAYOUT, height=350, title='Monthly Cost by Environment',
                             showlegend=True)
        st.plotly_chart(fig_env, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">Cost by Service</div>', unsafe_allow_html=True)
        svc_cost = filtered.groupby('service')['net_cost'].sum().sort_values(ascending=True).reset_index()
        fig_svc = px.bar(svc_cost, x='net_cost', y='service', orientation='h',
                        color='net_cost', color_continuous_scale='Purp')
        fig_svc.update_layout(**PLOTLY_LAYOUT, height=350, title='Total Cost by Service',
                             coloraxis_showscale=False)
        fig_svc.update_xaxes(title='Total Net Cost (USD)')
        st.plotly_chart(fig_svc, use_container_width=True)


# ── TAB 2: Department Analysis ─────────────────────────────────
with tab2:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-header">Cost by Business Unit</div>', unsafe_allow_html=True)
        bu_cost = filtered.groupby('business_unit')['net_cost'].sum().sort_values(ascending=True).reset_index()
        fig_bu = px.bar(bu_cost, x='net_cost', y='business_unit', orientation='h',
                       color='business_unit', color_discrete_sequence=['#818CF8', '#C084FC', '#F472B6', '#34D399', '#FBBF24'])
        fig_bu.update_layout(**PLOTLY_LAYOUT, height=350, title='Total Cost by Business Unit',
                            showlegend=False)
        fig_bu.update_xaxes(title='Total Net Cost (USD)')
        st.plotly_chart(fig_bu, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">Cost by Department</div>', unsafe_allow_html=True)
        dept_cost = filtered.groupby('department')['net_cost'].sum().sort_values(ascending=True).reset_index()
        fig_dept = px.bar(dept_cost, x='net_cost', y='department', orientation='h',
                         color='department', color_discrete_sequence=['#60A5FA', '#2DD4BF', '#FB923C', '#F87171', '#A78BFA'])
        fig_dept.update_layout(**PLOTLY_LAYOUT, height=350, title='Total Cost by Department',
                              showlegend=False)
        fig_dept.update_xaxes(title='Total Net Cost (USD)')
        st.plotly_chart(fig_dept, use_container_width=True)

    # Heatmap: BU × Service
    st.markdown('<div class="section-header">Cost Heatmap: Business Unit × Service</div>', unsafe_allow_html=True)
    pivot = filtered.pivot_table(values='net_cost', index='business_unit', columns='service', aggfunc='sum').fillna(0)
    fig_heat = px.imshow(pivot, text_auto=',.0f', color_continuous_scale='Purp',
                        aspect='auto')
    fig_heat.update_layout(**PLOTLY_LAYOUT, height=400, title='Net Cost: Business Unit × Service')
    st.plotly_chart(fig_heat, use_container_width=True)

    # Efficiency leaderboard
    st.markdown('<div class="section-header">Cost Efficiency Leaderboard</div>', unsafe_allow_html=True)
    efficiency_board = filtered.groupby('department').agg(
        total_cost=('net_cost', 'sum'),
        avg_efficiency=('cost_efficiency_ratio', 'mean'),
        avg_discount_util=('discount_utilization', 'mean'),
        avg_commitment=('total_commitment_coverage', 'mean'),
        idle_rate=('idle_resource_indicator', 'mean'),
        total_savings=('total_savings', 'sum')
    ).reset_index()
    efficiency_board['idle_rate'] = (efficiency_board['idle_rate'] * 100).round(1)
    efficiency_board['avg_efficiency'] = (efficiency_board['avg_efficiency'] * 100).round(1)
    efficiency_board['avg_discount_util'] = (efficiency_board['avg_discount_util'] * 100).round(1)
    efficiency_board['avg_commitment'] = (efficiency_board['avg_commitment'] * 100).round(1)
    efficiency_board.columns = ['Department', 'Total Cost ($)', 'Efficiency (%)', 'Discount Util (%)',
                                'Commitment Coverage (%)', 'Idle Rate (%)', 'Total Savings ($)']
    efficiency_board = efficiency_board.sort_values('Efficiency (%)')
    st.dataframe(efficiency_board, hide_index=True, use_container_width=True)


# ── TAB 3: Provider Breakdown ──────────────────────────────────
with tab3:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-header">Cost Split by Provider</div>', unsafe_allow_html=True)
        prov_cost = filtered.groupby('cloud_provider')['net_cost'].sum().reset_index()
        fig_pie = px.pie(prov_cost, values='net_cost', names='cloud_provider',
                        color_discrete_sequence=['#818CF8', '#34D399', '#FBBF24'],
                        hole=0.45)
        fig_pie.update_layout(**PLOTLY_LAYOUT, height=400)
        fig_pie.update_traces(textinfo='label+percent', textfont_size=13)
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">Provider Cost by Service</div>', unsafe_allow_html=True)
        prov_svc = filtered.groupby(['cloud_provider', 'service'])['net_cost'].sum().reset_index()
        fig_prov_svc = px.bar(prov_svc, x='cloud_provider', y='net_cost', color='service',
                             barmode='group', color_discrete_sequence=PLOTLY_LAYOUT['colorway'])
        fig_prov_svc.update_layout(**PLOTLY_LAYOUT, height=400, title='Cost by Provider × Service')
        fig_prov_svc.update_yaxes(title='Net Cost (USD)')
        st.plotly_chart(fig_prov_svc, use_container_width=True)

    # Region analysis
    st.markdown('<div class="section-header">Cost by Region</div>', unsafe_allow_html=True)
    region_cost = filtered.groupby(['region', 'cloud_provider'])['net_cost'].sum().reset_index()
    fig_region = px.bar(region_cost, x='region', y='net_cost', color='cloud_provider',
                       barmode='stack', color_discrete_sequence=['#818CF8', '#34D399', '#FBBF24'])
    fig_region.update_layout(**PLOTLY_LAYOUT, height=400, title='Cost by Region (Stacked by Provider)')
    fig_region.update_yaxes(title='Net Cost (USD)')
    st.plotly_chart(fig_region, use_container_width=True)

    # Discount comparison
    st.markdown('<div class="section-header">Discount & Commitment Metrics by Provider</div>', unsafe_allow_html=True)
    prov_metrics = filtered.groupby('cloud_provider').agg(
        avg_discount=('discount_rate_pct', 'mean'),
        avg_sp_cov=('savings_plan_coverage_pct', 'mean'),
        avg_ri_cov=('reserved_instance_coverage_pct', 'mean'),
        avg_on_demand=('on_demand_exposure', 'mean')
    ).reset_index()
    prov_metrics_melted = pd.melt(prov_metrics, id_vars='cloud_provider',
                                  var_name='Metric', value_name='Value')
    prov_metrics_melted['Metric'] = prov_metrics_melted['Metric'].map({
        'avg_discount': 'Discount Rate',
        'avg_sp_cov': 'Savings Plan Coverage',
        'avg_ri_cov': 'RI Coverage',
        'avg_on_demand': 'On-Demand Exposure'
    })
    fig_metrics = px.bar(prov_metrics_melted, x='cloud_provider', y='Value', color='Metric',
                        barmode='group', color_discrete_sequence=['#818CF8', '#C084FC', '#FBBF24', '#F87171'])
    fig_metrics.update_layout(**PLOTLY_LAYOUT, height=400)
    fig_metrics.update_yaxes(title='Percentage', tickformat='.0%')
    st.plotly_chart(fig_metrics, use_container_width=True)


# ── TAB 4: Waste Detection ─────────────────────────────────────
with tab4:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-header">Top Wasteful Projects</div>', unsafe_allow_html=True)
        waste_projects = filtered.groupby(['account_id', 'project_id']).agg(
            total_cost=('net_cost', 'sum'),
            avg_waste_score=('waste_score', 'mean'),
            avg_on_demand_exposure=('on_demand_exposure', 'mean'),
            idle_records=('idle_resource_indicator', 'sum'),
            total_records=('idle_resource_indicator', 'count')
        ).reset_index()
        waste_projects['idle_pct'] = (waste_projects['idle_records'] / waste_projects['total_records'] * 100).round(1)
        waste_projects = waste_projects.sort_values('avg_waste_score', ascending=False).head(15)
        waste_projects['project'] = waste_projects['account_id'] + '/' + waste_projects['project_id']

        fig_waste = px.bar(waste_projects, x='avg_waste_score', y='project', orientation='h',
                          color='avg_waste_score', color_continuous_scale='Reds',
                          hover_data=['total_cost', 'idle_pct'])
        fig_waste.update_layout(**PLOTLY_LAYOUT, height=500, title='Top 15 Projects by Waste Score',
                               coloraxis_showscale=False)
        fig_waste.update_xaxes(title='Average Waste Score')
        st.plotly_chart(fig_waste, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">Idle Resource Distribution</div>', unsafe_allow_html=True)
        idle_by_env = filtered.groupby('environment')['idle_resource_indicator'].mean().reset_index()
        idle_by_env['idle_resource_indicator'] *= 100
        fig_idle = px.bar(idle_by_env, x='environment', y='idle_resource_indicator',
                         color='environment', color_discrete_sequence=['#818CF8', '#FBBF24', '#34D399'])
        fig_idle.update_layout(**PLOTLY_LAYOUT, height=300, title='Idle Rate by Environment',
                              showlegend=False)
        fig_idle.update_yaxes(title='Idle Resource Rate (%)')
        st.plotly_chart(fig_idle, use_container_width=True)

        # Anomaly breakdown
        st.markdown('<div class="section-header">Anomaly Detection</div>', unsafe_allow_html=True)
        anomalies = filtered[filtered['is_anomaly_derived'] == 1]
        if len(anomalies) > 0:
            anom_by_svc = anomalies.groupby('service')['net_cost'].sum().sort_values(ascending=True).reset_index()
            fig_anom = px.bar(anom_by_svc, x='net_cost', y='service', orientation='h',
                            color='net_cost', color_continuous_scale='Reds')
            fig_anom.update_layout(**PLOTLY_LAYOUT, height=300, title=f'Anomalous Cost by Service ({len(anomalies):,} records)',
                                 coloraxis_showscale=False)
            fig_anom.update_xaxes(title='Net Cost (USD)')
            st.plotly_chart(fig_anom, use_container_width=True)
        else:
            st.info("No anomalies detected in the current filter selection.")

    # Non-production cost analysis
    st.markdown('<div class="section-header">Non-Production Spend Analysis</div>', unsafe_allow_html=True)
    col3, col4, col5 = st.columns(3)

    env_costs = filtered.groupby('environment')['net_cost'].sum()
    total = env_costs.sum()

    with col3:
        prod_cost = env_costs.get('prod', 0)
        st.metric("Production Cost", f"${prod_cost:,.0f}", f"{prod_cost/total*100:.1f}% of total")
    with col4:
        staging_cost = env_costs.get('staging', 0)
        st.metric("Staging Cost", f"${staging_cost:,.0f}", f"{staging_cost/total*100:.1f}% of total")
    with col5:
        dev_cost = env_costs.get('dev', 0)
        st.metric("Dev Cost", f"${dev_cost:,.0f}", f"{dev_cost/total*100:.1f}% of total")

    # Savings opportunity
    st.markdown('<div class="section-header">💡 Estimated Savings Opportunities</div>', unsafe_allow_html=True)
    non_prod_savings = (staging_cost * 0.6 + dev_cost * 0.7)
    commitment_savings = total * 0.08
    idle_savings = total * idle_pct / 100 * 0.5

    savings_data = pd.DataFrame({
        'Opportunity': ['Non-Prod Scheduling', 'Increase Commitments', 'Idle Resource Cleanup', 'Spot Instance Adoption'],
        'Estimated Annual Savings': [non_prod_savings, commitment_savings, idle_savings, total * 0.03],
        'Effort': ['Medium', 'Medium', 'Low', 'High']
    })
    savings_data['Estimated Annual Savings'] = savings_data['Estimated Annual Savings'].apply(lambda x: f"${x:,.0f}")
    st.dataframe(savings_data, hide_index=True, use_container_width=True)


# ── TAB 5: Detailed Data ──────────────────────────────────────
with tab5:
    st.markdown('<div class="section-header">Filtered Data Explorer</div>', unsafe_allow_html=True)
    st.markdown(f"Showing **{len(filtered):,}** records based on current filters.")

    display_cols = ['date', 'cloud_provider', 'account_id', 'project_id', 'environment',
                   'business_unit', 'department', 'service', 'resource_type', 'region',
                   'usage_quantity', 'usage_unit', 'list_cost', 'net_cost', 'discount_amount',
                   'cost_efficiency_ratio', 'on_demand_exposure', 'waste_score',
                   'idle_resource_indicator', 'is_anomaly_derived']

    st.dataframe(filtered[display_cols].head(500), hide_index=True, use_container_width=True)

    # Download button
    csv = filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        "📥 Download Filtered Data (CSV)",
        csv,
        "cloud_budget_filtered.csv",
        "text/csv"
    )


# ── Footer ─────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    '<div style="text-align: center; color: #64748B; font-size: 12px;">'
    'Cloud Cost Optimizer Dashboard | Data: 2023 | Built with Streamlit + Plotly'
    '</div>',
    unsafe_allow_html=True
)
