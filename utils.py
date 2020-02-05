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


class Test:
    # пока храним в поле класса, но надо будет это поменять потому что каждый экземпляр будет переписывать данные, например хранить в базе
    route_map = {}
    def route(self, path, method='GET'):
        def inner_route(f):
            Test.route_map[(path, method)] = f.__name__
            def inner_inner_route(*args, **kwargs):
                rez = f(*args, **kwargs)
                return rez
            return inner_inner_route
        return inner_route

    def test(self, path, method='GET'):
        func = Test.route_map.get((path, method))
        print(globals().get(func)())

test = Test()

@test.route('/')
def logic():
    return 'test555'

@test.route('/start')
def logic1():
    return 'test666'

test.test('/')
test.test('/start')


