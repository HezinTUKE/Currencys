import os
import yaml
import aiopg.sa

BASE_DIR = os.getcwd()
config_path = os.path.join(BASE_DIR, 'configs', 'postgresql.yaml')


def _get_db_config(path):
    """
    Reads data from the configs/postgresql.yaml.
    P.S. Function can be used for other .yaml files.
    """
    with open(path, encoding='utf8') as conf:
        config = yaml.safe_load(conf)
    return config


async def pg_context(app):
    """
    Creates Postgresql engine
    """
    conf = app['config']['postgres']
    engine = await aiopg.sa.create_engine(**conf)
    app['db'] = engine

    yield

    app['db'].close()
    await app['db'].wait_closed()


config = _get_db_config(config_path)
