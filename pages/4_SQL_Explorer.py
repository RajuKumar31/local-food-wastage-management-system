# ============================================
# PAGE 4: SQL EXPLORER
# ============================================

import streamlit as st
import pandas as pd

from sqlalchemy import create_engine

# ============================================
# CUSTOM CSS
# ============================================

st.markdown("""
<style>

.main {
    background-color: #F8FAFC;
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

.metric-card {
    background:white;
    padding:20px;
    border-radius:15px;
    text-align:center;
    box-shadow:0px 5px 15px rgba(0,0,0,0.08);
    border-top:5px solid #2563EB;
}

.chart-card {
    background:white;
    padding:20px;
    border-radius:18px;
    box-shadow:0px 8px 20px rgba(0,0,0,0.08);
    margin-bottom:20px;
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
    connection_string,
    pool_pre_ping=True
)

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
# HERO SECTION
# ============================================

st.markdown(
    """
    <div style="
        background: linear-gradient(135deg,#1E3A8A,#2563EB);
        padding:30px;
        border-radius:20px;
        color:white;
        margin-bottom:25px;
    ">

    <h1>🗄️ SQL Explorer</h1>

    <p style="font-size:18px;">
    Execute business-focused SQL analyses directly
    from PostgreSQL and explore platform insights.
    </p>

    </div>
    """,
    unsafe_allow_html=True
)

# ============================================
# KPI SECTION
# ============================================

engine = get_engine()

total_queries = 13

total_providers = pd.read_sql(
    "SELECT COUNT(*) AS count FROM providers",
    engine
).iloc[0,0]

total_receivers = pd.read_sql(
    "SELECT COUNT(*) AS count FROM receivers",
    engine
).iloc[0,0]

total_claims = pd.read_sql(
    "SELECT COUNT(*) AS count FROM claims",
    engine
).iloc[0,0]

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "SQL Queries",
        total_queries
    )

with col2:
    st.metric(
        "Providers",
        f"{total_providers:,}"
    )

with col3:
    st.metric(
        "Receivers",
        f"{total_receivers:,}"
    )

with col4:
    st.metric(
        "Claims",
        f"{total_claims:,}"
    )

st.divider()

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
            SUM(quantity) AS total_food_available
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
            location,
            COUNT(*) AS total_listings
        FROM food_listings
        GROUP BY location
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
            food_type,
            COUNT(*) AS total_listings
        FROM food_listings
        GROUP BY food_type
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
            status,
            COUNT(*) AS total_claims,
            ROUND(
                COUNT(*) * 100.0
                / SUM(COUNT(*)) OVER (),
                2
            ) AS percentage_of_claims
        FROM claims
        GROUP BY status
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
            provider_id,
            name,
            type,
            contact
        FROM providers
        WHERE city = 'New Carol'
        ORDER BY name;
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
            p.type AS provider_type,
            SUM(f.quantity) AS total_quantity
        FROM food_listings f
        JOIN providers p
            ON f.provider_id = p.provider_id
        GROUP BY p.type
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
            r.name,
            r.type,
            COUNT(c.claim_id) AS total_claims
        FROM claims c
        JOIN receivers r
            ON c.receiver_id = r.receiver_id
        GROUP BY
            r.name,
            r.type
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
            f.food_name,
            COUNT(c.claim_id) AS total_claims
        FROM claims c
        JOIN food_listings f
            ON c.food_id = f.food_id
        GROUP BY f.food_name
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
            f.meal_type,
            COUNT(c.claim_id) AS total_claims,
            ROUND(
                COUNT(c.claim_id) * 100.0
                / SUM(COUNT(c.claim_id)) OVER (),
                2
            ) AS percentage_of_claims
        FROM claims c
        JOIN food_listings f
            ON c.food_id = f.food_id
        GROUP BY f.meal_type
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
            p.name,
            p.type,
            SUM(f.quantity) AS total_quantity
        FROM food_listings f
        JOIN providers p
            ON f.provider_id = p.provider_id
        GROUP BY
            p."name",
            p."type"
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
            p.name,
            p.type,
            COUNT(c.claim_id) AS successful_claims
        FROM providers p
        JOIN food_listings f
            ON p.provider_id = f.provider_id
        JOIN claims c
            ON f.food_id = c.food_id
        WHERE c.status = 'Completed'
        GROUP BY
            p.name,
            p.type
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
            r.name,
            r.type,
            ROUND(
                AVG(f.quantity),
                2
            ) AS avg_quantity_claimed
        FROM receivers r
        JOIN claims c
            ON r.receiver_id = c.receiver_id
        JOIN food_listings f
            ON c.food_id = f.food_id
        GROUP BY
            r.name,
            r.type
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
                City,
                COUNT(*) AS provider_count
            FROM providers
            GROUP BY City
        ),

        receiver_counts AS (
            SELECT
                City,
                COUNT(*) AS receiver_count
            FROM receivers
            GROUP BY City
        )

        SELECT
            COALESCE(p.City, r.City) AS city,
            COALESCE(provider_count, 0) AS provider_count,
            COALESCE(receiver_count, 0) AS receiver_count
        FROM provider_counts p
        FULL OUTER JOIN receiver_counts r
            ON p.City = r.City
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
# QUERY SELECTION
# ============================================

st.markdown(
    "## 📋 SQL Query Explorer"
)

query_categories = {

    "Level 1 Queries": [

        q for q in queries

        if q["level"] == "Level 1 Queries"

    ],

    "Level 2 Queries": [

        q for q in queries

        if q["level"] == "Level 2 Queries"

    ],

    "Level 3 Queries": [

        q for q in queries

        if q["level"] == "Level 3 Queries"

    ]

}

selected_category = st.selectbox(
    "Select Query Category",
    list(query_categories.keys())
)

selected_query = st.selectbox(
    "Select SQL Query",
    [
        q["title"]
        for q in query_categories[
            selected_category
        ]
    ]
)

current_query = next(

    q

    for q in query_categories[
        selected_category
    ]

    if q["title"] == selected_query

)

st.divider()

# ============================================
# QUERY INFORMATION CARD
# ============================================

st.markdown(
    f"""
    <div style="
        background:white;
        padding:20px;
        border-radius:15px;
        box-shadow:0px 5px 15px rgba(0,0,0,0.08);
        margin-bottom:20px;
    ">

    <h3>{current_query['title']}</h3>

    <p>
    {current_query['question']}
    </p>

    </div>
    """,
    unsafe_allow_html=True
)

# ============================================
# SHOW SQL CODE
# ============================================

with st.expander(
    "📝 View SQL Query",
    expanded=False
):

    st.code(
        current_query["sql"],
        language="sql"
    )

st.divider()

# ============================================
# RUN QUERY
# ============================================

try:

    result = run_query(
        current_query["sql"]
    )

    st.markdown(
        "## 📊 Query Results"
    )

    col1, col2 = st.columns(
        [3,1]
    )

    with col1:

        st.success(
            f"Returned {len(result):,} rows"
        )

    with col2:

        st.metric(
            "Columns",
            len(result.columns)
        )

    st.dataframe(
        result,
        use_container_width=True,
        height=450
    )

except Exception as e:

    st.error(
        f"Query Failed: {e}"
    )

st.divider()

# ============================================
# RESULT SUMMARY
# ============================================

st.markdown(
    "## 📈 Result Summary"
)

if "result" in locals():

    col1, col2, col3 = st.columns(3)

    with col1:

        st.info(
            f"Rows Returned: {len(result):,}"
        )

    with col2:

        st.info(
            f"Columns: {len(result.columns)}"
        )

    with col3:

        st.info(
            f"Query Level: {current_query['level']}"
        )

st.divider()

# ============================================
# BUSINESS INSIGHTS
# ============================================

st.markdown(
    "## 💡 Business Insights"
)

st.markdown(
    f"""
    <div style="
        background:#DBEAFE;
        padding:20px;
        border-radius:15px;
        border-left:5px solid #2563EB;
        margin-bottom:20px;
    ">

    <h4>Key Insight</h4>

    <p>
    {current_query['insight']}
    </p>

    </div>
    """,
    unsafe_allow_html=True
)

# ============================================
# WHY THIS MATTERS
# ============================================

st.markdown(
    "## 🎯 Why This Analysis Matters"
)

if current_query["level"] == 1:

    st.success(
        """
        Level 1 queries provide foundational
        operational visibility by analyzing
        individual database tables.

        These analyses help monitor inventory,
        providers, receivers and claims.
        """
    )

elif current_query["level"] == 2:

    st.success(
        """
        Level 2 queries combine multiple
        datasets to uncover relationships
        between providers, food listings,
        claims and receivers.

        These analyses support business
        decision making.
        """
    )

else:

    st.success(
        """
        Level 3 queries perform advanced
        business analysis using multi-table
        joins and aggregation logic.

        These insights help evaluate
        redistribution efficiency and
        platform performance.
        """
    )

st.divider()

# ============================================
# SQL SKILLS DEMONSTRATED
# ============================================

st.markdown(
    "## 🚀 SQL Skills Demonstrated"
)

col1, col2, col3 = st.columns(3)

with col1:

    st.info(
        """
        ✅ Aggregations

        SUM()
        COUNT()
        AVG()
        GROUP BY
        """
    )

with col2:

    st.info(
        """
        ✅ Joins

        INNER JOIN
        LEFT JOIN
        FULL OUTER JOIN
        """
    )

with col3:

    st.info(
        """
        ✅ Advanced SQL

        Window Functions

        CTEs

        Business Analytics
        """
    )

st.divider()