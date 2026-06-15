from datetime import datetime
import flet

class DayBlock(flet.Row):
    def __init__(self, text, icon, max, min, *args, **kwargs):
        super().__init__(
            expand=True,
            alignment=flet.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=flet.CrossAxisAlignment.CENTER,
            controls=[
                flet.Text(text, size=16, color='#ffffff'),
                flet.Row(
                    spacing=10,
                    vertical_alignment=flet.CrossAxisAlignment.CENTER,
                    controls=[
                        flet.Image(src=f'icons_svg/{icon}.svg'),
                        flet.Text(min, size=16, color='#ffffff'),
                        flet.Container(
                            width=60,
                            height=8,
                            border_radius=60,
                            gradient=flet.LinearGradient(
                                begin=flet.Alignment.CENTER_LEFT,
                                end=flet.Alignment.CENTER_RIGHT,
                                colors=['#87CEFA', '#FFDF56']
                            )
                        ),
                        flet.Text(max, size=16, color='#ffffff')
                    ]
                )
            ],
            *args, **kwargs
        )

class DailyWeatherContainer(flet.Container):
    def __init__(self, *args, **kwargs):
        super().__init__(
            expand=True,
            width=float("inf"),
            height=277,
            padding=10,
            bgcolor=flet.Colors.with_opacity(0.2, '#000000'),
            border_radius=10,
            *args, **kwargs
        )

        self.weekday_map = {
            'Sunday': 'Нд',
            'Monday': 'Пн',
            'Tuesday': 'Вт',
            'Wednesday': 'Ср',
            'Thursday': 'Чт',
            'Friday': 'Пт',
            'Saturday': 'Сб',
        }
        self.container_title = flet.Text(value='Завантажуємо прогноз...', size=16, color='#ffffff')
        self.daily_list = flet.Column(spacing=8)

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
                self.daily_list
            ]
        )

    def set_data(self, data):
        if not data:
            self.container_title.value = 'Не вдалося завантажити прогноз'
            self.daily_list.controls = []
            self.tz_id = None

        self.container_title.value = '5-Денний прогноз'
        controls = []
        for i, d in enumerate(data):
            controls.append(
                DayBlock(self.get_weekday(i, d['date']), d['main']['icon'], d['main']['max'], d['main']['min'])
            )
            if i < len(data) - 1:
                controls.append(flet.Divider(height=2, color=flet.Colors.with_opacity(0.2, '#ffffff'), expand=True))

        self.daily_list.controls = controls

    def get_weekday(self, ind, date):
        if ind == 0:
            return 'Сьогодні'
        return self.weekday_map[datetime.strptime(date, '%Y-%m-%d').strftime('%A')]
