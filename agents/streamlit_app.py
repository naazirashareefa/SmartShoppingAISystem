import streamlit as st
from recommend_utils import recommend_products_for_user
import sqlite3

DB_PATH = 'smart_shopping.db'

def get_user_list(): 
    conn = sqlite3.connect(DB_PATH) 
    c = conn.cursor() 
    c.execute("SELECT user_id, name FROM Users")
    users = c.fetchall() 
    conn.close() 
    return users

def get_product_details(product_id):
    conn = sqlite3.connect(DB_PATH) 
    c = conn.cursor()
    c.execute("SELECT name, category, price, popularity_score FROM Products WHERE product_id = ?", (product_id,)) 
    row = c.fetchone() 
    conn.close() 
    return row

def main(): 
    st.title("🛒 Smart Shopping - Personalized Recommendations")
    users = get_user_list()
    user_dict = {f"{name} ({uid})": uid for uid, name in users}
    selected_user = st.selectbox("Select a User", list(user_dict.keys()))

    if selected_user:
        uid = user_dict[selected_user]
        st.subheader(f"Recommendations for {selected_user}")
        recs = recommend_products_for_user(uid, top_n=5)

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