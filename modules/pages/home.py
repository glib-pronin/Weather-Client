from ..components import *
import flet

def home_page(page: flet.Page):
    user = page.app_container.auth_manager.user
    weather_service = page.app_container.weather_service

    async def load_weather():
        data = await weather_service.get_weather(user['lat'], user['lng'], user['city'])
        current_weather.set_data(data['current'])
        await hourly_weather.set_data(data['hourly'].get('hours'), data['hourly'].get('general'))
        daily_weather.set_data(data['daily'])
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