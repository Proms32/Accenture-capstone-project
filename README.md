# Cloud Cost Optimization Analysis

> **Accenture Data Analytics Capstone Project**\
> *Uncovering avoidable cloud spend across AWS, Azure & GCP --- and
> building the roadmap to reclaim it.*

## 📌 Overview

Cloud spending can become difficult to understand and control when
resources are distributed across multiple cloud providers, teams,
services, regions, and environments.

This project analyzes cloud billing data to identify potential cost
inefficiencies, create meaningful cost-optimization KPIs, and turn the
findings into actionable recommendations through an interactive
dashboard.

## 🎯 Objectives

-   Analyze cloud spending and usage patterns
-   Identify potential areas of avoidable spending
-   Engineer cost-efficiency and FinOps KPIs
-   Detect anomalies and high-exposure resources
-   Compare spending across providers, teams, services, and environments
-   Build an interactive dashboard for decision-makers
-   Recommend practical cloud-cost optimization actions

## 📊 Dataset

**Source:** Kaggle --- Cloud Budget Dataset

  ----------------- -----------------
  Records                      54,750
  Columns                          40
  Period                       FY2023
  Cloud Providers     AWS, Azure, GCP
  Regions                           6
  ----------------- -----------------

The dataset contains billing, usage, ownership, service, environment,
discount, commitment, anomaly, and forecast-related information.

## 🔄 Workflow

``` text
Cloud Billing Data
       ↓
Data Cleaning & Validation
       ↓
KPI Engineering
       ↓
Exploratory Data Analysis
       ↓
Cost / Waste Analysis
       ↓
Interactive Dashboard
       ↓
Recommendations
```

## 🛠️ Tech Stack

-   **Python**
-   **Pandas / NumPy** --- data preparation and analysis
-   **Matplotlib / Plotly** --- visualization
-   **Streamlit** --- interactive dashboard
-   **Jupyter / VS Code** --- development
-   **Git / GitHub** --- version control

## 🔎 Key Findings

Our analysis highlighted several areas that may require optimization:

-   Cloud spending increased by **38.5% from January to December**
-   **Dev + Staging account for 22.2% of total spending**
-   Average commitment coverage is approximately **54.1%**
-   **11.3% of resource-days** meet the project's high-exposure
    condition
-   Approximately **8.4% of records** have low Savings Plan and Reserved
    Instance coverage
-   The analysis identified an estimated **\$123K--\$188K annual savings
    opportunity**

> The savings figure represents an estimated opportunity identified
> through the analysis, not guaranteed realized savings.

## 🖥️ Dashboard

The project includes an interactive **Streamlit + Plotly dashboard**
that allows users to explore:

-   Total and daily cloud spend
-   Cost trends
-   Provider and department comparisons
-   Cost-efficiency metrics
-   High-exposure / potential waste areas
-   Anomalies
-   Top projects by cost

### Dashboard filters

-   Date
-   Cloud Provider
-   Business Unit
-   Department
-   Environment
-   Region
-   Service

## 📁 Project Structure

``` text
cloud-cost-optimization/
│
├── data/
├── notebooks/
├── src/
├── dashboard/
├── charts/
├── reports/
├── requirements.txt
└── README.md
```

## ▶️ Getting Started

### Clone the repository

``` bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd cloud-cost-optimization
```

### Install dependencies

``` bash
pip install -r requirements.txt
```

### Run the dashboard

``` bash
streamlit run dashboard/dashboard.py
```

> Update the paths above if the final repository structure differs.

## 📚 Project Documentation

Detailed analysis and presentation material can be maintained separately
from this README:

-   **EDA Report** --- detailed exploratory analysis and visualizations
-   **Project Presentation** --- business story, findings and
    recommendations
-   **Analysis Notebook** --- data preparation and analysis
-   **Dashboard** --- interactive exploration of the results

## 🚀 Future Scope

-   Real-time cloud-cost monitoring
-   ML-based cost forecasting
-   Automated anomaly detection
-   Resource rightsizing recommendations
-   Automated optimization recommendations
-   Broader multi-cloud cost optimization

## 👥 Project

**Cloud Cost Optimization Analysis**\
**Accenture Data Analytics Capstone Project**
