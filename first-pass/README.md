# First pass — deriving the semantics and proving all 164 by hand

This directory archives the first pass of the program: a K-framework
semantics for the Python subset exercised by HumanEval was derived
bottom-up, and the partial correctness of all 164 HumanEval solutions
was proved against it, one problem at a time, with a human in the loop.
Everything the later automation depends on came out of this pass: the
unified reference semantics, the proof methodology, and the **kit** that packages the methodology as agent skills.

## How it worked

1. **Parse everything first.** A pure CPython-AST-to-K transliterator
   (`py2mpy.py`) was driven until all 164 solutions parsed; anything it
   could not express named the construct the semantics still had to
   cover.
2. **Prove per problem.** Each problem got the minimal semantics it
   needed plus a machine-checked proof (`kprove` ending in `#Top` — K's
   proof-complete signal) before moving on.
3. **Unify and migrate.** The per-problem semantics were consolidated
   into a single unified semantics that runs every question, and each
   proof was re-homed onto it, with reusable lemmas lifted into a shared
   library.
4. **Gate every proof.** A proof counts only if the reachability proof
   closes (`#Top`), a concrete smoke run passes, a corrupted
   postcondition makes the proof fail (non-vacuity), and the summary
   axioms match CPython on randomized inputs (differential testing).

## What is where

- [`questions/`](questions/) — one directory per HumanEval problem:
  `solution.py`, `spec.k` (the reachability claims), `verification.k`
  (invariants, summary functions, lemmas), smoke and differential
  tests.
- [`semantic/`](semantic/) — the unified reference semantics and shared
  lemma library, frozen as it stood at the end of this pass (`src/`),
  with its notes and tests. The campaign in
  [`../second-pass/`](../second-pass/) pinned and evolved its own copy;
  the live, still-developed semantics moved to the org's `semantics`
  repository.
- [`references/`](references/) — the ~112-repo corpus of proven K
  techniques (submodules) consulted when a construct was hard.
- [`scripts/`](scripts/) — the dataset splitter, `py2mpy.py`, and the
  re-verification driver.
- `data/` — regenerable HumanEval dissection output (gitignored;
  rebuilt by `scripts/dissect_humaneval.py`).

The second pass — three arms, six stages, independent audits, 164/164
in the kit arm — is archived in [`../second-pass/`](../second-pass/),
with a guided tour in [`../showcase/`](../showcase/README.md).
