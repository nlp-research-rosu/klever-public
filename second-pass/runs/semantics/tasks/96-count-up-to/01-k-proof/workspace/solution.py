def count_up_to(n):
    result = []
    candidate = 2
    is_prime = True
    divisor = 2
    while candidate < n:
        while divisor < candidate:
            if candidate % divisor == 0:
                is_prime = False
            divisor += 1
        if is_prime:
            result.append(candidate)
        candidate += 1
        is_prime = True
        divisor = 2
    return result
