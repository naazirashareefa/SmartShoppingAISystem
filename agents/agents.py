import sqlite3 
from datetime import datetime

DB_PATH = 'smart_shopping.db'

class CustomerAgent: 
    def __init__(self, user_id): 
        self.user_id = user_id
    def log_action(self, product_id, action_type):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute(
            '''INSERT INTO UserActions (user_id, product_id, action_type)
            VALUES (?, ?, ?)''',
            (self.user_id, product_id, action_type)
        )
        conn.commit()
        conn.close()
        print(f"[CustomerAgent] Action logged: {action_type} → {product_id}")

    def get_profile(self):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT * FROM Users WHERE user_id = ?", (self.user_id,))
        result = c.fetchone()
        conn.close()
        return result
class ProductAgent: 
    def __init__(self, product_id): 
        self.product_id = product_id
    def get_info(self):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT * FROM Products WHERE product_id = ?", (self.product_id,))
        result = c.fetchone()
        conn.close()
        return result

    def update_popularity(self, increment=1.0):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute(
            '''UPDATE Products
            SET popularity_score = popularity_score + ?
            WHERE product_id = ?''',
            (increment, self.product_id)
        )
        conn.commit()
        conn.close()
        print(f"[ProductAgent] Updated popularity for {self.product_id}")
        
class RecommendationAgent: 
    def __init__(self, user_id): 
        self.user_id = user_id 
        self.conn = sqlite3.connect(DB_PATH) 
        self.c = self.conn.cursor()
    def get_top_categories(self, limit=2):
        self.c.execute(
        '''
        SELECT p.category, COUNT(*) as freq
        FROM UserActions ua
        JOIN Products p ON ua.product_id = p.product_id
        WHERE ua.user_id = ?
        GROUP BY p.category
        ORDER BY freq DESC
        LIMIT ?
        ''',
        (self.user_id, limit)
        )
        return [row[0] for row in self.c.fetchall()]

    def recommend(self, top_n=5):
        top_categories = self.get_top_categories()

        if not top_categories:
            print(f"[RecommendationAgent] No user activity yet. Showing most popular products.")
            self.c.execute(
                '''
                SELECT product_id, name, popularity_score
                FROM Products
                ORDER BY popularity_score DESC
                LIMIT ?
                ''',
                (top_n,)
            )
        else:
            placeholders = ','.join(['?'] * len(top_categories))
            query = f'''
                SELECT product_id, name, popularity_score
                FROM Products
                WHERE category IN ({placeholders})
                ORDER BY popularity_score DESC
                LIMIT ?
            '''
            self.c.execute(query, (*top_categories, top_n))

        results = self.c.fetchall()
        self.log_recommendations(results)
        return results

    def log_recommendations(self, recommendations):
        now = datetime.now().isoformat()
        for product_id, _, score in recommendations:
            self.c.execute(
                '''
                INSERT INTO Recommendations (user_id, product_id, score, recommended_at)
                VALUES (?, ?, ?, ?)
                ''',
                (self.user_id, product_id, score, now)
            )
        self.conn.commit()

    def close(self):
        self.conn.close()
# if __name__ == "__main__": 
#     agent = RecommendationAgent("user123") 
#     recommendations = agent.recommend() 
#     for r in recommendations: 
#         print(r) 
#         agent.close()        
                
            