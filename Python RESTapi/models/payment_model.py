from db import get_db_connection

def get_all_payments():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM payments")
    payments = cursor.fetchall()
    conn.close()
    return payments

def get_payment_by_id(payment_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM payments WHERE id = %s", (payment_id,))
    result = cursor.fetchone()
    conn.close()
    return result

def create_payment(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO payments (user_id, amount, status, currency, payment_method, description) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, (
        data["user_id"],
        data["amount"],
        data.get("status", "pending"),
        data.get("currency", "INR"),
        data.get("payment_method"),
        data.get("description")
    ))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id

def update_payment(payment_id, data):
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = """UPDATE payments
             SET user_id = %s, amount = %s, status = %s, currency = %s, payment_method = %s, description = %s
             WHERE id = %s"""
    cursor.execute(sql, (
        data["user_id"],
        data["amount"],
        data.get("status"),
        data.get("currency"),
        data.get("payment_method"),
        data.get("description"),
        payment_id
    ))
    conn.commit()
    conn.close()

def delete_payment(payment_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM payments WHERE id = %s", (payment_id,))
    conn.commit()
    conn.close()