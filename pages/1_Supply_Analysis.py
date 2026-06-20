# ============================================
# PAGE 1: SUPPLY ANALYSIS
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
    page_title="Supply Analysis",
    page_icon="📦",
    layout="wide"
)

# ============================================
# CUSTOM CSS
# ============================================

st.markdown("""
<style>

/* Main App Background */
.stApp{
    background-color:#F8FAFC;
}

/* Sidebar */
[data-testid="stSidebar"]{
    background: linear-gradient(
        180deg,
        #1E3A8A,
        #2563EB
    ) !important;
}

/* Sidebar Text */
[data-testid="stSidebar"] *{
    color:white !important;
}

/* Sidebar Navigation */
[data-testid="stSidebarNav"]{
    background: transparent !important;
}

/* Selected Page */
[data-testid="stSidebarNav"] li[data-selected="true"]{
    background: rgba(255,255,255,0.15);
    border-radius:12px;
}

/* Hover Effect */
[data-testid="stSidebarNav"] li:hover{
    background: rgba(255,255,255,0.10);
    border-radius:12px;
}

/* KPI Cards */
.metric-card{
    background:white;
    padding:25px;
    border-radius:18px;
    text-align:center;
    box-shadow:0px 8px 20px rgba(0,0,0,0.08);
    border-top:5px solid #2563EB;
}

/* Chart Containers */
.chart-card{
    background:white;
    padding:20px;
    border-radius:18px;
    box-shadow:0px 8px 20px rgba(0,0,0,0.08);
    margin-bottom:20px;
}

/* Hero Banner */
.hero-card{
    background:linear-gradient(
        135deg,
        #1E3A8A,
        #2563EB
    );
    padding:30px;
    border-radius:20px;
    color:white;
}

/* Insight Cards */
.insight-card{
    background:#DBEAFE;
    padding:20px;
    border-radius:15px;
    border-left:5px solid #2563EB;
}

/* Recommendation Cards */
.recommendation-card{
    background:#FEF3C7;
    padding:20px;
    border-radius:15px;
    border-left:5px solid #F59E0B;
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
def load_supply_data():

    engine = get_engine()

    food_listings = pd.read_sql(
        "SELECT * FROM food_listings",
        engine
    )

    providers = pd.read_sql(
        "SELECT * FROM providers",
        engine
    )

    return food_listings, providers


food_listings, providers = load_supply_data()
filtered_food = food_listings.copy()

# ============================================
# HERO SECTION
# ============================================

st.markdown("""
<div style="
background:linear-gradient(
135deg,
#1E3A8A,
#2563EB
);
padding:30px;
border-radius:20px;
color:white;
">

<h1>📦 Supply Analysis</h1>

<p style="font-size:18px;">
Analyze food availability, provider
contributions and inventory trends
across the platform.
</p>

</div>
""",
unsafe_allow_html=True)

st.write("")

# ============================================
# KPI CALCULATIONS
# ============================================

total_listings = len(filtered_food)

total_quantity = (
    filtered_food["quantity"]
    .sum()
)

provider_types = (
    filtered_food["provider_type"]
    .nunique()
)

# ============================================
# KPI FUNCTION
# ============================================

def kpi_card(title, value, emoji):

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
# KPI ROW
# ============================================

col1, col2, col3 = st.columns(3)

with col1:
    kpi_card(
        "Food Listings",
        f"{total_listings:,}",
        "🍱"
    )

with col2:
    kpi_card(
        "Total Quantity",
        f"{total_quantity:,}",
        "📦"
    )

with col3:
    kpi_card(
        "Provider Types",
        f"{provider_types}",
        "🏢"
    )

st.write("")
st.divider()

# ============================================
# SUPPLY OVERVIEW
# ============================================

st.markdown("## 📊 Supply Overview")

col1, col2 = st.columns([2,1])

with col1:

    st.info(
        """
        This page analyzes food inventory,
        provider participation, food categories
        and supply distribution across the platform.
        """
    )

with col2:

    st.success(
        f"Current Inventory: {total_quantity:,} units"
    )

st.divider()

# ============================================
# FOOD INVENTORY ANALYSIS
# ============================================

st.markdown(
    "## 🍱 Food Inventory Analysis"
)

col1, col2 = st.columns(2)

# ============================================
# FOOD TYPE DISTRIBUTION
# ============================================

with col1:

    with st.container():

        st.markdown(
            "### 🍲 Food Type Distribution"
        )

        food_type_counts = (
            filtered_food["food_type"]
            .value_counts()
            .reset_index()
        )

        food_type_counts.columns = [
            "Food Type",
            "Count"
        ]

        fig, ax = plt.subplots(
            figsize=(8,5)
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

        ax.set_xlabel("")
        ax.set_ylabel("Count")

        for container in ax.containers:
            ax.bar_label(container)

        sns.despine()

        st.pyplot(fig)

        plt.close()

        st.caption(
            "Distribution of food listings across food categories."
        )

# ============================================
# MEAL TYPE DISTRIBUTION
# ============================================

with col2:

    with st.container():

        st.markdown(
            "### 🍽️ Meal Type Distribution"
        )

        meal_type_counts = (
            filtered_food["meal_type"]
            .value_counts()
            .reset_index()
        )

        meal_type_counts.columns = [
            "Meal Type",
            "Count"
        ]

        fig, ax = plt.subplots(
            figsize=(8,5)
        )

        sns.barplot(
            data=meal_type_counts,
            x="Meal Type",
            y="Count",
            hue="Meal Type",
            palette="Purples_r",
            legend=False,
            ax=ax
        )

        ax.set_xlabel("")
        ax.set_ylabel("Count")

        for container in ax.containers:
            ax.bar_label(container)

        sns.despine()

        st.pyplot(fig)

        plt.close()

        st.caption(
            "Availability of food inventory across meal categories."
        )

st.divider()

# ============================================
# PROVIDER PERFORMANCE ANALYSIS
# ============================================

st.markdown(
    "## 🏢 Provider Performance Analysis"
)

col1, col2 = st.columns(2)

# ============================================
# TOP PROVIDERS
# ============================================

with col1:

    with st.container():

        st.markdown(
            "### 🏆 Top 10 Providers by Quantity"
        )

        provider_quantity = (
            filtered_food
            .groupby("provider_id")["quantity"]
            .sum()
            .reset_index()
        )

        provider_quantity = provider_quantity.merge(
            providers[
                ["provider_id", "name"]
            ],
            on="provider_id",
            how="left"
        )

        top_10 = (
            provider_quantity
            .nlargest(
                10,
                "quantity"
            )
            .sort_values(
                "quantity"
            )
        )

        fig, ax = plt.subplots(
            figsize=(9,5)
        )

        sns.barplot(
            data=top_10,
            x="quantity",
            y="name",
            hue="name",
            palette="crest",
            legend=False,
            ax=ax
        )

        ax.set_xlabel(
            "Total Quantity"
        )

        ax.set_ylabel("")

        for container in ax.containers:
            ax.bar_label(container)

        sns.despine()

        st.pyplot(fig)

        plt.close()

        st.caption(
            "Top contributing providers based on food quantity donated."
        )

# ============================================
# PROVIDER CONTRIBUTION
# ============================================

with col2:

    with st.container():

        st.markdown(
            "### 📦 Provider Type Contribution"
        )

        contribution = (
            filtered_food
            .groupby(
                "provider_type"
            )["quantity"]
            .sum()
            .reset_index()
            .sort_values(
                "quantity",
                ascending=False
            )
        )

        fig, ax = plt.subplots(
            figsize=(8,5)
        )

        sns.barplot(
            data=contribution,
            x="provider_type",
            y="quantity",
            hue="provider_type",
            palette="Blues_r",
            legend=False,
            ax=ax
        )

        ax.set_xlabel("")
        ax.set_ylabel(
            "Quantity"
        )

        for container in ax.containers:
            ax.bar_label(container)

        sns.despine()

        st.pyplot(fig)

        plt.close()

        st.caption(
            "Total food quantity contributed by each provider category."
        )

st.divider()


# ============================================
# EXECUTIVE INSIGHTS
# ============================================

st.markdown(
    "## 💡 Executive Insights"
)

col1, col2 = st.columns(2)

# ============================================
# INSIGHT 1
# ============================================

with col1:

    st.info(
        """
        ### 🍱 Balanced Food Availability

        Food inventory is distributed across
        Vegetarian, Vegan and Non-Vegetarian
        categories, ensuring diverse food
        options for receivers.

        This balanced distribution improves
        accessibility and supports a wider
        range of dietary preferences.
        """
    )

# ============================================
# INSIGHT 2
# ============================================

with col2:

    st.info(
        """
        ### 🍽️ Consistent Meal Coverage

        Food listings are spread across
        Breakfast, Lunch, Dinner and Snacks.

        This indicates a healthy supply
        pipeline throughout the day and
        increases redistribution opportunities.
        """
    )

st.write("")

col1, col2 = st.columns(2)

# ============================================
# INSIGHT 3
# ============================================

with col1:

    st.success(
        """
        ### 🏢 Strong Provider Network

        Provider participation is diversified
        across Restaurants, Supermarkets,
        Grocery Stores and Catering Services.

        This reduces dependency on a single
        contributor segment and improves
        supply stability.
        """
    )

# ============================================
# INSIGHT 4
# ============================================

with col2:

    st.success(
        """
        ### 🏆 High-Impact Contributors

        A small group of providers contributes
        a significant share of total food
        quantity.

        Maintaining engagement with these
        providers is critical for sustaining
        platform supply.
        """
    )

st.divider()

# ============================================
# BUSINESS RECOMMENDATIONS
# ============================================

st.markdown(
    "## 🚀 Business Recommendations"
)

st.warning(
    """
    **Recommendation 1**

    Strengthen partnerships with top-performing
    providers through recognition programs,
    incentives and dedicated engagement
    initiatives.
    """
)

st.warning(
    """
    **Recommendation 2**

    Focus on increasing food listings in
    high-demand meal categories to improve
    redistribution effectiveness.
    """
)

st.warning(
    """
    **Recommendation 3**

    Expand provider onboarding efforts in
    underrepresented categories to maintain
    a balanced and resilient supply network.
    """
)

st.warning(
    """
    **Recommendation 4**

    Monitor inventory trends regularly and
    use data-driven forecasting to anticipate
    demand fluctuations.
    """
)

st.divider()

# ============================================
# PAGE SUMMARY
# ============================================

st.markdown(
    """
    ### 📊 Supply Analysis Summary

    This dashboard provides visibility into
    food inventory, provider participation,
    category distribution and supply-side
    performance metrics.

    The analysis highlights a balanced supply
    ecosystem supported by a diversified
    provider network and multiple food
    categories.
    """
)