-- Active: 1762966803547@@127.0.0.1@3306@food_delivery_db
-- Create Customers Table
CREATE TABLE customers (
    customer_id VARCHAR(20) PRIMARY KEY,
    age INT,
    gender VARCHAR(10),
    city VARCHAR(50),
    area VARCHAR(50),
    INDEX idx_city (city),
    INDEX idx_age (age)
);

-- Create Restaurants Table
CREATE TABLE restaurants (
    restaurant_id VARCHAR(20) PRIMARY KEY,
    restaurant_name VARCHAR(100),
    cuisine_type VARCHAR(50),
    INDEX idx_cuisine (cuisine_type)
);

-- Create Orders Table
CREATE TABLE orders (
    order_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20),
    restaurant_id VARCHAR(20),
    order_date DATE,
    order_time TIME,
    order_value DECIMAL(10, 2),
    discount_applied DECIMAL(10, 2),
    final_amount DECIMAL(10, 2),
    payment_mode VARCHAR(20),
    order_status VARCHAR(20),
    cancellation_reason VARCHAR(100),
    order_day VARCHAR(20),
    peak_hour BOOLEAN,
    profit_margin DECIMAL(10, 4),
    profit_margin_pct DECIMAL(10, 2),
    order_value_category VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id),
    INDEX idx_order_date (order_date),
    INDEX idx_customer_id (customer_id),
    INDEX idx_restaurant_id (restaurant_id),
    INDEX idx_status (order_status)
);

-- Create Deliveries Table
CREATE TABLE deliveries (
    order_id VARCHAR(20) PRIMARY KEY,
    delivery_partner_id VARCHAR(20),
    delivery_time_min DECIMAL(10, 2),
    distance_km DECIMAL(10, 2),
    delivery_rating INT,
    delivery_performance VARCHAR(20),
    restaurant_rating DECIMAL(3, 1),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    INDEX idx_delivery_rating (delivery_rating),
    INDEX idx_performance (delivery_performance)
);
