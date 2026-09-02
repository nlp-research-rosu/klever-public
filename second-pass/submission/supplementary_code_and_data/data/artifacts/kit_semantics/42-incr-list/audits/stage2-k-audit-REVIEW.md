# Independent adversarial review: 42-incr-list

## Executive conclusion

The candidate contains a legitimate, result-constraining partial-correctness
proof of the submitted program. I rebuilt both K definitions from source,
reran the positive claims, mechanically compared the submitted translated
program with the constructor term executed by the entry claim, reviewed every
local proof extension and the complete supplied-semantics rule inventory, and
rejected fresh false-result and body mutations.

The formal entry domain is every finite K `ValSeq` whose elements are `Int`,
`Bool`, or `Float`. It is symbolic and unbounded in list length and integer
magnitude; it is not a finite-example or bounded-unrolling theorem. This covers
the material numerical-list domain of the HumanEval prompt. Nonnumeric values,
custom CPython objects, and exception behavior are outside the theorem.

No candidate-local rule replaces program execution, returns an oracle value,
uses a priority shortcut, or encodes the desired answer operationally.

## 1. Input and provenance integrity

The launcher record declares `record_layout: pipeline-v3`,
`semantics_mode: SUPPLIED_SEMANTICS`, and problem `42-incr-list`.
`/reference/reference-semantics` is present, as required for that mode.

I read `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
`/task.json`, `/generation-result.json`, every required record under
`/generation-evidence`, and all 303 JSONL records in the structured trace. The
generation records were treated only as untrusted historical claims.

Integrity results:

- The campaign lock is byte-hashed as
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  exactly the hash recorded in `/audit-input.json`, and its parsed object
  exactly equals the launcher's `audit_campaign` block.
- All required pipeline-v3 records exist, are readable, and are regular files
  or directories rather than symlinks. Recorded file hashes for the run/task
  manifests, stage result/invocation, prompt, metrics, runtime metrics, usage,
  final response, output log, canonical, prompt, and translator match.
- The sole trace JSONL file hashes as
  `89f1fddb9021b08ec893fa5b5006e1af2f9f1af2b6f51d2d3001b40cffbece2a`,
  matching `/generation-result.json`; every line parses as JSON.
- `/candidate/prompt.py` and `/candidate/py2mpy.py` are byte-identical to the
  trusted mounts.
- Recursive type/path/content comparison of candidate and trusted
  `reference-semantics/` trees found the same 25 entries, no additional or
  missing paths, no changed bytes, and no symlinks.
- Required candidate proof sources `solution.py`, `solution.mpy`,
  `verification.k`, and `spec.k` are present. Candidate-built `*-kompiled`
  directories and caches were not used.

The independent checker and full bounded output are
[stage1_integrity.py](evidence/stage1_integrity.py) and
[stage1_integrity.log](evidence/stage1_integrity.log). There is no
infrastructure breach.

## 2. Program fidelity and canonical comparison

The trusted prompt's contract is: `incr_list(l)` returns a list in which each
element of `l` is incremented by one. The trusted canonical implementation is
the comprehension `[(e + 1) for e in l]`.

The candidate implements the same result by allocating a fresh `result`,
iterating once over `l`, appending `x + 1`, and returning `result`. It does not
mutate or alias the input. The initialization `x = 0` is semantically
irrelevant to the returned list.

I translated the scratch copy with the trusted translator:

```text
python3 py2mpy.py solution.py > regenerated-solution.mpy
```

The regenerated and submitted files are byte-identical and both hash as
`65cc282e256d28de035166d1cfbf776c6a63ed7749110a0027ee5ccafbd2c1fd`.

The independent differential test imports the trusted canonical and candidate
entry points separately. It checks the two documented examples, eight
empty/one-element/boundary cases, all 3,906 integer lists of length 0 through 5
over `[-2,2]`, 1,000 seeded generated integer lists of lengths through 64 with
large-magnitude values, three mixed `Bool`/`Float`/`Int` cases, input
preservation, fresh-result identity, and three invalid-element exception-parity
cases. All 4,919 value cases had zero mismatches; the invalid cases agreed on
`TypeError`.

Artifacts:

- [stage2_differential.py](evidence/stage2_differential.py)
- [stage2_fidelity.sh](evidence/stage2_fidelity.sh)
- [stage2_fidelity.log](evidence/stage2_fidelity.log)

## 3. Clean proof reconstruction

All source required for execution was copied to
`/tmp/audit-work/42-incr-list-audit`. No candidate-provided compiled definition
or cache was copied or referenced.

The available toolchain is K v7.1.293. In the final clean reconstruction,
LLVM and Haskell definitions were created under the previously unused
`fresh-build-003` scratch directory:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled

kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
```

Both builds exited 0. Reviewer-authored concrete execution exercised the empty
list, singleton and negative boundaries, both prompt examples, booleans, and
floats. `krun` exited 0 with `.K`, `NoExc`, and exit code 0.

The loop claim was run directly:

```text
kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC --claims SPEC.loop-inv
```

It printed `#Top` and exited 0. The full spec run, which keeps the loop
circularity available while proving the entry claim, also printed `#Top` and
exited 0:

```text
kprove spec.k --definition audit-verification-kompiled --spec-module SPEC
```

Evidence:

- [stage3_rebuild.sh](evidence/stage3_rebuild.sh)
- [stage3_rebuild.log](evidence/stage3_rebuild.log)
- [stage3_llvm_kompile.log](evidence/stage3_llvm_kompile.log)
- [stage3_concrete_krun.log](evidence/stage3_concrete_krun.log)
- [stage3_haskell_kompile.log](evidence/stage3_haskell_kompile.log)
- [stage3_loop_kprove.log](evidence/stage3_loop_kprove.log)
- [stage3_all_claims_kprove.log](evidence/stage3_all_claims_kprove.log)

The compiler warnings concern unused variables or non-exhaustive functions in
unrelated supplied-semantics modules; the target proof itself closes. Two
earlier reviewer wrapper attempts rejected already-successful concrete runs
because my exit-cell grep first assumed one-line formatting and was then
over-escaped. Those attempts are preserved as
`stage3_reviewer_harness_attempt{1,2}.log`; the final reconstruction uses a
new directory and succeeds independently.

## 4. Adequacy and real-program pinning

### Claim meanings

`SPEC.loop-inv` starts at the real loop head with:

- remaining iterable `list(REM)`;
- the exact translated target `Name("x")`;
- the exact body `result.append(x + 1)`;
- the current result heap object containing `list(ACC)`; and
- normal return/exception/exit cells.

Its precondition is `allNumeric(REM)`. It removes the completed loop and
changes that heap object to `list(incrAcc(ACC, REM))`, preserving framed
scopes, other heap entries, heap allocation state, call stack, exception
state, and the surrounding continuation. The final value of local `x` is
existentially unconstrained, which is harmless because it is not observable
after the function frame is popped; the result heap is constrained exactly.

`SPEC.incr-list` starts from the complete initial configuration with input
object `0 |-> list(INPUT)`, heap allocator 1, module scope 0, and an empty call
stack. It executes `#loadAll` on the function definition and then calls the
loaded binding with `ref(0)`. Its precondition is
`allNumeric(INPUT)`, meaning every element is a K `Int`, `Bool`, or `Float`.

The postcondition requires:

- returned value `ref(1)`;
- the loaded module binding to the exact closure body;
- input heap object 0 unchanged;
- a distinct fresh object 1 containing
  `list(incrAcc(.ValSeq, INPUT))`;
- heap allocator advanced from 1 to 2;
- restored module environment/scope allocator and empty stack; and
- `noRet`, `NoExc`, and exit code 0.

`incrAcc` is deterministic: it consumes one `ValSeq` constructor at a time and
appends the fixed-semantics value `applyBin("+", V, 1)`. It is not a free
result variable or an implication that leaves the heap unconstrained.

### Mechanical program identity

Trusted regeneration first pins `solution.py` to submitted `solution.mpy`.
For the second bridge, I parsed `solution.mpy` with `kast`, compiled the entry
claim with `kprove --dry-run`, extracted the KORE argument of its `#loadAll`,
and compared the two constructor terms. They are byte-identical and hash as:

```text
48bd950b67efb5eccebe1495a35277ee0127fbd24ee77ce8bd0b0e011d785aa2
```

Thus the entry claim loads and calls the actual submitted binding and body;
the comparison is not based on visually similar prose or an external source
file. See [stage4_pinning.sh](evidence/stage4_pinning.sh),
[stage4_extract_kore_loadall.py](evidence/stage4_extract_kore_loadall.py), and
[stage4_pinning.log](evidence/stage4_pinning.log).

### Satisfying states and ground substitutions

The entry precondition is satisfiable, for example with
`INPUT = vCons(0, .ValSeq)` and heap `0 |-> list(INPUT)`.
`allNumeric(INPUT)` reduces to true. Substituting this input into the claimed
summary gives heap object 1 as `list(vCons(1, .ValSeq))`; both Python
implementations return `[1]`.

Independent substitutions for empty, `[-1,0,1]`, `[1,2,3]`, and the longer
documented example likewise match both Python results. Exact K constructor
states are recorded in [stage4_witness.log](evidence/stage4_witness.log) by
[stage4_witness.py](evidence/stage4_witness.py).

The theorem is unbounded over finite algebraic `ValSeq`s. The excluded
nonnumeric cases do not materially narrow the task's numerical-list contract:
the prompt examples are integer lists, and the canonical/candidate primitive
nonnumeric cases tested above raise rather than produce a list. The formal
theorem additionally covers booleans and floats supported by the supplied
semantics.

## 5. Rule-by-rule static soundness review

The exhaustive inventory is
[stage5_rule_inventory.md](evidence/stage5_rule_inventory.md), generated by
[stage5_inventory.py](evidence/stage5_inventory.py). It covers all 26 relevant
K files and contains 941 individually located/classified entries:

- 230 syntax declarations;
- 703 rules, including 238 ordinary cell-transition rules, 430 equations, and
  35 concrete equations;
- five evaluation contexts;
- one configuration; and
- both reachability claims.

It separately records all `function`, `total`, `symbol`, `no-evaluators`,
`concrete`, `owise`, priority, strictness, and macro attributes. There are no
`functional` or simplification declarations. The supplied tree is fixed and
integrity-checked; each unchanged target-unreached rule is identified rather
than silently treated as a candidate extension.

### Used-construct map

| Submitted construct | Fixed declaration/behavior used |
|---|---|
| `Module`, `FuncDef`, `Params` | `syntax.k`; `core.k` load/sequencing; `functions.k` closure binding |
| `Assign(Name, ...)`, `Name` | strict RHS evaluation, current-scope update, and lexical lookup in `core.k`/`controls.k` |
| `ListExpr()` | left-to-right argument fold, `vals2valSeq`, fresh `#alloc(list(...))` in `list.k` |
| `For(Name("x"), Name("l"), body)` | input expression evaluated once; heap ref dereferenced; `#loop`, list iterator, target binding, and exact body continuation |
| `Call(Attribute(...,"append"), ...)` | callee-before-arguments evaluation; bound receiver; in-place append of exactly one value |
| `BinOp("+", x, Int(1))` | left-to-right strict operands, `applyBin`; exact Int/Bool/Float addition cases |
| `Return(Name("result"))` | return value stored, continuation discarded as Python return requires, call frame/env restored, heap result retained |

The entry configuration fixes binding selection: `#loadAll` inserts
`"incr_list"` into module scope 0, lookup finds that binding before builtins,
and the closure call creates and later removes one function scope. Argument
evaluation passes `ref(0)` unchanged. Result-list allocation at heap location 1
is fresh because the pre-heap contains only location 0 and `heapLoc` is 1.
Append mutates location 1 only. The input snapshot is safe here because the
submitted body never mutates its input.

### Proof-local extension inventory

| Extension | Class and complete justification |
|---|---|
| `isNumericVal` | Definitional summary. `Int`, `Bool`, and `Float` constructor cases are sort-disjoint; the `owise` case is their complement. Total and result-independent. |
| `allNumeric` | Definitional summary. Base/cons cases are exhaustive and disjoint; recursion strictly descends on the `ValSeq` tail. |
| `incrAcc` | Definitional result summary, not an operational bridge. Base/cons cases are exhaustive and disjoint; recursion strictly consumes `REM`; the appended value is the fixed semantics' exact `applyBin("+",V,1)`. |
| `loop-inv` | Derived circularity over the exact real `#loop`, target, body, environment binding, result heap, and arbitrary continuation. It introduces no abrupt return or omitted state effect. |

There are no candidate-local operational rewrite rules, priorities,
simplifications, opaque symbols, fresh result oracles, or `[concrete]` rules.
No proof-local equation overlap was found. The duplicate supplied mixed
Float/Int addition equations have the same guards and identical right-hand
sides, so their overlap does not admit different results.

The supplied Float operations are an explicit low-level trust boundary:
symbolic `addF` and `intToF` remain opaque under Haskell, while supplied
`[concrete]` equations evaluate them under LLVM. This affects only the
additional Float part of the formal domain; the theorem threads the exact same
terms produced by fixed program execution and the summary, rather than choosing
their values through a proof-local oracle. Int and Bool increments reduce to
ordinary K arithmetic.

I make no claim that an inventoried rule is unsound, so there is no missing
false-conclusion witness for an unsoundness allegation.

## 6. Fresh non-vacuity and body-sensitivity tests

The reviewer-authored false-result spec keeps the genuine general loop
circularity, executes the original submitted `+1` body on satisfying input
`[0]`, and demands output `[2]`. Its dry run builds successfully with exit 0.
The real proof exits 1 with `WarnStuckClaimState`; the terminal configuration
contains output `vCons(1, .ValSeq)`, demonstrating the exact unmet result
obligation rather than a parser or import failure.

The separate body-sensitivity spec changes the actual `#loadAll` constructor
term from `x + 1` to `x + 2` while retaining intended output `[1]` for input
`[0]`. It also dry-runs successfully, then exits 1 with a terminal output
`vCons(2, .ValSeq)`. This mutation changes the program term the claim executes;
it is not an edit to an unused external source file.

Artifacts:

- [stage6_false_spec.k](evidence/stage6_false_spec.k)
- [stage6_body_mutant_spec.k](evidence/stage6_body_mutant_spec.k)
- [stage6_mutations.sh](evidence/stage6_mutations.sh)
- [stage6_false_dry_run.log](evidence/stage6_false_dry_run.log)
- [stage6_false_kprove.log](evidence/stage6_false_kprove.log)
- [stage6_body_mutant_dry_run.log](evidence/stage6_body_mutant_dry_run.log)
- [stage6_body_mutant_kprove.log](evidence/stage6_body_mutant_kprove.log)
- [stage6_mutations.log](evidence/stage6_mutations.log)

The final wrapper exits 0 only after confirming both expected nonzero proof
statuses and their stuck residuals.

## 7. Proven versus assumed accounting

### Formally established

Relative to the supplied `MPY` proof semantics, for every finite `INPUT` whose
elements are `Int`, `Bool`, or `Float`, execution from the entry claim's exact
initial state is partially correct: on completion it returns the fresh
`ref(1)`, preserves input object 0, stores in object 1 the same-order sequence
obtained by applying fixed-semantics `+ 1` to every input element, restores the
call-frame state, and has no modeled exception or nonzero exit.

The proof establishes this by executing the actual module definition, binding,
function call, allocation, loop, name lookup, addition, append, return, and
frame teardown. Differential testing and prose are not used in place of that
reachability proof.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| Trusted `py2mpy.py` | Source-to-MPY bridge | Acceptable benchmark input. Byte regeneration and constructor-level KORE comparison show exactly which translated program is proved. |
| Supplied `MPY` semantics and K builtins | All operational steps | Acceptable selected semantics boundary. Recursive integrity comparison passed; target-path rules were statically reviewed and concretely exercised. It is intentionally a Python subset, not a claim about every CPython behavior. |
| `addF` and `intToF` | Float elements only | Acceptable named supplied primitives. Symbolic Haskell execution is structural/conditional on their fixed contract; LLVM concrete equations and differential Float cases support, but do not universally prove, the CPython bridge. |
| Other `no-evaluators` symbols: `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `subF`, `divF`, `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `truncF`, `roundF`, `roundFN`, `sqrtF`, `sortVS`, `sortKeyVS`, `md5hexCodes`; concrete-only symbolic helpers `floorFI`, `toF`, `ceilF` | None in this target theorem | Imported fixed-semantics boundary but target-unreached; they cannot supply this proof's result. |
| K v7.1.293 parser, kompilers, Haskell backend, and underlying solver/runtime | Machine-check validity | Standard unavoidable proof-tool trust boundary. Fresh builds and both positive/negative results are recorded. |
| Trusted canonical CPython function | Differential oracle and intent bridge | Finite evidence only. It supports implementation fidelity; it is not substituted for K reachability. |
| Interpretation of the prompt as numerical lists | Gate B | Acceptable. Examples are integer lists, the operation requires numeric `+ 1`, and the theorem includes the full unbounded Int domain plus supported Bool/Float values. Primitive nonnumeric cases produce `TypeError` in both Python implementations and are explicitly excluded. |

Gate A passes: execution is real, result-constraining, state-preserving, and
non-vacuous. Gate B passes: the theorem covers the material unbounded source
domain with no fixed size/value bound. Gate C passes: all commands, source
mutations, finite test scope, logs, and trust boundaries are preserved.

The proof is therefore sound and legitimate for the stated partial-correctness
scope, with no material adequacy gap.

VERDICT: PASS
LEGITIMACY: LEGIT
