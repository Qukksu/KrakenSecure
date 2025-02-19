# Импортируем необходимые модули и классы
from src.database.Base import Base
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker
from sqlalchemy import String
from typing import Any, Optional, List
from pydantic import BaseModel


# Penis
#fixme: поменяй название класса и таблицы, а то как то не серьезно

class BbpTableBase(Base):
    """
    Класс, представляющий структуру таблицы "bbp" в базе данных.

    Атрибуты:
        __tablename__ (str): Имя таблицы в базе данных.
        id (Mapped[int]): Уникальный идентификатор записи (первичный ключ).
        login (Mapped[str]): Логин пользователя (максимальная длина - 30 символов).
        password (Mapped[str]): Пароль пользователя.
        notes (Mapped[str]): Заметки пользователя.
    """
    __tablename__ = "bbp"  # Указываем имя таблицы в базе данных

    # Определяем столбцы таблицы с помощью Mapped
    id: Mapped[int] = mapped_column(primary_key=True)  # Первичный ключ
    login: Mapped[str] = mapped_column(String(30))  # Логин пользователя (макс. 30 символов)
    password: Mapped[str] = mapped_column(String)  # Пароль пользователя
    notes: Mapped[str] = mapped_column(String)  # Заметки пользователя

    def __repr__(self):
        """
        Возвращает строковое представление объекта BbpTableBase.

        Returns:
            str: Строковое представление объекта в формате "login ; password ; notes".
        """
        return f"{self.login} ; {self.password} ; {self.notes}"


class BbpUpdateSchema(BaseModel):
    """
    Pydantic модель для обновления данных в таблице "bbp".

    Атрибуты:
        login (Optional[str]): Логин для обновления (необязательный).
        password (Optional[str]): Пароль для обновления (необязательный).
        notes (Optional[str]): Заметки для обновления (необязательный).
    """
    login: Optional[str] = None  # Логин для обновления (необязательный)
    password: Optional[str] = None  # Пароль для обновления (необязательный)
    notes: Optional[str] = None  # Заметки для обновления (необязательный)


class BbpCRUD:
    """
    Класс для выполнения CRUD-операций с таблицей "bbp" в базе данных.
    """

    def __init__(self, engine):
        """
        Инициализирует CRUD-операции, создавая сессию подключения к базе данных.

        Args:
            engine: SQLAlchemy engine, представляющий подключение к базе данных.
        """
        self.Session = sessionmaker(bind=engine)  # Создаем сессию для работы с базой данных

    def create(self, login, password, notes):
        """
        Создает новую запись в таблице "bbp".

        Args:
            login (str): Логин пользователя.
            password (str): Пароль пользователя.
            notes (str): Заметки пользователя.

        Returns:
            BbpTableBase: Объект созданной записи.
        """
        with self.Session() as session:
            new_record = BbpTableBase(login=login, password=password, notes=notes)  # Создаем новую запись
            session.add(new_record)  # Добавляем запись в сессию
            session.commit()  # Сохраняем изменения в базе данных
            session.refresh(new_record)  # Обновляем объект, чтобы получить сгенерированный ID
            return new_record

    def read(self, record_id: int):
        """
        Получает запись из таблицы "bbp" по ID.

        Args:
            record_id (int): ID записи для получения.

        Returns:
            BbpTableBase: Объект записи, если найден, иначе None.
        """
        with self.Session() as session:
            return session.get(BbpTableBase, record_id)  # Получаем запись по ID

    def read_all(self):
        """
        Получает все записи из таблицы "bbp".

        Returns:
            List[BbpTableBase]: Список объектов записей.
        """
        with self.Session() as session:
            return session.query(BbpTableBase).all()

    def update(self, record_id: int, update_data: BbpUpdateSchema):
        """
        Обновляет запись в таблице "bbp" по ID, используя Pydantic модель.

        Args:
            record_id (int): ID записи для обновления.
            update_data (BbpUpdateSchema): Pydantic модель с данными для обновления.

        Returns:
            BbpTableBase: Объект обновленной записи, если найден, иначе None.
        """
        with self.Session() as session:
            record = session.get(BbpTableBase, record_id)  # Получаем запись по ID
            if record:
                # Обновляем атрибуты записи данными из Pydantic модели
                for key, value in update_data.model_dump(exclude_unset=True).items():
                    setattr(record, key, value)  # Устанавливаем новое значение атрибута

                session.commit()  # Сохраняем изменения в базе данных
                session.refresh(record)  # Обновляем объект после коммита
                return record
            return None

    def delete(self, record_id: int):
        """
        Удаляет запись из таблицы "bbp" по ID.

        Args:
            record_id (int): ID записи для удаления.

        Returns:
            bool: True, если запись была удалена, иначе False.
        """
        with self.Session() as session:
            record = session.get(BbpTableBase, record_id)  # Получаем запись по ID
            if record:
                session.delete(record)  # Удаляем запись из сессии
                session.commit()  # Сохраняем изменения в базе данных
                return True
            return False

