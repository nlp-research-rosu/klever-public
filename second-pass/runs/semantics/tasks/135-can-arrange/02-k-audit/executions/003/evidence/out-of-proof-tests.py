def can_arrange(arr):
    result = -1
    index = 0
    previous = 0
    for current in arr:
        if index > 0:
            if current < previous:
                result = index
        previous = current
        index = index + 1
    return result


# Both are duplicate-free arrays whose adjacent values support ordering.
# The prompt does not exclude them, but ints(VS) is false for their elements.
assert can_arrange([1.25, -2.5, 3.75, 0.5]) == 3
assert can_arrange(["ant", "bee", "ape", "zebra", "yak"]) == 4
