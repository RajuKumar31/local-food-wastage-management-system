# ============================================
# PAGE 2: DEMAND ANALYSIS
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
    page_title="Demand Analysis",
    page_icon="🤝",
    layout="wide"
)

# ============================================
# CUSTOM CSS
# ============================================

st.markdown("""
<style>

/* Main App */

.stApp{
    background-color:#F8FAFC;
}

/* Sidebar */

[data-testid="stSidebar"]{
    background:linear-gradient(
        180deg,
        #1E3A8A,
        #2563EB
    ) !important;
}

[data-testid="stSidebar"] *{
    color:white !important;
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

/* Hero */

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

/* Charts */

.chart-card{
    background:white;
    padding:20px;
    border-radius:18px;
    box-shadow:0px 8px 20px rgba(0,0,0,0.08);
    margin-bottom:20px;
}

/* Insights */

.insight-card{
    background:#DBEAFE;
    padding:20px;
    border-radius:15px;
    border-left:5px solid #2563EB;
}

/* Recommendations */

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
        f"@{DB_HOST}:{DB_PORT}"
        f"/{DB_NAME}"
        f"?sslmode=require"
    )

    return create_engine(
        connection_string
    )


# ============================================
# LOAD DATA
# ============================================

@st.cache_data
def load_demand_data():

    engine = get_engine()

    claims = pd.read_sql(
        "SELECT * FROM claims",
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

    return (
        claims,
        receivers,
        food_listings
    )


claims, receivers, food_listings = (
    load_demand_data()
)


# ============================================
# CREATE ANALYSIS DATASET
# ============================================

claims_analysis = (

    claims

    .merge(
        receivers,
        on="receiver_id",
        how="left"
    )

    .merge(
        food_listings,
        on="food_id",
        how="left"
    )

)


# ============================================
# DATA VALIDATION
# ============================================

claims_analysis = (
    claims_analysis
    .dropna(
        subset=[
            "status",
            "type",
            "meal_type"
        ]
    )
)

claims_analysis.reset_index(
    drop=True,
    inplace=True
)

# ============================================
# HERO SECTION
# ============================================

st.markdown("""
<div class="hero-card">

<h1>🤝 Demand Analysis</h1>

<p style="font-size:18px;">
Understand receiver behavior, food demand trends,
claim performance and beneficiary participation.
</p>

</div>
""", unsafe_allow_html=True)

st.write("")

# ============================================
# SIDEBAR FILTERS
# ============================================

st.sidebar.header("🎯 Demand Filters")

all_receiver_types = sorted(
    claims_analysis["type"]
    .dropna()
    .unique()
)

selected_receiver_types = (
    st.sidebar.multiselect(
        "Receiver Type",
        options=all_receiver_types,
        default=all_receiver_types
    )
)

all_statuses = sorted(
    claims_analysis["status"]
    .dropna()
    .unique()
)

selected_statuses = (
    st.sidebar.multiselect(
        "Claim Status",
        options=all_statuses,
        default=all_statuses
    )
)

all_meal_types = sorted(
    claims_analysis["meal_type"]
    .dropna()
    .unique()
)

selected_meal_types = (
    st.sidebar.multiselect(
        "Meal Type",
        options=all_meal_types,
        default=all_meal_types
    )
)

# ============================================
# APPLY FILTERS
# ============================================

filtered_claims = claims_analysis[

    claims_analysis["type"].isin(
        selected_receiver_types
    )

    &

    claims_analysis["status"].isin(
        selected_statuses
    )

    &

    claims_analysis["meal_type"].isin(
        selected_meal_types
    )

]

# ============================================
# KPI CALCULATIONS
# ============================================

total_claims = len(
    filtered_claims
)

completed_claims = len(

    filtered_claims[

        filtered_claims["status"]
        ==
        "Completed"

    ]

)

pending_claims = len(

    filtered_claims[

        filtered_claims["status"]
        ==
        "Pending"

    ]

)

cancelled_claims = len(

    filtered_claims[

        filtered_claims["status"]
        ==
        "Cancelled"

    ]

)

completion_rate = (

    (
        completed_claims
        /
        total_claims
    ) * 100

    if total_claims > 0

    else 0

)

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
# KPI ROW
# ============================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    metric_card(
        "Total Claims",
        f"{total_claims:,}",
        "📋"
    )

with col2:

    metric_card(
        "Completed",
        f"{completed_claims:,}",
        "✅"
    )

with col3:

    metric_card(
        "Pending",
        f"{pending_claims:,}",
        "⏳"
    )

with col4:

    metric_card(
        "Cancelled",
        f"{cancelled_claims:,}",
        "❌"
    )

st.write("")

st.divider()

# ============================================
# DEMAND OVERVIEW
# ============================================

st.markdown(
    "## 📊 Demand Overview"
)

col1, col2 = st.columns(
    [2,1]
)

with col1:

    st.info(
        """
        This dashboard evaluates receiver demand,
        claim activity, beneficiary engagement and
        meal preferences across the food redistribution platform.
        """
    )

with col2:

    st.success(
        f"Completion Rate: {completion_rate:.1f}%"
    )

st.divider()

# ============================================
# DEMAND ACTIVITY ANALYSIS
# ============================================

st.markdown(
    "## 📈 Demand Activity Analysis"
)

col1, col2 = st.columns(2)

# ============================================
# CLAIM STATUS DISTRIBUTION
# ============================================

with col1:

    st.markdown(
        "### 📋 Claim Status Distribution"
    )

    status_counts = (

        filtered_claims["status"]

        .value_counts()

        .reset_index()

    )

    status_counts.columns = [
        "Status",
        "Count"
    ]

    fig, ax = plt.subplots(
        figsize=(8,5)
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

    ax.set_xlabel("")
    ax.set_ylabel("Claims")

    for container in ax.containers:
        ax.bar_label(container)

    sns.despine()

    st.pyplot(fig)

    plt.close()

    st.caption(
        "Distribution of completed, pending and cancelled claims."
    )

# ============================================
# RECEIVER TYPE DISTRIBUTION
# ============================================

with col2:

    st.markdown(
        "### 🤝 Receiver Type Distribution"
    )

    receiver_counts = (

        filtered_claims["type"]

        .value_counts()

        .reset_index()

    )

    receiver_counts.columns = [
        "Receiver Type",
        "Count"
    ]

    fig, ax = plt.subplots(
        figsize=(8,5)
    )

    sns.barplot(
        data=receiver_counts,
        x="Receiver Type",
        y="Count",
        hue="Receiver Type",
        palette="Greens_r",
        legend=False,
        ax=ax
    )

    ax.set_xlabel("")
    ax.set_ylabel("Claims")

    for container in ax.containers:
        ax.bar_label(container)

    sns.despine()

    st.pyplot(fig)

    plt.close()

    st.caption(
        "Claim activity segmented by receiver category."
    )

st.divider()

# ============================================
# BENEFICIARY ANALYSIS
# ============================================

st.markdown(
    "## 🍽️ Beneficiary Analysis"
)

col1, col2 = st.columns(2)

# ============================================
# CLAIMS BY MEAL TYPE
# ============================================

with col1:

    st.markdown(
        "### 🍱 Claims by Meal Type"
    )

    meal_claims = (

        filtered_claims["meal_type"]

        .value_counts()

        .reset_index()

    )

    meal_claims.columns = [
        "Meal Type",
        "Claims"
    ]

    fig, ax = plt.subplots(
        figsize=(8,5)
    )

    sns.barplot(
        data=meal_claims,
        x="Meal Type",
        y="Claims",
        hue="Meal Type",
        palette="YlOrBr",
        legend=False,
        ax=ax
    )

    ax.set_xlabel("")
    ax.set_ylabel("Claims")

    for container in ax.containers:
        ax.bar_label(container)

    sns.despine()

    st.pyplot(fig)

    plt.close()

    st.caption(
        "Demand distribution across meal categories."
    )

# ============================================
# TOP RECEIVERS
# ============================================

with col2:

    st.markdown(
        "### 🏆 Top 10 Receivers by Claims"
    )

    top_receivers = (

        filtered_claims

        .groupby(
            ["receiver_id", "name"]
        )["claim_id"]

        .count()

        .reset_index()

    )

    top_receivers.columns = [
        "receiver_id",
        "receiver_name",
        "claims"
    ]

    top_receivers = (

        top_receivers

        .nlargest(
            10,
            "claims"
        )

        .sort_values(
            "claims"
        )

    )

    fig, ax = plt.subplots(
        figsize=(9,5)
    )

    sns.barplot(
        data=top_receivers,
        x="claims",
        y="receiver_name",
        hue="receiver_name",
        palette="crest",
        legend=False,
        ax=ax
    )

    ax.set_xlabel(
        "Number of Claims"
    )

    ax.set_ylabel("")

    for container in ax.containers:
        ax.bar_label(container)

    sns.despine()

    st.pyplot(fig)

    plt.close()

    st.caption(
        "Most active beneficiaries based on claim activity."
    )

st.divider()

# ============================================
# DEMAND HIGHLIGHTS
# ============================================

st.markdown(
    "## 🎯 Demand Highlights"
)

col1, col2 = st.columns(2)

with col1:

    highest_meal = (
        meal_claims.iloc[0]["Meal Type"]
        if len(meal_claims) > 0
        else "N/A"
    )

    highest_meal_count = (
        meal_claims.iloc[0]["Claims"]
        if len(meal_claims) > 0
        else 0
    )

    st.info(
        f"""
        ### 🍽️ Highest Demand Meal

        **{highest_meal}**

        generated

        **{highest_meal_count:,} claims**

        making it the most requested meal category.
        """
    )

with col2:

    top_receiver = (
        top_receivers.iloc[-1]["receiver_name"]
        if len(top_receivers) > 0
        else "N/A"
    )

    top_receiver_claims = (
        top_receivers.iloc[-1]["claims"]
        if len(top_receivers) > 0
        else 0
    )

    st.success(
        f"""
        ### 🏆 Most Active Receiver

        **{top_receiver}**

        submitted

        **{top_receiver_claims:,} claims**

        during the selected period.
        """
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
        f"""
        ### 📋 Claim Completion Performance

        Out of **{total_claims:,} claims**,
        only **{completed_claims:,}** were
        successfully completed.

        Current completion rate is

        **{completion_rate:.1f}%**

        indicating room for operational
        improvement.
        """
    )

# ============================================
# INSIGHT 2
# ============================================

with col2:

    st.info(
        f"""
        ### 🍽️ Meal Demand Trends

        Demand is distributed across
        multiple meal categories.

        **{highest_meal}** currently
        represents the strongest
        demand segment with

        **{highest_meal_count:,} claims**.
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
        ### 🤝 Receiver Participation

        NGOs, Charities and Community
        Organizations represent a major
        portion of platform beneficiaries.

        This indicates strong utilization
        of redistributed food resources.
        """
    )

# ============================================
# INSIGHT 4
# ============================================

with col2:

    st.success(
        """
        ### 📊 Distributed Demand

        Claim activity is distributed
        across multiple receivers.

        The platform is not dependent
        on a single beneficiary group,
        creating a healthy demand ecosystem.
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

    Improve claim completion rates through
    automated notifications and follow-up
    reminders for pending claims.
    """
)

st.warning(
    """
    **Recommendation 2**

    Increase food supply in meal categories
    showing consistently higher demand.
    """
)

st.warning(
    """
    **Recommendation 3**

    Strengthen relationships with highly
    active receivers to improve redistribution
    efficiency.
    """
)

st.warning(
    """
    **Recommendation 4**

    Analyze cancellation reasons to identify
    operational bottlenecks and reduce
    claim failure rates.
    """
)

st.divider()

# ============================================
# PAGE SUMMARY
# ============================================

st.markdown(
    """
    ## 📊 Demand Analysis Summary

    This dashboard provides insights into
    receiver behavior, food demand patterns,
    claim performance and beneficiary
    participation.

    The analysis highlights opportunities
    to improve claim completion rates,
    optimize food allocation and strengthen
    beneficiary engagement.
    """
)

st.divider()