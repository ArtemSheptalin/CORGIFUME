from django.core.exceptions import ValidationError
import re


'''
    Свой собственный метод проверки данных, введённых в форме
    Значение value это то, что введёт пользователь в форму
    Данный способ считается более предпочтительным
'''


def validate_name_only(value):
    if not len(value) > 10:
        raise ValidationError('Ваше имя должно состоять более чем 10 символов...')
    return value


def validate_blacklisted(value):
    blacklist = ['abc123']
    if value in blacklist:
        raise ValidationError('Вы в чёрном списке!')


def check_phone_number(value):
    validate_phone_number_pattern = "^\\+?\\d{1,4}?[-.\\s]?\\(?\\d{1,3}?\\)?[-.\\s]?\\d{1,4}[-.\\s]?\\d{1,4}[-.\\s]?\\d{1,9}$"
    result = re.match(validate_phone_number_pattern, value) 
    
    if bool(result) is False:
        raise ValidationError('Вы ввели неверный формат телефона!')


def check_email(value):
    needed_symbols = '@.com'
    for i in value:
        if value not in needed_symbols:
            raise ValidationError('Вы ввели неверный формат почты!')