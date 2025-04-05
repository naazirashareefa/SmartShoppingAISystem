import sqlite3 
import numpy as np 
from sklearn.metrics.pairwise import cosine_similarity 
import ast

DB_PATH = 'smart_shopping.db'

def get_all_categories(): 
    conn = sqlite3.connect(DB_PATH) 
    c = conn.cursor() 
    c.execute('SELECT DISTINCT category FROM Products') 
    categories = [row[0] for row in c.fetchall()] 
    conn.close() 
    return categories

def one_hot_encode_category(category, all_categories): 
    vector = [1 if cat == category else 0 for cat in all_categories] 
    return np.array(vector)

def build_product_matrix(): 
    conn = sqlite3.connect(DB_PATH) 
    c = conn.cursor() 
    c.execute('SELECT product_id, category, popularity_score FROM Products') 
    products = c.fetchall() 
    conn.close()
    all_categories = get_all_categories()
    
    matrix = []
    product_ids = []
    for pid, cat, score in products:
        vector = one_hot_encode_category(cat, all_categories)
        matrix.append(vector)
        product_ids.append((pid, score))  # store popularity too

    return np.array(matrix), product_ids, all_categories
def build_user_profile(user_id, all_categories): 
    conn = sqlite3.connect(DB_PATH) 
    c = conn.cursor()
    # Try preferences from profile first
    c.execute('SELECT preferences FROM Users WHERE user_id = ?', (user_id,))
    pref_row = c.fetchone()
    if pref_row and pref_row[0]:
        try:
            prefs = ast.literal_eval(pref_row[0])  # safely convert string list
            user_vector = np.sum([one_hot_encode_category(cat, all_categories) for cat in prefs], axis=0)
            conn.close()
            return user_vector
        except:
            pass  # fallback to interaction-based if preference parsing fails

    # Fallback: infer from user interaction history
    c.execute('''
        SELECT p.category
        FROM UserActions ua
        JOIN Products p ON ua.product_id = p.product_id
        WHERE ua.user_id = ?
    ''', (user_id,))
    categories = [row[0] for row in c.fetchall()]
    conn.close()

    if not categories:
        return np.zeros(len(all_categories))  # no data

    user_vector = np.sum([one_hot_encode_category(cat, all_categories) for cat in categories], axis=0)
    return user_vector
def recommend_products_for_user(user_id, top_n=5): 
    product_matrix, product_ids, all_categories = build_product_matrix() 
    user_vector = build_user_profile(user_id, all_categories)
    similarities = cosine_similarity([user_vector], product_matrix)[0]  # [0] gets the 1D vector

    scored_products = []
    for idx, (pid, popularity) in enumerate(product_ids):
        score = similarities[idx]
        scored_products.append((pid, score))

    # Sort by similarity score descending
    scored_products.sort(key=lambda x: x[1], reverse=True)

    return scored_products[:top_n]
from recommend_utils import recommend_products_for_user

def test_cb_recommendations(): 
    print("\n📘 Content-Based Recommendations") 
    for uid in ['U001', 'U002', 'U003', 'U004', 'U005']: 
        print(f"\nUser: {uid}")
        recs = recommend_products_for_user(uid, top_n=3) 
        for pid, score in recs: 
            print(f" → {pid} (Score: {score:.3f})")

if __name__ == "__main__":

    test_cb_recommendations()

