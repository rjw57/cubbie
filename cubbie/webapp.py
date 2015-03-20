"""
WSGI-compatible web application object for cubbie.

"""
from flask import Flask, Blueprint, jsonify, url_for, abort
from flask_jwt import jwt_required, JWT, current_user

from cubbie.model import db, User, Production, Capability
from cubbie.blueprint.identicon import identicon

jwt = JWT()

def create_app(api_url_prefix=''):
    app = Flask(__name__)
    init_app(app, api_url_prefix)
    return app

def init_app(app, api_url_prefix=''):
    db.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(api, url_prefix=api_url_prefix)
    app.register_blueprint(
        identicon, url_prefix=api_url_prefix + '/identicon'
    )

    return app

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

    # Get some image url for the user
    image_url = current_user.image_url
    if image_url is None:
        image_url = url_for('identicon.profile', hash=current_user.id)
    image = dict(url=image_url)

    return jsonify({
        '_type': 'User#profile',
        'displayname': current_user.displayname,
        'productions': productions,
        'image': image,
    })

@api.route('/profile/<int:id>')
def user_info(id):
    abort(400)
#    u = User.query.get(id)
#    if u is None:
#        abort(404)
#
#    # Find productions user is a part of
#    productions_q = Production.query.join(Capability).\
#        filter(Capability.user == u)
#    productions = list(
#        dict(id=p.id)
#        for p in productions_q
#    )
#
#    # Get some image url for the user
#    image_url = current_user.image_url
#    if image_url is None:
#        image_url = url_for('identicon.profile', hash=current_user.id)
#    image = dict(url=image_url)
#
#    return jsonify({
#        '_type': 'User#profile',
#        'displayname': current_user.displayname,
#        'productions': productions,
#        'image': image,
#    })

@api.route('/verify')
@jwt_required()
def verify_token():
    return jsonify(dict(status='ok'))

@api.route('/production/<slug>')
def production(slug):
    p = Production.query.filter(Production.slug == slug).first()
    if p is None:
        abort(404)

    cq = Capability.query.filter(Capability.production == p).\
        join(Production).join(User).\
        with_entities(User.displayname, User.id, Capability.type)

    users = []
    for uname, uid, t in cq:
        users.append(dict(
            displayname=uname, type=t,
            profileUrl=url_for('api.user_info', id=uid)
        ))

    performances = list(dict(
        startsAt=p.starts_at.isoformat(),
        duration=(p.ends_at - p.starts_at).total_seconds(),
        performanceUrl=url_for('api.performance', id=p.id),
        isCancelled=p.is_cancelled
    ) for p in p.performances)

    prod = dict(
        _type='Production#summary', name=p.name,
        users=users, performances=performances
    )

    return jsonify(prod)

@api.route('/performance/<int:id>')
def performance(id):
    abort(400)

@jwt.user_handler
def get_user_from_jwt(payload):
    try:
        u = User.query.get(payload['user'])
    except KeyError:
        abort(401, {'error': 'No user key in JWT payload'})
    if u is None or not u.is_active:
        abort(401, {'error': 'No such user'})
    return u
