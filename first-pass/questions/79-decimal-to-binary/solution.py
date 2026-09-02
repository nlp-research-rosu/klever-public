# solution.py — canonical verbatim minus the docstring (real bin() + slice).


def decimal_to_binary(decimal):
    return "db" + bin(decimal)[2:] + "db"
