def decimal_to_binary(decimal):
    return "db" + bin(decimal)[2:] + "db"


assert decimal_to_binary(0) == "db0db"
assert decimal_to_binary(1) == "db1db"
assert decimal_to_binary(2) == "db10db"
assert decimal_to_binary(15) == "db1111db"
assert decimal_to_binary(32) == "db100000db"
assert decimal_to_binary(103) == "db1100111db"
assert decimal_to_binary(256) == "db100000000db"
assert decimal_to_binary(-1) == "dbb1db"
assert decimal_to_binary(-15) == "dbb1111db"
