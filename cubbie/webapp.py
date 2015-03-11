"""
WSGI-compatible web application object for cubbie.

"""
from flask import (
    Flask, Blueprint, jsonify, render_template, current_app,
    url_for
)
from flask_jwt import jwt_required, JWT, current_user

from cubbie.model import db, User, Production, Capability
from cubbie.signin import gplus

jwt = JWT()

def create_app():
    app = Flask(__name__)
    db.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(ui)
    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(gplus, url_prefix='/signin/gplus')

    return app

ui = Blueprint(
    'ui', __name__, template_folder='ui/templates',
    static_folder='ui/static', static_url_path='/static/ui',
)

@ui.route('/signin')
def index():
    return render_template('signin.html',
        google=dict(
            client_id=current_app.config['GOOGLE_CLIENT_ID'],
            connect_url=url_for('signin.gplus.connect'),
        ),
    )

api = Blueprint('api', __name__)

@api.route('/profile')
@jwt_required()
def profile():
    # Find productions user is a part of
    productions_q = Production.query.join(Capability).\
        filter(Capability.user == current_user)
    productions = list(
        dict(id=p.id)
        for p in productions_q
    )

    return jsonify({
        '_type': 'User#profile',
        'displayname': current_user.displayname,
        'productions': productions,
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
