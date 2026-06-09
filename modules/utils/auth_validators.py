import re

def is_valid_email(email):
    return re.match(r'^[a-zA-Z0-9+_%.-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)

def is_valid_password(password):
    if len(password) < 6:
        return False, 'Пароль повинен бути більше 5 символів'
    if not re.search(r'[a-z]', password, flags=re.IGNORECASE):
        return False, 'Пароль повинен містити латинські символи'
    if not re.search(r'[0-9]', password):
        return False, 'Пароль повинен містити цифри'
    return True, ''