from flask import Blueprint, request, jsonify
from models.payment_model import (
    get_all_payments,
    get_payment_by_id,
    create_payment,
    update_payment,
    delete_payment
)
from models.user_model import(get_user_by_id)

router = Blueprint('payments', __name__)

@router.route('/payments', methods=['GET'])
def fetch_payments():
    """
    Get all payments
    ---
    tags:
      - Payments
    responses:
      200:
        description: List of all payments
    """
    payments = get_all_payments()
    return jsonify(payments), 200

@router.route('/payments/<int:payment_id>', methods=['GET'])
def fetch_payment(payment_id):
    """
    Get a payment by ID
    ---
    tags:
      - Payments
    parameters:
      - name: payment_id
        in: path
        type: integer
        required: true
        description: ID of the payment
    responses:
      200:
        description: Payment details
      404:
        description: Payment not found
    """
    payment = get_payment_by_id(payment_id)
    if payment:
        return jsonify(payment), 200
    return jsonify({'error': 'Payment not found'}), 404

@router.route('/payments', methods=['POST'])
def add_payment():
    """
    Create a new payment
    ---
    tags:
      - Payments
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - user_id
            - amount
            - payment_method
            - card_no
          properties:
            user_id:
              type: integer
            amount:
              type: number
            payment_method:
              type: string
            card_no:
              type: number
            card_expiry:
              type: string
              format: date
            card_cvc:
              type: integer
            status:
              type: string
              default: pending
            currency:
              type: string
              default: INR
            description:
              type: string
    responses:
      201:
        description: Payment created
      400:
        description: Missing or invalid required fields
      404:
        description: User not found
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body must be JSON'}), 400

    required_fields = ['user_id', 'amount', 'payment_method', 'card_no']
    missing_fields = [field for field in required_fields if not data.get(field)]
    if missing_fields:
        return jsonify({'error': f"Missing required fields: {', '.join(missing_fields)}"}), 400

    # Optional: Validate user exists
    user = get_user_by_id(data['user_id'])
    if not user:
        return jsonify({'error': 'User ID not found'}), 404

    create_payment(data)
    return jsonify({'message': 'Payment created'}), 201


@router.route('/payments/<int:payment_id>', methods=['PUT'])
def edit_payment(payment_id):
    """
    Update a payment
    ---
    tags:
      - Payments
    parameters:
      - name: payment_id
        in: path
        required: 
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - user_id
            - amount
            - payment_method
            - card_no
          properties:
            user_id:
              type: integer
            amount:
              type: number
            payment_method:
              type: string
            card_no:
              type: string
            card_expiry:
              type: string
              format: date
            card_cvc:
              type: string
            status:
              type: string
              default: pending
            currency:
              type: string
              default: INR
            description:
              type: string
    responses:
      200:
        description: Payment updated
      400:
        description: Missing required fields
    """
    data = request.get_json()
    required_fields = ['user_id', 'amount', 'payment_method', 'card_no']
    if not all(data.get(field) for field in required_fields):
        return jsonify({'error': 'user_id, amount, card number and payment_method are required'}), 400
    try:
        update_payment(payment_id, data)
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    return jsonify({'message': 'Payment updated'}), 200


@router.route('/payments/<int:payment_id>', methods=['DELETE'])
def remove_payment(payment_id):
    """
    Delete a payment
    ---
    tags:
      - Payments
    parameters:
      - name: payment_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Payment deleted
    """
    payment = get_payment_by_id(payment_id)
    if not payment:
        return jsonify({'error': 'User ID not present'}), 404
    
    delete_payment(payment_id)
    return jsonify({'message': 'User deleted'}), 200
