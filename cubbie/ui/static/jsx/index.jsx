var dispatcher = new Flux.Dispatcher();

React.render(
    <AuthorisedPage dispatcher={dispatcher} authTokenKey="cubbieAuthToken">
        <HelloWorld />
    </AuthorisedPage>,
    document.getElementById('page-wrapper')
);
