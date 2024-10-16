from .database import get_connection
import bcrypt
from datetime import datetime

class User:
    @staticmethod
    def create_user(username, email, password):
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
        
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (username, email, password_hash, salt) VALUES (%s, %s, %s, %s)",
            (username, email, password_hash.decode('utf-8'), salt.decode('utf-8'))
        )
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def get_user_by_username(username):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        return user

    @staticmethod
    def verify_password(username, password):
        user = User.get_user_by_username(username)
        if user:
            stored_hash = user[3].encode('utf-8')
            salt = user[4].encode('utf-8')
            return bcrypt.checkpw(password.encode('utf-8'), stored_hash)
        return False

    @staticmethod
    def update_last_login(username):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE users SET last_login = %s WHERE username = %s",
            (datetime.now(), username)
        )
        conn.commit()
        cur.close()
        conn.close()