# Independent adversarial audit: 8-sum-product

## Audit outcome

The candidate contains a legitimate, result-constraining partial-correctness
proof of the submitted program under the supplied MPY semantics. Both target
claims were rebuilt from source and independently closed with exit status 0 and
`#Top`. The program term used by the end-to-end claim is KAST-identical to the
submitted `solution.mpy`; the loop-summary rewrite also has an independently
proved, bridge-free universal connection theorem over its complete match
domain. A fresh false sum-plus-one postcondition parsed successfully and then
failed on the expected false equality.

The outcome is `CONCERNS / LEGIT`, rather than `PASS / LEGIT`, because four
required generation/provenance records and every structured generation trace
are absent. This prevents a complete provenance audit even though the proof
itself was reconstructed and validated independently. There is no
infrastructure breach and no material proof-adequacy gap.

## 1. Input and provenance integrity

The rendered mode is `SUPPLIED_SEMANTICS`. The trusted
`/reference/reference-semantics` tree is present, so the mount agrees with the
rendered mode and this is not an `AUDIT_ERROR`.

The recursive, no-dereference comparison of
`/candidate/reference-semantics` against the trusted tree exited 0. Both trees
contain only regular files/directories and no symlinks. There are no missing,
additional, mistyped, or changed entries in the candidate semantics tree. The
candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
counterparts (`cmp` exit 0). All proof/program source artifacts used below are
regular files.

The following required provenance artifacts are missing:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`

No structured trace or JSONL trace is present. Consequently there were no
untrusted generation claims in those records to inspect. `/candidate` also has
no `PROOF.md`; no candidate prose or prior `#Top` was relied on. The unrelated
`__pycache__`, `concrete-tests.*`, and `prove.sh` entries are outside the
semantics integrity tree and were not reused as proof evidence.

Evidence: `evidence/01_integrity.sh` and
`evidence/01_integrity.log` contain the complete inventories, type checks,
hashes, exact comparisons, commands, and statuses.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract is: for a finite list of integers, return a pair whose
first component is the sum of all elements and whose second component is their
product; the empty-list result is `(0, 1)`. The canonical implementation starts
accumulators at 0 and 1, updates them once per list element, and returns the two
accumulators.

`solution.py` implements the same algorithm. Its extra `number = 0` assignment
only initializes the loop target and has no effect on either returned
accumulator. It is also the correct empty-loop target state.

The trusted translator regenerated
`/tmp/audit-work/reconstruction/regenerated-solution.mpy` from the scratch
`solution.py`. It is byte-identical to the submitted `solution.mpy`; both have
SHA-256
`bae83a86f088ab4d5b32780ca935236951339a37b25ccf9f6cbbcf3ef073dccc`.

The independent differential oracle imports `/reference/canonical.py` by
absolute path, while the candidate entry point is imported from the clean
scratch copy. It covers:

- the two documented examples;
- empty/non-empty loop boundaries, singleton negative/zero/positive values,
  sign changes, repeated negatives, and a zero in the product;
- values around signed 64-bit boundaries and much larger Python integers;
- all 19,608 lists of lengths 0 through 5 over `{-3,-2,-1,0,1,2,3}`;
- 2,000 seeded generated lists of lengths 0 through 30 with values in
  `[-1,000,000,1,000,000]`.

All 21,619 comparisons matched. This finite evidence supports the
implementation-to-contract bridge; it is not used as a substitute for the K
proof.

Evidence: `evidence/differential.py`,
`evidence/02_program_fidelity.sh`, and
`evidence/02_program_fidelity.log`.

## 3. Clean proof reconstruction

Only candidate source files were copied to
`/tmp/audit-work/reconstruction`; candidate compiled definitions,
`__pycache__`, and caches were excluded. A pre-build search recorded no
`*-kompiled` directory. The toolchain was K v7.1.337.

The fresh commands and outcomes were:

1. `kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-kompiled`
   — exit 0.
2. `krun concrete-audit.mpy --definition runtime-kompiled --output pretty`
   — exit 0, final `.K`, `NoExc`, and exit code 0 after empty, normal,
   negative, zero-product, and large-integer assertions.
3. `kompile verification.k --backend haskell --main-module SUM-PRODUCT-VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-kompiled`
   — exit 0.
4. `kprove spec.k --definition verification-kompiled --spec-module SUM-PRODUCT-LOOP-SPEC --output pretty`
   — exit 0 and `#Top`.
5. `kompile verification.k --backend haskell --main-module SUM-PRODUCT-LEMMA --syntax-module MPY-SYNTAX --output-definition verification-lemma-kompiled`
   — exit 0.
6. `kprove spec.k --definition verification-lemma-kompiled --spec-module SUM-PRODUCT-FUNCTION-SPEC --output pretty`
   — exit 0 and `#Top`.

Thus every positive target claim closes independently. The LLVM build emitted
non-exhaustiveness warnings for fixed-semantics functions in unused language
features (`mapStrVS`, several float helpers, `joinCodes`, and out-of-bounds
`valSeqAt`) plus unused-variable warnings in `strLt`. None is reachable in this
program or added by the candidate; the semantics tree is the exact supplied
baseline.

Evidence: `evidence/concrete-audit.py`,
`evidence/03_reconstruct.sh`, and
`evidence/03_reconstruct.log`.

## 4. Adequacy and real-program pinning

### Claims in plain language

`loop-correct` starts at the real `#loop` control point with environment 1,
the actual loop target and body, an arbitrary finite integer sequence, integer
sum/product accumulators, and an integer current-target value. It reaches the
arbitrary trailing continuation after replacing the accumulators with their
left-folded sum/product and replacing `number` with the last iterated integer
(or preserving its old value on an empty sequence). The module scope is
preserved.

`function-correct` starts from the initial MPY configuration, loads the exact
translated module, and calls `sum_product` on an arbitrary finite sequence of
mathematical integers. It returns exactly
`tuple(sum-fold(0, IS), product-fold(1, IS))`, leaves the loaded function
closure in module scope, and pins environment, scope allocation, heap, stack,
return, exception, and exit-code cells. The postcondition is a direct equality
to a constructed two-element tuple, not a free result, tautology, or one-way
implication.

### Program identity and control-flow match

The end-to-end `<k>` cell uses `#loadAll(sumProductModule)` followed by the real
call. To check the transcription mechanically, `kast` parsed both the submitted
`solution.mpy` and the proof macro under `SUM-PRODUCT-VERIFICATION`, expanded
macros, and emitted KORE. `cmp` exited 0; both KORE terms have SHA-256
`f2c97a7dc3701b9a386906e93ea121072f6f9f2d82dc7b8862f65b9a08312039`.
This is stronger than a visual comparison and shows that the claim executes
the submitted translated program term.

The loop helper is the exact two-`AugAssign` body reached from the submitted
`For`. The fixed semantics evaluates the iterable once, binds `number`, runs
the two assignments in order, and returns to the next `#loop`. Function
lookup, one-argument binding, return, frame pop, and the trailing continuation
all remain active; no helper substitutes a different function or skips the
load/call/initialization path.

A concrete satisfying entry state is obtained with `IS = .IntSeq`: the stated
initial configuration is exactly the MPY initial configuration and the result
reduces to `(0,1)`. A satisfying loop state occurs in the real call with
`IS = [2,-3]`, environment 1, the loaded function in module scope,
`numbers = list(intVals([2,-3]))`, `total = 0`, `product = 1`, `number = 0`,
and the real return/end-call suffix as `CONT`. Omitted cells can be filled by
the actual call frame.

Ground substitutions agree with both Python implementations:

- `IS = []` gives `(0,1)`;
- `IS = [1,2,3,4]` gives `(10,24)`;
- `IS = [-2,-3,4]` gives `(-1,24)`.

Evidence: `evidence/sum-product-macro.mpy`,
`evidence/04a_program_term_identity.sh`,
`evidence/04a_program_term_identity.log`, and the named cases in
`evidence/02_program_fidelity.log`.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The source-located inventory enumerates the complete text and disposition of
all 707 rules, 234 syntax declarations, two claims, one configuration, five
contexts, 29 modules, 90 imports, and 25 file requirements. Source attributes
include 148 `function`, 110 `total`, 25 `symbol`, 22 `no-evaluators`, 46
priority, 26 `owise`, 35 `concrete`, six `macro`, one `macro-rec`, two
`strict`, and one `seqstrict`. There are no source `[functional]` or
`[simplification]` declarations; K derives functional axioms from
`[function]`.

The complete per-declaration and numbered-source record is
`evidence/04_static_inventory.log`, generated by
`evidence/k_inventory.py` through
`evidence/04_static_inventory.sh`. Every fixed-semantics rule is marked as an
integrity-identical supplied-baseline rule, with the used execution slice
separately identified. Every proof-local rule has an individual decision.

Per supplied-semantics file:

| File | Rules | Static disposition |
|---|---:|---|
| `semantics.k` | 0 | Assembly/import modules only; exact trusted baseline. |
| `syntax.k` | 0 | AST declarations and evaluation attributes; used declarations match the translator output. |
| `core.k` | 46 | Fixed configuration, sequencing, lookup, literals, and left-to-right argument evaluation; used slice reviewed. |
| `iter.k` | 0 | Iterator protocol declarations only. |
| `range.k` | 6 | Fixed and unused. |
| `operators.k` | 10 | Fixed dispatch layer; the program’s accumulator operations ultimately use the integer cases. |
| `int.k` | 16 | Fixed; `+` and `*` are mathematical K integer addition/multiplication. |
| `bool.k` | 13 | Fixed and unused by the submitted body. |
| `float.k` | 121 | Fixed, unused, and the main source of supplied opaque float primitives. |
| `str.k` | 28 | Fixed; only ASCII docstring construction is used, then discarded. |
| `set.k` | 12 | Fixed and unused. |
| `list.k` | 27 | Fixed; concrete list tests use it, while symbolic `intVals` iteration is proof-local and exhaustive. |
| `tuple.k` | 21 | Fixed; target binding and two-element return construction are used. |
| `subscript.k` | 40 | Fixed and unused. |
| `comprehension.k` | 7 | Fixed and unused. |
| `methods.k` | 75 | Fixed and unused. |
| `controls.k` | 34 | Fixed; assignment, augmented assignment, for-loop protocol, and loop label rules are used. |
| `functions.k` | 15 | Fixed; definition, parameter binding, return, end-call, and pop rules are used. |
| `builtins.k` | 137 | Fixed and unused by the program body. |
| `call.k` | 21 | Fixed; ordinary call routing and `closureVal` dispatch are used. |
| `sort.k` | 19 | Fixed, opaque in proof mode, and unused. |
| `assert.k` | 3 | Fixed; used only by auditor concrete tests, not the theorem. |
| `dict.k` | 28 | Fixed and unused. |
| `concrete.k` | 16 | Fixed concrete-only rules; included only in the LLVM runtime, never in either Haskell proof definition. |

These 695 rules are not candidate proof extensions: they are byte-for-byte the
selected trusted semantics. Unused opaque symbols (float operations, sorting,
and MD5) cannot affect control, state, or the postcondition here.

### Construct-to-semantics map

| Submitted construct | Declaration and operative rules |
|---|---|
| `Module`, statement sequence | `syntax.k`; `core.k` `#loadAll`, statement sequencing, and `.Stmts`. |
| `ImportFrom("typing",...)` | `syntax.k`; the `controls.k` non-math `ImportFrom` no-op. |
| `FuncDef`, `Params` | `syntax.k`; `functions.k` closure creation. |
| `Call(Name(...), argument)` | `syntax.k`; `core.k` lookup and left-to-right `#evalArgs`; `call.k` callee and `closureVal` dispatch. |
| `Expr(Str(...))` | `str.k` string literal equations, then `controls.k` expression discard. |
| `Assign(Name, Int)` | strict RHS evaluation, `core.k` integer literal, and `controls.k` current-scope write. |
| `For(Name, Name, body)` | strict iterable lookup; `controls.k` `For`, `#loop`, iterator result, target binding, and loop-label rules. |
| `AugAssign(Name,"+"/"*",Name)` | strict RHS lookup; `controls.k` in-scope accumulator update; `int.k` exact `+Int`/`*Int`. |
| `Return(TupleExpr(...))` | `tuple.k` left-to-right tuple construction; `functions.k` return and frame pop. |

The fixed configuration and frame rules preserve evaluation order, bindings,
module/local separation, call stack, allocation counters, return state, and
exceptions along this path. The formal input is a finite `IntSeq`; it excludes
non-integer list elements and therefore never needs unmodeled mixed-type
arithmetic.

### The 12 proof-local rules

| Lines in `verification.k` | Rule(s) | Decision |
|---|---|---|
| 9–12 | `sumProductLoopBody` macro | Exact submitted loop body; sound. |
| 15–22 | `sumProductBody` macro | Exact submitted function body; sound. |
| 25–29 | `sumProductModule` macro | Exact submitted module; KAST identity checked. |
| 36 | Empty `intVals` iterator | Exact empty iterator result; sound. |
| 37–38 | Cons `intVals` iterator | Yields the head and recurs on the tail; sound. |
| 42 | Sum-fold base | Returns the accumulator; sound. |
| 43–44 | Sum-fold step | Adds the head and structurally descends; sound. |
| 47 | Product-fold base | Returns the accumulator; sound. |
| 48–49 | Product-fold step | Multiplies by the head and structurally descends; sound. |
| 52 | `lastInt` base | Preserves the prior target on empty input; sound. |
| 53 | `lastInt` step | Replaces the target with each head and structurally descends; sound. |
| 62–88 | Promoted loop rewrite, priority 40 | Operational bridge; sound over its complete match domain by the bridge-free theorem below. |

The empty/cons guards are constructor-disjoint and exhaustive over `IntSeq`.
All three `[total]` folds terminate by structural descent and have no
overlaps. `intVals` is not an unconstrained oracle: its two iterator rules
fully expose its finite integer sequence. There are no proof-local opaque,
`no-evaluators`, `owise`, simplification, or unguarded answer-encoding symbols.

The promoted loop rule reads `<k>`, `<env>`, and scopes 0/1 plus a framed
`REST`; it writes only the three local bindings and replaces the loop region
with the already-quantified `CONT`. It preserves the global scope, framed
scopes, environment, heap, allocation counters, stack, return, exception, and
exit-code cells. Its binding is pinned by `<env> 1`, its body and target are
exact, and it neither returns nor pops a frame.

The candidate’s first target proves the loop statement with the concrete
builtins frame. To eliminate the remaining frame-generality question, the
auditor created the same claim with arbitrary disjoint `REST` scopes and
arbitrary `CONT`, imported only `SUM-PRODUCT-VERIFICATION` (not the proposed
lemma), and ran:

`kprove bridge-universal-spec.k --definition verification-kompiled --spec-module LOOP-BRIDGE-UNIVERSAL-CONNECTION --output pretty`

It exited 0 with `#Top`. This is a bridge-free universal connection theorem
over the rewrite’s full match domain. A boundary sensitivity test at
`<env> 0` proves the fixed semantics updates scope 0; the deliberately false
claim that the bridge updates scope 1 fails and leaves those scope-0 updates in
the residual. Thus priority does not broaden the rule past its environment
guard.

No inventoried candidate rule was found unsound, so there is no claimed
unsound rule requiring a false-conclusion witness. The narrower warnings from
LLVM concern unused, trusted baseline features rather than proof-local rules.

Evidence: `evidence/04_static_inventory.log`,
`evidence/bridge-universal-spec.k`,
`evidence/05a_bridge_connection.sh`,
`evidence/05a_bridge_connection.log`,
`evidence/bridge-fixed-spec.k`,
`evidence/bridge-enabled-spec.k`,
`evidence/05_bridge_witness.sh`, and
`evidence/05_bridge_witness.log`.

## 6. Fresh non-vacuity test

The auditor-authored mutation changes the first returned component from
`intSeqSumFrom(0, IS)` to the demonstrably false
`intSeqSumFrom(0, IS) +Int 1`. The empty sequence satisfies the original entry
precondition and witnesses falsity: the real result is `(0,1)`, while the
mutation demands `(1,1)`.

`kprove ... --dry-run` exited 0, establishing that the mutation parsed and
built against the reconstructed lemma definition. The actual proof command was:

`kprove spec-vacuity.k --definition verification-lemma-kompiled --spec-module SUM-PRODUCT-FRESH-FALSE-SPEC --output pretty`

It exited 1 with `WarnStuckClaimState`. The residual is the expected failed
implication between `intSeqSumFrom(0, IS) +Int 1` and
`intSeqSumFrom(0, IS)`, while the actual returned configuration contains the
unmutated sum and product. This is an exercised, result-bearing obligation, not
a parser error, timeout, missing import, or unrelated crash.

Evidence: `evidence/spec-vacuity.k`,
`evidence/06_nonvacuity.sh`, and
`evidence/06_nonvacuity.log`.

## 7. Proven versus assumed accounting

What is machine established:

- Under the supplied MPY definition, the exact submitted translated module,
  when called on `list(intVals(IS))` for any finite `IntSeq`, returns the tuple
  of the defined sum and product folds, subject to the partial-correctness
  interpretation of the reachability claim.
- The loop body realizes the generalized accumulator equations and target
  update.
- The staged operational rule is connected to fixed execution over its entire
  match domain.
- The result equality is discriminating: the fresh off-by-one result is
  rejected.

Trusted or informal boundaries:

- K v7.1.337, its Haskell/LLVM backends, reachability logic, and K’s built-in
  mathematical integer/map/list/string operations are trusted.
- The entire supplied MPY tree is the selected fixed semantics. It contains
  opaque primitives for unrelated float, sort, and MD5 behavior. None is
  reachable from this program or influences its result.
- The trusted `py2mpy.py` translator is outside the K theorem. Byte-identical
  regeneration and KAST identity establish the concrete bridge used here.
- Interpreting `IntSeq`, `+Int`, `*Int`, and the two left folds as the ordinary
  mathematical sum/product of a finite integer list is an elementary informal
  intent bridge, supported by the defining equations and 21,619 differential
  cases. Testing is finite evidence only.
- The canonical Python implementation is a testing oracle, not an axiom or K
  proof rule.
- Behavior for non-integer elements, malformed calls, resource exhaustion,
  host exceptions outside the modeled subset, and unused Python features is
  outside the formal claim.

Gate A (real-program soundness and non-vacuity) passes. Gate B (intent
adequacy) passes for finite lists of integers. Gate C is limited only by the
missing required generation metadata/logs and absent structured trace; all
reviewer-generated dynamic and static evidence is reproducible. That
auditability limitation determines `CONCERNS`, while the independently
validated proof remains `LEGIT`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
