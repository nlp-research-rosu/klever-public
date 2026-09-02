from itertools import product

from solution import parse_music


LEGEND = {"o": 4, "o|": 2, ".|": 1}


def contract_oracle(music_string):
    return [LEGEND[note] for note in music_string.split()]


def layouts(notes):
    if not notes:
        return ("", " ", "\t", "\n", "\r\n")
    cases = []
    for separator in (" ", "  ", "\t", "\n", "\r\n"):
        body = separator.join(notes)
        cases.extend((body, separator + body, body + separator,
                      separator + body + separator))
    return tuple(cases)


checked = 0
mismatches = []
for length in range(6):
    for notes in product(tuple(LEGEND), repeat=length):
        for text in layouts(notes):
            checked += 1
            expected = contract_oracle(text)
            actual = parse_music(text)
            if actual != expected:
                mismatches.append((text, expected, actual))

prompt_example = "o o| .| o| o| .| .| .| .| o o"
checked += 1
if parse_music(prompt_example) != contract_oracle(prompt_example):
    mismatches.append((
        prompt_example,
        contract_oracle(prompt_example),
        parse_music(prompt_example),
    ))

print("differential cases=" + str(checked) +
      " mismatches=" + str(len(mismatches)))
if mismatches:
    print(mismatches[:5])
    raise SystemExit(1)
