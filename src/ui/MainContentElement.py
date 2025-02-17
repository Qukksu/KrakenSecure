import customtkinter as ctk
import pyperclip  # Для копирования в буфер обмена


class MainContentElement(ctk.CTkFrame):
    """
    Класс для создания плашки с полями для ввода логина, пароля (с возможностью скрытия и копирования) и заметок.
    """

    def __init__(self, parent, *args, **kwargs):
        """
        Инициализация плашки.

        Args:
            parent: Родительский виджет.
            *args: Дополнительные аргументы для ctk.CTkFrame.
            **kwargs: Дополнительные именованные аргументы для ctk.CTkFrame.
        """
        super().__init__(parent, *args, **kwargs)

        self.login_var = ctk.StringVar()
        self.password_var = ctk.StringVar()
        self.notes_var = ctk.StringVar()
        self.password_visible = False
        self.grid_columnconfigure(1, weight=1)  # Растягиваем второй столбец

        # Создание и размещение элементов
        self.create_widgets()

    def create_widgets(self):
        """
        Создает и размещает виджеты в плашке.
        """
        # Метка и поле для логина
        # ctk.CTkLabel(self, text="Логин:").grid(row=0, column=0, sticky=ctk.W, padx=5, pady=5)
        login_entry = ctk.CTkEntry(self, textvariable=self.login_var, placeholder_text="login", width=40)
        login_entry.grid(row=0, column=1, sticky=(ctk.W + ctk.E), padx=5, pady=5)

        # Метка и поле для пароля
        ctk.CTkLabel(self, text="Пароль:").grid(row=1, column=0, sticky=ctk.W, padx=5, pady=5)
        self.password_entry = ctk.CTkEntry(self, textvariable=self.password_var, width=40, show="*")
        self.password_entry.grid(row=1, column=1, sticky=(ctk.W + ctk.E), padx=5, pady=5)

        # Кнопка для отображения/скрытия пароля
        self.toggle_password_button = ctk.CTkButton(self, text="Показать", command=self.toggle_password)
        self.toggle_password_button.grid(row=1, column=2, sticky=ctk.E, padx=5, pady=5)

        # Кнопка для копирования пароля
        copy_password_button = ctk.CTkButton(self, text="Копировать", command=self.copy_password)
        copy_password_button.grid(row=1, column=3, sticky=ctk.E, padx=5, pady=5)

        # Метка и поле для заметок
        ctk.CTkLabel(self, text="Заметки:").grid(row=2, column=0, sticky=ctk.W, padx=5, pady=5)
        notes_entry = ctk.CTkEntry(self, textvariable=self.notes_var, width=40)
        notes_entry.grid(row=2, column=1, sticky=(ctk.W + ctk.E), padx=5, pady=5)

    def toggle_password(self):
        """
        Переключает видимость пароля.
        """
        if self.password_visible:
            self.password_entry.configure(show="*")
            self.toggle_password_button.configure(text="Показать")
            self.password_visible = False
        else:
            self.password_entry.configure(show="")
            self.toggle_password_button.configure(text="Скрыть")
            self.password_visible = True

    def copy_password(self):
        """
        Копирует пароль в буфер обмена.
        """
        password = self.password_var.get()
        if password:
            pyperclip.copy(password)


if __name__ == "__main__":
    app = ctk.CTk()
    app.title("Password Plashka Example")

    # Создание и размещение плашки
    plashka = MainContentElement(app)
    plashka.pack(padx=10, pady=10, fill=ctk.X)

    app.mainloop()
