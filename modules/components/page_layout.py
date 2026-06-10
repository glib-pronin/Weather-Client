from .buttons import BackButton
import flet

def page_layout(page: flet.Page, route, content, show_back=False):
    top=68
    header_controls = []
    if show_back:
        header_controls.append(
            BackButton(
                'Назад',
                text_color='#0D133F',
                on_click=lambda e: page.run_task(page.app_container.resolve_route, page, page.app_container.auth_manager)
            )
        )
        top=0
    
    return flet.View(
        route=route,
        padding=0,
        expand=True,
        horizontal_alignment=flet.CrossAxisAlignment.STRETCH,
        controls=[
            flet.SafeArea(
                expand=True,
                content=flet.Container(
                    padding=flet.Padding(left=20, top=top, right=20, bottom=0),
                    expand=True,
                    gradient=flet.LinearGradient(
                        begin=flet.Alignment.BOTTOM_LEFT,
                        end=flet.Alignment.TOP_RIGHT,
                        colors=['#B0C4DE', '#FFFFFF']
                    ),
                    content=flet.Column(
                        spacing=37,
                        expand=True,
                        horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                        controls=[
                            *header_controls,
                            flet.Column(
                                spacing=60,
                                horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                                controls=[
                                    flet.Image(
                                        src='welcome_image.png',
                                        width=160,
                                        height=160,
                                        fit=flet.BoxFit.COVER
                                    ),
                                    content
                                ]
                            ),
                        ]
                    )
                )
            )
        ],
    )