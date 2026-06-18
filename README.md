# 🍱 Local Food Wastage Management System

## 📌 Project Overview

The Local Food Wastage Management System is an end-to-end Data Analytics project designed to analyze food donation, redistribution, and claim patterns across a food-sharing platform.

Using PostgreSQL, SQL, Python, Pandas, and Streamlit, the project transforms raw operational data into actionable business insights through interactive dashboards and analytical reporting.

The objective is to identify inefficiencies in food redistribution, improve claim completion rates, reduce food wastage, and support data-driven decision-making.

---

# 🎯 Business Problem

Food providers often have surplus food that could be redistributed to NGOs, charities, shelters, and individuals. However, inefficient matching, delayed claims, and poor visibility into supply and demand can result in unnecessary food waste.

This project provides analytical dashboards and business intelligence tools to monitor:

* Food supply patterns
* Receiver demand behavior
* Claim completion performance
* Food expiry risks
* Operational efficiency

---

# 🛠️ Technology Stack

### Programming & Analytics

* Python
* Pandas
* NumPy

### Database

* PostgreSQL
* SQLAlchemy
* Psycopg2

### Visualization

* Streamlit
* Matplotlib
* Seaborn

### Development Tools

* VS Code
* Jupyter Notebook
* pgAdmin 4
* Git & GitHub

---

# 🗄️ Database Schema

The project uses four relational tables.

## Providers

| Column      |
| ----------- |
| Provider_ID |
| Name        |
| Type        |
| Address     |
| City        |
| Contact     |

---

## Receivers

| Column      |
| ----------- |
| Receiver_ID |
| Name        |
| Type        |
| City        |
| Contact     |

---

## Food Listings

| Column        |
| ------------- |
| Food_ID       |
| Food_Name     |
| Quantity      |
| Expiry_Date   |
| Provider_ID   |
| Provider_Type |
| Location      |
| Food_Type     |
| Meal_Type     |

---

## Claims

| Column      |
| ----------- |
| Claim_ID    |
| Food_ID     |
| Receiver_ID |
| Status      |
| Timestamp   |

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

A total of 13 business-focused SQL queries were implemented and integrated into the SQL Explorer dashboard.

## Level 1 – Single Table Queries

### Query 1

Total Food Quantity Available

### Query 2

City with Highest Number of Food Listings

### Query 3

Most Common Food Types

### Query 4

Claim Status Percentage Distribution

### Query 5

Provider Contact Lookup

---

## Level 2 – Two Table Queries

### Query 6

Food Listings by Provider

### Query 7

Claims by Receiver

### Query 8

Food Type Demand Analysis

### Query 9

Most Claimed Meal Type

### Query 10

Top Providers by Quantity Donated

---

## Level 3 – Advanced Analytics

### Query 11

Provider with Most Successful Claims

### Query 12

Average Quantity Claimed per Receiver

### Query 13

Detailed Claims Analysis Report

All 13 queries can be explored interactively within the SQL Explorer dashboard.

---

# 📈 Dashboard Pages

## Executive Summary Dashboard

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

## Supply Analysis

Analyzes food supply patterns across providers.

### Visualizations

* Provider Type Distribution
* Food Type Distribution
* Meal Type Distribution
* Top Cities by Listings

### Key Focus

* Food availability
* Provider participation
* Regional distribution

---

## Demand Analysis

Analyzes receiver behavior and food demand.

### Visualizations

* Claim Status Distribution
* Receiver Type Distribution
* Claims by Meal Type
* Top Receivers by Claims

### Key Focus

* Demand concentration
* Receiver engagement
* Claim trends

---

## Operations Analysis

Monitors redistribution efficiency.

### Visualizations

* Days Until Expiry Distribution
* Completion Rate by Receiver Type
* Top Providers by Successful Claims
* Average Quantity per Receiver

### Operational KPIs

* Completion Rate
* Successful Claims
* Expired Claims
* Average Days Until Expiry

---

## SQL Explorer

Interactive SQL analysis interface.

Each query displays:

* Business Question
* SQL Query
* Query Output
* Business Insight

Features:

* Expandable SQL code blocks
* Live PostgreSQL execution
* Top 20 rows preview for large results

---

## Business Insights

Executive-level findings and recommendations derived from EDA, SQL analysis, and dashboard metrics.

Includes:

* Strategic findings
* Operational recommendations
* Risk identification
* Improvement opportunities

---

# 💡 Key Business Insights

## 1. Low Claim Completion Rate

Only 339 out of 1,000 claims were completed successfully.

**Completion Rate:** 33.9%

### Business Impact

A significant portion of food listings are not successfully redistributed.

### Recommendation

Implement automated reminders and improve claim follow-up workflows.

---

## 2. Breakfast Has the Highest Demand

Breakfast generated 278 claims, making it the most requested meal category.

### Business Impact

Receiver demand is strongest for breakfast-related food items.

### Recommendation

Encourage providers to prioritize breakfast donations.

---

## 3. Demand Exceeds Supply in Several Categories

Certain meal categories show substantially higher claim activity compared to listing volume.

### Business Impact

Supply-demand imbalance can reduce redistribution effectiveness.

### Recommendation

Align donation campaigns with high-demand meal categories.

---

## 4. NGOs and Charities Drive Platform Usage

NGOs and charities account for the largest share of receiver participation.

### Business Impact

These organizations are the primary beneficiaries of redistribution efforts.

### Recommendation

Strengthen partnerships and engagement programs with high-performing receiver groups.

---

## 5. Food Expiry Risk Requires Attention

55 claims occurred after food expiry dates.

Among them, 15 claims were marked as completed.

### Business Impact

Expired food redistribution introduces operational and food-safety risks.

### Recommendation

Implement expiry alerts and block claims on expired inventory.

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
├── queries.sql
├── database.sql
├── requirements.txt
├── README.md
│
├── eda.ipynb
├── data_cleaning.ipynb
├── profiling_notes.ipynb
│
└── .gitignore
```

---

# 🚀 How to Run the Project

## Clone Repository

```bash
git clone <repository-url>
cd Local-Food-Wastage-Management-System
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Configure Environment Variables

Create a `.env` file:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=food_wastage_db
DB_USER=your_username
DB_PASSWORD=your_password
```

## Run Streamlit Application

```bash
streamlit run app.py
```

---

# 📷 Dashboard Screenshots

Add screenshots of:

* Executive Summary Dashboard
* Supply Analysis
* Demand Analysis
* Operations Analysis
* SQL Explorer
* Business Insights

inside the `Image/` folder and embed them here.

---

# 👨‍💻 Author

**Raju Kumar S**

Data Analyst | SQL | PostgreSQL | Power BI | Excel | Streamlit

### Connect With Me

* LinkedIn: https://www.linkedin.com/in/YOUR-LINKEDIN
* GitHub: https://github.com/YOUR-GITHUB
* Portfolio: https://YOUR-PORTFOLIO

This project demonstrates skills in data cleaning, SQL analysis, PostgreSQL database design, dashboard development, business intelligence, and data storytelling.
