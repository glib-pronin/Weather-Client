from ..components import *
import flet

def home_page(page: flet.Page):
    user = page.app_container.auth_manager.user
    weather_service = page.app_container.weather_service

    async def update_current():
        data = await weather_service.update_current_weather(user['lat'], user['lng'], user['city'])     
        current_weather.set_data(data)   
        set_container_bg(data.get('icon_code', ''))
        page.update()

    async def load_weather():
        data = await weather_service.get_weather(user['lat'], user['lng'], user['city'])
        current_weather.set_data(data['current'])
        await hourly_weather.set_data(data['hourly'].get('hours'), data['hourly'].get('general'))
        daily_weather.set_data(data['daily'])
        set_container_bg(data['current'].get('icon_code', ''))
        page.update()
        page.app_container.time_manager.create_task(update_current, 600)

    current_weather = CurrentWeatherContainer()
    hourly_weather = HourlyWeatherContainer()
    daily_weather = DailyWeatherContainer()
    
    home_container = flet.Container(
        padding=flet.Padding(left=20, top=10, right=20, bottom=10),
        expand=True,
        animate=flet.Animation(500),
        gradient=flet.LinearGradient(
            begin=flet.Alignment.BOTTOM_LEFT,
            end=flet.Alignment.TOP_RIGHT,
            colors=['#87CEFA', '#FFDF56']
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
    bg_colors_map = {
        "01d": ['#87CEFA', '#FFDF56'],
        "02d": ['#87CEFA', '#FFDF56'],
        "01n": ['#191970', '#8A2BE2'],
        "02n": ['#191970', '#8A2BE2'],
        "03d": ['#C0C0C0', '#FFD27F'],
        "03n": ['#696969', '#9974BC'],
        "04d": ['#A9A9A9', '#696969'],
        "04n": ['#A9A9A9', '#696969'],
        "09d": ['#808080', '#5DACE2'],
        "09n": ['#808080', '#5DACE2'],
        "10d": ['#808080', '#5DACE2'],
        "10n": ['#808080', '#5DACE2'],
        "11d": ['#4A4A4A', '#5DACE2'],
        "11n": ['#4A4A4A', '#5DACE2'],
        "13d": ['#FFFFFF', '#B0C4DE'],
        "13n": ['#FFFFFF', '#B0C4DE'],
    }

    def set_container_bg(icon):
        print(icon)
        home_container.gradient.colors = bg_colors_map.get(icon, ['#87CEFA', '#FFDF56'])

    page.run_task(load_weather)

    return flet.View(
        route='/home',
        padding=0,
        expand=True,
        horizontal_alignment=flet.CrossAxisAlignment.STRETCH,
        controls=[
            flet.SafeArea(
                expand=True,
                content=home_container
            ),
        ]
    )