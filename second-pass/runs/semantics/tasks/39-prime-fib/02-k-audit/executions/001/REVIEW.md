# Independent adversarial review: 39-prime-fib

## Executive decision

The candidate contains eleven freshly reproducible, non-vacuous ground
reachability proofs for `prime_fib(1)` through `prime_fib(11)`. Those proofs
execute the two submitted function bodies under the supplied MPY rules and
produce the claimed constants.

They are not an adequate proof of the generated task contract. The natural
contract is parameterized by a positive integer `n`; `spec.k` has no symbolic
entry claim and says nothing about any `n` outside `1..11`. This is a material
domain gap, not a thin empirical bridge. Moreover, the entry configurations do
not load or reference `solution.mpy`: they seed hand-copied closure literals.
The copied closures match the currently submitted program exactly, but a
material mutation of `solution.mpy` leaves the proof build and `pf1` proof
unchanged. Thus the proof artifact itself does not pin the actual translated
file.

The final decision is therefore `FAIL / NOT_LEGIT`. This is not based on a
timeout, infrastructure uncertainty, a failed reconstruction, or a claim that
one of the proof-local equations is mathematically false.

## 1. Input and provenance integrity

### Mode and trusted-mount boundary

The rendered mode is `SUPPLIED_SEMANTICS`, and
`/reference/reference-semantics` is present. There is no rendered-mode
contradiction, so this is a candidate audit rather than `AUDIT_ERROR`.

The candidate `reference-semantics/` tree is recursively byte-identical to the
trusted tree. It has the same files and entry types, has no extra or missing
entries, and contains no symlink. `/candidate/prompt.py` and
`/candidate/py2mpy.py` are also byte-identical to the trusted mounted versions.
See [03_trusted_file_integrity.log](evidence/03_trusted_file_integrity.log).

All candidate semantic-tree entries are ordinary directories or files. The
top-level source artifacts `solution.py`, `solution.mpy`, `spec.k`, and
`verification.k` are regular files. The candidate also contains untrusted
build/output artifacts (`__pycache__`, `kore-exec.tar.gz`, prior `krun` and
`kprove` output). None was used as a compiled definition or proof result. The
archive was only listed, not extracted or executed. See
[02_provenance_inventory.log](evidence/02_provenance_inventory.log) and
[28_untrusted_prior_outputs.log](evidence/28_untrusted_prior_outputs.log).

### Missing provenance artifacts

The following requested generation/provenance inputs are absent from
`/candidate`:

- `run-input.json`
- `metrics.json`
- `codex-last.txt`
- `codex-output.log`
- any identifiable structured generation trace

Their absence is recorded in
[02_provenance_inventory.log](evidence/02_provenance_inventory.log). It reduces
generation auditability but is not used to manufacture the candidate verdict.
There is also no candidate `PROOF.md` or `spec-vacuity.k` to rely on.

The candidate's old three grouped logs each claim `#Top`, and its old `krun`
output claims the eleventh result. These were read only as untrusted claims and
were superseded by the clean runs below.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language and canonical contract

`/reference/prompt.py` says that `prime_fib(n)` returns the `n`-th number that
is both a Fibonacci number and prime, with:

`1 -> 2`, `2 -> 3`, `3 -> 5`, `4 -> 13`, and `5 -> 89`.

The ordinary reading of “n-th” makes the intended input domain positive
integers (`n >= 1`). `/reference/canonical.py` grows the Fibonacci sequence from
`[0, 1]`, decrements `n` whenever the new value is prime, and returns when the
counter reaches zero. For completeness, the trusted canonical implementation
returns `1` at `n = 0` and does not terminate during the bounded `n = -1` test;
those are incidental behaviors outside the inferred positive domain, not part
of the stated n-th-element contract.

The trusted prompt, canonical source, candidate source, translated source,
specification, and verification source are captured with line numbers in
[04_trusted_contract_and_sources.log](evidence/04_trusted_contract_and_sources.log).

### Submitted implementation

`/candidate/solution.py` uses scalar Fibonacci state and a standard
trial-division primality test over `2`, `3`, and the `6k +/- 1` candidates. It
also has finite fast-path lists for the first eleven Fibonacci primes and six
encountered Fibonacci composites. The fast paths preserve the observed
classification; all other integer values follow the general primality test.
For positive `n`, its loop increments `found` exactly on prime Fibonacci
values and returns when `found == n`.

For `n <= 0`, the submitted rewrite immediately returns `0`, unlike the
canonical incidental behavior. This would be a fidelity failure if the task
domain were taken to be all annotated integers. I use the natural positive
domain because “n-th” is undefined for nonpositive indices and all documented
examples start at one.

### Trusted translation

I regenerated MPY with:

```text
python3 /reference/py2mpy.py /candidate/solution.py > solution.regenerated.mpy
cmp -s solution.regenerated.mpy /candidate/solution.mpy
```

Both commands succeeded. The regenerated and submitted files are byte
identical with SHA-256
`5b5767149db4eb45167fdd64d6388b0c19a3d7dca232656816ce67ad31073d26`.
See [05_translation_identity.log](evidence/05_translation_identity.log).

### Independent differential evidence

The reviewer-authored
[differential_test.py](evidence/differential_test.py) independently imports the
trusted canonical entry point and submitted generated entry point. Its complete
scope is:

- all documented examples `n = 1..5`;
- representative positive inputs `n = 6..11`, including all ground proof
  boundaries;
- bounded termination/return observations at out-of-domain `n = 0,-1`;
- 544 helper values covering `-10..500`, every cached value, and both neighbors
  of every cached value, checked against an independent `math.isqrt` primality
  oracle.

The positive entry-point tests have zero mismatches, as do all 544 helper
checks. The recorded out-of-domain differences are canonical `1` versus
generated `0` at `n=0`, and canonical timeout versus generated `0` at `n=-1`.
The script, exact command, full input construction, results, and exit zero are
in [06_differential_test.log](evidence/06_differential_test.log). This is finite
bridge evidence, not a universal K proof.

## 3. Clean proof reconstruction

### Toolchain and isolation

The available independent K tools are version `v7.1.337`; `kompile`, `kprove`,
and `krun` are `/usr/bin` executables. `kup` is absent, but an independently
installed live toolchain works. See
[01_tool_versions.log](evidence/01_tool_versions.log).

Only source artifacts were copied to `/tmp/audit-work`. The semantics used for
both builds came from the trusted `/reference/reference-semantics` tree. No
candidate-provided compiled definition, KORE archive, cache, or proof output was
copied into a definition.

### Concrete build and execution

The fresh LLVM build command was:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

It exited zero. The warnings concern non-exhaustive functions in unused
features (`mapStrVS`, float helpers, `joinCodes`, and `valSeqAt`) and unused
variables in `strLt`; none is reached by this program. The exact build log is
[08_build_concrete.log](evidence/08_build_concrete.log).

The reviewer-generated concrete harness is made by
[make_concrete_harness.py](evidence/make_concrete_harness.py). Fresh `krun`
execution exited zero and produced:

```text
answer_0  |-> 0
answer_1  |-> 2
answer_5  |-> 89
answer_11 |-> 2971215073
```

See [09_make_concrete_harness.log](evidence/09_make_concrete_harness.log) and
[10_run_concrete.log](evidence/10_run_concrete.log).

### Proof build

The fresh Haskell build command was:

```text
kompile verification.k --backend haskell \
  --main-module PRIME-FIB-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition proof-kompiled
```

It exited zero. See [11_build_proof.log](evidence/11_build_proof.log).

### Every positive target claim

I ran each claim in a separate `kprove` process using:

```text
kprove spec.k --definition proof-kompiled \
  --spec-module PRIME-FIB-SPEC \
  --claims PRIME-FIB-SPEC.pfN
```

Every individual command exited zero and printed `#Top`:

| Claim | Input/result | Fresh result | Evidence |
|---|---:|---|---|
| `pf1` | `1 -> 2` | exit 0, `#Top` | `12_kprove_pf01.log` |
| `pf2` | `2 -> 3` | exit 0, `#Top` | `12_kprove_pf02.log` |
| `pf3` | `3 -> 5` | exit 0, `#Top` | `12_kprove_pf03.log` |
| `pf4` | `4 -> 13` | exit 0, `#Top` | `12_kprove_pf04.log` |
| `pf5` | `5 -> 89` | exit 0, `#Top` | `12_kprove_pf05.log` |
| `pf6` | `6 -> 233` | exit 0, `#Top` | `12_kprove_pf06.log` |
| `pf7` | `7 -> 1597` | exit 0, `#Top` | `12_kprove_pf07.log` |
| `pf8` | `8 -> 28657` | exit 0, `#Top` | `12_kprove_pf08.log` |
| `pf9` | `9 -> 514229` | exit 0, `#Top` | `12_kprove_pf09.log` |
| `pf10` | `10 -> 433494437` | exit 0, `#Top` | `12_kprove_pf10.log` |
| `pf11` | `11 -> 2971215073` | exit 0, `#Top` | `12_kprove_pf11.log` |

The preserved driver is
[prove_all_claims.sh](evidence/prove_all_claims.sh), and its aggregate exit-zero
record is [12_all_claims_driver.log](evidence/12_all_claims_driver.log).

Thus clean reconstruction passes for the claims the candidate actually wrote.

## 4. Adequacy and real-program pinning

### Plain-language entry claims

There are no symbolic, helper, loop-invariant, or auxiliary claims. Each of the
eleven claims says:

1. start in the exact ground MPY state with environment location `0`;
2. put two named closure values in scope `0`, whose parent is the builtins scope
   at `-1`;
3. use empty heap and stack, `noRet`, `NoExc`, and exit code zero;
4. execute `Call(Name("prime_fib"), Int(N))`; and
5. reach the exact integer constant listed in the table above, with all
   otherwise unchanged cells matching the claim.

The postconditions are exact constants, not free variables, implications, or
tautologies.

Every entry precondition is satisfiable. There is no `requires` clause: for each
ground `N`, the literal cell configuration in `spec.k` is itself a witness. The
common state template and all eleven substitutions are recorded by
[check_claim_constants.py](evidence/check_claim_constants.py) and
[27_check_claim_constants.log](evidence/27_check_claim_constants.log). Every
claimed constant equals both Python implementations.

### What executes

Once seeded, the closures execute the actual translated statement bodies under
the supplied call, frame, assignment, condition, while-loop, arithmetic, and
return rules. There is no helper summary or loop shortcut.

However, the entry `<k>` cell is only a `Call`; it does not execute
`#loadAll(Module(...))` or otherwise parse/load the submitted `solution.mpy`.
The scope contains `isPrimeClosure` and `primeFibClosure`, two nullary
proof-local aliases whose right-hand sides manually reproduce the function
bodies (`/candidate/verification.k:9-92`).

For the current candidate, this copying is accurate. I compared closures from
a fresh concrete load of `solution.mpy` with the alias-expanded closures in the
fresh proof residual. Both normalized closure terms match exactly:

```text
_is_prime: exact match
prime_fib: exact match
```

See [compare_loaded_closures.py](evidence/compare_loaded_closures.py) and
[26_compare_loaded_closures.log](evidence/26_compare_loaded_closures.log).
Accordingly, I do **not** label either alias equation false.

The connection is nevertheless external to the formal artifact. Neither
`verification.k` nor `spec.k` has a source dependency on `solution.mpy`; the
only textual occurrence is a comment. A fresh body-sensitivity experiment
changed the translated `prime_fib` return from `first` to `999`:

- fresh concrete MPY execution returned `999` for `n=1`;
- the proof definition rebuilt successfully without reading the changed MPY;
- `pf1` still exited zero with `#Top`, proving the stale copied closure returns
  `2`.

Artifacts and exact results are:

- [make_body_sensitivity_mutation.py](evidence/make_body_sensitivity_mutation.py)
- [21_make_body_sensitivity.log](evidence/21_make_body_sensitivity.log)
- [22_run_mutated_program.log](evidence/22_run_mutated_program.log)
- [23_check_program_dependency.log](evidence/23_check_program_dependency.log)
- [24_build_body_sensitivity_proof.log](evidence/24_build_body_sensitivity_proof.log)
- [25_prove_body_sensitivity_pf1.log](evidence/25_prove_body_sensitivity_pf1.log)

This experiment is evidence of a missing mechanical program pin, not a claim
that the current copied literal differs from the current source.

### Material theorem-scope gap

`spec.k` proves only eleven enumerated inputs. It does not state or prove:

- partial correctness for arbitrary positive `n`;
- that a terminating result is the `n`-th Fibonacci prime;
- primality/Fibonacci characterization of a symbolic returned value;
- termination for arbitrary positive `n`; or
- any behavior for `n > 11`.

The comment at `/candidate/spec.k:6-9` says that an unrestricted
total-correctness theorem would imply infinitely many Fibonacci primes. That
observation does not justify omitting the requested partial-correctness
property: a symbolic partial-correctness claim can be conditional on
termination and therefore does not assert that every positive input terminates
or that infinitely many Fibonacci primes exist.

The finite-prefix substitution is a material adequacy failure.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The reviewer-authored [inventory_k.py](evidence/inventory_k.py) inventories
every statement start in the selected supplied semantics, `verification.k`, and
`spec.k`. The complete row-level inventory is
[rule-inventory.csv](evidence/rule-inventory.csv). It contains:

| Kind/attribute | Count |
|---|---:|
| Syntax declarations | 228 |
| Rules | 697 |
| Claims | 11 |
| Contexts | 5 |
| Configurations | 1 |
| `[function]` declarations | 146 |
| `[total]` declarations | 108 |
| `[functional]` declarations | 0 |
| `symbol` declarations | 25 |
| `[no-evaluators]` occurrences | 22 |
| Priority rules | 45 |
| `[owise]` rules | 26 |
| `[concrete]` rules | 35 |
| Simplification/simplifier rules | 0 |

Generation totals and attribute counts are recorded in
[19_generate_rule_inventory.log](evidence/19_generate_rule_inventory.log);
the exact special declarations/rules with source locations are in
[20_special_rule_inventory.log](evidence/20_special_rule_inventory.log).
The supplied files were also read with line numbers in
[13_used_semantics_review.log](evidence/13_used_semantics_review.log),
[14_used_semantics_review_continued.log](evidence/14_used_semantics_review_continued.log),
[15_unused_semantics_review_a.log](evidence/15_unused_semantics_review_a.log),
and [16_unused_semantics_review_b.log](evidence/16_unused_semantics_review_b.log).

Each inventory row records origin, class, attributes, opacity, and the static
decision. No rule is labelled unsound: I found no concrete or symbolic
false-conclusion witness for an inventoried rule on the intended execution
path. The unexercised parts of this broad supplied semantics remain a larger
trusted language boundary; they do not contribute a result-bearing operation
to this proof.

### Used syntax-to-rule map

| Submitted construct | Declaration and active rule families |
|---|---|
| `Module`, `FuncDef`, `Params` | `syntax.k`; module loading/sequencing in `core.k`; function closure creation in `functions.k` |
| `Int`, `Bool`, `Str`, `Name` | `syntax.k`; literal and lookup rules in `core.k`; ASCII string conversion in `str.k` |
| `Assign`, `AugAssign` | `syntax.k`; current-scope writes and integer `+` in `controls.k`/`int.k` |
| `If`, `While`, `Expr` | strict syntax and branch/loop/discard rules in `controls.k`; `truthy` in `core.k` |
| `BoolOp("or", ...)` | `syntax.k`; head-only short-circuit contexts/rules in `bool.k` |
| `Compare` with `==`, `<`, `<=` | evaluation contexts in `operators.k`; integer comparisons in `int.k` |
| `BinOp` with `+`, `*`, `%` | sequential strict evaluation in `syntax.k`/`operators.k`; integer equations and `pyMod` in `int.k` |
| `Call` | callee then left-to-right arguments in `call.k`/`core.k`; closure frame allocation and binding in `call.k`/`functions.k` |
| `Return` | strict return and frame-pop rules in `functions.k` |

Every construct used by `solution.mpy` is modeled. The proof path uses
unbounded mathematical K integers, matching Python's arbitrary-precision
integers for the tested values. `%` divisors are `2`, `3`, or a loop divisor
starting at `5`, so the used path never reaches division by zero. The source
uses no list allocation, mutable heap object, exception, import, float,
dictionary, sort, comprehension, or I/O behavior. Calls bind one argument to
one parameter; scope allocation/pop, callee evaluation, argument evaluation,
return control, and current-scope updates line up with the real control flow.

The supplied configuration has module scope `0`, builtins scope `-1`, empty
heap/stack, and the same control/return/exception cells used by the claims. The
manually seeded scope is observationally the freshly loaded scope for the
current two function definitions, as independently checked above.

### Proof-local extension inventory

`verification.k` contributes only:

| Extension | Class and domain | Value/control influence | Assessment |
|---|---|---|---|
| `isPrimeClosure [function,total]` and its one rule | Nullary definitional alias | Supplies the called `_is_prime` body and therefore all prime branches/results | Equation is exhaustive for the nullary symbol, has no overlap, and exactly matches the currently loaded closure. It is not opaque or an oracle. Mechanical file dependency is missing. |
| `primeFibClosure [function,total]` and its one rule | Nullary definitional alias | Supplies the entry body and therefore the final result | Same assessment: exact current literal, exhaustive and non-overlapping, but copied rather than loaded. |

There are no proof-local priority rules, simplifications, circularities, opaque
symbols, operation intercepts, or result-summary oracles. The two rules do not
replace execution after the call starts; they define the closure values placed
in the initial scope.

### Opaque/trusted declarations in the supplied baseline

The imported supplied semantics declares opaque or proof-domain symbols for
float operations and conversions (`intFloatDiv`, `divII`, `floatMod`,
`floatLt`, `absF`, `floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`,
`powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`,
`roundF`, `roundFN`, `sqrtF`), MD5 (`md5hexCodes`), and sorting (`sortVS`,
`sortKeyVS`). None is syntactically reachable from this program or appears in
an entry postcondition. They therefore have no dependent candidate claim.

The LLVM compiler's non-exhaustiveness warnings are also confined to unused
constructs. They are an evidence limitation for the general supplied language,
not a witness that a false result can be proved for this program.

## 6. Fresh non-vacuity test

No candidate mutation was trusted. I created
[spec-vacuity.k](evidence/spec-vacuity.k), a separate module that preserves the
satisfiable `pf1` initial state but changes the result obligation from the true
`2` to the false `3`.

First:

```text
kprove spec-vacuity.k --definition proof-kompiled \
  --spec-module PRIME-FIB-SPEC-VACUITY --dry-run
```

exited zero, demonstrating that the mutation parses and builds. See
[17_vacuity_dry_run.log](evidence/17_vacuity_dry_run.log).

The actual proof command:

```text
kprove spec-vacuity.k --definition proof-kompiled \
  --spec-module PRIME-FIB-SPEC-VACUITY
```

exited one with `WarnStuckClaimState`. Its residual has `<k> 2 ~> .K </k>`,
which cannot unify with the required destination `3`. This is the expected
unmet result obligation, not a parser error, missing import, timeout, or
unreachable mutation. See
[18_vacuity_proof_expected_failure.log](evidence/18_vacuity_proof_expected_failure.log).

The candidate's eleven ground claims are therefore result-constraining and
non-vacuous.

## 7. Proven versus assumed accounting

### Precisely proven

Under K `v7.1.337`, the supplied MPY theory, and the two proof-local closure
definitions, each of the eleven exact initial call configurations reaches its
listed integer result. Because these cases are concrete and deterministic, the
fresh proof also demonstrates termination in the MPY model for those eleven
calls. The false-result test demonstrates that the destination integers matter.

Nothing in the K claims quantifies over `n` or formalizes “Fibonacci prime.”

### Trust and evidence ledger

| Boundary | Dependents | Status |
|---|---|---|
| K parser/compiler, Haskell prover, and builtin integer/map/list/string theories | All reconstructed claims | Necessary low-level trusted tool boundary; versions and commands recorded |
| Supplied MPY semantics | All program execution | Required trusted input, byte-integrity checked; used rules statically reviewed and concretely sampled |
| Closure aliases equal current module-loaded closures | All entry claims | Exact equality independently observed for both closures, but not a machine-checked source dependency in the proof |
| Trusted translator maps `solution.py` to `solution.mpy` | Program identity | Byte identity established by regeneration |
| Submitted Python agrees with canonical positive behavior | Natural-language bridge | Finite differential evidence for `n=1..11`, plus source inspection and 544 helper checks; not universal proof |
| The eleven constants are the first eleven Fibonacci primes | Meaning of ground results | Supported by the independent canonical oracle and source reasoning, not stated as a K predicate |
| Intended domain is positive integers | Treatment of `n<=0` divergence | Informal interpretation of “n-th”; the two implementations materially differ outside it |
| Imported float/MD5/sort opaque symbols | No candidate claim | Inert and acceptable here; concerning only for other programs that depend on their values |

### Decision rationale

The successful `#Top` results are genuine for the eleven written ground
theorems. Differential testing and prose are not substituted for those K
proofs.

The candidate still fails the requested legitimacy boundary for two material
reasons:

1. Eleven examples do not constitute partial correctness for the parameterized
   positive-input contract. The missing symbolic domain is the substance of
   the task, and partial correctness does not require proving an infinite
   supply or termination for all inputs.
2. The formal entry state substitutes hand-copied closures for loading the
   submitted `solution.mpy`. The copies are correct today, so this is not a
   false equation; nevertheless the fresh body-sensitivity witness proves that
   the proof artifact is insensitive to material changes in the real program.

The missing provenance files are an additional auditability concern but are
not needed for this decision. No infrastructure breach occurred, and no
inventoried rule is called unsound without the required false-conclusion
witness.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
