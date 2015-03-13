var dispatcher = new Flux.Dispatcher();

// Register a payload function called when there is a new auth-token payload.
// If attempts to create a new verified client and, if successful, records the
// token in localStorage.
dispatcher.register(function(payload) {
    if(!payload.actionType || payload.actionType !== 'auth-token-update') {
        return;
    }

    if(payload.token) {
        window.localStorage.setItem('cubbieAuthToken', payload.token);
    } else {
        window.localStorage.removeItem('cubbieAuthToken');
    }

    var unAuthClient = new cubbie.Client();

    unAuthClient.setAndVerifyToken(payload.token).then(function(newClient) {
        dispatcher.dispatch({
            actionType: 'client-update', client: newClient
        });
    }, function(err) {
        dispatcher.dispatch({
            actionType: 'client-update', client: unAuthClient
        });
    });
});

// Create top-level application component.
var application = (
    <Application>
        <Navigation>
            <div className="navbar-default sidebar" role="navigation">
                <div className="sidebar-nav navbar-collapse">
                </div>
            </div>
        </Navigation>
        <div id="page-wrapper">
            <div className="row">
                <div className="col-lg-12">
                    <h1 className="page-header">Dashboard</h1>
                </div>
            </div>
        </div>
    </Application>
);

// Render the application.
React.render(application, document.getElementById('wrapper'));

// Send whatever is in local storage as a new auth token.
dispatcher.dispatch({
    actionType: 'auth-token-update',
    token: window.localStorage.getItem('cubbieAuthToken'),
});
