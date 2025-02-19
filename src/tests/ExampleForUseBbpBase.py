from src.core.Config import config
from src.core.Database import database
from src.database.BbpBase import BbpCRUD, BbpUpdateSchema, BbpTableBase


def test():
    """
    engine = database.engine
    db = BbpCRUD(engine=engine)
    После первого старта создаётся файл .env из места запуска модуля
    В этом .env файле

    Configuration file
    SQLITE_PATH=

    в SQLITE_PATH нужно написать SQLITE_PATH=sqlite:///Имя базы данных(путь), можно
    создать в памяти без сохранения в файл, в имя вписать :memory: (SQLITE_PATH=sqlite:///:memory:

    """
    db = BbpCRUD(engine=database.engine)  # создание объекта таблицы
    BbpTableBase.metadata.create_all(database.engine)  # Создание всех таблиц
    # new operation
    create_result = db.create(login="test_login",
                              password="test_password",
                              notes="test_notes")
    print("create result: " + str(create_result))

    # read operation for id
    read_result = db.read(record_id=0)
    print(read_result)

    # read all operation
    read_all_result = db.read_all()
    print(read_all_result)

    # update operation
    model_for_update = BbpUpdateSchema(
        login="test_updated_login",
        password="test_updated_password",
        notes="test_updated_nones"
    )
    update_result = db.update(record_id=0,
                              update_data=model_for_update)
    print(update_result)

    # delete operation
    deleted_result = db.delete(record_id=0)
    print(deleted_result)


test()
