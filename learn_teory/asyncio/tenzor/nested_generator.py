def bottom():
    print('in bottom')
    return (yield 42)


def middle():
    print('in middle')
    return (yield from bottom())


def top():
    print('in top')
    return (yield from middle())


print('top')
gen = top()
print('top next')
value = next(gen)
print(value)

try:
    print('gen send')
    value = gen.send(value * 2)
except StopIteration as e:
    value = e.value

print(value)
