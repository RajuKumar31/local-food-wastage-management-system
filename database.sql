-- ============================================
-- DATABASE CREATION
-- ============================================

CREATE DATABASE food_wastage_db;

-- ============================================
-- PROVIDERS TABLE
-- ============================================

CREATE TABLE providers (
Provider_ID INT PRIMARY KEY,
Name VARCHAR(255),
Type VARCHAR(100),
Address TEXT,
City VARCHAR(100),
Contact VARCHAR(50)
);

-- ============================================
-- RECEIVERS TABLE
-- ============================================

CREATE TABLE receivers (
Receiver_ID INT PRIMARY KEY,
Name VARCHAR(255),
Type VARCHAR(100),
City VARCHAR(100),
Contact VARCHAR(50)
);

-- ============================================
-- FOOD LISTINGS TABLE
-- ============================================

CREATE TABLE food_listings (
Food_ID INT PRIMARY KEY,
Food_Name VARCHAR(255),
Quantity INT,
Expiry_Date DATE,
Provider_ID INT,
Provider_Type VARCHAR(100),
Location VARCHAR(100),
Food_Type VARCHAR(100),
Meal_Type VARCHAR(100),

```
CONSTRAINT fk_food_provider
    FOREIGN KEY (Provider_ID)
    REFERENCES providers (Provider_ID)
```

);

-- ============================================
-- CLAIMS TABLE
-- ============================================

CREATE TABLE claims (
Claim_ID INT PRIMARY KEY,
Food_ID INT,
Receiver_ID INT,
Status VARCHAR(50),
Timestamp TIMESTAMP,

```
CONSTRAINT fk_claim_food
    FOREIGN KEY (Food_ID)
    REFERENCES food_listings (Food_ID),

CONSTRAINT fk_claim_receiver
    FOREIGN KEY (Receiver_ID)
    REFERENCES receivers (Receiver_ID)
```

);
