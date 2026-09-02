assert ",".join(["a", "bc", "d"]) == "a,bc,d"
assert "".join(["x", "y"]) == "xy"
assert ", ".join([]) == ""
assert "banana".count("an") == 2
assert "aaaa".count("aa") == 2
assert "abc".count("z") == 0
assert "  hi there \n".strip() == "hi there"
assert "abc".strip() == "abc"
assert "".strip() == ""
assert len("ok".encode("ascii")) == 2
words = "a-b".split("-")
assert "+".join(words) == "a+b"
