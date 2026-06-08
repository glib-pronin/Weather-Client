import flet

def page_layout(page, route, content):
    return flet.View(
        route=route,
        padding=0,
        expand=True,
        horizontal_alignment=flet.CrossAxisAlignment.STRETCH,
        controls=[
            flet.Container(
                padding=flet.Padding(left=20, top=68, right=20, bottom=0),
                expand=True,
                gradient=flet.LinearGradient(
                    begin=flet.Alignment.BOTTOM_LEFT,
                    end=flet.Alignment.TOP_RIGHT,
                    colors=['#B0C4DE', '#FFFFFF']
                ),
                content=flet.Column(
                    spacing=60,
                    expand=True,
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
                )
            )
        ]
    )