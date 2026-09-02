from solution import median


print("odd_strings", median(["c", "a", "b"]))
print("prompt_even", median([-10, 4, 6, 1000, 10, 20]))

for label, value in (
    ("empty", []),
    ("even_strings", ["a", "b"]),
    ("incomparable", [1, "a"]),
):
    try:
        median(value)
    except Exception as error:
        print(label, type(error).__name__)
    else:
        raise AssertionError(f"{label} unexpectedly returned")
