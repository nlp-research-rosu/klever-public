def order_by_points(nums):
    return sorted(
        nums,
        key=lambda n: sum(map(int, str(abs(n))))
        - (2 * int(str(abs(n))[0]) if n < 0 else 0),
    )
