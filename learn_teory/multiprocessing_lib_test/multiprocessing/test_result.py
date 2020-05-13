import multiprocessing
from concurrent.futures import ProcessPoolExecutor
import time


def test_result(value):
    time.sleep(3)
    return value


if __name__ == '__main__':
    
    with ProcessPoolExecutor(max_workers=1) as executor:
        result_object = executor.submit(test_result, 5)
        print(result_object.result())
    
    # если главный процесс заканчивается быстрее чем дочерний, то дочерний всё равно ожидаем
    '''
    p = multiprocessing.Process(target=test_result, args=(5,))
    p.start()
    print('test')
    '''
