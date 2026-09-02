def sort_array(array):
    return array[-1]


try:
    sort_array([])
except IndexError:
    print("CPYTHON_RESULT: IndexError")
else:
    raise AssertionError("CPython unexpectedly returned from [][-1]")
