import contextlib
import time


@contextlib.contextmanager
def test():
    # вместо принтов могли быть какие нибудь блокирующие действия, поэтому можно рассмотреть асинхронный вариант
    # менеджера контекста, который бы не блокировал выполнение нашей проги
    # в случае эксита с исключением используем трай фанайли
    try:
        print('enter start')
        time.sleep(1)
        print('enter finish')
        #raise Exception
        yield 'test'

        print('exit start')
        time.sleep(2)
        print('exit finish')
    except Exception:
        print('opana')
    finally:
        print('in')


with test() as test:
    print('in main')
    print(test)
