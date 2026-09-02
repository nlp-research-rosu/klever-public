def decimal_to_binary(decimal):
    binary = "db"
    if decimal == 0:
        binary = "0" + binary
    while decimal != 0:
        binary = chr(48 + decimal % 2) + binary
        decimal = decimal // 2
    return "db" + binary


assert decimal_to_binary(0) == "db0db"
assert decimal_to_binary(1) == "db1db"
assert decimal_to_binary(15) == "db1111db"
assert decimal_to_binary(32) == "db100000db"
assert decimal_to_binary(255) == "db11111111db"
