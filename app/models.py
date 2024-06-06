from sqlalchemy import (
    MetaData, Table, Column, Integer,
    Float, DateTime, String
)

meta = MetaData()

_currency = Table(
    'currencies', meta,

    Column('id', Integer, primary_key=True),
    Column('currency', String, nullable=False),
    Column('date_', DateTime, nullable=False),
    Column('price', Float, nullable=False)
)


async def insert_table(conn, args):
    """
    Inserts data to table currencies and returns new id.
    param: args - object of the data -
    {currency : X, data_ : Y, price : Z}.
    """
    res = await conn.execute(
        _currency.insert()
        .values(**args)
        .returning(_currency.c.id))

    return res


async def get_page_rows(conn, page, max_size=10):
    """
    Select data with the shift by max_size (10) * (page - 1).
    param: page - number of the page;
    param: max_size - max size of the page (in our case equals 10).
    """
    res = await conn.execute(
        _currency.select()
        .order_by(_currency.c.date_.desc())
        .offset((page - 1) * max_size)
        .limit(max_size))
    return await res.fetchall()


async def clear_history(conn):
    """
    Removes all data from the table (currencies)
    and returns the list of the deleted id.
    """
    res = await conn.execute(
        _currency.delete()
        .returning(_currency.c.id))

    return await res.fetchall()
