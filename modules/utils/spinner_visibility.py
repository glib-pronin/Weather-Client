def change_spinner_visibility(page, spinner, element, is_spinner_visible):
    spinner.visible = is_spinner_visible
    element.visible = not is_spinner_visible
    page.update()