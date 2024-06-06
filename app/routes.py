from .views import get_currency, get_history, clear_history_req


def setup_routes(app):
    app.router.add_get('/price/history', get_history)
    app.router.add_delete('/price/history', clear_history_req)
    app.router.add_get('/price/{currency}', get_currency)
