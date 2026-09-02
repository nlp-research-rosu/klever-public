# Independent adversarial review: 58-common

The candidate contains a legitimate, freshly reconstructed reachability proof
for **finite integer lists**.  The proof executes the exact submitted
`solution.mpy`, constrains the returned list to a deterministic sorted
intersection, and rejects a fresh false result obligation.  The result is
`CONCERNS / LEGIT`, rather than `PASS`, because the trusted prompt annotates the
arguments only as `list`, while the K configuration and claim admit only
integer lists.  That restriction is observable: the generated Python and the
trusted canonical implementation diverge on some non-integer literal-list
inputs.  In addition, the connection between the small generated K semantics
and ordinary Python is audited mathematically and empirically, not proved by a
separate K connection theorem.

## 1. Input and provenance integrity

### Rendered-mode boundary

This is a `GENERATED_SEMANTICS` audit.  `/reference/reference-semantics` is
absent as required; it is neither an entry nor a symlink.  There is no trusted
hidden semantics and no infrastructure contradiction.  The live tools are K
v7.1.293.  See `evidence/00-environment.log`.

### Candidate artifact inventory

I inspected the complete candidate tree and the required untrusted metadata:

- Regular source/evidence files present:
  `run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`,
  `prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`, `semantic.k`,
  `verification.k`, `spec.k`, `mutation-spec.k`, and `prove.sh`.
- A structured trace is present at
  `/candidate/codex-trace/2026/07/22/rollout-2026-07-22T05-16-05-019f8953-4b0c-78f2-bbcc-2c3fb4e7a761.jsonl`.
- No candidate symlinks, device nodes, sockets, or other special file types
  were found.  No required source artifact is missing or mistyped.
- `/candidate/verification-kompiled/` and `/candidate/__pycache__/` are extra
  generated caches.  They are not integrity failures, but they were not copied
  to scratch and were never used.

The complete type inventory is in `evidence/01-artifact-inventory.log`.

The untrusted metadata and trace claim a successful generation run, four
concrete executions, one `#Top`, and rejection of the candidate's program
mutation.  I treated those only as claims.  Their bounded extraction is in
`evidence/01-claims-metadata.log` and
`evidence/01-structured-trace-summary.log`.

### Prompt and translator provenance

`/candidate/prompt.py` is byte-identical to `/reference/prompt.py`; both have
SHA-256
`1ea0b2ba5f5fa366f20d0edd79ce1af5dc42629807502c5868700fcb9117b8b0`.
`/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`; both have
SHA-256
`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.
The `run-input.json` digests agree with those trusted files.  See
`evidence/01-provenance.log`.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

From `/reference/prompt.py`, `common(l1, l2)` must return the common elements
of the two lists, with duplicates removed and the result sorted in ascending
order.  The trusted `/reference/canonical.py` implements this by comparing
every pair, adding equal left-hand elements to a set, then returning
`sorted(list(ret))`.

The candidate implementation is:

```python
def common(l1: list, l2: list):
    return sorted(set(l1) & set(l2))
```

For ordinary finite integer lists this is the same algorithmic result by a
different route: convert both lists to sets, intersect them, and sort.

### Trusted translation identity

I copied source only to `/tmp/audit-work/58-common`, ran the trusted translator
from `/reference/py2mpy.py`, and compared its output with the submitted
`solution.mpy`.  `cmp` exited 0 and both files have SHA-256
`eebc62af976e883d21d2c6b999274ce697a1b48def70706a46560330a50d2722`.
See `evidence/02-scratch-and-regeneration.log`.

### Independent differential testing

`evidence/differential_common.py` imports the trusted canonical entry point
directly from `/reference/canonical.py` and the generated entry point from the
scratch copy.  It covers:

- both documented examples;
- empty/empty and one-sided empty inputs;
- singleton hit and miss;
- duplicates, disjoint lists, negatives, reverse order, and very large
  arbitrary-precision integers;
- all 7,225 pairs of lists of length 0 through 3 over `{-2, 0, 1, 2}`;
- 1,000 deterministic generated pairs (seed 580058).

The exact command was:

```text
python3 /audit-output/evidence/differential_common.py
```

It exited 0 after 8,237 pairs with `mismatch_count=0`.  The inputs, generation
parameters, command, status, and result are in `evidence/02-differential.log`.

As a scope probe, ordinary homogeneous strings, tuples, and floats also matched
on three cases (`evidence/07-broader-python-domain.log`).  That does not extend
the K theorem.

### Literal-list domain limitation

The prompt gives `list` annotations but no element type.  The candidate's K
semantics explicitly narrows values to integer lists
(`/candidate/semantic.k:14-18`).  The generated Python is also not equivalent
to the canonical implementation on every literal Python-list input that the
canonical implementation can evaluate:

- for `[[1]]` versus `[[2]]`, and two analogous one-sided-empty cases, the
  canonical returns `[]` while the candidate eagerly constructs a set and
  raises `TypeError`;
- for the same `NaN` object in both lists, the canonical returns `[]`, while
  the candidate returns `[nan]`.

The reviewer-authored probe, exact outcomes, and zero-status expected-divergence
run are in `evidence/out_of_formal_domain_divergence.py` and
`evidence/07-out-of-formal-domain-divergence.log`.  These cases are outside the
formal `Ints` precondition, so they do not refute the K claim.  They do show
that the integer restriction is a material intent-coverage limitation rather
than merely a notational choice.

## 3. Clean proof reconstruction

Only `solution.py`, `solution.mpy`, `semantic.k`, `verification.k`, and `spec.k`
were copied from the candidate.  The trusted translator and canonical source
were copied under distinct names.  No `*-kompiled` directory or Python cache
was copied.

### Fresh concrete definition

Exact command:

```text
kompile semantic.k --backend llvm --main-module SEMANTIC \
  --syntax-module SEMANTIC-SYNTAX --output-definition semantic-kompiled
```

It exited 0.  See `evidence/03-build-concrete.log`.

The reviewer-authored `evidence/concrete_semantics_checks.py` then ran the
fresh LLVM definition on eight normal and boundary inputs.  The cases exercise
empty recursion, membership hit and miss, duplicate removal, both intersection
branches, both insertion-order branches, negatives, and arbitrary-size
integers.  Every `krun` exited 0 and every final `<k>` list matched the trusted
Python result; `MISMATCH_COUNT=0`.  Exact per-case commands, K configurations,
Python results, and statuses are in `evidence/03-concrete-semantics.log`.

### Fresh proof definition

Exact command:

```text
kompile verification.k --backend haskell --main-module VERIFICATION \
  --syntax-module SEMANTIC-SYNTAX \
  --output-definition verification-kompiled
```

It exited 0.  See `evidence/03-build-proof.log`.

`spec.k` contains one positive target claim.  I ran all claims in its module:

```text
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

The command exited 0 and printed exactly `#Top`.  See
`evidence/03-positive-proof.log`.  This is an independent reconstruction of the
candidate's positive result, not reuse of its compiled definition or logs.

## 4. Adequacy and real-program pinning

### Entry precondition in plain language

The claim in `/candidate/spec.k:9-25` has no textual `requires`, but its
configuration and sorts impose the following precondition:

- `<k>` contains the exact translated module with a two-argument function named
  `common`, parameters `"l1"` and `"l2"`, and the submitted single return
  expression;
- `<l1>` is `list(IS1)` and `<l2>` is `list(IS2)`;
- `IS1` and `IS2` are arbitrary finite sequences of mathematical K `Int`
  values.

There are no heap, globals, stack, exception, or I/O cells.

### Postcondition in plain language

The entire `<k>` computation becomes
`list(commonSpec(IS1 ; IS2))`, with both input cells unchanged.  The sole
`commonSpec` equation unfolds this to:

```text
list(sortInts(intersectInts(uniqueInts(IS1) ; uniqueInts(IS2))))
```

There is no free right-hand result variable, existential result, implication,
or tautological condition.  All `IS1` and `IS2` occurrences are fixed by the
left-hand input cells.

### Actual-program identity and control flow

`evidence/check_program_pinning.py` removes layout only and compares the
submitted `solution.mpy` with the entry claim's `<k>` left-hand side.  The
normalized terms are identical and the script exited 0; see
`evidence/04-program-pinning.log`.  The trusted translator already established
that this term is the submitted `solution.py`.

There are no loop or helper reachability claims.  Actual control follows the
module-entry rule, the single `Return`, and the compositional evaluator.  The
only proof-local helper, `commonSpec`, appears on the destination side and has a
complete defining equation; it does not rewrite or bypass the program body.

### Satisfiable witness and ground substitution

A concrete satisfying state is:

```text
IS1 = 3,3,-1,2
IS2 = 3,-1,-1
<l1> list(3,3,-1,2) </l1>
<l2> list(3,-1,-1) </l2>
```

Substitution into the destination gives `list(-1,3)`.  The independently loaded
canonical Python, generated Python, and fresh K execution all returned
`[-1, 3]`; this is case 5 in `evidence/03-concrete-semantics.log` and is also
covered by `evidence/02-differential.log`.

## 5. Rule-by-rule static soundness review

There are no generated helper K files beyond `semantic.k`; the only other
local theory file is `verification.k`.  The line-numbered sources are preserved
in `evidence/02-source-review.log`, and the machine-extracted declaration
inventory is in `evidence/05-rule-inventory-source.log`.

### Syntax, configuration, and attribute inventory

Local syntax declarations are exhaustive as follows:

1. `PyModule`: `Module(PyStmt)`.
2. `PyStmt`: `FuncDef(String, Params, PyStmt)`.
3. `PyStmt`: `Return(PyExpr)`.
4. `Params`: exactly two `String` parameters.
5. `PyExpr`: `Name(String)`.
6. `PyExpr`: `Call(PyExpr, PyExpr)`.
7. `PyExpr`: `BinOp(String, PyExpr, PyExpr)`.
8. `Ints`: comma-separated built-in K integers.
9. `PyValue`: `list(Ints)`.
10. `PyValue`: `set(Ints)`.
11. `Bool`: `containsInt(Int; Ints)` with `[function]`.
12. `Ints`: `uniqueInts(Ints)` with `[function]`.
13. `Ints`: `intersectInts(Ints; Ints)` with `[function]`.
14. `Ints`: `insertInt(Int; Ints)` with `[function]`.
15. `Ints`: `sortInts(Ints)` with `[function]`.
16. `PyValue`: `makeSet(PyValue)` with `[function]`.
17. `PyValue`: `setAnd(PyValue; PyValue)` with `[function]`.
18. `PyValue`: `sortedValue(PyValue)` with `[function]`.
19. `PyValue`: `eval(PyExpr; String; PyValue; String; PyValue)` with
    `[function]`.
20. `KItem`: `execute(PyStmt; String; PyValue; String; PyValue)`.
21. `Ints`: `commonSpec(Ints; Ints)` with `[function]`.

The configuration has exactly `<k>`, `<l1>`, and `<l2>` inside `<py>`.
`<l1>` and `<l2>` are read-only input values.  There are no local `[total]`,
`[functional]`, `[simplification]`, `[concrete]`, priority, `owise`, macro, or
opaque declarations.  No rule allocates, mutates, prints, raises, or changes an
input cell.

### Construct coverage for the submitted program

| Submitted construct | Declaration and behavior |
|---|---|
| `Module` | `PyModule`; rule R23 enters the pinned `common` body |
| `FuncDef` | `PyStmt`; matched by R23 with its two real parameter names |
| `Params` | `Params`; R23 binds the two input cells positionally |
| `Return` | `PyStmt`; R24 evaluates its expression |
| `Call` | `PyExpr`; R20 handles `set`, R21 handles `sorted` |
| `Name` | `PyExpr`; R18/R19 look up `l1`/`l2` |
| `BinOp("&",...)` | `PyExpr`; R22 evaluates integer-set intersection |
| external input lists | `PyValue list(Ints)`; R14 converts them to sets |

Every syntax constructor in `solution.mpy` is declared and reaches a rule.
Unsupported source constructs remain unmodeled and would fail to parse or
stick, which is appropriate for this minimal generated semantics.

### Exhaustive rule inventory and judgment

The following enumerates every local rule in `semantic.k` and
`verification.k`.

| ID | Source | Rule effect | Static judgment |
|---|---|---|---|
| R1 | `semantic.k:36` | membership in empty `Ints` is false | True definition |
| R2 | `semantic.k:37` | compare head, otherwise recurse on tail | True integer-membership recurrence; strictly descends |
| R3 | `semantic.k:40` | unique of empty is empty | True base case |
| R4 | `semantic.k:41-42` | drop a head that occurs later | Preserves the represented set and removes an earlier duplicate |
| R5 | `semantic.k:43-44` | retain a head absent from the tail | Preserves the represented set and establishes uniqueness |
| R6 | `semantic.k:47` | intersection with empty left sequence is empty | True base case |
| R7 | `semantic.k:48-49` | retain a left head found in the right sequence | True filtering recurrence |
| R8 | `semantic.k:50-51` | discard a left head absent from the right | True complementary recurrence |
| R9 | `semantic.k:54` | insert into empty sequence | True base case |
| R10 | `semantic.k:55-56` | place `I` before first `J >= I` | Correct insertion into a sorted tail |
| R11 | `semantic.k:57-58` | retain smaller `J` and recurse | Correct complementary insertion branch; strictly descends |
| R12 | `semantic.k:61` | sort empty sequence | True base case |
| R13 | `semantic.k:62` | insertion-sort the recursively sorted tail | Correct insertion-sort recurrence; strictly descends |
| R14 | `semantic.k:67` | `set(list(IS))` becomes `set(uniqueInts(IS))` | Correct for finite integer lists |
| R15 | `semantic.k:68` | filter the left set representation by right membership | Correct on the duplicate-free representation established by R14 |
| R16 | `semantic.k:69` | sort a set representation into a list | Correct for integer sets; representation order becomes unobservable |
| R17 | `semantic.k:70` | sort an integer-list value | Correct, though unused by this submitted expression |
| R18 | `semantic.k:77` | first-parameter lookup | Correct positional/lexical lookup |
| R19 | `semantic.k:78-79` | second-parameter lookup when names differ | Correct and disjoint from R18 for the actual `"l1"`/`"l2"` parameters |
| R20 | `semantic.k:80-81` | evaluate the recognized unary `set` call | Correct under the clean built-in environment assumed by the model |
| R21 | `semantic.k:82-83` | evaluate the recognized unary `sorted` call | Correct for modeled integer list/set values |
| R22 | `semantic.k:84-86` | evaluate `&` by set intersection | Correct and pure for modeled integer sets |
| R23 | `semantic.k:94-97` | invoke the pinned `common` body using `<l1>/<l2>` | Correct entry-harness rule for the exact submitted program and initial `.K` continuation |
| R24 | `semantic.k:98-99` | replace the single modeled `Return` with its evaluated value | Correct for the exact one-statement body and initial `.K` continuation |
| R25 | `verification.k:9-10` | define `commonSpec` as unique/intersect/sort | Truthful definitional summary; it does not replace execution |

R4/R5 and R7/R8 have complementary `containsInt`/`notBool` guards.  R10/R11
have complementary `<=Int`/`>Int` guards.  Base and nonempty list patterns are
disjoint.  R18/R19 are disjoint on the actual distinct parameter names, and
the remaining evaluator patterns have distinct outer constructors or literal
operation names.  Thus there is no disagreeing overlap on the entry domain.

Although the helpers are not marked `[total]`, the actually used domains are
covered: membership, uniqueness, intersection, insertion, and sorting cover
all finite `Ints`; the partial value/evaluator functions cover every value and
expression reached by the exact claim.  All recursion is on a strict tail, so
there is no circular or non-descending equation.  The two expression operands
are pure and have no modeled state or exception effects, so the absence of an
observable evaluation-order distinction is harmless here.

`R14` establishes duplicate-free internal `set` values before `R15`.  The raw
grammar itself permits malformed terms such as a `set` sequence containing
duplicates, and the module/return rules syntactically frame arbitrary K
continuations with `...`.  Those are reuse/generalization gaps: neither a
malformed internal set nor a nonempty continuation is reachable from the
submitted entry claim on integer-list inputs.  Under the required witness
standard, I therefore do not label these rules unsound; no false conclusion
can be enabled by them on the claimed input domain.

R23 is an explicit entry harness, not a full semantics of importing a Python
module and then performing a separate call.  For the pinned body it preserves
the relevant binding, returned value, and all modeled cells.  R20/R21 recognize
built-ins by syntax rather than a global environment.  This is faithful for
the submitted source in an ordinary clean Python environment, but it excludes
built-in rebinding, monkeypatching, exceptions, allocation identity, and
resource exhaustion.  Those exclusions are recorded in stage 7.

No rule encodes a concrete answer, produces an unconstrained result, skips the
program in favor of `commonSpec`, or introduces an opaque oracle.

## 6. Fresh non-vacuity test

I inspected but did not rely on `/candidate/mutation-spec.k`; it mutates the
program rather than the result obligation.  I authored a distinct result
mutation in `evidence/fresh-vacuity-spec.k`.  It keeps the exact submitted
program and input cells, but changes the destination from:

```text
list(commonSpec(IS1 ; IS2))
```

to:

```text
list(0, commonSpec(IS1 ; IS2))
```

The satisfying falsifying witness is `IS1 = .Ints`, `IS2 = .Ints`: the real
result is `list(.Ints)`, while the mutation requires `list(0,.Ints)`.

First, `kprove ... --dry-run` parsed and built the mutation successfully with
exit 0 (`evidence/06-mutation-build.log`).  The actual proof command was:

```text
kprove fresh-vacuity-spec.k --definition verification-kompiled \
  --spec-module FRESH-VACUITY-SPEC
```

It exited 1 with `WarnStuckClaimState`.  The residual explicitly contains the
failed equality between
`0, sortInts(intersectInts(...))` and
`sortInts(intersectInts(...))`, followed by the final real program
configuration.  This is the expected unmet result obligation, not a parser
error, missing import, timeout, or unrelated crash.  See
`evidence/06-mutation-proof.log`.

## 7. Proven versus assumed accounting

### What the K proof establishes

Under the candidate's generated theory, for every two finite K integer
sequences `IS1` and `IS2`, the exact submitted constructor program, started
with `<l1> list(IS1) </l1>` and `<l2> list(IS2) </l2>`, reaches:

```text
<k>
  list(sortInts(intersectInts(uniqueInts(IS1) ; uniqueInts(IS2)))) ~> .K
</k>
```

with the input cells unchanged.  This is a result-constraining
partial-correctness theorem about the real translated program.  The helper
recurrences have the ordinary mathematical meaning of sorted, duplicate-free
integer intersection.

### Trust ledger

| Boundary | Effect and dependents | Assessment |
|---|---|---|
| K built-in `Int`, integer equality/order, `Bool`, `String` equality, list syntax, parser, LLVM/Haskell backends | All helper equations, builds, execution, and proof | Acceptable low-level K trust boundary |
| Trusted CPython AST translator | Connects `solution.py` text to `solution.mpy` | Trusted input plus fresh byte-identity reconstruction; not part of the K theorem |
| Entry harness R23 | Connects the module constructor and input cells to invocation of `common(l1,l2)` | Acceptable for this pinned entry program; not a general Python module/call semantics |
| Python `set`, `&`, and `sorted` on finite integers | Connects R14-R22 to ordinary Python behavior and natural-language intent | Mathematically direct and concretely tested, but informal rather than a machine-checked CPython connection theorem |
| Clean built-in environment and no exceptional/resource behavior | Affects call selection and termination/exceptions | Explicit modeling assumption; appropriate for normal HumanEval execution, but excluded from the theorem |
| Integer-only inputs | Determines the entire formal theorem domain | Material limitation because the trusted prompt says only `list` |
| Trusted canonical implementation as oracle | Supports program-fidelity and semantics checks | Finite empirical evidence only; it does not replace the K proof |

There are **no opaque symbols**, fresh result oracles, unproved proof-local
lemmas, operational proof shortcuts, totality declarations, or simplification
axioms.  `commonSpec` is a fully defined symbol.  Its dependents are only the
entry destination and the fresh mutation; its value is fixed by R25 and the
audited helper equations.

The 8,237-pair differential run and eight concrete K executions support the
Python/K bridge only on their documented cases.  The structural rule review
supplies the general mathematical argument over finite integer sequences.
Neither the generation trace, the candidate's prior `#Top`, nor differential
testing was used as a substitute for the fresh reachability proof.

### Gate and decision accounting

- **Gate A — real-program soundness: PASS.**  The exact body executes; every
  result-bearing symbol is defined; the destination is deterministic; a
  satisfying witness exists; and the fresh false result mutation is rejected.
- **Gate B — intent adequacy: LIMITED.**  The theorem is faithful to finite
  integer lists but the trusted prompt does not explicitly restrict list
  elements to integers.  Concrete out-of-domain divergences demonstrate the
  limitation.  The Python-semantics bridge is also informal.
- **Gate C — trust and reproducibility: PASS.**  Reviewer scripts, bounded
  command logs, exact statuses, outputs, and hashes are preserved under
  `evidence/`; see `evidence/99-final-evidence-inventory.log`.

The stage-2 divergence does not make a false K conclusion provable under the
entry claim's `Ints` precondition, so it does not justify `FAIL / NOT_LEGIT`.
It does prevent an unqualified `PASS`.  The correct completed-audit outcome is
therefore a sound but limited proof.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
