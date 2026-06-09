from ..components import page_layout, CustomButton, CustomInput
from ..utils import change_spinner_visibility
import flet

def login_page(page: flet.Page):

    async def on_login(e):
        email_input.error = None
        change_spinner_visibility(page, spinner, login_btn, True)

        email = email_input.value.strip()
        password = password_input.value.strip()
        res = await page.app_container.auth_manager.login(email, password)
        if res:
            await page.app_container.resolve_route(page, page.app_container.auth_manager)
        else:
            email_input.error = 'Неправильні адреса або пароль'
            change_spinner_visibility(page, spinner, login_btn, False)

    spinner = flet.ProgressRing(height=40, width=40, color='#0D133F', visible=False)
    email_input = CustomInput('Введіть електронну пошту')
    password_input = CustomInput('Введіть пароль', True, True)
    login_btn = CustomButton(content='Увійти до акаунту', on_click=on_login)
    content = flet.Column(
        spacing=44,
        horizontal_alignment=flet.CrossAxisAlignment.CENTER,
        controls=[
            flet.Text(
                value='Авторизація',
                size=24,
                color='#0D133F',
                weight=flet.FontWeight.BOLD
            ),
            flet.Column(
                spacing=16,
                controls=[
                    email_input,
                    password_input,
                    flet.GestureDetector(
                        content=flet.Text(
                            value='Ще немає акаунту? Зараєструватися',
                            size=16,
                            color='#0D133F',
                            weight=flet.FontWeight.NORMAL,
                            opacity=0.6, 
                        ),
                        on_tap=lambda e: page.run_task(page.push_route, '/register')
                    )
                ]
            ),
            login_btn,
            spinner
        ]
    )
    return page_layout(page, '/login', content)