# solution.py — canonical verbatim minus the docstring (real genexp reading
# the free var mean; float ops are the shared opaque leaves).


def mean_absolute_deviation(numbers):
    mean = sum(numbers) / len(numbers)
    return sum(abs(x - mean) for x in numbers) / len(numbers)
