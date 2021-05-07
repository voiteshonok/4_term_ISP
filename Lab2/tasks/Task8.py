def cashed(func):
    results = dict()

    def wrapped(*args, **kwargs):
        key = str(id(func)) + " " + str(tuple(args) + tuple(kwargs.values()))
        if key in results.keys():
            print('i have smth for u')
        else:
            results[key] = func(*args, **kwargs)
        return results[key]

    return wrapped


@cashed
def a(aaa, bbb):
    return aaa * bbb


print(a(1, 2))

print(a(aaa=1, bbb=2))
print(a(1, bbb=2))
print(a(1, 2))
