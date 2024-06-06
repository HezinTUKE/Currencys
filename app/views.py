import os
import json
from datetime import datetime
import ccxt
from ccxt.base.errors import BadSymbol
from aiohttp import web
from .models import insert_table, get_page_rows, clear_history


def find_symbol(responser: dict, symbol):
    """
    Function wich searchs symbol in symbols.txt and returns symbol in short .
    For example: user input Bitcoin - function will return BTC
    """
    if symbol in responser.keys():
        return symbol

    for key, values in responser.items():
        if symbol in values:
            return key

    return symbol


def _to_json(res):
    """
    Function converts list of tuples (fetchall) to json
    """
    data = [dict(i) for i in res]
    final = json.dumps(data, default=str)
    return final


async def get_currency(request):
    """
    Get last price from “kucoin” exchange of the coin (currency argument)
    paired to USDT and save it into database with actual timestamp rounded to
    seconds. In case currency not found, return HTTP 400 error code.
    """
    async with request.app['db'].acquire() as conn:
        currency = request.match_info['currency'].upper()
        kucoin = ccxt.kucoin()

        try:
            txt = os.path.join(os.getcwd(), 'app', 'symbols.txt')

            with open(txt, encoding='utf8') as f:
                symbol_responser_dict = f.read()

            symbol_responser_dict = eval(symbol_responser_dict)
            currency = find_symbol(symbol_responser_dict, currency)
            trades = kucoin.fetch_ticker(f'{currency}/USDT')
            last = trades['last']
            row = {
                'currency': currency,
                'date_': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'price': last
            }

            await insert_table(conn, row)

            return web.json_response({'price': last})
        except BadSymbol:
            return web.HTTPNotFound()
        except web.HTTPException as ex:
            return ex.status


async def get_history(request):
    """
    Gets records from database (paginated) where page size is 10.
    """
    async with request.app['db'].acquire() as conn:
        try:
            page = int(request.rel_url.query['page'])
            res = await get_page_rows(conn, abs(page))
            final = _to_json(res)

            return web.json_response({'records': final})
        except web.HTTPException as ex:
            return ex


async def clear_history_req(request):
    """
    Removes all records in database.
    """
    async with request.app['db'].acquire() as conn:
        try:
            res = await clear_history(conn)
            final = _to_json(res)
            return web.json_response({'removed_ids': final})
        except web.HTTPException as ex:
            return ex
