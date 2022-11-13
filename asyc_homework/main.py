import asyncio
import more_itertools
from aiohttp import ClientSession
import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String


PG_DSN = 'postgresql+asyncpg://app:1234@127.0.0.1:5435/netology'
engine = create_async_engine(PG_DSN)
Base = declarative_base(bind=engine)
Session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class People(Base):
    __tablename__ = 'people'

    id = Column(Integer, primary_key=True)
    birth_year = Column(String(50))
    eye_color = Column(String(50))
    films = Column(String(1024))
    gender = Column(String(50))
    hair_color = Column(String(50))
    height = Column(Integer)
    homeworld = Column(String(100))
    mass = Column(Integer)
    name = Column(String(50))
    skin_color = Column(String(50))
    species = Column(String(1024))
    starships = Column(String(1024))
    vehicles = Column(String(1024))


CHUNK_SIZE = 10


async def insert(results):
    async with Session() as db_session:
        people = [People(
            birth_year=result.get('birth_year'),
            eye_color=result.get('eye_color'),
            films=result.get('films'),
            gender=result.get('gender'),
            hair_color=result.get('hair_color'),
            height=result.get('height'),
            homeworld=result.get('homeworld'),
            mass=result.get('mass'),
            name=result.get('name'),
            skin_color=result.get('skin_color'),
            species=result.get('species'),
            starships=result.get('starships'),
            vehicles=result.get('vehicles')
        ) for result in results]
        db_session.add_all(people)
    await db_session.commit()


async def foo(tasks_chunk):
    for task in tasks_chunk:
        result = await task
        yield result


async def get_people(people_id, session):
    async with session.get(f'https://swapi.dev/api/people/{people_id}') as response:
        return await response.json()


async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()
    db_tasks = []
    async with ClientSession() as http_session:
        tasks = (asyncio.create_task(get_people(i, http_session)) for i in range(1, 101))
        for tasks_chunk in more_itertools.chunked(tasks, CHUNK_SIZE):
            results = []
            async for result in foo(tasks_chunk):
                results.append(result)
            db_tasks.append(asyncio.create_task(insert(results)))
    for task in db_tasks:
        await task


start = datetime.datetime.now()
asyncio.run(main())
print(datetime.datetime.now() - start)
