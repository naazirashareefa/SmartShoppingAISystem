import streamlit as st
from recommend_utils import recommend_products_for_user
import sqlite3
from database_setup import create_tables
from simulator import seed_users, seed_products
import os

BASE_DIR = os.path.dirname(os.path.abspath(file)) 
DB_PATH = os.path.join(BASE_DIR, '..', 'smart_shopping.db')

def get_user_list(): 
    try: 
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT user_id, name FROM Users") 
        users = c.fetchall() 
        return users 
    except sqlite3.Error as e: 
        st.error(f"Database error: {e}") 
        return [] 
    finally: 
        conn.close()

def get_product_details(product_id):
    try: 
        conn = sqlite3.connect(DB_PATH) 
        c = conn.cursor() 
        c.execute("SELECT name, category, price, popularity_score FROM Products WHERE product_id = ?", (product_id,)) 
        row = c.fetchone() 
        return row 
    except sqlite3.Error as e: 
        st.warning(f"Could not fetch product details: {e}") 
        return None 
    finally: 
        conn.close()

def main():
    st.set_page_config(page_title="Smart Shopping AI", page_icon="🛒") 
    st.title("🛒 Smart Shopping - Personalized Recommendations")

    # Ensure DB & Tables exist (optional but useful in the cloud)
    create_tables()
    seed_users()
    seed_products()
    
    users = get_user_list()
    if not users:
        st.warning("No users found in database.")
        return
    
    user_dict = {f"{name} ({uid})": uid for uid, name in users}
    selected_user = st.selectbox("Select a User", list(user_dict.keys()))

    if selected_user:
        uid = user_dict[selected_user]
        st.subheader(f"Recommendations for {selected_user}")
        recs = recommend_products_for_user(uid, top_n=5)
    
        if not recs:
            st.info("No recommendations available.")
            return

        for pid, score in recs:
            details = get_product_details(pid)
            if details:
                name, category, price, pop = details
                st.markdown(f"""
                📦 **{name}**
                - Category: {category}
                - Price: ₹{price:.2f}
                - Popularity Score: {pop}
                - Match Score: {score:.2f}
                ---
                """)

if __name__ == '__main__':
    main()
