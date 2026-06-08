import flet 

class CustomButton(flet.Button):
    def __init__(self, content, on_click, *args, **kwargs):
        super().__init__(
            content=content,
            on_click=on_click,
            bgcolor='#0D133F',
            color='#FFFFFF',
            width=335,
            style=flet.ButtonStyle(
                shape=flet.RoundedRectangleBorder(radius=100),
                text_style=flet.TextStyle(size=16, weight=flet.FontWeight.W_500),
                padding=flet.Padding(left=24, top=16, right=24, bottom=16),
                mouse_cursor=flet.MouseCursor.CLICK
            ),
            *args, **kwargs
        )
        