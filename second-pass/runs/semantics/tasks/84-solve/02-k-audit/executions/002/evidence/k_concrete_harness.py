def solve(N):
    digit_sum = (
        N % 10
        + (N // 10) % 10
        + (N // 100) % 10
        + (N // 1000) % 10
        + (N // 10000) % 10
    )
    return bin(digit_sum)[2:]


assert solve(0) == "0"
assert solve(1) == "1"
assert solve(9) == "1001"
assert solve(10) == "1"
assert solve(99) == "10010"
assert solve(147) == "1100"
assert solve(150) == "110"
assert solve(1000) == "1"
assert solve(9999) == "100100"
assert solve(10000) == "1"
