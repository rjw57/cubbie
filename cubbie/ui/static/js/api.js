// Cubbie API wrapper

var cubbie = {
    endpoints: {},  // Set in base.html
};

// verifyToken returns a promise which is resolved with a token after it has
// been verified or is rejected if verification fails.
cubbie.verifyToken = function(token) {
    return new Promise(function(resolve, reject) {
        console.log('verifying auth token:', token);

        // Faslsy tokens are never valid
        if(!token) {
            reject(Error('null token'));
            return;
        }

        // Verify token
        $.ajax({
            url: cubbie.endpoints.verifyToken,
            headers: {
                'Authorization': 'Bearer ' + token,
            },
            dataType: 'json',
            success: function(resp) {
                if(resp.status === 'ok') {
                    console.log('verification succeeded');
                    resolve(token);
                } else {
                    console.error('unexpected response verifying token:', resp);
                    reject(Error('unexpected response from verify endpoint'));
                }
            },
            error: function(err) {
                console.warning('token verification failed:', err);
                reject(Error('token failed verification: ' + err));
            },
        });
    });
}
