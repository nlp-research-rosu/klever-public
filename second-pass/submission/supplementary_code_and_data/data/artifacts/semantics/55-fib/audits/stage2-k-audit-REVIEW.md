# Independent adversarial audit: 55-fib

The candidate contains a legitimate partial-correctness proof for the submitted
program over its intended natural-number input domain. I rebuilt both K
definitions from source, reran the claims independently, mechanically pinned
the claim term to the trusted regeneration of `solution.mpy`, reviewed every
source declaration/rule, and obtained relevant failures from both a body
mutation and a fresh false postcondition.

## 1. Input and provenance integrity

Status: PASS.

`/audit-input.json` declares:

- problem `55-fib`, condition `semantics`;
- `semantics_mode = SUPPLIED_SEMANTICS`;
- `record_layout = legacy-selected-stage1`;
- complete input provenance.

The campaign object in `/audit-input.json` is structurally identical to
`/audit-campaign-lock.json`. The lock's independently computed SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
exactly the recorded value.

I read and checked the required legacy-selected records: `/run.json`,
`/task.json`, `/generation-result.json`, `invocation.json`, `metrics.json`,
`codex-last.txt`, `codex-output.log`, `prompt.txt`, the structured trace, and
the present `usage.json`. `runtime-metrics.json` is absent, but that historical
record is explicitly not required for this layout. The trace contains 580
valid JSON lines and one regular trace file whose SHA-256 matches the
invocation/result manifests. Every invocation output digest and every
launcher-recorded regular-file digest checked by the audit script matches.
Generation reports and prior `#Top` text were treated only as claims.

All launcher `container_paths` exist, are readable, and are not symlinks. The
entire candidate tree contains only regular files/directories. Candidate
`prompt.py` and `py2mpy.py` are byte-identical to the trusted mounts.

The trusted `/reference/reference-semantics` exists, as SUPPLIED_SEMANTICS
requires. An lstat-sensitive recursive comparison found the same 25 entries,
entry types, modes, and contents under `/candidate/reference-semantics`; there
are no missing, additional, mistyped, changed, or symlinked entries. Thus there
is no infrastructure breach and no supplied-semantics integrity failure.

Evidence: `evidence/stage1_integrity.py`,
`evidence/stage1-integrity.log`.

## 2. Program fidelity and candidate-versus-canonical checks

Status: PASS.

The trusted prompt asks `fib(n: int)` to return the nth Fibonacci number and
gives `fib(10)=55`, `fib(1)=1`, and `fib(8)=21`. The trusted canonical defines
`F(0)=0`, `F(1)=1`, and recursively returns `F(n-1)+F(n-2)`.

The candidate uses the standard iterative pair update:

```text
(a,b) = (0,1)
repeat n times: (a,b) = (b,a+b)
return a
```

For natural `n`, after `i` iterations the pair is `(F(i),F(i+1))`, so the
returned value is `F(n)`. `N >= 0` is the intended domain: “nth Fibonacci”
and the canonical base/recursive structure define natural indices; the
canonical has no specified negative-index result. This is not a finite bound:
the formal claim quantifies over every unbounded K integer satisfying
`N >=Int 0`.

Running the trusted translator over the scratch copy and piping its bytes to
`cmp` against submitted `solution.mpy` exited 0. The submitted MPY is therefore
the exact trusted translation of `solution.py`.

The independent differential script imports the two Python entry points from
their trusted/candidate paths and also uses a separately written iterative
oracle. It covers all documented examples, canonical branch boundaries
`0,1,2`, all values `0..20`, deterministic generated values with seed 550055,
and broader values 25 and 30. There were 25 unique inputs and zero mismatches.
There is no collection “empty” input for this unary integer function; `n=0`
is the zero-iteration/boundary case.

Evidence: `evidence/stage2-translation.log`,
`evidence/differential_fib.py`, `evidence/stage2-differential.log`.

## 3. Clean proof reconstruction

Status: PASS.

I copied source artifacts to `/tmp/audit-work/55-fib-audit` and did not reuse
any candidate-built definition or cache. The K toolchain is v7.1.293, matching
the campaign lock.

The exact reconstruction results were:

| Check | Exit/result |
|---|---|
| Fresh LLVM `MPY-KRUN` definition | 0 |
| Concrete assertions at 0, 1, 2, 8, 10, 30 | 0; final `.K`, `NoExc`, exit code 0 |
| Concrete load of actual `solution.mpy` | 0; exact `fib` closure installed |
| Fresh Haskell `FIB-VERIFICATION` definition | 0 |
| Original complete `FIB-SPEC` | 0, `#Top` |
| `fib-loop` selected alone | 0, `#Top` |
| `fib-all-natural` composed with separately proved `fib-loop` | 0, `#Top` |

For the compositional entry run, `fib-loop` was marked trusted only in that
second command after it had independently returned `#Top`; the original
unfiltered spec also returned `#Top` without command-line trust. This separates
lemma proof from entry use without treating the lemma as an unproved
assumption.

A diagnostic selection of only `fib-all-natural` filtered out its declared
dependency and began unbounded symbolic loop unrolling; I interrupted it with
exit 130. It is not counted as either positive or negative proof evidence.

Exact commands, statuses, and bounded output are indexed in
`evidence/COMMANDS.md` and preserved in the `stage3-*.log` files.

## 4. Adequacy and real-program pinning

Status: PASS.

The auxiliary `fib-loop` claim has no extra logical precondition beyond its
typed configuration shape. In plain language, if control is at the exact
remaining `range(I,N,1)` loop with the submitted tuple-assignment body and a
local frame containing `n=N,a=A,b=B,_=OLD_INDEX`, then the loop reaches its
continuation with `a=fibRun(A,B,I,N)`. It leaves `n` and every other scope/cell
unchanged; final `b` and `_` are existential integers because the entry result
does not need them. The arbitrary continuation is safe here because the exact
body contains only evaluation and assignment—no return, exception, break,
continue, allocation, or output.

The entry claim requires an integer `N >= 0` and the exact empty module,
builtins, heap, stack, return, exception, allocation, and exit state. It loads
the exact module, resolves and calls its `fib` binding, and reaches the K
integer `fibSpec(N)`. At the target the callee frame is removed, scope
allocation is restored, the module contains the exact `fibClosure`, and the
heap, stack, return, exception, and exit cells are restored as stated.

`evidence/pinning_check.py` expands the nullary `fibProgram` and `fibBody`
definitions, removes layout only outside string literals, and compares the
constructor term with the submitted MPY. The terms are identical, with
normalized digest
`929ad72804535584d9d15640755b0581ac6b599fb17fe747e69efc8ec1764180`.
The entry `<k>` cell executes `#loadAll(fibProgram)` and then calls the bound
name `fib`; `verification.k` has no operational `<k>` rewrite at all.

Concrete satisfying entry witnesses `N=0,1,2,8,10,30` give formal values
`0,1,1,21,55,832040`, identical to both Python implementations. A satisfying,
reachable loop witness is the callee state after initialization with
`N=3,I=0,A=0,B=1`; its summary is 2.

For body sensitivity, I changed the program term actually executed by
`fibBody` from `Assign(Name("a"),Int(0))` to `Int(1)`, rebuilt successfully,
and reran the original spec. The proof exited 1 with a relevant stuck residual
requiring the false equality:

```text
fibRun(0,1,0,N) = fibRun(1,1,0,N)
```

This rules out a theorem detached from the immutable submitted body.

Evidence: `evidence/stage4-pinning.log`,
`evidence/stage4-ground-witnesses.log`,
`evidence/verification-body-mutation.k`,
`evidence/stage4-body-mutation-build.log`,
`evidence/stage4-body-mutation-proof.log`.

## 5. Rule-by-rule static soundness review

Status: PASS.

`evidence/rule-inventory.tsv`, generated by
`evidence/inventory_k.py`, enumerates every source `configuration`, `syntax`,
`context`, `rule`, and `claim` block in the supplied semantics,
`verification.k`, and `spec.k`, including multiline guards and attributes.
The inventory contains 941 records:

- 701 rules, 232 syntax declarations, 5 contexts, 1 configuration, 2 claims;
- 150 function declarations, 109 total declarations, 45 priority rules,
  26 owise rules, 35 concrete rules, and 22 explicitly no-evaluator opaque
  proof symbols;
- no source simplification rule and no `functional` declaration.

Of the 928 supplied-semantics records, 83 are reached by the exact typed fib
term and were checked against the execution below. The other 845 are
constructor/symbol-disjoint from this program and proof. Each inventory row
records that decision. The baseline is also byte-identical to the
condition-selected trusted semantics; no proof-local rule is hidden there.

The exact source-to-rule map is:

| Program operation | Governing fixed rules and soundness decision |
|---|---|
| Module/statement load | `core.k` `#loadAll` and sequencing execute each real statement in order. |
| Function definition/call | `functions.k` installs the exact closure; `call.k` resolves the value, evaluates the integer argument, allocates a callee frame, and binds `n`. No textual-name call interception exists. |
| Docstring expression | `str.k` converts this concrete ASCII string; `controls.k` discards the resulting expression value. It cannot affect the result. |
| Integer/name/assignment | `core.k` evaluates integer literals and performs lexical lookup; `controls.k` updates the current frame. The exact frame has no `$cells`, so cell-priority alternatives cannot match. |
| `range(n)` | Lookup walks from the local frame through module to the real builtin binding; `builtins.k` creates `rangeObj(0,N,1)`. |
| `for` control | `controls.k` invokes the iterator once per iteration; `range.k` yields exactly while `I<N` for step 1 and advances to `I+1`. Exhaustion resumes the existing continuation. |
| Tuple update | `TupleExpr` evaluates `b` and `a+b` left-to-right before `tuple.k` unpacks and binds `a`, then `b`. This preserves Python simultaneous-assignment behavior. |
| Addition | `operators.k` dispatches two evaluated integer operands to `int.k` integer addition. K integers and Python integers are both unbounded here. |
| Return/pop | `functions.k` evaluates `a`, sets the return state, restores caller control/environment, removes the callee scope, and restores the saved scope location. |

Configuration/cell review found no omitted observable effect: the exact path
does not allocate heap objects, mutate globals other than installing `fib`,
raise exceptions, produce output, or change the exit code. Evaluation order,
binding, loop control, stack/return handling, and cleanup are all reflected in
the entry and loop claims.

The six local rules are all valid:

- `fibBody`, `fibClosure`, and `fibProgram` are exact definitional expansions,
  not operational bridges.
- `fibRun(A,_,I,N)=A` for `I>=N` and
  `fibRun(A,B,I,N)=fibRun(B,A+B,I+1,N)` for `I<N` have disjoint, exhaustive
  integer guards. The recursive measure `N-I` strictly decreases in the second
  case, so `[total]` is justified.
- `fibSpec(N)=fibRun(0,1,0,N)` is a total definition.

There are no local priority, owise, concrete, opaque, or simplification rules.
In particular, there is no rule rewriting the real loop/call to an oracle.
`fibRun` is result-bearing, but it is fully defined and is connected to the
fixed loop execution by the separately proved universal `fib-loop` claim. Its
use is not circular: the proof definition contains no `#loop => fibRun`
rewrite.

The supplied baseline contains proof-opaque symbols for float operations
(`intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `subF`, `divF`,
`addF`, `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `intToF`,
`truncF`, `roundF`, `roundFN`, `sqrtF`), sorting (`sortVS`, `sortKeyVS`), and
MD5 (`md5hexCodes`). The related concrete-only `floorFI`, `toF`, and `ceilF`
symbols are also symbolic boundaries in Haskell proofs. None occurs in the
program term, claim result, path condition, or dependency. Likewise, LLVM
warnings about incomplete cases in unused `mapStrVS`, float helpers,
`joinCodes`, and `valSeqAt` cannot affect this exact proof. I found no
candidate-introduced unsound rule, so no false-conclusion witness is claimed.

## 6. Fresh non-vacuity test

Status: PASS.

I created a new spec whose entry postcondition is
`fibSpec(N) +Int 1`, retaining the real program and independently provable
loop lemma. The mutation is demonstrably false at the satisfying input `N=0`:
the real/formal result is 0, while the mutation demands 1.

`kprove --dry-run` parsed and built the mutated spec successfully with exit 0.
The actual proof then exited 1 with `WarnStuckClaimState`; its implication
residual is exactly:

```text
fibRun(0,1,0,N) +Int 1 = fibRun(0,1,0,N)
```

This is the expected unmet result obligation, not a parser error, timeout,
missing import, or unrelated backend failure.

Evidence: `evidence/spec-vacuity-audit.k`,
`evidence/stage6-vacuity-dry-run.log`,
`evidence/stage6-vacuity-proof.log`.

## 7. Proven-versus-assumed accounting

Status: PASS.

What is formally proved under the supplied semantics is:

> For every K integer `N >= 0`, executing the exact trusted translation of the
> submitted `fib` module and calling `fib(N)` reaches the integer
> `fibRun(0,1,0,N)`, while reaching the stated clean final module/heap/stack/
> return/exception/exit configuration.

By its exhaustive equations, `fibRun(0,1,0,N)` is the standard Fibonacci fold:
the invariant pair after `i` updates is `(F(i),F(i+1))`. Thus the K result is
the nth Fibonacci number. This mathematical interpretation is a direct
inductive consequence of the equations, not an opaque oracle or an empirical
replacement for execution.

Trust/assumption ledger:

| Boundary | Role and judgment |
|---|---|
| K v7.1.293 prover/backend and builtin INT/BOOL/MAP/LIST/STRING theories | Ordinary machine-checking trust boundary; acceptable. |
| Supplied reference semantics | Condition-selected fixed semantics, recursively byte-identical in the candidate. All material fib operations were reviewed; acceptable. |
| Trusted `py2mpy.py` | Translation boundary; exact byte regeneration discharges the source-to-MPY instance used here. |
| Natural-language meaning of “nth Fibonacci” | Standard induction connecting the fully defined fold to the contract; acceptable and domain-aligned. |
| Python differential testing | Finite independent support for implementation/canonical agreement only; not used as a substitute for the K proof. |
| Partial correctness/termination | The claimed result is partial correctness. No behavior is claimed for negative indices or non-integer calls, and no separate general termination theorem is claimed. This matches the typed natural-index contract. |
| Unused supplied opaque primitives | Listed in Stage 5; no value, control, state, exception, or postcondition dependency, so acceptable for this theorem. |

Kit Gate A (real-program soundness), Gate B (intent adequacy), and Gate C
(trust/evidence auditability) all pass. There is no material domain narrowing,
substituted program, non-constraining result, unproved operational bridge, or
candidate-specific unsound semantic rule.

VERDICT: PASS
LEGITIMACY: LEGIT
