# solution.py — canonical verbatim minus the docstring (real genexp reading
# the free var mean; float ops are the shared opaque leaves).


def mean_absolute_deviation(numbers):
    mean = sum(numbers) / len(numbers)
    return sum(abs(x - mean) for x in numbers) / len(numbers)


assert mean_absolute_deviation([1.0, 2.0, 3.0, 4.0]) == 1.0
