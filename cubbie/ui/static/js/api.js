// Cubbie API wrapper

var cubbie = {};

// verifyToken returns a promise which is resolved with a token after it has
// been verified or is rejected if verification fails.
cubbie.verifyToken = function(token) {
    return new Promise(function(resolve, reject) {
        console.log('verifying:', token);

        // Faslsy tokens are never valid
        if(!token) {
            reject(Error('null token'));
            return;
        }

        // TODO: verification
        resolve(token);
    });
}
