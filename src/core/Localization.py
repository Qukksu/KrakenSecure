import json

from src.core.Config import config


class Localization:
    """
    Класс для управления локализацией, загружает JSON из файла и предоставляет доступ к данным.

    Attributes:
        __file (str): Путь к файлу JSON.
        localization (dict): Словарь, содержащий данные локализации, загруженные из JSON.
    """

    def __init__(self, path_to_file: str):
        """
        Инициализирует экземпляр класса Localization.

        Args:
            path_to_file (str): Путь к файлу JSON, содержащему данные локализации.
        """
        self.__file = path_to_file
        self.localization = None  # Изначально устанавливаем значение None
        self._load_json()

    def _load_json(self):
        """
        Загружает данные локализации из JSON файла.

        Обрабатывает исключения при открытии и чтении файла,
        а также при разборе JSON.
        """
        try:
            with open(self.__file, 'r', encoding='utf-8') as f:
                self.localization = json.load(f)
        except FileNotFoundError:
            print(f"Ошибка: Файл {self.__file} не найден.")
            with open(self.__file, 'w', encoding='utf-8') as f:
                f.write('')
            self.localization = {}  # Устанавливаем пустой словарь, чтобы избежать ошибок
        except json.JSONDecodeError:
            print(f"Ошибка: Некорректный JSON формат в файле {self.__file}.")
            self.localization = {}  # Устанавливаем пустой словарь, чтобы избежать ошибок
        except Exception as e:
            print(f"Произошла ошибка при загрузке JSON: {e}")
            self.localization = {}

    @property
    def local(self):
        """
        Возвращает словарь с данными локализации.

        Returns:
            dict: Словарь, содержащий данные локализации.
        """
        return self.localization


localization = Localization(config.get("LOCALIZATION_FILE"))
