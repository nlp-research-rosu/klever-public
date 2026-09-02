# Filter by Substring K Verification Design

## Goal

Implement the HumanEval `filter_by_substring` function in the translator's Python subset, execute the translated constructor term with a locally written K semantics, and prove the function's universal filtering contract with `kprove`.

## Python implementation

`solution.py` preserves the prompt's import, signature, type annotations, and docstring. Its body returns a list comprehension that keeps each `string` from `strings` exactly when Python's `substring in string` predicate holds. This deliberately limits the translated term to `FuncDef`, `Params`, `Return`, `ListComp`, `CompFor`, `Name`, `Compare`, and `CmpOp` constructors.

`solution.mpy` is always regenerated from `solution.py` by the immutable `py2mpy.py`; it is not hand-authored.

## K architecture

`semantic.k` owns the constructor syntax and its meaning. It provides a compact big-step evaluator over a map environment. Definitions are installed in a function map, parameters are bound to argument values, returns evaluate their expression, names look up their binding, string membership uses K's string operation, and a one-generator list comprehension recursively traverses its source list while preserving order and duplicates.

The semantics is generic over the constructor patterns used by this solution rather than matching the function name or the exact complete program. Unsupported constructors remain outside this intentionally small semantics.

`verification.k` imports the semantics, mirrors the generated program as a K function term for proof use, and defines an independent recursive `filterRef` function on K lists. The reference retains a head exactly when the substring occurs in it.

`spec.k` imports verification support and states:

1. A symbolic reduction claim connects the exact translated program, for arbitrary `PyList` input and arbitrary `String` substring, to the generic comprehension evaluator.
2. A base claim and exhaustive keep/drop constructor-step claims prove that evaluator equal to `filterRef` by structural induction, with the recursive tail equality stated as the induction hypothesis.
3. A claim for the empty-list prompt example.
4. A claim for the four-element prompt example, including order preservation.

## Execution and proof flow

`prove.sh` uses strict shell settings. It regenerates `solution.mpy`, compiles the semantics, runs both prompt examples through `krun`, then invokes `kprove` once per positive claim so every required proof command has an independently visible exit status and `#Top` result. Build products go in `.kbuild/` inside the current directory.

## Validation and failure handling

Development follows a red/green sequence: first create claims that cannot compile or close without the implementation/semantics, observe the expected failure, then add the minimum semantics needed to close them. The final gate reruns translation, Python examples, K compilation, K execution, every positive proof, and shell syntax checking. If a proof cannot close after concrete diagnostics, the best artifacts and exact blocker are recorded in `NOTES.md`.

## Constraints

- Do not modify `prompt.py` or `py2mpy.py`.
- Keep every generated artifact under `/work`.
- Do not substitute finite testing for the universal contract claim.
- Claim success only when every positive `kprove` invocation prints `#Top` and exits zero.
