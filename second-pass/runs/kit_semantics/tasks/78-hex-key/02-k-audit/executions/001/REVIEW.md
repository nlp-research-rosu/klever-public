# Independent adversarial review: 78-hex-key

The candidate contains a legitimate partial-correctness proof of the generated
program. I did not rely on the candidate's compiled definitions, `PROOF.md`,
logs, prior `#Top`, or generation report. I reconstructed the proof from copied
source in `/tmp/audit-work/reconstruction`, reviewed the full supplied semantics
and every proof-local declaration/rule, and created a new false-result mutation.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout: pipeline-v3`,
`semantics_mode: SUPPLIED_SEMANTICS`, and the expected problem/condition
`78-hex-key` / `kit-semantics`. The trusted
`/reference/reference-semantics` tree is present, so the mounts agree with the
rendered mode and there is no infrastructure stop condition.

The independent checker in
[`provenance_check.py`](evidence/provenance_check.py) and its exact command log
[`stage1-provenance.log`](evidence/stage1-provenance.log) established:

- `/audit-campaign-lock.json` is a regular file, its SHA-256 is the value
  recorded in `/audit-input.json`, and its parsed object exactly equals the
  `audit_campaign` block.
- All launcher-declared container mounts exist and are readable. The required
  pipeline-v3 records were inspected:
  `/run.json`, `/task.json`, `/generation-result.json`,
  `invocation.json`, `metrics.json`, `runtime-metrics.json`, `usage.json`,
  `codex-last.txt`, `codex-output.log`, `prompt.txt`, and the structured trace.
  A bounded full-log scan (line/byte counts, first/last records, and all
  success/failure marker matches) is preserved in
  [`stage1-generation-record-scan.log`](evidence/stage1-generation-record-scan.log);
  those markers were treated only as untrusted historical claims.
- Every recorded regular-file hash and every evidence-file hash in
  `generation-result.json` and `invocation.json` matches the mounted file.
  An independently reimplemented manifest-tree digest is
  `79fd048e...239bd86` for `/candidate`, matching both recorded stage-one
  workspace hashes. The analogous trace-tree digest is
  `e17b2148...c613bb02`, matching `usage.json`.
- The one structured trace file has the recorded hash
  `6c4fa283...a61e20`; all 383 lines parse as JSON. Its event counts are one
  `session_meta`, 110 `event_msg`, 270 `response_item`, one `world_state`, and
  one `turn_context`.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to the trusted
  mounts, with hashes `0f302c...ae6e` and `406485...db16`.
- Candidate `reference-semantics/` and the trusted tree have exactly the same
  25 relative entries, entry types, and file bytes. There are no missing,
  additional, mistyped, special, or symlinked entries. Both independently
  produce the recorded manifest tree hash
  `4e06397a...de3789f`.
- All six required candidate proof deliverables are regular, non-symlink files.

The generation prose and trace claim success, but I used them only to check
record presence and provenance. No proof conclusion below depends on those
claims. Stage 1 passes.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract asks `hex_key(num)` to count occurrences of the uppercase
hexadecimal digits `2`, `3`, `5`, `7`, `B`, and `D`; `num` is an empty or valid
uppercase hexadecimal string. The trusted canonical implementation iterates by
index over `num` and increments for membership in the corresponding six-element
tuple.

Candidate `solution.py` initializes `count` to zero, iterates each character,
adds the Boolean result of membership in `"2357BD"`, and returns `count`.
Python's Boolean-to-integer addition makes this extensionally identical on the
contract domain.

I regenerated the constructor program with the trusted translator:

```text
python3 /tmp/audit-work/reconstruction/py2mpy.py \
  /tmp/audit-work/reconstruction/solution.py \
  > /tmp/audit-work/reconstruction/solution.regenerated.mpy
cmp /tmp/audit-work/reconstruction/solution.regenerated.mpy \
  /candidate/solution.mpy
```

Both commands exited 0; the submitted and regenerated files are byte-identical.
See [`stage2-translate.log`](evidence/stage2-translate.log) and
[`stage2-translation-identity.log`](evidence/stage2-translation-identity.log).

The independent differential program
[`differential_test.py`](evidence/differential_test.py) imports the trusted and
generated entry points separately and uses a third, independently written
set-membership oracle. It checked:

- all five documented examples and the empty input;
- all 16 single-character branch cases, covering each of the six true and ten
  false membership outcomes;
- prime-only, non-prime-only, repeated-character, alternating, and long
  boundary patterns;
- every valid uppercase hexadecimal string of lengths zero through four; and
- 1,000 deterministic generated strings with lengths zero through 256.

The run made 70,935 comparisons and found zero mismatches
([`stage2-differential.log`](evidence/stage2-differential.log)). There is no
program/specification divergence. Stage 2 passes.

## 3. Clean proof reconstruction

Only source artifacts were copied into scratch by
[`prepare_scratch.sh`](evidence/prepare_scratch.sh). Candidate-provided
`runtime-kompiled`, `verification-kompiled`, caches, bytecode, and binaries were
not copied or used. The live tools all report K `v7.1.293`
([`stage3-tool-versions.log`](evidence/stage3-tool-versions.log)).

I rebuilt the concrete definition:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-audit-kompiled
```

It exited 0. The warnings concern non-exhaustive helpers for unrelated
float/method/builtin/subscript operations and unused variables in `strLt`;
none is reached by this program. The complete bounded output is in
[`stage3-kompile-llvm.log`](evidence/stage3-kompile-llvm.log).

An auditor-authored eleven-case concrete K program
[`concrete_audit.py`](evidence/concrete_audit.py) was translated with the
trusted translator and executed against that fresh LLVM definition. `krun`
exited 0 with `.K`, `NoExc`, and exit code 0
([`stage3-krun-concrete.log`](evidence/stage3-krun-concrete.log)).

I independently rebuilt the proof definition:

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-audit-kompiled
```

This exited 0
([`stage3-kompile-haskell.log`](evidence/stage3-kompile-haskell.log)).
I then ran every positive target:

```text
kprove spec.k --definition verification-audit-kompiled \
  --spec-module SPEC --claims SPEC.hex-loop
```

This independently proves the loop lemma without `--trusted`; it printed
`#Top` and exited 0
([`stage3-kprove-hex-loop.log`](evidence/stage3-kprove-hex-loop.log)).

```text
kprove spec.k --definition verification-audit-kompiled \
  --spec-module SPEC --claims SPEC.hex-key,SPEC.hex-loop \
  --trusted SPEC.hex-loop
```

This proves the entry claim using the exact already-proved loop claim; it also
printed `#Top` and exited 0
([`stage3-kprove-hex-key.log`](evidence/stage3-kprove-hex-key.log)).
The source and fresh definition hashes used for this composition are preserved
in [`stage7-source-hashes.log`](evidence/stage7-source-hashes.log).

Both required dynamic reconstruction gates therefore pass.

## 4. Adequacy and real-program pinning

### Claims in plain language

`SPEC.hex-loop` starts at the real `#loop` control term with:

- an arbitrary finite remaining `str(CS)` iterator;
- the exact target `Name("digit")`;
- the exact augmented-assignment body testing membership in `"2357BD"`;
- the exact suffix `(Return(Name("count")) .Stmts) ~> #endcall`;
- the real callee environment, local frame, call frame, counters, empty heap,
  return state, exception state, and exit code.

It says loop completion changes `count` from `ACC` to
`ACC +Int hexCount(CS)`, permits `digit` to contain the actual final character,
and preserves the rest of the modeled state and exact continuation. `NUMCS`
need not equal remaining `CS`: the source `num` local is unchanged while `CS`
is the remaining internal iterator. This generalization includes every real
loop state and does not fabricate a result.

`SPEC.hex-key` starts with lookup and invocation of the exact `hex_key` closure
on arbitrary finite `str(CS)`. Its precondition fixes the module binding,
function parameter/body/defining environment, scopes, allocation counters,
empty heap and stack, return/exception state, and exit code. Its destination
result is an integer constrained by the equality
`?RESULT ==Int hexCount(CS)`. This is not a free result, tautology, or one-way
implication.

### Mechanical program pinning

Trusted regeneration already gives byte identity between source translation and
submitted `solution.mpy`. In addition,
[`constructor_compare.py`](evidence/constructor_compare.py) mechanically
extracts the closure body actually executed by `SPEC.hex-key`, parses both it
and the trusted-regenerated module with `kast`, and compares their constructor
trees. Both canonicalized trees hash to
`1aa3c2a...c55292a8` and compare equal. The binding is `hex_key`, the sole
parameter is `num`, and the defining environment is 0
([`stage4-constructor-compare.log`](evidence/stage4-constructor-compare.log)).
Thus the claim pins the real submitted body, not a substituted summary program.

### Satisfiability and concrete substitutions

The entry precondition is realized by environment 0, the exact module closure
at scope 0 with parent `-1`, `builtinsScope` at `-1`, `scopeLoc` 1, empty heap
and stack, `noRet`, `NoExc`, and exit code 0. The concrete witness script
[`ground_witnesses.py`](evidence/ground_witnesses.py) instantiated `CS` with:

```text
""          -> hexCount 0 -> canonical 0 -> candidate 0
"2"         -> hexCount 1 -> canonical 1 -> candidate 1
"A"         -> hexCount 0 -> canonical 0 -> candidate 0
"D"         -> hexCount 1 -> canonical 1 -> candidate 1
"AB"        -> hexCount 1 -> canonical 1 -> candidate 1
"ABED1A33"  -> hexCount 4 -> canonical 4 -> candidate 4
```

All comparisons succeeded
([`stage4-ground-witnesses.log`](evidence/stage4-ground-witnesses.log)).

### Trusted loop reuse

The loop claim's first proof is the bridge-free universal connection theorem
for precisely the context later admitted by `--trusted SPEC.hex-loop`. It has
no continuation wildcard: loop body, remaining `Return` statement,
`#endcall`, environment, scope map shape, stack frame, heap, counters, return,
exception, and exit cells agree. The theorem is universal over the same
`CS`, `ACC`, `GLOBALS`, `NUMCS`, and initial `digit` domain.

The bridge changes only the internal loop term, `count`, and final local
`digit`; it preserves all other cells and leaves the exact return suffix.
Its value feeds the real fixed-semantics `Return`/frame-pop path. Ground K
execution and the fresh mutation in stage 6 confirm the bridge-enabled entry
result agrees with fixed execution at a distinguishing boundary. The helper
claim therefore matches real control flow and has adequate context
containment. Stage 4 passes.

## 5. Rule-by-rule static soundness review

[`k_inventory.py`](evidence/k_inventory.py) generated the exhaustive
[`k-rule-inventory.tsv`](evidence/k-rule-inventory.tsv) from all supplied K
sources, `verification.k`, and `spec.k`. It contains 933 records:

- 228 syntax declarations;
- one configuration;
- five evaluation contexts;
- 697 rules: 459 equational and 238 operational; and
- two reachability claims.

The attribute inventory contains 146 `function`, 108 `total`, 25 `symbol`, 22
`no-evaluators`, 32 `concrete`, 29 priority, 26 `owise`, four macro, one
recursive macro, and the strictness declarations. There are no
`simplification` or `functional` declarations. The candidate's own
`verification.k` contributes only one `[function,total]` symbol and two
equations; it contributes no priority, opaque, concrete, simplification,
ordinary operational, or answer-bypassing rule.

[`review_inventory.py`](evidence/review_inventory.py) assigns an explicit
assessment and rationale to every one of the 933 rows in
[`k-rule-review.tsv`](evidence/k-rule-review.tsv). The complete generation
counts and exact commands are in
[`stage5-inventory-generation.log`](evidence/stage5-inventory-generation.log)
and
[`stage5-rule-review-generation.log`](evidence/stage5-rule-review-generation.log).

### Used-construct mapping

| Program construct | Fixed declarations/rules checked | Result |
|---|---|---|
| `Call(Name("hex_key"), str(CS))` | `call.k` callee/argument routing and exact closure invocation; `core.k` lookup and left-to-right argument fold | Exact binding, argument, new local scope, saved continuation, and call frame |
| `Assign` / integer and string initialization | strict RHS declarations; `controls.k` current-scope write; `core.k` `Int`; `str.k` ASCII literal conversion | Both initializations execute and update only the local map |
| `For(Name("digit"), Name("num"), ...)` | `For` strict iterable declaration; `controls.k` `#loop/#loopStep/#loopLbl`; `str.k` iterator; `tuple.k` name target binding | Iterable evaluated once; each code yields a singleton string in order; target updated before body |
| `Compare(..., "in", Str("2357BD"))` | explicit left-then-right contexts in `operators.k`; string `applyCmp`; `strPrefix/strContains` | Exact singleton substring membership, with disjoint exhaustive recursive cases |
| `count += Bool` | strict RHS; `controls.k` existing-name `AugAssign`; `int.k` `Int + Bool` | Adds exactly 1 for true and 0 for false |
| `Return(Name("count"))` | strict return expression; `functions.k` `Return`, `#pop`, saved continuation and state restoration | Real result returned; local scope removed and caller state restored |

The syntax strictness enforces the material Python order: assignment and
augmented-assignment RHS evaluation, one-time `For` iterable evaluation,
left-to-right comparison operands, return-expression evaluation, callee lookup,
then left-to-right arguments. On the exact plain local frame, the cell/ref
priority rules have false guards or incompatible constructors; no priority
rule preempts the ordinary path. The empty heap remains empty, allocation
counters remain fixed except for the temporary scope counter restored on pop,
and no exception/output state is fabricated.

### Proof-local rules

`hexCount(.IntSeq) => 0` and the `iCons(C,CS)` recurrence are disjoint and
exhaustive over finite `IntSeq`. The recurrence tests the same fixed-semantics
singleton membership as the program, adds 0 or 1, and recurses on the strict
tail. It terminates structurally. `[total]` is justified by those constructor
cases. `hexCount` never appears on the left of an operational configuration
rule, so it is a definitional summary, not an operational bridge or oracle.

### Supplied but unreachable boundaries

The supplied semantics contains 25 opaque/total proof-domain symbols:
`md5hexCodes`; `sortVS`; `sortKeyVS`; and the float symbols
`intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `floorFI`, `toF`,
`ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`,
`decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`, and
`sqrtF`. None of their constructors, call intercepts, results, or dependents is
reachable from `solution.mpy`, `hexCount`, either branch, any state update, or
the postcondition. `MPY-CONCRETE` is imported only by the LLVM runtime module
and is absent from the Haskell proof definition.

Other supplied subset limitations—unsupported exception cases, non-ASCII
literal conversion, unrelated collection/float/import approximations, and
non-exhaustive helpers named by the LLVM compiler—also have incompatible LHS
terms on this exact program. They do not enable a false conclusion about an
intended-domain input. I found no materially unsound used rule and therefore
make no unsupported unsoundness allegation or false-witness claim. Stage 5
passes.

## 6. Fresh non-vacuity test

I did not reuse the candidate's mutation. The fresh auditor artifact
[`fresh-false-mutation.k`](evidence/fresh-false-mutation.k) uses the valid
uppercase hexadecimal input `"BD2"`, for which the real result is 3, and
deliberately requires the exact program to return 2.

First, `kprove --dry-run` parsed and built the mutation successfully with exit
0 ([`stage6-mutation-dry-run.log`](evidence/stage6-mutation-dry-run.log)).
The actual proof command then exited 1 with `WarnStuckClaimState`. Its residual
configuration contains:

```text
<k>
  3 ~> .K
</k>
```

and cannot unify with the false destination 2
([`stage6-mutation-proof.log`](evidence/stage6-mutation-proof.log)). This is the
expected unmet result obligation, not a parser error, missing import, timeout,
or unrelated crash. The theorem is result-constraining and non-vacuous. Stage
6 passes.

## 7. Proven versus assumed accounting

### What the K proof establishes

For every finite K `IntSeq` `CS`, from the exact entry configuration in
`SPEC.hex-key`, if the exact translated `hex_key` invocation terminates under
the supplied `MPY` semantics, its returned integer equals `hexCount(CS)`.
The independently proved loop theorem establishes that each remaining
singleton string contributes exactly its membership Boolean in `"2357BD"`.

For the source contract's empty or valid uppercase hexadecimal strings, that
recurrence is precisely the number of occurrences of `2`, `3`, `5`, `7`, `B`,
and `D`. The formal domain is broader than the source domain; it does not
exclude any valid input, impose a length bound, prove only examples, or use
bounded unrolling. This is partial correctness and does not claim termination.

### Trust ledger

| Boundary | Influence | Assessment and evidence |
|---|---|---|
| Exact supplied `reference-semantics/` | Value, binding, order, control, state, calls/returns, and exceptions | Required `SUPPLIED_SEMANTICS` trust boundary; byte/type-identical to trusted mount. Used rules were statically checked and concretely exercised. Acceptable. |
| Trusted `py2mpy.py` | Python-source to constructor bridge | Required input; candidate copy is identical, regenerated output is byte-identical, and parsed claim/program constructor trees match. Differential evidence additionally supports source behavior. Acceptable. |
| `SPEC.hex-loop` reused via `--trusted` | Accelerates the real loop and determines the accumulator | Not an unproved oracle: the same source claim closed first without `--trusted`, under the same fresh definition, over the complete later match domain. Exact-context composition is acceptable. |
| K `v7.1.293`, Haskell/LLVM backends, SMT and K builtin hooks | Foundational parsing, rewriting, arithmetic, strings, and proof checking | Standard checker/toolchain trust. Versions and fresh source builds are recorded. Acceptable. |
| Mapping ASCII `"2357BD"` to the six prime-valued hexadecimal digits | Human-facing meaning of the proved recurrence | Direct finite mathematical bridge from the trusted prompt and literal codes; also checked on every contract alphabet branch. Acceptable. |
| 70,935 CPython differential cases and eleven concrete K cases | Empirical source/semantics support only | Finite evidence, not used as the universal K proof or as a replacement for a connection theorem. Properly limited. |
| Termination | Whether a result state is reached | Outside partial correctness. Every source-contract input is a finite string and the concrete loop consumes one constructor per step, but the theorem itself does not assert termination. Acceptable for this requested proof class. |

There is no result-bearing external oracle, proof-local opaque symbol,
task-answer rewrite, unmodeled used operation, silently strengthened
precondition, or substituted body. Kit Gates A, B, and C all pass, and the
benchmark decision boundary maps this to a legitimate pass.

VERDICT: PASS
LEGITIMACY: LEGIT
