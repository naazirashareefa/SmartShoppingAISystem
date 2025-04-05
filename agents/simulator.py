from agents import CustomerAgent, ProductAgent, RecommendationAgent 
import sqlite3 
import random 
import time

DB_PATH = 'smart_shopping.db'

def seed_users(): 
    users = [ ('U001', 'Alice', 30, 'F', 'NY', '["Electronics", "Sportswear"]'), ('U002', 'Bob', 25, 'M', 'CA', '["Casual", "Sportswear"]'), ('U003', 'Charlie', 40, 'M', 'TX', '["Electronics"]'), ('U004', 'Diana', 22, 'F', 'FL', '["Casual"]'), ('U005', 'Ethan', 35, 'M', 'WA', '["Sportswear", "Electronics"]') ]
    conn = sqlite3.connect(DB_PATH) 
    c = conn.cursor() 
    c.executemany('INSERT OR IGNORE INTO Users VALUES (?, ?, ?, ?, ?, ?)', users) 
    conn.commit() 
    conn.close() 
    print("✅ Users inserted.")

def seed_products():
    products = [ ('P001', 'Running Shoes', 'Sportswear', 59.99, 10), ('P002', 'Basketball', 'Sportswear', 19.99, 15), ('P003', 'T-shirt', 'Casual', 12.99, 8), ('P004', 'Jeans', 'Casual', 29.99, 12), ('P005', 'Wireless Earbuds', 'Electronics', 49.99, 25), ('P006', 'Laptop Bag', 'Electronics', 34.99, 18), ('P007', 'Smartwatch', 'Electronics', 89.99, 30), ('P008', 'Sports Jacket', 'Sportswear', 39.99, 20), ('P009', 'Graphic Tee', 'Casual', 15.99, 10), ('P010', 'Bluetooth Speaker', 'Electronics', 29.99, 22) ]
    conn = sqlite3.connect(DB_PATH) 
    c = conn.cursor() 
    c.executemany('INSERT OR IGNORE INTO Products VALUES (?, ?, ?, ?, ?)', products) 
    conn.commit()
    conn.close() 
    print("✅ Products inserted.")

def simulate_interactions(): 
    user_ids = ['U001', 'U002', 'U003'] 
    product_ids = ['P001', 'P002', 'P003', 'P004', 'P005', 'P006']
    for _ in range(10):
        uid = random.choice(user_ids)
        pid = random.choice(product_ids)
        action = random.choice(['view', 'purchase'])
        print(f"🔍 Simulating {uid} → {action} → {pid}")
        user = CustomerAgent(uid)
        user.log_action(pid, action)
        prod = ProductAgent(pid)
        prod.update_popularity(1.5 if action == 'purchase' else 0.5)
        time.sleep(0.1)
def test_recommendations(): 
    print("\n💡 Getting recommendations...") 
    for uid in ['U001', 'U002', 'U003']: 
        print(f"\nUser: {uid}") 
        rec = RecommendationAgent(uid) 
        results = rec.recommend() 
        for r in results: 
            print(f" → {r[1]} (Score: {r[2]})")
            rec.close()

if __name__ == "__main__":
    seed_users() 
    seed_products() 
    simulate_interactions()
    test_recommendations()        