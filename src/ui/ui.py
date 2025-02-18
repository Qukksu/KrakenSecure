import flet as ft

def main(page: ft.Page):
    page.title = "Менеджер паролей"
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.bgcolor = "#222222"

    saved_passwords = []

    # Функции для меню
    def open_settings(e):
        page.snack_bar = ft.SnackBar(ft.Text("Настройки пока недоступны"), bgcolor=ft.colors.ORANGE)
        page.snack_bar.open = True
        page.update()

    def open_creators(e):
        page.snack_bar = ft.SnackBar(ft.Text("Разработано командой гениев"), bgcolor=ft.colors.ORANGE)
        page.snack_bar.open = True
        page.update()

    appbar = ft.AppBar(
        leading=ft.Icon(ft.Icons.LOCK_OUTLINE, color=ft.colors.WHITE),
        leading_width=40,
        title=ft.Text("Менеджер паролей", color=ft.colors.WHITE),
        center_title=False,
        bgcolor="#333333",
        actions=[
            ft.TextButton(
                content=ft.Text("Создать", color=ft.colors.WHITE),
                on_click=lambda e: open_create_password()
            ),
            ft.TextButton(
                content=ft.Text("Пароли", color=ft.colors.WHITE),
                on_click=lambda e: open_saved_passwords()
            ),
            ft.PopupMenuButton(
                icon=ft.icons.MORE_VERT,
                tooltip="Дополнительно",
                items=[
                    ft.PopupMenuItem(text="Настройки", on_click=open_settings),
                    ft.PopupMenuItem(text="Создатели", on_click=open_creators),
                ],
                icon_color=ft.colors.WHITE
            )
        ],
    )

    # Остальной код без изменений
    password_input = ft.TextField(label="Введите пароль", password=True, width=300)

    def check_password(e):
        if password_input.value == "1111":
            page.controls.clear()
            page.appbar = appbar
            show_welcome_page()
            page.update()
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Неверный пароль!"), bgcolor=ft.colors.RED)
            page.snack_bar.open = True
            page.update()

    login_button = ft.ElevatedButton(
        text="Войти",
        on_click=check_password,
        color=ft.colors.WHITE,
        bgcolor="#7C4DFF",
    )

    login_content = ft.Column(
        [password_input, login_button],
        horizontal_alignment="center",
        spacing=20,
    )

    def show_welcome_page():
        welcome_content = ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("Добро пожаловать в менеджер паролей", size=24, color="white"),
                        ft.Text("KrakenSecure", size=24, color="#7C4DFF"),
                    ],
                    alignment="center",
                ),
                ft.Text("Управляйте своими паролями легко и безопасно.", size=16, color="white"),
            ],
            horizontal_alignment="center",
            spacing=10,
        )
        page.add(welcome_content)
        page.update()

    def open_create_password():
        page.controls.clear()
        page.appbar = appbar

        login_field = ft.TextField(label="Логин", width=300)
        password_field = ft.TextField(label="Пароль", password=True, width=300)
        note_field = ft.TextField(label="Заметка (необязательно)", width=300)

        def save_record(e):
            if login_field.value and password_field.value:
                saved_passwords.append({
                    "login": login_field.value,
                    "password": password_field.value,
                    "note": note_field.value,
                })
                page.snack_bar = ft.SnackBar(ft.Text("Запись успешно сохранена!"), bgcolor=ft.colors.GREEN)
                page.snack_bar.open = True
                open_saved_passwords()
                page.update()
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Логин и пароль обязательны!"), bgcolor=ft.colors.RED)
                page.snack_bar.open = True
                page.update()

        save_button = ft.ElevatedButton(text="Сохранить", on_click=save_record)

        create_password_content = ft.Column(
            [
                ft.Text("Создание записи", size=20, color="white"),
                login_field,
                password_field,
                note_field,
                save_button,
            ],
            horizontal_alignment="center",
            spacing=20,
        )

        page.add(create_password_content)
        page.update()

    def copy_to_clipboard(value):
        page.set_clipboard(value)
        page.snack_bar = ft.SnackBar(ft.Text(f"Скопировано: {value}"), bgcolor=ft.colors.GREEN)
        page.snack_bar.open = True
        page.update()

    def open_saved_passwords():
        page.controls.clear()
        page.appbar = appbar

        if not saved_passwords:
            saved_passwords_content = ft.Column(
                [
                    ft.Text("Сохраненные пароли", size=20, color="white"),
                    ft.Text("У вас пока нет сохраненных паролей.", size=16, color="white"),
                ],
                horizontal_alignment="center",
                spacing=10,
            )
        else:
            saved_passwords_list = []
            for index, record in enumerate(saved_passwords):
                def delete_record(e, idx):
                    del saved_passwords[idx]
                    open_saved_passwords()
                    page.update()

                card_content = ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Text(f"Логин: {record['login']}", size=16, color="white"),
                                    ft.IconButton(
                                        icon=ft.icons.CONTENT_COPY,
                                        on_click=lambda e, login=record['login']: copy_to_clipboard(login),
                                        tooltip="Копировать логин",
                                        style=ft.ButtonStyle(color=ft.colors.WHITE)
                                    ),
                                ],
                                alignment="spaceBetween",
                            ),
                            ft.Row(
                                [
                                    ft.Text(f"Пароль: {'●' * len(record['password'])}", size=16, color="white"),
                                    ft.IconButton(
                                        icon=ft.icons.CONTENT_COPY,
                                        on_click=lambda e, password=record['password']: copy_to_clipboard(password),
                                        tooltip="Копировать пароль",
                                        style=ft.ButtonStyle(color=ft.colors.WHITE)
                                    ),
                                ],
                                alignment="spaceBetween",
                            ),
                            ft.Row(
                                [
                                    ft.Text(f"Заметка: {record['note']}" if record['note'] else "Без заметки", color="white"),
                                    ft.IconButton(
                                        icon=ft.icons.DELETE_FOREVER,
                                        on_click=lambda e, idx=index: delete_record(e, idx),
                                        tooltip="Удалить запись",
                                        style=ft.ButtonStyle(color=ft.colors.WHITE)
                                    ),
                                ],
                                alignment="spaceBetween",
                            ),
                        ],
                        spacing=10,
                    ),
                    padding=15,
                    border_radius=10,
                    bgcolor="#333333",
                    margin=ft.margin.symmetric(horizontal=10, vertical=5),
                )
                saved_passwords_list.append(card_content)

            saved_passwords_content = ft.Column(
                [
                    ft.Text("Сохраненные пароли", size=20, color="white"),
                    *saved_passwords_list,
                ],
                horizontal_alignment="center",
                spacing=10,
            )

        container = ft.Container(
            content=saved_passwords_content,
            width=600,
            height=800,
            alignment=ft.alignment.center,
        )
        page.add(container)
        page.update()

    page.add(login_content)

ft.app(target=main)