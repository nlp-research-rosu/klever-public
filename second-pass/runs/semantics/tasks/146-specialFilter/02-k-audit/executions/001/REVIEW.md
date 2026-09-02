# Independent adversarial audit: 146-specialFilter

The candidate is **not a legitimate partial-correctness proof of the requested
program over its intended integer-list domain**. Fresh reconstruction does
produce `#Top` for both submitted claims, and the implementation agrees with
the canonical Python function on the tested domain. Those facts do not rescue
the proof: the only function-entry theorem is for the empty list, while the
universal loop theorem replaces the result-bearing decimal computation with
three unconstrained proof-local symbols that are reused in its postcondition.
A fresh opposite-interpretation experiment proves a symbolic conclusion whose
concrete `N = 12` instance is false.

The rendered mode is `SUPPLIED_SEMANTICS`. The trusted mount is consistent with
that mode, so this is a candidate verdict rather than an infrastructure error.

## 1. Input and provenance integrity

I treated every file below `/candidate` as untrusted and copied only source
artifacts into fresh directories below `/tmp/audit-work`. I did not copy or use
candidate compiled definitions or caches.

The mode boundary passes. `/reference/reference-semantics` is a real directory.
A recursive path/type/content comparison between it and
`/candidate/reference-semantics` found zero differences. There are no missing,
additional, changed, mistyped, or symlinked entries in the candidate semantics
tree. The candidate `prompt.py` and `py2mpy.py` are regular files and byte-match
their trusted versions:

- prompt SHA-256:
  `310a71d2feca4b63bf4ab0279cac60820a61a57157a413efd62823e6c69eb917`
- translator SHA-256:
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`

The required source files `solution.py`, `solution.mpy`, `spec.k`, and
`verification.k` are regular files, not symlinks. No source-type defect was
found.

The requested provenance records are all missing:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`

No structured generation trace is present. `PROOF.md` is also absent. The
candidate does contain untrusted `call-proof.out` and `loop-proof.out` files,
each containing only `#Top`, plus `concrete-krun.out`; none was relied on.

Evidence: [integrity script](/audit-output/evidence/stage1_integrity.sh) and
[bounded log](/audit-output/evidence/stage1_integrity.log).

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt requires counting array elements that:

1. are greater than 10; and
2. have odd first and last digits in their ordinary decimal representation.

The trusted canonical implementation iterates over `nums`, converts each
qualifying number with `str`, converts its first and last characters to
integers, and tests membership in `(1, 3, 5, 7, 9)`. The candidate uses direct
character membership in `"13579"`. For positive integers, these tests are
equivalent.

Trusted retranslation of the scratch copy of `solution.py` exited 0 and was
byte-identical to submitted `solution.mpy`; both have SHA-256
`d3d8c79a12490216fd14e7573efbd7abb0031ed6ae1ae9e4bd8a269df68ff113`.

I independently loaded `/reference/canonical.py` and `/candidate/solution.py`
with bytecode writes disabled. The deterministic corpus included both
documented examples, the empty list, threshold values 9/10/11, first- and
last-digit branch combinations, negative values, large integers, every
singleton from -250 through 400, all pairs from a 25-value branch-boundary
set, and 1,000 seeded generated lists. Results:

- domain tested: finite lists of Python integers
- cases: 2,289
- mismatches: 0
- complete-input SHA-256:
  `54f046ad18798f63707bb7a5e3492e320a5ddf4e0f270c7a902eb3a6bc7158c4`

In particular, both Python functions return 0 for `[12]`, 1 for `[15]`, 2 for
`[12, 15, 33]`, and 0 for `[]`.

The K proof formalizes only finite integer lists. The prompt says “numbers,”
but its digit operation and the supplied task context support the integer
reading; non-integer numeric inputs remain outside the formal theorem.

Evidence: [fidelity script](/audit-output/evidence/stage2_fidelity.sh),
[fidelity log](/audit-output/evidence/stage2_fidelity.log),
[differential source](/audit-output/evidence/differential_test.py), and
[complete inputs](/audit-output/evidence/differential-inputs.json).

## 3. Clean proof reconstruction

I used K v7.1.337. The final clean rerun used
`/tmp/audit-work/candidate-clean-rerun`, containing only copied candidate
sources and the integrity-checked supplied semantics. It contained no
candidate definition or cache.

The reconstruction script records the exact commands. Results were:

| Operation | Exit | Required result |
|---|---:|---|
| Trusted translation of reviewer concrete test | 0 | generated `.mpy` |
| LLVM `MPY-KRUN` build | 0 | fresh `runtime-kompiled` |
| Reviewer concrete `krun` | 0 | final `NoExc` |
| Haskell `SPECIALFILTER-VERIFICATION-LOOP` build | 0 | fresh `loop-kompiled` |
| `SPECIALFILTER-LOOP-SPEC` proof | 0 | exact `#Top` line |
| Haskell `SPECIALFILTER-VERIFICATION` build | 0 | fresh `verification-kompiled` |
| `SPECIALFILTER-SPEC` proof | 0 | exact `#Top` line |
| Reconstruction wrapper | 0 | all checks passed |

The reviewer concrete program executes the exact function body on empty,
normal, branch-boundary, and documented-example inputs. The exact submitted
`solution.mpy` also executes under the fresh LLVM definition and installs the
expected closure with `NoExc`; it has no call expression, so that run naturally
does not evaluate a result.

The LLVM build emitted non-exhaustiveness warnings from the supplied baseline,
and proof builds emitted unused-variable warnings from `str.k`; none was a
build or prover failure. An initial reviewer wrapper expected `NoExc` on one
line even though pretty output split the cell over three lines. That initial
wrapper-only mismatch is preserved separately; after correcting the grep, a
second source-clean reconstruction exited 0. No candidate result depends on
that reviewer harness issue.

Evidence: [reconstruction script](/audit-output/evidence/stage3_reconstruction.sh),
[successful complete log](/audit-output/evidence/stage3_reconstruction.log),
[initial harness-mismatch log](/audit-output/evidence/stage3_reconstruction_initial_harness_mismatch.log),
[loop proof](/audit-output/evidence/stage3_loop_proof.log),
[call proof](/audit-output/evidence/stage3_call_proof.log),
[concrete run](/audit-output/evidence/stage3_concrete_krun.log), and
[exact submitted-program run](/audit-output/evidence/stage3_exact_solution_krun_command.log).

Thus the dynamic closure gate passes only in the literal sense: both claims
close under the candidate-extended theory. Soundness and adequacy do not.

## 4. Adequacy and real-program pinning

### Plain-language meaning of the claims

`specialfilter-loop-correct` starts at the supplied semantics' internal
`#loop` control term over an arbitrary proof-only integer sequence `NS`. The
local frame has arbitrary original `nums = ALL`, count `C`, old loop target,
and old `digits`. It requires that global lookup does not shadow `str` and that
the builtin binding is `typeV("str")`. On termination it says:

- count becomes `C + specialCount(NS)`;
- `num` becomes the last item of `NS`, or stays unchanged if `NS` is empty;
- `digits` becomes the decimal string of the last element of `NS` greater than
  10, or stays unchanged if there is none.

The loop precondition is satisfiable. For example, choose
`NS = ALL = .IntSeq`, `C = 0`, old `num = 0`, old
`digits = str(.IntSeq)`, an empty global map, and a builtin map containing
`"str" |-> typeV("str")`. A nonempty witness such as `NS = ALL = [15]` is
also satisfiable.

`specialfilter-empty-call-correct` invokes a manually constructed closure whose
body is `#specialFunctionBody`, with the exact argument
`list(intVals(.IntSeq))`. In plain language it proves only: calling that closure
on the empty list returns 0 and restores the stated frame/heap/return state.
Its precondition is satisfiable with the exact empty global/heap/stack cells and
a builtin map containing the required `str` binding.

### Pinning and result constraint

The three syntax macros reproduce the submitted element body, whole function
body, and module term exactly. The loop claim follows the real internal
`For -> #loop -> #iterNext -> #loopStep` control path. A count-increment body
mutation from 1 to 2 builds but makes the original loop obligation fail on the
expected arithmetic residual, so the direct loop proof is body-sensitive.

There are nevertheless two material pinning failures:

1. No claim executes `#specialModule` or the submitted
   `Module(FuncDef(...))` term and then looks up/calls `specialFilter`.
   `#specialModule` is unused. The entry claim instead constructs a closure
   directly.
2. The sole closure-entry claim hard-codes `.IntSeq`, the empty list. No
   nonempty function call is proved. The universal internal loop lemma is not
   composed into a universal function-entry reachability claim.

There is also a result-constraint failure. `specialCount` is numerical only
relative to `hasOddEndDigits`, which depends on the unconstrained symbols
`decimalCodes`, `decimalLength`, and `decimalCodeAt`. The same symbols enter
execution and the postcondition. This is not an independent theorem that the
program computes ordinary decimal end digits.

Concrete substitution illustrates the gap:

- the only admissible entry input, `[]`, has claimed result 0, and both Python
  functions return 0;
- for an internal loop state with `NS = [12, 15, 33]` and `C = 0`, standard
  decimal interpretation gives `specialCount(NS) = 2`, matching both Python
  functions, but that interpretation is not fixed by the K proof;
- for `NS = [12]`, standard behavior gives 0, while Stage 5 demonstrates an
  admitted symbolic interpretation under which the same body proves count 1.

The empty-entry theorem is therefore real but trivial and too narrow; the
universal theorem is internal and not independently tied to the requested
numeric result.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

I mechanically inventoried every declaration and rule in the supplied
`semantics.k`, all its helper K files, and candidate `verification.k`, with
file, module, line, attributes, and compact full text. There are 962 entries:

- supplied fixed semantics: 227 syntax declarations, 695 rules, 5 contexts,
  and 1 configuration (928 entries);
- candidate `verification.k`: 14 syntax declarations and 20 rules
  (34 entries);
- across the full inventory: 155 function declarations, 117 `total`
  declarations, 25 `no-evaluators` opaque symbols, 28 `symbol` declarations,
  29 priority-bearing entries, 3 simplification rules, and no `functional`
  declarations.

Evidence: [inventory generator](/audit-output/evidence/build_rule_inventory.py),
[inventory log](/audit-output/evidence/rule-inventory.log), and
[complete 962-entry inventory](/audit-output/evidence/rule-inventory.md).

The 928 baseline entries are byte-identical to the selected trusted supplied
semantics, so each is classified as fixed semantics rather than a candidate
proof extension. This authority does not claim that all unused baseline rules
are universal CPython semantics; it fixes the language level against which the
candidate proof must be judged.

For the constructs actually used by `solution.mpy`, the mapping is complete:

| Program construct | Fixed declaration/execution path |
|---|---|
| `Module`, `FuncDef`, `Params` | `syntax.k`; `core.k` module loading and statement sequencing; `functions.k` closure installation |
| `Name`, `Int`, `Str` | `core.k` lookup/literals; `str.k` literal coding |
| `Assign`, `AugAssign`, `If`, `For` | `controls.k`, including `For -> #loop` and scope updates |
| `Compare >`, unary `-`, integer `+` | `operators.k` dispatch and `int.k` cases |
| `BoolOp and` | `bool.k` left-to-right short-circuit contexts/rules |
| `Call(Name("str"), ...)` | `call.k` callee/argument order and type dispatch; `builtins.k` integer-string rule |
| `Subscript` at 0 and -1 | `subscript.k` receiver/index order, normalization, length, and projection |
| string membership | `str.k` `applyCmp("in",...)` and `strContains` |
| `Return` and call frame | `functions.k` return, pop, environment restoration |

The configuration contains control, environment, scopes, allocation counters,
heap, call stack, return state, exception, and exit code. The relevant fixed
rules evaluate callees and arguments left to right, preserve the call frame,
write `count`, `num`, and `digits` in the current scope, and implement loop
target binding before the body. The synthetic loop path performs no heap
allocation or output. No used construct is silently unmodeled.

### All 34 proof-local entries

The complete disposition of the candidate additions is:

| Entries | Count | Classification and decision |
|---|---:|---|
| `#specialElementBody`, `#specialFunctionBody`, `#specialModule` syntax and their macro equations | 6 | Exact syntactic aliases; sound. `#specialModule` is unused by claims. |
| `decimalCodes`, `decimalLength`, `decimalCodeAt` declarations | 3 | Program-derived opaque `function,total,symbol,no-evaluators` values; no defining equations or external contract. They influence branches and the final count. Illegitimate as a result-bearing trust boundary. |
| Simplifications from fixed `Int2String`/length/projection to the three decimal symbols | 3 | Result-bearing operational/equational bridges over all `N` (and all `I` for projection). No bridge-free universal connection theorem exists. Collectively unsound for a theorem about fixed execution; false-conclusion witness below. |
| `decimalString` declaration/equation | 2 | A terminating alias, but its claimed decimal meaning is conditional on the unjustified bridge. |
| `hasOddEndDigits` declaration/equation | 2 | Faithfully mirrors the two membership computations only relative to the opaque symbols; it does not establish ordinary decimal meaning. |
| `boolAsInt` declaration and two equations | 3 | Exhaustive, disjoint, and mathematically sound. |
| `specialBit` declaration/equation | 2 | Exhaustive and sound relative to `hasOddEndDigits`; not an independent intent bridge. |
| `intVals` declaration and two iterator rules | 3 | Disjoint base/cons rules, structurally faithful to list iteration, and acceptable as a typed proof representation. |
| `specialCount` declaration and two equations | 3 | Disjoint structural recursion and sound relative to `specialBit`. |
| `finalNum` declaration and two equations | 3 | Disjoint structural recursion matching Python's retained loop target. |
| `finalDigits` declaration and two equations | 3 | Disjoint structural recursion matching the assignment on `N > 10`, conditional on `decimalString`. |
| Priority-40 loop-summary rule | 1 | Exact `<k>` context and guards of the separately proved loop claim; no arbitrary continuation is admitted. It updates the same scope fields and frames other cells. However, its supposed derivation imports the same opaque bridges and uses the same opaque result, so it is not a bridge-free fixed-semantics connection theorem. |

These groups total all 34 candidate entries. The seven ordinary helper
functions other than the three opaque symbols are total by exhaustive
constructor or boolean cases; their recursive cases descend structurally.
Their guards are disjoint or their right-hand sides agree. The two `intVals`
iterator rules are disjoint from each other and from the supplied list rules.
The priority summary overlaps the supplied generic loop step and intentionally
preempts it only in `SPECIALFILTER-VERIFICATION`; it is absent from the module
used to prove the loop claim.

### False-conclusion witness for the decimal bridges

The complete match domain of the three bridges is any occurrence of:

- `strToCodes(Int2String(N))`;
- `isLen(decimalCodes(N))`;
- `intSeqAt(decimalCodes(N), I)`.

They affect the value assigned to `digits`, the two membership branches,
`count`, `specialCount`, `finalDigits`, and the final loop postcondition. Their
only claimed support is that execution and contract use the same symbols,
which is circular.

I supplied a consistent opposite interpretation allowed by those symbols:
every symbolic integer has decimal length 2 and every projected character is
ASCII 49 (`'1'`). In a definition that imports the candidate proof syntax but
not its loop-summary rule, `kprove` directly executes the actual element body
and proves `#Top` for the symbolic claim “every `N > 10` increments count.”
The concrete instance `N = 12` is false: both Python implementations return 0
for `[12]`.

A separate ground attempt did not use the symbolic bridge: the fixed hook
reduced 12 to codes 49,50, the body produced count 0, and the false count-1
claim became stuck. This contrast is the witness: the symbolic bridge admits a
universal conclusion whose ground fixed-semantics instance disagrees.

Evidence:
[opposite interpretation](/audit-output/evidence/oracle-witness.k),
[symbolic false claim](/audit-output/evidence/oracle-witness-spec.k),
[successful `#Top` log](/audit-output/evidence/stage5_oracle_witness_symbolic.log),
[ground attempt sources](/audit-output/evidence/oracle-witness-ground-attempt-spec.k),
and [ground stuck log](/audit-output/evidence/stage5_oracle_witness.log).

The independent body-sensitivity mutation changed `count += 1` to
`count += 2`. Its definition built, and the original loop obligation failed
with the expected residual comparing `C + 2 + specialCount(REST)` against
`C + (specialCount(REST) + 1)`. This supports control/body fidelity but does
not repair the decimal-value oracle.

Evidence: [mutation patch](/audit-output/evidence/body-mutation.patch),
[script](/audit-output/evidence/stage5_body_sensitivity.sh), and
[log](/audit-output/evidence/stage5_body_sensitivity.log).

## 6. Fresh non-vacuity test

The candidate has no `spec-vacuity.k`. I created a new claim with the same
satisfiable empty-call precondition but changed the required return from 0 to
1.

The mutation parsed and built to KORE under `kprove --dry-run` with exit 0.
The actual proof exited 1 with `WarnStuckClaimState`; its reachable residual
contains `0 ~> .K`, while the destination requires 1, followed by the expected
“cannot be rewritten further” prover error. The failure is therefore the
intended unmet result obligation, not a parser, import, timeout, or unrelated
backend failure.

This establishes non-vacuity of the narrow empty-input result constraint. It
does not establish universal entry coverage and does not validate the opaque
loop result.

Evidence: [false spec](/audit-output/evidence/spec-vacuity.k),
[non-vacuity script](/audit-output/evidence/stage6_nonvacuity.sh),
[dry-run log](/audit-output/evidence/stage6_vacuity_dry_run.log), and
[stuck proof log](/audit-output/evidence/stage6_vacuity_proof.log).

## 7. Proven versus assumed accounting

Under the supplied semantics plus all candidate proof extensions, the two
successful reachability proofs establish exactly:

- an arbitrary-length internal loop transforms the named local variables
  according to `specialCount`, `finalNum`, and `finalDigits`; and
- a directly constructed exact-body closure returns 0 on the empty synthetic
  integer list and restores the stated call state.

They do not establish a universal call theorem for `specialFilter`, do not
execute the submitted module in an entry claim, and do not establish that
`specialCount` is the count of standard-decimal odd-ended integers.

The trust ledger is:

| Boundary | Influence and dependents | Assessment |
|---|---|---|
| Byte-identical supplied semantics | All execution and both claims | Accepted fixed semantics by the rendered mode. |
| Trusted `py2mpy.py` | Python-to-`.mpy` program identity | Accepted; byte identity independently checked. |
| K v7.1.337 toolchain/backend | Builds and reachability closure | Normal proof-system trust boundary. |
| `intVals` representation and iterator rules | Universal integer-list loop | Acceptable typed representation; exact base/cons behavior. |
| Three opaque decimal symbols and simplification bridges | String value, indexing, membership branches, `specialBit`, `specialCount`, loop summary | Illegitimate program-derived oracle. No bridge-free connection theorem; false symbolic conclusion witnessed. |
| Priority loop summary | Empty call proof and any future caller proof | Exact context and body-sensitive, but justified only under the illegitimate decimal theory. |
| Python differential corpus | Implementation-to-canonical bridge on 2,289 integer-list cases | Useful finite evidence only; not a universal K theorem. |
| Standard-decimal interpretation of opaque symbols | Human-facing meaning of the loop postcondition | Merely informal/empirical; absent from the formal theory. |
| Termination | All reachability conclusions | Not proved; ordinary partial-correctness limitation. |

Gate assessment:

- Dynamic reconstruction: **PASS** (`#Top` for both claims).
- Real-program soundness/result-bearing abstraction: **FAIL**.
- Intent adequacy/universal entry pinning: **FAIL**.
- Evidence auditability: **limited** by missing generation records, though the
  independent evidence produced here is reproducible.
- Fresh narrow-claim non-vacuity: **PASS**.

The material failures meet the decision boundary for `FAIL / NOT_LEGIT`: the
proof covers only an empty end-to-end call and relies on a result-bearing,
unconstrained oracle chain for its universal internal result.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
