def simplify(x, n):
    x_num, x_den = x.split("/")
    n_num, n_den = n.split("/")
    return (int(x_num) * int(n_num)) % (int(x_den) * int(n_den)) == 0


assert simplify("1/5", "5/1") == True
assert simplify("1/6", "2/1") == False
assert simplify("7/10", "10/2") == False
assert simplify("1/1", "1/1") == True
assert simplify("1/2", "1/1") == False
assert simplify("2/3", "3/2") == True
assert simplify("12/35", "70/24") == True
assert simplify("18014398509481985/2", "1/1") == False
