# ============================================
# PAGE 3: OPERATIONS ANALYSIS
# ============================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os


# ============================================
# DATABASE CONNECTION
# ============================================

@st.cache_resource
def get_engine():

    load_dotenv()

    connection_string = (
        f"postgresql+psycopg2://"
        f"{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}"
        f"/{os.getenv('DB_NAME')}"
    )

    return create_engine(connection_string)


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

    return claims, food_listings, providers, receivers


claims, food_listings, providers, receivers = load_operations_data()


# ============================================
# MERGED DATASET
# ============================================

claims_analysis = (
    claims
    .merge(
        food_listings,
        on="Food_ID",
        how="left"
    )
    .merge(
        providers,
        on="Provider_ID",
        how="left",
        suffixes=("", "_Provider")
    )
    .merge(
        receivers,
        on="Receiver_ID",
        how="left",
        suffixes=("", "_Receiver")
    )
)

# ============================================
# DAYS UNTIL EXPIRY
# ============================================

claims_analysis["Expiry_Date"] = pd.to_datetime(
    claims_analysis["Expiry_Date"]
)

claims_analysis["Timestamp"] = pd.to_datetime(
    claims_analysis["Timestamp"]
)

claims_analysis["Days_Until_Expiry"] = (
    claims_analysis["Expiry_Date"]
    - claims_analysis["Timestamp"]
).dt.days


# ============================================
# PAGE TITLE
# ============================================

st.title("⚙️ Operations Analysis")

st.markdown(
    """
    Monitor platform efficiency,
    claim performance and food redistribution effectiveness.
    """
)


# ============================================
# KPI CARDS
# ============================================

completion_rate = (
    (
        claims_analysis["Status"] == "Completed"
    ).mean() * 100
)

expired_claims = (
    claims_analysis["Days_Until_Expiry"] < 0
).sum()

successful_claims = (
    claims_analysis["Status"] == "Completed"
).sum()

avg_days = (
    claims_analysis["Days_Until_Expiry"]
    .mean()
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Completion Rate",
        f"{completion_rate:.1f}%"
    )

with col2:
    st.metric(
        "Successful Claims",
        f"{successful_claims:,}"
    )

with col3:
    st.metric(
        "Expired Claims",
        expired_claims
    )

with col4:
    st.metric(
        "Avg Days Until Expiry",
        f"{avg_days:.1f}"
    )

st.divider()


# ============================================
# ROW 1
# ============================================

col1, col2 = st.columns(2)


# Days Until Expiry Histogram
with col1:

    st.subheader(
        "Days Until Expiry Distribution"
    )

    fig, ax = plt.subplots(figsize=(8, 5))

    sns.histplot(
        data=claims_analysis,
        x="Days_Until_Expiry",
        bins=20,
        kde=True,
        color="steelblue",
        ax=ax
    )

    ax.axvline(
        0,
        color="red",
        linestyle="--",
        linewidth=2,
        label="Expiry Boundary"
    )

    ax.legend()

    plt.tight_layout()

    st.pyplot(fig)

    plt.close()


# Completion Rate by Receiver Type
with col2:

    st.subheader(
        "Completion Rate by Receiver Type"
    )

    total_claims = (
        claims_analysis
        .groupby("Type_Receiver")["Claim_ID"]
        .count()
        .reset_index(name="Total_Claims")
    )

    completed_claims = (
        claims_analysis[
            claims_analysis["Status"] == "Completed"
        ]
        .groupby("Type_Receiver")["Claim_ID"]
        .count()
        .reset_index(name="Completed_Claims")
    )

    completion_df = (
        total_claims
        .merge(
            completed_claims,
            on="Type_Receiver"
        )
    )

    completion_df["Completion_Rate"] = (
        completion_df["Completed_Claims"]
        /
        completion_df["Total_Claims"]
        * 100
    )

    fig, ax = plt.subplots(figsize=(8, 5))

    sns.barplot(
        data=completion_df,
        x="Type_Receiver",
        y="Completion_Rate",
        hue="Type_Receiver",
        palette="Greens",
        legend=False,
        ax=ax
    )

    for container in ax.containers:
        ax.bar_label(
            container,
            fmt="%.1f"
        )

    ax.set_ylabel("Completion Rate (%)")

    plt.tight_layout()

    st.pyplot(fig)

    plt.close()


st.divider()


# ============================================
# ROW 2
# ============================================

col1, col2 = st.columns(2)


# Top Providers by Successful Claims
with col1:

    st.subheader(
        "Top 10 Providers by Successful Claims"
    )

    provider_success = (
        claims_analysis[
            claims_analysis["Status"] == "Completed"
        ]
        .groupby(
            ["Provider_ID", "Name"]
        )["Claim_ID"]
        .count()
        .reset_index(name="Successful_Claims")
    )

    provider_success = (
        provider_success
        .nlargest(
            10,
            "Successful_Claims"
        )
        .sort_values(
            "Successful_Claims"
        )
    )

    fig, ax = plt.subplots(figsize=(8, 5))

    sns.barplot(
        data=provider_success,
        x="Successful_Claims",
        y="Name",
        hue="Name",
        palette="crest",
        legend=False,
        ax=ax
    )

    for container in ax.containers:
        ax.bar_label(container)

    plt.tight_layout()

    st.pyplot(fig)

    plt.close()

# Average Quantity per Receiver
with col2:

    st.subheader(
        "Average Quantity per Receiver"
    )

    receiver_avg = (
        claims_analysis
        .groupby(
            ["Receiver_ID", "Name_Receiver"]
        )["Quantity"]
        .mean()
        .reset_index(
            name="Average_Quantity"
        )
    )

    receiver_avg = (
        receiver_avg
        .nlargest(
            10,
            "Average_Quantity"
        )
        .sort_values(
            "Average_Quantity"
        )
    )

    fig, ax = plt.subplots(figsize=(8, 5))

    sns.barplot(
        data=receiver_avg,
        x="Average_Quantity",
        y="Name_Receiver",
        hue="Name_Receiver",
        palette="mako",
        legend=False,
        ax=ax
    )

    for container in ax.containers:
        ax.bar_label(
            container,
            fmt="%.1f"
        )

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
    - Overall claim completion rate is approximately 33.9%.

    - Most food is claimed around 11 days before expiry,
      though a small number of claims occur after expiry.

    - Barry Group ranks among the strongest operational
      contributors in terms of successful claim outcomes.

    - Average quantity per receiver should be interpreted
      alongside claim frequency to avoid small-sample bias.
    """
)


# ============================================
# SECTION B: CRUD OPERATIONS
# ============================================

st.divider()
st.header("Data Management")

tab1, tab2, tab3 = st.tabs([
    "Add Records",
    "Update Records",
    "Delete Records"
])


# ============================================
# TAB 1: ADD RECORDS
# ============================================

with tab1:

    add_tab1, add_tab2, add_tab3, add_tab4 = st.tabs([
        "Add Provider",
        "Add Receiver",
        "Add Food Listing",
        "Add Claim"
    ])

    with add_tab1:
        st.subheader("Add New Provider")

        with st.form("add_provider_form"):
            name = st.text_input("Provider Name")
            provider_type = st.selectbox(
                "Provider Type",
                ["Restaurant", "Grocery Store",
                 "Supermarket", "Catering Service"]
            )
            address = st.text_input("Address")
            city = st.text_input("City")
            contact = st.text_input("Contact")
            submitted = st.form_submit_button("Add Provider")

            if submitted:
                if not name or not city or not contact:
                    st.error(
                        "Name, City and Contact are required."
                    )
                else:
                    try:
                        with engine.connect() as conn:
                            max_id = conn.execute(
                                text(
                                    'SELECT MAX("Provider_ID")'
                                    ' FROM providers'
                                )
                            ).scalar()
                            new_id = (max_id or 0) + 1
                            conn.execute(
                                text("""
                                    INSERT INTO providers
                                    ("Provider_ID","Name","Type",
                                     "Address","City","Contact")
                                    VALUES
                                    (:id,:name,:type,
                                     :address,:city,:contact)
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
                            f"Provider '{name}' added "
                            f"with ID {new_id}."
                        )
                        st.cache_data.clear()
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")

    with add_tab2:
        st.subheader("Add New Receiver")

        with st.form("add_receiver_form"):
            name = st.text_input("Receiver Name")
            receiver_type = st.selectbox(
                "Receiver Type",
                ["NGO", "Charity", "Shelter", "Individual"]
            )
            city = st.text_input("City")
            contact = st.text_input("Contact")
            submitted = st.form_submit_button("Add Receiver")

            if submitted:
                if not name or not city or not contact:
                    st.error(
                        "Name, City and Contact are required."
                    )
                else:
                    try:
                        with engine.connect() as conn:
                            max_id = conn.execute(
                                text(
                                    'SELECT MAX("Receiver_ID")'
                                    ' FROM receivers'
                                )
                            ).scalar()
                            new_id = (max_id or 0) + 1
                            conn.execute(
                                text("""
                                    INSERT INTO receivers
                                    ("Receiver_ID","Name","Type",
                                     "City","Contact")
                                    VALUES
                                    (:id,:name,:type,
                                     :city,:contact)
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
                            f"Receiver '{name}' added "
                            f"with ID {new_id}."
                        )
                        st.cache_data.clear()
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")

    with add_tab3:
        st.subheader("Add New Food Listing")

        with st.form("add_food_form"):
            food_name = st.selectbox(
                "Food Name",
                ["Rice", "Soup", "Bread", "Fruits",
                 "Vegetables", "Dairy", "Chicken",
                 "Fish", "Pasta", "Salad"]
            )
            quantity = st.number_input(
                "Quantity", min_value=1, max_value=100
            )
            expiry_date = st.date_input("Expiry Date")
            provider_id = st.number_input(
                "Provider ID", min_value=1
            )
            provider_type = st.selectbox(
                "Provider Type",
                ["Restaurant", "Grocery Store",
                 "Supermarket", "Catering Service"]
            )
            location = st.text_input("Location")
            food_type = st.selectbox(
                "Food Type",
                ["Vegetarian", "Vegan", "Non-Vegetarian"]
            )
            meal_type = st.selectbox(
                "Meal Type",
                ["Breakfast", "Lunch", "Dinner", "Snacks"]
            )
            submitted = st.form_submit_button(
                "Add Food Listing"
            )

            if submitted:
                try:
                    with engine.connect() as conn:
                        provider_exists = conn.execute(
                            text("""
                                SELECT COUNT(*) FROM providers
                                WHERE "Provider_ID" = :id
                            """),
                            {"id": int(provider_id)}
                        ).scalar()

                        if provider_exists == 0:
                            st.error(
                                "Provider ID does not exist."
                            )
                        else:
                            max_id = conn.execute(
                                text(
                                    'SELECT MAX("Food_ID")'
                                    ' FROM food_listings'
                                )
                            ).scalar()
                            new_id = (max_id or 0) + 1
                            conn.execute(
                                text("""
                                    INSERT INTO food_listings
                                    ("Food_ID","Food_Name",
                                     "Quantity","Expiry_Date",
                                     "Provider_ID","Provider_Type",
                                     "Location","Food_Type",
                                     "Meal_Type")
                                    VALUES
                                    (:id,:food_name,:quantity,
                                     :expiry_date,:provider_id,
                                     :provider_type,:location,
                                     :food_type,:meal_type)
                                """),
                                {
                                    "id": new_id,
                                    "food_name": food_name,
                                    "quantity": int(quantity),
                                    "expiry_date": expiry_date,
                                    "provider_id": int(provider_id),
                                    "provider_type": provider_type,
                                    "location": location,
                                    "food_type": food_type,
                                    "meal_type": meal_type
                                }
                            )
                            conn.commit()
                            st.success(
                                f"Food listing '{food_name}' "
                                f"added with ID {new_id}."
                            )
                            st.cache_data.clear()
                            st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

    with add_tab4:
        st.subheader("Add New Claim")

        with st.form("add_claim_form"):
            food_id = st.number_input(
                "Food ID", min_value=1
            )
            receiver_id = st.number_input(
                "Receiver ID", min_value=1
            )
            status = st.selectbox(
                "Status",
                ["Pending", "Completed", "Cancelled"]
            )
            timestamp = st.date_input("Claim Date")
            submitted = st.form_submit_button("Add Claim")

            if submitted:
                try:
                    with engine.connect() as conn:
                        food_exists = conn.execute(
                            text("""
                                SELECT COUNT(*)
                                FROM food_listings
                                WHERE "Food_ID" = :id
                            """),
                            {"id": int(food_id)}
                        ).scalar()

                        receiver_exists = conn.execute(
                            text("""
                                SELECT COUNT(*)
                                FROM receivers
                                WHERE "Receiver_ID" = :id
                            """),
                            {"id": int(receiver_id)}
                        ).scalar()

                        if food_exists == 0:
                            st.error(
                                "Food ID does not exist."
                            )
                        elif receiver_exists == 0:
                            st.error(
                                "Receiver ID does not exist."
                            )
                        else:
                            max_id = conn.execute(
                                text(
                                    'SELECT MAX("Claim_ID")'
                                    ' FROM claims'
                                )
                            ).scalar()
                            new_id = (max_id or 0) + 1
                            conn.execute(
                                text("""
                                    INSERT INTO claims
                                    ("Claim_ID","Food_ID",
                                     "Receiver_ID","Status",
                                     "Timestamp")
                                    VALUES
                                    (:id,:food_id,
                                     :receiver_id,:status,
                                     :timestamp)
                                """),
                                {
                                    "id": new_id,
                                    "food_id": int(food_id),
                                    "receiver_id": int(receiver_id),
                                    "status": status,
                                    "timestamp": timestamp
                                }
                            )
                            conn.commit()
                            st.success(
                                f"Claim added with ID {new_id}."
                            )
                            st.cache_data.clear()
                            st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")


# ============================================
# TAB 2: UPDATE RECORDS
# ============================================

with tab2:
    st.subheader("Update Provider Details")

    with st.form("update_provider_form"):
        update_id = st.number_input(
            "Provider ID to Update", min_value=1
        )
        field_to_update = st.selectbox(
            "Field to Update",
            ["Name", "Type", "City", "Contact"]
        )
        new_value = st.text_input("New Value")
        if field_to_update == "Type":
            new_value = st.selectbox(
                "New Provider Type",
                ["Restaurant", "Grocery Store",
                 "Supermarket", "Catering Service"]
            )
        submitted = st.form_submit_button("Update Provider")

        if submitted:
            if not new_value:
                st.error("New value is required.")
            else:
                try:
                    with engine.connect() as conn:
                        result = conn.execute(
                            text(f"""
                                UPDATE providers
                                SET "{field_to_update}"
                                    = :value
                                WHERE "Provider_ID" = :id
                            """),
                            {
                                "value": new_value,
                                "id": int(update_id)
                            }
                        )
                        conn.commit()
                    if result.rowcount == 0:
                        st.warning(
                            f"No provider found "
                            f"with ID {update_id}."
                        )
                    else:
                        st.success(
                            f"Provider ID {update_id} "
                            f"updated successfully."
                        )
                        st.cache_data.clear()
                        st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")


# ============================================
# TAB 3: DELETE RECORDS
# ============================================

with tab3:
    st.subheader("Delete Food Listing")
    st.warning(
        "This action is permanent and cannot be undone."
    )

    with st.form("delete_food_form"):
        delete_id = st.number_input(
            "Food ID to Delete", min_value=1
        )
        submitted = st.form_submit_button(
            "Delete Food Listing"
        )

        if submitted:
            try:
                with engine.connect() as conn:
                    result = conn.execute(
                        text("""
                            DELETE FROM food_listings
                            WHERE "Food_ID" = :id
                        """),
                        {"id": int(delete_id)}
                    )
                    conn.commit()
                if result.rowcount == 0:
                    st.warning(
                        f"No food listing found "
                        f"with ID {delete_id}."
                    )
                else:
                    st.success(
                        f"Food listing ID {delete_id} "
                        f"deleted successfully."
                    )
                    st.cache_data.clear()
                    st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")