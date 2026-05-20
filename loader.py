import pandas as pd
import mysql.connector
from mysql.connector import Error
import numpy as np

# MySQL Connection Config
config = {
    'host': 'localhost',
    'user': 'root',  # Change to your MySQL user
    'password': '2028',   # Change to your password
    'database': 'food_delivery_db'
}

try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    print(" Connected to MySQL")
except Error as e:
    print(f" Connection failed: {e}")
    exit()

# Read CSV
df = pd.read_csv('Final_dataset.csv')  # Full path to your CSV
print(f" Connected to CSV: {df.shape[0]} rows, {df.shape[1]} columns")

# Handle missing values
df = df.fillna(0)

# 1. Insert Customers (unique)
customers = df[['Customer_ID', 'Customer_Age', 'Customer_Gender', 'City', 'Area']].drop_duplicates()
print(f"Inserting {len(customers)} customers...")
for idx, row in customers.iterrows():
    try:
        cursor.execute("""
            INSERT IGNORE INTO customers (customer_id, age, gender, city, area)
            VALUES (%s, %s, %s, %s, %s)
        """, (row['Customer_ID'], int(row['Customer_Age']), row['Customer_Gender'], row['City'], row['Area']))
    except Error as e:
        print(f"Error: {e}")

conn.commit()

print("Customers inserted")

# 2. Insert Restaurants (unique)
restaurants = df[['Restaurant_ID', 'Restaurant_Name', 'Cuisine_Type']].drop_duplicates()
print(f"Inserting {len(restaurants)} restaurants...")
for idx, row in restaurants.iterrows():
    try:
        cursor.execute("""
            INSERT IGNORE INTO restaurants (restaurant_id, restaurant_name, cuisine_type)
            VALUES (%s, %s, %s)
        """, (row['Restaurant_ID'], row['Restaurant_Name'], row['Cuisine_Type']))
    except Error as e:
        print(f"Error: {e}")

conn.commit()
print(" Restaurants inserted")

# 3. Insert Orders
print(f"Inserting {len(df)} orders...")
for idx, row in df.iterrows():
    try:
        cursor.execute("""
            INSERT IGNORE INTO orders (order_id, customer_id, restaurant_id, order_date, order_time, 
            order_value, discount_applied, final_amount, payment_mode, order_status, 
            cancellation_reason, order_day, peak_hour, profit_margin, profit_margin_pct, order_value_category)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            row['Order_ID'], row['Customer_ID'], row['Restaurant_ID'],
            pd.to_datetime(row['Order_Date']).date(), row['Order_Time'],
            float(row['Order_Value']), float(row['Discount_Applied']), float(row['Final_Amount']),
            row['Payment_Mode'], row['Order_Status'], row['Cancellation_Reason'],
            row['Order_Day'], bool(row['Peak_Hour']), float(row['Profit_Margin']),
            float(row['Profit_Margin_Pct']), row['Order_Value_Category']
        ))
    except Error as e:
        print(f"Error: {e}")
    
    if (idx + 1) % 10000 == 0:
        print(f"  {idx + 1}/{len(df)} inserted")

conn.commit()
print(" Orders inserted")

# 4. Insert Deliveries
print(f"Inserting {len(df)} deliveries...")
for idx, row in df.iterrows():
    try:
        cursor.execute("""
            INSERT IGNORE INTO deliveries (order_id, delivery_partner_id, delivery_time_min, 
            distance_km, delivery_rating, delivery_performance, restaurant_rating)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            row['Order_ID'], row['Delivery_Partner_ID'], float(row['Delivery_Time_Min']),
            float(row['Distance_km']), int(row['Delivery_Rating']), row['Delivery_Performance'],
            float(row['Restaurant_Rating'])
        ))
    except Error as e:
        print(f"Error: {e}")
    
    if (idx + 1) % 10000 == 0:
        print(f"  {idx + 1}/{len(df)} inserted")

conn.commit()
print(" Deliveries inserted")

# Verify
cursor.execute("SELECT COUNT(*) FROM orders")
order_count = cursor.fetchone()[0]
print(f"\n Total orders in DB: {order_count}")

cursor.close()
conn.close()
print(" Connection closed")
