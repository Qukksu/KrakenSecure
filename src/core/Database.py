from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.core.Config import config
from src.database.Base import Base


class DataBase:
    def __init__(self, database_path, echo=False):
        self._database_path = database_path
        self._Engine = create_engine(database_path, echo=echo)
        self._Async_engine = None
        self._Metadata = MetaData()

    @property
    def engine(self):
        return self._Engine

    async def create_async_engine(self) -> AsyncEngine:
        return create_async_engine(self._database_path, echo=True)

    @property
    async def async_engine(self) -> AsyncEngine:
        if self._Async_engine is None:
            self._Async_engine = await self.create_async_engine()  # Await the engine creation here
        return self._Async_engine

    @property
    def metadata(self):
        return self._Metadata

    def create_db_and_tables(self) -> None:
        Base.metadata.create_all(self._Engine)


async def get_async_session():
    engine = await database.async_engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # Инициализируем async_session только после создания таблиц и получения engine
    _async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    return _async_session


database = DataBase(config.get("SQLITE_PATH"), echo=True)
