# ============================================
# PAGE 5: BUSINESS INSIGHTS
# ============================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sqlalchemy import create_engine

# ============================================
# PAGE CONFIG
# ============================================

st.set_page_config(
    page_title="Business Insights",
    page_icon="📈",
    layout="wide"
)

# ============================================
# CUSTOM CSS
# ============================================

st.markdown("""
<style>

.stApp{
    background-color:#F8FAFC;
}

/* Green Executive Theme */

[data-testid="stSidebar"]{
    background:linear-gradient(
        180deg,
        #14532D,
        #16A34A
    ) !important;
}

[data-testid="stSidebar"] *{
    color:white !important;
}

.hero-card{
    background:linear-gradient(
        135deg,
        #14532D,
        #16A34A
    );
    padding:30px;
    border-radius:20px;
    color:white;
}

.metric-card{
    background:white;
    padding:25px;
    border-radius:18px;
    text-align:center;
    box-shadow:0px 8px 20px rgba(0,0,0,0.08);
    border-top:5px solid #16A34A;
}

.insight-card{
    background:#F0FDF4;
    padding:20px;
    border-radius:15px;
    border-left:5px solid #16A34A;
    margin-bottom:15px;
}

.footer{
    text-align:center;
    color:gray;
    padding:20px;
}

</style>
""", unsafe_allow_html=True)

# ============================================
# DATABASE CONNECTION
# ============================================

@st.cache_resource
def get_engine():

    DB_HOST = st.secrets["DB_HOST"]
    DB_PORT = st.secrets["DB_PORT"]
    DB_NAME = st.secrets["DB_NAME"]
    DB_USER = st.secrets["DB_USER"]
    DB_PASSWORD = st.secrets["DB_PASSWORD"]

    connection_string = (
        f"postgresql+psycopg2://"
        f"{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        f"?sslmode=require"
    )

    return create_engine(
        connection_string
    )


# ============================================
# LOAD DATA
# ============================================

@st.cache_data
def load_data():

    engine = get_engine()

    providers = pd.read_sql(
        """
        SELECT *
        FROM providers
        """,
        engine
    )

    receivers = pd.read_sql(
        """
        SELECT *
        FROM receivers
        """,
        engine
    )

    food_listings = pd.read_sql(
        """
        SELECT *
        FROM food_listings
        """,
        engine
    )

    claims = pd.read_sql(
        """
        SELECT *
        FROM claims
        """,
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
# STANDARDIZE COLUMN NAMES
# ============================================

providers.columns = (
    providers.columns
    .str.lower()
)

receivers.columns = (
    receivers.columns
    .str.lower()
)

food_listings.columns = (
    food_listings.columns
    .str.lower()
)

claims.columns = (
    claims.columns
    .str.lower()
)

# ============================================
# DATA PREPARATION
# ============================================

providers.columns = providers.columns.str.lower()
receivers.columns = receivers.columns.str.lower()
food_listings.columns = food_listings.columns.str.lower()
claims.columns = claims.columns.str.lower()

claims_analysis = (
    claims
    .merge(
        food_listings,
        on="food_id",
        how="left"
    )
)

completed_claims = (
    claims["status"]
    .eq("Completed")
    .sum()
)

completion_rate = (
    completed_claims
    /
    len(claims)
) * 100

total_food_available = (
    food_listings["quantity"]
    .sum()
)

top_meal_type = (
    claims_analysis["meal_type"]
    .value_counts()
    .idxmax()
)

food_listings["expiry_date"] = pd.to_datetime(
    food_listings["expiry_date"]
)

claims["timestamp"] = pd.to_datetime(
    claims["timestamp"]
)

expiry_analysis = (
    claims
    .merge(
        food_listings[
            ["food_id","expiry_date"]
        ],
        on="food_id",
        how="left"
    )
)

expiry_analysis["days_until_expiry"] = (
    expiry_analysis["expiry_date"]
    -
    expiry_analysis["timestamp"]
).dt.days

avg_days_until_expiry = (
    expiry_analysis[
        "days_until_expiry"
    ].mean()
)
# ============================================
# HERO SECTION
# ============================================

st.markdown("""
<div class="hero-card">

<h1>📈 Business Insights & Strategic Recommendations</h1>

<p style="font-size:18px;">
Executive dashboard summarizing food supply,
receiver demand, operational performance,
and platform-wide business opportunities.
</p>

</div>
""", unsafe_allow_html=True)

st.write("")

# ============================================
# KPI CARD FUNCTION
# ============================================

def metric_card(
    title,
    value,
    emoji
):

    st.markdown(
        f"""
        <div class="metric-card">

        <h1>{emoji}</h1>

        <h2>{value}</h2>

        <p>{title}</p>

        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================
# KPI SECTION
# ============================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    metric_card(
        "Food Available",
        f"{int(total_food_available):,}",
        "🍱"
    )

with col2:

    metric_card(
        "Completion Rate",
        f"{completion_rate:.1f}%",
        "✅"
    )

with col3:

    metric_card(
        "Top Meal Type",
        top_meal_type,
        "🥗"
    )

with col4:

    metric_card(
        "Avg Days To Expiry",
        f"{avg_days_until_expiry:.1f}",
        "📅"
    )

st.write("")

st.divider()

# ============================================
# EXECUTIVE OVERVIEW
# ============================================

st.markdown(
    "## 📊 Executive Overview"
)

col1, col2 = st.columns(
    [2,1]
)

with col1:

    st.info(
        """
        This page consolidates findings from:

        • Supply Analysis

        • Demand Analysis

        • Operations Analysis

        • SQL Analytics

        into a single executive summary for
        business decision-making.
        """
    )

with col2:

    st.success(
        f"""
        Platform Health Score

        Completion Rate:
        {completion_rate:.1f}%
        """
    )

st.divider()

# ============================================
# BUSINESS SNAPSHOT
# ============================================

st.markdown(
    "## 🚀 Business Snapshot"
)

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Providers",
        f"{len(providers):,}"
    )

with col2:

    st.metric(
        "Receivers",
        f"{len(receivers):,}"
    )

with col3:

    st.metric(
        "Food Listings",
        f"{len(food_listings):,}"
    )

with col4:

    st.metric(
        "Claims",
        f"{len(claims):,}"
    )

st.divider()

# ============================================
# TOP BUSINESS FINDINGS
# ============================================

st.markdown(
    "## 🏆 Executive Business Findings"
)

st.markdown(
    """
    <div class="insight-card">

    <h4>1️⃣ Claim Completion Performance</h4>

    <p>

    Only <b>33.9%</b> of claims were successfully completed.

    This indicates substantial operational inefficiencies
    between food availability and successful redistribution.

    </p>

    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="insight-card">

    <h4>2️⃣ Breakfast Demand Exceeds Supply</h4>

    <p>

    Breakfast generated the highest number of claims
    across all meal categories.

    Demand is growing faster than available inventory,
    creating a supply-demand imbalance.

    </p>

    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="insight-card">

    <h4>3️⃣ Restaurants Drive Food Supply</h4>

    <p>

    Restaurants contribute the largest share of food
    donations and remain the most valuable provider
    segment on the platform.

    </p>

    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="insight-card">

    <h4>4️⃣ Food Distribution Is Well Balanced</h4>

    <p>

    Receiver activity is broadly distributed across
    charities, NGOs and community organizations.

    No single receiver dominates claim activity.

    </p>

    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="insight-card">

    <h4>5️⃣ Expiry Risk Requires Attention</h4>

    <p>

    Several claims occur very close to food expiry
    deadlines, creating operational and compliance
    risks.

    Automated expiry monitoring should be prioritized.

    </p>

    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

# ============================================
# STRATEGIC RECOMMENDATIONS
# ============================================

st.markdown(
    "## 📌 Strategic Recommendations"
)

col1, col2 = st.columns(2)

with col1:

    st.markdown(
        """
        <div class="insight-card">

        <h4>🎯 Improve Claim Completion Rates</h4>

        <p>

        Reduce cancellation rates by improving
        communication between providers and
        receivers.

        Introduce claim reminders and SLA-based
        claim resolution tracking.

        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="insight-card">

        <h4>🥞 Increase Breakfast Inventory</h4>

        <p>

        Breakfast demand consistently exceeds
        available inventory.

        Launch provider campaigns focused on
        breakfast donations to improve
        fulfillment rates.

        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

with col2:

    st.markdown(
        """
        <div class="insight-card">

        <h4>🏢 Strengthen Restaurant Partnerships</h4>

        <p>

        Restaurants contribute the largest
        quantity of food donations.

        Develop recognition programs and
        long-term partnerships to increase
        contribution volume.

        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="insight-card">

        <h4>⏰ Implement Expiry Monitoring</h4>

        <p>

        Introduce automated alerts for food
        approaching expiry.

        Prioritize near-expiry inventory to
        maximize successful redistribution.

        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()

# ============================================
# SUPPORTING VISUALS
# ============================================

st.markdown(
    "## 📊 Supporting Visual Analytics"
)

col1, col2 = st.columns(2)

# ============================================
# CLAIM STATUS DISTRIBUTION
# ============================================

with col1:

    st.markdown(
        "### Claim Status Distribution"
    )

    status_counts = (
        claims["status"]
        .value_counts()
        .reset_index()
    )

    status_counts.columns = [
        "Status",
        "Count"
    ]

    fig, ax = plt.subplots(
        figsize=(7,5)
    )

    sns.barplot(
        data=status_counts,
        x="Status",
        y="Count",
        palette="Greens",
        ax=ax
    )

    for container in ax.containers:
        ax.bar_label(
            container,
            padding=3
        )

    ax.set_xlabel(
        "Claim Status"
    )

    ax.set_ylabel(
        "Number of Claims"
    )

    ax.set_title(
        "Claim Completion Overview",
        fontsize=13,
        fontweight="bold"
    )

    sns.despine()

    st.pyplot(fig)

    plt.close()

# ============================================
# CLAIMS BY MEAL TYPE
# ============================================

with col2:

    st.markdown(
        "### Claims by Meal Type"
    )

    meal_claims = (
        claims_analysis["meal_type"]
        .value_counts()
        .reset_index()
    )

    meal_claims.columns = [
        "Meal Type",
        "Claims"
    ]

    fig, ax = plt.subplots(
        figsize=(7,5)
    )

    sns.barplot(
        data=meal_claims,
        x="Meal Type",
        y="Claims",
        palette="YlGn",
        ax=ax
    )

    for container in ax.containers:
        ax.bar_label(
            container,
            padding=3
        )

    ax.set_xlabel(
        "Meal Type"
    )

    ax.set_ylabel(
        "Claims"
    )

    ax.set_title(
        "Demand by Meal Category",
        fontsize=13,
        fontweight="bold"
    )

    sns.despine()

    st.pyplot(fig)

    plt.close()

st.divider()

# ============================================
# EXECUTIVE PERFORMANCE DASHBOARD
# ============================================

st.markdown(
    "## 🚀 Executive Performance Dashboard"
)

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Completion Rate",
        f"{completion_rate:.1f}%"
    )

with col2:

    st.metric(
        "Food Listings",
        f"{len(food_listings):,}"
    )

with col3:

    st.metric(
        "Claims Processed",
        f"{len(claims):,}"
    )

st.divider()

# ============================================
# EXECUTIVE SUMMARY
# ============================================

st.markdown(
    "## 📋 Executive Summary"
)

st.markdown(
    """
    <div class="insight-card">

    <h4>Platform Performance Overview</h4>

    <p>

    The Local Food Wastage Management System
    successfully connects food providers and
    receivers through a centralized food
    redistribution platform.

    Analysis indicates healthy participation
    from both supply and demand stakeholders,
    with strong provider diversity and balanced
    receiver engagement.

    </p>

    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="insight-card">

    <h4>Key Business Outcomes</h4>

    <p>

    • Strong provider participation across all categories

    • Restaurants contribute the highest food volume

    • Breakfast demand exceeds available inventory

    • Food distribution remains equitable across receivers

    • Completion rates require operational improvement

    </p>

    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="insight-card">

    <h4>Operational Priorities</h4>

    <p>

    The greatest opportunities for improvement
    lie in increasing claim completion rates,
    reducing expiry-related losses, and
    improving redistribution efficiency.

    </p>

    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

# ============================================
# PROJECT CONCLUSION
# ============================================

st.markdown(
    "## 🎯 Project Conclusion"
)

st.success(
    """
    The Local Food Wastage Management System
    demonstrates how data analytics can be
    leveraged to reduce food waste and improve
    food accessibility.

    Technologies Used:

    ✅ PostgreSQL

    ✅ SQL

    ✅ Python

    ✅ Pandas

    ✅ Matplotlib

    ✅ Seaborn

    ✅ Streamlit

    Key Deliverables:

    ✅ Exploratory Data Analysis (EDA)

    ✅ SQL Business Analytics

    ✅ Supply Analysis Dashboard

    ✅ Demand Analysis Dashboard

    ✅ Operations Analysis Dashboard

    ✅ Executive Business Insights Dashboard

    This project provides a scalable foundation
    for data-driven food redistribution and
    operational decision-making.
    """
)

st.divider()

# ============================================
# PROJECT ACHIEVEMENTS
# ============================================

st.markdown(
    "## 🏆 Project Achievements"
)

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "EDA Visualizations",
        "9"
    )

with col2:

    st.metric(
        "SQL Queries",
        "13"
    )

with col3:

    st.metric(
        "Dashboard Pages",
        "5"
    )

st.divider()

# ============================================
# FINAL RECOMMENDATION
# ============================================

st.markdown(
    "## 🚀 Final Recommendation"
)

st.info(
    """
    Focus future platform improvements on:

    • Increasing claim completion rates

    • Expanding breakfast inventory

    • Strengthening restaurant partnerships

    • Implementing real-time expiry monitoring

    • Enhancing redistribution efficiency

    These initiatives will maximize food recovery,
    reduce waste, and improve overall platform impact.
    """
)

st.divider()

# ============================================
# FOOTER
# ============================================

st.markdown(
    """
    <div class="footer">

    <h4>🍱 Local Food Wastage Management System</h4>

    Built by <b>Raju Kumar S</b><br>

    Data Analyst | SQL | Power BI | Python | Streamlit

    <br><br>

    © 2026 | Business Analytics Portfolio Project

    </div>
    """,
    unsafe_allow_html=True
)