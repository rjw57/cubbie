"""
UI blueprint for cubbie

The UI for cubbie is broken out into a separate module to make the separation
between UI and API more explicit. It also allows for the static/ and templates/
directories to be directly under the module root rather than buried deep in the
cubbie module itself.

The UI blueprint itself also depends on other blueprints for signin support,
etc. For this reason, apps should use register_with_app() to actually implement
the UI.

"""
from cubbie.webapp import init_app as cubbie_init_app
from flask import Flask, Blueprint, render_template, url_for, current_app
from flask_bower import Bower

from cubbieui.signin import gplus

ui = Blueprint(
    'ui', __name__,
    template_folder='templates/', static_folder='static/',
    static_url_path='/static/ui'
)

@ui.route('/')
def index():
    return render_template('index.html')

@ui.route('/signin')
def signin():
    return render_template(
        'signin.html',
        redirect_url=url_for('ui.index'),
        google=dict(
            # FIXME: client_id should just be retrieved directly from
            # config object
            client_id=current_app.config['GOOGLE_CLIENT_ID'],
            connect_url=url_for('signin.gplus.connect'),
        ),
    )

app = Flask(__name__)
cubbie_init_app(app, api_url_prefix='/api')
bower = Bower(app)

app.register_blueprint(ui)
app.register_blueprint(gplus, url_prefix='/signin/gplus')
