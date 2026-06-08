from ..components import page_layout, CustomButton, CustomInput
import flet

def register_page(page: flet.Page, container):
    
    def on_register():
        ...

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
                    CustomInput('Введіть електронну пошту'),
                    CustomInput('Введіть пароль', True, True),
                    CustomInput('Підтвердьте пароль', True, True),
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
            CustomButton(
                content='Створити акаунт',
                on_click=on_register
            )
        ]
    )
    return page_layout(page, '/register', content)