import json
import unittest

from src.core.Localization import Localization


class TestLocalization(unittest.TestCase):
    """
    Юнит тесты для класса Localization.
    """

    def setUp(self):
        """
        Подготовка к тестам: создание временного файла с JSON данными.
        """
        self.test_file = 'files_for_tests/test_localization.json'
        self.test_data = {'test_key': 'test_value'}
        with open(self.test_file, 'w', encoding='utf-8') as f:
            json.dump(self.test_data, f)
        self.localization = Localization(self.test_file)

    def tearDown(self):
        """
        Завершение тестов: удаление временного файла.
        """
        import os
        os.remove(self.test_file)

    def test_load_json_success(self):
        """
        Тест успешной загрузки JSON данных.
        """
        self.assertEqual(self.localization.local, self.test_data)

    def test_load_json_file_not_found(self):
        """
        Тест обработки исключения FileNotFoundError.
        """
        import os
        os.remove(self.test_file)
        localization = Localization(self.test_file)
        self.assertEqual(localization.local, {})

    def test_load_json_decode_error(self):
        """
        Тест обработки исключения JSONDecodeError.
        """
        with open(self.test_file, 'w', encoding='utf-8') as f:
            f.write('не JSON')
        localization = Localization(self.test_file)
        self.assertEqual(localization.local, {})

    def test_local_property(self):
        """
        Тест свойства local.
        """
        self.assertEqual(self.localization.local, self.test_data)


if __name__ == '__main__':
    unittest.main()
