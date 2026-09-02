# Independent adversarial review: 37-sort-even

The candidate reconstructs a real, non-vacuous K proof for a raw-integer-list
fragment, but it does **not** prove the HumanEval contract as written.  The
prompt annotates the argument only as `list`; it does not restrict elements to
integers.  Both trusted canonical Python and generated Python correctly handle
homogeneous orderable non-integers, while the generated K semantics explicitly
models list elements as K `Int` values and fails on a concrete string-list
witness.  This is a material source-contract domain narrowing.  Under the
benchmark's explicit mapping, the otherwise sound-but-limited result is
`FAIL / NOT_LEGIT`.

## 1. Input and provenance integrity

The launcher declares `record_layout = legacy-selected-stage1`,
`condition = bare`, and `semantics_mode = GENERATED_SEMANTICS`.  The campaign
object in `/audit-input.json` is exactly equal to
`/audit-campaign-lock.json`; the lock's SHA-256 is the recorded
`ad5dfcc0...a78d745`.

All launcher-declared container paths exist and are readable.  The required
legacy-selected-stage1 records are regular, non-symlink files:

- `/run.json`, `/task.json`, and `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`, `usage.json`,
  `codex-last.txt`, `codex-output.log`, and `prompt.txt`; and
- the single 432-line structured JSONL trace below
  `/generation-evidence/codex-trace/`.

The optional `usage.json` is present. Historical `runtime-metrics.json` is not
required by this legacy layout and was not fabricated.  Every one of the 432
trace lines parses as JSON.  The trace contains 63 custom tool calls, 25
function calls, seven assistant messages, and a terminal task-complete event.
I scanned the complete 45,400-line `codex-output.log`; its historical failures
and final `#Top` are treated only as untrusted generation claims.

Independent SHA-256 checks match the launcher records for the campaign lock,
trusted prompt, trusted translator, canonical implementation, candidate prompt,
candidate translator, run/task/result/invocation records, metrics, usage,
generation prompt, last message, output log, legacy records, and trace file.
The retained candidate's installed pipeline tree digest is
`de3c9455...9957a`, exactly the `workspace_sha256` in both
`generation-result.json` and `invocation.json`.  The trace file hash
`c44291c8...72d51` matches both generation manifests, and its installed
pipeline tree digest `9c198f51...41dd1` matches `usage.json`.

`/candidate/prompt.py` and `/candidate/py2mpy.py` are byte-identical to
`/reference/prompt.py` and `/reference/py2mpy.py`.  Neither
`/reference/reference-semantics` nor `/candidate/reference-semantics` exists,
which is the required generated-semantics boundary.  A recursive type scan
found only directories and regular files, not symlinks or special entries.
There is no infrastructure breach.

Evidence:
[`stage1-provenance-full.txt`](evidence/stage1-provenance-full.txt),
[`stage1-hashes-and-trace-shape.txt`](evidence/stage1-hashes-and-trace-shape.txt),
[`stage1-candidate-tree.txt`](evidence/stage1-candidate-tree.txt), and
[`stage1-generation-claims-scan.txt`](evidence/stage1-generation-claims-scan.txt).

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For an input list `l`, return a list of the same length such that:

1. every odd-indexed element is unchanged;
2. the output's even-indexed subsequence is the sorted version of the input's
   even-indexed subsequence; and
3. consequently, no even-position value is added or lost.

The written annotation is `list`, not `list[int]`.  The natural Python domain
therefore includes lists whose even elements are mutually orderable.  The
trusted canonical implementation uses Python's list sort and exhibits this
behavior for integers, floats, booleans, and strings.

The generated implementation extracts every second element recursively,
insertion-sorts that subsequence, then recursively rebuilds the original list
around the untouched odd positions.  This is a different but faithful
algorithm at Python level.

### Translator identity

Running the trusted translator:

```text
python3 /reference/py2mpy.py \
  /tmp/audit-work/37-sort-even/solution.py \
  > /tmp/audit-work/37-sort-even/regenerated-solution.mpy
```

exited 0.  `cmp -s` against the submitted `solution.mpy` exited 0; both files
have SHA-256 `2144d649...917705`.

### Independent differential

[`differential_test.py`](evidence/differential_test.py) imports the trusted and
generated modules independently and also checks the contract directly.  It
covered:

- both prompt examples;
- empty, singleton, two-element, odd/even length, equal, ordered, reversed,
  negative, and duplicate branch boundaries;
- all 97,656 integer lists of lengths 0 through 7 over
  `{-2,-1,0,1,2}`;
- 1,000 deterministic lists of lengths 0 through 40 over
  `[-10000,10000]`; and
- homogeneous string, float, and boolean lists.

It exited 0 after 98,672 cases with zero implementation mismatches and zero
contract failures.  In particular:

```text
["b", "odd", "a"] -> ["a", "odd", "b"]
```

for both Python implementations.

Evidence:
[`stage2-fidelity-and-differential.txt`](evidence/stage2-fidelity-and-differential.txt).

## 3. Clean proof reconstruction

I copied only source artifacts, by explicit filename, to
`/tmp/audit-work/37-sort-even`.  No candidate-provided compiled definition or
cache was copied.

### Fresh builds and executions

Fresh LLVM compilation of `semantic.k` exited 0.  It emitted a significant
warning that `headInt` is non-exhaustive despite being declared
`[function,total,smtlib(headInt)]`.  Fresh Haskell compilation of
`verification.k` exited 0.

Concrete LLVM executions of the actual regenerated `solution.mpy` all exited 0
and matched independent Python for:

- `[]`;
- `[4]`;
- both prompt examples;
- equal even-position values;
- a reversed, odd-length case; and
- a negative odd-length case.

These cases exercise both equality outcomes, all `<=`/`>` outcomes including
equality, both rebuild branches, recursive base cases, function lookup,
one- and two-argument binding, calls, list literals, concatenation, indexing,
and the `[1:]`/`[2:]` slices.

The source-contract witness `["b","odd","a"]` does not execute. `krun` exits
113 at:

```text
headInt ( ListItem ( "b" )
ListItem ( "odd" )
ListItem ( "a" ) )
```

### Positive claims

The complete fresh command:

```text
kprove spec.k --definition verification-kompiled \
  --spec-module SPEC -w none
```

exited 0 and printed `#Top`, closing all ten claims.

The five concrete/symbolic examples and the leaf helper claims
`even-correct`, `insert-correct`, and `rebuild-correct` also printed `#Top`
when selected individually.  `sort-correct` legitimately depends on
`insert-correct`; selecting
`insert-correct,sort-correct` closes with `#Top`. `top-correct` depends on
`even-correct`, `insert-correct`, `sort-correct`, and `rebuild-correct`; that
five-claim closure also exits 0 with `#Top`.  Filtering `sort-correct` alone
removes its required insertion theorem and produces a stuck residual; this is
a dependency diagnostic, not the positive reconstruction.

Evidence:
[`stage3-kompile-semantic-llvm.log`](evidence/stage3-kompile-semantic-llvm.log),
[`stage3-concrete-krun.log`](evidence/stage3-concrete-krun.log),
[`stage3-noninteger-krun.log`](evidence/stage3-noninteger-krun.log),
[`stage3-kompile-verification-haskell.log`](evidence/stage3-kompile-verification-haskell.log),
[`stage3-kprove-all.log`](evidence/stage3-kprove-all.log),
[`stage3-individual-kprove.log`](evidence/stage3-individual-kprove.log), and
[`stage3-dependency-closure-kprove.log`](evidence/stage3-dependency-closure-kprove.log).

## 4. Adequacy and real-program pinning

### Claims in plain language

| Claim | Precondition and postcondition |
|---|---|
| `empty-example` | With no precondition, the embedded entry program maps `[]` to `[]`. |
| `prompt-example` | With no precondition, it maps `[5,6,3,4]` to `[3,6,5,4]`. |
| `first-prompt-example` | With no precondition, it maps `[1,2,3]` to itself. |
| `symbolic-four-ordered` | For arbitrary integers `A,B,C,D` with `A <= C`, it returns `[A,B,C,D]`. |
| `symbolic-four-reversed` | For arbitrary integers `A,B,C,D` with `A > C`, it returns `[C,B,A,D]`. |
| `even-correct` | For any K list `L`, executing the real `even_values` helper returns `evenPositions(L)`. |
| `insert-correct` | For integer `X` and any K list `L`, executing the real insertion helper returns `insertReference(pyInt(X),L)`. |
| `sort-correct` | For any K list `L`, executing the real sort helper returns `sortReference(L)`. |
| `rebuild-correct` | For any K lists `L,EVENS`, executing the real rebuild helper returns `rebuildReference(L,EVENS)`. |
| `top-correct` | For any K list `L`, executing the embedded entry program returns exactly `sortEvenReference(L)`. |

Every RHS fixes the returned list; there is no free result variable, tautology,
or one-way implication in a positive claim.  [`claim_witnesses.py`](evidence/claim_witnesses.py)
provides a concrete satisfying state for all ten preconditions.  The entry
witnesses agree with both Python implementations, and helper witnesses agree
with direct Python helper execution.

### Program identity

Trusted regeneration proves the submitted `solution.mpy` corresponds to
`solution.py`.  Separately:

1. `kast` parsed `solution.mpy` as a `Program`;
2. `krun --term` evaluated `solutionProgram()` from `verification.k`; and
3. their pretty constructor terms were byte-identical (`cmp` exit 0, common
   SHA-256 `66b85b00...4553`).

This mechanically checks the function bindings, helper bodies, entry body,
operators, calls, indices, and slices. The only surface normalization is K's
explicit empty-list constructors such as `.Exprs`.

A separate body-sensitivity copy changed the **embedded** `sort_even` body to
`Return(Name("l"))`.  The mutated definition built successfully, but the
prompt-example proof exited 1 with the mutated body visible in the residual.
Thus the claim depends on the program term it executes; merely changing an
external source file was not used as the test.

Evidence:
[`stage4-constructor-pinning.txt`](evidence/stage4-constructor-pinning.txt),
[`stage4-body-sensitivity.log`](evidence/stage4-body-sensitivity.log), and
[`stage4-claim-witnesses.txt`](evidence/stage4-claim-witnesses.txt).

### Property and domain adequacy

`top-correct` proves refinement to `sortEvenReference`, whose equations
structurally express extraction, insertion sort, and rebuilding.  The candidate
does not separately prove in K that `sortReference` is sorted and a
permutation or that rebuilding preserves every odd position. Those are simple
informal induction obligations and are strongly supported by the independent
tests, but they remain an informal summary-to-contract bridge.

More importantly, the claimed/intended domain is not aligned.  No entry
precondition restricts `L` to integer elements, yet `semantic.k` comments that
runtime lists contain K `Int` values and its evaluator can only reconstruct
such lists.  Partial correctness over stuck non-integer paths cannot substitute
for the terminating behavior of the actual Python program.  The string witness
shows a material class of source-contract inputs is excluded.

## 5. Rule-by-rule static soundness review

The exhaustive inventory is
[`RULE-INVENTORY.md`](evidence/RULE-INVENTORY.md). It lists:

- every local syntax/configuration declaration;
- all four semantic helper functions and all six proof-side reference
  functions;
- the `[total]` and `smtlib` attributes;
- all 39 rules in `semantic.k`;
- all 13 rules in `verification.k`;
- all ten claims and their dependency structure; and
- the rule mapping for every constructor in `solution.mpy`.

There are no local priority, `owise`, `[functional]`, `[simplification]`, or
`[concrete]` declarations, no proof-local operational rewrite, and no
unconstrained result oracle.

### Integer fragment

For raw-integer lists and the control paths used by this submitted program:

- `dropList`, positive slicing, `headInt`, indexing, concatenation, integer
  equality/order, and list construction agree with Python;
- function lookup and binding select the exact submitted functions/arguments;
- call arguments, comparison operands, binary operands, and literal items are
  evaluated left-to-right;
- return and branch control are preserved;
- all guard pairs are disjoint and exhaustive for the relevant integer cases;
  and
- recursion descends by one or two list elements.

The `If` rule discards a trailing statement suffix, but every actual `If` is
the complete function body and every branch returns, so no reachable submitted
control is lost. Missing exceptions, negative slices, missing bindings, and
bad arities are narrower language gaps not reached by the integer entry
program.

The proof-side equations are truthful recursive definitions on integer lists.
`solutionProgram` names the parsed source rather than replacing its execution.
`evenPositions`, insertion, sorting, and rebuilding are definitional summaries;
the operational interpreter still executes every submitted helper body.  There
is no task-answer rewrite or program-defined oracle.

### Material full-domain defect and false-behavior witness

`semantic.k:135` rewrites every index result as
`pyInt(headInt(dropList(L,I)))`, without a valid-index or integer-element guard.
`semantic.k:151` accepts only `pyInt` when rebuilding a list literal.
`headInt` is declared total/SMT-backed but has only the equation for a
nonempty integer-headed list.

Concrete witness:

```text
input = ["b", "odd", "a"]
canonical.py result = ["a", "odd", "b"]
solution.py result  = ["a", "odd", "b"]
K result            = no result; exit 113 at headInt(ListItem("b") ...)
```

This witness satisfies the written source contract and demonstrates the false
modeling conclusion: indexing a string element is forced toward an
integer-typed `pyInt(...)` rather than preserving `"b"`.  It is the witness for
the full-domain soundness/coverage finding; I do not claim the same rule is
false on its nonempty raw-integer subdomain.

The unrestricted helper claim `rebuild-correct` also admits too-short `EVENS`
lists, where both operational and reference sides contain opaque
`headInt(.List)` instead of Python `IndexError`. That scope is overbroad, but
the top-level integer execution always supplies exactly enough even values.

## 6. Fresh non-vacuity test

The final reviewer-authored
[`spec-vacuity.k`](evidence/spec-vacuity.k) uses the satisfiable input `[]`,
allows the actual returned list as `?RESULT`, and mutates the result-bearing
postcondition to require `size(?RESULT) ==Int 1`.  Both Python implementations
return `[]`, so the mutation is demonstrably false.

The dry run:

```text
kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY --dry-run
```

exited 0, proving the mutation parses/builds. The real proof command without
`--dry-run` exited 1 with `WarnStuckClaimState`; the residual has final
`pyList(.List)` and says the terms unify but the implication between conditions
fails. This is the expected unmet result obligation.

Two earlier direct wrong-constructor mutations were rejected because the
backend stopped with `DecidePredicateUnknown` before a clean final implication
failure. Their logs remain visible; they are not used as non-vacuity evidence.

Evidence:
[`stage6-vacuity-final.log`](evidence/stage6-vacuity-final.log),
[`stage6-vacuity.log`](evidence/stage6-vacuity.log), and
[`stage6-vacuity-valid.log`](evidence/stage6-vacuity-valid.log).

## 7. Proven versus assumed accounting

### What is machine-checked

Under the candidate-generated K theory, the exact constructor term regenerated
from `solution.py` executes to `pyList(sortEvenReference(L))`, using mutually
supporting recursive reachability claims for extraction, insertion, sorting,
and rebuilding. The complete claim set is unbounded in list length and integer
magnitude; it is not a fixed-size unrolling. Concrete example claims also
close. The theorem is result-constraining and non-vacuous.

### Trust ledger

| Boundary | Influence | Assessment |
|---|---|---|
| K 7.1.293 compiler, LLVM/Haskell backends, reachability prover, and SMT integration | All builds, concrete executions, and symbolic closure | Normal proof-tool trust boundary. |
| Imported `INT`, `BOOL`, `STRING`, `MAP`, and `LIST` domains, including `size`, `range`, `minInt`, maps, list concatenation, and integer comparisons | Values, guards, lookup, and list operations | Normal low-level K-library boundary. |
| Generated `semantic.k` as a Python-subset model | Binding, evaluation order, calls, returns, branches, and final value | Empirically and statically supported for actual raw-integer paths; unacceptable as a model of all orderable lists admitted by the prompt. |
| `headInt` as `[function,total,smtlib(headInt)]` | Every index and reference-list head | Equation is correct on nonempty raw-integer lists. Empty/non-integer applications are opaque/non-executable and materially affect excluded source inputs. |
| `solutionProgram()` embedding | Which program is proved | Mechanical constructor comparison and body mutation support exact identity. |
| `evenPositions`, `insertReference`, `sortReference`, `rebuildReference`, `sortEvenReference` | Formal postcondition | Truthful recursive definitions for integer lists; no execution bypass. Their implication of sortedness/permutation/odd-position preservation is an informal induction, not a separate K theorem. |
| Recursive helper claims | Closure of `sort-correct` and `top-correct` | Machine-checked with explicit dependency closures; structural descent prevents zero-step circularity. |
| Differential testing | Python rewrite/canonical agreement and finite semantics support | 98,672 finite Python cases and seven K integer executions; evidence only, never a universal proof. |
| Termination and Python exceptions | Whether execution reaches a post-state | Not proved. Partial correctness is silent on termination; exceptions are not modeled. |

### Gate and verdict reasoning

For the explicitly declared raw-integer runtime fragment, the proof-extension
soundness gate passes: the actual program executes, the summaries are
definitional, the RHS is fixed, dependencies close, and the false
postcondition is rejected. Evidence is reproducible.

Intent adequacy fails. The HumanEval source contract does not say
`list[int]`, and a whole material class of terminating, orderable-list inputs
accepted by both Python implementations is outside the generated semantics.
In generic Kit terminology this is `SOUND-BUT-LIMITED`; the benchmark prompt
explicitly requires such a materially narrowed source-contract domain to map
to `FAIL / NOT_LEGIT`, not `CONCERNS / LEGIT`.

The audit is complete. A concise command/status index is
[`COMMANDS.md`](evidence/COMMANDS.md).

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
