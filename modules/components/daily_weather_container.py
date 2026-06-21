from datetime import datetime
import flet

class DayBlock(flet.Row):
    COLOR_MAP = {
        -21: '#0084FF',
        -18: '#1B93FF',
        -15: '#3DA6FF',
        -12: '#53B3FF',
        -9: '#5EBCFF',
        -6: '#5BBEF4',
        -3: '#67C8F0',
        0: '#7DD9EB',
        3: '#FFEDA5',
        6: '#FFE787',
        9: '#FFE270',
        12: '#FFDF5C',
        15: '#FFDA46',
        18: '#FFD322',
        21: '#F1C100',
        24: '#FF9E05',
        27: '#E67E22',
        30: '#CB6104',
        33: '#CB6104',
        36: '#FB2B02',
    }

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
                                colors=self.get_gradient_colors(int(min[:-1]), int(max[:-1]))
                            )
                        ),
                        flet.Text(max, size=16, color='#ffffff')
                    ]
                )
            ],
            *args, **kwargs
        )

    def get_gradient_colors(self, min_t, max_t):
        colors = []
        min_t = max(-21, min_t)
        min_t_normalized = round(min_t / 3) * 3
        colors.append(self.COLOR_MAP[min_t_normalized])
        max_t = min(36, max_t)
        max_t_normalized = round(max_t / 3) * 3
        colors.append(self.COLOR_MAP[max_t_normalized])
        return colors

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
