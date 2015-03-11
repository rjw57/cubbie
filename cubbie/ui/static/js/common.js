// Common Javascript for cubbie

// A promise which is resolved with the current user's auth token or rejected
// if there is none.
var authTokenPromise = new Promise(function(resolve, reject) {
    var authToken = window.localStorage.getItem('cubbieAuthToken');

    // TODO: validate auth token

    if(authToken) {
        resolve(authToken);
    } else {
        reject(Error('no auth token'));
    }
});

// A promise which is resolved with the current user's profile or rejected if
// there is no logged in user.
var currentUserPromise = new Promise(function(resolve, response) {
    return authTokenPromise.then(function(authToken) {
        $.ajax({
            url: apiProfileUrl,
            headers: {
                'Authorization': 'Bearer ' + token,
            },
            dataType: 'json',
            success: resolve,
            error: reject,
        });
    });
});
