-- ============================================
-- DATABASE CREATION
-- ============================================

CREATE DATABASE food_wastage_db;

-- ============================================
-- PROVIDERS TABLE
-- ============================================

CREATE TABLE providers (
    provider_id INT PRIMARY KEY,
    name VARCHAR(255),
    type VARCHAR(100),
    address TEXT,
    city VARCHAR(100),
    contact VARCHAR(50)
);

-- ============================================
-- RECEIVERS TABLE
-- ============================================

CREATE TABLE receivers (
    receiver_id INT PRIMARY KEY,
    name VARCHAR(255),
    type VARCHAR(100),
    city VARCHAR(100),
    contact VARCHAR(50)
);

-- ============================================
-- FOOD LISTINGS TABLE
-- ============================================

CREATE TABLE food_listings (
    food_id INT PRIMARY KEY,
    food_name VARCHAR(255),
    quantity INT,
    expiry_date DATE,
    provider_id INT,
    provider_type VARCHAR(100),
    location VARCHAR(100),
    food_type VARCHAR(100),
    meal_type VARCHAR(100),

    CONSTRAINT fk_food_provider
        FOREIGN KEY (provider_id)
        REFERENCES providers(provider_id)
);

-- ============================================
-- CLAIMS TABLE
-- ============================================

CREATE TABLE claims (
    claim_id INT PRIMARY KEY,
    food_id INT,
    receiver_id INT,
    status VARCHAR(50),
    timestamp TIMESTAMP,

    CONSTRAINT fk_claim_food
        FOREIGN KEY (food_id)
        REFERENCES food_listings(food_id),

    CONSTRAINT fk_claim_receiver
        FOREIGN KEY (receiver_id)
        REFERENCES receivers(receiver_id)
);
