from datetime import datetime
from zoneinfo import ZoneInfo
import flet

class HourBlock(flet.Container):
    def __init__(self, hour, icon, temp, key, *args, **kwargs):
        self.time_text = flet.Text(hour, size=14, color='#ffffff')

        super().__init__(
            expand=True,
            width=51,
            padding=flet.Padding.symmetric(horizontal=4, vertical=7),
            key=key,
            border_radius=90,
            content=flet.Column(
                expand=True,
                alignment=flet.MainAxisAlignment.SPACE_BETWEEN,
                horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                controls=[
                    self.time_text,
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
        self.tz_id = None

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


    async def set_data(self, data, general):
        if not data:
            self.container_title.value = 'Не вдалося завантажити прогноз'
            self.hourly_list.controls = []
            self.tz_id = None
            return 
        
        self.container_title.value = general['desc']
        self.tz_id = general['tz_id']
        controls = []
        for d in data:
            block = HourBlock(
                d['hour'], 
                d['icon'], 
                d['temp'], 
                d['hour']
            )
            controls.append(block)
        self.hourly_list.controls = controls
        self.update()
        await self.select_current()
    
    def get_local_hour(self):
        return str(datetime.now(ZoneInfo(self.tz_id)).hour).zfill(2)
    
    async def select_current(self):
        current_hour = self.get_local_hour()
        index = 0
        for i, block in enumerate(self.hourly_list.controls):
            if block.key == current_hour:
                block.bgcolor = flet.Colors.with_opacity(0.2, '#FFFFFF')
                block.time_text.value = 'Зараз'
                block.time_text.size = 12
                index = i
            else:
                block.time_text.size = 14
                block.time_text.value = block.key
                block.bgcolor = None
        await self.hourly_list.scroll_to(offset=54*index, duration=500)