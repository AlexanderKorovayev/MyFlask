"""
модуль для вспомогательных функций
"""


def check_type(obj, base_type):
    """
    Метод проверки соответсвия объекта базовому типу
    :param obj: объект, который необходимо проверить
    :param base_type: базовый тип
    :return: True or False
    """
    rez = False
    if obj.__name__ == 'object':
        return rez
    for base in obj.__bases__:
        if base.__name__ == base_type.__name__:
            rez = True
            return rez
        else:
            rez = check_type(base, base_type)
            if rez is True:
                return rez
    return rez

