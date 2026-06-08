from ..components import page_layout, CustomButton
import flet

def welcome_page(page: flet.Page, container):

    async def on_click():
        await page.push_route('/login')

    content = flet.Column(
        spacing=44,
        horizontal_alignment=flet.CrossAxisAlignment.CENTER,
        controls=[
            flet.Column(
                spacing=24,
                horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                controls=[
                    flet.Text(
                        value='Вітаємо у додатку!',
                        size=24,
                        color='#0D133F',
                        weight=flet.FontWeight.BOLD
                    ),
                    flet.Text(
                        value='Актуальна погода\nу будь-якому місті світу',
                        size=16,
                        color='#0D133F',
                        weight=flet.FontWeight.NORMAL,
                        opacity=0.6, 
                        text_align=flet.TextAlign.CENTER
                    )
                ]
            ),
            CustomButton(
                content='Авторизуватися',
                on_click=on_click
            )
        ]
    )
    return page_layout(page, '/welcome', content)