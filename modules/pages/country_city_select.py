from ..components import *
from ..utils import elements_state, check_query, Debounce
import flet

def country_city_select_page(page: flet.Page):
    auth = page.app_container.auth_manager
    location_service = page.app_container.location_service
    debounce = Debounce(300, page)
    page.run_task(location_service.load_countries)
    location_service.set_location(auth.user['country'], auth.user['country_code'], auth.user['city'])

    show_back = 'show-back=1' in page.route

    async def on_country_suffix_click(e):
        country_input.set_value('')
        country_input.set_disabed(False)
        country_input.set_suffix_icon_visible(False)

        city_input.set_value('')
        city_input.set_disabed(True)
        city_input.set_suffix_icon_visible(False)
        city_input.set_opacity(elements_state[False]['input_opacity'])
        city_suggestion.hide()

        continue_btn.opacity = elements_state[False]['btn_opacity']
        continue_btn.disabled = True

        page.update()
        if auth.user['city']:
            res = await location_service.clear_location()
            if res:
                auth.set_user(res)
            print(auth.user)

    def on_country_input_change(e):
        query = e.control.value
        if not check_query(query, country_suggestion.hide):
            page.update()
            return
        countries = location_service.filter_countries(query)
        country_suggestion.show()
        if countries:
            country_suggestion.set_items([
                SuggestionItem(
                    text=country['name'],
                    data=country,
                    on_click=on_country_selected
                )
                for country in countries
            ])
        else:
            country_suggestion.set_empty_state()
        page.update()

    def on_country_selected(country):
        location_service.selected_country = country['name']
        location_service.selected_country_code = country['code']

        country_input.set_value(country['name'])
        country_input.set_disabed(True)
        country_input.set_suffix_icon_visible(True)

        city_input.set_disabed(False)
        city_input.set_opacity(1)

        country_suggestion.hide()
        page.update()

    async def on_city_input_change(e):
        query = e.control.value
        if not check_query(query, city_suggestion.hide):
            page.update()
            return
        cities = await location_service.search_cities(query)
        city_suggestion.show()
        if cities:
            city_suggestion.set_items([
                SuggestionItem(
                    text=city['display_name'],
                    data=city,
                    on_click=on_city_selected
                )
                for city in cities
            ])
        else:
            city_suggestion.set_empty_state()
        page.update()

    def on_city_selected(city):
        location_service.selected_city = city['name']
        city_input.set_value(city['name'])
        city_input.set_disabed(True)
        city_input.set_suffix_icon_visible(True)
        city_suggestion.hide()
        continue_btn.opacity = elements_state[True]['btn_opacity']
        continue_btn.disabled = False

    def on_city_suffix_click(e):
        city_input.set_value('')
        city_input.set_disabed(False)
        city_input.set_suffix_icon_visible(False)
        continue_btn.opacity = elements_state[False]['btn_opacity']
        continue_btn.disabled = True
        location_service.selected_city = None
        page.update()

    async def on_continue(e):
        user = await location_service.save_selection(auth.user)
        if not user:
            return
        auth.set_user(user)
        await page.push_route('/home')
        
    country_input = InputWithIcons('Введіть назву країни', on_suffix_click=on_country_suffix_click, on_change=on_country_input_change)
    country_input.set_value(auth.user['country'])
    country_input.set_disabed(elements_state[not show_back]['disabled'])
    country_input.set_suffix_icon_visible(elements_state[show_back]['icon_visibility'])
    
    city_input = InputWithIcons('Введіть назву міста', on_suffix_click=on_city_suffix_click, on_change=lambda e: debounce.run(on_city_input_change, e))
    city_input.set_opacity(elements_state[show_back]['input_opacity'])
    city_input.set_disabed(True)
    city_input.set_suffix_icon_visible(elements_state[show_back]['icon_visibility'])
    city_input.set_value(auth.user['city'])

    country_suggestion = SuggestionsContainer(120)
    city_suggestion = SuggestionsContainer(176)

    continue_btn = CustomButton(
        content='Продовжити',
        on_click=on_continue,
        opacity=elements_state[show_back]['btn_opacity'],
        disabled=elements_state[show_back]['disabled']
    )

    content = flet.Stack(
        clip_behavior=flet.ClipBehavior.NONE,
        controls=[
            flet.Column(
                spacing=44,
                horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                controls=[
                    flet.Text(
                        value='Оберіть своє місто',
                        size=24,
                        color='#0D133F',
                        weight=flet.FontWeight.BOLD
                    ),
                    flet.Column(
                        spacing=16,
                        controls=[
                            country_input,
                            city_input
                        ]
                    ),
                    continue_btn
                ]
            ),
            country_suggestion,
            city_suggestion
        ]
    )
    return page_layout(page, '/welcome', content, show_back)