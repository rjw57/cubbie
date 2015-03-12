"""
Blueprints supporting various third-party sign in systems.

"""
from apiclient.discovery import build
from apiclient.errors import HttpError
from flask import Blueprint, jsonify, request, current_app
from oauth2client.client import (
    AccessTokenCredentials, FlowExchangeError, AccessTokenRefreshError
)
import httplib2

from cubbie.model import db, User, UserIdentity
from cubbie.auth import make_user_token

# Blueprint supporting sign-in/register with G+.
#
# The basic workflow is that the Javascript in the login form gets a one-time
# auth token from Google and POSTs it to /connect. This code converts the auth
# token to an access token and retrieves the users' basic profile.
#
# If the profile corresponds to a known user, a JWT for the user is returned. If
# the user is previously unknown, a user is created, a JWT returned *and*
# is_new_user is set to true. The calling JavaScript may then work out whether to
# redirect to the profile editing page or to redirect elsewhere.
gplus = Blueprint('signin.gplus', __name__)

GPLUS_SERVICE = build('plus', 'v1')

@gplus.route('/connect', methods=['POST'])
def connect():
    # Get the code from the POST body
    json = request.get_json()
    if json is None or 'access_token' not in json:
        r = jsonify({
            'error': 'no_access_token',
            'message': 'no access_token in body',
        })
        r.status_access_token = 400
        return r
    access_token = json['access_token']

    # Create access token-only credentials
    credentials = AccessTokenCredentials(
        access_token, user_agent=None,
        revoke_uri='https://accounts.google.com/o/oauth2/revoke',
    )

    # Create authorized HTTP client
    http = httplib2.Http()
    http = credentials.authorize(http)

    try:
        # Request basic user info
        req = GPLUS_SERVICE.people().get(userId='me')
        profile = req.execute(http=http)
    finally:
        # Always try to revoke the token
        credentials.revoke(http=http)

    # Extract data of interest
    displayname = profile['displayName']
    image_url = profile.get('image', {}).get('url', None)
    gplus_id = profile['id']

    # Do we have a user with this identity?
    user = User.query.join(UserIdentity).\
        filter(UserIdentity.provider == 'gplus').\
        filter(UserIdentity.provider_user_id == gplus_id).first()

    is_new_user = user == None
    if is_new_user:
        # No, create one
        user = User(displayname=displayname, image_url=image_url)
        db.session.add(user)
        new_user_id = UserIdentity(
            provider='gplus', provider_user_id=gplus_id,
            user=user
        )
        db.session.add(new_user_id, is_active=True)
        db.session.commit()

    # Create a JWT for the user
    token = make_user_token(user)

    return jsonify(dict(
        token=token, is_new_user=is_new_user
    ))
