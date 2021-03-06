
from pydantic import BaseSettings

from starlette.config import Config


config = Config('.env')


class Settings(BaseSettings):

    DEBUG = config('DEBUG', cast=bool, default=False)
    server_host = config('server_host', cast=str, default='127.0.0.1')
    server_port = config('server_port', cast=int, default='8000')
    DATABASE_URL = config('DATABASE_URL', cast=str, default='')

    if DATABASE_URL.startswith('postgresql'):
        ...
    else:
        DATABASE_URL = 'postgresql' + DATABASE_URL[8:]
