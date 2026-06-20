# ============================================
# LOCAL FOOD WASTAGE MANAGEMENT SYSTEM
# EXECUTIVE DASHBOARD
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
    page_title="Local Food Wastage Management System",
    page_icon="🍱",
    layout="wide"
)

# ============================================
# CUSTOM CSS
# ============================================

st.markdown("""
<style>

.main {
    background-color: #F8FAFC;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #1E3A8A,
        #2563EB
    );
}

section[data-testid="stSidebar"] * {
    color: white;
}

.kpi-card {
    background:white;
    padding:25px;
    border-radius:18px;
    box-shadow:0px 8px 20px rgba(0,0,0,0.08);
    text-align:center;
    border-top:5px solid #2563EB;
}

.hero-card {
    background: linear-gradient(
        135deg,
        #1E3A8A,
        #2563EB
    );
    padding:30px;
    border-radius:20px;
    color:white;
}

.footer {
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
# HERO SECTION
# ============================================

st.markdown("""
<div class="hero-card">

<h1>🍱 Local Food Wastage Management System</h1>

<p style="font-size:18px;">
Transforming food redistribution through
data-driven analytics and business intelligence
</p>

</div>
""", unsafe_allow_html=True)

st.write("")

# ============================================
# QUICK NAVIGATION
# ============================================

st.markdown("## 🚀 Quick Navigation")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.page_link(
        "pages/1_Supply_Analysis.py",
        label="📦 Supply"
    )

with col2:
    st.page_link(
        "pages/2_Demand_Analysis.py",
        label="📈 Demand"
    )

with col3:
    st.page_link(
        "pages/3_Operations_Analysis.py",
        label="⚙️ Operations"
    )

with col4:
    st.page_link(
        "pages/4_SQL_Explorer.py",
        label="🗄️ SQL Explorer"
    )

with col5:
    st.page_link(
        "pages/5_Business_Insights.py",
        label="💡 Insights"
    )

st.divider()

# ============================================
# KPI CALCULATIONS
# ============================================

total_providers = len(providers)
total_receivers = len(receivers)
total_food_listings = len(food_listings)

completed_claims = (
    claims["status"] == "Completed"
).sum()

completion_rate = (
    completed_claims / len(claims)
) * 100

# ============================================
# KPI FUNCTION
# ============================================

def kpi_card(title, value, emoji):

    st.markdown(
        f"""
        <div class="kpi-card">
            <h1>{emoji}</h1>
            <h2>{value}</h2>
            <p>{title}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================
# KPI ROW
# ============================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    kpi_card(
        "Providers",
        f"{total_providers:,}",
        "🏢"
    )

with col2:
    kpi_card(
        "Receivers",
        f"{total_receivers:,}",
        "🤝"
    )

with col3:
    kpi_card(
        "Food Listings",
        f"{total_food_listings:,}",
        "🍱"
    )

with col4:
    kpi_card(
        "Completion Rate",
        f"{completion_rate:.1f}%",
        "✅"
    )

st.divider()

# ============================================
# PLATFORM OVERVIEW
# ============================================

st.markdown("## 📊 Platform Overview")

col1, col2 = st.columns([2,1])

with col1:
    st.info("""
    This platform connects food providers,
    NGOs, charities and receivers to reduce
    food wastage and improve redistribution
    efficiency.
    """)

with col2:
    st.success(
        f"Current Completion Rate: {completion_rate:.1f}%"
    )

st.divider()

# ============================================
# EXECUTIVE DASHBOARD CHARTS
# ============================================

st.markdown("## 📈 Executive Dashboard")

col1, col2 = st.columns(2)

# ============================================
# CLAIM STATUS DISTRIBUTION
# ============================================

with col1:

    st.markdown("### 📋 Claims by Status")

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
        hue="Status",
        palette="Blues_r",
        legend=False,
        ax=ax
    )

    for container in ax.containers:
        ax.bar_label(container)

    sns.despine()

    st.pyplot(fig)

    plt.close()


# ============================================
# FOOD TYPE DISTRIBUTION
# ============================================

with col2:

    st.markdown("### 🍱 Listings by Food Type")

    food_type_counts = (
        food_listings["food_type"]
        .value_counts()
        .reset_index()
    )

    food_type_counts.columns = [
        "Food Type",
        "Count"
    ]

    fig, ax = plt.subplots(
        figsize=(7,5)
    )

    sns.barplot(
        data=food_type_counts,
        x="Food Type",
        y="Count",
        hue="Food Type",
        palette="Oranges_r",
        legend=False,
        ax=ax
    )

    for container in ax.containers:
        ax.bar_label(container)

    sns.despine()

    st.pyplot(fig)

    plt.close()


st.write("")

col1, col2 = st.columns(2)

# ============================================
# CLAIMS BY MEAL TYPE
# ============================================

with col1:

    st.markdown("### 🍽️ Claims by Meal Type")

    meal_claims = claims.merge(
        food_listings[
            ["food_id", "meal_type"]
        ],
        on="food_id",
        how="left"
    )

    meal_counts = (
        meal_claims["meal_type"]
        .value_counts()
        .reset_index()
    )

    meal_counts.columns = [
        "Meal Type",
        "Claims"
    ]

    fig, ax = plt.subplots(
        figsize=(7,5)
    )

    sns.barplot(
        data=meal_counts,
        x="Meal Type",
        y="Claims",
        hue="Meal Type",
        palette="Purples_r",
        legend=False,
        ax=ax
    )

    for container in ax.containers:
        ax.bar_label(container)

    sns.despine()

    st.pyplot(fig)

    plt.close()


# ============================================
# PROVIDER CONTRIBUTION
# ============================================

with col2:

    st.markdown("### 🏢 Provider Contribution")

    contribution = (
        food_listings
        .groupby("provider_type")["quantity"]
        .sum()
        .reset_index()
        .sort_values(
            "quantity",
            ascending=False
        )
    )

    fig, ax = plt.subplots(
        figsize=(7,5)
    )

    sns.barplot(
        data=contribution,
        x="provider_type",
        y="quantity",
        hue="provider_type",
        palette="crest",
        legend=False,
        ax=ax
    )

    for container in ax.containers:
        ax.bar_label(container)

    sns.despine()

    st.pyplot(fig)

    plt.close()

st.divider()

# ============================================
# KEY TAKEAWAYS
# ============================================

st.markdown("## 💡 Executive Summary")

st.success(
    f"""
    • {completion_rate:.1f}% of claims have been completed successfully.

    • The platform currently manages {total_food_listings:,} food listings.

    • Provider participation remains diversified across multiple provider categories.

    • Meal demand is distributed across Breakfast, Lunch, Dinner and Snacks.

    • Continued monitoring of pending and cancelled claims can improve redistribution efficiency.
    """
)