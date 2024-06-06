from aiohttp import web
from app.routes import setup_routes
from app.middlewares import handle_error
from settings import config, pg_context

app = web.Application(
    middlewares=[
        handle_error
    ]
)

app['config'] = config
app.cleanup_ctx.append(pg_context)

setup_routes(app)
web.run_app(app)
