import threading


def test():
    return 5


if __name__ == '__main__':
    t = threading.Thread(target=test)
    test = t.start()
    print(test)
