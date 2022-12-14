from sqlalchemy import Column, Integer, String, Date, func
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Ad(Base):

    __tablename__ = 'ad'
    id = Column(Integer, primary_key=True)
    header = Column(String(120), unique=False, nullable=False)
    description = Column(String(500), nullable=False)
    create_date = Column(Date, server_default=func.now())
    owner = Column(String(120), nullable=False)
