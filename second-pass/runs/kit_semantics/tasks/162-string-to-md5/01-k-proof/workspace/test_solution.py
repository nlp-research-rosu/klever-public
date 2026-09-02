import random
import re
import string
import subprocess

from solution import string_to_md5


def openssl_md5(text):
    completed = subprocess.run(
        ["openssl", "dgst", "-md5"],
        input=text.encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    return completed.stdout.decode("ascii").rsplit("=", 1)[1].strip()


cases = [
    "",
    "Hello world",
    "a",
    "abc",
    "message digest",
    "abcdefghijklmnopqrstuvwxyz",
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
    "1234567890" * 8,
    "\0",
    "\n",
    "π",
    "🙂",
    "漢字",
]

rng = random.Random(20260730)
alphabet = string.ascii_letters + string.digits + string.punctuation + " \n\tπ🙂"
for _ in range(200):
    length = rng.randrange(0, 257)
    cases.append("".join(rng.choice(alphabet) for _ in range(length)))

mismatches = []
for text in cases:
    expected = None if text == "" else openssl_md5(text)
    actual = string_to_md5(text)
    if actual != expected:
        mismatches.append((text, expected, actual))
    if actual is not None and re.fullmatch(r"[0-9a-f]{32}", actual) is None:
        mismatches.append((text, "32 lowercase hex digits", actual))

print(f"DIFFERENTIAL_CASES={len(cases)} MISMATCHES={len(mismatches)}")
print(f"PROMPT_EXAMPLE={string_to_md5('Hello world')}")
print(
    "UTF8_BOUNDARY text='π' "
    f"codepoints={[ord(character) for character in 'π']} "
    f"bytes={list('π'.encode('utf-8'))}"
)
if mismatches:
    raise AssertionError(mismatches[:3])
