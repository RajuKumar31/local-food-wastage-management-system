# 🍱 Local Food Wastage Management System

## 📌 Project Overview

The Local Food Wastage Management System is an end-to-end Data Analytics and Business Intelligence project designed to analyze food donation, redistribution, and claim activity across a food-sharing ecosystem.

The solution integrates PostgreSQL (Neon Cloud Database), SQL, Python, Pandas, and Streamlit to transform operational data into actionable business insights through interactive dashboards and analytical reporting.

The primary objective is to reduce food wastage, improve redistribution efficiency, optimize claim completion rates, and support data-driven decision-making.

---

# 🚀 Project Highlights

✅ Built an end-to-end analytics solution using PostgreSQL, SQL, Python, and Streamlit

✅ Designed and implemented a relational database with 4 interconnected tables

✅ Developed 6 interactive dashboard pages

✅ Performed SQL-based business analysis using 13 analytical queries

✅ Deployed data from local PostgreSQL to Neon Cloud PostgreSQL

✅ Generated business recommendations to improve redistribution efficiency

---

# 🎯 Business Problem

Food providers such as restaurants, supermarkets, catering services, and grocery stores frequently generate surplus food that can be redistributed to NGOs, charities, shelters, and community organizations.

However, inefficient claim management, delayed redistribution, and poor visibility into supply-demand patterns often lead to unnecessary food wastage.

This project provides analytical dashboards and business intelligence tools to monitor:

* Food supply patterns
* Receiver demand behavior
* Claim completion performance
* Food expiry risks
* Provider contribution trends
* Operational efficiency

---

# 🛠️ Technology Stack

## Programming & Analytics

* Python
* Pandas
* NumPy

## Database

* PostgreSQL
* Neon PostgreSQL (Cloud Database)
* SQLAlchemy
* Psycopg2

## Visualization

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

# 🗄️ Database Schema

The project consists of four relational tables.

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

Providers → Food Listings

Food Listings → Claims

Receivers → Claims

This relational structure enables supply, demand, and operational analysis across the entire food redistribution lifecycle.

---

# 📊 Dataset Overview

The project analyzes:

* 1,000 Providers
* 1,000 Receivers
* 1,000 Food Listings
* 1,000 Claims

Data was cleaned, validated, profiled, and loaded into PostgreSQL before analysis.

---

# 🔍 SQL Analysis

A total of 13 business-focused SQL queries were developed and integrated into the SQL Explorer dashboard.

## Level 1 – Descriptive Analysis

1. Total Food Quantity Available
2. City with Highest Number of Food Listings
3. Most Common Food Types
4. Claim Status Percentage Distribution
5. Provider Contact Lookup

## Level 2 – Relational Analysis

6. Food Listings by Provider
7. Claims by Receiver
8. Food Type Demand Analysis
9. Most Claimed Meal Type
10. Top Providers by Quantity Donated

## Level 3 – Business Insights

11. Provider with Most Successful Claims
12. Average Quantity Claimed per Receiver
13. Detailed Claims Analysis Report

All queries can be executed directly through the SQL Explorer dashboard.

---

# 📈 Dashboard Pages

## 1. Executive Summary Dashboard

Provides a high-level overview of platform performance.

### KPIs

* Total Providers
* Total Receivers
* Total Food Listings
* Claim Completion Rate

### Visualizations

* Provider Type Distribution
* Claim Status Distribution

---

## 2. Supply Analysis

Analyzes food availability and provider contributions.

### Features

* Provider Type Filters
* Food Type Filters
* Meal Type Filters

### Visualizations

* Food Type Distribution
* Meal Type Distribution
* Top Providers by Quantity
* Provider Contribution Analysis

---

## 3. Demand Analysis

Analyzes receiver behavior and food demand patterns.

### Visualizations

* Receiver Type Distribution
* Claim Status Distribution
* Meal Type Demand Analysis
* Top Receivers by Claims

---

## 4. Operations Analysis

Monitors redistribution effectiveness and food expiry risk.

### KPIs

* Claim Completion Rate
* Successful Claims
* Expired Claims
* Average Days Until Expiry

### Visualizations

* Days Until Expiry Distribution
* Completion Rate by Receiver Type
* Top Providers by Successful Claims
* Average Quantity Claimed per Receiver

---

## 5. SQL Explorer

Interactive SQL analysis interface.

### Features

* Business Questions
* SQL Queries
* Query Results
* Business Insights

---

## 6. Business Insights

Executive-level findings and recommendations derived from:

* SQL Analysis
* Exploratory Data Analysis
* Dashboard Metrics
* Operational Trends

---

# 💡 Key Business Insights

## Low Claim Completion Rate

Completed Claims: 339

Completion Rate: 33.9%

### Recommendation

Implement automated reminders and improve claim follow-up workflows.

---

## Breakfast Has Highest Demand

Breakfast generated the highest number of claims.

### Recommendation

Encourage providers to prioritize breakfast donations.

---

## Supply-Demand Imbalance

Certain meal categories experience significantly higher demand than supply.

### Recommendation

Align food donation campaigns with demand trends.

---

## NGOs Drive Platform Usage

NGOs and charitable organizations account for the largest share of claims.

### Recommendation

Strengthen engagement and partnership programs.

---

## Food Expiry Risk

Multiple claims occurred after food expiry dates.

### Recommendation

Implement expiry alerts and automated claim restrictions.

---

# 📂 Project Structure

```text
local-food-wastage-management-system/

│
├── Data/
├── Image/
├── pages/
│
├── app.py
├── database.sql
├── queries.sql
├── requirements.txt
├── README.md
│
├── eda.ipynb
├── data_cleaning.ipynb
├── profiling_notes.ipynb
│
├── .gitignore
└── .streamlit/
```

---

# 🚀 How to Run the Project

## Clone Repository

```bash
git clone <repository-url>
cd local-food-wastage-management-system
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Configure Database

Create a `.streamlit/secrets.toml` file:

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

**Raju Kumar S**

Data Analyst | Business Analyst | Power BI Developer

### Connect With Me

LinkedIn:
https://www.linkedin.com/in/rajukumarsahani/

GitHub:
https://github.com/RajuKumar31

Portfolio:
https://rajukumar31.github.io/

---

## Skills Demonstrated

* Data Cleaning & Validation
* Exploratory Data Analysis (EDA)
* Database Design
* PostgreSQL & SQL
* Business Intelligence
* Data Visualization
* Dashboard Development
* Streamlit Deployment
* Business Insight Generation
* Analytical Problem Solving
