from ..components import page_layout, CustomButton, CustomInput
import flet

def login_page(page: flet.Page, container):

    def on_login():
        ...

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
                    CustomInput('Введіть електронну пошту'),
                    CustomInput('Введіть пароль', True, True),
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
            CustomButton(
                content='Увійти до акаунту',
                on_click=on_login
            )
        ]
    )
    return page_layout(page, '/login', content)