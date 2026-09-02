# Independent adversarial audit: 25-factorize

## Executive decision

The candidate does not contain a legitimate partial-correctness proof of the
real generated program over the task's intended input domain.

The fresh K reconstruction succeeds, but what it reconstructs is only a finite
ground test theorem for 13 constants. There is no symbolic entry claim for an
arbitrary positive integer, no induction/circularity, and no theorem connecting
the recursive program to a universal factorization specification. More
seriously for real-program pinning, every proof claim starts from a
proof-local, hard-coded `SolutionModule()` copy. Neither `spec.k` nor the proof
build consumes `solution.mpy`. A fresh body-sensitivity experiment changed
`solution.py` to return `[]`, regenerated a byte-consistent `solution.mpy` with
the trusted translator, observed `krun(25) = []`, rebuilt the unchanged proof,
and still obtained `#Top` for all original claims. Thus the proof is insensitive
to the actual generated program artifact.

The finite claims themselves are discriminating: a fresh wrong-output mutation
for 25 builds and gets stuck rather than proving. That does not repair the
missing domain theorem or the substituted-program pinning defect.

## 1. Input and provenance integrity

### Rendered-mode boundary

The rendered mode is `GENERATED_SEMANTICS`. `/reference/reference-semantics`
does not exist, as required. I did not search for or infer a hidden reference
semantics. There is no infrastructure-mode contradiction, so a candidate
verdict is appropriate.

Evidence: [01_provenance.sh](evidence/01_provenance.sh) and
[01_provenance.log](evidence/01_provenance.log).

### Required artifacts and types

All candidate source artifacts needed for this submission are present as
regular files: `prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`,
`semantic.k`, `verification.k`, `spec.k`, and `prove.sh`. `run-input.json`,
`metrics.json`, `codex-last.txt`, `codex-output.log`, and the JSONL structured
trace are also regular files. `find -P` found no symlinked required artifact
and no mistyped required source entry.

The candidate contains extra `semantic-kompiled/` and
`verification-kompiled/` trees plus prose, mutation, logs, and trace artifacts.
Those are not source-integrity failures, but none was trusted or reused. Fresh
definitions were built below `/tmp/audit-work/25-factorize-audit`.

The candidate prompt is byte-identical to `/reference/prompt.py`
(`b619821e...b3788`), and the candidate translator is byte-identical to
`/reference/py2mpy.py` (`406485ea...db16`). These hashes also agree with the
untrusted `run-input.json` claims. There are no missing, changed, additional,
mistyped, or symlinked trusted prompt/translator entries to report.

### Untrusted generation records

Both JSON metadata files parse. The 621-record JSONL trace parses record by
record. The 66,336-line `codex-output.log` and the structured trace were
consumed from the candidate only as historical evidence. Their relevant claims
are that all 26 positive claims produced `#Top`, the mutation failed, and the
proof is a “broad ground proof partition.” The log also records
`WarnTrivialClaim` for every final positive claim. None of those historical
claims was accepted without reconstruction.

Stage 1 result: provenance integrity passes; candidate-built products remain
outside the trust boundary.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language and canonical contract

For a meaningful positive integer input `n`, `factorize(n)` must return the
prime factors of `n`, including multiplicity, in nondecreasing order, with
their product equal to `n`. The trusted canonical implementation performs
iterative trial division starting at 2, repeatedly emits a divisor, and appends
the remaining factor when it exceeds 1. It returns `[]` for 0 and 1 and raises
`ValueError` on negative inputs through `math.sqrt`. The prompt does not state
an explicit numeric lower bound, although prime factorization and the product
condition make `n >= 1` the coherent mathematical domain.

The candidate implements the same trial-division idea recursively:

- `n < 2` returns `[]`;
- `divisor * divisor > n` returns `[n]`;
- divisibility prepends the divisor and recurses on the quotient with the same
  divisor;
- non-divisibility increments the divisor.

This is mathematically correct for normally terminating positive executions,
but it uses one CPython call frame per candidate divisor.

### Trusted translation

I regenerated the constructor tree from the copied `solution.py` using the
trusted translator. The regenerated and submitted `.mpy` files are byte
identical and have the same SHA-256,
`bf6ee159...c676714e`.

Evidence: [02_translation.sh](evidence/02_translation.sh) and
[02_translation.log](evidence/02_translation.log).

### Independent differential test

The reviewer-authored script imports the trusted canonical entry point and the
generated entry point from explicit scratch paths. Its documented scope is:

- all integers 0 through 2048;
- the three prompt examples;
- public and helper branch boundaries;
- fixed primes, squares, prime powers, and mixed composites;
- 500 deterministic generated inputs from 1 through 100,000 using seed
  `250723`;
- positive recursion stress input 999,983;
- 11 direct reachable-helper boundary states;
- separate negative probes -4 and -1.

Among 2,540 unique nonnegative entry inputs, 2,539 outcomes match exactly. The
one positive-domain mismatch is:

```text
n=999983
canonical=('return', [999983])
generated=('raise', 'RecursionError')
```

All normally returning generated outputs for `n >= 1` satisfy the independent
product/order/primality check, and all 11 helper boundary expectations pass.
For -4 and -1, the canonical raises `ValueError` while the generated function
returns `[]`.

The positive recursion mismatch is material implementation-to-intent evidence
because the prompt gives no small-input bound. It does not by itself refute a
normal-termination-only partial-correctness implication, but it exposes a real
CPython behavior that the generated K semantics does not model.

Evidence: [02_differential.py](evidence/02_differential.py),
[02_run_differential.sh](evidence/02_run_differential.sh), and
[02_differential.log](evidence/02_differential.log). The expected script exit is
1 because the mismatch is retained rather than hidden.

Stage 2 result: current translation fidelity passes; mathematical behavior
matches broadly on small/representative inputs, but unbounded positive-domain
program fidelity fails at a concrete CPython recursion boundary.

## 3. Clean proof reconstruction

### Fresh builds

Only copied source files were placed in scratch. Before compilation, no
`*kompiled` directory existed at the scratch root. With K
v7.1.293, both commands exited 0:

```text
kompile semantic.k --backend haskell --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/25-factorize-audit/semantic-fresh-kompiled

kompile verification.k --backend haskell --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/25-factorize-audit/verification-fresh-kompiled
```

Evidence: [03_build_fresh.sh](evidence/03_build_fresh.sh) and
[03_build_fresh.log](evidence/03_build_fresh.log).

### Every positive claim

`spec.k` contains 26 unlabeled claims. I split it mechanically into 26
one-claim audit modules, preserving each claim text, and invoked `kprove`
independently on each module. Every one exited 0 and printed an exact `#Top`.
The claim-to-source-line manifest is
[03_split_claims.log](evidence/03_split_claims.log), the run summary is
[03_claims_summary.log](evidence/03_claims_summary.log), and the bounded
per-claim records run from
[03_claim_01.log](evidence/03_claim_01.log) through
[03_claim_26.log](evidence/03_claim_26.log).

Every independent run also reports `WarnTrivialClaim`. Here, ground
`[function]` normalization evaluates the fixed internal machine and the
property functions before reachability search. This warning is not alone proof
of vacuity: Stage 6 confirms that a false ground destination is rejected.

### Concrete generated-semantics execution

The actual submitted scratch `solution.mpy` was executed through the fresh
semantic definition on -1 and 18 normal/nonnegative boundary inputs:
0, 1, 2, 3, 4, 5, 8, 9, 15, 16, 24, 25, 26, 49, 70, 97, 100, and 999. Every
`krun` exited 0. On all 18 nonnegative cases the K result equals both Python
implementations; on -1 it equals the generated Python result `[]` and differs
from the canonical exception.

An optional K run at 999,983 did not complete within the reviewer’s 20-second
per-case bound. That timeout is recorded only as an evidence limitation; it is
not treated as a candidate failure or used in the verdict.

Evidence: [03_semantics_compare.py](evidence/03_semantics_compare.py),
[03_run_semantics_compare.sh](evidence/03_run_semantics_compare.sh), and
[03_semantics_compare.log](evidence/03_semantics_compare.log).

Stage 3 result: the candidate’s finite positive suite reconstructs completely.
This establishes closure of those ground claims under the supplied theory, not
adequacy of the theorem.

## 4. Adequacy and real-program pinning

### Formal preconditions and postconditions

Let

```text
S = {1, 2, 3, 4, 8, 9, 13, 25, 31, 70, 100, 360, 999}.
```

There is no symbolic entry claim, no `requires` clause, and no claim for an
arbitrary `N`.

For each `n` in `S`, the first claim family has the implicit precondition
`true` on one ground initial term, `Run(SolutionMachine(n))`. Its postcondition
is one exact ground `Halted` state, including `.Map` caller locals, the fixed
function map, an empty stack, and the exact list below.

| Input | Exact asserted value |
|---:|---|
| 1 | `[]` |
| 2 | `[2]` |
| 3 | `[3]` |
| 4 | `[2,2]` |
| 8 | `[2,2,2]` |
| 9 | `[3,3]` |
| 13 | `[13]` |
| 25 | `[5,5]` |
| 31 | `[31]` |
| 70 | `[2,5,7]` |
| 100 | `[2,2,5,5]` |
| 360 | `[2,2,2,3,3,5]` |
| 999 | `[3,3,3,37]` |

For each same `n`, the second family also has implicit precondition `true` on
one ground expression. Its postcondition is `Observe(true)` after evaluating
the hard-coded machine value and checking product equality, nondecreasing
order, and primality.

Every entry precondition is satisfiable: its witness is the displayed ground
left-hand term itself. There are no symbolic environment constraints to
satisfy. The independent differential scope includes every member of `S`, so
substitution agrees with both Python implementations on all 13, while the
fresh K runs/claims agree with the asserted lists.

The postconditions are result-constraining for these constants. They are not
tautologies, free-variable results, or one-way implications. They simply have
finite scope.

### Recursive control and helper claims

There is no recursive helper claim, loop invariant, circularity, or induction.
The 13 executions are reduced as ground function computations. Although
`FactorFrom` and `FactorizeSpec` look like a mathematical trial-division
summary, no submitted claim references either symbol and no connection theorem
relates them to program execution.

### The actual `.mpy` is not the proof entry

The concrete configuration in `semantic.k` can execute a parsed
`solution.mpy`. The proof claims do not use that configuration or a `<k>`
cell. They enter at `Run(SolutionMachine(n))`, where `SolutionMachine` obtains
its functions from a separate, manually written `SolutionModule()` equation in
`verification.k`.

The current hard-coded tree was inspected and matches the current submitted
constructor tree. That snapshot equality is an informal/current-artifact
bridge, not a dependency of the proof. `kprove` never reads `solution.mpy`.

The reviewer’s body-sensitivity witness is decisive:

1. Copy `solution.py`, change only the public entry to `return []`.
2. Regenerate `solution.mpy` with the trusted translator and confirm byte
   identity with the mutated `.mpy`.
3. Confirm the mutated `.mpy` differs from the submitted one.
4. Execute the mutated `.mpy`; `krun` returns `[]` for 25.
5. Freshly rebuild unchanged `semantic.k`, `verification.k`, and `spec.k` in
   the mutation directory.
6. Run the original 26 claims; `kprove` still exits 0 and prints `#Top`.

Thus a program whose actual translated result contradicts the proof’s `[5,5]`
postcondition leaves the proof unchanged. This is precisely the
substituted-program/body-sensitivity failure prohibited by the proof-extension
soundness contract.

Evidence: [04_body_sensitivity.sh](evidence/04_body_sensitivity.sh) and
[04_body_sensitivity.log](evidence/04_body_sensitivity.log).

Stage 4 result: FAIL. The ground results are constrained, but the theorem
neither ranges over the intended domain nor pins its execution to the actual
submitted `.mpy`.

## 5. Rule-by-rule static soundness review

The exhaustive expanded inventory, including every local syntax production,
configuration component, function declaration, and individual rule decision,
is [05_rule_inventory.md](evidence/05_rule_inventory.md). The source-level
attribute/rule census is [05_static_checks.log](evidence/05_static_checks.log).
There are no additional generated helper K files.

### Declaration inventory

`semantic.k` has 21 local declaration groups:

- SS01-SS09: translated `Module`, statement/parameter/string/expression lists,
  `ImportFrom`, `FuncDef`, `If`, `Return`, `Int`, `Name`, `BinOp`, `Compare`,
  `ListExpr`, `Call`, and comparison operators;
- SS10-SS16: runtime values, closures, frames, result, `Machine`/`Halted`,
  proof wrapper, and all 14 explicit continuation items;
- SS17-SS21: functions `collect`, `bind`, `bindLists`, `evalBinOp`, and
  `evalCompare`.

`verification.k` has 15 local declaration groups:

- VS01-VS04: `SolutionModule`, `SolutionFunctions`, `SolutionMachine`, and
  `collectStmts`;
- VS05-VS14: `FactorFrom`, `FactorizeSpec`, `PrependFactor`, `Product`,
  `OrderedFrom`, `MachineValue`, `HasDivisor`, `IsPrime`, `AllPrime`, and
  `ValidFactorization`;
- VS15: the non-function `Observe` wrapper.

All 20 declarations named above as functions use `[function]`. There is no
local `[total]`, `[functional]`, `[simplification]`, `[concrete]`, `[owise]`,
priority, macro, alias, or opaque declaration. Accordingly there are no local
priority or simplification rules to trust. No function is claimed total;
unsupported terms remain visibly partial.

### Construct coverage and state/control review

Every construct used by `solution.mpy` maps to syntax and behavior:

- module/import/function collection: SS01-SS05 and SR01/SR27-SR29;
- exact-arity parameter binding: SR03/SR30-SR32;
- statements, conditionals, returns: SR04-SR09;
- literals and local lookup: SR11-SR15;
- left-to-right arithmetic and comparison evaluation: SR16-SR21 plus
  SR33-SR40;
- left-to-right one/two-argument calls: SR22-SR26 plus SR03;
- entry/final result: SR01-SR02/SR10.

The configuration’s `<input>` is copied to an `IntVal` argument, `<result>` is
updated only from `Halted`, and environment/function-map/stack changes occur in
the internal machine. Calls push `(continuation, caller locals)`, returns
discard the callee suffix, pop exactly one frame, and restore caller locals.
The true/false guard rules are complementary. Operator/type and literal/call
arity cases are disjoint on the submitted terms. Division and remainder are
guarded against zero; all reachable operands are positive. This is a sound
minimal model for the small, normally terminating submitted executions.

The model intentionally omits CPython recursion-depth exceptions and finite
stack resources. The 999,983 differential witness shows that omission is
observable on an unbounded positive domain.

### Every semantic rule decision

The 40 `semantic.k` rules are individually decided as follows (the cited
inventory supplies exact LHS/RHS and line ranges):

- SR01-SR09: sound entry, final export, invocation, statement sequencing,
  condition selection, and return behavior on the submitted program.
- SR10: sound on reachable outer-return states but syntactically over-broad
  because it does not require an empty stack. No nonempty-stack `Finish` state
  is reachable from the submitted entry, so this is recorded as a narrowness
  gap, not labeled unsound.
- SR11-SR26: sound literal/name/list, left-to-right operator/comparison, and
  one/two-argument call transitions.
- SR27-SR28: sound empty collection and harmless removal of the submitted
  annotation-only import.
- SR29: sound for the two unique submitted function names. On an unused module
  with duplicate names it would make an earlier definition override a later
  one, unlike Python. Because the submitted program has no duplicate
  definition, this is an out-of-subset limitation, not an unsoundness finding
  about an intended execution.
- SR30-SR32: sound exact-arity binding; mismatches are partial rather than
  fabricated.
- SR33-SR40: sound unbounded-integer/list primitives on the reachable positive
  operands and exact used operators.

### Every verification rule decision

The 22 `verification.k` rules are individually decided as follows:

- VR01 defines the hard-coded current program tree. The equation is internally
  truthful, but its use as the proof’s program source is not file-sensitive.
  VR02-VR04 truthfully derive the function map/direct machine from VR01 and
  inherit that pinning defect.
- VR05 is the below-2 base of `FactorFrom`.
- VR06 stops with `[N]` when `D*D>N`; as a general valid-factorization summary
  it lacks the invariant that smaller candidates have been eliminated.
- VR07 likewise needs that invariant before emitted `D` is known prime and
  ordered. VR08 is the guarded candidate advance, VR09 starts at 2, and VR10
  prepends. VR05-VR10 are unused by all submitted claims.
- VR11-VR12 correctly compute products; VR13-VR14 correctly check
  nondecreasing order; VR15 extracts only halted machine values;
  VR16-VR18 correctly search for divisors from candidate 2 in their actual
  uses; VR19 correctly defines primality; VR20-VR21 check all list elements;
  VR22 is the correct conjunction of product, order, and primality.

The concrete witness for VR06’s missing helper invariant is
`FactorFrom(6,3) = [6]`: 6 is composite, so the result is not a valid prime
factorization. A fresh K claim proves
`ValidFactorization(6, FactorFrom(6,3)) == false` with `#Top`.
Evidence: [05_factorfrom_witness.k](evidence/05_factorfrom_witness.k) and
[05_factorfrom_witness.log](evidence/05_factorfrom_witness.log). This is an
over-broad mathematical-helper defect, not the mechanism closing the submitted
claims; the dead-code check in `05_static_checks.log` finds no use of
`FactorFrom`, `FactorizeSpec`, or `PrependFactor` in `spec.k`.

There is no unconstrained oracle, opaque result-bearing symbol, or
task-answer rewrite in the operational semantics. The exact expected outputs
are in finite postconditions, which is legitimate for those finite theorems
but inadequate for the task-wide theorem.

Stage 5 result: the used small-step/function equations are sound on the
submitted ground executions. Static review independently confirms two broader
limitations—hard-coded program substitution and an invariant-free unused
helper—but finds no hidden semantic rule that can replace the missing
universal proof.

## 6. Fresh non-vacuity test

The candidate’s `mutation-spec.k` was not trusted or reused. I created a fresh
mutation for satisfying ground input 25 that changes the exact result from the
true `[5,5]` to the false one-element list `[5]`.

The mutation artifact is
[06_audit_false_spec.k](evidence/06_audit_false_spec.k). It is byte-identical
to the scratch file used for execution.

Results:

```text
kprove ... --dry-run
exit 0

kprove ... --spec-module AUDIT-FALSE-SPEC
exit 1
WarnStuckClaimState: yes
exact #Top: no
residual actual result: [5,5]
```

The dry run establishes successful parse/build, and the proof failure is the
expected unmet result obligation rather than a parser error, missing import,
timeout, or unrelated crash. Both Python implementations return `[5,5]` for
25, so the mutation is demonstrably false on its satisfying input.

Evidence: [06_run_nonvacuity.sh](evidence/06_run_nonvacuity.sh),
[06_false_mutation_dry_run.log](evidence/06_false_mutation_dry_run.log),
[06_false_mutation_proof.log](evidence/06_false_mutation_proof.log), and
[06_nonvacuity_summary.log](evidence/06_nonvacuity_summary.log).

Stage 6 result: PASS for non-vacuity of the finite exact-output claim. This does
not test universal coverage or actual-file sensitivity; Stage 4’s independent
body mutation tests the latter and fails.

## 7. Proven versus assumed accounting

### What the successful reachability suite actually proves

Under the candidate K definition, the proof-local constructor constant
`SolutionModule()` and its direct internal machine reduce, for each of the 13
constants in `S`, to the listed exact factor list. For the same 13 constants,
the resulting list has K-integer product equal to the input, is nondecreasing
from 2, and every element passes the K divisor-search primality predicate.

That is all. The successful suite does not prove:

- correctness for any positive integer outside `S`;
- a universally quantified relationship between `SolutionMachine(N)` and
  `FactorizeSpec(N)`;
- that a proof build depends on or executes the submitted `solution.mpy`;
- termination;
- absence of CPython `RecursionError`;
- negative-input behavior matching the trusted canonical;
- a full Python semantics outside the exact constructs/states used.

### Trust and assumption ledger

| Boundary | Dependents | Classification |
|---|---|---|
| K v7.1.293 compiler/prover and built-in unbounded `Int`, `Bool`, `Map`, and `List` theories | All K results | Ordinary low-level proof trust boundary; acceptable and freshly exercised. |
| Trusted mounted prompt, canonical implementation, and translator | Intent/translation/differential bridge | Authorized trusted inputs. |
| Snapshot equality between current `solution.mpy` and the hard-coded `SolutionModule()` tree | Claim that the finite theorem describes the current submitted body | Informal/manual bridge only; not consumed by `kprove` and fails body sensitivity. Illegitimate as the required real-program pin. |
| Generated semantics versus CPython | Meaning of K machine execution | Independently supported on 18 nonnegative concrete K cases and 2,539 matching nonnegative differential cases; finite evidence only. Recursion-limit behavior is observably omitted. |
| `FactorFrom` trial invariant | Meaning of unused mathematical helper | Unstated and false for arbitrary `(N,D)`; concrete `N=6,D=3` witness preserved. No submitted claim depends on the helper. |
| Product/order/primality helper equations | Meaning of 13 contract checks | No opaque symbols; equations are ordinary mathematics and were reviewed rule by rule. |
| Absence of resource bounds/exceptions | Extension from mathematical recursion to actual CPython | Not proved. The 999,983 mismatch is concrete contrary evidence for total functional behavior. |

Differential tests, concrete `krun` results, translation identity, and the
body/non-vacuity mutations are evidence for the specific bridges they exercise.
None substitutes for a universal K reachability proof.

### Gate summary and decision

- Gate A, real-program soundness: **FAIL**. The proof entry is the hard-coded
  VR01 tree, not the actual `.mpy`; a translated body mutation changes concrete
  execution but leaves all proof claims at `#Top`.
- Gate B, intent adequacy: **FAIL**. Only 13 fixed inputs are proved. The
  natural contract ranges over positive integers and no general entry theorem
  exists.
- Gate C, trust/evidence auditability: the reconstructed finite evidence is
  reproducible, but the CPython bridge is finite and has a documented recursion
  counterexample. This cannot rescue Gates A or B.

Fresh `#Top` is therefore genuine only for a result-constraining, finite theorem
about a substituted proof-local program term. Under the stated decision
boundary, a substituted program or a missing task-wide proof is
`FAIL / NOT_LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
