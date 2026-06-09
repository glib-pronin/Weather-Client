from modules.core import router_change, AppContainer
import flet

async def main(page: flet.Page):
    page.title = 'WeatherApp'
    page.storage = flet.SharedPreferences()
    page.app_container = AppContainer(on_logout=lambda: page.run_task(page.push_route, '/welcome'), storage=page.storage)

    page.on_close = page.app_container.on_close
    page.on_route_change = lambda e: router_change(page)

    await page.app_container.auth_manager.load_tokens()
    await page.app_container.auth_manager.me()
    await page.app_container.resolve_route(page, page.app_container.auth_manager)


if __name__ == '__main__':
    flet.run(main, assets_dir='assets')



