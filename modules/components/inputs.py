import flet

class CustomInput(flet.TextField):
    def __init__(self, placeholder, password=False, can_reveal_password=False, on_change=None, prefix=None, *args, **kwargs):
        super().__init__(
            password=password,
            can_reveal_password=can_reveal_password,
            bgcolor='#A0ABBA',
            border_radius=4,
            width=335,
            prefix=prefix,
            # height=40,
            hint_text=placeholder,
            text_style=flet.TextStyle(color='#FFFFFF', size=16),
            hint_style=flet.TextStyle(color='#FFFFFF', size=16),
            content_padding=flet.Padding.all(7),
            border_color='#A0ABBA',
            on_change=on_change,
            *args, **kwargs
        )

class InputWithIcons(flet.Container):
    def __init__(self, placeholder, on_suffix_click=None, on_change=None, *args, **kwargs):
        super().__init__(
            width=335,
            height=40,
            bgcolor='#A0ABBA',
            border_radius=4,
            padding=flet.Padding.symmetric(vertical=7, horizontal=7),
            *args, **kwargs
        )

        self.prefix_icon = flet.Icon(flet.Icons.SEARCH, color='#ffffff', size=22)
        self.suffix_icon = flet.GestureDetector(
            flet.Image(src='close_icon.png', width=20, height=20),
            mouse_cursor=flet.MouseCursor.CLICK,
            on_tap=on_suffix_click
        )
        self.input = flet.TextField(
            hint_text=placeholder,
            border_width=0,
            expand=True,
            content_padding=flet.Padding.symmetric(vertical=0),
            text_style=flet.TextStyle(color='#FFFFFF', size=16, height=1),
            hint_style=flet.TextStyle(color='#FFFFFF', size=16, height=1),
            on_change=on_change
        )
        self.content = flet.Row(
            vertical_alignment=flet.CrossAxisAlignment.CENTER,
            spacing=4,
            controls=[
                self.prefix_icon,
                self.input,
                self.suffix_icon
            ]
        )
    
    def set_value(self, value):
        self.input.value = value

    def set_opacity(self, value):
        self.opacity = value

    def set_disabed(self, disabled):
        self.input.disabled = disabled

    def set_suffix_icon_visible(self, visible):
        self.suffix_icon.visible = visible