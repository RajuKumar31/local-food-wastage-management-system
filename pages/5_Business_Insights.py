# ============================================
# PAGE 5: BUSINESS INSIGHTS
# ============================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# ============================================
# DATABASE CONNECTION
# ============================================

from pathlib import Path

@st.cache_resource
def get_engine():

    load_dotenv(
        Path(__file__).resolve().parent.parent / ".env"
    )

    connection_string = (
        f"postgresql+psycopg2://"
        f"{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}"
        f"/{os.getenv('DB_NAME')}"
    )

    return create_engine(connection_string)


# ============================================
# LOAD DATA
# ============================================

@st.cache_data
def load_data():

    engine = get_engine()

    providers = pd.read_sql(
        "SELECT * FROM providers",
        engine
    )

    receivers = pd.read_sql(
        "SELECT * FROM receivers",
        engine
    )

    food_listings = pd.read_sql(
        "SELECT * FROM food_listings",
        engine
    )

    claims = pd.read_sql(
        "SELECT * FROM claims",
        engine
    )

    return (
        providers,
        receivers,
        food_listings,
        claims
    )


providers, receivers, food_listings, claims = load_data()


# ============================================
# DATA PREPARATION
# ============================================

claims_analysis = (
    claims
    .merge(
        food_listings,
        on="Food_ID",
        how="left"
    )
)

completed_claims = (
    claims["Status"] == "Completed"
).sum()

completion_rate = (
    completed_claims
    / len(claims)
) * 100

total_food_available = (
    food_listings["Quantity"]
    .sum()
)

top_meal_type = (
    claims_analysis["Meal_Type"]
    .value_counts()
    .idxmax()
)

food_listings["Expiry_Date"] = pd.to_datetime(
    food_listings["Expiry_Date"]
)

claims["Timestamp"] = pd.to_datetime(
    claims["Timestamp"]
)

expiry_analysis = (
    claims
    .merge(
        food_listings[
            ["Food_ID", "Expiry_Date"]
        ],
        on="Food_ID",
        how="left"
    )
)

expiry_analysis["Days_Until_Expiry"] = (
    expiry_analysis["Expiry_Date"]
    - expiry_analysis["Timestamp"]
).dt.days

avg_days_until_expiry = (
    expiry_analysis["Days_Until_Expiry"]
    .mean()
)


# ============================================
# PAGE TITLE
# ============================================

st.title("📈 Business Insights")

st.markdown(
    """
    Executive-level insights and strategic
    recommendations derived from the analysis
    of food donations, claims and platform operations.
    """
)

st.divider()


# ============================================
# KPI CARDS
# ============================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Total Food Available",
        f"{total_food_available:,}"
    )

with col2:

    st.metric(
        "Completion Rate",
        f"{completion_rate:.1f}%"
    )

with col3:

    st.metric(
        "Top Claimed Meal Type",
        top_meal_type
    )

with col4:

    st.metric(
        "Avg Days Until Expiry",
        f"{avg_days_until_expiry:.1f}"
    )

st.divider()

# ============================================
# TOP BUSINESS FINDINGS
# ============================================

st.subheader("🏆 Top Business Findings")

st.success("""
**1. Only 33.9% of claims were successfully completed**

Source:
• EDA Chart 5
• SQL Query 4

Business Impact:
A significant proportion of food requests are either
cancelled or remain unresolved, representing lost
redistribution opportunities.

Recommended Action:
Investigate operational bottlenecks causing claim
cancellations and delayed processing.
""")

st.success("""
**2. Breakfast demand exceeds supply**

Source:
• EDA Chart 4
• EDA Chart 9
• SQL Query 9

Finding:
Breakfast generated 278 claims from only
254 available listings.

Business Impact:
Breakfast appears to be the highest-demand
meal category on the platform.

Recommended Action:
Encourage providers to donate more breakfast
items to better align supply with demand.
""")

st.success("""
**3. Restaurants contribute the highest food volume**

Source:
• SQL Query 6
• SQL Query 10

Finding:
Restaurants contributed 6,923 units of food,
the highest among all provider categories.

Business Impact:
Restaurants are the platform's most important
supply-side partners.

Recommended Action:
Strengthen restaurant partnerships and create
incentive programs for repeat donations.
""")

st.success("""
**4. Claim activity is broadly distributed**

Source:
• EDA Chart 7
• SQL Query 7

Finding:
The most active receivers submitted only
4–5 claims each.

Business Impact:
No single receiver dominates platform usage,
indicating relatively balanced access to food
redistribution services.

Recommended Action:
Continue monitoring equitable food distribution
across all receiver groups.
""")

st.success("""
**5. Expiry management presents operational risk**

Source:
• EDA Chart 8
• Operations Analysis

Finding:
55 claims (5.5%) occurred after the food expiry date,
including 15 completed claims.

Business Impact:
This indicates food is occasionally being redistributed
beyond its intended expiry window, creating potential
food safety and compliance concerns.

Recommended Action:
Implement automated expiry alerts, prioritize
near-expiry inventory, and prevent claims on
already expired food items.
""")

st.divider()


# ============================================
# STRATEGIC RECOMMENDATIONS
# ============================================

st.subheader("📌 Strategic Recommendations")

col1, col2 = st.columns(2)

with col1:

    st.info("""
### Recommendation 1

**Improve Claim Completion Rates**

Focus on reducing cancellation rates through
better communication between providers and
receivers and faster claim processing.
""")

    st.info("""
### Recommendation 2

**Increase Breakfast Inventory**

Breakfast demand consistently exceeds supply.

Target providers with breakfast-focused donation
campaigns to improve fulfillment rates.
""")

with col2:

    st.info("""
### Recommendation 3

**Expand Restaurant Partnerships**

Restaurants contribute the largest quantity
of food and represent the highest-impact
donor segment.

Develop retention and recognition programs
for top-performing providers.
""")

    st.info("""
### Recommendation 4

**Implement Expiry Monitoring**

Introduce automated alerts for food nearing
expiry to improve redistribution efficiency
and reduce waste.
""")

st.divider()

# ============================================
# SUPPORTING VISUALS
# ============================================

st.subheader("📊 Supporting Visuals")

col1, col2 = st.columns(2)

# --------------------------------------------
# Claim Status Distribution
# --------------------------------------------

with col1:

    st.markdown("### Claim Status Distribution")

    status_counts = (
        claims["Status"]
        .value_counts()
        .reset_index()
    )

    status_counts.columns = [
        "Status",
        "Count"
    ]

    fig, ax = plt.subplots(
        figsize=(7, 4)
    )

    sns.barplot(
        data=status_counts,
        x="Status",
        y="Count",
        hue="Status",
        palette="Oranges",
        legend=False,
        ax=ax
    )

    ax.set_xlabel("Claim Status")
    ax.set_ylabel("Number of Claims")

    for container in ax.containers:
        ax.bar_label(container)

    plt.tight_layout()

    st.pyplot(fig)

    plt.close()


# --------------------------------------------
# Claims by Meal Type
# --------------------------------------------

with col2:

    st.markdown("### Claims by Meal Type")

    meal_claims = (
        claims_analysis["Meal_Type"]
        .value_counts()
        .reset_index()
    )

    meal_claims.columns = [
        "Meal_Type",
        "Claims"
    ]

    fig, ax = plt.subplots(
        figsize=(7, 4)
    )

    sns.barplot(
        data=meal_claims,
        x="Meal_Type",
        y="Claims",
        hue="Meal_Type",
        palette="YlOrBr",
        legend=False,
        ax=ax
    )

    ax.set_xlabel("Meal Type")
    ax.set_ylabel("Claims")

    for container in ax.containers:
        ax.bar_label(container)

    plt.tight_layout()

    st.pyplot(fig)

    plt.close()

st.divider()


# ============================================
# EXECUTIVE SUMMARY
# ============================================

st.subheader("📋 Executive Summary")

st.markdown("""
### Key Takeaways

**Food Supply**
- The platform contains **25,794 food units** available for redistribution.
- Food availability is relatively balanced across Vegetarian, Vegan, and Non-Vegetarian categories.
- Restaurants are the largest contributors, supplying **6,923 food units**.

**Food Demand**
- Breakfast is the most requested meal category with **278 claims**.
- Rice is the most frequently claimed food item.
- Receiver activity is broadly distributed, with no dominant beneficiary.

**Operational Performance**
- Only **33.9%** of claims were completed successfully.
- Expiry management remains an operational challenge.
- A meaningful portion of claims occur close to expiry deadlines.

**Platform Health**
- Supply and demand are both active and well-distributed.
- The biggest opportunity lies in improving claim completion and reducing food waste caused by late claims.
""")

st.divider()


# ============================================
# PROJECT CONCLUSION
# ============================================

st.subheader("🎯 Project Conclusion")

st.info("""
The Local Food Wastage Management System project
demonstrates how data analytics can support food
redistribution efforts by connecting providers and
receivers through a centralized platform.

Using PostgreSQL, SQL, Python, Pandas,
Matplotlib, Seaborn, and Streamlit, the project
identified supply trends, demand patterns,
operational bottlenecks, and opportunities to
improve food recovery efficiency.

Key outcomes include:

• Identification of high-performing provider groups
• Analysis of receiver engagement patterns
• Measurement of claim completion performance
• Detection of supply-demand imbalances
• Monitoring of expiry-related operational risks

The dashboard provides a foundation for data-driven
decision-making that can help reduce food waste and
improve food accessibility.
""")

st.divider()


# ============================================
# DASHBOARD FOOTER
# ============================================

st.success(
    "✅ Dashboard Complete | PostgreSQL + SQL + Python + Streamlit + Business Analytics"
)