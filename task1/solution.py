def strict(func):
    def wrapper(*args, **kwargs):
        annotations = func.__annotations__

        for arg, annotation in zip(args, annotations.values()):
            if not isinstance(arg, annotation):
                raise TypeError

        for kwarg in kwargs:
            if not isinstance(kwargs[kwarg], annotations[kwarg]):
                raise TypeError

        return func(*args, **kwargs)
    return wrapper
