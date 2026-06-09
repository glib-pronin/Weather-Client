from ..components import page_layout, CustomButton, CustomInput, InputWithIcons
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

    async def on_click():
        print('click')

    show_back = 'show-back=1' in page.route

    country_input = InputWithIcons('Введіть назву країни')
    country_input.set_disability(elements_state[not show_back]['disabled'])
    country_input.set_suffix_icon_visibility(elements_state[show_back]['icon_visibility'])
    
    city_input = InputWithIcons('Введіть назву міста')
    city_input.set_opacity(elements_state[show_back]['input_opacity'])
    city_input.set_disability(True)
    city_input.set_suffix_icon_visibility(elements_state[show_back]['icon_visibility'])

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
                    CustomButton(
                        content='Продовжити',
                        on_click=on_click,
                        opacity=elements_state[show_back]['btn_opacity'],
                        disabled=elements_state[show_back]['disabled']
                    )
                ]
            )
        ]
    )
    return page_layout(page, '/welcome', content, show_back)