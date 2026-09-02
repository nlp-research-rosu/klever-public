def parse_music(music_string):
    note_map = {'o': 4, 'o|': 2, '.|': 1}
    return [note_map[x] for x in music_string.split(' ') if x]


# Smoke checks — the HumanEval/17 dataset `check` cases (bare-value asserts).
assert parse_music('') == []
assert parse_music('o o o o') == [4, 4, 4, 4]
assert parse_music('.| .| .| .|') == [1, 1, 1, 1]
assert parse_music('o| o| .| .| o o o o') == [2, 2, 1, 1, 4, 4, 4, 4]
assert parse_music('o| .| o| .| o o| o o|') == [2, 1, 2, 1, 4, 2, 4, 2]
