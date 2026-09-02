# Independent adversarial audit — 56-correct-bracketing

## Executive decision

The candidate's files rebuild cleanly, the submitted Python implementation is
correct on the tested intended domain, the generated concrete semantics agrees
with Python on all auditor-selected concrete cases, and all seven submitted K
claims close with `#Top`.  The result constraints are non-vacuous.

Nevertheless, this is not a legitimate universal proof of the real submitted
program.  The only universal entry claim invokes a proof-only value
`SeqVal(BS)` and therefore executes `forBracketSeq`; the actual initial
configuration wraps `$INPUT:String` in `SVal` and executes `forString`.  No K
connection theorem proves those two result-bearing execution paths equivalent.
The universal claim also executes the manually duplicated symbol
`correctProgram()` rather than the parsed bytes of `solution.mpy`.  A fresh
body-sensitivity experiment changed the actual submitted-program tree to a
demonstrably wrong function; the purported universal proof remained `#Top`
because it never read that tree.  Four ground string claims and finite
differential tests do not repair either universal pinning gap.

This is a Gate A failure under the Kit proof-extension contract and meets the
problem's `FAIL / NOT_LEGIT` boundary for a proof of a substituted execution
domain/program representation.

All builds and mutations were performed under
`/tmp/audit-work/reconstruction`.  Candidate-provided compiled definitions,
caches, traces, and reports were not reused.

## 1. Input and provenance integrity

### Trusted-input and mode checks

The rendered mode is `GENERATED_SEMANTICS`.  The trusted mount
`/reference/reference-semantics` is absent as required; it was neither searched
for elsewhere nor inferred.  There is no infrastructure contradiction, so a
candidate verdict is appropriate.

The candidate's `prompt.py` and `py2mpy.py` are byte-identical to the trusted
mounts:

| Artifact | Trusted/candidate SHA-256 | `cmp` |
|---|---|---|
| `prompt.py` | `4d14ffd571dae1770eb5e26636b128c8520cee2173f2f4a592277c6cd094e644` | exit 0 |
| `py2mpy.py` | `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16` | exit 0 |

Every required candidate artifact is present as an ordinary file:
`run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`,
`prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`, `semantic.k`,
`verification.k`, `spec.k`, and executable `prove.sh`.  The structured trace is
one ordinary JSONL file.  No candidate symlinks were found.  There are no
missing, changed, mistyped, or symlinked required source artifacts.

The candidate root additionally contains `__pycache__`, three `*-kompiled`
directories, `expanded.k`, and `kore-exec.tar.gz`.  These are untrusted derived
or cache artifacts.  They are not required by the source dependency closure
(`semantic.k` requires `verification.k`; `spec.k` requires `semantic.k`) and
were ignored.  In particular, the fresh rebuild succeeded without copying
`expanded.k` or any compiled directory.

### Untrusted provenance claims read

`run-input.json` identifies problem `56-correct-bracketing`, condition `bare`,
and no supplied semantics.  Its prompt and translator hashes agree with the
trusted hashes above.  `metrics.json` claims a 1,268-second, exit-0 generation
run.  `codex-last.txt` and `codex-output.log` claim that the translator
comparison, five concrete runs, and `kprove` succeeded.  The structured trace
has 424 valid JSON records and no malformed line; its final event repeats the
same `KPROVE_PASSED` claim.  These were treated only as provenance claims and
not as proof evidence.

Evidence:

- `evidence/01_integrity.sh` and `evidence/01_integrity.log`
- `evidence/01_trace_summary.py` and `evidence/01_trace_summary.log`

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

From trusted `/reference/prompt.py`, the input is a finite string whose
characters are only `<` and `>`.  The result is true exactly when the brackets
are correctly balanced: scanning left-to-right, no prefix may contain more
closing than opening brackets, and the final counts must be equal.

Trusted `/reference/canonical.py` implements that contract with an integer
depth, immediate false on a negative prefix, and a final `depth == 0` check.

Candidate `solution.py` uses the same algorithm.  It changes only the loop
variable name and spells `+= 1`/`-= 1` as `depth = depth + 1` and
`depth = depth - 1`.  These are equivalent for Python integers.  Its `else`
branch treats any non-`<` character as a close, matching the canonical
implementation; the stated domain contains only `>`.

### Trusted translation

The trusted translator was run from the scratch copy:

```text
python3 /tmp/audit-work/reconstruction/reference/py2mpy.py \
  /tmp/audit-work/reconstruction/candidate-src/solution.py \
  > /tmp/audit-work/reconstruction/solution.regenerated.mpy
```

It exited 0.  `cmp -s` against the submitted `solution.mpy` exited 0, and both
files have SHA-256
`3039e272296d96e5905974965b5613d576d5dba41743b002a2acff18e3d09409`.

### Independent differential test

The reviewer-authored test imports the trusted canonical entry point and the
scratch copy of the generated entry point independently.  It covers:

- the four documented examples;
- empty input and immediate-negative, unmatched-open, nested, sequential,
  balanced, and unbalanced boundaries;
- every one of the 8,191 strings of lengths 0 through 12 over `<>`;
- 2,000 deterministic generated strings of lengths 0 through 256;
- five long boundary patterns through length 1,024.

There were 10,210 comparisons and zero mismatches.  Both implementations
returned actual `bool` values.

Evidence:

- `evidence/02_fidelity.sh` and `evidence/02_fidelity.log`
- `evidence/02_differential.py`

This establishes strong finite program-fidelity evidence, not a universal K
connection theorem.

## 3. Clean proof reconstruction

K version `v7.1.293` was available independently at `/usr/bin`.  Only source
files copied to `/tmp/audit-work/reconstruction/candidate-src` were used.

### Fresh source builds

These exact source builds both exited 0:

```text
kompile semantic.k --backend llvm --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/reconstruction/fresh-llvm-kompiled

kompile semantic.k --backend haskell --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/reconstruction/fresh-haskell-kompiled
```

No candidate `llvm-kompiled`, `haskell-kompiled`, or `semantic-kompiled`
directory was copied or consulted.

### Concrete generated-semantics execution

The actual submitted `solution.mpy` was run under the fresh LLVM definition for
`""`, `"<"`, `"<>"`, `">"`, `"><"`, `"<<>>"`, `"<>>"`, and
`"<<><>>"`.  Every run exited 0 with `.K` and the expected `result(BVal(...))`.

A separate reviewer script compared fresh `krun` execution against both Python
implementations on 14 normal and boundary inputs:

```text
input=''        -> true
input='<'       -> false
input='>'       -> false
input='<>'      -> true
input='><'      -> false
input='<<'      -> false
input='>>'      -> false
input='<<>>'    -> true
input='<><>'    -> true
input='<>>'     -> false
input='<<><>>'  -> true
input='<<<>>>'  -> true
input='<<><>'   -> false
input='><<>'    -> false
```

All 14 three-way comparisons agreed and every `krun` exited 0.

### Positive proof targets

The unmodified original `spec.k` was proved as a whole:

```text
kprove spec.k \
  --definition /tmp/audit-work/reconstruction/fresh-haskell-kompiled \
  --spec-module SPEC
```

It printed `#Top` and exited 0.

For independent selection, the reviewer made a semantics-preserving scratch
copy of `spec.k` that only adds labels to the four unlabeled claims.  The two
loop claims are a mutually recursive invariant SCC, so they must be selected
together; the universal claim requires that SCC.  These selections all printed
`#Top` and exited 0:

```text
kprove audit-spec.k --definition .../fresh-haskell-kompiled \
  --spec-module AUDIT-SPEC \
  --claims AUDIT-SPEC.loop-zero,AUDIT-SPEC.loop-positive

kprove audit-spec.k --definition .../fresh-haskell-kompiled \
  --spec-module AUDIT-SPEC \
  --claims AUDIT-SPEC.loop-zero,AUDIT-SPEC.loop-positive,AUDIT-SPEC.universal-correctness

kprove audit-spec.k --definition .../fresh-haskell-kompiled \
  --spec-module AUDIT-SPEC --claims AUDIT-SPEC.example-open
kprove audit-spec.k --definition .../fresh-haskell-kompiled \
  --spec-module AUDIT-SPEC --claims AUDIT-SPEC.example-pair
kprove audit-spec.k --definition .../fresh-haskell-kompiled \
  --spec-module AUDIT-SPEC --claims AUDIT-SPEC.example-nested
kprove audit-spec.k --definition .../fresh-haskell-kompiled \
  --spec-module AUDIT-SPEC --claims AUDIT-SPEC.example-negative-prefix
```

Evidence:

- `evidence/03_reconstruction.sh` and `evidence/03_reconstruction.log`
- `evidence/03_semantics_differential.py` and
  `evidence/03_semantics_differential.log`

Reconstruction therefore passes.  `#Top` establishes closure under the
candidate theory; it does not settle whether that theory and claim describe the
real submitted execution.

## 4. Adequacy and real-program pinning

### Plain-language reading of every claim

1. `loop-zero`: for every proof-only bracket sequence `BS`, with a synthetic
   `forBracketSeq` loop at depth 0, arbitrary function map, a store headed by
   `depth = 0`, and no result, executing the loop, final return, and function
   boundary terminates with Boolean `bracketSeqSpec(BS,0)`.  Final map and
   environment are existential.
2. `loop-positive`: the same statement at any integer `D > 0`, returning
   `bracketSeqSpec(BS,D)`.
3. `universal-correctness`: for every `BS:BracketSeq`, starting with empty
   functions/environment and no result, expand `correctProgram()` and invoke
   `correct_bracketing` on `SeqVal(BS)`; termination must produce
   `bracketSeqSpec(BS,0)`.
4. Ground example 1: the duplicated program invoked on real-model `SVal("<")`
   returns false.
5. Ground example 2: the duplicated program invoked on `SVal("<>")` returns
   true.
6. Ground example 3: the duplicated program invoked on `SVal("<<><>>")`
   returns true.
7. Ground example 4: the duplicated program invoked on `SVal("><<>")` returns
   false.

All postconditions constrain `<result>` to a specific Boolean expression or
constant; the returned value is not existential, free, a tautology, or a
one-way implication.  Stage 6 independently confirms that this constraint is
discriminating.

### Satisfiable preconditions and ground substitutions

Concrete witnesses exist for every claim family:

- `loop-zero`: `BS=noBrackets()`, function map `.Map`, store
  `bind("depth",IVal(0),emptyStore())`, and `noResult()`.
- `loop-positive`: `BS=closeBracket(noBrackets())`, `D=1`, function map
  `.Map`, store `bind("depth",IVal(1),emptyStore())`, and `noResult()`.  This is
  the reachable internal state after consuming the first `<` of `<>`.
- `universal-correctness`: `BS=noBrackets()` with the explicitly empty cells.
- Each ground example has exactly the empty cells written in its claim.

Ground substitutions for empty, `<`, `<>`, `><`, `<<><>>`, and `><<>` make
`bracketSeqSpec` agree with both Python implementations.  For the internal
positive-depth witness, the remaining `>` at `D=1` yields true, consistent with
both entry implementations on the full input `<>`.

Evidence: `evidence/04_precondition_witnesses.py` and
`evidence/04_precondition_witnesses.log`.

### Material universal-input substitution

The real configuration in `semantic.k:65-71` is:

```text
<k> $PGM:Pgm ~> invoke("correct_bracketing", SVal($INPUT:String)) </k>
```

Consequently, real input follows:

```text
SVal(S) -> forString(S, X, BODY)
```

using rules `semantic.k:136-145`.

The universal claim at `spec.k:35-43` instead injects:

```text
correctProgram() ~> invoke("correct_bracketing", SeqVal(BS))
```

and therefore follows:

```text
SeqVal(BS) -> forBracketSeq(BS, X, BODY)
```

using separate rules `semantic.k:138-152`.

`SeqVal` is not produced by the parser, initial configuration, a program
expression, or any real execution rule.  No claim starts from
`SVal(S)` for symbolic `S`; no claim connects an encoding of `BS` to a `String`;
and no auxiliary reachability theorem proves `forString` and `forBracketSeq`
equivalent over all intended strings.  The same `bracketSeqSpec` symbol in the
synthetic execution and postcondition only characterizes that synthetic
execution.  It cannot transfer the result to the real string path.

The four concrete `SVal` claims cover only four strings.  The candidate-defined
`bracketSpec(String,Int)` would express a real-string summary, but it is unused
by every claim.

This is a result-bearing program-derived abstraction without the universal
connection theorem required by the Kit validation contract.  It is a Gate A
failure, not merely thin empirical support.

### Submitted-program body insensitivity

The entry claims also use `correctProgram()`, whose rule manually duplicates
the submitted AST through `targetLoopBody()` and `targetTail()`.  Static review
finds the current duplicate extensionally identical to the current
`solution.mpy`, but the K proof does not parse or depend on that file.

The reviewer created an isolated scratch source case, kept the K sources
unchanged, changed its `solution.py` body from final `depth == 0` to final
`depth == 1`, regenerated that case's `solution.mpy` with the trusted
translator, and confirmed:

- the mutant MPY differs from the submitted MPY (`cmp` exit 1);
- mutant Python returns true on intended-domain input `"<"`, while the trusted
  answer is false;
- fresh `krun` of the mutant MPY also returns `BVal(true)` on `"<"`;
- without changing `semantic.k`, the selected loop plus purported universal
  claim still prints `#Top` and exits 0.

Thus the proof is insensitive to a material change in the program artifact it
purports to prove.  This is not offered as a counterexample to the current
candidate implementation, which is correct; it is direct evidence that the K
entry theorem is not pinned to the submitted program bytes.

Evidence: `evidence/04_pinning_test.sh` and
`evidence/04_pinning_test.log`.

## 5. Rule-by-rule static soundness review

The complete line-by-line inventory is preserved in
`evidence/05_inventory.md`; its extraction/count check is
`evidence/05_inventory_check.sh` with output in
`evidence/05_inventory_check.log`.

### Inventory totals

- `semantic.k`: 39 local rules/equations.
- `verification.k`: 11 local defining equations.
- `spec.k`: seven reachability claims.
- `[function,total]`: `targetLoopBody`, `targetTail`, `bracketSpec`,
  `bracketEmpty`, `bracketOpen`, `bracketNegative`, and `bracketSeqSpec`.
- `[function]` but not `[total]`: `lookup`.
- No local `[functional]`, opaque, priority, simplification, `[concrete]`,
  `[owise]`, macro, or alias declaration/rule.

The local syntax inventory covers every production for `Pgm`, `Stmts`,
`Strings`, `Params`, the five statement forms, six expression forms, `CmpOp`,
four value constructors, function/store/result forms, thirteen continuations,
the proof-only `BracketSeq` datatype, and all five verification functions.
Every individual production and its lines are enumerated in
`evidence/05_inventory.md`.

### Operational rules S1-S39

The exhaustive inventory assigns IDs as follows:

| IDs | Rules | Judgment |
|---|---|---|
| S1-S2 | Shadowing-store lookup | True, disjoint equations; absent lookup is intentionally partial and not reached. |
| S3 | Module execution | Correct for the submitted single-module IR. |
| S4-S6 | `targetLoopBody`, `targetTail`, `correctProgram` expansion | Current expansions match the translated AST, but S6 is only a manually maintained duplicate and has the machine-pinning gap shown in Stage 4. |
| S7-S10 | Statement sequencing, empty statements, function registration, one-argument invocation | Correct for the single top-level function; deliberately incomplete for nested calls. |
| S11-S16 | Literal wrapping, name lookup, assignment evaluation/update | Correct for all submitted reads and writes. |
| S17-S20 | Left-to-right integer `+`/`-` | Correct; both K and Python integers are unbounded here. |
| S21-S25 | Left-to-right string/int equality and integer less-than | Correct on all used operand types. |
| S26-S28 | Guard evaluation and Boolean branch selection | Correct, disjoint branches. |
| S29-S33 | Iterable evaluation and actual `SVal` string loop | Empty/nonempty guards partition strings; each iteration binds the first character and shortens the suffix.  Correct for the intended ASCII alphabet. |
| S31, S34-S36 | Proof-only `SeqVal`/`BracketSeq` loop | Internally coherent under its declared interpretation, but an alternate unreachable input path with no connection theorem to S29-S33.  This is the material proof-domain gap. |
| S37-S39 | Return evaluation, abrupt continuation discard, and result write | Correct on reachable returns of this sole top-level call.  S38 accepts an overly broad `_REST:K` and would mishandle an observable caller continuation or nested call; no such context is reachable in the submitted program, so this is recorded as a semantics-scope gap rather than labeled an intended-domain unsoundness. |

The full table in `evidence/05_inventory.md` lists S1 through S39 individually,
with exact source lines and judgments.

### Verification equations V1-V11

`bracketSpec` and its three Boolean dispatch helpers (V1-V7) define the
canonical depth scan over a K string.  The non-`<` branch matches the real
Python `else`; intended inputs make that character `>`.  Boolean cases are
exhaustive and recursion consumes one character.

`bracketSeqSpec` (V8-V11) defines the same depth scan over the proof-only free
datatype.  Empty/open constructors are exhaustive with the two close rules;
the close guards `D-1 < 0` and `D-1 >= 0` are disjoint and exhaustive over
integers.  Recursion is structurally descending.  The `[total]` attributes are
therefore justified by the equations rather than assumed merely from the
attribute.

No inventoried local equation has a demonstrated false mathematical conclusion
on the intended input domain.  Accordingly, this review does not label an
individual rule unsound without the required witness.  The rejection rests on
the narrower but decisive fact that the successful universal claim proves the
alternate S31/S34-S36 execution, not the real S29-S33 execution.

### Configuration, order, state, calls, and control

- The four cells are sufficient for the target: computation, functions,
  environment, and result.  The program uses no heap, output, allocation, or
  exceptions.
- Expressions evaluate left-to-right through explicit continuations.
- Assignments shadow previous bindings; reads obtain the newest binding.
- The function definition is registered before the configured call.
- Invocation binds the sole parameter and resets the store, which is correct
  for this one non-nested call.
- The early return correctly discards the remaining loop iterations and final
  return on reachable target paths.
- Real string iteration shortens its suffix, and proof-only constructor
  iteration structurally shortens its sequence.

### Construct coverage

Every construct in `solution.mpy` maps to declared syntax and operational
rules: `Module`, statement lists, `FuncDef`, `Params`, `Assign`, `For`, `If`,
`Return`, `Name`, all three literal sorts, `BinOp(+/-)`, and
`Compare(string ==, int ==, int <)`.  Minimal missing behavior for unused
Python constructs is acceptable in `GENERATED_SEMANTICS` mode.

## 6. Fresh non-vacuity test

There was no candidate `spec-vacuity.k`.  The reviewer created a fresh distinct
module, preserved as `evidence/06_spec_vacuity.k`.  It leaves the satisfiable
entry state and real-model input `SVal("<>")` unchanged but mutates the required
result from true to false.

Both trusted canonical Python and candidate Python return true on `"<>"`.
Then:

```text
kprove audit-spec-vacuity.k \
  --definition /tmp/audit-work/reconstruction/fresh-haskell-kompiled \
  --spec-module AUDIT-SPEC-VACUITY \
  --claims AUDIT-SPEC-VACUITY.false-pair \
  --dry-run
```

parsed/built the mutation successfully and exited 0.

The same command without `--dry-run` exited 1.  It emitted
`WarnStuckClaimState`; the residual had `.K` and
`result(BVal(true))`, directly exposing the unmet false-result obligation.
This was an expected proof failure, not a parser error, missing import, timeout,
or unrelated crash.

Evidence:

- `evidence/06_spec_vacuity.k`
- `evidence/06_nonvacuity.sh`
- `evidence/06_nonvacuity.log`

Non-vacuity passes.  It shows the ground result claim is discriminating; it
does not connect the universal synthetic execution to real strings.

## 7. Proven versus assumed accounting

### What the successful reachability proof actually establishes

Under the candidate's own generated K theory:

- the two mutually recursive circularities summarize `forBracketSeq` at zero
  and positive depth;
- for every finite `BS:BracketSeq`, the hard-coded
  `correctProgram()` invoked with synthetic `SeqVal(BS)` returns exactly
  `bracketSeqSpec(BS,0)`, assuming termination in the partial-correctness
  interpretation;
- the hard-coded program invoked with four concrete `SVal` strings returns the
  four stated constants.

Those are result-constraining theorems in the submitted theory.  They are not a
universal theorem for the actual configured input `SVal($INPUT:String)` or the
parsed submitted `solution.mpy`.

### Trust and assumption ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K v7.1.293 parser/compiler, LLVM executor, Haskell prover, and `#Top` result | All reconstructed builds, runs, and claims | Necessary low-level tool trust; acceptable. |
| Built-in K `Int`, `Bool`, `String`, `Map`, equality/order/arithmetic, `lengthString`, and `substrString` | Concrete semantics and both reference checkers | Ordinary fixed primitive boundary; acceptable on the intended ASCII domain. |
| Trusted mounted prompt, canonical Python, and translator | Contract, program differential, MPY identity | Authorized trusted inputs. |
| CPython and finite differential harness | 10,210 Python comparisons and 14 K/Python comparisons | Strong finite evidence only; not a universal proof. |
| Generated operational semantics S1-S39 | All K executions and claims | Individually audited.  Adequate for the real concrete target path, with documented non-target limitations. |
| `targetLoopBody` and `targetTail` macro equations | Loop claims and universal claim | Exact current AST fragments; truthful definitional summaries. |
| `correctProgram()` duplicate | Every submitted claim | Manually equal to the current program but not machine-connected to `solution.mpy`; body-sensitivity test proves the K theorem ignores program-file changes.  Illegitimate as the sole real-program pin. |
| `BracketSeq`, `SeqVal`, and `forBracketSeq` | Both loop claims and the only universal claim | Proof-created, result-bearing alternate execution representation.  No universal theorem connects it to `SVal`/`forString`.  This is the decisive illegitimate assumption. |
| `bracketSeqSpec` equations | Universal postcondition | Truthful mathematical definition over `BracketSeq`, exhaustively audited.  It fixes the synthetic result but does not prove a relation to real string execution. |
| `bracketSpec` equations | No claim | Truthful but unused; cannot support the universal theorem. |
| Existential final maps/environments | All claims | They omit internal final-state details, but the task observes only the Boolean return; acceptable. |
| `functionBoundary()` sentinel and broad return rule | All returns | Correct on target paths; over-broad outside the target call shape.  Documented limitation, not the verdict basis. |

There are no proof-local opaque values that freely determine the final Boolean,
no simplification or priority axioms, and no unguarded overlapping total
equations.  The principal problem is not an oracle giving the wrong Boolean;
it is the lack of any theorem transferring the proven Boolean from the
proof-only execution to the actual program execution.

### Gate summary

- Real-program soundness / Gate A: **FAIL**.  A5 non-vacuity passes, but A1/A3
  body and value-representation connection obligations fail.
- Intent adequacy / Gate B: **FAIL for the formal universal theorem**.  The
  Python implementation matches intent, but the theorem's universal domain is
  synthetic and unconnected to actual strings.
- Trust/evidence / Gate C: reconstruction and reviewer evidence are
  reproducible, but finite tests cannot replace the missing universal
  connection theorem.

The clean `#Top` results are genuine for the submitted theory, and the
candidate implementation appears correct.  The candidate nevertheless lacks a
legitimate partial-correctness proof of the real generated program required by
the audit problem.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
