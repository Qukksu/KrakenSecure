import flet as ft


class PasswordManager:
    def __init__(self, page: ft.Page):
        self.page = page
        self.saved_passwords = []
        self._init_page()
        self._create_ui_elements()
        self._show_login()

    def _init_page(self):
        self.page.title = "KrakenSecure - Менеджер паролей"
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.bgcolor = "#222222"

    def _create_ui_elements(self):
        self.appbar = ft.AppBar(
            leading=ft.Icon(ft.Icons.LOCK_OUTLINE, color=ft.colors.WHITE),
            leading_width=40,
            title=ft.GestureDetector(
                content=ft.Text("KrakenSecure", color=ft.colors.WHITE),
                on_tap=lambda e: self._navigate_to_welcome()
            ),
            center_title=False,
            bgcolor="#333333",
            actions=self._create_appbar_actions()
        )

    def _create_appbar_actions(self):
        return [
            ft.TextButton("Создать", on_click=lambda e: self._navigate_to_create()),
            ft.TextButton("Пароли", on_click=lambda e: self._navigate_to_passwords()),
            ft.PopupMenuButton(
                icon=ft.icons.MORE_VERT,
                items=[
                    ft.PopupMenuItem(text="Настройки", on_click=self._show_temp_message),
                    ft.PopupMenuItem(text="Создатели", on_click=self._show_temp_message),
                ],
                icon_color=ft.colors.WHITE
            )
        ]

    def _navigate(self, content):
        self.page.controls.clear()
        self.page.appbar = self.appbar
        self.page.add(content)
        self.page.update()

    def _show_temp_message(self, e):
        message = "Настройки пока недоступны" if e.control.text == "Настройки" else "Разработано командой гениев"
        self._show_snackbar(message, ft.colors.ORANGE)

    def _show_snackbar(self, message, color=ft.colors.GREEN):
        self.page.snack_bar = ft.SnackBar(ft.Text(message), bgcolor=color)
        self.page.snack_bar.open = True
        self.page.update()

    def _show_login(self):
        password_input = ft.TextField(
            label="Введите пароль",
            password=True,
            width=300,
            border_color="#7C4DFF"
        )
        login_button = ft.ElevatedButton(
            "Войти",
            on_click=lambda e: self._check_password(password_input.value),
            color=ft.colors.WHITE,
            bgcolor="#7C4DFF",
            width=150
        )
        login_content = ft.Column(
            [password_input, login_button],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER
        )
        self._navigate(login_content)

    def _check_password(self, password):
        if password == "1111":
            self._navigate_to_welcome()
        else:
            self._show_snackbar("Неверный пароль!", ft.colors.RED)

    def _navigate_to_welcome(self):
        welcome_content = ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(
                            "Добро пожаловать в менеджер паролей",
                            size=24,
                            color="white"),
                        ft.Text(
                            "KrakenSecure",
                            size=24,
                            color="#7C4DFF"),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER),
                ft.Text(
                    "Управляйте своими паролями легко и безопасно.",
                    size=16,
                    color="white",
                    text_align=ft.TextAlign.CENTER),
            ],
            spacing=15,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER)
        self._navigate(welcome_content)

    def _navigate_to_create(self):
        fields = {
            "Логин": ft.TextField(
                label="Логин",
                width=300,
                border_color="#7C4DFF"),
            "Пароль": ft.TextField(
                label="Пароль",
                password=True,
                width=300,
                border_color="#7C4DFF"),
            "Заметка": ft.TextField(
                label="Заметка (необязательно)",
                width=300,
                border_color="#7C4DFF")}

        save_button = ft.ElevatedButton(
            "Сохранить",
            on_click=lambda e: self._save_record(fields),
            color=ft.colors.WHITE,
            bgcolor="#7C4DFF",
            width=150
        )

        form_content = ft.Column(
            [
                ft.Text(
                    "Создание записи",
                    size=20,
                    color="white",
                    text_align=ft.TextAlign.CENTER),
                *fields.values(),
                ft.Container(
                    save_button,
                    alignment=ft.alignment.center)],
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            width=400)
        self._navigate(form_content)

    def _save_record(self, fields):
        if not all([fields["Логин"].value, fields["Пароль"].value]):
            self._show_snackbar("Логин и пароль обязательны!", ft.colors.RED)
            return

        record = {
            "login": fields["Логин"].value,
            "password": fields["Пароль"].value,
            "note": fields["Заметка"].value or ""
        }

        encrypted_record = self.core.encrypt_data(record)
        self.saved_passwords.append(record)
        self._save_to_file(encrypted_record)
        self._show_snackbar("Запись успешно сохранена!")
        self._navigate_to_passwords()
    def _navigate_to_passwords(self):
        content = ft.ListView(
            controls=[
                ft.Text("Сохраненные пароли",
                        size=20,
                        color="white",
                        text_align=ft.TextAlign.CENTER)
            ],
            spacing=15,
            width=600,
            height=400,
            auto_scroll=True
        )

        if not self.saved_passwords:
            content.controls.append(
                ft.Text("У вас пока нет сохраненных паролей.",
                        size=16,
                        color="white",
                        text_align=ft.TextAlign.CENTER)
            )
        else:
            content.controls.extend(
                self._create_password_card(record, index)
                for index, record in enumerate(self.saved_passwords)
            )

        self._navigate(content)

    def _create_password_card(self, record, index):
        return ft.Container(
            content=ft.Column([
                self._create_row("Логин", record['login'], True),
                self._create_row("Пароль", '●' * len(record['password']), True),
                self._create_note_row(record, index)
            ], spacing=12),
            padding=15,
            border_radius=10,
            bgcolor="#333333",
            margin=ft.margin.symmetric(vertical=5),
            width=550
        )

    def _create_row(self, label, value, copyable=False):
        return ft.Row(
            [
                ft.Text(
                    f"{label}:",
                    size=16,
                    color="white",
                    width=80),
                ft.Text(
                    value,
                    size=16,
                    color="white",
                    expand=True),
                ft.Container(
                    self._create_copy_button(value) if copyable else ft.Container(),
                    alignment=ft.alignment.center_right,
                    expand=True)],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            width=500)

    def _create_note_row(self, record, index):
        return ft.Row(
            [
                ft.Text("Заметка:", size=16, color="white", width=80),
                ft.Text(record['note'] or "-",
                        size=16,
                        color="white",
                        expand=True,
                        overflow=ft.TextOverflow.ELLIPSIS),
                ft.Container(
                    ft.IconButton(
                        icon=ft.icons.DELETE_FOREVER,
                        on_click=lambda e, idx=index: self._delete_record(idx),
                        tooltip="Удалить запись",
                        icon_color=ft.colors.RED
                    ),
                    alignment=ft.alignment.center_right,
                    expand=True
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            width=500
        )

    def _create_copy_button(self, value):
        return ft.IconButton(
            icon=ft.icons.CONTENT_COPY,
            on_click=lambda e: self._copy_to_clipboard(value),
            tooltip=f"Копировать {value}",
            icon_color=ft.colors.WHITE,
            bgcolor="#7C4DFF",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5))
        )

    def _copy_to_clipboard(self, value):
        self.page.set_clipboard(value)
        self._show_snackbar(f"Скопировано: {value.split(': ')[0]}")

    def _delete_record(self, index):
        del self.saved_passwords[index]
        self._navigate_to_passwords()


def main(page: ft.Page):
    PasswordManager(page)


ft.app(target=main)
