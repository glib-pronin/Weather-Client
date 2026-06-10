from ..components import *
import flet

elements_state = {
    True: {
        'btn_opacity': 1,
        'input_opacity': 1,
        'disabled': False,
        'icon_visibility': True
    },
    False: {
        'btn_opacity': 0.3,
        'input_opacity': 0.4,
        'disabled': True,
        'icon_visibility': False
    }
}

def country_city_select_page(page: flet.Page):
    user = page.app_container.auth_manager.user
    location_service = page.app_container.location_service
    page.run_task(location_service.load_countries)
    location_service.set_location(user['country'], user['country_code'], user['city'])

    show_back = 'show-back=1' in page.route

    async def on_country_suffix_click(e):
        country_input.set_value('')
        country_input.set_disabed(False)
        country_input.set_suffix_icon_visible(False)

        city_input.set_value('')
        city_input.set_disabed(True)
        city_input.set_suffix_icon_visible(False)
        city_input.set_opacity(elements_state[False]['input_opacity'])

        continue_btn.opacity = elements_state[False]['btn_opacity']
        continue_btn.disabled = True

        page.update()
        if user['city']:
            res = await location_service.clear_location()
            if res:
                page.app_container.auth_manager.set_user(res)

    def on_country_input_change(e):
        query = e.control.value
        if len(query.strip()) < 3:
            country_suggestion.hide()
        else:
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


    country_input = InputWithIcons('Введіть назву країни', on_suffix_click=on_country_suffix_click, on_change=on_country_input_change)
    country_input.set_value(user['country'])
    country_input.set_disabed(elements_state[not show_back]['disabled'])
    country_input.set_suffix_icon_visible(elements_state[show_back]['icon_visibility'])
    
    city_input = InputWithIcons('Введіть назву міста')
    city_input.set_opacity(elements_state[show_back]['input_opacity'])
    city_input.set_disabed(True)
    city_input.set_suffix_icon_visible(elements_state[show_back]['icon_visibility'])
    city_input.set_value(user['city'])

    country_suggestion = SuggestionsContainer(120)

    continue_btn = CustomButton(
        content='Продовжити',
        on_click=...,
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
            country_suggestion
        ]
    )
    return page_layout(page, '/welcome', content, show_back)