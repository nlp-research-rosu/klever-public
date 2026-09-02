# Independent adversarial review: 66-digitsum

The candidate's positive K claims can be reconstructed and are
result-constraining, but they are not a legitimate proof of the HumanEval
contract. There are two independently fatal findings:

1. The submitted implementation and theorem count only ASCII `A` through `Z`.
   The trusted canonical uses `char.isupper()` on the unrestricted Python
   string domain. For the satisfying input `"É"`, the canonical result is 201
   while the submitted Python program, generated K execution, and formal
   postcondition all produce 0. This is a material source-contract narrowing,
   which the benchmark maps to `FAIL / NOT_LEGIT`.
2. The generated semantics proves the ASCII summary by a task-specific
   `loopString` bridge that never binds the loop variable and never executes
   the matched `If`, assignment, addition, or `ord` call. Its arbitrary
   continuation frame admits a concrete false state/control transition. A
   second exact-`If` bridge is also false on part of its match domain.

All audit work was performed from copied source in
`/tmp/audit-work/66-digitsum-audit`; no candidate-provided compiled definition
or cache was used.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- problem `66-digitsum`;
- condition `bare`;
- record layout `legacy-selected-stage1`;
- semantics mode `GENERATED_SEMANTICS`;
- no mounted reference-semantics tree.

The independent checker read and parsed `/audit-input.json`,
`/audit-campaign-lock.json`, `/run.json`, `/task.json`,
`/generation-result.json`, `invocation.json`, `metrics.json`, the present
`usage.json`, all 555 JSONL trace records, and the complete unstructured
generation prompt/output/last-message records. Historical runtime metrics are
not required by this layout. All required paths are real readable files or
directories, and the candidate, reference, and generation trees contain no
symlinks or unsupported nodes.

The campaign lock is byte-hash
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`
and exactly equals the `audit_campaign` object. Every declared per-file hash
matches its mounted bytes. The independently computed pipeline-contract
candidate-tree hash
`dd90e9dd22473230987142d9ba2ad102dc5937203f488ddd5caf18eff2e8ea57`
matches both the retained workspace and stage-result records; the trace-tree
hash
`292e624d7ba8b6e8756421fd84edf791e1f5564e0ab1bca364dd7dead56eca83`
matches `usage.json`. The checker also records, without conflating hash
serializations, the launcher snapshot digests from `audit-input.json`.

`/candidate/prompt.py` and `/candidate/py2mpy.py` are byte-identical to their
trusted mounted versions. As required for `GENERATED_SEMANTICS`,
`/reference/reference-semantics` does not exist. The required proof sources
`solution.py`, `solution.mpy`, `semantic.k`, `verification.k`, `spec.k`, and
`prove.sh` are present.

Evidence: [provenance checker](/audit-output/evidence/provenance_check.py),
[provenance log](/audit-output/evidence/stage1-provenance.log), and
[toolchain log](/audit-output/evidence/toolchain.log). The observed toolchain
is K 7.1.293 and Python 3.10.12. There is no audit-infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The trusted prompt asks `digitSum(s)` to sum the character codes of uppercase
characters and gives no ASCII-only input restriction. The trusted canonical
makes the intended predicate precise:

```python
sum(ord(char) if char.isupper() else 0 for char in s)
```

Thus the intended domain is Python strings, empty string returns 0, and every
character for which Python `str.isupper()` is true contributes `ord(char)`.

The submitted program instead uses:

```python
if "A" <= char <= "Z":
    total = total + ord(char)
```

That is equivalent only on an ASCII-restricted domain that the source contract
does not impose.

### Translator identity

Running the trusted translator on the submitted source produced a file
byte-identical to `solution.mpy`; both hashes are
`a2f334bc86693f03e6fa6fd533bdeea1daeb7cb4b5ad778141b075d9722bd2ef`.
The translator and `cmp` both exited 0. Evidence:
[translator log](/audit-output/evidence/stage2-translator-identity.log).

### Independent differential

The independent differential imports the trusted canonical and submitted entry
points. It checks all six examples, empty input, both sides of the `A` and `Z`
branch boundaries, representative mixed strings, all 1,114,112 Python
one-character values, and 2,000 deterministic generated strings.

- All prompt examples and ASCII boundaries match.
- There are 1,885 singleton mismatches.
- There are 1,809 mismatches among the 2,000 generated strings.
- Concrete witness: `"É"` gives canonical 201 and candidate 0.
- Concrete mixed witness: `"AΩZ"` gives canonical 1092 and candidate 155.

Evidence: [differential script](/audit-output/evidence/differential_test.py) and
[results](/audit-output/evidence/stage2-differential.log).

This material divergence on the intended domain is independently sufficient
for `FAIL / NOT_LEGIT`.

## 3. Clean proof reconstruction

The source-only scratch copy was compiled into new output directories with:

```text
kompile semantic.k --backend llvm --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-semantic-llvm-kompiled

kompile semantic.k --backend haskell --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-semantic-haskell-kompiled
```

Both builds exited 0. Evidence:
[LLVM build](/audit-output/evidence/stage3-kompile-llvm.log) and
[Haskell build](/audit-output/evidence/stage3-kompile-haskell.log).

Fresh generated-semantics execution was compared with both Python programs on
18 normal, empty, branch-boundary, escaping, newline, BMP Unicode, and astral
Unicode inputs. Every K result equals the submitted ASCII-only Python result.
On `"É"`, `"Ω"`, `"AΩZ"`, and `"𝔄"`, K disagrees with the trusted canonical in
the same way as the submitted implementation. Evidence:
[K differential script](/audit-output/evidence/k_semantics_differential.py)
and [K concrete log](/audit-output/evidence/stage3-k-concrete.log).

The original positive proof command was:

```text
kprove spec.k --definition audit-semantic-haskell-kompiled \
  --spec-module SPEC
```

It printed `#Top` and exited 0. To audit the two obligations modularly, the loop
claim was also run alone and printed `#Top` with exit 0. The entry claim was
then run with that separately established loop claim marked trusted; it printed
`#Top` and exited 0. This is the appropriate modular dependency: removing the
loop circularity makes the unbounded entry loop unprovable by finite unrolling.

Evidence:

- [all original claims](/audit-output/evidence/stage3-kprove-all.log);
- [loop claim alone](/audit-output/evidence/stage3-kprove-loop.log);
- [entry using established loop claim](/audit-output/evidence/stage3-kprove-entry.log);
- [labeled audit spec](/audit-output/evidence/spec-labeled.k).

Transparent failed audit-attempt logs are retained separately: the first entry
split omitted its required invariant, one concurrent K invocation produced a
transient Java-launch error, and one label spelling was rejected. They are not
candidate proof failures and do not replace the successful clean commands.

## 4. Adequacy and real-program pinning

### Claims in plain language

The entry claim has no precondition. For every K string `S`, it starts with the
submitted constructor module, input `S`, empty environment, and `noResult`; it
requires the computation and environment to become empty and the result to be
`intVal(upperAsciiSum(S))`.

The loop claim says that for every K-string suffix `S`, integer accumulator
`A`, arbitrary input string, and frame map not containing `total`, the exact
task-specific loop followed by `return total` produces
`intVal(A + upperAsciiSum(S))` and clears the environment.

Both preconditions are satisfiable:

- entry witness: `S = ""`;
- loop witness: `S = "AB"`, `A = 7`, input `"witness-input"`, and
  `FRAME = ("other" |-> intVal(99))`; its stated destination is 138.

For the concrete satisfying entry input `"AB"`, generated K, submitted Python,
and canonical Python all return 131. For the equally satisfying input `"É"`,
the formal destination and submitted implementations return 0, but canonical
Python returns 201.

### Mechanical program identity

The trusted translator identity links `solution.py` to `solution.mpy`. The
parsed constructor JSON for `solution.mpy` was then compared with the parsed
left-hand program term of the entry claim. Both canonical JSON terms hash to
`d06d4a8b7b6041d2c13165ec516c94889457f3d656d4761b00c96c163489f6c7`
and compare equal. This also accounts mechanically for the user-list unit that
is printed as an empty argument in `.mpy` source and as `.Stmts` inside a K
claim.

Evidence: [constructor comparison](/audit-output/evidence/constructor_compare.py)
and [pinning log](/audit-output/evidence/stage4-constructor-pinning.log).
The claim therefore pins the submitted constructor term; it is not a
substituted program and its result is not a free variable or tautology.

### Body sensitivity

Changing the actual constructor body from `total = 0` to `total = 1`, while
retaining the original result obligation, parses successfully but fails with
`WarnStuckClaimState` and the residual inequality
`upperAsciiSum(S) + 1 =/= upperAsciiSum(S)`. The dry run exits 0 and proof exits
1. Evidence:
[body mutation](/audit-output/evidence/spec-body-mutation.k) and
[body-sensitivity log](/audit-output/evidence/stage4-body-sensitivity.log).

Program-term pinning and result sensitivity pass. Adequacy still fails because
the postcondition is the wrong ASCII-only source property and because the
generated semantics does not execute every material operation in that pinned
term.

## 5. Rule-by-rule static soundness review

The complete inventory lists all 28 local syntax/declaration groups, all 24
ordinary semantic rules, all four verification simplifications, the
configuration, imports, and both claims:
[exhaustive inventory](/audit-output/evidence/rule-inventory.md). The extraction
command and attributes search are in
[inventory log](/audit-output/evidence/stage5-static-inventory-command.log).

There are no local `[total]`, `[functional]`, opaque, fresh, priority, macro,
`owise`, or numeric-priority declarations. The only local proof-directed
attributes are `[function]` and `[simplification]`. The source constructs map
as follows:

| Submitted construct | Declaration | Operational handling |
|---|---|---|
| module/function/parameter | `Module`, `FuncDef`, `Params` | exact entry rule R15 |
| statement sequence | `Stmts` | R16-R17 |
| initialization assignment | `Assign`, `Name`, `Int` | R01, R03-R05, R18 |
| `for char in s` | `For`, `Name` | R20 then task-specific R21-R23 |
| chained `if` | `If`, `Compare`, `CmpOp`, `Str` | syntactically matched and skipped by R22; separate shortcut R19 |
| integer addition | `BinOp` | R06/R09 if executed; skipped in loop by R22 |
| `ord(char)` | `Call` | R07/R10 if executed; skipped in loop by R22 |
| return | `Return` | R24 |

R01-R07, R09, R12-R13, R16-R18, R21, R23-R24 are faithful on the
well-typed values actually supplied to their matches. R10, R11, R14, and the
verification contribution rule R27 lack length-one guards around `ordChar`;
their target-path callers supply one-character substrings, so this is a
narrower partiality/evidence gap rather than an additional claimed false target
result. The verification recursion R25-R27 has disjoint base/recursive guards
and decreases string length. R28 is true integer associativity, consistently
oriented toward right association. There are no conflicting equation overlaps.

Two operational rules fail the generated-language audit:

1. **R19, `semantic.k:111-123`: false complete match domain.** It replaces the
   exact `If` statement by an unconditional `pythonUpperOrd` computation,
   skipping Python's chained-comparison short circuit. Its match admits any
   string bound to `X`. With the same exact statement using `X = "s"` and valid
   input `s = ""`, Python follows the false branch and returns 0. Fresh Haskell
   K execution instead returns `#Bottom` because the bridge reaches
   `ordChar("")`. This is a concrete false control/state conclusion over a
   satisfying string input, not a speculative concern. Evidence:
   [witness source](/audit-output/evidence/if_short_circuit_witness.py) and
   [execution log](/audit-output/evidence/stage5-if-short-circuit-witness.log).
2. **R22, `semantic.k:130-148`: task-answer bridge with a false state
   footprint.** It pattern-matches the exact property-bearing loop body, but
   rewrites directly to `addUpper(first-character)` and recursion. It never
   binds `char`, never evaluates the comparison, and never executes the
   assignment/addition/`ord` call. Its framed `<k> ... </k>` accepts arbitrary
   continuations. A boundary witness retains the same loop and immediately
   returns `char`: for input `"A"`, Python returns `"A"`, while K has only `s`
   and `total` in the environment and fails at
   `eval(Name("char"), ...)`. Thus the bridge's transition falsely omits the
   Python loop-variable state on its declared match domain. Evidence:
   [witness source](/audit-output/evidence/loop_observer.py) and
   [execution log](/audit-output/evidence/stage5-loop-context-witness.log).

No bridge-free universal connection theorem narrows either rule to a sound
complete context or proves state/control equivalence. R22 is the rule the
submitted program actually uses. Its `addUpper`/`pythonUpperOrd` RHS duplicates
the ASCII contribution used by `upperAsciiSum`; the positive proof therefore
relates two hand-written ASCII recursions while bypassing the submitted loop's
material operations. The 18 fresh concrete K comparisons support only the
tested output values for the exact `return total` continuation. They cannot
replace the missing universal operational connection.

Under the required `writing-semantics` boundary, minimal syntax coverage would
have been acceptable. Task-specific answer execution and a rule that skips
observable binding/control are not merely minimal coverage.

## 6. Fresh non-vacuity test

The fresh mutation leaves the pinned program unchanged and changes the entry
destination to:

```k
intVal(upperAsciiSum(S) +Int 1)
```

`S = ""` satisfies the original unguarded precondition and is demonstrably
false for the mutation: actual result 0 versus required result 1. The mutation
dry run exits 0, so it builds and reaches the proof backend. The proof exits 1
with `WarnStuckClaimState`; its residual explicitly contains
`upperAsciiSum(S) +Int 1 =/= upperAsciiSum(S)`. This is the expected unmet
result obligation, not a parser error, timeout, unrelated crash, or unreachable
mutation.

Evidence: [fresh mutation](/audit-output/evidence/spec-vacuity.k) and
[non-vacuity log](/audit-output/evidence/stage6-non-vacuity.log).

The K claim is result-constraining and non-vacuous. That does not cure the
contract and semantics failures.

## 7. Proven versus assumed accounting

### What the successful K proof actually establishes

Conditional on the candidate-generated K theory, the submitted constructor
term maps every K string `S` to the recursively defined ASCII-only
`upperAsciiSum(S)`. The loop claim supplies the circularity that relates
`loopString` to the same summary. The theorem is universal over K strings and
not a finite unrolling, and the false-postcondition test shows it discriminates
the result.

It does **not** establish that the trusted HumanEval canonical and submitted
Python functions agree on every Python string. It also does not establish,
using bridge-free semantics, that executing the submitted Python loop body has
the `loopString` transition used by the proof.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K 7.1.293 compiler/backend and built-in mathematical `Int`, `Bool`, `Map`, list/K-sequence, `String`, `lengthString`, `substrString`, and `ordChar` operations | all builds, execution, and proof | Normal low-level trust boundary; versions and fresh commands recorded. |
| K-string/Python-string correspondence and K `ordChar`/Python `ord` correspondence on length-one strings | concrete semantics and ASCII summary | Informal modeling bridge, finitely supported on normal, escaped, BMP, and astral cases; not a universal Python semantics theorem. |
| R15 direct-entry convention and syntactic pinning of `ord` | entry claim | Acceptable only for this closed generated module; there is no general Python function-binding/call semantics. |
| R19 exact-`If` operational bridge | general declared `If` behavior, though bypassed by target R22 | Illegitimate complete match domain; concrete empty-string false transition yields `#Bottom`. |
| R22/R23 task-specific loop summary | loop claim and entry claim | Illegitimate property-bearing operational bridge. No universal connection theorem; skips material execution and has a concrete loop-variable state/control counterexample. |
| R25-R28 ASCII contract functions and simplifications | formal postconditions | Equations are ordinary mathematics on their reachable domains, but they formalize an ASCII-only property rather than the trusted source contract. |
| Fresh differential tests | empirical K-to-submitted-Python and submitted-to-canonical bridges | Reproducible finite evidence only. The exhaustive Python singleton test refutes, rather than supports, full source-contract equivalence. |

Gate A fails because the target proof depends on R22 and there is no sound
full-context operational connection; R19 is also false on its declared domain.
Gate B independently fails because the proved ASCII property materially
narrows the canonical `str.isupper()` contract. Gate C evidence is reproducible
but cannot repair either failure.

The clean `#Top`, exact constructor identity, body sensitivity, and
non-vacuity are genuine positive facts about the candidate theory. They do not
make that theory a legitimate proof of the real HumanEval task. The benchmark's
explicit mapping makes this material source-contract narrowing, as well as the
task-answer operational bridge, `FAIL / NOT_LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
