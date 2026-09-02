# Adversarial proof audit: 108-count-nums

The candidate has a reproducible and non-vacuous K proof under its own
idealized semantics, and its entry theorem mechanically pins the submitted
constructor tree. It is nevertheless not a legitimate partial-correctness proof
of the real generated Python program on the unrestricted HumanEval contract:
the program uses recursion for both list traversal and digit traversal, while
the generated semantics gives calls an unbounded K stack and has no exceptional
control. On concrete contract inputs where CPython terminates by raising
`RecursionError`, the K semantics fabricates normal integer returns and the
formal entry claims assert those returns. This is a material real-program
semantics failure with concrete witnesses, not a hypothetical unused-language
gap.

## 1. Input and provenance integrity

`/audit-input.json` declares:

* problem `108-count-nums`, condition `bare`;
* record layout `legacy-selected-stage1`;
* semantics mode `GENERATED_SEMANTICS`;
* complete input provenance and the launcher container-path map.

I used only those container paths. All required records for this layout are
present, readable real files/directories, and contain no symlink or unsupported
entry:

* `/run.json`, `/task.json`, `/generation-result.json`;
* `/generation-evidence/invocation.json`, `metrics.json`, `codex-last.txt`,
  `codex-output.log`, `prompt.txt`, and the structured trace;
* optional recorded `/generation-evidence/usage.json`;
* `/candidate`, `/reference/canonical.py`, `/reference/prompt.py`, and
  `/reference/py2mpy.py`.

Historical `runtime-metrics.json` is absent, which is explicitly permitted for
this legacy-selected layout. The campaign object in `/audit-input.json` equals
`/audit-campaign-lock.json`; the lock's SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
matching the recorded hash.

Every recorded single-file SHA-256 checked in
[`01_provenance.log`](evidence/01_provenance.log) matches, including the
canonical, prompt, translator, all mandatory generation records, and optional
usage record. The sole trace JSONL has recorded and actual hash
`06a69067b60f58cfffc02c0e626895aa961465701d29e9a114da846f74e5743f`.
All 198 nonempty trace lines parse as JSON; the event/payload inventory is in
that log. Independent length-delimited tree hashes are
`c79888a8ac62ec5fedab2e767d09b339673d4cb957216282a512795c3fff78a7`
for `/candidate` and
`45125ca904315d9fa9bd2b6b31003bdb3d5130b8a86c53b9a7bfd5d643bd44c5`
for the trace. Those respectively match the retained-workspace hashes in the
stage result/invocation and the source-trace hash in `usage.json`.

Candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
mounted versions. As required for `GENERATED_SEMANTICS`,
`/reference/reference-semantics` does not exist; the candidate also has no
`reference-semantics` tree. The generation records were inspected only as
untrusted historical claims. There is no infrastructure breach.

Reproducer:
[`01_provenance_check.py`](evidence/01_provenance_check.py) and
[`01_run_provenance.sh`](evidence/01_run_provenance.sh).

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For an array of integers, return how many elements have positive decimal digit
sum. For a negative integer, only its leading decimal digit is signed negative:
for example, the digit sum of `-123` is `-1 + 2 + 3 = 4`. The prompt states no
list-length or integer-magnitude bound.

The trusted canonical implements that contract by converting each integer to
decimal digits, signing its leading digit, and counting positive sums. The
candidate implements the same mathematics recursively:

* `digit_sum` peels a positive or negative number by decimal quotient/remainder;
* `count_nums` consumes the list head and recurses on `arr[1:]`.

Fresh translation with trusted `/reference/py2mpy.py` is byte-identical to the
submitted `solution.mpy`; both have SHA-256
`4667564c66364b12dfbaed8b67a464cbf96334d266154c27999ace07aab1937b`.

The independent differential script covered the three documented examples,
empty input, every helper branch boundary around `-10/-9` and `9/10`,
zero/positive signed-sum cases, all lists of lengths zero through three over a
15-value boundary alphabet, and 500 deterministic random lists containing
integers of up to 50 decimal digits. There were zero mismatches in 4,126
ordinary cases.

The unrestricted source domain exposes two material divergences in the audited
CPython 3.10 runtime (recursion limit 1,000):

| Satisfying input | Trusted canonical | Candidate Python |
|---|---:|---|
| `[1] * 1200` | returns `1200` | raises `RecursionError` |
| `[10**1199]` | returns `1` | raises `RecursionError` |

These are ordinary finite lists of Python integers admitted by the contract.
The implementation therefore does not implement the contract over its
unrestricted domain. Evidence:
[`02_differential.py`](evidence/02_differential.py) and
[`02_program_fidelity.log`](evidence/02_program_fidelity.log).

## 3. Clean proof reconstruction

I copied only source artifacts to new scratch directories and did not copy or
reuse candidate definitions or caches. K reports version `7.1.293`.

The final clean reconstruction in
[`03c_clean_reconstruction.log`](evidence/03c_clean_reconstruction.log)
performed, in order:

```text
python3 py2mpy.py solution.py > solution.mpy
cmp solution.submitted.mpy solution.mpy
kompile semantic.k --main-module MPY-SEMANTIC --syntax-module MPY-SYNTAX \
  --backend llvm --output-definition semantic-kompiled
krun ... list()
krun ... list(-1, 11, -11)
krun ... list(-123, -100, -99, 0, 10)
kompile verification.k --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX --backend haskell \
  --output-definition verification-kompiled
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

Both builds exited zero. The three `krun` results were respectively
`IntV(0)`, `IntV(1)`, and `IntV(2)`. The proof command exited zero and printed
`#Top`. Fresh exact boundary executions for `-10`, `-9`, `9`, and `10` also
exited zero with results `0`, `0`, `1`, and `1`; see
[`03d_concrete_boundaries.log`](evidence/03d_concrete_boundaries.log).

The seven originally unlabeled claims were copied without semantic changes and
given audit-only labels in [`spec-labeled.k`](evidence/spec-labeled.k).
The digit helper plus the three mutually inductive count claims closed as one
dependency set. Each entry claim then closed with that proven dependency set;
every such `kprove` invocation exited zero and printed `#Top`. See
[`03b_claim_dependency_groups.log`](evidence/03b_claim_dependency_groups.log).
Individual nonempty count/entry claims are not standalone claims when their
explicit digit/count dependencies are excluded; that diagnostic fact does not
invalidate the successful mutually checked set.

Thus fresh verification succeeds under the submitted theory. This dynamic gate
does not validate that theory against real Python.

## 4. Adequacy and real-program pinning

### Claims in plain language

The four helper claims state:

1. for every mathematical integer `N`, calling submitted `digit_sum` under the
   exact submitted function map returns `signedDigitSum(N)`, restoring any
   caller environment/stack and preserving any continuation;
2. calling submitted `count_nums` on the empty list returns zero;
3. on a nonempty list whose head has positive signed digit sum, it returns
   `countPositive` of the whole list;
4. the same result holds for the complementary nonpositive-head case.

The three entry claims start with clean function/environment/stack cells, load
`solutionProgram`, and invoke `count_nums`:

* empty input has no additional precondition and must return zero;
* nonempty positive-head input requires `signedDigitSum(I) > 0` and must return
  `countPositive(VCons(I,REST))`;
* nonempty nonpositive-head input requires `signedDigitSum(I) <= 0` and must
  return the same exact summary.

Those two guards are disjoint and exhaustive for all integer heads, while
`VNil`/`VCons` cover every finite formal list. The return is not free,
existential, tautological, or merely implication-constrained.

### Mechanical identity and witnesses

Fresh `kast --expand-macros --output kore` produced byte-identical, 2,496-byte
terms for submitted `solution.mpy` and proof term `solutionProgram`; both hash
to
`a0dace845f04e05cc7f16fb0cd65272634d1fb01b1318d98fc82e178fca46ee1`.
This is constructor-level identity, not a prose bridge. The exact program loads
the exact two function bodies summarized by `solutionFuns`.

Concrete satisfying entry witnesses are:

| Entry case | Witness | Formal guard | Canonical / candidate / K result |
|---|---|---|---:|
| empty | `[]` | none | `0 / 0 / 0` |
| positive head | `[11]` | `signedDigitSum(11)=2>0` | `1 / 1 / 1` |
| nonpositive head | `[-11,11]` | `signedDigitSum(-11)=0<=0` | `1 / 1 / 1` |

Finally, I changed the actual `countBody` empty return from `Int(0)` to
`Int(1)`. Its expanded `solutionProgram` then differed from submitted
`solution.mpy` at byte 1,635, and the empty entry proof failed with exit 1 and
`WarnStuckClaimState` at the mutated `IntV(1)`. The theorem is sensitive to the
body term it executes. Full commands and outputs:
[`04_pinning_and_body_sensitivity.log`](evidence/04_pinning_and_body_sensitivity.log).

Program-term pinning therefore passes. Real-program semantic pinning does not:
the exact constructor is executed by a language model whose recursive control
behavior differs materially from CPython, as Stage 5 demonstrates.

## 5. Rule-by-rule static soundness review

The exhaustive local inventory is
[`05_rule_inventory.md`](evidence/05_rule_inventory.md). A mechanical check
found exactly 39 rules in `semantic.k`, 11 rules in `verification.k`, and seven
claims in `spec.k`, with no other candidate K helper files and no local
priority, simplification, concrete, anywhere, or opaque declarations; see
[`05_inventory_check.log`](evidence/05_inventory_check.log).

### Construct coverage

Every constructor in `solution.mpy` is declared and mapped:

| Used construct group | Declaration/rules |
|---|---|
| module and two function definitions | S09-S15; R07-R08 |
| invocation, binding, call, return, caller state | S42-S57; R09-R12, R16, R35 |
| nested `if` and Boolean guards | R13-R15 |
| integer/name/empty-list expressions | R17-R19 |
| unary minus; `+`, `%`, `//` with left-to-right order | R20-R26 |
| `<`, `>`, and only-used list equality against `[]` | R27-R34 |
| `arr[0]` and exact `arr[1:]` slice | R36-R39 |

The four proof macros V01-V04 expand to exact submitted constructor subtrees.
They do not rewrite operational `<k>` terms after compilation. The
result-bearing summaries are definitional, not oracles:

* V05-V07 (`signedDigitSum`) have disjoint exhaustive guards
  `N < -9`, `N > 9`, and `-9 <= N <= 9`; recursive magnitude decreases.
* V08-V09 (`boolToInt`) cover both Boolean constructors and agree with the
  trusted `ite` SMT hook.
* V10-V11 (`countPositive`) cover `VNil` and `VCons` disjointly and recurse on
  the finite tail.

No verification rule bypasses source execution or encodes a task result into
an operational transition. Within the idealized unbounded machine, evaluation
order, environments, caller restoration, branches, and all used arithmetic
operations are coherent. Division/remainder see positive dividend/divisor on
every submitted path, so K `/Int`/`%Int` agree with the relevant Python `//`/`%`
uses. Missing behavior for unused general statement sequences, non-used
operators, and non-used slice forms is permissible in generated-semantics mode.

### Material unsoundness and required false-conclusion witness

Rules R11/R12 (calls/returns) use an unbounded mathematical K `List` as their
stack; R35 drives both recursive functions. They never model Python's recursion
limit or `RecursionError`. This is not merely missing semantics for an unused
construct: recursive calls are the implementation's only algorithm.

Fresh concrete comparison gives the false conclusions:

```text
input [1] * 1200
  trusted canonical Python: returns 1200
  submitted Python: raises RecursionError
  generated K semantics on exact solution.mpy: returns IntV(1200)

input [10**1199]
  trusted canonical Python: returns 1
  submitted Python: raises RecursionError
  generated K semantics on exact solution.mpy: returns IntV(1)
```

All commands exited as expected; the two `krun` pipelines exited `0,0`.
Evidence:
[`05_recursion_semantics_witness.log`](evidence/05_recursion_semantics_witness.log).

Accordingly, C06/C07's universal normal-result conclusion includes formal
values corresponding to real executions that terminate exceptionally. The
generated semantics silently replaces that abrupt control effect with a normal
return. The full-source contract contains no bound that would make these
witnesses unreachable. This fails call/control/exception fidelity and is a
concrete real-program false conclusion enabled by R11/R12/R35.

## 6. Fresh non-vacuity test

The fresh mutation
[`spec-vacuity-audit.k`](evidence/spec-vacuity-audit.k) changes the reachable
empty-entry result obligation from `IntV(0)` to deliberately false `IntV(1)`.
Its precondition is satisfied by the clean initial state and input `[]`, for
which both Python implementations return zero.

`kprove --dry-run` exited zero, demonstrating successful parse/build. The real
proof then exited 1—not by timeout, parser error, or missing import—and printed
`WarnStuckClaimState`; its residual had the fully executed configuration at
`IntV(0) ~> .K`, unable to reach `IntV(1)`. The audit wrapper itself exited
zero after checking those expected facts. See
[`06_false_mutation.log`](evidence/06_false_mutation.log) and the raw residual
[`06_false_mutation_kprove.raw.log`](evidence/06_false_mutation_kprove.raw.log).

The formal proof is result-constraining and non-vacuous.

## 7. Proven versus assumed accounting

### What the successful K proof establishes

Conditional on the candidate's generated semantics and imported K domain
theory, the exact submitted constructor program, from clean formal cells,
returns `countPositive(INPUT)` for every finite formal `VList` of mathematical
integers. The mutually checked helper claim establishes that the exact
`digit_sum` body returns the recursively defined `signedDigitSum`; the count
claims then perform structural recursion over the list. This is universal in
the formal algebra and is not a finite unrolling.

It does **not** establish the corresponding universal statement about actual
CPython execution, because the semantic bridge maps finite exceptional Python
executions to normal formal returns.

### Trust ledger

| Boundary | Influence | Accounting |
|---|---|---|
| K 7.1.293 parser, LLVM/Haskell backends, reachability logic | All builds, execution, and proofs | Standard toolchain trust; fresh reconstruction reduces artifact trust but cannot prove the toolchain. |
| Imported `INT`, `BOOL`, `STRING`, `MAP`, `LIST` domain definitions | Arithmetic, conditions, bindings, formal stack | Acceptable low-level K primitives. Used division/remainder domain is independently constrained to positive operands. |
| `boolToInt` `smt-hook((ite #1 1 0))` | Final count arithmetic and proof simplification | Acceptable named SMT boundary; its two exhaustive concrete equations fix exactly the same values. |
| Trusted `/reference/py2mpy.py` | Python-AST-to-constructor identity | Benchmark-supplied translator; byte regeneration plus KORE constructor comparison pins the submitted term. |
| V05-V11 summary equations | Formal postcondition value | Not opaque: exhaustive truthful equations, decreasing recursion, and machine-checked execution claims connect program bodies to them. |
| English signed-decimal intent to `signedDigitSum` | Human-facing property meaning | Ordinary decimal-mathematics bridge; supported by canonical differential tests but not itself a separate machine theorem. No mismatch was found. |
| Trusted canonical and 4,126 ordinary differential cases | Program/intent evidence on tested inputs | Finite empirical support only; not substituted for the K proof. |
| Generated call/return semantics as a model of real Python | Control, exceptional behavior, termination mode, and universal entry results | **Illegitimate for the claimed domain.** It omits the used recursion-limit effect and admits concrete false normal-return conclusions. |

Gate A (real-program soundness) fails on the exception/control witness despite
passing program-term identity and non-vacuity. Gate B (source-contract
adequacy) also fails because the implementation and semantics disagree on a
material unrestricted portion of the list/integer domain. The evidence itself
is reproducible and auditable, but Gate C cannot repair either failure.

The aggregate `#Top` is therefore a valid theorem only of an idealized
unbounded-stack substitute machine. Under the benchmark's explicit mapping,
materially narrowing or changing the unrestricted HumanEval source-contract
domain is `FAIL / NOT_LEGIT`, not a non-fatal concern.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
