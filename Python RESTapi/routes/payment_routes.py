from flask import Blueprint, request, jsonify
from models.payment_model import (
    get_all_payments,
    get_payment_by_id,
    create_payment,
    update_payment,
    delete_payment
)

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
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - user_id
              - amount
              - payment_method
            properties:
              user_id:
                type: integer
              amount:
                type: number
              payment_method:
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
      201:
        description: Payment created
      400:
        description: Missing required fields
    """
    data = request.get_json()
    required_fields = ['user_id', 'amount', 'payment_method']
    if not all(data.get(field) for field in required_fields):
        return jsonify({'error': 'user_id, amount, and payment_method are required'}), 400
    payment_id = create_payment(data)
    return jsonify({'message': 'Payment created', 'payment_id': payment_id}), 201

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
        type: integer
        required: true
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - user_id
              - amount
              - payment_method
            properties:
              user_id:
                type: integer
              amount:
                type: number
              payment_method:
                type: string
              status:
                type: string
              currency:
                type: string
              description:
                type: string
    responses:
      200:
        description: Payment updated
      400:
        description: Missing required fields
    """

    data = request.get_json()
    required_fields = ['user_id', 'amount', 'payment_method']
    if not all(data.get(field) for field in required_fields):
        return jsonify({'error': 'user_id, amount, and payment_method are required'}), 400
    update_payment(payment_id, data)
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
    delete_payment(payment_id)
    return jsonify({'message': 'Payment deleted'}), 200