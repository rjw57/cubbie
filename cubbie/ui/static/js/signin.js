// Signin page support.
//
// The following variables must be defined outside of this script:
//
//  googleConnectUrl

function gapiLoaded() {
    gapi.signin.render('gplusButton');
    document.getElementById('gplusButton').disabled = false;
}

function signinCallback(authResult) {
    var body;

    if(authResult.access_token) {
        // Request our own JWT-based access token.
        body = { access_token: authResult.access_token };
        $.ajax({
            url: googleConnectUrl,
            type: 'POST',
            data: JSON.stringify(body),
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            success: function(response) {
                console.log('resp:', response);
            },
        });
    }
}

