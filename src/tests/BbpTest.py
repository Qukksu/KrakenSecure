import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database.BbpBase import BbpTableBase, BbpCRUD, BbpUpdateSchema


class TestBbpCRUD(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Настройка тестовой базы данных
        cls.engine = create_engine('sqlite:///database.db')  # Используем in-memory SQLite для тестов
        cls.Session = sessionmaker(bind=cls.engine)
        cls.crud = BbpCRUD(cls.engine)
        # Создание таблицы для тестирования (необходимо добавить определение BbpTableBase)
        BbpTableBase.metadata.create_all(cls.engine)

    def test_create(self):
        # Тестирование создания записи
        login = 'test_user'
        password = 'secure_password'
        notes = 'Test notes'

        record = self.crud.create(login, password, notes)

        self.assertIsNotNone(record.id)  # Проверяем, что ID был сгенерирован
        self.assertEqual(record.login, login)
        self.assertEqual(record.password, password)
        self.assertEqual(record.notes, notes)

    def test_read(self):
        # Тестирование чтения записи
        login = 'another_user'
        password = 'another_password'
        notes = 'Another test notes'

        created_record = self.crud.create(login, password, notes)

        retrieved_record = self.crud.read(created_record.id)

        self.assertEqual(retrieved_record.id, created_record.id)  # Проверяем, что записи совпадают

    def test_update(self):
        # Тестирование обновления записи
        login = 'update_user'
        password = 'update_password'
        notes = 'Update notes'

        created_record = self.crud.create(login, password, notes)

        update_data = BbpUpdateSchema(login='updated_user', password='new_password', notes='Updated notes')

        updated_record = self.crud.update(created_record.id, update_data)

        self.assertEqual(updated_record.login, update_data.login)  # Проверяем обновленные данные
        self.assertEqual(updated_record.password, update_data.password)
        self.assertEqual(updated_record.notes, update_data.notes)

    def test_delete(self):
        # Тестирование удаления записи
        login = 'delete_user'
        password = 'delete_password'
        notes = 'Delete this note'

        created_record = self.crud.create(login, password, notes)

        result = self.crud.delete(created_record.id)

        self.assertTrue(result)  # Проверяем успешное удаление

        deleted_record = self.crud.read(created_record.id)

        self.assertIsNone(deleted_record)  # Проверяем, что запись больше не существует


if __name__ == '__main__':
    unittest.main()
