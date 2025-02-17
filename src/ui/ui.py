import customtkinter as ctk
from src.ui.Button_add_password import Button_add_password
from src.ui.MainContentElement import MainContentElement


class KrakenSecureUI:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.geometry("1000x680")
        self.root.title("KrakenSecure Password Manager")

        # Инициализация стилей
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # Инициализация компонентов
        self.setup_sidebar()
        self.setup_main_content()

    def setup_sidebar(self):
        """Боковая панель с навигацией"""
        self.sidebar = ctk.CTkFrame(self.root, width=200, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")

        # Логотип
        ctk.CTkLabel(
            self.sidebar,
            text="KrakenSecure",
            font=ctk.CTkFont(size=20, weight="bold"),
            anchor="w"
        ).pack(pady=(30, 40), padx=20)

        # Кнопки навигации
        nav_buttons = [
            ("Add Password", self.add_password),
            ("Generate Password", self.generate_password),
            ("Settings", self.open_settings)
        ]

        for text, command in nav_buttons:
            ctk.CTkButton(
                self.sidebar,
                text=text,
                command=command,
                fg_color="transparent",
                border_width=2,
                corner_radius=8,
                anchor="w"
            ).pack(pady=5, padx=10, fill="x")

    def setup_main_content(self):
        """Основная область контента"""
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        element = MainContentElement(self.main_frame)

        element.pack(padx=10, pady=10, fill=ctk.X)
        #
        # # Заголовок
        # ctk.CTkLabel(
        #     self.main_frame,
        #     text="Password Manager Dashboard",
        #     font=ctk.CTkFont(size=24, weight="bold"),
        #     text_color="#2A8CFF"
        # ).pack(pady=30)

    # Методы-заглушки для окон
    def add_password(self):
        Button_add_password()

    def generate_password(self):
        window = ctk.CTkToplevel(self.root)
        window.geometry("400x300")
        window.title("Password Generator")

    def open_settings(self):
        window = ctk.CTkToplevel(self.root)
        window.geometry("400x300")
        window.title("Settings")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = KrakenSecureUI()
    app.run()
