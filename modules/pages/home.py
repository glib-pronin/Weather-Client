from ..components import *
import flet, asyncio

def home_page(page: flet.Page):
    user = page.app_container.auth_manager.user

    async def load_weather():
        # await asyncio.sleep(1)
        current_weather.set_data({
            'city_name': user['city'],
            'icon_code': '01d',
            'temp': '11°',
            'desc': 'Хмарно',
            'max_min': 'Макс.:11°, мін.:0°'
        })
        hourly_weather.set_data([{'hour': i, 'icon': '02d', 'temp': '11°'} for i in range(23)], 'Хмарна погода до кінця дня')
        daily_weather.set_data([{'text': 'Сб', 'icon': '01d', 'max': '11°', 'min': '1°'} for i in range(5)], '5-Денний прогноз')
        page.update()

    current_weather = CurrentWeatherContainer()
    hourly_weather = HourlyWeatherContainer()
    daily_weather = DailyWeatherContainer()
    
    page.run_task(load_weather)

    return flet.View(
        route='/home',
        padding=0,
        expand=True,
        horizontal_alignment=flet.CrossAxisAlignment.STRETCH,
        controls=[
            flet.SafeArea(
                expand=True,
                content=flet.Container(
                    padding=flet.Padding(left=20, top=10, right=20, bottom=10),
                    expand=True,
                    gradient=flet.LinearGradient(
                        begin=flet.Alignment.BOTTOM_LEFT,
                        end=flet.Alignment.TOP_RIGHT,
                        colors=['#C0C0C0', '#FFD27F']
                    ),
                    content=flet.Column(
                        scroll=flet.ScrollMode.AUTO,
                        horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                        spacing=10,
                        controls=[
                            BackButton(
                                'Вибрати інше місто',
                                '#ffffff',
                                lambda e: page.run_task(page.push_route, '/select-country-city?show-back=1'),
                                18
                            ),
                            flet.Divider(
                                color=flet.Colors.with_opacity(0.2, '#ffffff'),
                                height=2
                            ),
                            current_weather,
                            hourly_weather,
                            daily_weather
                        ]
                    ),
                )
            ),
        ]
    )