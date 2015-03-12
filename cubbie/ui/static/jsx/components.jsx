// React components used throughout cubbie

"use strict";

var HelloWorld = React.createClass({
    render: function() {
        return (
            <p>Hello, world, {this.props.authToken}</p>
        );
    },
});

// AuthorisedPage is a component which maintains an authorisation token in local
// storage which persists between sessions. The default value is the value from
// local storage. A "null" token corresponds to no user being logged in.
//
// The authorisation token is passed to the children via the authToken prop but
// only after the token is verified.
//
// The key used to set/retrieve the auth token is set via the "authTokenKey"
// prop. The default is "authToken".
//
// The dispatcher prop can be set to a flux-style dispatcher instance. This
// prop will be passed to all children.
//
// AuthorisedPage listens via the dispatcher for a payload with actionType of
// "auth-token-update". The auth token is then set to the value of the "token"
// field in the payload. If "tokenKey" is set in the payload, it must match the
// authTokenKey property before the auth token is updated.
//
// *DO NOT MODIFY THE LOCAL STORAGE DIRECTLY.*
//
// Unknown props are transferred onto the div container wrapping children.
var AuthorisedPage = React.createClass({
    getInitialState: function() {
        var dispatcherId;

        // If there's a global dispatcher, register
        if(this.props.dispatcher) {
            dispatcherId = this.props.dispatcher.register(this.newPayload);
        }

        return { dispatcherId: dispatcherId, verifiedAuthToken: null };
    },
    getDefaultProps: function() {
        return { authTokenKey: 'authToken' };
    },
    render: function() {
        var authToken = this.state.verifiedAuthToken;
        var dispatcher = this.props.dispatcher;
        return (
            <div {...this.props}>
            {React.Children.map(this.props.children, function(child) {
                return React.addons.cloneWithProps(child, {
                    dispatcher: dispatcher, authToken: authToken
                });
            })}
            </div>
        )
    },
    componentWillMount: function() {
        // If there's a token in local storage, verify it
        this.verifyToken(window.localStorage.getItem(this.props.authTokenKey));
    },
    componentWillUnmount: function() {
        // Unregister from the global dispatcher
        if(this.props.dispatcher && this.state.dispatcherId) {
            this.props.dispatcher.unregister(this.state.dispatcherId);
        }
    },
    newPayload: function(payload) {
        // Ignore actions unrelated to us
        if(!payload.actionType || payload.actionType !== 'auth-token-update') {
            return;
        }

        // If there's a tokenKey property, it should match.
        if(payload.tokenKey && payload.tokenKey != this.props.authTokenKey) {
            return;
        }

        // Re-verify token
        this.verifyToken(payload.token);
    },
    verifyToken: function(unverifiedToken) {
        var self = this;
        cubbie.verifyToken(unverifiedToken).then(function(verifiedToken) {
            // Update local storage
            window.localStorage.setItem(self.props.authTokenKey, verifiedToken);

            // Update state
            self.setState({ verifiedAuthToken: verifiedToken });
        }).catch(function(err) {
            console.error('token verification failed:', err);

            // Update state
            self.setState({ verifiedAuthToken: null });
        });
    },
});
