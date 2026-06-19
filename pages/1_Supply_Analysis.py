# ============================================
# PAGE 1: SUPPLY ANALYSIS
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


# ============================================
# PAGE TITLE
# ============================================

st.title("📦 Supply Analysis")

st.markdown(
    """
    Explore food availability, provider contributions,
    and inventory composition.
    """
)


# ============================================
# SIDEBAR FILTERS
# ============================================

st.sidebar.header("Filters")


all_provider_types = sorted(
    food_listings["provider_type"].unique()
)

selected_provider_types = st.sidebar.multiselect(
    "Provider Type",
    options=all_provider_types,
    default=all_provider_types
)


all_food_types = sorted(
    food_listings["food_type"].unique()
)

selected_food_types = st.sidebar.multiselect(
    "Food Type",
    options=all_food_types,
    default=all_food_types
)


all_meal_types = sorted(
    food_listings["meal_type"].unique()
)

selected_meal_types = st.sidebar.multiselect(
    "Meal Type",
    options=all_meal_types,
    default=all_meal_types
)


# ============================================
# APPLY FILTERS
# ============================================

filtered_food = food_listings[
    food_listings["provider_type"].isin(selected_provider_types)
    &
    food_listings["food_type"].isin(selected_food_types)
    &
    food_listings["meal_type"].isin(selected_meal_types)
]


# ============================================
# KPI CARDS
# ============================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Food Listings",
        f"{len(filtered_food):,}"
    )

with col2:
    st.metric(
        "Total Quantity",
        f"{filtered_food['quantity'].sum():,}"
    )

with col3:
    st.metric(
        "Provider Types",
        filtered_food["provider_type"].nunique()
    )


st.divider()


# ============================================
# ROW 1
# ============================================

col1, col2 = st.columns(2)

# Food Type Distribution
with col1:

    st.subheader("Food Type Distribution")

    food_type_counts = (
        filtered_food["food_type"]
        .value_counts()
        .reset_index()
    )

    food_type_counts.columns = [
        "Food_Type",
        "Count"
    ]

    fig, ax = plt.subplots(figsize=(7, 4))

    sns.barplot(
        data=food_type_counts,
        x="Food_Type",
        y="Count",
        hue="Food_Type",
        palette="Oranges_r",
        legend=False,
        ax=ax
    )

    for container in ax.containers:
        ax.bar_label(container)

    st.pyplot(fig)
    plt.close()


# Meal Type Distribution
with col2:

    st.subheader("Meal Type Distribution")

    meal_type_counts = (
        filtered_food["meal_type"]
        .value_counts()
        .reset_index()
    )

    meal_type_counts.columns = [
        "Meal_Type",
        "Count"
    ]

    fig, ax = plt.subplots(figsize=(7, 4))

    sns.barplot(
        data=meal_type_counts,
        x="Meal_Type",
        y="Count",
        hue="Meal_Type",
        palette="Purples",
        legend=False,
        ax=ax
    )

    for container in ax.containers:
        ax.bar_label(container)

    st.pyplot(fig)
    plt.close()


st.divider()


# ============================================
# ROW 2
# ============================================

col1, col2 = st.columns(2)

# Top Providers
with col1:

    st.subheader(
        "Top 10 Providers by Quantity"
    )

    provider_quantity = (
        filtered_food
        .groupby("provider_id")["quantity"]
        .sum()
        .reset_index()
    )

    provider_quantity = provider_quantity.merge(
        providers[["provider_id", "name"]],
        on="provider_id",
        how="left"
    )

    top_10 = (
        provider_quantity
        .nlargest(10, "quantity")
        .sort_values("quantity")
    )

    fig, ax = plt.subplots(figsize=(8, 5))

    sns.barplot(
        data=top_10,
        x="quantity",
        y="name",
        hue="name",
        palette="crest",
        legend=False,
        ax=ax
    )

    for container in ax.containers:
        ax.bar_label(container)

    st.pyplot(fig)
    plt.close()


# Provider Contribution
with col2:

    st.subheader(
        "Provider Type Contribution"
    )

    contribution = (
        filtered_food
        .groupby("provider_type")["quantity"]
        .sum()
        .reset_index()
        .sort_values(
            "quantity",
            ascending=False
        )
    )

    fig, ax = plt.subplots(figsize=(7, 4))

    sns.barplot(
        data=contribution,
        x="provider_type",
        y="quantity",
        hue="provider_type",
        palette="Blues_d",
        legend=False,
        ax=ax
    )

    for container in ax.containers:
        ax.bar_label(container)

    st.pyplot(fig)
    plt.close()


st.divider()


# ============================================
# INSIGHTS
# ============================================

st.subheader("Key Insights")

st.markdown(
    """
    - Food availability is balanced across Vegetarian, Vegan,
      and Non-Vegetarian categories.

    - Breakfast and Snacks represent a large share of
      available food listings.

    - Restaurants contribute the highest overall quantity
      of food.

    - Barry Group is the leading individual food provider.
    """
)