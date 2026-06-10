import flet

class SuggestionItem(flet.GestureDetector):
    def __init__(self, text, data, on_click, *args, **kwargs):
        super().__init__(
            content=flet.Container(
                height=32,
                alignment=flet.Alignment.CENTER_LEFT,
                content=flet.Text(
                    value=text,
                    size=14,
                    color='#ffffff'
                )
            ),
            on_tap=lambda e: on_click(data), 
            mouse_cursor=flet.MouseCursor.CLICK,
            *args, **kwargs
        )

class SuggestionsContainer(flet.Container):
    def __init__(self, top, *args, **kwargs):
        super().__init__(
            visible=False,
            width=335,
            top=top,
            gradient=flet.LinearGradient(
                begin=flet.Alignment.TOP_CENTER,
                end=flet.Alignment.BOTTOM_CENTER,
                colors=['#6D7589', '#A2ACBA']
            ),
            border_radius=4,
            padding=flet.Padding(left=8, top=8, right=8, bottom=0),
            *args, **kwargs
        )
        
        self.list_view = flet.ListView(
            spacing=0,
            padding=0,
            height=0
        )

        self.content = flet.Column(
            spacing=10,
            controls=[
                flet.Text(
                    'Результати пошуку',
                    color=flet.Colors.with_opacity(0.8, '#FFFFFF'),
                    size=12,
                ),
                self.list_view
            ]
        )
    
    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False 

    def set_items(self, items):
        self.list_view.controls = items
        self.list_view.height = min(len(items)*32, 200)

    def set_empty_state(self):
        self.list_view.controls = [
            flet.Container(
                height=32,
                alignment=flet.Alignment.CENTER_LEFT,
                content=flet.Text(
                    value='Нічого не знайдено',
                    color='#ffffff',
                    size=14,
                )
            )
        ]
        self.list_view.height = 32