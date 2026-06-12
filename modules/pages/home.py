from ..components import BackButton, CustomButton
import flet

def home_page(page: flet.Page):
    return flet.View(
        route='/home',
        padding=0,
        expand=True,
        horizontal_alignment=flet.CrossAxisAlignment.STRETCH,
        controls=[
            flet.SafeArea(
                expand=True,
                content=flet.Container(
                    padding=flet.Padding(left=20, top=0, right=20, bottom=0),
                    expand=True,
                    gradient=flet.LinearGradient(
                        begin=flet.Alignment.BOTTOM_LEFT,
                        end=flet.Alignment.TOP_RIGHT,
                        colors=['#C0C0C0', '#FFD27F']
                    ),
                    content=flet.Column(
                        scroll=flet.ScrollMode.AUTO,
                        controls=[
                            BackButton(
                                'Вибрати інше місто',
                                '#ffffff',
                                lambda e: page.run_task(page.push_route, '/select-country-city?show-back=1')
                            ), 
                            flet.Text(
                                page.app_container.auth_manager.user['city'],
                                color='black'
                            ),
                            CustomButton('Logout', lambda e: page.run_task(page.app_container.auth_manager.logout))
                        ]
                    ),
                )
            ),
        ]
    )