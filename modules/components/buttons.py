import flet 

class CustomButton(flet.Button):
    def __init__(self, content, on_click, opacity=1, disabled=False, *args, **kwargs):
        super().__init__(
            content=content,
            on_click=on_click,
            bgcolor='#0D133F',
            color='#FFFFFF',
            width=335,
            height=52,
            opacity=opacity, 
            disabled=disabled,
            style=flet.ButtonStyle(
                shape=flet.RoundedRectangleBorder(radius=100),
                text_style=flet.TextStyle(size=16, weight=flet.FontWeight.W_500),
                padding=flet.Padding(left=24, top=16, right=24, bottom=16),
                mouse_cursor=flet.MouseCursor.CLICK
            ),
            *args, **kwargs
        )

class BackButton(flet.Container):
    def __init__(self, value, text_color, on_click, *args, **kwargs):
        super().__init__(
            height=41,
            on_click=on_click,
            content=flet.Row(
                alignment=flet.MainAxisAlignment.START,
                vertical_alignment=flet.CrossAxisAlignment.CENTER,
                expand=True,
                spacing=5,
                controls=[
                    flet.Icon(
                        icon=flet.Icons.ARROW_BACK_ROUNDED,
                        color=text_color,
                        size=18
                    ),
                    flet.Text(
                        value=value,
                        size=12,
                        color=text_color,
                    )
                ]
            ),
            *args, **kwargs
        )
        