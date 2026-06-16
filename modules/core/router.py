from ..pages import *
import flet

def router_change(page: flet.Page):
    page.views.clear()
    page.app_container.time_manager.cancel_all()
    if page.route == '/welcome':
        page.views.append(welcome_page(page))
    elif page.route == '/login':
        page.views.append(login_page(page))
    elif page.route == '/verify_email':
        page.views.append(verify_email_page(page))
    elif page.route == '/register':
        page.views.append(register_page(page))
    elif page.route.startswith('/select-country-city'):
        page.views.append(country_city_select_page(page))
    elif page.route == '/home':
        page.views.append(home_page(page))

async def resolve_route(page: flet.Page, auth_manager):
    if auth_manager.pending_email:
        await page.push_route('/login')
        return
    if not auth_manager.user:
        await page.push_route('/welcome')
        return
    if not auth_manager.user.get('city'):
        await page.push_route('/select-country-city')
        return
    await page.push_route('/home')
    
