import re

from solution import valid_date


def oracle(date):
    match = re.fullmatch(r"([0-9]{2})-([0-9]{2})-([0-9]{4})", date)
    if match is None:
        return False
    month = int(match.group(1))
    day = int(match.group(2))
    limits = (0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
    return 1 <= month <= 12 and 1 <= day <= limits[month]


def main():
    tested = 0
    mismatches = []

    for year in ("0000", "2000", "9999"):
        for month in range(100):
            for day in range(100):
                date = f"{month:02d}-{day:02d}-{year}"
                tested += 1
                if valid_date(date) != oracle(date):
                    mismatches.append(date)

    malformed = (
        "",
        "03-11-200",
        "003-11-2000",
        "03/11/2000",
        "03-11/2000",
        "0a-11-2000",
        "03-b1-2000",
        "03-11-20c0",
        "０3-11-2000",
        "03-11-２０００",
    )
    for date in malformed:
        tested += 1
        if valid_date(date) != oracle(date):
            mismatches.append(date)

    print(f"tested={tested} mismatches={len(mismatches)}")
    if mismatches:
        print("first_mismatches=", mismatches[:10])
        raise SystemExit(1)


if __name__ == "__main__":
    main()
