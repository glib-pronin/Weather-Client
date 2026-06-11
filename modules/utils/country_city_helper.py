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

def check_query(query, callback):
    if len(query.strip()) < 3:
        callback()
        return False
    return True