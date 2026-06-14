import flet

class HourBlock(flet.Container):
    def __init__(self, hour, icon, temp, *args, **kwargs):
        super().__init__(
            expand=True,
            width=51,
            padding=flet.Padding.symmetric(horizontal=4, vertical=7),
            # bgcolor=flet.Colors.with_opacity(0.2, '#000000'),
            border_radius=90,
            content=flet.Column(
                expand=True,
                alignment=flet.MainAxisAlignment.SPACE_BETWEEN,
                horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                controls=[
                    flet.Text(hour, size=14, color='#ffffff'),
                    flet.Image(src=f'icons_svg/{icon}.svg'),
                    flet.Text(temp, size=14, color='#ffffff'),
                ]
            ),
            *args, **kwargs
        )

class HourlyWeatherContainer(flet.Container):
    def __init__(self, *args, **kwargs):
        super().__init__(
            expand=True,
            width=float("inf"),
            height=176,
            padding=10,
            bgcolor=flet.Colors.with_opacity(0.2, '#000000'),
            border_radius=10,
            *args, **kwargs
        )

        self.container_title = flet.Text(value='Завантажуємо прогноз...', size=16, color='#ffffff')
        self.hourly_list = flet.ListView(horizontal=True, expand=True, spacing=3, auto_scroll=False, height=93)

        self.content = flet.Column(
            expand=True,
            spacing=16,
            controls=[
                flet.Column(
                    spacing=8,
                    controls=[
                        self.container_title,
                        flet.Divider(height=2, color=flet.Colors.with_opacity(0.2, '#ffffff'), expand=True),
                    ]
                ),
                self.hourly_list
            ]
        )

    def set_data(self, data, title):
        self.container_title.value = title
        self.hourly_list.controls = [
            HourBlock(str(d['hour']).zfill(2), d['icon'], d['temp'])
            for d in data
        ]