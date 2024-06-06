from sqlalchemy import create_engine, MetaData
from app.models import _currency

# URL for connecting to Postgres DB with engine.
DB_URL = "postgresql://{user}:{pswrd}@{host}:{port}/{db_name}".format(
    user="postgres", pswrd="admin", host="localhost",
    port="5432", db_name="test_currency"
)

engine = create_engine(DB_URL, isolation_level='AUTOCOMMIT')

meta = MetaData()

# Creates the table (currencies).
meta.create_all(bind=engine, tables=[_currency])
