from db import get_db_connection

def get_all_users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

def get_user_by_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def create_user(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO users (name, email, phone, country) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (data["name"], data["email"], data.get("phone"), data.get("country")))
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return user_id

def update_user(user_id, data):
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "UPDATE users SET name = %s, email = %s, phone = %s, country = %s WHERE id = %s"
    cursor.execute(sql, (data["name"], data["email"], data.get("phone"), data.get("country"), user_id))
    conn.commit()
    conn.close()

def delete_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()
    conn.close()