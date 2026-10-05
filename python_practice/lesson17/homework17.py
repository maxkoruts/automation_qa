#Generator — 1
print(f"Generator 1")
def even_numbers(n):
    for i in range(0, n + 1, 2):
        yield i

print(list(even_numbers(10)))  # [0, 2, 4, 6, 8, 10]
print()

#Generator — 2
print(f"Generator 2")
def fibonacci(n):
    a, b = 0, 1
    while a <= n:
        yield a
        a, b = b, a + b

print(list(fibonacci(666)))  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
print()

#Iterators — 1
print(f"Iterator 1")
class ReverseIterator:
    def __init__(self, data):
        self.data = data
        self.index = len(data)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == 0:
            raise StopIteration
        self.index -= 1
        return self.data[self.index]

for item in ReverseIterator([1, 2, 3, 4, 5]):
    print(item)
print()

#Iterators — 2
print(f"Iterator 2")
class EvenIterator:
    def __init__(self, n):
        self.n = n
        self.current = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.current > self.n:
            raise StopIteration
        value = self.current
        self.current += 2
        return value

print(list(EvenIterator(10)))  # [0, 2, 4, 6, 8, 10]
print()

#Decorators — 1
print(f"Decorator 1")
import functools

def log_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Виклик {func.__name__} з args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} повернула: {result}")
        return result
    return wrapper

@log_calls
def add(a, b):
    return a + b

add(2, b=3)
print()

#Decorators — 2
print(f"Decorator 2")
import functools

def handle_exceptions(default=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"Помилка у {func.__name__}: {type(e).__name__}: {e}")
                return default
        return wrapper
    return decorator

@handle_exceptions(default=0)
def divide(a, b):
    return a / b

print(divide(10, 2))
print(divide(10, 0))

print()