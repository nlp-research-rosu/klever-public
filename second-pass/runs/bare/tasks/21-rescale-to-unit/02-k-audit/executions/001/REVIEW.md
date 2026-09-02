# Independent adversarial review: 21-rescale-to-unit

This audit used only fresh source copies under `/tmp/audit-work`. Candidate
compiled definitions, caches, logs, prose, and traces were treated as
untrusted evidence. The reconstructed K claims do close and the proof is
non-vacuous inside the candidate's exact-rational model. It is nevertheless
not a legitimate proof of the real Python program: the model gives Python
float subtraction and division exact-rational behavior, for which there are
concrete false-conclusion witnesses on finite, exactly representable inputs.
In addition, the seven claims cover only fixed list shapes and do not prove the
contract for arbitrary valid list lengths.

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `GENERATED_SEMANTICS`. `/reference/reference-semantics`
does not exist, while the trusted mount contains exactly
`canonical.py`, `prompt.py`, and `py2mpy.py`. This is consistent with the
rendered mode; there is no infrastructure breach. See
`evidence/stage1_commands.sh` and `evidence/stage1.log`.

### Artifact and provenance checks

The following required candidate artifacts are present as regular files:
`run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`, the
JSONL structured trace, `prompt.py`, `py2mpy.py`, `solution.py`,
`solution.mpy`, `semantic.k`, `verification.k`, `spec.k`, and `prove.sh`.
`prove.sh` is executable. None is a symlink. No required source artifact is
missing, mistyped, changed relative to a trusted counterpart, or symlinked.
There are no candidate helper K source files beyond `semantic.k`,
`verification.k`, and `spec.k`.

The candidate also contains `semantic-kompiled/`,
`verification-kompiled/`, and `__pycache__/`. These are generated extras, not
source integrity failures; none was copied into or used by the audit builds.

Byte comparisons and hashes establish:

- Candidate `prompt.py` equals `/reference/prompt.py`, SHA-256
  `f5d1f07614da8dffb7e6ede02cdedd73f58405f47aeb516b82318416a4acf0c7`.
- Candidate `py2mpy.py` equals `/reference/py2mpy.py`, SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.
- Those hashes agree with the corresponding claims in `run-input.json`.

I read the complete untrusted JSONL trace and text generation log with
`evidence/trace_summary.py`. The JSONL has 302 valid JSON records and no
malformed record; the text log has 21,860 lines. `run-input.json` identifies
the correct problem and bare/generated-semantics condition. `metrics.json`
claims exit 0 without timeout. `codex-last.txt`, the text log, and trace all
claim that `kprove` succeeded. Those statements were not relied on; their
fresh reconstruction is in stage 3.

Stage result: integrity passes; there is no audit-infrastructure error.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

`prompt.py` asks for `rescale_to_unit(numbers: List[float])`, where `numbers`
has at least two elements. The intended transform is pointwise

`(x - minimum(numbers)) / (maximum(numbers) - minimum(numbers))`,

so the minimum becomes 0 and the maximum becomes 1. The trusted canonical
implementation computes exactly that Python expression with `min`, `max`, and
a list comprehension.

The written prompt does not say that the extrema must differ, but both the
formula and canonical implementation require a nonzero range to return a
list: an all-equal nonempty list raises `ZeroDivisionError`. Empty input raises
`ValueError`. A charitable successful-return domain is therefore a list of at
least two floats with distinct extrema. Nothing in the prompt bounds their
magnitudes or excludes finite IEEE-754 edge cases.

### Source and translation fidelity

`solution.py` uses the same algorithm as the canonical implementation, with
renamed local variables and multiline formatting. A fresh invocation of the
trusted translator produced SHA-256
`69c695ed27f93cc676020bc8a8c4adf2af65d50eb54ef1f213fe312d3b512682`,
byte-identical to submitted `solution.mpy`. Exact commands and statuses are in
`evidence/stage2_commands.sh` and `evidence/stage2.log`.

### Independent differential test

`evidence/differential.py` independently imports the trusted canonical entry
point and the scratch-copy candidate entry point. It records complete inputs
and bit-level float outcomes in `evidence/differential-results.json`.
Coverage was:

- the documented example;
- empty, singleton, and all-equal cases;
- minimum-length increasing and descending inputs;
- negative values, fractional values, signed zero, repeated extrema;
- large and tiny finite values, infinities, and NaN;
- 200 deterministic generated lists of lengths 2 through 12, seed `210021`,
  including duplicates and varied ordering.

All 215 cases matched, including exception types/messages and result float
bits; mismatch count was zero. This supports candidate-versus-canonical
fidelity only. Because both Python functions use the same arithmetic, it
cannot validate the different exact-rational arithmetic used by K.

Stage result: program and translation fidelity pass.

## 3. Clean proof reconstruction

### Fresh builds

Only these candidate sources were copied:
`prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`, `semantic.k`,
`verification.k`, `spec.k`, and `prove.sh`. The scratch source directory had
no compiled definition. K version 7.1.293 was available.

The audit deleted only its own prior scratch build directories, then built:

- an LLVM concrete definition from `semantic.k`, main module `SEMANTIC`,
  syntax module `MPY-SYNTAX`;
- a Haskell proof definition from `verification.k`, main module
  `VERIFICATION`, syntax module `MPY-SYNTAX`.

Both `kompile` commands exited 0. Exact commands are in
`evidence/stage3_commands.sh`; bounded output is in `evidence/stage3.log`.

### Concrete generated-semantics execution

Fresh `krun` executions of the actual scratch `solution.mpy` produced:

- `[1,2,3,4,5]` -> exact rationals `[0,1/4,1/2,3/4,1]`;
- `[8,-3]` -> `[1,0]`;
- `[-5,-5,0,5,5]` -> `[0,0,1/2,1,1]`.

The corresponding Python results agree numerically for these cases.

Boundary behavior is materially thinner than Python:

- singleton and equal two-element inputs reach `0 /Rat 0` and `krun` exits
  113;
- empty `vlist()` reaches the residual `minValue(vlist(.Rats))` and exits 113.

Python raises `ZeroDivisionError` for the first two and `ValueError` for the
third. The K model therefore rejects these paths by getting stuck rather than
modeling the real exceptions. They are outside the successful-return domain,
but this remains part of the trust-boundary accounting.

### Independent positive claims

The seven otherwise unchanged claims were labeled in a scratch audit copy so
each could be selected independently. Each command:

`kprove spec-labeled.k --definition ... --spec-module SPEC-LABELED --claims SPEC-LABELED.cN`

for `N = 1..7` exited 0 and printed `#Top`. The labels alter neither
preconditions nor postconditions. `evidence/stage3.log` records every command,
output, and status.

Stage result: clean build and internal K closure pass.

## 4. Adequacy and real-program pinning

### Plain-language claim inventory

All claims start with empty `<functions>` and `<env>` cells, a `noResult`
result cell, and `verify(solutionProgram, INPUT)` in `<k>`. Their destinations
constrain `<k>` to a specific `done(VALUE)` and retain the empty/reset
auxiliary cells.

1. Claim 1 has no precondition. It proves only the concrete prompt example,
   length 5, with exact output `[0,1/4,1/2,3/4,1]`.
2. Claim 2 has no precondition. It proves only concrete
   `[-5,0,5,5] -> [0,1/2,1,1]`.
3. Claim 3 universally quantifies rationals `A < B`, but only for the
   two-element increasing input `[A,B]`; it returns `[0,1]`.
4. Claim 4 assumes `A < B < C` (plus redundant `A < C`), but only for the
   three-element increasing input `[A,B,C]`; it returns
   `[0,(B-A)/(C-A),1]`.
5. Claim 5 has the same three-element increasing shape and additionally
   assumes `A != C`; it equates the result to proof-local `rescaleSpec`.
6. Claim 6 assumes `A < B < C` for the three-element descending input
   `[C,B,A]`; it returns `[1,(B-A)/(C-A),0]`.
7. Claim 7 assumes `A < B` for exactly `[A,A,B,B]`; it returns `[0,0,1,1]`.

There are no helper or loop claims. The recursive list evaluators are simply
unrolled for these fixed list lengths.

### Pinning and result constraint

`solutionProgram` is a proof-local function whose right-hand side is a
hand-expanded constructor tree. The audit parsed both submitted
`solution.mpy` and that expanded right-hand side to KORE; the two files were
byte-identical after parsing, SHA-256
`9398feb77f7e305f60ce6228d1aafd7edd0395aee8450ba28203b23dab932c72`.
See `evidence/solution-program-expanded.mpy`,
`evidence/stage4_commands.sh`, and `evidence/stage4.log`.

Thus the copied term is the current submitted program, although the proof
build does not itself consume `solution.mpy` and would not automatically
detect a later source change. The independent parse identity check pins this
audited snapshot.

The `verify` wrapper does not replace the function body with an answer. It
executes module registration, invokes `rescale_to_unit`, executes both
assignments and the return expression under ordinary candidate semantics, and
then uses `collect` to move the result into `done` while resetting auxiliary
cells. Destinations contain concrete or algebraically defined values, never a
free result variable, tautology, or one-way implication.

### Satisfying states and concrete substitutions

`evidence/claim_witnesses.py` exhibits a satisfying state for every entry
claim. Representative bindings are:

- claims 3 and 7: `A=0, B=2`;
- claims 4, 5, and 6: `A=0, B=1, C=2`;
- claims 1 and 2 use their concrete inputs.

All initial cells have the exact values required by each claim. Substitution
into every postcondition agrees with both Python implementations for those
witnesses; failure count is zero in `evidence/stage4.log`.

### Material theorem-scope gap

No claim quantifies over a list of arbitrary length. In particular, there is
no theorem for an arbitrary list with at least two elements and distinct
extrema, no generic recursive-list invariant/summary theorem, and no generic
proof that all points undergo the required affine transform. A concrete
length-5 example is not a universal length-5 theorem, and the only
`rescaleSpec` agreement claim is restricted to one sorted length-3 shape.
Therefore even a perfectly faithful numerical semantics would leave the
requested task theorem materially unproved.

Stage result: the seven narrow claims constrain and execute the copied
program, but they are inadequate as a proof of the task contract.

## 5. Rule-by-rule static soundness review

There are no generated helper K source files. The complete local inventory is
28 rules in `semantic.k`, 9 rules in `verification.k`, and 7 reachability
claims in `spec.k`. The mechanical inventory and attribute search are in
`evidence/stage5.log`.

### Syntax, attributes, and configuration

`MPY-SYNTAX` declares:

- `Program = Module(Stmts)`;
- whitespace-separated `Stmts` and comma-separated `Strings` lists;
- `Params(Strings)`, `CellVars(Strings)`, and `FreeVars(Strings)`;
- statements `ImportFrom`, `FuncDef`, `Assign`, and `Return`;
- expressions `Name`, one-argument `Call`, `BinOp`, `ListComp`, and `Bool`;
- `CompFor`;
- rational lists `Rats`;
- values `Rat`, `vlist(Rats)`, and `noResult`;
- stored definitions `function(Params,Stmts)`.

`SEMANTIC` additionally declares `boot`, `exec`, and `invoke` K items. Its
function symbols are `eval`, `evalComp`, `prepend`, `evalNumber`, `minValue`,
`maxValue`, `minRats`, and `maxRats`.

`VERIFICATION` declares function `solutionProgram`, proof-harness K items
`verify`, `collect`, and `done`, and functions `rescaleSpec` and `scaleRats`.

All listed evaluator/specification symbols use `[function]`; none uses
`[total]` or `[functional]`. There are no opaque symbols, trusted claims,
priority rules, `owise` rules, concrete rules, macros, or anywhere rules.
The only simplifications are the three rational equations reviewed below.

The configuration contains exactly `<k>`, `<functions>`, `<env>`, and
`<result>` inside `<python>`. Each non-`<k>` cell is read or written. A heap,
allocation identity, stack, or I/O cell is unnecessary for the submitted
pure function, although real Python exception state and IEEE-754 status are
not represented.

### Used-construct coverage

Every constructor in submitted `solution.mpy` has a declaration and a used
rule path:

- `Module`, `ImportFrom`, and `FuncDef` are handled by module boot/registration;
- the one `Params` entry binds `numbers`; capture metadata is parsed and safely
  ignored because this is a module-level capture-free function;
- `Assign`, `Name`, and the textual calls to `min`/`max` update `minimum` then
  `maximum`;
- `Return`, `ListComp`, `CompFor`, and its literal `Bool(true)` construct the
  result in original order;
- the only binary operations, `-` and `/`, reach `evalNumber`;
- `Stmts`, `Strings`, rational values, and `vlist` supply sequencing and data.

The semantics would visibly get stuck on many unused Python constructs, which
is acceptable for generated minimal semantics.

### `semantic.k` rules S1-S28

1. S1, line 64, expands `boot(Module(SS),ARG)` to module execution followed by
   invocation of the named entry point. This is correct for the submitted
   single-module program.
2. S2, line 66, consumes empty statement lists. Correct.
3. S3, line 67, ignores `ImportFrom`. This is correct for the used
   `from typing import List`, whose annotation has been erased. It is
   over-broad for effectful imports but has no false witness through the
   submitted program.
4. S4, lines 69-70, registers a function by name and continues module
   execution. Correct for the module.
5. S5, lines 72-74, looks up a one-parameter function, resets the local
   environment to that parameter binding, and executes its body. The actual
   binding is unshadowed and has one argument, so binding and evaluation are
   correct for this program.
6. S6, lines 76-77, evaluates a pure expression in the old environment and
   updates the named variable before continuing. This preserves the two
   assignments' order and state.
7. S7, lines 79-81, discards the remaining body statements, preserves the K
   continuation, and stores the evaluated return value. This correctly models
   the used return control effect.
8. S8, line 95, performs environment lookup. Correct for unique map keys.
9. S9, line 97, evaluates the used textual `min` call through `minValue`.
   Correct because no Python binding shadows `min`.
10. S10, line 98, similarly handles the unshadowed `max`.
11. S11, line 100, dispatches every `BinOp` to `evalNumber`; unsupported
    operators then get stuck. The used `-` and `/` are covered.
12. S12, lines 102-103, evaluates a list comprehension but ignores its filter
    expression. The actual filter is the translator's `Bool(true)`, so this is
    sound on every execution of the submitted syntax. The rule is globally
    over-broad: a program with `Bool(false)` could incorrectly retain all
    elements. That witness is not reachable from the submitted program, so it
    is recorded as a narrowness/reuse gap rather than the intended-domain
    unsoundness finding.
13. S13, line 105, performs numeric environment lookup. Correct for rational
    loop elements and extrema.
14. S14, lines 106-107, interprets Python subtraction as exact `-Rat`.
15. S15, lines 108-109, interprets Python division as exact `/Rat`.
16. S16, line 111, gives an empty result for an exhausted comprehension.
    Correct.
17. S17, lines 112-114, evaluates the head with a temporary loop binding and
    recurses on the tail while preserving the outer environment. Correct for
    this pure comprehension and descends structurally.
18. S18, line 116, prepends the computed rational. Correct.
19. S19, line 118, seeds nonempty minimum folding with the head. Correct.
20. S20, line 119, seeds nonempty maximum folding with the head. Correct.
21. S21, line 121, returns the accumulated minimum on an empty tail. Correct.
22. S22, lines 122-123, retains the accumulator when it is less than the head.
23. S23, lines 124-125, retains it when equal.
24. S24, lines 126-127, replaces it when greater.
25. S25, line 129, returns the accumulated maximum on an empty tail.
26. S26, lines 130-131, retains it when greater than the head.
27. S27, lines 132-133, retains it when equal.
28. S28, lines 134-135, replaces it when less.

S16-S28 are terminating on finite rational lists. The three comparison guards
for each extrema fold are pairwise disjoint and exhaustive over ordinary K
rationals. Empty extrema and zero division are deliberately uncovered rather
than falsely totalized.

S14 and S15 are true equations over K's rational domain, but they are
materially unsound as semantics for the used operations of the real
`List[float]` program. This is not merely an informal precision concern:
`evidence/semantic_gap.py` and `evidence/stage5.log` preserve two
false-conclusion witnesses.

The smallest decisive witness uses finite, exactly representable Python
floats:

`A = -2^53`, `B = 1`, `C = 2^53`.

It satisfies claim 4's `A < B < C` precondition. Fresh K execution concludes
the middle output is
`9007199254740993 / 18014398509481984`, while both candidate and canonical
Python executions return exactly `0.5`. Python subtraction rounds
`1 - (-2^53)` before division; exact `-Rat` does not. Thus the K rules enable
a concrete result conclusion that is false of the real generated program on
the intended float type domain.

A second witness uses the finite, exactly representable values
`[-2^1023, 0, 2^1023]`. Exact rationals return `[0,1/2,1]`; Python's range
subtraction overflows, and both real implementations return `[0,0,NaN]`.
This also falsifies the natural-language endpoint conclusion. Neither witness
depends on NaN or infinity in the input, equal extrema, or an excluded short
list.

### `verification.k` rules V1-V9

1. V1, line 9, simplifies `R + (-1*R)` to zero. This is valid rational
   arithmetic.
2. V2, line 10, simplifies `R/R` to one under the necessary nonzero guard.
3. V3, line 11, simplifies `0/R` to zero under the necessary nonzero guard.
   V1-V3 do not overlap inconsistently and do not define division by zero.
4. V4, lines 17-31, defines `solutionProgram` as the actual parsed constructor
   tree. It is a definitional alias, not an oracle; stage 4 checked identity.
5. V5, lines 38-40, starts the proof harness by executing module statements,
   invoking the real body, and appending `collect`. Its `<k>` pattern has no
   arbitrary suffix, and it does not summarize a result.
6. V6, lines 42-45, matches the exact `collect` continuation after return,
   transfers the existing result `V` to `done(V)`, and resets only the three
   auxiliary cells shown. It neither chooses nor fabricates `V`; its exact
   `<k>` context prevents unintended continuation loss.
7. V7, lines 52-53, defines `rescaleSpec` for a nonempty rational list using
   the already reviewed extrema folds.
8. V8, line 55, defines the empty scaling tail.
9. V9, lines 56-58, defines pointwise affine scaling under a nonzero-range
   guard and structurally descends.

V7-V9 truthfully define exact rational rescaling. They do not provide a
connection theorem to IEEE-754 execution, and using the same exact operations
on both sides of claim 5 does not repair that missing bridge. No fresh opaque
value or unconstrained result-bearing oracle occurs.

### Claims C1-C7

C1-C7 are exactly the seven entry claims restated in stage 4. There are no
auxiliary circularities, trusted claims, or loop invariants. Each closes by
finite symbolic/concrete execution under the above rules. Their equations are
internally consistent, but C4 (and the exact-rational interpretation more
generally) has the concrete real-Python counterexample above. C5 is limited to
three sorted elements and only equates execution with a proof-local exact
rational specification. None supplies the missing arbitrary-list theorem.

Stage result: most local rules are faithful to the submitted pure fragment
within an exact-rational abstraction, and no answer oracle or execution bypass
was found. The arithmetic abstraction is nevertheless materially unsound for
the real Python float operations, with explicit intended-domain false
conclusions.

## 6. Fresh non-vacuity test

No candidate `spec-vacuity.k` exists. I created
`evidence/spec-vacuity-audit.k`, mutating the result-bearing destination for
the concrete satisfying input `[0,2]` from the true `[0,1]` to false `[0,0]`.
Both Python implementations confirm `[0,1]`.

The mutated specification successfully parsed and built: `kprove --dry-run`
exited 0. Actual proof then exited 1 with `WarnStuckClaimState`. Its residual
shows the reachable configuration
`done(vlist(0,1,.Rats))` failing to unify with the mutated destination. This
is the expected unmet result obligation, not a parser error, timeout,
unreachable mutation, or unrelated crash. Commands and full bounded residual
are in `evidence/stage6_commands.sh` and `evidence/stage6.log`.

Stage result: the candidate claims are internally non-vacuous and
result-constraining. This does not cure their semantics and scope failures.

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Conditional on the fresh K definition, K's builtin rational/map/boolean/string
domains, and the proof-local rules, the exact submitted constructor tree:

- returns the two concrete outputs in claims 1 and 2;
- returns `[0,1]` for every exact-rational increasing two-point input;
- returns the stated exact-rational affine results for the specified sorted or
  descending three-point shapes;
- agrees with exact-rational `rescaleSpec` for the one sorted three-point
  shape;
- returns `[0,0,1,1]` for the specified repeated-extrema four-point shape.

The wrapper additionally establishes that these results reach `done` with
empty/reset auxiliary cells. The false mutation shows those results matter.

### Trust and assumption ledger

- **K toolchain and proof kernel/backend:** trusted. Fresh execution supplies
  `#Top`; the audit does not independently prove K itself sound.
- **Builtin `RAT`, `BOOL`, `MAP`, and `STRING` modules:** trusted primitives.
  Their ordinary mathematical use is acceptable for a theorem explicitly
  about exact rationals.
- **Trusted translator:** byte-matched to the mounted reference and freshly
  reproduced `solution.mpy`; acceptable source-to-constructor provenance.
- **Hand-expanded `solutionProgram`:** not proved equal inside K, but its
  parsed KORE is byte-identical to submitted `solution.mpy`. This is adequate
  snapshot pinning evidence and does not carry the result.
- **`verify`/`collect` harness:** proof-local instrumentation. Static context
  and state-footprint review shows it executes the body and merely packages
  its existing result; acceptable internally.
- **Exact-rational interpretation of Python floats:** an assumed empirical/
  informal bridge, not a proved connection theorem. It affects every
  arithmetic result and is illegitimate for a claim about the real program,
  because stage 5 supplies concrete false interpretations on satisfying,
  finite float inputs.
- **Python exception behavior:** omitted. K gets stuck for empty/equal-range
  inputs instead of raising the real exception. This is a documented language
  limitation, not proof of those behaviors.
- **Candidate-to-canonical equivalence:** supported by direct source
  inspection and 215 differential cases. This is finite empirical evidence,
  not a universal K theorem; it does not support the K arithmetic bridge.
- **Natural-language property for arbitrary list lengths:** assumed rather
  than proved. No generic list claim, induction, invariant, or summary
  connection exists.
- **Termination:** K reachability here executes fixed finite list shapes.
  The report makes no universal termination claim for arbitrary Python inputs.

### Decision

The reconstructed proof is genuine and non-vacuous only for seven narrow
theorems in an exact-rational model. It does not establish partial correctness
of the real generated Python program over the prompt's float domain:

1. exact-rational subtraction/division permits a demonstrably false claim-4
   result on finite, exactly representable, satisfying input; and
2. no claim covers arbitrary lists of at least two distinct elements.

These are material semantics and adequacy failures, not thin testing or an
informal bridge that happens to preserve all claimed conclusions. Under the
required decision boundary, the candidate is not legitimate.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
