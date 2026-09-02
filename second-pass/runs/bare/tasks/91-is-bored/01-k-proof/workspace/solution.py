def is_bored(S):
    count = 0
    for sentence in S.replace("!", ".").replace("?", ".").split("."):
        if sentence.strip().startswith("I "):
            count += 1
    return count
