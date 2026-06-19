# ============================================
# PAGE 2: DEMAND ANALYSIS
# ============================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sqlalchemy import create_engine

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

    return claims, receivers, food_listings


claims, receivers, food_listings = load_demand_data()


# ============================================
# MERGE DATA
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
# PAGE TITLE
# ============================================

st.title("🤝 Demand Analysis")

st.markdown(
    """
    Explore receiver behaviour, claim activity,
    and food demand patterns across the platform.
    """
)


# ============================================
# SIDEBAR FILTERS
# ============================================

st.sidebar.header("Filters")


all_receiver_types = sorted(
    claims_analysis["type"].unique()
)

selected_receiver_types = st.sidebar.multiselect(
    "Receiver Type",
    options=all_receiver_types,
    default=all_receiver_types
)


all_statuses = sorted(
    claims_analysis["status"].unique()
)

selected_statuses = st.sidebar.multiselect(
    "Claim Status",
    options=all_statuses,
    default=all_statuses
)


all_meal_types = sorted(
    claims_analysis["meal_type"].unique()
)

selected_meal_types = st.sidebar.multiselect(
    "Meal Type",
    options=all_meal_types,
    default=all_meal_types
)


# ============================================
# APPLY FILTERS
# ============================================

filtered_claims = claims_analysis[
    claims_analysis["type"].isin(selected_receiver_types)
    &
    claims_analysis["status"].isin(selected_statuses)
    &
    claims_analysis["meal_type"].isin(selected_meal_types)
]


# ============================================
# KPI CARDS
# ============================================

total_claims = len(filtered_claims)

completed_claims = len(
    filtered_claims[
        filtered_claims["status"] == "Completed"
    ]
)

pending_claims = len(
    filtered_claims[
        filtered_claims["status"] == "Pending"
    ]
)

cancelled_claims = len(
    filtered_claims[
        filtered_claims["status"] == "Cancelled"
    ]
)


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Claims",
        f"{total_claims:,}"
    )

with col2:
    st.metric(
        "Completed",
        f"{completed_claims:,}"
    )

with col3:
    st.metric(
        "Pending",
        f"{pending_claims:,}"
    )

with col4:
    st.metric(
        "Cancelled",
        f"{cancelled_claims:,}"
    )


st.divider()


# ============================================
# ROW 1
# ============================================

col1, col2 = st.columns(2)


# Claim Status Distribution
with col1:

    st.subheader(
        "Claim Status Distribution"
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

    fig, ax = plt.subplots(figsize=(7, 4))

    sns.barplot(
        data=status_counts,
        x="Status",
        y="Count",
        hue="Status",
        palette="Oranges",
        legend=False,
        ax=ax
    )

    for container in ax.containers:
        ax.bar_label(container)

    plt.tight_layout()
    st.pyplot(fig)
    plt.close()


# Receiver Type Distribution
with col2:

    st.subheader(
        "Receiver Type Distribution"
    )

    receiver_counts = (
        filtered_claims["type"]
        .value_counts()
        .reset_index()
    )

    receiver_counts.columns = [
        "receiver_type",
        "Count"
    ]

    fig, ax = plt.subplots(figsize=(7, 4))

    sns.barplot(
        data=receiver_counts,
        x="receiver_type",
        y="Count",
        hue="receiver_type",
        palette="Greens_r",
        legend=False,
        ax=ax
    )

    for container in ax.containers:
        ax.bar_label(container)

    plt.tight_layout()
    st.pyplot(fig)
    plt.close()


st.divider()


# ============================================
# ROW 2
# ============================================

col1, col2 = st.columns(2)


# Claims by Meal Type
with col1:

    st.subheader(
        "Claims by Meal Type"
    )

    meal_claims = (
        filtered_claims["meal_type"]
        .value_counts()
        .reset_index()
    )

    meal_claims.columns = [
        "meal_type",
        "claims"
    ]

    fig, ax = plt.subplots(figsize=(7, 4))

    sns.barplot(
        data=meal_claims,
        x="meal_type",
        y="claims",
        hue="meal_type",
        palette="YlOrBr",
        legend=False,
        ax=ax
    )

    for container in ax.containers:
        ax.bar_label(container)

    plt.tight_layout()
    st.pyplot(fig)
    plt.close()


# Top 10 Receivers by Claims
with col2:

    st.subheader(
        "Top 10 Receivers by Claims"
    )

    top_receivers = (
        filtered_claims
        .groupby(["receiver_id", "name"])["claim_id"]
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
        .nlargest(10, "claims")
        .sort_values("claims")
    )

    fig, ax = plt.subplots(figsize=(8, 5))

    sns.barplot(
        data=top_receivers,
        x="claims",
        y="receiver_name",
        hue="receiver_name",
        palette="crest",
        legend=False,
        ax=ax
    )

    for container in ax.containers:
        ax.bar_label(container)

    plt.tight_layout()
    st.pyplot(fig)
    plt.close()


# ============================================
# INSIGHTS
# ============================================

st.divider()

st.subheader("Key Insights")

st.markdown(
    """
    - Claim completion rate remains approximately 33.9%,
      indicating substantial opportunity for operational improvement.

    - Breakfast generates the highest number of claims,
      demonstrating stronger demand than other meal categories.

    - NGOs and Charities account for a significant share
      of platform beneficiaries.

    - Claim activity is broadly distributed across receivers,
      with no single receiver dominating food redistribution.
    """
)