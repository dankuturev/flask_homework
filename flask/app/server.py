import atexit
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker


from admodel import Base


app = Flask('server')

DSN = 'postgresql://app:1234@127.0.0.1:5431/netology'
engine = create_engine(DSN)
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)


def on_exit():
    engine.dispose()


atexit.register(on_exit)

