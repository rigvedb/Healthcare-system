import logging
from flask import request, jsonify, g, Blueprint
from flask_httpauth import HTTPBasicAuth
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from scheduling_app.models import User, db

auth_bp = Blueprint('auth', __name__)
auth = HTTPBasicAuth()
jwt = JWTManager()

# Set up logging
logging.basicConfig(level=logging.DEBUG)

@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        g.user = user
        return True
    return False

@auth_bp.route('/register', methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        logging.debug(f'Register request data: {data}')
        if 'username' not in data or 'password' not in data or 'role' not in data:
            return jsonify({'message': 'Missing username, password, or role'}), 400

        if User.query.filter_by(username=data['username']).first():
            return jsonify({'message': 'User already exists'}), 400

        user = User(username=data['username'], role=data['role'])
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return jsonify({'message': 'Internal server error'}), 500

@auth_bp.route('/login', methods=['POST'])
@auth.login_required
def login_user():
    access_token = create_access_token(identity=g.user.username)
    return jsonify({'token': access_token}), 200

@auth_bp.route('/protected', methods=['GET'])
@jwt_required
def protected():
    return jsonify({'message': f'Welcome {g.user.username}'}), 200