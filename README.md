# 🍱 Local Food Wastage Management System

## 🚀 Live Application

🔗 **Explore the Dashboard:**
https://local-food-wastage-management-system-m4gt6gc6bjfa3sn5okqgf8.streamlit.app/

---

# 🌍 Transforming Surplus Food into Actionable Impact

The **Local Food Wastage Management System** is an end-to-end Data Analytics and Business Intelligence solution designed to reduce food wastage by connecting food providers with organizations and individuals in need.

The project leverages **PostgreSQL, SQL, Python, Pandas, and Streamlit** to transform operational food redistribution data into meaningful business insights through interactive dashboards, analytical reporting, and executive-level recommendations.

By analyzing food availability, demand patterns, claim activity, and operational performance, the platform helps stakeholders make data-driven decisions that improve redistribution efficiency and minimize food waste.

---

# 🎯 Business Problem

Every day, restaurants, supermarkets, catering services, and grocery stores generate surplus food that could be redistributed instead of discarded.

At the same time, NGOs, shelters, charities, and community organizations face challenges accessing available food resources.

Without proper visibility into:

* Food supply
* Receiver demand
* Claim activity
* Expiry risks
* Provider performance

valuable food resources are often wasted.

This project addresses these challenges through a centralized analytics platform that enables efficient food redistribution and operational monitoring.

---

# ⭐ Project Highlights

✅ Designed and implemented a relational PostgreSQL database

✅ Built a complete analytics pipeline using SQL and Python

✅ Developed 6 interactive business dashboards

✅ Created 13 business-focused SQL analyses

✅ Integrated PostgreSQL with Streamlit

✅ Deployed cloud-hosted solution using Neon PostgreSQL and Streamlit Community Cloud

✅ Generated executive-level business recommendations

✅ Applied real-world Data Analyst and Business Intelligence workflows

---

# 📊 Business Questions Answered

This solution helps stakeholders answer critical questions such as:

### Supply Analysis

* Which provider types contribute the most food?
* Which meal categories have the highest inventory?
* Who are the top food contributors?

### Demand Analysis

* Which receivers submit the most claims?
* Which meal types generate the highest demand?
* How is demand distributed across receiver categories?

### Operations Analysis

* What percentage of claims are completed successfully?
* How close to expiry is food when claimed?
* Which providers achieve the highest successful claim rates?

### Strategic Insights

* Where are operational bottlenecks occurring?
* Which areas require process improvement?
* How can food redistribution efficiency be increased?

---

# 🛠️ Technology Stack

## Data Analytics

* Python
* Pandas
* NumPy

## Database

* PostgreSQL
* Neon PostgreSQL (Cloud Database)
* SQLAlchemy
* Psycopg2

## Data Visualization

* Streamlit
* Matplotlib
* Seaborn

## Development Tools

* VS Code
* Jupyter Notebook
* pgAdmin 4
* Git
* GitHub

---

# 🏗️ Solution Architecture

```text
Raw CSV Files
        │
        ▼
Data Cleaning & Validation
        │
        ▼
Exploratory Data Analysis
        │
        ▼
PostgreSQL Database
        │
        ▼
SQL Business Analytics
        │
        ▼
Interactive Streamlit Dashboards
        │
        ▼
Executive Business Insights
```

---

# 🗄️ Database Schema

The project uses four interconnected relational tables.

## Providers

| Column      |
| ----------- |
| provider_id |
| name        |
| type        |
| address     |
| city        |
| contact     |

## Receivers

| Column      |
| ----------- |
| receiver_id |
| name        |
| type        |
| city        |
| contact     |

## Food Listings

| Column        |
| ------------- |
| food_id       |
| food_name     |
| quantity      |
| expiry_date   |
| provider_id   |
| provider_type |
| location      |
| food_type     |
| meal_type     |

## Claims

| Column      |
| ----------- |
| claim_id    |
| food_id     |
| receiver_id |
| status      |
| timestamp   |

---

# 🔗 Entity Relationships

```text
Providers
    │
    ▼
Food Listings
    │
    ▼
Claims
    ▲
    │
Receivers
```

This structure enables end-to-end analysis of the food redistribution lifecycle.

---

# 📊 Dataset Overview

The project analyzes:

| Dataset       | Records |
| ------------- | ------- |
| Providers     | 1,000   |
| Receivers     | 1,000   |
| Food Listings | 1,000   |
| Claims        | 1,000   |

Total records analyzed: **4,000+**

---

# 🔍 SQL Business Analytics

A dedicated SQL Explorer was developed to demonstrate business-focused SQL problem solving.

## Level 1 — Single Table Analysis

1. Total Food Quantity Available
2. City with Highest Food Listings
3. Most Common Food Types
4. Claim Status Distribution
5. Provider Contact Lookup

## Level 2 — Relational Analysis

6. Food Listings by Provider
7. Claims by Receiver
8. Food Type Demand Analysis
9. Most Claimed Meal Type
10. Top Providers by Quantity Donated

## Level 3 — Business Insights

11. Provider with Most Successful Claims
12. Average Quantity Claimed per Receiver
13. Detailed Claims Performance Report

---

# 📈 Dashboard Modules

## 🏠 Executive Dashboard

High-level platform overview with key performance indicators.

### KPIs

* Total Providers
* Total Receivers
* Total Food Listings
* Claim Completion Rate

---

## 📦 Supply Analysis

Analyzes inventory availability and provider contribution trends.

### Visualizations

* Provider Type Distribution
* Food Type Distribution
* Meal Type Distribution
* Top Providers by Quantity
* Provider Contribution Analysis

---

## 🤝 Demand Analysis

Analyzes receiver behavior and food demand patterns.

### Visualizations

* Claim Status Distribution
* Receiver Type Distribution
* Claims by Meal Type
* Top Receivers by Claims

---

## ⚙️ Operations Analysis

Evaluates redistribution efficiency and operational performance.

### KPIs

* Completion Rate
* Successful Claims
* Expired Claims
* Average Days Until Expiry

### Visualizations

* Days Until Expiry Distribution
* Completion Rate by Receiver Type
* Top Providers by Successful Claims
* Average Quantity Claimed per Receiver

---

## 🗄️ SQL Explorer

Interactive SQL analytics interface featuring:

* Business Questions
* SQL Queries
* Query Results
* Business Insights

---

## 💡 Business Insights

Executive-level recommendations generated from:

* SQL Analysis
* Exploratory Data Analysis
* Operational Metrics
* Dashboard KPIs

---

# 📈 Key Business Insights

### Claim Completion Requires Improvement

Current completion rate stands at approximately **33.9%**.

**Recommendation:**
Implement automated reminders and claim tracking workflows.

---

### Breakfast Demand Is Highest

Breakfast generates the highest claim volume.

**Recommendation:**
Increase breakfast-focused food donation campaigns.

---

### Supply-Demand Imbalance Exists

Certain food categories experience significantly higher demand than supply.

**Recommendation:**
Align provider outreach initiatives with demand patterns.

---

### NGOs Drive Platform Utilization

NGOs and charitable organizations account for a significant share of claims.

**Recommendation:**
Strengthen NGO engagement and partnership programs.

---

### Food Expiry Risk Remains Significant

Several claims occur close to expiry dates.

**Recommendation:**
Implement automated expiry alerts and prioritization systems.

---

# 🏆 Key Results

* Built 6 dashboard modules
* Developed 13 SQL business analyses
* Integrated PostgreSQL with Streamlit
* Created cloud-hosted analytics application
* Generated actionable business recommendations
* Delivered end-to-end analytics workflow

---

# 💼 Skills Demonstrated

### Analytics

* Exploratory Data Analysis (EDA)
* Data Cleaning & Validation
* Statistical Analysis

### Database

* PostgreSQL
* SQL Query Optimization
* Relational Database Design

### Business Intelligence

* KPI Development
* Dashboard Design
* Business Reporting
* Data Storytelling

### Development

* Python
* Streamlit
* Git & GitHub
* Cloud Deployment

---

# 📂 Project Structure

```text
local-food-wastage-management-system/

├── Data/
├── Image/
├── pages/

├── app.py
├── database.sql
├── queries.sql
├── requirements.txt
├── README.md

├── eda.ipynb
├── data_cleaning.ipynb
├── profiling_notes.ipynb

├── .gitignore
└── .streamlit/
```

---

# 🚀 Running the Project Locally

## Clone Repository

```bash
git clone https://github.com/RajuKumar31/local-food-wastage-management-system.git
cd local-food-wastage-management-system
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Configure Database Secrets

Create:

```text
.streamlit/secrets.toml
```

Add:

```toml
DB_HOST="your_host"
DB_PORT="5432"
DB_NAME="your_database"
DB_USER="your_username"
DB_PASSWORD="your_password"
```

## Run Application

```bash
streamlit run app.py
```

---

# 👨‍💻 Author

## Raju Kumar S

Data Analyst | Business Analyst | Power BI Developer

🔗 LinkedIn:
https://www.linkedin.com/in/rajukumarsahani/

🔗 GitHub:
https://github.com/RajuKumar31

🔗 Portfolio:
https://rajukumar31.github.io/

---

### If you found this project interesting, consider giving it a ⭐ on GitHub.
