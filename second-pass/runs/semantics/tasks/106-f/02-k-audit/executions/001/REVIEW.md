# Independent adversarial audit: Problem 106-f

Audit mode: `SUPPLIED_SEMANTICS`  
Scratch reconstruction: `/tmp/audit-work/fresh`  
Evidence: `/audit-output/evidence`

## 1. Input and provenance integrity

The rendered mode and trusted mounts are consistent: `/reference/reference-semantics`
exists, so there is no infrastructure breach and a candidate verdict is appropriate.

The candidate is missing four requested provenance artifacts:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`

No optional structured generation trace is present. Because these files do not
exist, there were no generation claims in them to credit. The complete
candidate tree is in `evidence/candidate-tree.log`; it also contains
`prove.sh` and an ignored `__pycache__/solution.cpython-310.pyc`, but no
candidate-built K definition or K cache. `prove.sh` was read only as an
untrusted claimed procedure.

`evidence/stage1-integrity.log` records the following independent checks:

- Candidate `prompt.py` is byte-identical to `/reference/prompt.py`
  (`cmp` exit 0).
- Candidate `py2mpy.py` is byte-identical to `/reference/py2mpy.py`
  (`cmp` exit 0).
- A recursive, no-dereference comparison of candidate and trusted
  `reference-semantics/` trees has exit 0.
- Every candidate semantics entry has the same regular-file/directory type as
  the trusted tree. There are no missing, additional, changed, mistyped, or
  symlinked entries in that tree.
- All proof source artifacts (`solution.py`, `solution.mpy`, `spec.k`,
  `verification.k`) are regular files, not symlinks.

The integrity script exits 1 solely because the four provenance files are
missing. Source and scratch-copy hashes are preserved in
`evidence/source-hashes.log`. The exact tree/type evidence is in
`evidence/candidate-tree.log` and `evidence/reference-tree.log`.

Stage result: integrity of the trusted prompt, translator, proof sources, and
supplied semantics passes; provenance completeness has a documented concern.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementations

For a nonnegative integer `n`, the prompt requires a list with one entry for
each one-based index `i=1..n`. If `i` is even, entry `i` is
`1*2*...*i`; if `i` is odd, it is `1+2+...+i`. Thus `f(0)=[]` and the
documented example is `f(5)=[1,2,6,24,15]`.

The trusted canonical implementation recomputes the product or sum in a nested
loop for each `i`. The candidate keeps two running accumulators. Immediately
after its updates at iteration `i`, `factorial=i!` and
`total=1+...+i`, so selecting by parity is extensionally the same algorithm.

### Translator identity

The submitted Python was regenerated with the trusted translator:

```text
python3 /reference/py2mpy.py /tmp/audit-work/fresh/solution.py \
  > /tmp/audit-work/fresh/solution.regenerated.mpy
cmp -- solution.regenerated.mpy solution.mpy
```

Both files have SHA-256
`df32d7402b425e332cf43fe54e6dead3182c62b558d3eb51f28c2396fa43feb7`;
the command exits 0. See `evidence/translator-regeneration.log` and the
preserved `evidence/solution.regenerated.mpy`.

### Independent differential execution

`evidence/differential_test.py` independently loads the trusted canonical
entry point and the scratch copy of the generated entry point.
`evidence/differential_inputs.json` records the full input set:

- documented `n=5`;
- empty/boundary cases `-5,-1,0`;
- every early parity/loop boundary `1..8`;
- every integer `9..50`, plus `64,100,200`.

There are 56 unique cases: 54 nonnegative intended-domain cases and two
negative probes outside the symbolic theorem. The run reports
`MISMATCH_COUNT: 0`, exit 0, and result digest
`6cbc18facc69e84a1bc6a771ee7b58cf40218e1871c221680c946054af5bce41`.
Exact results and the command are in `evidence/differential-test.log`.

This is finite evidence, not a universal proof. The independent code
inspection above and the K theorem below carry the universal argument on
`N>=0`.

Stage result: pass.

## 3. Clean proof reconstruction

Only source files were copied into a new `/tmp/audit-work/fresh` tree. The
trusted supplied semantics was copied from `/reference`, while the candidate
program and proof sources came from `/candidate`. No candidate compiled
definition was present or reused.

The independently installed tools are `/usr/bin/kompile`,
`/usr/bin/kprove`, and `/usr/bin/krun`, all K version `v7.1.337`; see
`evidence/tool-versions.log`.

### Concrete definition and execution

The following fresh build exits 0:

```text
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

See `evidence/kompile-runtime.log`. The compiler emits non-exhaustive warnings
for fixed supplied functions on unused value forms; none is candidate-local or
reachable from this integer/list program.

The reviewer harness in `evidence/concrete_harness.py` checks
`n=0,1,2,5,8`. Translation followed by `krun` exits 0 and finishes with
`<exit-code> 0 </exit-code>`; the heap contains the expected lists. See
`evidence/krun-concrete.log`.

### Proof definition

The fresh symbolic build also exits 0:

```text
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

See `evidence/kompile-verification.log`.

### Every positive target

Every labeled positive target was run independently:

| Target | Exact proof selection | Result |
|---|---|---|
| `loop-correct` | `kprove spec.k --definition verification-kompiled --spec-module SPEC --claims loop-correct` | exit 0, `#Top` |
| `f-symbolic` | `kprove spec.k --definition verification-kompiled --spec-module SPEC --claims loop-correct,f-symbolic --trusted loop-correct` | exit 0, `#Top` |
| `f-zero` | `kprove spec.k --definition verification-kompiled --spec-module SPEC --claims f-zero` | exit 0, `#Top` |
| `f-five` | `kprove spec.k --definition verification-kompiled --spec-module SPEC --claims f-five` | exit 0, `#Top` |

The exact commands, bounded output, and statuses are in
`evidence/kprove-loop-correct.log`, `evidence/kprove-f-symbolic.log`,
`evidence/kprove-f-zero.log`, and `evidence/kprove-f-five.log`.

`f-symbolic` uses `loop-correct` as a trusted lemma only after the identical
claim has independently closed. Thus `--trusted loop-correct` is a proof
composition mechanism, not an unproved candidate assumption.

Stage result: pass.

## 4. Adequacy and real-program pinning

### Plain-language claims

`loop-correct` starts at the literal `#while` in the submitted function. Its
frame has `n=N`, `i=I`, factorial accumulator `F`, triangular accumulator
`T`, and heap object 0 equal to an arbitrary existing `PREFIX`. Its
precondition is `1 <= I <= N+1`. At loop exit it requires `i=N+1` and the
heap list to be `PREFIX` followed by a suffix satisfying
`outputOK(suffix,I,N,F,T)`. Final accumulator values are existential because
the function result does not expose them.

`f-symbolic` starts from an exact `Call(Name("f"),Int(N))` with `N>=0`.
Scope 0 binds `f` to a closure whose parameter and complete body are the
submitted `solution.mpy` body. The initial heap and stack are empty and both
allocation counters are pinned. The post-state returns `ref(0)`, heap object 0
is exactly `list(?OUTPUT)`, and
`outputOK(?OUTPUT,1,N,1,0)` must hold.

`f-zero` executes that same closure at `n=0` and constrains heap object 0 to
the empty sequence. `f-five` executes it at `n=5` and constrains the heap
sequence to exactly `[1,2,6,24,15]`.

### Actual-program identity

The symbolic entry begins after the deterministic module-loader step, with the
function closure prebound. This does not substitute a summary for execution:
the closure contains the complete translated body, and the `<k>` cell invokes
it through the fixed call/frame semantics. The fixed `FuncDef` rule in
`functions.k:14-16` binds exactly this `closureVal(PNS,BODY,L)` when the
submitted top-level `Module(FuncDef(...))` is loaded. The top level contains
only that function definition. The fresh LLVM run independently executes the
full submitted `Module`.

The exact AST-to-rule mapping is in
`evidence/used-construct-mapping.md`. In particular, no `Call` interception,
opaque result, or operational bridge replaces the body, loop, arithmetic,
branch, heap append, or return.

### Result constraint and satisfying states

`outputOK` consumes exactly one `vCons` while `I<=N` and accepts the empty
suffix only when `I>N`. Its even rule requires the emitted value
`F*I`; its odd rule requires `T+I`; both advance to
`I+1,F*I,T+I`. With the entry values `I=1,F=1,T=0`, the pre-iteration
invariant is:

```text
F = (I-1)!
T = 1 + ... + (I-1)
```

Hence each emitted even value is `I!`, each emitted odd value is
`1+...+I`, and the accepted suffix has exactly `N` elements. Actual program
output is a finite constructor sequence built from the empty list, so no
underspecified opaque `ValSeq` can satisfy the postcondition.

`evidence/claim_witnesses.py` supplies concrete satisfying states:

- loop claim: `N=5,I=1,F=1,T=0,PREFIX=[99],MODULE=.Map`;
- symbolic entry: `N=5` and all pinned cells from the claim;
- concrete entries: their pinned `n=0` and `n=5` configurations, both with
  precondition `true`.

The script confirms the loop precondition, `outputOK`, final
`PREFIX++suffix`, and equality of the claimed `n=0` and `n=5` results with
both Python implementations. It exits 0; see
`evidence/claim-witnesses.log`.

As an operational-sensitivity check, `evidence/spec-body-mutant.k` changes the
executed entry body from `total += i` to `total += 2` while retaining the
original proved loop lemma and postcondition. It parses and reaches execution,
then exits 1 with a stuck implication on the wrong emitted prefix. See
`evidence/kprove-body-mutant.log`. This rules out body insensitivity.

Stage result: pass.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/build_rule_inventory.py` scans every declaration in the assembled
`semantics.k`, all supplied helper K files, `verification.k`, and `spec.k`.
`evidence/rule-inventory.log` contains all 940 line-addressable records:

| Category | Count |
|---|---:|
| syntax declarations | 228 |
| ordinary rules | 592 |
| `owise` rules | 26 |
| priority rules | 45 |
| concrete-only rules | 35 |
| simplification rules | 4 |
| contexts | 5 |
| configurations | 1 |
| claims | 4 |

Of these, 928 declarations are the byte-verified trusted supplied semantics,
eight are candidate-local declarations in `verification.k`, and four are the
claims. `evidence/special-declarations.log` separately enumerates all
`total`, opaque/symbol, priority, and simplification declarations and confirms
there is no `functional` declaration.

Every supplied-semantics file was inspected. The file-by-file disposition and
the complete mapping of every construct used by `solution.mpy` are in
`evidence/used-construct-mapping.md`. The used path consists of:

- module/function binding and exact closure calls;
- scopes, parameter binding, stack/frame return, and monotonic heap allocation;
- left-to-right argument and operand evaluation;
- integer literals, `+`, `*`, `%`, `<=`, and `==`;
- assignment, augmentation, conditional, and while control;
- empty-list construction and in-place `append`;
- return of the allocated list reference.

Cells read or changed by those rules match the claims: `<env>`,
`<scopes>`, `<scopeLoc>`, `<heap>`, `<heapLoc>`, `<stack>`, and `<ret>`.
The loop performs no allocation or function-frame transition, so framing the
other cells in `loop-correct` is appropriate. The entry claim pins allocation
and stack behavior and returns the escaping heap reference. The omitted
exception and exit-code cells are inert for this program.

The supplied semantics contains opaque float, sorting, and digest symbols:
`sortVS`, `sortKeyVS`, `intFloatDiv`, `divII`, `floatMod`, `floatLt`,
`absF`, `floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`,
`powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `intToF`,
`truncF`, `roundF`, `roundFN`, `sqrtF`, and `md5hexCodes`. None occurs in
the submitted AST, any reachable value, `outputOK`, or a target
postcondition. They have no dependent claim here.

### Every candidate-local declaration

The candidate adds no priority rule, opaque symbol, ordinary operational rule,
or execution bridge.

1. `outputOK(...)[function,total]` is a transparent definitional
   postcondition. It never rewrites a program configuration.
2. The empty-suffix rule applies only for `I>N` and truthfully says no
   indices remain.
3. The even-step rule requires `I<=N`, even parity, and
   `V=F*I`, then recurs with the correct updated accumulators.
4. The odd-step rule requires `I<=N`, non-even parity, and
   `V=T+I`, with the same accumulator updates.

The base and step domains are disjoint. The parity guards are disjoint and
exhaustive on the reachable integer/divisor-2 domain. Although `[total]`
leaves malformed or nonmatching arguments underspecified, it supplies no
equation asserting `true` for them. The body mutation and symbolic
postcondition mutation both get stuck on such unmet `outputOK` obligations,
so totality is not acting as an unconstrained success oracle.

The remaining four local declarations are simplifications:

1. `(A++B)++C = A++(B++C)` is valid by induction on `A`.
2. `A++[] = A` is valid by induction on `A`.
3. `P++A = P++B` implies `A=B` by induction on finite `P`.
4. `P=P++A` implies `A=[]`; sequence lengths give
   `len(P)=len(P)+len(A)`, hence `len(A)=0`.

Their only material overlap—associativity with right identity—has the same
normal result. The cancellation consequences are compatible with both.
`evidence/check_local_algebra.py` additionally checks 29,791 small instances
of associativity and left cancellation, plus all small right-identity and
fixed-prefix cases, with zero failures. This finite check supports, but does
not replace, the induction arguments.

`outputOK` does encode the intended mathematical result, but only as the
postcondition to be proved. It does not replace, intercept, or fabricate any
program execution. No inventoried candidate-local rule is unsound, so no
false-conclusion witness is applicable.

Stage result: pass.

## 6. Fresh non-vacuity test

The reviewer-created `evidence/spec-vacuity-fresh.k` copies the exact `n=5`
entry execution but changes the result-constraining last heap value from the
true `15` to the false `16`. Its precondition is `true`, and `n=5` is the
explicit satisfying witness.

The dry run:

```text
kprove spec-vacuity-fresh.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY-FRESH \
  --claims f-five-false-last \
  --dry-run
```

exits 0 and emits a valid `kore-exec` command, establishing that the mutation
builds; see `evidence/vacuity-build.log`.

The same command without `--dry-run` exits 1 with
`WarnStuckClaimState`. Its residual shows completed execution with heap
`[1,2,6,24,15]`, which cannot unify with the mutated destination ending in
`16`. This is the expected unmet result obligation, not a parser error,
timeout, missing import, or unrelated crash. See
`evidence/kprove-vacuity-fresh.log`.

As an additional symbolic check,
`evidence/spec-vacuity-symbolic.k` changes the symbolic postcondition from
`outputOK(?OUTPUT,1,N,1,0)` to the false
`outputOK(?OUTPUT,1,N,1,1)`. It also builds with exit 0 and then fails with
exit 1 on the exact implication from the proved original postcondition to the
mutated one. See `evidence/vacuity-symbolic-build.log` and
`evidence/kprove-vacuity-symbolic.log`.

Stage result: pass; the proof is non-vacuous and result-discriminating.

## 7. Proven versus assumed accounting

### What is machine-proved

Relative to the supplied MPY semantics and the proof-local rules audited above,
the reconstructed reachability proof establishes:

> For every K integer `N>=0`, if the exact submitted `f` call terminates, it
> returns the heap reference to a finite list containing one value for every
> `i=1..N`; the value is the running product through `i` when `i` is even and
> the running sum through `i` when `i` is odd.

It also independently proves the exact `n=0` and `n=5` executions. This is a
partial-correctness result; termination is not part of the claimed theorem.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| Trusted supplied MPY semantics | All K claims | Mandated by `SUPPLIED_SEMANTICS`; candidate copy is recursively identical. Used rules were statically mapped to this program. |
| K built-in integer/Boolean/map/list equality, heating/cooling, Haskell backend, and reachability/circularity implementation | All symbolic execution | Standard toolchain trust boundary. Fresh K `v7.1.337` builds and runs are recorded. |
| Trusted translator `/reference/py2mpy.py` | Python-to-MPY identity | Mandated trusted input; byte reproduction eliminates a candidate translator substitution. |
| `loop-correct` used under `--trusted` in the entry run | `f-symbolic` only | Acceptable derived lemma: the exact claim was independently machine-proved to `#Top` first. |
| Transparent mathematical reading of `outputOK` and finite-sequence cancellation | Natural-language conclusion and four simplifications | Ordinary induction arguments are given in Stages 4–5. There is no opaque result or empirical oracle in this bridge. |
| Opaque fixed-semantics float/sort/MD5 symbols listed in Stage 5 | None | Unreachable and result-independent in this proof. |
| Trusted canonical Python implementation and CPython execution | Differential evidence only | Zero mismatches over 56 recorded inputs support program/intent fidelity but do not replace the K proof. |
| Fresh LLVM `krun` smoke harness | Concrete semantics bridge at five cases | Finite supporting evidence only; not used as a universal theorem. |
| Preloaded exact closure in entry claims | Entry-point setup | The fixed module/`FuncDef` rule deterministically creates the same closure; no body or binding is abstracted. |

### Limitations and final decision

The universal formal domain is nonnegative K integers. Non-integers are outside
the prompt/program theorem, and negative integers are outside the symbolic
claim even though both Python implementations agreed on the two negative
probes. Final accumulator locals, termination, and unrelated language
constructs are not claimed.

The proof is sound, result-constraining, non-vacuous, and pins the real
generated function body. I assign `CONCERNS / LEGIT`, rather than `PASS`,
because the candidate omitted all four requested generation/provenance
records; this is an audit-evidence limitation even though independent trusted
comparisons reconstructed the relevant provenance and found no proof defect.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
