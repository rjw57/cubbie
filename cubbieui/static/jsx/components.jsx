// React components used throughout cubbie

"use strict";

// ClientMixin is a mixin which registers with the dispatcher in order to
// respond to client updates. It calls this.clientDidUpdate to reflect new
// clients when they arrive.
var ClientMixin = {
    getInitialState: function() {
        if(!window.dispatcher) {
            // in the absence of a dispatcher, we can only return the
            // unauthorised client.
            return { client: new cubbie.Client() };
        }

        var self = this, d = window.dispatcher;
        return {
            client: new cubbie.Client(),
            clientMixinDispatcherId: d.register(function(payload) {
                if(!payload.actionType) { return; }
                if(payload.actionType != 'client-update') { return; }
                if(self.clientDidUpdate) {
                    self.clientDidUpdate(payload.client);
                }
            }),
        };
    },
    componentWillUnmount: function() {
        var d = window.dispatcher;
        if(d && this.state.clientMixinDispatcherId) {
            d.unregister(this.state.clientMixinDispatcherId);
        }
    },
};

var Application = React.createClass({
    mixins: [ClientMixin],
    getInitialState: function() {
        return { };
    },
    render: function() {
        var p = this.state.profile;
        return (<div>
            { React.Children.map(this.props.children, function(c) {
                return React.addons.cloneWithProps(c, {
                    profile: p,
                });
            }) }
        </div>);
    },
    clientDidUpdate: function(client) {
        var self = this;

        this.replaceState({ });
        if(client.getIsAuthorized()) {
            client.getProfile().then(function(profile) {
                self.setState({ profile: profile });
            });
        }
    },
});

var Navigation = React.createClass({
    render: function() {
        var p = this.props.profile;
        var userOrSignIn;
        if(p) {
            userOrSignIn = <NavUserDropdown profile={p}/>;
        } else {
            userOrSignIn = <NavSignIn/>;
        }

        return (
<nav className="navbar navbar-default navbar-static-top" role="navigation" style={{marginBottom: 0}}>
    <div className="navbar-header">
        <button type="button" className="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
            <span className="sr-only">Toggle navigation</span>
            <span className="icon-bar"></span>
            <span className="icon-bar"></span>
            <span className="icon-bar"></span>
        </button>
        <a className="navbar-brand" href="{{ url_for('ui.index') }}">Cubbie</a>
    </div>

    <ul className="nav navbar-top-links navbar-right">
        { userOrSignIn }
    </ul>

    { this.props.children }
</nav>
        );
    },
});

var NavUserDropdown = React.createClass({
    render: function() {
        var p = this.props.profile;
        return (
<li className="dropdown">
    <a href="#" className="dropdown-toggle" data-toggle="dropdown"
            role="button" aria-expanded="false">
        <img src={ p.image.url } className="navbar-avatar img-circle" />
        { this.props.profile.displayname }
        <span className="caret"></span>
    </a>
    <ul className="dropdown-menu" role="menu">
        <li><a href="#" onClick={this.signOut}>Sign out</a></li>
    </ul>
</li>
        );
    },
    signOut: function() {
        if(!window.dispatcher) { return; }
        window.dispatcher.dispatch({
            actionType: 'auth-token-update', token: null
        });
    },
});

var NavSignIn = React.createClass({
    render: function() {
        // FIXME: don't hard code URLs
        return <li><a href="/signin">Sign In</a></li>;
    },
});
