import flet

class CustomInput(flet.TextField):
    def __init__(self, placeholder, password=False, can_reveal_password=False, *args, **kwargs):
        super().__init__(
            password=password,
            can_reveal_password=can_reveal_password,
            bgcolor='#A0ABBA',
            border_radius=4,
            width=335,
            height=40,
            hint_text=placeholder,
            text_style=flet.TextStyle(color='#FFFFFF', size=16),
            hint_style=flet.TextStyle(color='#FFFFFF', size=16),
            content_padding=flet.Padding.all(7),
            border_color='#A0ABBA',
            *args, **kwargs
        )
