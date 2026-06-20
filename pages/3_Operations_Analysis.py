# ============================================
# PAGE 3: OPERATIONS ANALYSIS
# ============================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sqlalchemy import (
    create_engine,
    text
)

# ============================================
# PAGE CONFIG
# ============================================

st.set_page_config(
    page_title="Operations Analysis",
    page_icon="⚙️",
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
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        f"?sslmode=require"
    )

    return create_engine(
        connection_string
    )

engine = get_engine()

# ============================================
# LOAD DATA
# ============================================

@st.cache_data
def load_operations_data():

    engine = get_engine()

    claims = pd.read_sql(
        "SELECT * FROM claims",
        engine
    )

    food_listings = pd.read_sql(
        "SELECT * FROM food_listings",
        engine
    )

    providers = pd.read_sql(
        "SELECT * FROM providers",
        engine
    )

    receivers = pd.read_sql(
        "SELECT * FROM receivers",
        engine
    )

    return (
        claims,
        food_listings,
        providers,
        receivers
    )

claims, food_listings, providers, receivers = (
    load_operations_data()
)

# ============================================
# CREATE ANALYSIS DATASET
# ============================================

claims_analysis = (

    claims

    .merge(
        food_listings,
        on="food_id",
        how="left"
    )

    .merge(
        providers,
        on="provider_id",
        how="left",
        suffixes=(
            "",
            "_provider"
        )
    )

    .merge(
        receivers,
        on="receiver_id",
        how="left",
        suffixes=(
            "",
            "_receiver"
        )
    )

)

# ============================================
# DATE CONVERSION
# ============================================

claims_analysis["expiry_date"] = (
    pd.to_datetime(
        claims_analysis["expiry_date"]
    )
)

claims_analysis["timestamp"] = (
    pd.to_datetime(
        claims_analysis["timestamp"]
    )
)

# ============================================
# DAYS UNTIL EXPIRY
# ============================================

claims_analysis["days_until_expiry"] = (

    claims_analysis["expiry_date"]

    -

    claims_analysis["timestamp"]

).dt.days

# ============================================
# DATA VALIDATION
# ============================================

claims_analysis = (
    claims_analysis
    .dropna(
        subset=[
            "status",
            "days_until_expiry"
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

<h1>⚙️ Operations Analysis</h1>

<p style="font-size:18px;">
Monitor operational efficiency, claim performance,
expiry risk and food redistribution effectiveness.
</p>

</div>
""", unsafe_allow_html=True)

st.write("")

# ============================================
# KPI CALCULATIONS
# ============================================

completion_rate = (

    (
        claims_analysis["status"]
        ==
        "Completed"
    ).mean()

) * 100

successful_claims = (

    claims_analysis["status"]
    ==
    "Completed"

).sum()

expired_claims = (

    claims_analysis["days_until_expiry"]
    < 0

).sum()

avg_days = (

    claims_analysis["days_until_expiry"]
    .mean()

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
        "Completion Rate",
        f"{completion_rate:.1f}%",
        "✅"
    )

with col2:

    metric_card(
        "Successful Claims",
        f"{successful_claims:,}",
        "📦"
    )

with col3:

    metric_card(
        "Expired Claims",
        f"{expired_claims:,}",
        "⚠️"
    )

with col4:

    metric_card(
        "Avg Days To Expiry",
        f"{avg_days:.1f}",
        "📅"
    )

st.write("")

st.divider()

# ============================================
# OPERATIONS OVERVIEW
# ============================================

st.markdown(
    "## 📊 Operations Overview"
)

col1, col2 = st.columns(
    [2,1]
)

with col1:

    st.info(
        """
        This dashboard evaluates platform
        efficiency, food expiry risk,
        claim success rates and operational
        performance across providers and receivers.
        """
    )

with col2:

    st.success(
        f"Overall Completion Rate: {completion_rate:.1f}%"
    )

st.divider()

# ============================================
# FOOD EXPIRY RISK ANALYSIS
# ============================================

st.markdown(
    "## ⚠️ Food Expiry Risk Analysis"
)

col1, col2 = st.columns(2)

# ============================================
# DAYS UNTIL EXPIRY DISTRIBUTION
# ============================================

with col1:

    st.markdown(
        "### 📅 Days Until Expiry Distribution"
    )

    fig, ax = plt.subplots(
        figsize=(8,5)
    )

    sns.histplot(
        data=claims_analysis,
        x="days_until_expiry",
        bins=20,
        kde=True,
        color="#2563EB",
        ax=ax
    )

    ax.axvline(
        x=0,
        color="red",
        linestyle="--",
        linewidth=2
    )

    ax.set_xlabel(
        "Days Until Expiry"
    )

    ax.set_ylabel(
        "Number of Claims"
    )

    sns.despine()

    st.pyplot(fig)

    plt.close()

    st.caption(
        "Claims occurring after the red line represent expired food listings."
    )

# ============================================
# EXPIRY RISK BREAKDOWN
# ============================================

with col2:

    st.markdown(
        "### 🚨 Expiry Risk Breakdown"
    )

    expiry_summary = pd.DataFrame({

        "Category": [
            "Safe",
            "Near Expiry",
            "Expired"
        ],

        "Count": [

            len(
                claims_analysis[
                    claims_analysis[
                        "days_until_expiry"
                    ] > 3
                ]
            ),

            len(
                claims_analysis[
                    (
                        claims_analysis[
                            "days_until_expiry"
                        ] >= 0
                    )
                    &
                    (
                        claims_analysis[
                            "days_until_expiry"
                        ] <= 3
                    )
                ]
            ),

            len(
                claims_analysis[
                    claims_analysis[
                        "days_until_expiry"
                    ] < 0
                ]
            )

        ]

    })

    fig, ax = plt.subplots(
        figsize=(8,5)
    )

    sns.barplot(
        data=expiry_summary,
        x="Category",
        y="Count",
        hue="Category",
        palette="Blues_r",
        legend=False,
        ax=ax
    )

    for container in ax.containers:
        ax.bar_label(container)

    sns.despine()

    st.pyplot(fig)

    plt.close()

    st.caption(
        "Categorization of food listings based on expiry risk."
    )

st.divider()

# ============================================
# RECEIVER PERFORMANCE ANALYSIS
# ============================================

st.markdown(
    "## 🤝 Receiver Performance Analysis"
)

receiver_performance = (

    claims_analysis

    .groupby("type_receiver")

    .agg(
        total_claims=(
            "claim_id",
            "count"
        ),
        completed_claims=(
            "status",
            lambda x:
            (
                x == "Completed"
            ).sum()
        )
    )

    .reset_index()

)

receiver_performance[
    "completion_rate"
] = (

    receiver_performance[
        "completed_claims"
    ]

    /

    receiver_performance[
        "total_claims"
    ]

) * 100

fig, ax = plt.subplots(
    figsize=(10,5)
)

sns.barplot(
    data=receiver_performance,
    x="type_receiver",
    y="completion_rate",
    hue="type_receiver",
    palette="crest",
    legend=False,
    ax=ax
)

ax.set_ylabel(
    "Completion Rate (%)"
)

ax.set_xlabel("")

for container in ax.containers:
    ax.bar_label(
        container,
        fmt="%.1f"
    )

sns.despine()

st.pyplot(fig)

plt.close()

st.caption(
    "Completion rates by receiver category."
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
# TOP PROVIDERS BY SUCCESSFUL CLAIMS
# ============================================

with col1:

    st.markdown(
        "### 🏆 Top Providers by Successful Claims"
    )

    # Count completed claims by provider

    provider_success = (

        claims_analysis[
            claims_analysis["status"] == "Completed"
        ]

        .groupby("provider_id")["claim_id"]

        .count()

        .reset_index()

    )

    provider_success.columns = [
        "provider_id",
        "Successful Claims"
    ]

    # Merge provider names

    provider_success = provider_success.merge(
        providers[
            ["provider_id", "name"]
        ],
        on="provider_id",
        how="left"
    )

    # Top 10 providers

    provider_success = (

        provider_success

        .nlargest(
            10,
            "Successful Claims"
        )

        .sort_values(
            "Successful Claims"
        )

    )

    fig, ax = plt.subplots(
        figsize=(9,5)
    )

    sns.barplot(
        data=provider_success,
        x="Successful Claims",
        y="name",
        hue="name",
        palette="crest",
        legend=False,
        ax=ax
    )

    for container in ax.containers:
        ax.bar_label(
            container,
            padding=3
        )

    ax.set_xlabel(
        "Successful Claims"
    )

    ax.set_ylabel(
        "Provider"
    )

    sns.despine()

    st.pyplot(fig)

    plt.close()

    st.caption(
        "Top performing providers based on completed food claims."
    )
# ============================================
# AVERAGE QUANTITY PER RECEIVER
# ============================================

with col2:

    st.markdown(
        "### 📦 Average Quantity Claimed"
    )

    quantity_analysis = (

        claims_analysis

        .groupby("type_receiver")["quantity"]

        .mean()

        .reset_index()

    )

    quantity_analysis.columns = [
        "Receiver Type",
        "Average Quantity"
    ]

    fig, ax = plt.subplots(
        figsize=(8,5)
    )

    sns.barplot(
        data=quantity_analysis,
        x="Receiver Type",
        y="Average Quantity",
        hue="Receiver Type",
        palette="Blues_r",
        legend=False,
        ax=ax
    )

    for container in ax.containers:
        ax.bar_label(
            container,
            fmt="%.1f"
        )

    sns.despine()

    st.pyplot(fig)

    plt.close()

    st.caption(
        "Average quantity received per claim by receiver category."
    )

st.divider()

# ============================================
# OPERATIONAL HIGHLIGHTS
# ============================================

st.markdown(
    "## 🎯 Operational Highlights"
)

col1, col2, col3 = st.columns(3)

with col1:

    safe_food = len(
        claims_analysis[
            claims_analysis[
                "days_until_expiry"
            ] > 0
        ]
    )

    st.success(
        f"""
        ### ✅ Safe Food Listings

        **{safe_food:,}**

        claims occurred before
        food expiry.
        """
    )

with col2:

    st.warning(
        f"""
        ### ⚠️ Expired Claims

        **{expired_claims:,}**

        claims occurred after
        food expiry dates.
        """
    )

with col3:

    top_provider = (

        provider_success.iloc[-1]["name"]

        if len(provider_success) > 0

        else "N/A"

    )

    st.info(
        f"""
        ### 🏆 Best Provider

        **{top_provider}**

        achieved the highest
        number of successful claims.
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
        ### 📊 Claim Performance

        The platform processed

        **{len(claims_analysis):,} claims**

        with an overall completion rate of

        **{completion_rate:.1f}%**

        indicating opportunities to improve
        redistribution efficiency.
        """
    )

# ============================================
# INSIGHT 2
# ============================================

with col2:

    st.info(
        f"""
        ### ⚠️ Expiry Risk

        A total of

        **{expired_claims:,} claims**

        were associated with expired food.

        This represents a significant
        operational and food-safety risk.
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
        ### 🏢 Provider Contribution

        Provider participation remains
        diversified across the platform,
        reducing dependency on a single
        food source.
        """
    )

# ============================================
# INSIGHT 4
# ============================================

with col2:

    st.success(
        """
        ### 🤝 Receiver Utilization

        Food demand is distributed across
        multiple receiver categories,
        supporting broader community impact.
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

    Implement automated expiry alerts
    for listings approaching expiration.
    """
)

st.warning(
    """
    **Recommendation 2**

    Restrict claim creation for food
    items that have already expired.
    """
)

st.warning(
    """
    **Recommendation 3**

    Prioritize high-performing providers
    to improve redistribution efficiency.
    """
)

st.warning(
    """
    **Recommendation 4**

    Improve follow-up processes for
    pending claims to increase
    completion rates.
    """
)

st.divider()

# ============================================
# OPERATIONS SUMMARY
# ============================================

st.markdown(
    "## 📊 Operations Summary"
)

st.success(
    f"""
    • Completion Rate: **{completion_rate:.1f}%**

    • Successful Claims: **{successful_claims:,}**

    • Expired Claims: **{expired_claims:,}**

    • Average Days Until Expiry:
      **{avg_days:.1f} days**

    • The platform demonstrates strong
      provider participation but can
      improve claim completion and
      expiry management processes.
    """
)

# ============================================
# DATA MANAGEMENT
# ============================================

st.divider()

st.markdown(
    "## 🗄️ Data Management"
)

st.caption(
    """
    Manage Providers, Receivers,
    Food Listings and Claims directly
    from the dashboard.
    """
)

tab1, tab2, tab3 = st.tabs([
    "➕ Add Records",
    "✏️ Update Records",
    "🗑️ Delete Records"
])

# ============================================
# TAB 1: ADD RECORDS
# ============================================

with tab1:

    st.markdown(
        """
        ### ➕ Add New Records
        """
    )

    add_tab1, add_tab2, add_tab3, add_tab4 = st.tabs([
        "Provider",
        "Receiver",
        "Food Listing",
        "Claim"
    ])

    # ----------------------------------------
    # ADD PROVIDER
    # ----------------------------------------

    with add_tab1:

        with st.form("add_provider_form"):

            name = st.text_input("Provider Name")

            provider_type = st.selectbox(
                "Provider Type",
                [
                    "Restaurant",
                    "Grocery Store",
                    "Supermarket",
                    "Catering Service"
                ]
            )

            address = st.text_input("Address")

            city = st.text_input("City")

            contact = st.text_input("Contact")

            submitted = st.form_submit_button(
                "Add Provider"
            )

            if submitted:

                try:

                    with engine.connect() as conn:

                        max_id = conn.execute(
                            text(
                                'SELECT MAX("Provider_ID") FROM providers'
                            )
                        ).scalar()

                        new_id = (max_id or 0) + 1

                        conn.execute(
                            text("""
                            INSERT INTO providers
                            ("Provider_ID","Name","Type","Address","City","Contact")
                            VALUES
                            (:id,:name,:type,:address,:city,:contact)
                            """),
                            {
                                "id": new_id,
                                "name": name,
                                "type": provider_type,
                                "address": address,
                                "city": city,
                                "contact": contact
                            }
                        )

                        conn.commit()

                    st.success(
                        f"✅ Provider added successfully (ID {new_id})"
                    )

                    st.cache_data.clear()
                    st.rerun()

                except Exception as e:
                    st.error(f"Error: {e}")

    # ----------------------------------------
    # ADD RECEIVER
    # ----------------------------------------

    with add_tab2:

        with st.form("add_receiver_form"):

            name = st.text_input("Receiver Name")

            receiver_type = st.selectbox(
                "Receiver Type",
                [
                    "NGO",
                    "Charity",
                    "Shelter",
                    "Individual"
                ]
            )

            city = st.text_input("City")

            contact = st.text_input("Contact")

            submitted = st.form_submit_button(
                "Add Receiver"
            )

            if submitted:

                try:

                    with engine.connect() as conn:

                        max_id = conn.execute(
                            text(
                                'SELECT MAX("Receiver_ID") FROM receivers'
                            )
                        ).scalar()

                        new_id = (max_id or 0) + 1

                        conn.execute(
                            text("""
                            INSERT INTO receivers
                            ("Receiver_ID","Name","Type","City","Contact")
                            VALUES
                            (:id,:name,:type,:city,:contact)
                            """),
                            {
                                "id": new_id,
                                "name": name,
                                "type": receiver_type,
                                "city": city,
                                "contact": contact
                            }
                        )

                        conn.commit()

                    st.success(
                        f"✅ Receiver added successfully (ID {new_id})"
                    )

                    st.cache_data.clear()
                    st.rerun()

                except Exception as e:
                    st.error(f"Error: {e}")

    # ----------------------------------------
    # ADD FOOD LISTING
    # ----------------------------------------

    with add_tab3:

        with st.form("add_food_form"):

            food_name = st.text_input(
                "Food Name"
            )

            quantity = st.number_input(
                "Quantity",
                min_value=1
            )

            expiry_date = st.date_input(
                "Expiry Date"
            )

            provider_id = st.number_input(
                "Provider ID",
                min_value=1
            )

            provider_type = st.text_input(
                "Provider Type"
            )

            location = st.text_input(
                "Location"
            )

            food_type = st.selectbox(
                "Food Type",
                [
                    "Vegetarian",
                    "Vegan",
                    "Non-Vegetarian"
                ]
            )

            meal_type = st.selectbox(
                "Meal Type",
                [
                    "Breakfast",
                    "Lunch",
                    "Dinner",
                    "Snacks"
                ]
            )

            submitted = st.form_submit_button(
                "Add Food Listing"
            )

            if submitted:

                try:

                    with engine.connect() as conn:

                        max_id = conn.execute(
                            text(
                                'SELECT MAX("Food_ID") FROM food_listings'
                            )
                        ).scalar()

                        new_id = (max_id or 0) + 1

                        conn.execute(
                            text("""
                            INSERT INTO food_listings
                            ("Food_ID","Food_Name","Quantity",
                             "Expiry_Date","Provider_ID",
                             "Provider_Type","Location",
                             "Food_Type","Meal_Type")
                            VALUES
                            (:id,:food_name,:quantity,
                             :expiry_date,:provider_id,
                             :provider_type,:location,
                             :food_type,:meal_type)
                            """),
                            {
                                "id": new_id,
                                "food_name": food_name,
                                "quantity": quantity,
                                "expiry_date": expiry_date,
                                "provider_id": provider_id,
                                "provider_type": provider_type,
                                "location": location,
                                "food_type": food_type,
                                "meal_type": meal_type
                            }
                        )

                        conn.commit()

                    st.success(
                        f"✅ Food Listing added successfully (ID {new_id})"
                    )

                    st.cache_data.clear()
                    st.rerun()

                except Exception as e:
                    st.error(f"Error: {e}")

    # ----------------------------------------
    # ADD CLAIM
    # ----------------------------------------

    with add_tab4:

        with st.form("add_claim_form"):

            food_id = st.number_input(
                "Food ID",
                min_value=1
            )

            receiver_id = st.number_input(
                "Receiver ID",
                min_value=1
            )

            status = st.selectbox(
                "Status",
                [
                    "Pending",
                    "Completed",
                    "Cancelled"
                ]
            )

            timestamp = st.date_input(
                "Claim Date"
            )

            submitted = st.form_submit_button(
                "Add Claim"
            )

            if submitted:

                try:

                    with engine.connect() as conn:

                        max_id = conn.execute(
                            text(
                                'SELECT MAX("Claim_ID") FROM claims'
                            )
                        ).scalar()

                        new_id = (max_id or 0) + 1

                        conn.execute(
                            text("""
                            INSERT INTO claims
                            ("Claim_ID","Food_ID","Receiver_ID",
                             "Status","Timestamp")
                            VALUES
                            (:id,:food_id,:receiver_id,
                             :status,:timestamp)
                            """),
                            {
                                "id": new_id,
                                "food_id": food_id,
                                "receiver_id": receiver_id,
                                "status": status,
                                "timestamp": timestamp
                            }
                        )

                        conn.commit()

                    st.success(
                        f"✅ Claim added successfully (ID {new_id})"
                    )

                    st.cache_data.clear()
                    st.rerun()

                except Exception as e:
                    st.error(f"Error: {e}")

# ============================================
# UPDATE RECORDS
# ============================================

with tab2:

    st.subheader("✏️ Update Provider")

    with st.form("update_provider_form"):

        provider_id = st.number_input(
            "Provider ID",
            min_value=1
        )

        field = st.selectbox(
            "Field",
            ["Name", "Type", "City", "Contact"]
        )

        value = st.text_input(
            "New Value"
        )

        submitted = st.form_submit_button(
            "Update Provider"
        )

        if submitted:

            try:

                with engine.connect() as conn:

                    conn.execute(
                        text(f'''
                        UPDATE providers
                        SET "{field}"=:value
                        WHERE "Provider_ID"=:id
                        '''),
                        {
                            "value": value,
                            "id": provider_id
                        }
                    )

                    conn.commit()

                st.success(
                    "✅ Provider updated successfully."
                )

                st.cache_data.clear()
                st.rerun()

            except Exception as e:
                st.error(f"Error: {e}")

# ============================================
# DELETE RECORDS
# ============================================

with tab3:

    st.warning(
        "This action cannot be undone."
    )

    with st.form("delete_food_form"):

        food_id = st.number_input(
            "Food ID",
            min_value=1
        )

        submitted = st.form_submit_button(
            "Delete Food Listing"
        )

        if submitted:

            try:

                with engine.connect() as conn:

                    conn.execute(
                        text("""
                        DELETE FROM food_listings
                        WHERE "Food_ID"=:id
                        """),
                        {"id": food_id}
                    )

                    conn.commit()

                st.success(
                    "✅ Food listing deleted successfully."
                )

                st.cache_data.clear()
                st.rerun()

            except Exception as e:
                st.error(f"Error: {e}")

# ============================================
# REFRESH DATA
# ============================================

st.divider()

if st.button(
    "🔄 Refresh Dashboard Data",
    use_container_width=True
):

    st.cache_data.clear()

    st.success(
        "Dashboard refreshed successfully."
    )

    st.rerun()