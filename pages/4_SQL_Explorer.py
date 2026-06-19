# ============================================
# PAGE 4: SQL EXPLORER
# ============================================

import streamlit as st
import pandas as pd
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
# QUERY RUNNER
# ============================================

@st.cache_data
def run_query(query):

    engine = get_engine()

    return pd.read_sql(
        query,
        engine
    )

# ============================================
# PAGE TITLE
# ============================================

st.title("🗄️ SQL Explorer")

st.markdown("""
Explore all SQL analyses performed on the
Local Food Wastage Management System database.

All results are generated live from PostgreSQL.
""")

# ============================================
# SQL QUERIES
# ============================================

queries = [

    # ========================================
    # LEVEL 1
    # ========================================

    {
        "level": "Level 1 Queries",

        "title":
        "Query 1: Total Quantity of Food Available",

        "question":
        "What is the total quantity of food available from all providers?",

        "sql":
        """
        SELECT
            SUM("Quantity") AS total_food_available
        FROM food_listings;
        """,

        "insight":
        """
        Measures the total food inventory available on the platform.
        Helps stakeholders assess overall redistribution capacity
        and monitor food supply trends over time.
        """
    },

    {
        "level": "Level 1 Queries",

        "title":
        "Query 2: City With Highest Listings",

        "question":
        "Which city has the highest number of food listings?",

        "sql":
        """
        SELECT
            "Location",
            COUNT(*) AS total_listings
        FROM food_listings
        GROUP BY "Location"
        ORDER BY total_listings DESC
        LIMIT 1;
        """,

        "insight":
        """
        Identifies the city with the highest number of food listings.
        Since location values are synthetically generated,
        the result should be interpreted as a data distribution
        check rather than a true hotspot analysis.
        """
    },

    {
        "level": "Level 1 Queries",

        "title":
        "Query 3: Most Common Food Types",

        "question":
        "What are the most commonly available food types?",

        "sql":
        """
        SELECT
            "Food_Type",
            COUNT(*) AS total_listings
        FROM food_listings
        GROUP BY "Food_Type"
        ORDER BY total_listings DESC;
        """,

        "insight":
        """
        Identifies the dietary composition of available food inventory.
        Helps determine whether supply is balanced across food categories.
        """
    },

    {
        "level": "Level 1 Queries",

        "title":
        "Query 4: Claim Status Distribution",

        "question":
        "What percentage of food claims are completed, cancelled, or pending?",

        "sql":
        """
        SELECT
            "Status",
            COUNT(*) AS total_claims,
            ROUND(
                COUNT(*) * 100.0
                / SUM(COUNT(*)) OVER (),
                2
            ) AS percentage_of_claims
        FROM claims
        GROUP BY "Status"
        ORDER BY total_claims DESC;
        """,

        "insight":
        """
        Measures the distribution of claim outcomes.
        Helps stakeholders evaluate operational effectiveness
        by tracking completion, cancellation, and pending rates.
        """
    },

    {
        "level": "Level 1 Queries",

        "title":
        "Query 5: Provider Contact Lookup",

        "question":
        "What is the contact information of providers in a specific city?",

        "sql":
        """
        SELECT
            "Provider_ID",
            "Name",
            "Type",
            "Contact"
        FROM providers
        WHERE "City" = 'New Carol'
        ORDER BY "Name";
        """,

        "insight":
        """
        Demonstrates provider lookup functionality.
        In production, city would be user-selected
        to identify potential food donation sources.
        """
    },
        # ========================================
    # LEVEL 2
    # ========================================

    {
        "level": "Level 2 Queries",

        "title":
        "Query 6: Provider Type Contribution",

        "question":
        "Which type of food provider contributes the most food?",

        "sql":
        """
        SELECT
            p."Type" AS provider_type,
            SUM(f."Quantity") AS total_quantity
        FROM food_listings f
        JOIN providers p
            ON f."Provider_ID" = p."Provider_ID"
        GROUP BY p."Type"
        ORDER BY total_quantity DESC;
        """,

        "insight":
        """
        Restaurants contributed the highest total food quantity,
        followed closely by Supermarkets. Food contributions are
        relatively balanced across provider categories.
        """
    },

    {
        "level": "Level 2 Queries",

        "title":
        "Query 7: Top Receivers by Claims",

        "question":
        "Which receivers have claimed the most food?",

        "sql":
        """
        SELECT
            r."Name",
            r."Type",
            COUNT(c."Claim_ID") AS total_claims
        FROM claims c
        JOIN receivers r
            ON c."Receiver_ID" = r."Receiver_ID"
        GROUP BY
            r."Name",
            r."Type"
        ORDER BY total_claims DESC
        LIMIT 10;
        """,

        "insight":
        """
        The most active receivers submitted only 4–5 claims each,
        indicating that claim activity is broadly distributed across
        the receiver network with no dominant beneficiary.
        """
    },

    {
        "level": "Level 2 Queries",

        "title":
        "Query 8: Claims per Food Item",

        "question":
        "How many food claims have been made for each food item?",

        "sql":
        """
        SELECT
            f."Food_Name",
            COUNT(c."Claim_ID") AS total_claims
        FROM claims c
        JOIN food_listings f
            ON c."Food_ID" = f."Food_ID"
        GROUP BY f."Food_Name"
        ORDER BY total_claims DESC
        LIMIT 10;
        """,

        "insight":
        """
        Rice received the highest number of claims,
        followed by Soup and Dairy. Demand varies across
        food categories despite balanced supply.
        """
    },

    {
        "level": "Level 2 Queries",

        "title":
        "Query 9: Most Claimed Meal Type",

        "question":
        "Which meal type is claimed the most?",

        "sql":
        """
        SELECT
            f."Meal_Type",
            COUNT(c."Claim_ID") AS total_claims,
            ROUND(
                COUNT(c."Claim_ID") * 100.0
                / SUM(COUNT(c."Claim_ID")) OVER (),
                2
            ) AS percentage_of_claims
        FROM claims c
        JOIN food_listings f
            ON c."Food_ID" = f."Food_ID"
        GROUP BY f."Meal_Type"
        ORDER BY total_claims DESC;
        """,

        "insight":
        """
        Breakfast generated the highest number of claims
        and appears to have stronger demand relative
        to availability than other meal categories.
        """
    },

    {
        "level": "Level 2 Queries",

        "title":
        "Query 10: Top Providers by Quantity",

        "question":
        "What is the total quantity of food donated by each provider?",

        "sql":
        """
        SELECT
            p."Name",
            p."Type",
            SUM(f."Quantity") AS total_quantity
        FROM food_listings f
        JOIN providers p
            ON f."Provider_ID" = p."Provider_ID"
        GROUP BY
            p."Name",
            p."Type"
        ORDER BY total_quantity DESC
        LIMIT 10;
        """,

        "insight":
        """
        Barry Group was the highest contributing provider,
        followed by Evans, Wright and Mitchell.
        Contributions are distributed across multiple
        provider categories.
        """
    },
        # ========================================
    # LEVEL 3
    # ========================================

    {
        "level": "Level 3 Queries",

        "title":
        "Query 11: Providers With Most Successful Claims",

        "question":
        "Which provider has had the highest number of successful food claims?",

        "sql":
        """
        SELECT
            p."Name",
            p."Type",
            COUNT(c."Claim_ID") AS successful_claims
        FROM providers p
        JOIN food_listings f
            ON p."Provider_ID" = f."Provider_ID"
        JOIN claims c
            ON f."Food_ID" = c."Food_ID"
        WHERE c."Status" = 'Completed'
        GROUP BY
            p."Name",
            p."Type"
        ORDER BY successful_claims DESC
        LIMIT 10;
        """,

        "insight":
        """
        Barry Group recorded the highest number of successful claims.
        Providers from multiple categories contributed to completed
        food redistribution outcomes.
        """
    },

    {
        "level": "Level 3 Queries",

        "title":
        "Query 12: Average Quantity per Receiver",

        "question":
        "What is the average quantity of food claimed per receiver?",

        "sql":
        """
        SELECT
            r."Name",
            r."Type",
            ROUND(
                AVG(f."Quantity"),
                2
            ) AS avg_quantity_claimed
        FROM receivers r
        JOIN claims c
            ON r."Receiver_ID" = c."Receiver_ID"
        JOIN food_listings f
            ON c."Food_ID" = f."Food_ID"
        GROUP BY
            r."Name",
            r."Type"
        ORDER BY avg_quantity_claimed DESC
        LIMIT 10;
        """,

        "insight":
        """
        Top receivers average between 49 and 50 units per claim.
        This metric should be interpreted alongside claim frequency
        to avoid small-sample bias.
        """
    },

    {
        "level": "Level 3 Queries",

        "title":
        "Query 13: Providers and Receivers by City",

        "question":
        "How many food providers and receivers are there in each city?",

        "sql":
        """
        WITH provider_counts AS (
            SELECT
                "City",
                COUNT(*) AS provider_count
            FROM providers
            GROUP BY "City"
        ),

        receiver_counts AS (
            SELECT
                "City",
                COUNT(*) AS receiver_count
            FROM receivers
            GROUP BY "City"
        )

        SELECT
            COALESCE(p."City", r."City") AS city,
            COALESCE(provider_count, 0) AS provider_count,
            COALESCE(receiver_count, 0) AS receiver_count
        FROM provider_counts p
        FULL OUTER JOIN receiver_counts r
            ON p."City" = r."City"
        ORDER BY provider_count DESC,
                 receiver_count DESC;
        """,

        "insight":
        """
        City-level counts are highly dispersed due to synthetic
        geography. This query is best interpreted as a data
        coverage overview rather than hotspot analysis.
        """
    }

]

# ============================================
# DISPLAY QUERIES
# ============================================

current_level = None

for q in queries:

    if current_level != q["level"]:

        current_level = q["level"]

        st.header(current_level)

    with st.expander(q["title"]):

        st.markdown(
            f"""
            **Business Question**

            {q['question']}
            """
        )

        st.code(
            q["sql"],
            language="sql"
        )

        try:

            result = run_query(
                q["sql"]
            )

            if q["title"] == "Query 13: Providers and Receivers by City":

                st.dataframe(
                    result.head(20),
                    use_container_width=True
                )

                st.caption(
                    "Showing first 20 rows only for performance and readability."
                )

            else:

                st.dataframe(
                    result,
                    use_container_width=True
                )

        except Exception as e:

            st.error(
                f"Error executing query: {e}"
            )

        st.info(
            q["insight"]
        )

# ============================================
# PAGE FOOTER
# ============================================

st.divider()

st.success(
    "All SQL queries are executed live from PostgreSQL."
)