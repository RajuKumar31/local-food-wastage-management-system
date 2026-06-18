# ============================================
# PAGE 2: DEMAND ANALYSIS
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
        on="Receiver_ID",
        how="left"
    )
    .merge(
        food_listings,
        on="Food_ID",
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
    claims_analysis["Type"].unique()
)

selected_receiver_types = st.sidebar.multiselect(
    "Receiver Type",
    options=all_receiver_types,
    default=all_receiver_types
)


all_statuses = sorted(
    claims_analysis["Status"].unique()
)

selected_statuses = st.sidebar.multiselect(
    "Claim Status",
    options=all_statuses,
    default=all_statuses
)


all_meal_types = sorted(
    claims_analysis["Meal_Type"].unique()
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
    claims_analysis["Type"].isin(selected_receiver_types)
    &
    claims_analysis["Status"].isin(selected_statuses)
    &
    claims_analysis["Meal_Type"].isin(selected_meal_types)
]


# ============================================
# KPI CARDS
# ============================================

total_claims = len(filtered_claims)

completed_claims = len(
    filtered_claims[
        filtered_claims["Status"] == "Completed"
    ]
)

pending_claims = len(
    filtered_claims[
        filtered_claims["Status"] == "Pending"
    ]
)

cancelled_claims = len(
    filtered_claims[
        filtered_claims["Status"] == "Cancelled"
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
        filtered_claims["Status"]
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
        filtered_claims["Type"]
        .value_counts()
        .reset_index()
    )

    receiver_counts.columns = [
        "Receiver_Type",
        "Count"
    ]

    fig, ax = plt.subplots(figsize=(7, 4))

    sns.barplot(
        data=receiver_counts,
        x="Receiver_Type",
        y="Count",
        hue="Receiver_Type",
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
        filtered_claims["Meal_Type"]
        .value_counts()
        .reset_index()
    )

    meal_claims.columns = [
        "Meal_Type",
        "Claims"
    ]

    fig, ax = plt.subplots(figsize=(7, 4))

    sns.barplot(
        data=meal_claims,
        x="Meal_Type",
        y="Claims",
        hue="Meal_Type",
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
        .groupby(["Receiver_ID", "Name"])["Claim_ID"]
        .count()
        .reset_index()
    )

    top_receivers.columns = [
        "Receiver_ID",
        "Receiver_Name",
        "Claims"
    ]

    top_receivers = (
        top_receivers
        .nlargest(10, "Claims")
        .sort_values("Claims")
    )

    fig, ax = plt.subplots(figsize=(8, 5))

    sns.barplot(
        data=top_receivers,
        x="Claims",
        y="Receiver_Name",
        hue="Receiver_Name",
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