from modules.core import router_change
import flet 

async def main(page: flet.Page):
    page.title = 'WeatherApp'

    page.on_route_change = lambda e: router_change(page, None)
    await page.push_route('/welcome')

if __name__ == '__main__':
    flet.run(main, assets_dir='assets')
