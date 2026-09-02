#!/usr/bin/env python3
"""Finite adversarial check of the frozen find_max summary equations."""

from __future__ import annotations

import itertools
import json


Word = tuple[int, ...]


def source_operational_model(words: tuple[Word, ...]) -> Word:
    """Direct independent model of solution.py under the supplied operations."""
    best: Word = ()
    max_unique = 0
    for word in words:
        unique = len(set(word))
        if unique > max_unique:
            best = word
            max_unique = unique
        elif unique == max_unique and word < best:
            best = word
    return best


def k_summary(words: tuple[Word, ...], best: Word = (), score: int = 0):
    """The four guarded findMaxWords recurrences from verification.k."""
    if not words:
        return best, score
    word, rest = words[0], words[1:]
    unique = len(set(word))
    if unique > score:
        return k_summary(rest, word, unique)
    if unique == score and word < best:
        return k_summary(rest, word, score)
    if unique < score:
        return k_summary(rest, best, score)
    assert unique == score and not word < best
    return k_summary(rest, best, score)


def constant_empty(_words: tuple[Word, ...]) -> Word:
    return ()


def first_word(words: tuple[Word, ...]) -> Word:
    return words[0] if words else ()


def wrong_length_score(words: tuple[Word, ...]) -> Word:
    best: Word = ()
    score = 0
    for word in words:
        candidate_score = len(word)
        if candidate_score > score:
            best, score = word, candidate_score
        elif candidate_score == score and word < best:
            best = word
    return best


def main() -> None:
    word_universe: tuple[Word, ...] = (
        (),
        (-1,),
        (0,),
        (1,),
        (0, 0),
        (0, 1),
        (1, 0),
    )
    cases = [
        words
        for length in range(5)
        for words in itertools.product(word_universe, repeat=length)
    ]
    mismatches = []
    score_invariant_failures = []
    for words in cases:
        expected = source_operational_model(words)
        best, score = k_summary(words)
        if best != expected:
            mismatches.append({"words": words, "source": expected, "summary": best})
        if score != len(set(best)):
            score_invariant_failures.append(
                {"words": words, "best": best, "score": score}
            )

    adversarial = [
        ((0,),),
        ((1,), (0,)),
        ((0, 0), (1, 2)),
        ((),),
        ((), (1,)),
    ]
    mutations = {}
    for name, mutation in (
        ("constant_empty", constant_empty),
        ("first_word", first_word),
        ("wrong_length_score", wrong_length_score),
    ):
        witnesses = []
        for words in adversarial:
            expected = source_operational_model(words)
            observed = mutation(words)
            if observed != expected:
                witnesses.append(
                    {
                        "words": words,
                        "source": expected,
                        "mutation": observed,
                    }
                )
        mutations[name] = witnesses

    print(
        json.dumps(
            {
                "exhaustive_case_count": len(cases),
                "word_universe": word_universe,
                "source_summary_mismatch_count": len(mismatches),
                "score_invariant_failure_count": len(score_invariant_failures),
                "mutation_witnesses": mutations,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
