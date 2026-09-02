def solve(N):
    digit_sum = (
        N % 10
        + (N // 10) % 10
        + (N // 100) % 10
        + (N // 1000) % 10
        + (N // 10000) % 10
    )
    return bin(digit_sum)[2:]
