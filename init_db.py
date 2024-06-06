from sqlalchemy import create_engine, MetaData
from sqlalchemy_utils import database_exists, create_database
from app.models import _currency
from settings import config

# URL for connecting to Postgres DB with engine.
DB_URL = "postgresql://{user}:{password}@{host}:{port}/{database}".format(
    **config['postgres']
)

if not database_exists(DB_URL):
    create_database(DB_URL)

if database_exists(DB_URL):
    print("DATABASE was created")
else:
    print("DATABASE was not created")

engine = create_engine(DB_URL, isolation_level='AUTOCOMMIT')

meta = MetaData()

# Creates the table (currencies).
meta.create_all(bind=engine, tables=[_currency])
