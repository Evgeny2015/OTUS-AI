from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import os

# Initialize Flask app
app = Flask(__name__)

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username}>'

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

# Create database tables
with app.app_context():
    db.create_all()

# User Routes/URLs

@app.route('/api/users', methods=['GET'])
def get_users():
    """Get all users"""
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get a specific user by ID"""
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@app.route('/api/users', methods=['POST'])
def create_user():
    """Create a new user"""
    data = request.get_json()

    # Validate required fields
    if not data or not data.get('username') or not data.get('email'):
        return jsonify({'error': 'Username and email are required'}), 400

    # Check if user already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 409

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 409

    # Create new user
    user = User(
        username=data['username'],
        email=data['email']
    )

    db.session.add(user)
    db.session.commit()

    return jsonify(user.to_dict()), 201

@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update a user"""
    user = User.query.get_or_404(user_id)
    data = request.get_json()

    if 'username' in data:
        # Check if username is already taken by another user
        existing_user = User.query.filter_by(username=data['username']).first()
        if existing_user and existing_user.id != user_id:
            return jsonify({'error': 'Username already exists'}), 409
        user.username = data['username']

    if 'email' in data:
        # Check if email is already taken by another user
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user and existing_user.id != user_id:
            return jsonify({'error': 'Email already exists'}), 409
        user.email = data['email']

    user.updated_at = datetime.utcnow()
    db.session.commit()

    return jsonify(user.to_dict())

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user"""
    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'User deleted successfully'}), 200

@app.route('/')
def index():
    """Root endpoint with API documentation"""
    return jsonify({
        'message': 'Python HTTP Server with User Models',
        'endpoints': {
            'GET /api/users': 'Get all users',
            'GET /api/users/<id>': 'Get user by ID',
            'POST /api/users': 'Create new user',
            'PUT /api/users/<id>': 'Update user',
            'DELETE /api/users/<id>': 'Delete user'
        },
        'example_user': {
            'username': 'john_doe',
            'email': 'john@example.com'
        }
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
