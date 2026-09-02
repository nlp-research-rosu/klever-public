# Independent adversarial audit — 46-fib4

The candidate does **not** contain a partial-correctness proof of the requested
Fib4 function over its intended domain. Fresh reconstruction confirms two
honest, non-vacuous reachability claims: one executes a single loop-body update,
and one checks thirteen concrete calls for `n = 0..12`. Neither is a symbolic
entry claim for arbitrary nonnegative `n`, and the loop claim contains no Fib4
invariant or connection to a returned value. Thus the successful `#Top` results
prove a finite test suite and a local state rotation, not the stated program
contract.

No infrastructure failure occurred. K v7.1.337, both backends, the trusted
translator, and all required trusted mounts were available.

## 1. Input and provenance integrity

I treated all candidate content as untrusted and did not use candidate caches or
compiled definitions. The scratch tree is
`/tmp/audit-work/46-fib4-audit/candidate-src`; it contains candidate source
artifacts plus a fresh copy of the trusted supplied semantics from
`/reference/reference-semantics`.

The rendered mode is `SUPPLIED_SEMANTICS`, and
`/reference/reference-semantics` is present, so there is no mode/mount
contradiction and no `AUDIT_ERROR`.

Integrity results:

- `cmp -s /candidate/prompt.py /reference/prompt.py` exited 0.
- `cmp -s /candidate/py2mpy.py /reference/py2mpy.py` exited 0.
- `diff -r --no-dereference /reference/reference-semantics
  /candidate/reference-semantics` exited 0.
- Recursive type inventories contain the same directories and regular files in
  both semantics trees. Neither tree contains a symlink. There are no missing,
  additional, changed, or mistyped entries in the candidate semantics tree.
- `solution.py`, `solution.mpy`, `spec.k`, `verification.k`, `prove.sh`,
  `prompt.py`, and `py2mpy.py` are regular files.
- The requested untrusted provenance artifacts `run-input.json`,
  `metrics.json`, `codex-last.txt`, and `codex-output.log` are all missing.
  Each `test -f` exited 1. No structured trace or JSONL artifact is present.
  Consequently there were no generation claims to rely on or corroborate.
- Additional candidate artifacts are `concrete-tests.mpy`, `prove.sh`, and
  `__pycache__/`; none was treated as proof evidence or copied into the clean
  build.

Commands, per-check exits, complete inventories, and SHA-256 hashes are in
`evidence/stage1_integrity.sh` and `evidence/stage1_integrity.log`.

Stage 1 result: **integrity failure for missing provenance artifacts**, but the
trusted semantics boundary itself passes and permits the technical audit to
continue.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

`/reference/prompt.py` defines the sequence for nonnegative indices:

- `fib4(0) = 0`
- `fib4(1) = 0`
- `fib4(2) = 2`
- `fib4(3) = 0`
- for `n >= 4`, `fib4(n)` is the sum of the preceding four terms.

The requested implementation must compute the `n`th element efficiently and
without recursion. The examples require 4, 8, and 14 for inputs 5, 6, and 7.
The natural intended domain is integer `n >= 0`; an “empty” input does not
apply to this scalar interface.

The trusted canonical implementation maintains a four-element list and rotates
it. `/candidate/solution.py` uses six scalar locals and a `while` loop. It is
non-recursive, uses constant auxiliary space, and performs `O(n)` additions.
A different algorithm is acceptable.

### Translation fidelity

Using the scratch copy of `/reference/py2mpy.py`, I regenerated
`solution.mpy`. `cmp -s` exited 0, and both submitted and regenerated files have
SHA-256
`3fd876f2abd77d05fc6fd0e4a185520584d51f12b0f3efd4136daba1b561c47d`.
This is byte identity, not merely AST similarity.

### Independent differential test

`evidence/stage2_differential.py` independently imports the scratch copies of
the trusted canonical entry point and generated entry point. It covers:

- all four base branches and the loop boundary `n = 4`;
- documented examples 5, 6, and 7;
- every integer through 24;
- 128 deterministic generated inputs in `[0, 500]`;
- explicit representatives 50, 100, 128, 200, 257, and 500.

There were 136 distinct intended-domain cases and zero mismatches. The full
input list and results are in `evidence/stage2_fidelity.log`; the command exited
0.

For scope transparency, the script also probes excluded negative inputs. The
candidate differs from the canonical Python implementation at `n = -5` and
`n = -2`. Those are not sequence indices under the stated recurrence, so this
is not an intended-domain failure; it prevents overstating the differential as
equality over all Python integers.

Stage 2 result: **pass on the intended domain**, as finite differential
evidence. Testing does not prove universal equivalence.

## 3. Clean proof reconstruction

The pre-build scratch inventory showed only source files and the trusted
semantics copy—no `*-kompiled` directory or candidate cache. I then ran the
following bounded commands from
`/tmp/audit-work/46-fib4-audit/candidate-src`:

```text
timeout 300s kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-kompiled
```

Exit 0. Log: `evidence/stage3_llvm_build.log`.

```text
timeout 300s kompile verification.k --backend haskell --main-module FIB4-VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-kompiled
```

Exit 0. Log: `evidence/stage3_haskell_build.log`.

Every positive target claim was then run independently:

```text
timeout 300s kprove spec.k --definition verification-kompiled --spec-module FIB4-SPEC --claims FIB4-SPEC.loop-step --output pretty
```

Exit 0 and `#Top`. Log: `evidence/stage3_prove_loop_step.log`.

```text
timeout 300s kprove spec.k --definition verification-kompiled --spec-module FIB4-SPEC --claims FIB4-SPEC.operational-cases --output pretty
```

Exit 0 and `#Top`. Log:
`evidence/stage3_prove_operational_cases.log`.

The wrapper with exact commands and combined bounded output is
`evidence/stage3_reconstruction.sh` /
`evidence/stage3_reconstruction.log`.

The builds emitted warnings about unused variables in `strLt` and, on LLVM,
non-exhaustive function matches in fixed-semantics subsystems. They did not
cause a build/proof failure and are assessed in Stage 5.

Stage 3 result: **pass for both submitted claims**. This establishes closure
under the freshly built supplied theory; it does not establish adequacy.

## 4. Adequacy and real-program pinning

### Claim `loop-step`

Precondition, in plain language: the `<k>` cell contains exactly the six
assignments from the loop body. In current scope `L`, locals have arbitrary
integer values
`a=A`, `b=B`, `c=C`, `d=D`, `next_value=E`, and `i=I`. There is no `requires`
clause, no `n`, and no loop guard.

Postcondition: execution consumes that body and updates the locals to
`a=B`, `b=C`, `c=D`, `d=A+B+C+D`,
`next_value=A+B+C+D`, and `i=I+1`.

A satisfying pre-state is `L=0`, `A=0`, `B=0`, `C=2`, `D=0`, `E=0`, `I=4`,
with parent `parent(-1)` and the ordinary default remaining cells. This is the
real first loop-body state for `n >= 4`.

This claim exactly matches the submitted loop-body control flow and is
mathematically correct. It is not a loop invariant: it states no relationship
between `(a,b,c,d,i)` and sequence values, does not require `i <= n`, has no
summary of prior iterations, and constrains no function result.

### Claim `operational-cases`

Precondition, in plain language: the `<k>` cell contains thirteen assertions
that call `fib4` at the ground inputs 0 through 12 and compare each return to a
ground expected value. The current scope is 0; its `fib4` binding is an
explicit closure; builtins are at `-1`; heap and stack are empty; return state
is `noRet`; exception state is `NoExc`; and exit code is 0.

Postcondition: all assertions have been consumed, with the other explicitly
pinned cells still in their original states. Because a false assertion changes
`<exc>` to `AssertionError` and `<exit-code>` to 1, the target constrains every
one of those thirteen returns. It is not a free-variable or tautological
postcondition.

The literal configuration in `spec.k` is itself a satisfiable pre-state.
The module builds, and the equivalent exact function AST was also executed
concretely under the fresh LLVM definition for `n = 0, 3, 4, 12`, terminating
at `.K` with `NoExc` and exit code 0. See
`evidence/stage4_program_cases.py`, `evidence/stage4_pinning.sh`, and
`evidence/stage4_krun.log`.

The claim does not load `solution.mpy` through `#loadAll`; it manually
pre-populates the environment with a closure. This is not a substituted body
in the current artifacts: `evidence/stage4_closure_identity.py` verifies that,
after normalizing explicit `.Stmts` surface-list units, the embedded closure
body equals the submitted MPY `FuncDef` body. The independent test function's
Python AST also equals `solution.py`'s function AST. Nevertheless, this is an
external pinning check rather than a self-pinning K entry theorem.

Concrete substitutions agree with both Python implementations:
`n=0 -> 0`, `n=4 -> 2`, and `n=12 -> 386`; the Stage 2 test covers all thirteen
claimed inputs.

### Material adequacy failure

There is no entry claim of the form “for arbitrary integer `N >= 0`, invoke the
submitted `fib4(N)` and return the recurrence-defined Fib4 value.” The only
result-bearing claim enumerates `N = 0..12`. It says nothing about `n = 13`
(whose correct result is 744) or any larger input. The auxiliary state-rotation
claim cannot extend that finite theorem because it contains neither a
recurrence invariant nor a circularity connecting loop entry/exit to the
postcondition.

A function that agrees with this implementation through 12 and returns an
arbitrary value from 13 onward could satisfy the stated finite observations.
Therefore the proof does not constrain the material behavior required over the
intended domain.

Stage 4 result: **fail**. The current embedded body is exact, but the theorem
does not prove the real program's general contract.

## 5. Rule-by-rule static soundness review

The exhaustive, line-addressable inventory is
`evidence/stage5_rule_inventory.md`, generated by the preserved
`evidence/stage5_inventory.py`. It covers the trusted supplied
`semantics.k`, every helper K file, `verification.k`, and `spec.k`:

- 227 local syntax declarations;
- 695 semantic rules;
- 5 contexts;
- 1 configuration;
- 2 claims;
- 145 `[function]`, 107 `[total]`, 22 `[no-evaluators]`,
  45 priority, and 26 `[owise]` classifiers;
- zero `[functional]` and zero `[simplification]` declarations/rules.

Every inventory row identifies its source line, normalized record, attributes,
used/disjoint status, and review disposition. The detailed used-path mapping is
`evidence/stage5_used_path_review.md`.

### Candidate proof extensions

`verification.k` contains only:

```text
requires "reference-semantics/semantics.k"
module FIB4-VERIFICATION
  imports MPY
endmodule
```

It introduces no local syntax, function, totality/functional assertion, opaque
symbol, priority rule, ordinary rule, simplification, lemma, or operational
bridge. There is therefore no candidate rule that encodes the task answer,
intercepts a call, bypasses the program body, or supplies an unconstrained
result-bearing oracle. Searching the semantics and verification files found no
Fib4 identifiers or expected Fib4 constants; those appear only in the two
claims.

### Used constructs, order, state, and control

Every submitted construct maps to fixed supplied rules:

- `Module` and statement lists: `syntax.k:61`, `core.k:124-127`;
- `FuncDef`/`Params`: `syntax.k:53,57`, `functions.k:14-16`;
- `Call` and left-to-right argument evaluation: `call.k:20-21,69-75`,
  `core.k:185-191`;
- parameter binding and name lookup: `functions.k:63-75`,
  `core.k:130-154`;
- literals, integer `+`, `==`, and `<=`: `core.k:193-196`,
  `operators.k:12,15-17`, `int.k:9,22-27`;
- `If`/truthiness: `controls.k:51-54`, `core.k:199-205`;
- strict RHS assignment: `controls.k:9-18`;
- `While` guard/body/repetition: `controls.k:65-85`;
- return, frame pop, environment restoration, and scope deallocation:
  `functions.k:77-90`;
- result-constraining assertions: `assert.k:6-15`.

Strict/sequence-strict attributes and comparison contexts give the required
evaluation order. The function uses integer locals only, creates no heap
objects, and has no output or exceptional path on the intended inputs.
Call/return rules update and restore `<env>`, `<scopes>`, `<scopeLoc>`,
`<stack>`, and `<ret>`; positive targets also pin `<heap>`, `<exc>`, and
`<exit-code>`. Higher-priority cell-reference, heap-reference, float, list,
method, and builtin paths have constructor/guard-disjoint left sides for this
program. The assertion-failure rule cannot close a positive claim because its
observable exception and exit-code state differs; Stage 6 confirms this
dynamically.

### Opaque and unused facilities

The 22 explicit `[no-evaluators]` symbols are:
`intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `subF`, `divF`, `addF`,
`mulF`, `powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`,
`roundF`, `roundFN`, `sqrtF`, `sortVS`, `sortKeyVS`, and `md5hexCodes`.
Other symbolic total helpers include `floorFI`, `toF`, and `ceilF`. None occurs
in the submitted program, either positive claim, any path condition, or the
mutation, so none influences control, state, return value, or postcondition.

The LLVM compiler reported non-exhaustive `[total]` matches for `mapStrVS`,
`floorFI`, `toF`, `ceilF`, `joinCodes`, and `valSeqAt`. These are fixed
supplied-semantics coverage gaps in unused sorts/subsystems. I found no
concrete or symbolic false-conclusion witness that any can enable on the
intended Fib4 path, so I do **not** label them unsound. The narrower finding is
that the imported language is broader than the subset exercised by this proof.

No inventoried rule is alleged unsound; accordingly there is no missing
false-conclusion witness. The rejection rests on theorem scope, not an
unwitnessed semantics accusation.

Stage 5 result: **no proof-local soundness violation found**. The two claims
mean what their syntax says, but that meaning is inadequate.

## 6. Fresh non-vacuity test

No candidate `spec-vacuity.k` exists. I authored and preserved
`evidence/spec-vacuity.k`, with a distinct module and claim. It executes the
same pinned closure on the satisfying input `n = 7` but mutates the required
return from the actual 14 to 15.

The independent scratch Python witness printed:

```text
{'n': 7, 'canonical': 14, 'candidate': 14, 'mutated_expected': 15}
```

and exited 0.

The mutation build check was:

```text
timeout 120s kprove spec-vacuity.k --definition verification-kompiled --spec-module FIB4-SPEC-VACUITY --claims FIB4-SPEC-VACUITY.operational-cases-false --dry-run
```

It exited 0 and emitted the `kore-exec ... --prove ...` command, so the mutation
parsed and compiled successfully.

The actual mutation proof was:

```text
timeout 300s kprove spec-vacuity.k --definition verification-kompiled --spec-module FIB4-SPEC-VACUITY --claims FIB4-SPEC-VACUITY.operational-cases-false --output pretty
```

It exited 1 with `WarnStuckClaimState`; the residual has `.K` but
`<exc> AssertionError </exc>` and `<exit-code> 1 </exit-code>`, which cannot
unify with the positive destination. This is the expected reachable unmet
result obligation, not a parser error, timeout, or unrelated crash.

Exact commands and outputs are in `evidence/stage6_nonvacuity.sh`,
`evidence/stage6_mutation_dry_run.log`,
`evidence/stage6_mutation_proof.log`, and
`evidence/stage6_nonvacuity.log`.

Stage 6 result: **pass**. The finite operational claim is discriminating and
non-vacuous; non-vacuity does not enlarge its domain.

## 7. Proven versus assumed accounting

### Formally established by successful reachability

1. For arbitrary integer local values, the exact six-statement loop body
   rotates `(a,b,c,d)`, stores their sum in `d` and `next_value`, and increments
   `i` once.
2. Under the exact supplied MPY configuration and embedded closure, calls on
   each ground input 0 through 12 return the constants listed in `spec.k`,
   without an assertion exception and with the explicitly pinned state
   restored.

That is the entire successful theorem. It does not establish a result for a
symbolic input, a Fib4 loop invariant, the four-term recurrence for all
iterations, or partial correctness for every `n >= 0`.

### Trust boundary and assumptions

- **Supplied MPY semantics:** the complete
  `/reference/reference-semantics` tree is the selected fixed language model
  and was copied fresh. All claims depend on its configuration and operational
  rules. This is an acceptable problem-supplied trust boundary, with the unused
  totality warnings disclosed above.
- **K implementation and builtins:** K v7.1.337, the Haskell prover, LLVM
  executor, and imported `INT`, `BOOL`, `STRING`, `MAP`, `LIST`, and `K-EQUAL`
  theories are low-level trusted primitives. Integer addition/comparison,
  maps, and call-stack rewriting depend on them.
- **Opaque supplied symbols:** all explicit opaque symbols are listed in
  Stage 5. They are imported but have no dependency path to either Fib4 claim;
  the proof is not using their interpretation.
- **Source-to-MPY bridge:** `/reference/py2mpy.py` is a trusted input. Its fresh
  byte-identical regeneration supports that `solution.mpy` is the translation
  of `solution.py`; this bridge is checked by execution, not proved inside K.
- **Spec-body pinning:** the operational claim manually embeds the current MPY
  closure rather than loading the submitted file. The normalized identity
  check supports exact current-body pinning but is reviewer tooling, not a K
  connection theorem.
- **Intent/canonical bridge:** the recurrence interpretation and intended
  `n >= 0` domain come from the trusted prompt and canonical implementation.
  The 136-case differential provides finite empirical support that the
  implementation matches that intent. It is not a universal theorem and
  cannot replace the missing invariant.
- **Efficiency and non-recursion:** these follow by direct source inspection
  (`while`, constant scalar state), not from either reachability claim.
- **Termination:** the requested proof mode is partial correctness. The finite
  ground calls do terminate in K. No universal K termination theorem is
  claimed; informally, for `n >= 4`, `i` starts at 4 and increases to `n+1`.

Candidate prose, prior traces, `PROOF.md`, and compiled evidence played no role;
none of those proof-report artifacts was present. Differential and concrete
tests were used only for the bridges they actually exercise.

### Decision

Fresh reconstruction and non-vacuity show that the candidate has two genuine
but much weaker proofs. The required result is an input-parametric
partial-correctness theorem for the generated Fib4 program. Because no such
claim or recurrence invariant exists, the candidate falls squarely within the
decision rule for a missing/non-constraining target proof. The missing
provenance files are an additional integrity defect, but the material theorem
scope failure independently determines the verdict.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
