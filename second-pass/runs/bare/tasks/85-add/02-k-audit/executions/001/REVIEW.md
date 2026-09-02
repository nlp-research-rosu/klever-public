# Independent adversarial audit: 85-add

Decision: **CONCERNS / LEGIT**.

The candidate contains a freshly reconstructible, result-constraining
reachability proof for the exact submitted `solution.mpy` under its generated
semantics.  I found no intended-domain witness to a false returned value and no
unsound K equation.  The concerns are (1) proof-oriented priority
specializations whose connection to the generic evaluator is mathematically
sound but not fully expressed as one symbolic theorem in the candidate, (2) an
over-broad textual call-binding model, and (3) a real CPython recursion-resource
boundary that the abstract semantics omits.  These limit validation and
intent/implementation coverage without falsifying the partial-correctness
postcondition for normally returning executions.

All candidate artifacts, prior logs, generated traces, and compiled
definitions were treated as untrusted.  Builds and mutations occurred only in
`/tmp/audit-work/85-add`; reviewer scripts, mutations, and bounded logs are in
`/audit-output/evidence`.

## 1. Input and provenance integrity

### Mode boundary

`/reference/reference-semantics` is absent, including as a broken symlink, as
required by `GENERATED_SEMANTICS`.  There is no infrastructure-mode
contradiction.  See `evidence/01-mode-boundary.log` (exit 0).

### Trusted and candidate artifact checks

The trusted files `/reference/canonical.py`, `/reference/prompt.py`, and
`/reference/py2mpy.py` are regular files.  The candidate's required source
artifacts are all regular files:

- `solution.py`, `solution.mpy`
- `semantic.k`, `verification.k`, `spec.k`
- `prove.sh`
- `prompt.py`, `py2mpy.py`
- `run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`
- one structured JSONL trace under `codex-trace/`

There are no symlinks anywhere under `/candidate` or `/reference`.
`/candidate/prompt.py` is byte-identical to `/reference/prompt.py`, and
`/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py` (both
`cmp` statuses 0).  Hashes, types, and comparisons are in
`evidence/01-integrity-hashes-and-cmp.log`; the complete filesystem inventory
is in `evidence/01-file-inventory.log`.

The candidate additionally contains `semantic-kompiled/`,
`semantic-haskell-kompiled/`, `verification-kompiled/`, and `__pycache__/`.
These are extra generated caches, not source-integrity failures.  They were
not copied or used.  No `PROOF.md`, candidate `spec-vacuity.k`, or additional
helper K source was submitted; none was required by the generation prompt.

### Untrusted provenance claims

`run-input.json` claims problem `85-add`, condition `bare`, and
`semantics:false`; its prompt and translator hashes match the trusted files.
`metrics.json` claims exit 0 without timeout.  `codex-last.txt` and
`codex-output.log` claim three concrete executions, 3,950 Python tests, and a
`#Top`.  These were not accepted as proof evidence.  They are transcribed in
`evidence/01-untrusted-small-claims.log` and bounded/extracted in
`evidence/01-untrusted-log-claims.log`.

The structured trace has 232 valid JSON records, from
`2026-07-22T10:59:03.707Z` through `2026-07-22T11:13:22.992Z`.  Its relevant
tool-call claims are summarized without trusting their results in
`evidence/01-structured-trace-summary.log`.  An initial `jq` attempt recorded
in `evidence/01-structured-trace-validation.log` found `jq` unavailable; the
reviewer-authored `evidence/trace_summary.py` then parsed every line
successfully.

Stage 1 result: **PASS**.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementation

The trusted prompt asks: for a non-empty list of integers, return the sum of
the even-valued elements whose zero-based indices are odd.  The canonical
implementation iterates indices `1, 3, 5, ...`, filters values divisible by
two, and sums them.

The submitted implementation is:

```python
def add(lst):
    return 0 if len(lst) < 2 else (lst[1] if lst[1] % 2 == 0 else 0) + add(lst[2:])
```

For ordinary finite executions, each recursive step processes the element at
the current odd index `1`, conditionally adds it, and drops the first two
elements.  This is the same mathematical algorithm by structural induction
on pairs.

### Trusted translation

Only the trusted translator copied from `/reference/py2mpy.py` was used:

```text
python3 py2mpy.py solution.py | tee regenerated-solution.mpy
cmp submitted-solution.mpy regenerated-solution.mpy
```

Both files have SHA-256
`4e0eb1f41f80d2bd858d5ac263ff15e42f1102a5d45a497739fcf863c1bfde6a`;
`cmp` exited 0.  See `evidence/02-translation-byte-identity.log`.

### Independent differential test

`evidence/differential_test.py` independently imports the trusted canonical
entry point and the scratch candidate entry point.  Its oracle is a separate
loop.  It covers:

- the documented example;
- empty, singleton, lengths two and three;
- even, odd, zero, negative-even, mixed-negative, and large integers;
- every list of length 0 through 5 over `[-2,-1,0,1,2]`;
- 3,000 fixed-seed lists of lengths 0 through 80 with values in
  `[-10^12,10^12]`;
- lists `range(1998)` and `range(2000)`.

The exact command was:

```text
python3 evidence/differential_test.py /reference/canonical.py /tmp/audit-work/85-add/solution.py
```

There were 6,919 cases, zero wrong normal return values, and two outcome
differences.  On the two long lists, the candidate raised `RecursionError`
while the canonical function and independent oracle returned `0`; the script
therefore exited 1.  This is a real implementation/totality discrepancy on
the unbounded stated list domain.  It is not a counterexample to the
result postcondition of a partial-correctness theorem, because the candidate
does not return a wrong integer in those cases.  Full results are in
`evidence/02-python-differential.log`.

Stage 2 result: **PASS for returned-value fidelity, with a material
termination/resource concern**.

## 3. Clean proof reconstruction

### Isolation and toolchain

The scratch copy contains only candidate source files and trusted
prompt/translator/canonical files; no candidate `*-kompiled` directory was
copied.  See `evidence/02-scratch-copy.log`.  The independently installed
toolchain is K `v7.1.293` (build `2025-10-03`) with `kompile`, `krun`,
`kprove`, and `kast` in `/usr/bin`; Python is 3.10.12
(`evidence/03-toolchain.log`).

Fresh concrete and proof builds were:

```text
kompile semantic.k --backend llvm --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition semantic-llvm-kompiled

kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-haskell-kompiled
```

Both exited 0.  Logs are `evidence/03-build-concrete-llvm.log` and
`evidence/03-build-proof-haskell.log`.  The warnings concern zero-argument
`[symbol]` attributes and unused claim variables; there was no build error.

### Fresh generated-semantics execution

`evidence/generated_semantics_compare.py` ran the regenerated program through
the fresh LLVM definition on nine cases: empty, singleton, both length-two
parity branches, negative-even, the documented example, multiple
contributions, mixed negatives, and arbitrary-size integers.  Each `krun`
exited 0, and every K result equaled the candidate Python result, canonical
Python result, and independent oracle.  The exact nested commands and input
terms are in `evidence/03-generated-semantics-concrete-compare.log`; summary:
`cases=9 mismatches=0`.

On `list(range(1998))`, fresh K execution exited 0 with result `0`, while
candidate CPython raised `RecursionError` and canonical Python returned `0`.
The exact input generator, term hash, output hash, and outcomes are in
`evidence/07-long-execution-boundary.log`.  This confirms that the generated
semantics is an unbounded mathematical execution model rather than a model of
CPython stack resources.

### Fresh positive proofs

The exact submitted spec was proved with:

```text
kprove spec.k --definition verification-haskell-kompiled \
  --spec-module SPEC
```

It printed `#Top` and exited 0
(`evidence/03-kprove-all-submitted-claims.log`).

For claim-local evidence, `evidence/spec-labeled.k` adds labels without
changing either claim.  The recursive helper alone printed `#Top` and exited
0:

```text
kprove spec-labeled.k --definition verification-haskell-kompiled \
  --spec-module SPEC-LABELED --claims SPEC-LABELED.helper
```

See `evidence/03-kprove-helper-claim.log`.

The entry theorem depends on that recursive helper.  After the helper was
independently proved, the staged entry run retained both claims and marked
only the already-proved helper trusted:

```text
kprove spec-labeled.k --definition verification-haskell-kompiled \
  --spec-module SPEC-LABELED \
  --claims SPEC-LABELED.entry,SPEC-LABELED.helper \
  --trusted SPEC-LABELED.helper
```

It printed `#Top` and exited 0
(`evidence/03-kprove-entry-staged.log`).  This staging introduces no unproved
assumption: the exact trusted helper is the claim proved by the preceding
command.  Diagnostic attempts to filter the entry while also filtering away
its helper were interrupted after continued exploration; their incomplete
logs (`03-kprove-entry-claim.log` and
`03-kprove-entry-with-proved-helper.log`) are not treated as proof failures or
successes.

Stage 3 result: **PASS**.

## 4. Adequacy and real-program pinning

### Claims in plain language

The first claim (`spec.k:9-28`) says: for any inductive integer sequence
`VALUES`, any input cell, caller environment, caller stack, and K
continuation, if the exact singleton function map contains the submitted
`add` body, invoking that body on `pyList(VALUES)` reaches
`pyInt(oddIndexEvenSum(VALUES))`.  The input, caller environment, caller
stack, function map, and arbitrary continuation are preserved.  This is the
recursive call/induction claim.

The entry claim (`spec.k:31-50`) says: for any `ISeq VALUES`, starting from the
exact `solutionProgram ~> start` computation, input `pyList(VALUES)`, and
empty function/environment/stack cells loads the exact `add` body and reaches
the exact final K value `pyInt(oddIndexEvenSum(VALUES))`.

Neither claim has an explicit `requires`; their syntax sorts and cell patterns
are the preconditions.  The entry claim is stronger than the prompt by
including `nil` (empty input).  Both Python implementations and K return `0`
there, so this harmless extension does not weaken the theorem.

### Satisfying states and concrete substitution

A state satisfying the helper precondition is:

- `VALUES = cons(4,cons(2,cons(6,cons(7,nil))))`;
- K starts with `pyList(VALUES) ~> userCall("add")`;
- the function map is exactly the body written in `spec.k:12-26`;
- choose input `pyList(VALUES)`, environment `.Map`, stack `.List`, and empty
  suffix.

A state satisfying the entry precondition uses the same `VALUES`, input
`pyList(VALUES)`, and empty maps/stack with K
`solutionProgram ~> start`.

For this substitution,
`oddIndexEvenSum(VALUES) = evenPart(2) + evenPart(7) = 2`.
Candidate Python, canonical Python, the independent oracle, and fresh `krun`
all return `2` (`evidence/03-generated-semantics-concrete-compare.log`).

### Program identity and body sensitivity

Fresh `kast` expansion of `regenerated-solution.mpy` and fresh expansion of
the proof macro `solutionProgram` produced byte-identical KORE with SHA-256
`96c4f37adb93c32645fbf0a26e853a4627f80b2ce2da3a517ca3b0301b07a02b`;
both `kast` commands and `cmp` exited 0.  See
`evidence/04-program-pinning-kast.log`.

A body-sensitivity mutation changed the base result from `0` to `1`
(`evidence/solution-body-mutated.py`).  Trusted translation and `kast`
succeeded, but the mutated KORE hash changed to
`97c64ebc4e1f8e7fe47060d44e5b448ad7009312830293c7dabd3fa93896dae7`,
and comparison with the proof macro exited 1 as expected
(`evidence/04-body-sensitivity.log`).  The proof is therefore sensitive to
the submitted body rather than merely to the function name.

The postcondition is not a free variable, tautology, or implication: the final
K cell is exactly a `pyInt` containing the recursively defined mathematical
summary.  The helper matches the real recursive control point produced by
the call and environment-restoration rules.

Stage 4 result: **PASS**.

## 5. Rule-by-rule static soundness review

The exhaustive reviewer inventory is
`evidence/rule_inventory.md`.  It enumerates:

- every module, import, configuration cell, and local syntax declaration
  (`S01` through `S18`);
- all 39 rules in `semantic.k` (`R01` through `R39`);
- all four rules/macros in `verification.k` (`V01` through `V04`);
- both claims (`C01`, `C02`);
- every attribute: exactly one `[total]`, two `[priority(40)]`, two
  `[concrete]`, one `[macro]`, and the `[function]` declarations;
- the absence of `[functional]`, simplification rules, fresh values, and
  opaque result functions.

### Construct and state coverage

Every constructor in `solution.mpy` has a declaration and reachable rules.
Module loading strips the single `Return` wrapper and stores the exact
expression.  The outer conditional evaluates `len(lst) < 2`; the inner
conditional evaluates parity; addition is left-to-right; indexing uses `1`;
slicing uses `[2:]`; recursive calls evaluate their argument before binding
`lst`; caller environments are pushed and exactly restored.  The live K
suffix carries expression continuations through calls.  The input and
function cells are preserved except for the initial function load.

`size` covers `nil` and `cons`, is disjoint, structurally descending, and
justifies `[total]`.  `at` and `drop` are intentionally partial, have
disjoint zero/positive rules, and descend.  Their unmodeled negative or
out-of-range cases do not fabricate values; on the submitted path, the
length branch establishes at least two elements before index `1` and drop
`2`.  `evenPart` has exhaustive, disjoint even/non-even equations on every
ground integer.  `oddIndexEvenSum` has disjoint empty, singleton, and
two-or-more equations and descends by two elements.

### Priority operational bridges

The two priority rules are proof-oriented specializations and received extra
review:

1. `len(ARG) < 2` evaluates `ARG` once, then classifies `nil`, singleton, or
   two-or-more shape.  It preserves all cells and the arbitrary continuation.
2. `ITEM if ITEM % 2 == 0 else 0` evaluates `ITEM` once and returns
   `evenPart(ITEM)`.  The modeled expression language has no mutation, I/O,
   allocation, or nondeterminism; repeated evaluation of the identical
   expression in the generic path cannot change its result or final state.
   `evenPart` is not opaque: its two equations fix every ground integer.

For operational sensitivity, the reviewer removed both specializations,
rebuilt generic LLVM and Haskell definitions, and compared complete final
configurations.  Six cases exercising both length branches, both parity
branches, negative values, recursion, addition continuations, call
continuations, environment restoration, and final state were byte-identical
between specialized and generic semantics
(`evidence/05-build-generic-baseline.log`,
`evidence/05-operational-bridge-compare.log`; `cases=6 mismatches=0`).

The universal bridge checks reveal the main validation concern:

- Generic nil and singleton length cases prove with `#Top`
  (`evidence/05-len-nil-singleton-connection.log`).
- A direct two-or-more length connection gets stuck on the missing symbolic
  fact `size(REST)+2 >= 2`
  (`evidence/05-len-bridge-universal-connection.log`).  An attempted
  non-negativity reachability lemma also remains stuck because the prover does
  not split an unconstrained `ISeq`
  (`evidence/05-size-nonnegative-config-lemma.log`).  The fact is nonetheless
  an ordinary induction from the exhaustive `size` equations; there is no
  false ground or intended-input witness.  A functional-claim attempt was
  unsupported by this Haskell backend and is not treated as a verdict signal
  (`evidence/05-size-nonnegative-lemma.log`).
- The direct generic-to-`evenPart` claim gets stuck because `[concrete]`
  prevents symbolic `evenPart` reduction
  (`evidence/05-parity-bridge-universal-connection.log`).  Splitting the exact
  reachable generic computation into the exhaustive guards
  `SECOND % 2 == 0` and `SECOND % 2 =/= 0` proves both universal outcomes
  with `#Top` (`evidence/05-parity-split-universal-connection-fixed.log`).
  These outcomes are exactly the candidate's disjoint `evenPart` equations.

Thus the same result-bearing symbol appearing in the operational bridge and
summary is not accepted merely because it appears twice: its ground meaning
is fixed by exhaustive equations, its exact reachable generic expression is
universally checked under both guards, and opposite ground outcomes disagree
with both the generic and specialized concrete executions.  The missing
single symbolic connection artifact, and the broader `ITEM:Expr` match beyond
the exact submitted subscript, remain documented validation limitations.

### Over-broad but non-falsifying rules

The textual non-`len` call rule dispatches by name in `<functions>` without
modeling local shadowing or first-class callable values.  The specialized
`len` rule likewise assumes that textual `len` denotes the builtin.  These
would be too broad for full Python.  In the actual translated program, the
only local name is `lst`, the only user call is global `add`, and no construct
can create a shadowing binding.  No witness on the intended submitted-program
domain exists, so these are adequacy limitations rather than unsound-rule
findings.

The semantics also omits Python exceptions and stack limits.  Invalid
operations stop rather than fabricate a result, and the actual index/slice
operations are guarded.  The separately observed long-list `RecursionError`
is a termination/resource-model discrepancy, not a false normal result.

No rule is labeled unsound: the audit found no concrete or symbolic witness
on the intended input domain by which any inventoried rule enables a false
returned-value conclusion.  The priority rules are not unconstrained oracles
and do not replace the whole task result; the recursive odd-index aggregation
is still established by the helper claim and `oddIndexEvenSum` recursion.

Stage 5 result: **PASS for intended-domain rule soundness, with documented
bridge and language-model concerns**.

## 6. Fresh non-vacuity test

The reviewer-created `evidence/spec-vacuity-audit.k` keeps the real recursive
helper unchanged and changes only the entry result to:

```k
pyInt(oddIndexEvenSum(VALUES) +Int 1)
```

The satisfying input `[4,2,6,7]` makes the real result `2` and the mutated
obligation `3`, so the mutation is meaningful and reachable.

The dry run:

```text
kprove spec-vacuity-audit.k \
  --definition verification-haskell-kompiled \
  --spec-module SPEC-VACUITY-AUDIT --dry-run
```

parsed and built successfully with exit 0
(`evidence/06-false-mutation-dry-run.log`).  The actual proof command exited
1 with `WarnStuckClaimState`; its residual contains
`oddIndexEvenSum(VALUES) +Int 1 #Equals oddIndexEvenSum(VALUES)` and the final
real configuration contains `pyInt(oddIndexEvenSum(VALUES))`.  This is the
expected unmet result obligation, not a parser error, missing import, timeout,
or unrelated crash.  See `evidence/06-false-mutation-proof.log`.

Stage 6 result: **PASS**.

## 7. Proven versus assumed accounting

### What is machine-proved

Conditional on the fresh K definition:

1. The exact submitted translated AST loads the exact stored `add` body.
2. For every inductive integer sequence, an exact invocation of that body
   reaches `pyInt(oddIndexEvenSum(VALUES))` while preserving its caller state
   and continuation.
3. From the empty initial maps/stack and list input, the whole exact program
   reaches that same exact result.
4. The recursive helper and staged entry both close with `#Top`.
5. The theorem rejects a plus-one result mutation.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K parser/compiler, LLVM/Haskell backends, Kore prover, SMT reasoning | all builds, executions, proofs | Standard unavoidable tool trust. Fresh builds avoid candidate caches. |
| Imported K `INT`, `BOOL`, `STRING`, `MAP`, `LIST` primitives | arithmetic, comparisons, environments, stack | Acceptable low-level primitives. Python and K both use arbitrary-size integers here; divisor is positive `2`. |
| Trusted `/reference/py2mpy.py` | Python-to-`solution.mpy` bridge | Strongly supported by byte identity; no candidate translator was trusted. |
| `solutionProgram` macro equals submitted translation | entry claim | Machine-checked by expanded KORE identity and body-sensitivity mutation. |
| Generated language semantics models the used Python subset | all K conclusions about Python | Manually audited rule by rule and concretely compared. Concern: exceptions, CPython stack limits, name shadowing, and unused Python constructs are not modeled. |
| `len < 2` priority bridge | base/recursive branch choice | Ground/final-state evidence and two universal shape proofs; two-or-more case rests on the informal but elementary induction `size(rest)>=0`. Concern, not a false-rule witness. |
| parity priority bridge and `evenPart` | each selected contribution and final summary | Exact reachable generic computation is universally proved in exhaustive even/odd cases; ground equations are exhaustive. Concern remains that the candidate lacks one direct symbolic connection theorem and the rule match is broader than the submitted expression. |
| `oddIndexEvenSum` means “sum even values at odd indices” | natural-language interpretation | Its equations are the direct pairwise structural definition. The bridge is an ordinary informal induction, supported by zero normal-value mismatches in 6,919 differential cases; finite tests are not a universal proof. |
| CPython termination/resources | natural-language total behavior | Not proved. Long valid lists can raise `RecursionError`; the formal result is partial correctness for normal returns under an unbounded abstract semantics. |

The candidate's `PROOF.md` (absent), trace, prior `#Top`, and differential
tests are not used as substitutes for the fresh K proof.  Differential tests
support only the Python/canonical/summary bridge on tested inputs.  The K
theorem does not prove CPython termination, absence of exceptions, or
behavior for non-integer elements or non-list inputs.

### Final assessment

The fresh proof is sound and non-vacuous on the intended normally returning
program paths, and it pins the real submitted translation rather than a
substitute.  The priority specializations are truthfully defined and no
opposite intended-domain result is admitted, so the evidence does not justify
`FAIL / NOT_LEGIT`.  `PASS` would overstate the bridge and execution-model
coverage: full Python binding/exception/resource semantics is absent, the
candidate raises on sufficiently long valid lists, and the proof-oriented
bridges are not each connected by one complete symbolic theorem inside the
candidate.  The appropriate decision is therefore `CONCERNS / LEGIT`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
