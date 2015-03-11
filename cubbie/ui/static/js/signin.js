// Signin page support.
//
// The following variables must be defined outside of this script:
//
//  googleConnectUrl
//  apiProfileUrl

// gapiLoaded is replaced by gapiPromise but it must be present in the global
// namespace.
var gapiWasLoaded = false;
function gapiLoaded() { gapiWasLoaded = true; }

// Again, signinCallback must be in global namespace
var signinCallback;

// We create a promise which is resolved when gapi is loaded and rejected after
// a timeout. This is to allow UI to feed back that Google is having problems
// or that the user us using some "disconnect me"-style extension. Note that we
var gapiPromise = new Promise(function(resolve, reject) {
    // Resolve immediately if gapiLoaded has already been called
    if(gapiWasLoaded) { resolve(); return; }

    // Reject promise after 5 seconds if gapi has not loaded.
    gapiTimeout = setTimeout(function() {
        reject(Error('gapi timed out'));
    }, 5000);

    // On loading gapi, resolve promise and clear the timeout. Note that
    // this function replaces the global namespace one.
    gapiLoaded = function() {
        gapiWasLoaded = true;
        clearTimeout(gapiTimeout);
        resolve();
    }
});

// Convenience function to flag an error to the user
function notifyError(title, message) {
    return $.notify({
        title: '<strong>' + title + '</strong>',
        message: message,
    }, {
        type: 'danger',
        delay: 0,
        allow_dismiss: false,
    });
}

// Give the user a generic error ;->
function ohBugger() {
    notifyError(
        'There was an error signing in.',
        'Please reload the page and try again.'
    );
}

// A promise resolved with an authorization token after signin.
var signinPromise = new Promise(function(resolve, reject) {
    // If there's a token form, it can be used to directly paste in
    // an auth token.
    $('#tokenForm').submit(function() {
        var userData = {
            is_new_user: false,
            token: $('#manualToken').val(),
        };
        resolve(userData);
        return false;
    });

    // replace global signinCallback function
    signinCallback = function(authResult) {
        if(authResult.status && authResult.status.signed_in) {
            // successfully signed in

            // Request our JWT-based access token.
            $.ajax({
                url: googleConnectUrl,
                type: 'POST',
                data: JSON.stringify({
                    access_token: authResult.access_token,
                }),
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                success: function(response) {
                    if(!response.token) {
                        ohBugger();
                        reject(Error('unexpected response when requesting token'));
                        return;
                    }

                    resolve(response);
                },
                error: function(err) {
                    ohBugger();
                    console.error('error getting token:', err);
                    reject(Error('error getting token'));
                },
            });
        } else if(authResult.error === 'immediate_failed') {
            // We don't care if immediate signin failed.
            return;
        } else if(authResult.error === 'access_denied') {
            // User explicitly cancelled sign in, this isn't fatal.
            console.warn('sign in with google was denied by user');
        } else if(authResult.error) {
            // Some other authentication error
            console.error('auth error:', authResult.error);
        } else {
            // WTF is this?
            console.warn('unexpected auth response:', authResult);
        }
    }
});

// Enable sign in with Google button
gapiPromise.then(function() {
    // Render sign-in button
    gapi.signin.render('gplusButton');

    // Enable sign-in button
    $('#gplusButton').prop('disabled', false);
}).catch(function(err) {
    // Notify the user of the error loading gapi.
    console.error(err);
    notifyError(
        'There was a problem with Google signin.',
        'This can happen with third-party "disconnect me"-style extensions.'
    );
});

// After sign in, retrieve user info
signinPromise.then(function(signinResponse) {
    var token = signinResponse.token;

    $.ajax({
        url: apiProfileUrl,
        headers: {
            'Authorization': 'Bearer ' + token,
        },
        dataType: 'json',
        success: function(response) {
            $.notify({
                title: 'Welcome, ' + response.displayname,
                message: '<img src="' + response.image.url + '">',
            }, {
                type: 'success',
                delay: 0,
            });
        },
        error: function(err) {
            console.error('error loading profile', err);
        },
    });
});
