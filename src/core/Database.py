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

    @property
    def metadata(self):
        return self._Metadata

    def create_db_and_tables(self) -> None:
        Base.metadata.create_all(self._Engine)


def get_session():
    """
    Создает и возвращает фабрику сессий SQLAlchemy, попутно создавая таблицы в базе данных, если они еще не существуют.

    Returns:
        sessionmaker: Фабрика сессий SQLAlchemy.
    """

    # Создаем таблицы, если их еще нет
    Base.metadata.create_all(database.engine)

    # Инициализируем sessionmaker с настроенным движком
    _session = sessionmaker(bind=database.engine, expire_on_commit=False)
    return _session


database = DataBase(config.get("SQLITE_PATH"), echo=True)
