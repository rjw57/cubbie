"""
WSGI-compatible web application object for cubbie.

"""
from flask import Flask, Blueprint, jsonify
from flask_jwt import jwt_required, JWT, current_user

from cubbie.model import db, User

jwt = JWT()

def create_app():
    app = Flask(__name__)
    db.init_app(app)
    jwt.init_app(app)
    app.register_blueprint(api, url_prefix='/api')
    return app

api = Blueprint('api', __name__)

@api.route('/profile')
@jwt_required()
def profile():
    return jsonify({
        '_type': 'User#profile',
        'displayname': current_user.displayname,
    })

@jwt.user_handler
def get_user_from_jwt(payload):
    try:
        u = User.query.get(payload['user'])
    except KeyError:
        abort(400, {'error': 'No user key in JWT payload'})
    if u is None:
        abort(400, {'error': 'No such user'})
    return u
