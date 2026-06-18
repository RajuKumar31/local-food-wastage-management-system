-- ============================================
-- LOCAL FOOD WASTAGE MANAGEMENT SYSTEM
-- SQL Analysis Queries
-- Database: food_wastage_db
-- ============================================

-- ============================================
-- QUERY 1
-- Business Purpose:
-- Measures the total food inventory available on the platform.
-- Helps stakeholders assess overall redistribution capacity
-- and monitor food supply trends over time.
-- ============================================

SELECT
    SUM("Quantity") AS total_food_available
FROM food_listings;

-- ============================================
-- QUERY 2
-- Business Purpose:
-- Identifies the city with the highest number of food listings.
-- In this dataset, location values are synthetically generated and
-- highly dispersed, so the result should be interpreted as a data
-- distribution check rather than a real geographic hotspot analysis.
-- ============================================

SELECT
    "Location",
    COUNT(*) AS total_listings
FROM food_listings
GROUP BY "Location"
ORDER BY total_listings DESC
LIMIT 1;

-- ============================================
-- QUERY 3
-- Business Purpose:
-- Identifies the most commonly available food types on the platform.
-- Helps stakeholders understand the dietary composition of available
-- food inventory and assess whether supply is balanced across food categories.
-- ============================================

SELECT
    "Food_Type",
    COUNT(*) AS total_listings
FROM food_listings
GROUP BY "Food_Type"
ORDER BY total_listings DESC;

-- ============================================
-- QUERY 4
-- Business Purpose:
-- Measures the distribution of claim outcomes on the platform.
-- Helps stakeholders evaluate operational effectiveness by
-- tracking completion, cancellation, and pending claim rates.
-- ============================================

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

-- ============================================
-- QUERY 5
-- Business Purpose:
-- Retrieves provider contact information for a specific city.
-- In a production system, the city would be supplied as a user
-- parameter to help identify potential food donation sources.
-- Note: City values in this dataset are synthetically generated
-- and highly dispersed, so this query primarily demonstrates
-- lookup functionality rather than geographic analysis.
-- ============================================

SELECT
    "Provider_ID",
    "Name",
    "Type",
    "Contact"
FROM providers
WHERE "City" = 'New Carol'
ORDER BY "Name";

-- ============================================
-- QUERY 6
-- Business Purpose:
-- Identifies which provider categories contribute the most food.
-- Helps stakeholders understand where food supply originates
-- and prioritize engagement efforts with high-contributing
-- provider segments.
-- ============================================

SELECT
    p."Type" AS provider_type,
    SUM(f."Quantity") AS total_quantity
FROM food_listings f
JOIN providers p
    ON f."Provider_ID" = p."Provider_ID"
GROUP BY p."Type"
ORDER BY total_quantity DESC;

-- Result: Restaurants contributed the highest total food quantity
-- (6,923 units), followed closely by Supermarkets (6,696 units).
-- Food contributions were relatively balanced across provider
-- categories, indicating that the platform's food supply is not
-- heavily dependent on a single provider segment.

-- ============================================
-- QUERY 7
-- Business Purpose:
-- Identifies the receivers with the highest number of food claims.
-- Helps stakeholders understand platform engagement and identify
-- beneficiaries with the greatest demand for food assistance.
-- Note: This measures claim frequency, not food quantity received.
-- ============================================

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

-- Result: The most active receivers submitted only 4–5 claims each,
-- indicating that claim activity is broadly distributed across the
-- receiver network. No single beneficiary dominates platform usage,
-- suggesting relatively balanced access to food redistribution services.


-- ============================================
-- QUERY 8
-- Business Purpose:
-- Identifies the food items that receive the highest number of claims.
-- Helps stakeholders understand which food categories generate the
-- greatest recipient demand and can inform future donation priorities.
-- ============================================

SELECT
    f."Food_Name",
    COUNT(c."Claim_ID") AS total_claims
FROM claims c
JOIN food_listings f
    ON c."Food_ID" = f."Food_ID"
GROUP BY f."Food_Name"
ORDER BY total_claims DESC
LIMIT 10;

-- Result: Rice received the highest number of claims (122), followed by
-- Soup (114) and Dairy (110), while Fruits received the fewest claims (71).
-- Although all food categories attracted demand, the variation in claim
-- counts suggests that certain food items may be more popular or more
-- frequently requested than others. Stakeholders can use this insight
-- to better align future food donations with recipient demand patterns.


-- ============================================
-- QUERY 9
-- Business Purpose:
-- Identifies which meal types generate the highest claim activity.
-- Helps stakeholders understand recipient demand patterns and
-- determine whether food supply aligns with meal-specific demand.
-- ============================================

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

-- Result: Breakfast generated the highest number of claims
-- (278, 27.8% of all claims), followed by Lunch (250, 25.0%).
-- Demand is relatively balanced across meal categories, but
-- Breakfast shows slightly stronger demand relative to availability.
-- Comparing these results with meal listing counts (254 Breakfast
-- listings vs. 278 claims) suggests that breakfast items are claimed
-- more frequently than other meal types, indicating a potential
-- opportunity to prioritize breakfast donations.


-- ============================================
-- QUERY 10
-- Business Purpose:
-- Identifies the providers contributing the largest quantities of food.
-- Helps stakeholders recognize high-impact donation partners and
-- understand which organizations contribute most to food redistribution.
-- ============================================

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

-- Result: Barry Group (Restaurant) was the highest contributing provider,
-- donating 179 units of food, followed by Evans, Wright and Mitchell
-- (Catering Service) with 158 units. The top 10 contributors span
-- multiple provider categories, suggesting that food donations are
-- distributed across Restaurants, Catering Services, Grocery Stores,
-- and Supermarkets rather than being dominated by a single provider type.
--
-- Barry Group contributed approximately 54% more food than the
-- lowest-ranked provider in the top 10 (179 vs. 116 units),
-- indicating moderate variation in contribution levels among
-- high-performing providers.


-- ============================================
-- QUERY 11
-- Business Purpose:
-- Identifies providers whose donated food results in the greatest
-- number of successful claim completions. Helps stakeholders
-- evaluate which donation partners contribute most effectively
-- to actual food redistribution outcomes.
-- ============================================

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

-- Result: Barry Group (Restaurant) recorded the highest number of
-- successful claims (5), followed by four providers with 4 successful
-- claims each. Successful claim activity is distributed across multiple
-- provider categories, including Restaurants, Catering Services,
-- Grocery Stores, and Supermarkets.
--
-- While Barry Group also ranked as the top provider by total quantity
-- donated (Query 10), the small range of successful claims (3–5 among
-- the top 10 providers) suggests that completed food redistribution is
-- relatively evenly distributed across providers rather than dominated
-- by a single organization.


-- ============================================
-- QUERY 12
-- Business Purpose:
-- Calculates the average quantity of food claimed per receiver.
-- Helps stakeholders identify recipients that typically receive
-- larger food quantities and understand distribution patterns
-- across beneficiary groups.
-- ============================================

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

-- Result: Several receivers recorded an average claimed quantity of
-- 50 units per claim, with the top 10 ranging from 49 to 50 units.
-- The narrow spread among top-ranked receivers suggests that large
-- food quantities are not concentrated among a small group of beneficiaries.
--
-- Because food quantities in the dataset are bounded between 1 and 50,
-- many of the highest averages are likely driven by receivers with only
-- a small number of claims. Therefore, this metric should be interpreted
-- alongside claim frequency (Query 7) to avoid overstating receiver impact.


-- ============================================
-- QUERY 13
-- Business Purpose:
-- Compares the number of food providers and receivers in each city.
-- Helps assess geographic coverage of both supply and demand sides
-- of the platform.
--
-- Note: City values in this dataset are synthetically generated and
-- highly dispersed, so results should be interpreted cautiously.
-- ============================================

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
ORDER BY provider_count DESC, receiver_count DESC;

-- Result: The highest city-level counts were only 2–3 providers and
-- 0–1 receivers per city, reflecting the highly dispersed synthetic
-- geography of the dataset. Most cities contain very few entities,
-- and many appear on only one side of the platform (providers or
-- receivers but not both).
--
-- Because city values are synthetically generated and approximately
-- 96% unique, this query should be interpreted as a data coverage
-- overview rather than evidence of meaningful geographic clusters
-- or operational service areas.