#!/usr/bin/env python3
"""Independent finite sensitivity checks for the scanner definitions."""

from __future__ import annotations

import itertools
import json
from dataclasses import dataclass


ALPHABET = ("(", ")", " ")


@dataclass(frozen=True)
class State:
    depth: int
    current: str
    output: tuple[str, ...]
    last: str


def operational_run(chars: str, state: State) -> State:
    """Operational reading of source plus semantic.k's saturating PInt."""
    depth = state.depth
    current = state.current
    output = list(state.output)
    last = state.last
    for ch in chars:
        # semantic.k's #loop first binds ch for every character.
        last = ch
        if ch != " ":
            current += ch
            if ch == "(":
                depth += 1
            else:
                # semantic.k implements zero - 1 as zero for PInt.
                depth = max(depth - 1, 0)
                if depth == 0:
                    output.append(current)
                    current = ""
    return State(depth, current, tuple(output), last)


def run_spec(chars: str, state: State) -> State:
    """Direct reading of verification.k lines 17-22."""
    depth = state.depth
    current = state.current
    output = list(state.output)
    last = state.last
    for ch in chars:
        if ch == " ":
            last = " "
        elif ch == "(":
            depth += 1
            current += "("
            last = "("
        elif depth == 0:
            output.append(current + ")")
            current = ""
            last = ")"
        elif depth == 1:
            output.append(current + ")")
            current = ""
            depth = 0
            last = ")"
        else:
            depth -= 1
            current += ")"
            last = ")"
    return State(depth, current, tuple(output), last)


def mutated_run_spec(chars: str, state: State, mutation: str) -> State:
    depth = state.depth
    current = state.current
    output = list(state.output)
    last = state.last
    for ch in chars:
        if ch == " ":
            if mutation == "space_appends":
                current += " "
            last = " "
        elif ch == "(":
            if mutation != "lp_no_increment":
                depth += 1
            current += "("
            last = "("
        elif depth == 0:
            output.append(current + ")")
            current = ""
            last = ")"
        elif depth == 1:
            if mutation != "depth_one_no_emit":
                output.append(current + ")")
                current = ""
            depth = 0
            last = ")"
        else:
            if mutation == "nested_rp_emits":
                output.append(current + ")")
                current = ""
            else:
                current += ")"
            depth -= 1
            last = ")"
    return State(depth, current, tuple(output), last)


def all_sequences(max_length: int):
    for length in range(max_length + 1):
        for chars in itertools.product(ALPHABET, repeat=length):
            yield "".join(chars)


def main() -> None:
    initial_states = [
        State(depth, current, output, last)
        for depth in range(4)
        for current in ("", "(")
        for output in ((), ("()",))
        for last in ("", "(", ")", " ")
    ]
    cases = 0
    mismatch = None
    for state in initial_states:
        for chars in all_sequences(5):
            cases += 1
            observed = operational_run(chars, state)
            summarized = run_spec(chars, state)
            if observed != summarized:
                mismatch = {
                    "chars": chars,
                    "initial": state.__dict__,
                    "operational": observed.__dict__,
                    "summary": summarized.__dict__,
                }
                break
        if mismatch is not None:
            break

    mutation_witnesses: dict[str, object] = {}
    for mutation in (
        "space_appends",
        "lp_no_increment",
        "depth_one_no_emit",
        "nested_rp_emits",
    ):
        witness = None
        for state in initial_states:
            for chars in all_sequences(5):
                expected = operational_run(chars, state)
                mutated = mutated_run_spec(chars, state, mutation)
                if expected != mutated:
                    witness = {
                        "chars": chars,
                        "initial": state.__dict__,
                        "operational": expected.__dict__,
                        "mutated": mutated.__dict__,
                    }
                    break
            if witness is not None:
                break
        mutation_witnesses[mutation] = witness

    examples = {
        text: operational_run(text, State(0, "", (), "")).output
        for text in (
            "",
            "( ) (( )) (( )( ))",
            "()(())(()())",
            "(((())))",
            ")(",
        )
    }
    status = (
        "PASS"
        if mismatch is None
        and all(value is not None for value in mutation_witnesses.values())
        else "FAIL"
    )
    print(
        json.dumps(
            {
                "alphabet": list(ALPHABET),
                "initial_state_count": len(initial_states),
                "exhaustive_sequence_max_length": 5,
                "comparison_cases": cases,
                "operational_vs_runSpec_mismatch": mismatch,
                "counterfactual_mutation_witnesses": mutation_witnesses,
                "end_to_end_examples": examples,
                "status": status,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
