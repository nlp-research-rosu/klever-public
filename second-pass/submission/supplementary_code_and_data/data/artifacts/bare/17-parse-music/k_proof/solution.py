from typing import List


def parse_music(music_string: str) -> List[int]:
    beats = []
    for note in music_string.split(" "):
        if note == "o":
            beats = beats + [4]
        elif note == "o|":
            beats = beats + [2]
        else:
            beats = beats + [1]
    return beats
