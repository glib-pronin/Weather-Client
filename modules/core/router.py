from ..pages import *
import flet

def router_change(page: flet.Page, container):
    page.views.clear()
    if page.route == '/welcome':
        page.views.append(welcome_page(page, container))
    elif page.route == '/login':
        page.views.append(login_page(page, container))
    elif page.route == '/register':
        page.views.append(register_page(page, container))