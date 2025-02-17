import customtkinter as ctk
from src.core.Database import database

from src.database.BbpBase import BbpCRUD


class Button_add_password:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.geometry("400x300")
        self.root.title("Add New Password")
        self.create_buttons()

    def create_buttons(self):
        self.login_label = ctk.CTkLabel(self.root, text="Login:")
        self.login_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.login_entry = ctk.CTkEntry(self.root)
        self.login_entry.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        self.password_label = ctk.CTkLabel(self.root, text="Password:")
        self.password_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.password_entry = ctk.CTkEntry(self.root, show="*")  # Для скрытия пароля
        self.password_entry.grid(row=1, column=1, padx=10, pady=10, sticky="e")

        self.notes_label = ctk.CTkLabel(self.root, text="Notes:")
        self.notes_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.notes_entry = ctk.CTkTextbox(self.root, width=200, height=100)
        self.notes_entry.grid(row=2, column=1, padx=10, pady=10, sticky="e")

        self.save_button = ctk.CTkButton(self.root, text="Сохранить", command=self.save_data)
        self.save_button.grid(row=3, column=1, padx=10, pady=10, sticky="e")

    def save_data(self):
        login = self.login_entry.get()
        password = self.password_entry.get()
        notes = self.notes_entry.get("0.0", "end")  # Получаем текст из текстового поля

        bbp = BbpCRUD(database.engine)
        bbp.create(login, password, notes)
