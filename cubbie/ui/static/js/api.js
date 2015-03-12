// Cubbie API wrapper

var cubbie = {
    endpoints: {},  // Set in base.html

    Client: function() {
        this.verifiedToken = null; // initially, clients are unauthenticated
    }
};

// setAndVerifyToken returns a promise which is resolved with the client
// instance if the token has been verified or is rejected if verification fails.
// The auth token used by the client is only updated if verification succeeds.
cubbie.Client.prototype.setAndVerifyToken = function(token) {
    console.log('verifying auth token:', token);

    // Faslsy tokens are never valid
    if(!token) {
        return Promise.reject(Error('null token'));
    }

    // Verify token
    var self = this;
    return this.call(cubbie.endpoints.verifyToken, {
        headers: { 'Authorization': 'Bearer ' + token },
    }).then(function(resp) {
        if(!resp.status || resp.status !== 'ok') {
            return Promise.reject(Error('unexpected verification response'));
        }
        console.log('verification succeeded')
        self.verifiedToken = token;
        return Promise.resolve(self);
    });
};

// clearToken will unset the client's authentication token effectively logging
// out the user.
cubbie.Client.prototype.clearToken = function() {
    this.verifiedToken = null;
};

// call returns a promise which is resolved by the result of the API call or
// rejected with an error if the call fails. If there's a verified token, it
// will be presented as authorisation. The options object may have the following
// fields:
//
//  method: HTTP method to use, defaults to 'get' if no payload or 'post' if
//      there's a payload.
//  payload: Object which is serialised to JSON if non-null. Otherwise no
//      payload is sent.
//  headers: Additional HTTP headers.
cubbie.Client.prototype.call = function(url, options) {
    options = $.extend({
        headers: {},
    }, options);

    var data = options.payload ? JSON.stringify(options.payload) : null;

    // Default method logic
    if(!options.method) {
        options.method = options.payload ? 'post' : 'get';
    }

    // Do we have a token?
    if(this.verifiedToken) {
        options.headers = $.extend({
            'Authorization': 'Bearer ' + this.verifiedToken,
        }, options.headers);
    }

    return new Promise(function(resolve, reject) {
        $.ajax({
            url: url,
            method: options.method,
            data: data,
            contentType: 'application/json',
            headers: options.headers,
            dataType: 'json',
            success: function(resp) {
                resolve(resp);
            },
            error: function(err) {
                reject(err);
            },
        });
    });
};

// getIsAuthorized returns true if the client has a validated authorisation
// token. It returns false otherwise.
cubbie.Client.prototype.getIsAuthorized = function(token) {
    return !!this.verifiedToken;
};

// getProfile returns a promise which is resolved with the user's profile
cubbie.Client.prototype.getProfile = function() {
    return this.call(cubbie.endpoints.profile);
};
