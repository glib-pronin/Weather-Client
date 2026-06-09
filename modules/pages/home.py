from ..components import BackButton
import flet

def home_page(page: flet.Page):
    return flet.View(
        route='/home',
        padding=0,
        expand=True,
        horizontal_alignment=flet.CrossAxisAlignment.STRETCH,
        controls=[
            flet.SafeArea(
                BackButton(
                    'Вибрати інше місто',
                    '#ffffff',
                    lambda e: page.run_task(page.push_route, '/select-country-city?show-back=1')
                )
            ),
        ]
    )