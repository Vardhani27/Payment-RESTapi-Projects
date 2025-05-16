from flask import Blueprint, request, jsonify
from models.user_model import (
    get_all_users,
    get_user_by_id,
    create_user,
    update_user,
    delete_user
)

user_router = Blueprint('users', __name__)

@user_router.route('/users', methods=['GET'])
def fetch_users():
    """
    Get all users
    ---
    tags:
      - Users
    responses:
      200:
        description: A list of users
    """
    users = get_all_users()
    return jsonify(users), 200

@user_router.route('/users/<int:user_id>', methods=['GET'])
def fetch_user(user_id):
    """
    Get user by ID
    ---
    tags:
      - Users
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: ID of the user to fetch
    responses:
      200:
        description: User found
      404:
        description: User not found
    """
    user = get_user_by_id(user_id)
    if user:
        return jsonify(user), 200
    return jsonify({'error': 'User not found'}), 404

@user_router.route('/users', methods=['POST'])
def add_user():
    """
    Create a new user
    ---
    tags:
      - Users
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            email:
              type: string
            phone:
              type: string
    responses:
      201:
        description: User created
    """
    data = request.get_json()
    if not data.get('name') or not data.get('email'):
        return jsonify({'error': 'Name and email are required'}), 400
    user_id = create_user(data)
    return jsonify({'message': 'User created', 'user_id': user_id}), 201

@user_router.route('/users/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    """
    Update user details
    ---
    tags:
      - Users
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              name:
                type: string
              email:
                type: string
              phone:
                type: string
    responses:
      200:
        description: User updated
      400:
        description: Name and email are required
    """
    data = request.get_json()
    if not data.get('name') or not data.get('email'):
        return jsonify({'error': 'Name and email are required'}), 400
    update_user(user_id, data)
    return jsonify({'message': 'User updated'}), 200

@user_router.route('/users/<int:user_id>', methods=['DELETE'])
def remove_user(user_id):
    """
    Delete a user
    ---
    tags:
      - Users
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: ID of the user to delete
    responses:
      200:
        description: User deleted
    """
    delete_user(user_id)
    return jsonify({'message': 'User deleted'}), 200