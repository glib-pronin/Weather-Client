import flet

class CurrentWeatherContainer(flet.Container):
    def __init__(self, *args, **kwargs):
        super().__init__(
            expand=True,
            width=float("inf"),
            height=316,
            padding=flet.Padding.symmetric(vertical=25, horizontal=10),
            bgcolor=flet.Colors.with_opacity(0.2, '#000000'),
            border_radius=10,
            *args, **kwargs
        )

        self.city_name = flet.Text(value='Завантажуємо прогноз...', size=16, color='#ffffff')
        self.weather_icon = flet.Image(src=f'welcome_image.png', width=340, height=340, top=-120, left=-105, visible=False)
        self.temperature = flet.Text(value='', size=74, color='#ffffff', margin=flet.Margin.only(left=84))
        self.weather_description = flet.Text(value='', size=24, color='#ffffff', text_align=flet.TextAlign.CENTER)
        self.max_min = flet.Text(value='', size=16, color=flet.Colors.with_opacity(0.8, '#ffffff'))

        self.content = flet.Column(
            expand=True,
            horizontal_alignment=flet.CrossAxisAlignment.CENTER,
            spacing=16,
            controls=[
                self.city_name,
                flet.Row(
                    expand=True,
                    width=155,
                    controls=[
                        flet.Stack(
                            clip_behavior=flet.ClipBehavior.NONE,
                            controls=[
                                self.weather_icon,
                                self.temperature
                            ]
                        )
                    ]
                ),
                flet.Column(
                    spacing=10,
                    horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                    controls=[
                        self.weather_description,
                        self.max_min
                    ]
                )
            ]
        )

    def set_data(self, data):
        if not data:
            self.city_name.value = 'Не вдалося завантажити прогноз'
            self.city_name.size = 16
            self.weather_icon.visible = False
            self.temperature.value = ''
            self.weather_description.value = ''
            self.max_min.value = ''
            return
        
        self.city_name.value = data['city_name']
        self.city_name.size = 34
        self.weather_icon.src = f'icons_png/{data["icon_code"]}.png'
        self.weather_icon.visible = True
        self.temperature.value = data['temp']
        self.optimize_text(data['temp'])
        self.weather_description.value = data['desc']
        self.max_min.value = data['max_min']

    def optimize_text(self, text):
        if len(text) == 2:
            self.temperature.margin = flet.Margin.only(left=84)
            self.weather_icon.left = -145
        elif len(text) == 3: 
            self.temperature.margin = flet.Margin.only(left=64)
            self.weather_icon.left = -160
        else:
            self.temperature.margin = flet.Margin.only(left=54)
            self.weather_icon.left = -170