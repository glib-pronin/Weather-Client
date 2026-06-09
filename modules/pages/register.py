from ..components import page_layout, CustomButton, CustomInput
from ..utils import is_valid_email, is_valid_password, change_spinner_visibility
import flet

def register_page(page: flet.Page):
    
    async def on_register(e):
        email_input.error = None
        password_input.error = None
        confirm_password_input.error = None
        change_spinner_visibility(page, spinner, register_btn, True)

        email = email_input.value.strip()
        password = password_input.value.strip()
        confirm_password = confirm_password_input.value.strip()

        if not email or not is_valid_email(email):
            email_input.error = 'Некоректна адреса електронної пошти'
            change_spinner_visibility(page, spinner, register_btn, False)
            return
        res, error = is_valid_password(password)
        if not res:
            password_input.error = error
            change_spinner_visibility(page, spinner, register_btn, False)
            return
        if password != confirm_password:
            confirm_password_input.error = 'Паролі не збігаються'
            change_spinner_visibility(page, spinner, register_btn, False)
            return
        res = await page.app_container.auth_manager.register(email, password, confirm_password)
        if res:
            await page.app_container.resolve_route(page, page.app_container.auth_manager)
        else:
            email_input.error = 'Вже існує акаунт з такою поштою'
            change_spinner_visibility(page, spinner, register_btn, False)

    def on_change(e):
        if password_input.value != confirm_password_input.value and confirm_password_input.value.strip():
            confirm_password_input.error = 'Паролі не збігаються'
        else:
            confirm_password_input.error = None
        if e.control == password_input:
            res, error = is_valid_password(password_input.value)
            if not res:
                password_input.error = error
            else:
                password_input.error = None
            password_input.update()
        confirm_password_input.update()

    spinner = flet.ProgressRing(height=40, width=40, color='#0D133F', visible=False)
    email_input = CustomInput('Введіть електронну пошту')
    password_input = CustomInput('Введіть пароль', True, True, on_change)
    confirm_password_input = CustomInput('Підтвердьте пароль', True, True, on_change)
    register_btn = CustomButton(content='Створити акаунт', on_click=on_register)

    content = flet.Column(
        spacing=44,
        horizontal_alignment=flet.CrossAxisAlignment.CENTER,
        controls=[
            flet.Text(
                value='Реєстрація',
                size=24,
                color='#0D133F',
                weight=flet.FontWeight.BOLD
            ),
            flet.Column(
                spacing=16,
                controls=[
                    email_input,
                    password_input,
                    confirm_password_input,
                    flet.GestureDetector(
                        content=flet.Text(
                            value='Вже є акаунт? Увійти',
                            size=16,
                            color='#0D133F',
                            weight=flet.FontWeight.NORMAL,
                            opacity=0.6, 
                        ),
                        on_tap=lambda e: page.run_task(page.push_route, '/login')
                    ),
                    
                ]
            ),
            register_btn,
            spinner
        ]
    )
    return page_layout(page, '/register', content)