# ============================================
# IMPORTS
# ============================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from dotenv import load_dotenv
from sqlalchemy import create_engine
from pathlib import Path
import os


# ============================================
# PAGE CONFIG
# ============================================

st.set_page_config(
    page_title="Local Food Wastage Management System",
    page_icon="🍱",
    layout="wide"
)

# ============================================
# DATABASE CONNECTION
# ============================================

from pathlib import Path

@st.cache_resource
def get_engine():

    env_path = Path(__file__).resolve().parent / ".env"

    load_dotenv(env_path, override=True)

    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    if not all([DB_HOST, DB_PORT, DB_NAME, DB_USER]):
        st.error(
            f"""
            Environment variables missing

            HOST={DB_HOST}
            PORT={DB_PORT}
            DB={DB_NAME}
            USER={DB_USER}
            """
        )
        st.stop()

    connection_string = (
        f"postgresql+psycopg2://"
        f"{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
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
# PAGE TITLE
# ============================================

st.title("🍱 Local Food Wastage Management System")

st.markdown(
    "Executive Summary Dashboard"
)

# ============================================
# KPI CARDS
# ============================================

total_providers = len(providers)
total_receivers = len(receivers)
total_food_listings = len(food_listings)

completed_claims = (
    claims["Status"] == "Completed"
).sum()

completion_rate = (
    completed_claims / len(claims)
) * 100


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Providers",
        f"{total_providers:,}"
    )

with col2:
    st.metric(
        "Total Receivers",
        f"{total_receivers:,}"
    )

with col3:
    st.metric(
        "Total Food Listings",
        f"{total_food_listings:,}"
    )

with col4:
    st.metric(
        "Claim Completion Rate",
        f"{completion_rate:.1f}%"
    )
st.divider()

# ============================================
# CHARTS
# ============================================

col1, col2 = st.columns(2)


# --------------------------------------------
# Provider Type Distribution
# --------------------------------------------

with col1:

    provider_counts = (
        providers["Type"]
        .value_counts()
        .reset_index()
    )

    provider_counts.columns = [
        "Provider_Type",
        "Count"
    ]

    fig, ax = plt.subplots(
        figsize=(8, 5)
    )

    sns.barplot(
        data=provider_counts,
        x="Provider_Type",
        y="Count",
        hue="Provider_Type",
        palette="Blues_d",
        legend=False,
        ax=ax
    )

    ax.set_title(
        "Provider Type Distribution"
    )

    ax.set_xlabel(
        "Provider Type"
    )

    ax.set_ylabel(
        "Count"
    )

    for container in ax.containers:
        ax.bar_label(container)

    st.pyplot(fig)
    plt.close()

# --------------------------------------------
# Claim Status Distribution
# --------------------------------------------

with col2:

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
        figsize=(8, 5)
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

    ax.set_title(
        "Claim Status Distribution"
    )

    ax.set_xlabel(
        "Claim Status"
    )

    ax.set_ylabel(
        "Count"
    )

    for container in ax.containers:
        ax.bar_label(container)

    st.pyplot(fig)