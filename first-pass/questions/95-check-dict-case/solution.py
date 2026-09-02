def check_dict_case(d):
    keys = list(d.keys())
    n = len(keys)
    if n == 0:
        return False
    k0 = keys[0]
    if not isinstance(k0, str):
        return False
    if k0.isupper():
        first = 'upper'
    elif k0.islower():
        first = 'lower'
    else:
        return False
    if n == 1:
        return True
    k1 = keys[1]
    if not isinstance(k1, str):
        return False
    if first == 'upper':
        return k1.isupper()
    else:
        return k1.islower()
