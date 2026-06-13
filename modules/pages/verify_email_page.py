from ..components import page_layout, CustomButton, CustomInput
from ..utils import change_spinner_visibility
import flet

def verify_email_page(page: flet.Page):
    def on_change(e, ind):
        error_txt.value = ''
        field = e.control
        value = field.value or ''
        if value and value[-1].isdigit():
            field.value = value[-1]
        else: 
            field.value = ''
        if field.value:
            if ind < len(otp_fields) - 1:
                page.run_task(otp_fields[ind+1].focus)

    async def on_verify(e):
        code = ''.join([f.value for f in otp_fields])
        if len(code) <= 5:
            error_txt.value = 'Заповніть усі поля'
            page.update()
            return
        change_spinner_visibility(page, spinner, verify_btn, True)
        res = await page.app_container.auth_manager.verify_email(code)
        if res:
            await page.app_container.resolve_route(page, page.app_container.auth_manager)
        else:
            error_txt.value = 'Неправильний код'
            change_spinner_visibility(page, spinner, verify_btn, False)
            page.update()



    otp_fields = []
    otp_row = flet.Row(
        spacing=8,
        alignment=flet.MainAxisAlignment.CENTER,
        controls=[]
    )
    for i in range(6):
        field = flet.TextField(
            width=45,
            height=50,
            bgcolor='#A0ABBA',
            border_width=0,
            border_radius=4,
            content_padding=5,
            text_align=flet.TextAlign.CENTER,
            keyboard_type=flet.KeyboardType.NUMBER,
            on_change=lambda e, i=i: on_change(e, i)
        )
        otp_fields.append(field)
        otp_row.controls.append(field)

    error_txt = flet.Text(value='', size=14, color='red')
    spinner = flet.ProgressRing(height=40, width=40, color='#0D133F', visible=False)
    verify_btn = CustomButton(content='Підтвердити', on_click=on_verify)
    content = flet.Column(
        spacing=44,
        horizontal_alignment=flet.CrossAxisAlignment.CENTER,
        controls=[
            flet.Text(
                value='Підтвердження пошти',
                size=24,
                color='#0D133F',
                weight=flet.FontWeight.BOLD
            ),
            flet.Text(
                value=f'Ми надіслали код на вашу пошту ({page.app_container.auth_manager.pending_email})\nВведіть його нижче, щоб підтвердити акаунт',
                size=16,
                color='#0D133F',
                weight=flet.FontWeight.NORMAL,
                opacity=0.6, 
                text_align=flet.TextAlign.CENTER
            ),
            flet.Column(
                spacing=8,
                width=300,
                controls=[
                    otp_row,
                    error_txt,
                ]
            ),
            verify_btn,
            spinner
        ]
    )
    return page_layout(page, '/verify_email', content, show_back=True)