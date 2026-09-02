def sort_array(array):
    return sorted(
        array,
        reverse=len(array) > 0 and (array[0] + array[-1]) % 2 == 0,
    )
