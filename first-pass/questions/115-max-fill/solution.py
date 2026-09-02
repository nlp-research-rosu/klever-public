def max_fill(grid, capacity):
    # Behaviour-preserving rewrite of canonical.py for K verification.
    #   canonical: return sum([math.ceil(sum(arr) / capacity) for arr in grid])
    # Reformulated WITHOUT float / math.ceil:  for rowSum >= 0 and capacity >= 1,
    #   ceil(rowSum / capacity) == (rowSum + capacity - 1) // capacity   (floored //).
    # The list-comprehension + outer sum is unrolled into an accumulator loop.
    total = 0
    for arr in grid:
        total = total + (sum(arr) + capacity - 1) // capacity
    return total
