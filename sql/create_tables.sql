-- =============================================
-- Smart Retail Analytics Platform
-- Database: SmartRetailDB
-- =============================================

-- 1. USERS TABLE
CREATE TABLE Users (
    user_id    INT IDENTITY(1,1) PRIMARY KEY,
    full_name  NVARCHAR(100)  NOT NULL,
    email      NVARCHAR(100)  NOT NULL UNIQUE,
    password   NVARCHAR(255)  NOT NULL,   -- bcrypt hashed
    role       NVARCHAR(20)   NOT NULL DEFAULT 'analyst'
                               CHECK (role IN ('admin','analyst','viewer'))
);

-- 2. CUSTOMERS TABLE
CREATE TABLE Customers (
    customer_id           NVARCHAR(50) PRIMARY KEY,
    customer_unique_id    NVARCHAR(50),
    customer_city         NVARCHAR(100),
    customer_state        NVARCHAR(10)
);

-- 3. ORDERS TABLE
CREATE TABLE Orders (
    order_id                    NVARCHAR(50) PRIMARY KEY,
    customer_id                 NVARCHAR(50) REFERENCES Customers(customer_id),
    order_status                NVARCHAR(30),
    order_purchase_timestamp    DATETIME,
    order_delivered_timestamp   DATETIME
);

-- 4. PAYMENTS TABLE
CREATE TABLE Payments (
    payment_id           INT IDENTITY(1,1) PRIMARY KEY,
    order_id             NVARCHAR(50) REFERENCES Orders(order_id),
    payment_type         NVARCHAR(30),
    payment_value        DECIMAL(10,2)
);

-- 5. PRODUCTS TABLE
CREATE TABLE Products (
    product_id              NVARCHAR(50) PRIMARY KEY,
    product_category_name   NVARCHAR(100),
    product_weight_g        DECIMAL(10,2)
);

-- 6. INVENTORY TABLE
CREATE TABLE Inventory (
    inventory_id      INT IDENTITY(1,1) PRIMARY KEY,
    product_id        NVARCHAR(100) NOT NULL,
    product_name      NVARCHAR(150),
    stock_quantity    INT           NOT NULL DEFAULT 0,
    reorder_level     INT           NOT NULL DEFAULT 10,
    unit_price        DECIMAL(10,2) DEFAULT 0
);

-- =============================================
-- SAMPLE DATA
-- =============================================

-- Sample admin user
-- Password is: admin123  (bcrypt hashed)
INSERT INTO Users (full_name, email, password, role)
VALUES (
    'Admin User',
    'admin@smartretail.com',
    '$2b$12$KIXi5I3dJKiMV4oLvDf9xOvP7nIzEq6hVXmKb8R3YtN2wPqLs1Uuy',
    'admin'
);

-- Sample inventory
INSERT INTO Inventory (product_id, product_name, stock_quantity, reorder_level, unit_price)
VALUES
    ('P001', 'Laptop',      5,  10, 55000.00),
    ('P002', 'Mouse',       3,  10,   599.00),
    ('P003', 'Keyboard',    2,  10,  1299.00),
    ('P004', 'Monitor',    18,  10, 12000.00),
    ('P005', 'Headphones', 25,  10,  2500.00);