import datetime
from db import get_db_connection
from utils.crypto_utils import decrypt_card_data, encrypt_card_data, mask_card_number

def get_all_payments():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM payments")
    payments = cursor.fetchall()
    conn.close()
    for payment in payments:
        try:
            decrypted_card_no = decrypt_card_data(payment["card_no"])
            payment["card_no"] = mask_card_number(decrypted_card_no)
        except Exception as e:
            payment["card_no"] = "**** **** **** ****"
        # Always remove CVC from response for security
        payment.pop("card_cvc", None)

    return payments


def get_payment_by_id(payment_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM payments WHERE id = %s", (payment_id,))
    payment = cursor.fetchone()
    conn.close()

    if payment:
        try:
            decrypted_card_no = decrypt_card_data(payment["card_no"])
            payment["card_no"] = mask_card_number(decrypted_card_no)
            payment.pop("card_cvc")  # Don’t return CVC ever
        except Exception as e:
            payment["card_no"] = "**** **** **** ****"
    return payment

def create_payment(data):
    # Validation
    required_fields = ["user_id", "amount", "payment_method", "card_no"]
    for field in required_fields:
        if field not in data or not data[field]:
            raise ValueError(f"{field} is required")

    # Format expiry
    try:
        card_expiry = datetime.datetime.strptime(data["card_expiry"], "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("card_expiry must be in YYYY-MM-DD format")

    # Encryption
    encrypted_card_no = encrypt_card_data(data.get("card_no", ""))
    encrypted_cvc = encrypt_card_data(str(data.get("card_cvc", "")))

    # Insert
    conn = get_db_connection()
    cursor = conn.cursor()
    sql =  """
        INSERT INTO payments (
            user_id, amount, payment_method, status, currency,
            description, card_no, card_expiry, card_cvc
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
    cursor.execute(sql, (
        data['user_id'], 
        data['amount'], 
        data['payment_method'],
        data.get('status', 'pending'), 
        data.get('currency', 'INR'),
        data.get('description'), 
        encrypted_card_no,
        card_expiry,
        encrypted_cvc
    ))
    conn.commit()
    conn.close()

# def update_payment(payment_id, data):
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     sql = """"
#         UPDATE payments SET
#             user_id = %s,
#             amount = %s,
#             payment_method = %s,
#             status = %s,
#             currency = %s,
#             description = %s,
#             card_no = %s,
#             card_expiry = %s,
#             card_cvc = %s
#         WHERE id = %s
#         """
#     cursor.execute(sql, (
#         data['user_id'], 
#         data['amount'], 
#         data['payment_method'],
#         data.get('status', 'pending'), 
#         data.get('currency', 'INR'),
#         data.get('description'), 
#         data.get('card_no'),
#         data.get('card_expiry'), 
#         data.get('card_cvc'),
#         payment_id
#     ))
#     conn.commit()
#     conn.close()

def update_payment(payment_id, data):
    # Validation
    required_fields = ["user_id", "amount", "payment_method", "card_no"]
    for field in required_fields:
        if field not in data or not data[field]:
            raise ValueError(f"{field} is required")

    # Format expiry
    try:
        card_expiry = datetime.datetime.strptime(data["card_expiry"], "%Y-%m-%d").date()
    except (ValueError, KeyError):
        raise ValueError("card_expiry must be in YYYY-MM-DD format")

    # Encryption
    encrypted_card_no = encrypt_card_data(data.get("card_no", ""))
    encrypted_cvc = encrypt_card_data(str(data.get("card_cvc", "")))

    # Update query
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = """
        UPDATE payments
        SET user_id = %s,
            amount = %s,
            payment_method = %s,
            status = %s,
            currency = %s,
            description = %s,
            card_no = %s,
            card_expiry = %s,
            card_cvc = %s
        WHERE payment_id = %s
    """
    cursor.execute(sql, (
        data['user_id'],
        data['amount'],
        data['payment_method'],
        data.get('status', 'pending'),
        data.get('currency', 'INR'),
        data.get('description'),
        encrypted_card_no,
        card_expiry,
        encrypted_cvc,
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