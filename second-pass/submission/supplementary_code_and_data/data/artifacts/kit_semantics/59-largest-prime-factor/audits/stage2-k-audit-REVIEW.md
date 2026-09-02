# Independent adversarial review: 59-largest-prime-factor

This audit treats every candidate report, prior `#Top`, trace, cache, and
compiled definition as untrusted. I used the required `using-kit` and
`validating-proof` workflows, rebuilt from source in `/tmp/audit-work/h59`, and
used only reviewer-created outputs below `/audit-output/evidence`.

The reconstructed K theorem is sound, result-constraining, and attached to the
real generated program. It covers the entire HumanEval composite-integer
domain. The reason for `CONCERNS` rather than `PASS` is an evidence boundary:
K proves that execution returns the recursively defined `lpfFrom(N0, 2)`, while
the claim that this summary is the *largest prime factor* is discharged by a
correct but paper-level number-theoretic argument, not by a second
machine-checked K theorem.

## 1. Input and provenance integrity

`/audit-input.json` is readable and declares:

- `record_layout = pipeline-v3`
- `condition = kit-semantics`
- `semantics_mode = SUPPLIED_SEMANTICS`
- candidate, trusted prompt, translator, canonical implementation, supplied
  semantics, generation records, and trace through its `container_paths`

The trusted mount is consistent with this mode:
`/reference/reference-semantics` exists. No infrastructure stop condition was
encountered.

The reviewer script
[`provenance_check.py`](evidence/provenance_check.py) independently inspected
file types, symlinks, bytes, and hashes. Its exact command and results are in
[`provenance-check.log`](evidence/provenance-check.log). In particular:

- `/audit-campaign-lock.json` has SHA-256
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  matching `/audit-input.json`, and its JSON object exactly equals the
  `audit_campaign` block.
- All pipeline-v3 required records are present as regular files:
  `/run.json`, `/task.json`, `/generation-result.json`,
  `invocation.json`, `metrics.json`, `runtime-metrics.json`, `usage.json`,
  `codex-last.txt`, `codex-output.log`, `prompt.txt`, and the structured
  trace.
- Every launcher-declared individual file hash checked by the script matches.
  The final JSONL trace hash is
  `071408e7b120ed59955e81c1214a4abe82a44619c997d0db6975777e3e4eb532`,
  exactly the hash in `/generation-result.json`.
- The candidate's `prompt.py` and `py2mpy.py` are byte-identical to
  `/reference/prompt.py` and `/reference/py2mpy.py`.
- The candidate `reference-semantics/` tree recursively equals the trusted
  tree. There are no missing, additional, changed, mistyped, or symlinked
  entries.
- Independent typed manifests of the candidate, trusted semantics, and trace
  trees are preserved as
  [`candidate-tree-manifest.json`](evidence/candidate-tree-manifest.json),
  [`trusted-semantics-tree-manifest.json`](evidence/trusted-semantics-tree-manifest.json),
  and
  [`generation-trace-tree-manifest.json`](evidence/generation-trace-tree-manifest.json).

I read the run, task, result, invocation, metrics, runtime metrics, usage,
prompt, last-message, output-log, and structured-trace records. The trace
contains 394 valid JSON events across the original and OOM-resume turns. A
bounded full-event structural parse is recorded in
[`generation-trace-summary.log`](evidence/generation-trace-summary.log).
Generation claims such as “VALIDATED”, 4,331 differential cases, and prior
`#Top` results were not used as proof evidence.

One untrusted-record inconsistency is visible: `usage.json` says
`source_trace_sha256 =
f4f6e40a0eea719ffa8eaa6dd175b827ec99f72ebcd3dde97aa15efec9e54889`,
which is not the hash of the final mounted JSONL. This is not an infrastructure
breach: the final mounted file is present, readable, structurally valid, and
matches the authoritative stage output hash in `/generation-result.json`.
The inconsistency is confined to an internal claim in an untrusted usage
record.

All required candidate proof artifacts are present. Candidate
`runtime-kompiled/`, `verification-kompiled/`, `__pycache__/`, `PROOF.md`,
`prove.sh`, prior negative probes, and prior logs were ignored as authorities.

Stage 1 result: **PASS**.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

`/reference/prompt.py` requires `largest_prime_factor(n)` to return the largest
prime factor of an integer `n`, under the assumptions that `n > 1` and `n` is
not prime. Its examples are:

- `largest_prime_factor(13195) == 29`
- `largest_prime_factor(2048) == 2`

`/reference/canonical.py` enumerates divisors from 2 through `n`, tests their
primality, and retains the largest prime divisor.

The candidate `solution.py` instead performs trial division. It starts
`factor = 2`; while `n > factor`, it divides `n` by `factor` when divisible and
otherwise increments `factor`; it returns the remaining `n`. Mutating the local
parameter is observationally harmless because the function returns only the
largest factor and has no external state.

### Trusted translation identity

I copied source artifacts, but not compiled artifacts, to scratch. Running the
trusted translator there produced a file byte-identical to the submitted
`solution.mpy`:

```text
solution.mpy SHA-256:
7b5386bd187d75e90569bbfe39620c61a31c0c39d3740bf6eca58b4c91f88229
regenerated-solution.mpy SHA-256:
7b5386bd187d75e90569bbfe39620c61a31c0c39d3740bf6eca58b4c91f88229
```

The command and exit 0 are in
[`translator-byte-identity.log`](evidence/translator-byte-identity.log).

### Independent differential test

[`differential_audit.py`](evidence/differential_audit.py) imports the trusted
canonical entry point and the scratch copy of the generated entry point under
separate module names. It checks:

- both documented examples;
- the smallest composite boundary, 4;
- values selected to exercise initial loop exit, divisible, non-divisible, and
  repeated-division paths;
- every composite from 4 through 5000;
- seven additional generated composites, including powers and semiprimes; and
- four prime boundary cases covered by the broader K claim but not required by
  the prompt.

An “empty” case is not meaningful for this scalar integer contract. Inputs
below 2 and non-integers are outside the stated domain.

The run covered 4,338 prompt-domain cases and four claim-only prime cases,
with zero mismatches. The script, exact command, exit 0, and all generated
inputs/results are preserved in
[`differential-audit.log`](evidence/differential-audit.log) and
[`differential-inputs-results.json`](evidence/differential-inputs-results.json).

Stage 2 result: **PASS**.

## 3. Clean proof reconstruction

The source-only scratch setup is recorded in
[`scratch-prepare.log`](evidence/scratch-prepare.log). The copied semantics came
from the trusted `/reference/reference-semantics`, not from a candidate cache.
The toolchain record is in [`toolchain.log`](evidence/toolchain.log): K
v7.1.293 and Python 3.10.12.

### Concrete definition

I freshly ran:

```text
kompile /tmp/audit-work/h59/reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/h59/runtime-kompiled
```

It exited 0. The exact output is
[`kompile-llvm.log`](evidence/kompile-llvm.log). The compiler warned about
unrelated incomplete total helpers such as `mapStrVS`, `floorFI`, `joinCodes`,
and out-of-bounds `valSeqAt`; none can occur in this integer-only program.

A reviewer-authored concrete driver was translated with the trusted translator
and executed with the fresh LLVM definition. `krun` exited 0 with `.K`,
`NoExc`, an empty heap and stack, and these bindings:

```text
documented_13195       |-> 29
documented_2048        |-> 2
boundary_4             |-> 2
nondivisible_branch_15 |-> 5
repeated_division_16384|-> 2
```

See [`translate-concrete-driver.log`](evidence/translate-concrete-driver.log)
and [`krun-concrete.log`](evidence/krun-concrete.log).

### Proof definition and claims

I freshly ran:

```text
kompile --backend haskell /tmp/audit-work/h59/verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/h59/verification-kompiled
```

It exited 0; see
[`kompile-haskell.log`](evidence/kompile-haskell.log). Only unused-variable
warnings from trusted `str.k` appeared.

The candidate has two positive claims, an auxiliary loop circularity and the
entry theorem. I ran the loop claim alone and the complete spec from the fresh
definition:

```text
kprove spec.k --definition verification-kompiled \
  --spec-module SPEC --claims SPEC.loop
#Top
exit 0

kprove spec.k --definition verification-kompiled \
  --spec-module SPEC
#Top
exit 0
```

The complete-spec command is the target proof and proves both claims with the
loop circularity available to the entry theorem. Exact records are
[`kprove-loop.log`](evidence/kprove-loop.log) and
[`kprove-complete-spec.log`](evidence/kprove-complete-spec.log).

For completeness, I tried `--claims SPEC.entry` both with and without
`--trusted SPEC.loop`. In this K version, claim filtering omits the loop
circularity in both forms, causing unbounded symbolic loop unrolling. I
terminated those diagnostics; they are not candidate target commands and do
not contradict the successful complete-spec proof. They are documented in
[`kprove-entry.log`](evidence/kprove-entry.log) and
[`kprove-entry-with-proved-loop.log`](evidence/kprove-entry-with-proved-loop.log).

Stage 3 result: **PASS**.

## 4. Adequacy and real-program pinning

### Claims in plain language

`SPEC.loop` says:

- Start at the exact internal `#while` term used by the submitted body, followed
  by its exact `Return(Name("n"))`, `#endcall`, and empty continuation.
- The active local frame binds `n` to symbolic `N` and `factor` to symbolic
  `F`, with `F >= 2`.
- The exact submitted closure is present in the module scope; the caller frame,
  scope locations, heap, stack, return state, exception, and exit code are
  pinned.
- If this configuration terminates, it produces an integer equal to
  `lpfFrom(N, F)`, removes the callee frame, restores the caller, and leaves the
  stated observable cells intact.

`SPEC.entry` says:

- Start from the normal empty-module configuration.
- Load the embedded `Module(FuncDef("largest_prime_factor", ...))`.
- Call that binding with symbolic integer `N0`, under `N0 >= 2`.
- If the call terminates, the final integer is exactly
  `lpfFrom(N0, 2)`, with the function binding retained and all call-local state
  cleaned up.

The prompt's required domain is composites greater than 1. `N0 >= 2` is
strictly broader, so the claim does not narrow the HumanEval contract.

The result is not free or tautological. `?RESULT` is existential at the
destination but is constrained by an equality to a deterministic guarded
summary. The fresh false-result mutation in Stage 6 confirms that this
constraint is exercised.

### Mechanical program pinning

[`extract_entry_module.py`](evidence/extract_entry_module.py) extracts the
`Module(...)` inside `SPEC.entry` without copying it by hand. `kast` then parses
both the submitted `solution.mpy` and the extracted term to KORE.

The spec writes five explicit `.Stmts` list units. Those units are accepted in
claim syntax but not by the standalone program scanner, so the reviewer removed
only those identities and repeated the parse. Both constructor terms then had
the same 3,839-byte KORE and SHA-256:

```text
eb9409e5a571c610869b4da94884f5b409657488302ac0e6aa5cbe19802bba18
```

The initial scanner failure and the successful normalized comparison are both
preserved in [`program-pinning.log`](evidence/program-pinning.log) and
[`program-pinning-normalized.log`](evidence/program-pinning-normalized.log).
This is a mechanical constructor-level identity, not a visual source
comparison.

### Satisfiable states and concrete substitutions

The preconditions are plainly satisfiable:

- Entry witness `N0 = 4` satisfies `N0 >= 2`; both Python implementations and
  `lpfFrom(4,2)` return 2.
- Loop witness `N = 15, F = 2` satisfies `F >= 2`; both Python
  implementations and `lpfFrom(15,2)` return 5.
- The documented substitutions return 29 for 13195 and 2 for 2048.

Exact summary traces and comparisons are in
[`ground-claim-witness.log`](evidence/ground-claim-witness.log).

A separate reviewer mutation changed every embedded instance of the executed
function's initialization from `factor = 2` to `factor = 3`, including the
`#loadAll` program term and expected final closure. For `N0 = 4`, the mutated
program reaches result 4 rather than the original required result 2. It parses
successfully and is rejected by `kprove`; see
[`spec-body-mutation.k`](evidence/spec-body-mutation.k),
[`body-mutation-dry-run.log`](evidence/body-mutation-dry-run.log), and
[`body-mutation-proof.log`](evidence/body-mutation-proof.log). This demonstrates
body sensitivity of the term actually executed by the claim.

### Summary-to-contract bridge

The recursive summary follows the program:

```text
lpfFrom(N,F) = N                  when F >= 2 and N <= F
lpfFrom(N,F) = lpfFrom(N/F,F)     when F >= 2, N > F, and N % F = 0
lpfFrom(N,F) = lpfFrom(N,F+1)     when F >= 2, N > F, and N % F != 0
```

For a composite original input `X`, a suitable loop invariant is:

1. `n >= factor >= 2`;
2. no integer in `[2, factor)` divides `n`; and
3. the largest prime factor of `n` equals that of `X`.

Initially this is immediate. On a non-divisible step, incrementing `factor`
extends the excluded-divisor interval. On a divisible step, the excluded
interval makes `factor` prime. If `n = factor*q`, then `q >= factor`; otherwise
`q` itself would be a forbidden divisor in `[2,factor)`. Dividing by `factor`
therefore preserves the largest remaining prime factor and the excluded
interval. At exit, `n <= factor` and the invariant give `n = factor`; the lack
of smaller divisors makes it prime, and item 3 makes it the largest prime
factor of `X`.

This argument is mathematically sound and the differential test corroborates
it on finite inputs. It is not encoded as a K theorem. That is the non-fatal
adequacy/evidence limitation responsible for the final `CONCERNS` status.

Stage 4 result: **PASS with a documented informal intent bridge**.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[`inventory_k.py`](evidence/inventory_k.py) inventories the trusted assembled
semantics, every helper K file, and candidate `verification.k`.
[`rule-inventory.tsv`](evidence/rule-inventory.tsv) contains all 932 local
declarations:

- 228 syntax declarations;
- 698 ordinary rules;
- 5 evaluation contexts; and
- 1 configuration.

The inventory includes 147 `[function]` declarations, 107 `[total]`
declarations, 29 priority-bearing rules, 32 `[concrete]` rules, 26 `[owise]`
rules, 22 `[no-evaluators]` opaque declarations, three macro declarations and
one macro-recursive declaration. There are no `[functional]` declarations and
no simplification rules.

[`assess_inventory.py`](evidence/assess_inventory.py) attaches an audit
decision and rationale to every inventory row. The resulting exhaustive
[`rule-assessment.tsv`](evidence/rule-assessment.tsv) classifies:

- 4 proof-local declarations/rules as sound;
- 42 proof-relevant fixed rules as sound;
- 45 used foundation declarations as sound;
- 16 used syntax declarations as sound;
- 21 concrete-only declarations/rules as absent from the proof;
- 22 fixed opaque boundaries as unreachable;
- 9 known fixed-semantics limitations as unused or as having their subset
  assumption satisfied; and
- the remaining fixed declarations/rules as unreachable because their source
  constructor or value domain is absent from `solution.mpy`.

This per-row file is the detailed rule inventory; the rest of this section
records the substantive review conclusions rather than repeating 932 rows.

### Used syntax and fixed rule paths

| Submitted construct | Declaration and operational path |
|---|---|
| `Module`, `FuncDef`, `Params` | `syntax.k`; `core.k` `#loadAll`/statement sequencing; `functions.k` function binding |
| `Call`, `Name`, one integer argument | `call.k` callee-first routing; `core.k` lexical lookup and left-to-right `#evalArgs`; `functions.k` parameter binding |
| integer literals and locals | `core.k` literal and scope-map rules; `controls.k` assignment |
| `While` | `controls.k` `While => #while`, guard evaluation, `#whileCond`, and `#loopLbl` |
| `If` | `controls.k` strict condition and `#branch` true/false rules |
| `%`, `//`, `+` | `operators.k` sequential operand evaluation and dispatch; `int.k` integer equations |
| `>`, `==` | `operators.k` comparison contexts/dispatch; `int.k` Boolean comparisons |
| `Return` | `functions.k` return state, stack pop, scope deletion, environment restoration |

The syntax attributes give left-to-right evaluation for every material binary
operation, and the comparison contexts evaluate the left and then wrapped
right operand. Call lookup selects the module binding actually loaded. The
entry claim starts with an empty local module scope and the fixed builtins
scope, so there is no alternate binding. The call rule pushes the exact
continuation and frame; the loop claim includes that frame and exact return
suffix; `#pop` restores every pinned cell. No material state, exception,
allocation, or control effect is omitted.

All divisors in the proof are at least 2. Thus `pyMod(N,F)` and
`(N-pyMod(N,F))/F` implement Python floor modulo/division on the only domain
used, without division by zero. The `lpfFrom` divisible equation uses this
exact fixed-semantics expression.

### Proof-local extensions

`verification.k` adds only:

1. `syntax Int ::= lpfFrom(Int, Int) [function]`; and
2. three guarded equations.

There are no proof-local priority rules, simplification rules, opaque symbols,
`[total]` assertions, trusted primitives, or operational bridges.

The three guards are disjoint and exhaustive wherever the summary is used:
`F >= 2`, split first by `N <= F` versus `N > F`, and then by modulo zero
versus nonzero. Overlap cannot yield different right-hand sides. Recursion is
well-founded on the lexicographic natural measure `(N, N-F)` at reachable loop
heads: a division strictly lowers `N`, and an increment preserves `N` while
lowering `N-F`. `lpfFrom` never matches program syntax and therefore never
preempts fixed execution. `SPEC.loop` is the bridge-free connection theorem
from exact fixed loop execution to this summary.

Distinct ground outcomes 2, 5, and 29 are recorded in the satisfying-witness
evidence. The equations fix those values; an opposite interpretation is not
admitted.

### Priorities, opaque symbols, and fixed-semantics limitations

All 29 priority-bearing rules come from the trusted fixed semantics. The
potentially overlapping cell-reference, heap-reference, math-call, method, and
collection paths are rejected here by constructor shape or by guards: the
audited locals are integers, the scopes have no `"$cells"` marker, the heap is
empty, and the call is a plain call to the loaded closure. None can preempt the
used integer path.

The 22 `[no-evaluators]` symbols cover float operations, sorting, and MD5. No
submitted term constructs a float, string, collection, `sorted`, or MD5 call,
and none of these symbols occurs in either postcondition. They have no value,
control, state, or termination influence on the theorem. `MPY-CONCRETE` is
imported by the LLVM test module only and is absent from `VERIFICATION`.

The fresh LLVM build reported incomplete-total warnings for unused helpers.
`valSeqAt` is also intentionally underspecified out of bounds. These would be
important for programs using the affected features but cannot be reached by
this integer program.

Two supplied rules are deliberately not globally Python-faithful:

- `controls.k` treats unsupported `ImportFrom` forms as no-ops.
- `float.k` treats `Import` as a no-op for its syntactically intercepted math
  subset.

A concrete false-conclusion witness outside this submitted program is
`import does_not_exist; result = 7`: CPython raises
`ModuleNotFoundError`, while the no-op import rule permits execution to
continue to 7. The analogous `from does_not_exist import x` witnesses the
other rule. These are explicit fixed-subset boundaries, not candidate
proof-local extensions, and `solution.mpy` contains no import constructor.
They cannot enable a false conclusion on any intended input to this program.

The supplied frame-pop rule assumes that a local closure does not escape its
defining frame, and the assertion rule is smoke-program oriented. The
submitted function returns an integer and contains neither a nested closure
nor an assertion, so those fixed boundaries are also inert.

No rule encodes the largest-prime-factor answer, skips a material submitted
operation, fabricates a result for a used construct, or exposes an
unconstrained program-derived oracle.

Stage 5 result: **PASS for the audited theorem**.

## 6. Fresh non-vacuity test

I did not rely on the candidate `spec-negative.k`.

[`make_false_mutation.py`](evidence/make_false_mutation.py) created a distinct
reviewer spec with the satisfiable precondition `N0 == 15` and changed the
entry result obligation from:

```text
?RESULT ==Int lpfFrom(N0, 2)
```

to:

```text
?RESULT ==Int lpfFrom(N0, 2) +Int 1
```

The mutation is demonstrably false: the canonical implementation, generated
implementation, and summary all return 5, while the mutation requires 6.

`kprove --dry-run` exited 0, proving that the mutation parsed and built. The
actual proof exited 1 with `WarnStuckClaimState` and final `<k> 5 ~> .K </k>`.
It failed at the result obligation, not because of parsing, timeout, a missing
import, or an unrelated crash. The mutation and exact logs are:

- [`spec-vacuity.k`](evidence/spec-vacuity.k)
- [`false-mutation-dry-run.log`](evidence/false-mutation-dry-run.log)
- [`false-mutation-proof.log`](evidence/false-mutation-proof.log)

The independent embedded-body mutation described in Stage 4 also built and
failed with final result 4, providing separate body-sensitivity evidence.

Stage 6 result: **PASS**.

## 7. Proven versus assumed accounting

### What the K proof establishes

Under the exact supplied `MPY` definition and candidate `lpfFrom` equations,
for every K integer `N0 >= 2`, if the exact regenerated
`largest_prime_factor` call terminates, it:

- uses the loaded function binding;
- evaluates its argument and integer operations in the fixed order;
- executes the real initialization, loop, conditional, assignments, and
  return;
- restores the environment, scopes, stack, return, exception, heap, allocation,
  and exit-code cells specified by the claim; and
- returns exactly `lpfFrom(N0, 2)`.

The auxiliary claim establishes the corresponding exact loop execution theorem
for every integer `N` and every `F >= 2`. This is partial correctness. K does
not establish termination.

### Assumptions and trust ledger

| Boundary | Influence and dependents | Assessment |
|---|---|---|
| Supplied `reference-semantics/` | Defines all execution, state, and control used by both claims | Acceptable fixed task boundary; exact integrity verified. Material integer/call/control rules were statically audited. |
| Trusted `py2mpy.py` | Determines the constructor program associated with `solution.py` | Acceptable fixed task boundary; regenerated output is byte-identical, and the entry term has identical parsed KORE. Correctness of the translator relative to full CPython is not itself proved. |
| K v7.1.293 Haskell backend, SMT reasoning, and K integer/map/list hooks | Establish `#Top` and built-in arithmetic/state facts | Standard proof-engine trust boundary. Fresh reconstruction prevents candidate-cache substitution. |
| `lpfFrom` equations | Fix the postcondition value and close the loop/entry claims | Proven-connected definitional summary, not an opaque primitive or operational bridge. |
| Elementary number theory and unique prime factorization | Connects `lpfFrom(N,2)` to “largest prime factor of N” | Correct informal derivation, but not machine-checked in K; this is the main concern. |
| Termination measure | Supports total behavior informally, although the requested K result is partial correctness | The lexicographic measure is valid on reachable states; not part of the K theorem. |
| Differential and LLVM execution | Supports source/semantics adequacy on finite cases | Reproducible finite evidence only; not a substitute for the reachability proof or number-theory bridge. |
| Imported opaque float/sort/MD5 symbols and unused incomplete-total helpers | None: absent from executed terms and postconditions | Inert for this theorem; they do not need an interpretation to close or understand the result. |

### Final decision

Gate A (real-program soundness) passes: the proof executes the real body, has
no operational bridge or oracle, constrains the result, and rejects both result
and body mutations. Gate B covers the material source-contract domain; the
formal precondition is broader, not narrower. Gate C evidence is reproducible.

The theorem is therefore legitimate. It is not an unqualified `PASS` because
the K postcondition names an execution summary rather than formalizing
primality, divisibility, and maximality, leaving the final intent bridge to a
paper argument. Under the benchmark decision boundary, that non-fatal informal
intent bridge maps to `CONCERNS / LEGIT`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
