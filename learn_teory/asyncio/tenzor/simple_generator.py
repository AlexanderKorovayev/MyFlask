def jumping_range(up_to):
    index = 0
    while index < up_to:
        jump = yield index
        print(f'jump is {jump}')
        if jump is None:
            jump = 1
        index += jump
        print(f'in next, {index}')


if __name__ == '__main__':
    iterator = jumping_range(5)
    print(next(iterator))
    print('next iteration')
    print(next(iterator))
    print('next iteration')
    print(next(iterator))
    print('next iteration')
    print(iterator.send(2))
