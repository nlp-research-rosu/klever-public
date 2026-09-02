def is_bored(S):
    count = 0
    state = 0
    ch = ""
    code = 0
    for ch in S:
        code = ord(ch)
        if code == 46 or code == 63 or code == 33:
            state = 0
        elif state == 0:
            if code == 32 or (code >= 9 and code <= 13):
                state = 0
            elif code == 73:
                state = 1
            else:
                state = 2
        elif state == 1:
            if code == 32:
                count += 1
            state = 2
    return count


assert is_bored("Hello world") == 0
assert is_bored("The sky is blue. The sun is shining. I love this weather") == 1
assert is_bored("I am bored. I think. You are not!  I agree?Is this counted? Ironic.") == 3
assert is_bored("  I start here!\tI tab-leading.\n\nI newline-leading") == 3
assert is_bored("I. I? I!") == 0
assert is_bored("It is fine. Island time.") == 0
assert is_bored("You and I are going for a walk") == 0
