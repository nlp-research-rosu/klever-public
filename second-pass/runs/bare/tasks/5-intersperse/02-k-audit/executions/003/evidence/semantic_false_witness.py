#!/usr/bin/env python3
"""Python side of the generated-semantics parameter-binding counterexample."""


def f(x, y):
    return numbers


def main() -> int:
    try:
        value = f([1], 2)
    except BaseException as error:
        print(f"PYTHON_OUTCOME exception {type(error).__name__}: {error}")
        return 0 if isinstance(error, NameError) else 1
    print(f"PYTHON_OUTCOME return {value!r}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
