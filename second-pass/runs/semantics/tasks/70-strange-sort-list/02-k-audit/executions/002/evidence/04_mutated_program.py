def strange_sort_list(lst):
    ordered = sorted(lst)
    result = []
    i = 0
    while i < len(ordered):
        if i % 2 == 0:
            # Same mutation as 04_verification_body_mutation.k.
            result.append(ordered[0])
        else:
            result.append(ordered[len(ordered) - (i // 2) - 1])
        i += 1
    return result


assert strange_sort_list([1, 2, 3]) == [1, 3, 1]
assert strange_sort_list([1, 2, 3]) != [1, 3, 2]
