from aiohttp import web


@web.middleware
async def handle_error(request: web.Request, handler):
    try:
        if request.rel_url.query.get('page'):
            """
            Intercepts the parameter: page and checks whether it is
            a number or returns a 500 status code.
            """
            isdigit = request.rel_url.query['page'].replace("-", "").isdigit()
            if not isdigit:
                return web.json_response({'error': 500}, status=500)

        response: web.Response = await handler(request)

        if response.status >= 400:
            return web.json_response({'error': response.status},
                                     status=response.status)

        return response

    except web.HTTPException as ex:
        return web.json_response({'error': ex.status}, status=ex.status)
