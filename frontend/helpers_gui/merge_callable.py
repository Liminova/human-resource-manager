def merge_callable(callable_1, callable_2):
    def wrapper():
        callable_1()
        callable_2()

    return wrapper
