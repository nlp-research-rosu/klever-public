from typing import List


def parse_music(music_string: str) -> List[int]:
    result = []
    current = 0
    for char in music_string:
        if char == "o":
            current = 4
        elif char == ".":
            current = 1
        elif char == "|":
            if current == 4:
                current = 2
            result.append(current)
            current = 0
        else:
            if current == 4:
                result.append(current)
            current = 0
    if current == 4:
        result.append(current)
    return result
