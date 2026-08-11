# Cloud Cost Optimization Analysis

> **Accenture Data Analytics Capstone Project**  
> *Uncovering avoidable cloud spend across AWS, Azure & GCP — and building the roadmap to reclaim it.*

---

## 📌 Overview

Cloud spending can become difficult to understand and control when resources are distributed across multiple cloud providers, teams, services, regions, and environments.

This project analyzes cloud billing data to identify potential cost inefficiencies, create meaningful cost-optimization KPIs, and turn the findings into actionable recommendations through an interactive dashboard.

## 🎯 Objectives

- Analyze cloud spending and usage patterns
- Identify potential areas of avoidable spending
- Engineer cost-efficiency and FinOps KPIs
- Detect anomalies and high-exposure resources
- Compare spending across providers, teams, services, and environments
- Build an interactive dashboard for decision-makers
- Recommend practical cloud-cost optimization actions

## 📊 Dataset

**Source:** Kaggle — Cloud Budget Dataset

| Attribute | Details |
|---|---|
| Records | 54,750 |
| Columns | 40 |
| Period | FY2023 |
| Cloud Providers | AWS, Azure, GCP |
| Regions | 6 |

The dataset contains billing, usage, ownership, service, environment, discount, commitment, anomaly, and forecast-related information.

## 🔄 Workflow

```text
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

- **Python**
- **Pandas / NumPy** — data preparation and analysis
- **Matplotlib / Plotly** — visualization
- **Streamlit** — interactive dashboard
- **Jupyter / VS Code** — development
- **Git / GitHub** — version control

## 🔎 Key Findings

Our analysis highlighted several areas that may require optimization:

- Cloud spending increased by **38.5% from January to December**
- **Dev + Staging account for 22.2% of total spending**
- Average commitment coverage is approximately **54.1%**
- **11.3% of resource-days** meet the project's high-exposure condition
- Approximately **8.4% of records** have low Savings Plan and Reserved Instance coverage
- The analysis identified an estimated **$123K–$188K annual savings opportunity**

> **Note:** The savings figure represents an estimated opportunity identified through the analysis, not guaranteed realized savings.

## 🖥️ Interactive Dashboard

### 🌐 Live Application

**[Launch the Cloud Cost Optimizer Dashboard](https://cloud-cost-optimizer-room4.streamlit.app/)**

The Streamlit dashboard allows users to interactively explore the cloud cost analysis.

### Dashboard includes

- Total and daily cloud spend
- Monthly cost trends
- Provider comparisons
- Business unit analysis
- Department-level cost analysis
- Cost-efficiency metrics
- Cost by service and region
- High-exposure / potential waste areas
- Anomaly detection
- Top projects by waste score
- Estimated savings opportunities
- Detailed filtered data
- CSV download of filtered results

### Dashboard filters

Users can filter the analysis by:

- Date Range
- Cloud Provider
- Business Unit
- Department
- Environment
- Region
- Service

## 💻 Running the Dashboard Locally

The dashboard can also be run locally from the repository.

### 1. Clone the repository

```bash
git clone git@github.com:Proms32/Accenture-capstone-project.git
cd Accenture-capstone-project
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

### 3. Activate the environment

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Streamlit dashboard

```bash
streamlit run codes/dashboard.py
```

The dashboard will be available at:

```text
http://localhost:8501
```

### Main components

| Component | Description |
|---|---|
| `codes/dashboard.py` | Interactive Streamlit + Plotly dashboard |
| `codes/data_cleaning.py` | Data cleaning and preparation |
| `codes/eda_analysis.py` | Exploratory data analysis |
| `dataset/` | Raw and cleaned cloud billing datasets |
| `charts/` | EDA and analysis visualizations |
| `*.md` reports | Business, EDA, data-quality and recommendation documentation |
| `Cloud_Cost_Optimization_Professional_Deck_Final.pptx` | Final project presentation |
| `requirements.txt` | Python dependencies |

## 📚 Project Documentation

Detailed analysis and presentation material are included in the repository:

- **EDA Report** — detailed exploratory analysis and visualizations
- **Business Insights** — key findings derived from the analysis
- **Recommendations** — proposed cloud cost-optimization actions
- **Data Understanding** — overview of the dataset and its attributes
- **Data Quality Report** — data validation and quality assessment
- **Business Understanding** — project context and objectives
- **Implementation Plan** — project implementation approach
- **Project Presentation** — business story, findings and recommendations
- **Analysis Scripts** — data cleaning, EDA and dashboard implementation

## 🚀 Future Scope

- Real-time cloud-cost monitoring
- ML-based cost forecasting
- Automated anomaly detection
- Resource rightsizing recommendations
- Automated optimization recommendations
- Broader multi-cloud cost optimization

## 👥 Team

**Accenture Data Analytics Capstone Project**

| Team Member |
|---|
| **Proma Mondal** |
| **Yash Choudhary** |
| **Anurag Vyas** |
| **Aditya Marathe** |
| **Neam Adil** |

## 📌 Project

**Cloud Cost Optimization Analysis**  
**Accenture Data Analytics Capstone Project**
