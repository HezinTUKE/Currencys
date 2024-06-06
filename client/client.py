import aiohttp
import asyncio

URL_PRICE = "http://127.0.0.1:8080/price/{currency}"
URL_HISTORY_PARAM = "http://127.0.0.1:8080/price/history?page={page}"
URL_HISTORY = "http://127.0.0.1:8080/price/history"


async def fetch_response(session, url):
    async with session.get(url) as res:
        return await res.json(), res.status


async def get_price(currency='QORPO'):
    """
    Calls get method to receive price of the currency.
    """
    async with aiohttp.ClientSession() as session:
        res, status = await fetch_response(session,
                                           URL_PRICE.format(currency=currency))
        return res, status


async def get_history(page=1):
    """
    Calls get method to receive paginated hirstory.
    """
    async with aiohttp.ClientSession() as session:
        res, status = await fetch_response(session,
                                           URL_HISTORY_PARAM.format(page=page))
        return res, status


async def clear_history():
    """
    Call delete method to clear history
    """
    async with aiohttp.ClientSession() as session:
        async with session.delete(URL_HISTORY) as res:
            return await res.json(), res.status


async def multiple_get_price(currency='QORPO'):
    """
    Calls get method to receive multiple prices, in our case - 5.
    """
    url_list = [URL_PRICE.format(currency=currency)] * 5

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_response(session, url) for url in url_list]
        res = await asyncio.gather(*tasks)
        return res

if __name__ == '__main__':
    res, status = asyncio.run(clear_history())

    if status == 200:
        print(res)
    else:
        print(status)

    # res = asyncio.run(multiple_get_price())
    # print(res)
