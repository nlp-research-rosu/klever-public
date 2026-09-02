def even_odd_palindrome(n):
    if n < 10:
        even = n // 2
        odd = n - even
        return (even, odd)

    even = 4
    odd = 5

    pairs = n // 11
    if pairs > 9:
        pairs = 9
    even = even + pairs // 2
    odd = odd + pairs - pairs // 2

    if n >= 101:
        lead = n // 100
        if lead > 9:
            lead = 9
            extra = 10
        else:
            middle = (n // 10) % 10
            candidate = lead * 101 + middle * 10
            extra = middle
            if candidate <= n:
                extra = extra + 1

        previous = lead - 1
        even_leads = previous // 2
        odd_leads = previous - even_leads
        even = even + even_leads * 10
        odd = odd + odd_leads * 10
        if lead % 2 == 0:
            even = even + extra
        else:
            odd = odd + extra

    return (even, odd)
