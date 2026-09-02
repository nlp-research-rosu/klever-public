# Independent adversarial audit: 76-is-simple-power

This review treats every candidate artifact and every generation record as
untrusted evidence. I rebuilt from copied source in `/tmp/audit-work`, used the
mounted trusted translator, canonical implementation, prompt, and supplied
semantics, and did not use the candidate's compiled archive, bytecode, emitted
`spec.json`, or prior proof output.

## 1. Input and provenance integrity

The launcher record declares:

- `record_layout`: `legacy-selected-stage1`
- condition: `semantics`
- semantics mode: `SUPPLIED_SEMANTICS`
- problem: `76-is-simple-power`

The infrastructure boundary is intact:

- `/audit-input.json` and `/audit-campaign-lock.json` are present, regular
  files, readable, and not symlinks.
- The `audit_campaign` object in `/audit-input.json` is exactly equal to the
  lock object. The independently computed lock SHA-256 is
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  exactly the recorded value.
- Every record required by `legacy-selected-stage1` is present and of the
  correct regular-file/directory type: `/run.json`, `/task.json`,
  `/generation-result.json`, invocation and metrics JSON, `codex-last.txt`,
  `codex-output.log`, `prompt.txt`, and the structured trace. `usage.json` is
  present and was inspected. Historical runtime metrics are not required for
  this layout and were not reconstructed.
- The structured trace has 617 valid JSONL records. Its file SHA-256 is
  `70345e4add2646948fbe7a841aa4125e9ecb8fdaa069defbd39f4a9a5c7e2c5d`,
  matching the invocation/result manifests. The 28,347-line Codex output log
  and all other listed records have the recorded hashes. The trace contains
  intermediate failed/hanging construction attempts and an eventual claimed
  success; none was used as proof evidence.
- The candidate prompt and trusted prompt are byte-identical, SHA-256
  `4d99f80a460939bc03631f3a652d9af5d5a09da2fd8fab20205c9682f766a361`.
  The candidate and trusted translators are byte-identical, SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.
- The trusted supplied-semantics mount exists, as required by the rendered
  mode. Recursive comparison found the candidate and trusted semantics trees
  identical: the same 24 regular files, no additional or missing entries, no
  symlinks, and byte-identical contents for every file.
- All required candidate proof artifacts are present as regular files. A full
  independent per-file hash/type inventory is preserved. Candidate caches
  (`__pycache__`, `kore-exec.tar.gz`, and stale `spec.json`) were ignored.

Evidence:

- [`stage1-generation-inspection.log`](evidence/stage1-generation-inspection.log)
- [`stage1-record-hashes.log`](evidence/stage1-record-hashes.log)
- [`stage1-semantics-integrity.log`](evidence/stage1-semantics-integrity.log)
- [`stage1-candidate-inventory.log`](evidence/stage1-candidate-inventory.log)
- [`inspect_generation.py`](evidence/inspect_generation.py)

There is no infrastructure breach, so a candidate verdict is appropriate.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract and implementations

The trusted prompt says to return true exactly when `n**int = x`; the example
`x = 1` makes exponent zero part of the intended notion. The prompt states no
positivity restriction on `x` or `n`.

The trusted canonical starts at power 1, repeatedly multiplies by `n` while the
power is less than `x`, and compares the final power to `x`, with a special
case for `n == 1`.

The submitted implementation instead:

1. returns true for `x == 1`;
2. returns false for `x < 1`;
3. returns false for every `n <= 1`;
4. for `x > 1, n > 1`, repeatedly divides by `n` while divisible and tests
   whether the residue is 1.

This is a correct alternative algorithm over positive integers. It is not the
unrestricted equation in the prompt.

### Translator identity

I regenerated `solution.mpy` from `solution.py` using the trusted mounted
translator. The regenerated and submitted files are byte-identical, both with
SHA-256
`6ff96ae7a85be104dce4df1ba85354cb8958580c725fce1f81b76f081dfa28fd`.

Evidence: [`stage2-translator-identity.log`](evidence/stage2-translator-identity.log).

### Independent differential testing

The reviewer-authored test imports the trusted canonical and submitted
implementation independently. It covers all six documented examples, scalar
boundaries around `x = 1` and `n = 1`, every submitted branch, both loop exits,
12,000 exhaustive positive pairs, 500 seeded positive pairs, and an
unrestricted integer grid. An “empty” input is not applicable to two scalar
integer arguments.

Results:

- all 6 examples passed;
- 12,506 positive-integer cases had zero candidate/canonical/mathematical
  mismatches;
- on the 1,358-pair unrestricted integer grid, 126 canonical executions timed
  out, 6 terminating canonical executions disagreed with the candidate, and
  the candidate disagreed with the direct integer-power oracle 15 times.

The material witness is:

```text
x = 4, n = -2
(-2)**2 = 4
trusted canonical = True
submitted program = False
```

This witness is entirely within the K proof's own integer argument universe.
It also avoids relying only on an informal oracle because the trusted canonical
terminates and returns true.

The first differential invocation exited 142 because the reviewer script had
not installed its alarm handler. The corrected script and successful rerun are
preserved; that initial reviewer-harness defect is not candidate evidence.

Evidence:

- [`differential_test.py`](evidence/differential_test.py)
- [`stage2-differential-rerun.log`](evidence/stage2-differential-rerun.log)
- [`stage2-differential.log`](evidence/stage2-differential.log)

## 3. Clean proof reconstruction

The live K toolchain is K `v7.1.293`, matching the campaign record. `kup` is
absent, but independently installed `kompile`, `krun`, `kast`, and `kprove`
are available and run successfully. See
[`tool-versions.log`](evidence/tool-versions.log).

I copied only source artifacts to `/tmp/audit-work/repro`. I did not copy or
unpack any candidate-built definition or cache.

### Concrete definition

Fresh command:

```sh
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
```

This exited 0. The fresh concrete harness contains the submitted function plus
all prompt examples and branch/loop boundary assertions. Translation succeeded,
and:

```sh
krun audit_concrete_tests.mpy \
  --definition audit-runtime-kompiled --output none
```

exited 0.

Evidence:

- [`audit_concrete_tests.py`](evidence/audit_concrete_tests.py)
- [`audit_concrete_tests.mpy`](evidence/audit_concrete_tests.mpy)
- [`stage3-concrete-translate.log`](evidence/stage3-concrete-translate.log)
- [`stage3-kompile-llvm.log`](evidence/stage3-kompile-llvm.log)
- [`stage3-krun-concrete.log`](evidence/stage3-krun-concrete.log)

### Proof definition and all positive claims

Fresh command:

```sh
kompile verification.k --backend haskell \
  --main-module SIMPLE-POWER-VERIFICATION \
  --syntax-module SIMPLE-POWER-VERIFICATION \
  --output-definition audit-verification-kompiled
```

exited 0. I then ran every positive claim independently:

| Claim | Result |
|---|---|
| `loop-correct` | `#Top`, exit 0 |
| `function-one` | `#Top`, exit 0 |
| `function-below-one` | `#Top`, exit 0 |
| `function-degenerate-base` | `#Top`, exit 0 |
| `function-positive-domain`, with the separately proved identical `loop-correct` claim selected via `--trusted` | `#Top`, exit 0 |

The last command is a modular proof chain: K treats the loop claim as trusted
in that invocation, while the preceding independent invocation proves that
exact claim from the same source-built definition. No candidate proof cache or
certificate was imported.

Evidence:

- [`stage3-kompile-haskell.log`](evidence/stage3-kompile-haskell.log)
- [`stage3-kprove-loop-correct.log`](evidence/stage3-kprove-loop-correct.log)
- [`stage3-kprove-function-one.log`](evidence/stage3-kprove-function-one.log)
- [`stage3-kprove-function-below-one.log`](evidence/stage3-kprove-function-below-one.log)
- [`stage3-kprove-function-degenerate.log`](evidence/stage3-kprove-function-degenerate.log)
- [`stage3-kprove-function-positive.log`](evidence/stage3-kprove-function-positive.log)

Fresh parsing/emission also found exactly the five current claims; the
candidate's stale emitted `spec.json` was not used. See
[`stage4-fresh-spec-kast.log`](evidence/stage4-fresh-spec-kast.log).

## 4. Adequacy and real-program pinning

### Plain-language claims

- `loop-correct`: for any integer current `X` and `N > 1`, starting at the
  exact submitted while-loop head inside the exact return/end-call
  continuation, any terminating execution returns `positivePowerLoop(X,N)`,
  restores environment 0, pops the sole frame, restores scope location 1, and
  leaves `ret` at `noRet`.
- `function-one`: for every integer `N`, loading the exact module and calling
  it at `(1,N)` returns `simplePower(1,N)`.
- `function-below-one`: for every `X < 1` and every integer `N`, the call
  returns `simplePower(X,N)`.
- `function-degenerate-base`: for `X > 1, N <= 1`, the call returns
  `simplePower(X,N)`.
- `function-positive-domain`: for `X > 1, N > 1`, the call returns
  `simplePower(X,N)`.

The four entry preconditions partition every pair of K integers. They do not
partition the task property correctly; that is the Stage 2/7 adequacy failure,
not a vacuity in the K claims.

### Program identity and control fidelity

The entry claims execute `#loadAll(solutionModule)` and call the loaded
`is_simple_power` binding. I independently expanded both:

1. the trusted-regenerated `solution.mpy`; and
2. candidate macro `solutionModule`.

Their complete Kore terms are byte-identical, with the same SHA-256
`9a7c66079240b8170ed17caf447ba412e9590809af7920a12312e9ac61dfab6a`.
Thus the claims pin the real submitted function binding, parameters, body, and
constructor structure.

The loop lemma also pins the exact condition, assignment body, final return,
`#endcall`, environment, scope, scope allocator, stack frame, and return state.
Its match context is the context reached from the submitted function call:
callee scope 1, caller/module scope 0, sole `frame(.K,0,1)`, and exact trailing
return. It does not admit an arbitrary continuation and does not introduce
return, exception, or frame effects of its own.

Evidence: [`stage4-program-term-identity.log`](evidence/stage4-program-term-identity.log).

### Result constraint and satisfying witnesses

The result is a Boolean term, not a fresh variable, tautology, implication, or
unconstrained oracle. Concrete satisfying witnesses are:

| Claim partition | Witness | Formal result | Submitted | Canonical |
|---|---:|---:|---:|---:|
| one | `(1,4)` | true | true | true |
| below one | `(0,2)` | false | false | false |
| degenerate base | `(2,1)` | false | false | false |
| positive, true branch | `(8,2)` | true | true | true |
| positive, false branch | `(3,2)` | false | false | false |
| loop lemma | `X=8,N=2` | `positivePowerLoop(8,2)=true` | true | true |

Evidence:
[`claim_witnesses.py`](evidence/claim_witnesses.py) and
[`stage4-claim-witnesses.log`](evidence/stage4-claim-witnesses.log).

### Body sensitivity

I made a scratch-only mutation to the program term executed by the claim,
changing the loop assignment macro from `x = x // n` to `x = 1`. This is not
the ineffective experiment of editing an external Python file while keeping
the claimed term fixed.

The mutated definition built successfully. Constructor pinning then failed
with different Kore hashes and a structural diff at the assignment. The
mutated `loop-correct` proof also exited 1 with a meaningful stuck implication,
not a parser error or timeout.

Evidence:

- [`body-mutation-verification.k`](evidence/body-mutation-verification.k)
- [`stage4-body-mutation-kompile.log`](evidence/stage4-body-mutation-kompile.log)
- [`stage4-body-mutation-pinning.log`](evidence/stage4-body-mutation-pinning.log)
- [`stage4-body-mutation-proof.log`](evidence/stage4-body-mutation-proof.log)

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

I read and inventoried the complete supplied semantics, proof-local
`verification.k`, and `spec.k`: 707 rules, 234 syntax sentences, 5 contexts,
1 configuration, and 5 claims. The inventory found 146 sentences carrying
`function`, 107 carrying `total`, 45 priority, 26 `owise`, 35 `concrete`, 25
`symbol`, 10 macro, 2 strict, and 1 seqstrict attributes. There are no local
`functional`, `opaque`, or `simplification` attributes.

The complete sentence text, locations, declarations, guards, attributes, and
counts are preserved in:

- [`stage5-full-numbered-k-sources.log`](evidence/stage5-full-numbered-k-sources.log)
- [`stage5-k-rule-inventory-corrected.log`](evidence/stage5-k-rule-inventory-corrected.log)
- [`k_rule_inventory.py`](evidence/k_rule_inventory.py)

The earlier `stage5-k-rule-inventory.log` used an initial scanner that mistook
the quoted operator `"//"` for a comment. The corrected scanner is the
authoritative inventory.

Module-level accounting of every supplied rule is:

| Module/file | Rules | Syntax | Dependency decision |
|---|---:|---:|---|
| `assert.k` | 3 | 0 | Used only by the reviewer concrete harness, not a target claim; true/false assertion effects agree with that use. |
| `bool.k` | 13 | 0 | Boolean operators are disjoint from the used integer comparison cases; no task shortcut. |
| `builtins.k` | 137 | 38 | No builtin call occurs in the submitted body; rules cannot match the exact program path. |
| `call.k` | 21 | 3 | Proof-critical generic call path: evaluates callee, then arguments left-to-right, selects the looked-up closure, creates a frame, and binds parameters. No builtin/method pattern overlaps this call. |
| `comprehension.k` | 7 | 3 | No comprehension constructor occurs. |
| `concrete.k` | 16 | 5 | Imported only by `MPY-KRUN`, not the proof module; no target-proof dependency. |
| `controls.k` | 34 | 3 | Proof-critical `If`, `While`, assignment, and loop-control rules. Guards and priority cases are disjoint for plain integer locals; loop condition is reevaluated and assignment updates the current scope. |
| `core.k` | 46 | 37 | Proof-critical configuration, module loading, statement sequencing, name lookup, literals, truthiness, argument evaluation, and helpers. Cells and allocation are explicit. No allocation occurs in this body. |
| `dict.k` | 28 | 12 | No dictionary constructor/value occurs. |
| `float.k` | 121 | 34 | No float constructor/value occurs. Concrete-only/opaque float primitives do not occur in a claim or result. |
| `functions.k` | 15 | 4 | Proof-critical function definition, return, and pop. Return discards the remainder of the current function body as Python return should; pop restores the exact caller/frame state. |
| `int.k` | 16 | 1 | Proof-critical integer `==`, `<`, `<=`, `%`, and `//`. `pyMod` and floored division agree with Python for the used nonzero positive divisors. Under the loop's zero-remainder guard, `(X-pyMod(X,N))/N = X/N`, exactly justifying the summary recurrence. |
| `iter.k` | 0 | 1 | Protocol declaration only; absent from the program. |
| `list.k` | 27 | 5 | No list constructor/value occurs. |
| `methods.k` | 75 | 27 | No method call occurs. |
| `operators.k` | 10 | 0 | Proof-critical left/right comparison contexts and integer operator dispatch. Reference-dereference priority rules cannot match plain integer operands. |
| `range.k` | 6 | 2 | No range occurs. |
| `set.k` | 12 | 6 | No set occurs. |
| `sort.k` | 19 | 6 | No sorting occurs; proof-side opaque sort symbols are absent from all terms. |
| `str.k` | 28 | 5 | No Python string value/operator occurs. K string tokens used as names are handled by builtin String/Map operations, not these Python-string rules. |
| `subscript.k` | 40 | 15 | No subscript/slice occurs. |
| `syntax.k` | 0 | 16 | Declares the exact AST constructors. Strictness gives RHS-before-assignment, condition-before-branch/return, and seqstrict left-before-right integer operands. |
| `tuple.k` | 21 | 4 | No tuple value/unpacking occurs. |

`semantics.k` itself contains two assembly modules, 23 requires, and 23
imports, but no rules. The proof imports `MPY`, while concrete execution imports
`MPY-KRUN`.

Unused modules remain part of the supplied fixed-semantics trust boundary, but
their LHS constructors and sorted helper functions cannot arise from the
mechanically pinned submitted body. No unused rule overlaps the plain
integer/control terms above. Therefore they do not contribute to claim closure.

### Proof-local extension inventory

`verification.k` adds exactly 12 rules and 7 syntax declarations:

| Extension | Class and assessment |
|---|---|
| `simplePower(Int,Int)` plus four guarded equations | Result-bearing definitional summary, not an operational bridge. The guards `X=1`, `X<1`, `X>1∧N<=1`, and `X>1∧N>1` are disjoint and cover K integers. It exactly summarizes the submitted branches. It is not an adequate definition of the unrestricted prompt property; witness `(4,-2)` is discussed below. |
| `positivePowerLoop(Int,Int)` plus two equations | Result-bearing definitional summary. `pyMod=0` and `pyMod!=0` are disjoint/exhaustive where `N` is nonzero. On the proved positive domain, the recursive argument is a smaller positive integer; the recurrence exactly matches the submitted division. It does not replace a program redex. |
| `powerCondition`, `powerLoopBody`, `powerResult`, `powerLoop`, `powerBody`, `solutionModule` | Six compile-time macros and their expansion rules. They add no runtime behavior. Mechanical Kore comparison proves the final module macro is the translator output. |
| `loop-correct` | Derived reachability lemma over an exact fixed-semantics loop-head and exact continuation. It was independently proved before being selected as trusted in the modular entry proof. |
| Four entry claims | Target the actual loaded binding/body and constrain the returned Boolean summary. |

There are no candidate priority rules, semantic shortcuts, simplification
rules, opaque symbols, task-specific call interceptions, or rules rewriting an
actual program term directly to an oracle. The same symbol is not circularly
inserted into both an operational bridge and the postcondition because no such
bridge exists.

### Configuration, overlaps, and warnings

The target path explicitly accounts for `<k>`, `<env>`, `<scopes>`,
`<scopeLoc>`, `<stack>`, and `<ret>`. Heap, heap allocator, exception, and exit
cells are completed/framed by the fixed configuration and are not affected by
the submitted scalar program. The final scopes map is existential because the
claim is about the returned value; fixed execution still determines the map,
and no rule can fabricate the Boolean through that existential.

The LLVM build reported non-exhaustive `total` coverage for six supplied,
unused helpers: `mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, and
`valSeqAt`. Concrete symbolic counterterms involving internal `cellsMark`
values exist for those broad declarations, but none can arise on the submitted
program path and none occurs in a proof claim, summary, guard, or result.
Accordingly, this is a supplied-semantics evidence limitation, not a witnessed
false conclusion enabled on the intended submitted-program states. I do not
label those declarations an operative unsoundness for this theorem.

### Material adequacy witness

The proof-local rule

```k
rule simplePower(X, N) => false
  requires X >Int 1 andBool N <=Int 1
```

truthfully summarizes the submitted implementation, but it is not the task
predicate over the prompt's unrestricted integers. Substitution
`X=4, N=-2` satisfies the entry and equation guards, so the claimed result is
false. Yet `(-2)^2=4`, and the trusted canonical returns true. This is a
summary-to-property/domain failure, not an execution-semantics shortcut.

## 6. Fresh non-vacuity test

I created a fresh distinct spec module whose entry configuration is the real
submitted module/call at `x=1`, but whose destination is deliberately `false`.
`N=4` is a concrete state satisfying the precondition, and the real program
returns true.

The dry run parsed and built the mutation successfully, exit 0:

```sh
kprove spec-vacuity.k --definition audit-verification-kompiled \
  --spec-module SIMPLE-POWER-SPEC-VACUITY \
  --claims SIMPLE-POWER-SPEC-VACUITY.function-one-false \
  --dry-run --output none
```

The actual proof exited 1. Its reachable residual has `<k> true ~> .K </k>`
and does not unify with destination `false`; it reports
`WarnStuckClaimState` and the expected terminal prover error. This is a
meaningful unmet result obligation, not an unreachable mutation, parser
failure, timeout, or unrelated backend crash.

Evidence:

- [`spec-vacuity.k`](evidence/spec-vacuity.k)
- [`stage6-vacuity-spec-build.log`](evidence/stage6-vacuity-spec-build.log)
- [`stage6-vacuity-proof.log`](evidence/stage6-vacuity-proof.log)

The independent body-sensitivity failure in Stage 4 is separate from this
false-postcondition test.

## 7. Proven versus assumed accounting and verdict

### What the reachability proof establishes

Under the supplied K semantics and proof-local equations, the reconstructed
proof establishes partial correctness of the exact submitted `solution.mpy`
over K integer arguments:

- `x == 1` returns true;
- `x < 1` returns false;
- `x > 1, n <= 1` returns false;
- `x > 1, n > 1` repeatedly performs exact Python-style integer division
  while the remainder is zero and returns whether the residue is 1.

It also establishes the exact loop summary used in the last partition and
restores the stated call/control cells. It does not prove termination, although
termination for the guarded integer implementation has a straightforward
informal descending argument.

It does **not** establish the prompt's unrestricted `n**int=x` property. In
particular, it proves the submitted false result at `(4,-2)`.

### Trust ledger

1. **K toolchain and backend.** K `v7.1.293`, Kore execution, generated
   heating/cooling rules, SMT arithmetic, and K's unbounded Int/Bool/Map/List/
   String primitives are trusted. Every positive and negative run is recorded.
2. **Supplied semantics.** The byte-identical trusted supplied semantics is the
   fixed language model. The proof-critical scalar/function/control subset was
   reviewed rule by rule above. It models mathematical unbounded integers,
   appropriate for this scalar Python program.
3. **Translator bridge.** The mounted translator is trusted as the Python-AST
   to MPY constructor bridge. Byte regeneration and the macro-to-Kore identity
   check provide mechanical evidence for the exact submitted source/body.
4. **Modular loop lemma.** The positive entry invocation assumes
   `loop-correct` via `--trusted`; a separate clean invocation proves the exact
   same claim with `#Top`. This is a manually checked modular proof chain, not
   a candidate-supplied certificate.
5. **Proof-local summaries.** `simplePower` and `positivePowerLoop` are fully
   equation-defined on every use and contain no fresh value. The bridge from
   repeated exact division to existence of a power is ordinary mathematical
   induction only on `x>=1,n>=2`; it is false as a bridge to the unrestricted
   prompt.
6. **Opaque/concrete supplied symbols.** The 25 symbol/no-evaluator
   boundaries are `md5hexCodes`; `intFloatDiv`, `divII`, `floatMod`, `floatLt`,
   `absF`, `floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`,
   `gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`,
   `roundFN`, `sqrtF`; and `sortVS`, `sortKeyVS`. None occurs in the submitted
   term, claims, summaries, or residual proof obligations, so no target claim
   depends on an interpretation of one.
7. **Empirical evidence.** Concrete K execution and differential Python tests
   are finite supporting evidence only. They do not substitute for the K proof
   or for a universal summary-to-property theorem. The differential mismatch
   is used to refute adequacy, for which one satisfying counterexample is
   sufficient.

### Gate decisions

- **Gate A — real-program soundness: PASS.** The source-built claims close,
  pin the exact program, constrain its result, use a separately proved exact
  loop lemma, reject a false result, and are body-sensitive.
- **Gate B — intent adequacy: FAIL.** The prompt has no positive-base
  restriction, while both implementation and postcondition force false for
  every `x>1,n<=1`. The satisfying integer witness `(4,-2)` disagrees with the
  equation and trusted canonical. This materially narrows/misstates the
  HumanEval source-contract domain.
- **Gate C — auditability: PASS with declared supplied-semantics limitations.**
  All commands, sources, mutations, exact statuses, and bounded outputs are
  preserved; empirical evidence is not overstated.

In generic Kit terminology this is a sound-but-limited proof of the submitted
positive-base algorithm. The benchmark prompt explicitly requires a material
source-domain narrowing to map to `FAIL / NOT_LEGIT`, not to a legitimate
concern.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
