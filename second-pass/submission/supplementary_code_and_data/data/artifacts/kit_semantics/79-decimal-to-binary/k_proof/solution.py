def decimal_to_binary(decimal):
    binary = "db"
    if decimal == 0:
        binary = "0" + binary
    while decimal != 0:
        binary = chr(48 + decimal % 2) + binary
        decimal = decimal // 2
    return "db" + binary
