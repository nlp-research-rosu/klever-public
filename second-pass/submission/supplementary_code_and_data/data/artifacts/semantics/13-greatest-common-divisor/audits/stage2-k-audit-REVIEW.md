# Independent adversarial audit: 13-greatest-common-divisor

## Executive finding

The candidate's sources rebuild, every submitted positive claim prints `#Top`,
the submitted program term is mechanically pinned to `solution.mpy`, and a
fresh false-result mutation is rejected. Those facts do not make the universal
claim a legitimate proof of the program.

The decisive defect is the symbolic-only rule at
`/candidate/verification.k:51-58`. At the real loop head it preempts the
supplied `#while` semantics, deletes the loop, and writes the desired
`gcdSpec(A, B)` result directly into local `a`. There is no bridge-free
universal execution claim establishing that transformation. The separate
`euclid-step` claim proves only one tuple-assignment step and is not a
dependency of `program-correct`: an independently created spec containing
`program-correct` alone still proves `#Top`.

A body-sensitivity test makes the problem concrete. I changed the function body
actually embedded in the claim from the Euclidean assignment to `b = 0` and
changed the bridge's shared `GcdLoopBody` macro accordingly. Mechanical KORE
comparison confirms that the mutated claim executes that mutated function.
Under the supplied semantics the altered function returns `6` for `(6, 4)`,
while `gcdSpec(6, 4)` reduces to `2`. The mutated `euclid-step` claim correctly
fails, yet the universal `program-correct` claim still prints `#Top`. Thus the
target proof is independent of the only submitted execution claim that notices
the body and can establish a false conclusion on the intended integer domain.

This is an answer-encoding operational bridge, not a K proof of the Euclidean
loop. The final decision is therefore `FAIL / NOT_LEGIT`.

## 1. Input and provenance integrity

The declared record layout is `legacy-selected-stage1`; the rendered mode is
`SUPPLIED_SEMANTICS`. The required trusted semantics mount
`/reference/reference-semantics` is present, so the mode and mounts do not
contradict one another.

I read `/audit-input.json` first and used only its `container_paths` locations,
not its host provenance paths. All required records for this layout are present
and readable:

- `/run.json`, `/task.json`, and `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`, `usage.json`,
  `codex-last.txt`, `codex-output.log`, and `prompt.txt`;
- the one structured trace JSONL below
  `/generation-evidence/codex-trace/`.

Historical `runtime-metrics.json` is absent, but this layout does not require
it. The present legacy records were also inspected. The structured trace has
502 valid JSON records and no malformed line. Its observable action sequence,
including all tool calls and agent messages, is recorded in
`evidence/02-generation-record.log`; the generation result and final message
claim `KPROVE_PASSED`, which I treated only as untrusted history.

The campaign object in `/audit-input.json` is structurally equal to
`/audit-campaign-lock.json`. The independently calculated lock SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
matching the launcher record.

The following independent integrity checks all passed:

- candidate `prompt.py` is byte-identical to `/reference/prompt.py`;
- candidate `py2mpy.py` is byte-identical to `/reference/py2mpy.py`;
- recursive, no-dereference comparison of candidate and trusted
  `reference-semantics/` reports no missing, additional, changed, mistyped, or
  symlinked entry;
- the candidate, trusted inputs, and generation evidence contain no symlink;
- every candidate and supplied-semantics file was independently hashed and
  inventoried.

Exact commands, statuses, hashes, entry types, and per-file semantics hashes are
in `evidence/01-integrity.log`. There is no audit-infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementations

The prompt's contract is: for two integers `a` and `b`, return a greatest common
divisor. Its examples require `gcd(3, 5) == 1` and `gcd(25, 15) == 5`.

The trusted canonical implementation repeatedly performs
`a, b = b, a % b` while `b` is truthy and returns `a`. The candidate first
replaces both inputs by their absolute values, then performs the same Euclidean
transition while `b != 0`, and returns `a`. For ordinary mathematical gcd this
candidate is a valid algorithm and always chooses the conventional nonnegative
representative.

Trusted regeneration produced a byte-identical constructor file:

```text
solution.mpy             5d14d8f54a5051b7d84fb8c61fe12eb2330f21f81e7e2ddb8ad78170a7677197
solution.regenerated.mpy 5d14d8f54a5051b7d84fb8c61fe12eb2330f21f81e7e2ddb8ad78170a7677197
```

The command and exit statuses are in
`evidence/03-translator-regeneration.log`.

### Independent differential test

`evidence/differential_test.py` imports the trusted canonical function and the
scratch copy of the generated function independently. It covers the two prompt
examples; the integer zero/empty-magnitude boundary `(0, 0)`; `b == 0` and
`b != 0`; every sign combination; equal, divisible, and coprime inputs; large
integers; the exhaustive square `[-100,100]^2`; and 1,000 deterministic random
255-bit pairs. Integers have no separate empty value.

Across 41,404 unique cases:

- candidate versus `math.gcd`: 0 mismatches;
- canonical versus `math.gcd`: 20,688 mismatches;
- candidate versus canonical: 20,688 mismatches.

All candidate/canonical mismatches are sign cases. For example,
`candidate(54, -24) == 6`, while `canonical(54, -24) == -6`. I judge the
candidate's value to agree with the natural-language mathematical contract;
the prompt does not request the canonical implementation's negative-sign
artifact. If canonical extensional behavior is instead deemed normative over
all signed integers, this is an additional material fidelity discrepancy. It
is not needed for the proof verdict. The script, full input-generation method,
command, status, counts, and sample mismatches are preserved in
`evidence/04-differential.log`.

## 3. Clean proof reconstruction

I copied only candidate source files and the trusted supplied semantics to
`/tmp/audit-work/gcd`. I did not copy or reuse a candidate kompiled definition
or cache. The available toolchain reports K version 7.1.293.

Fresh reconstruction results:

| Operation | Result | Evidence |
|---|---:|---|
| LLVM kompile of trusted `MPY-KRUN` | exit 0 | `evidence/05-kompile-llvm.log` |
| Reviewer concrete suite under LLVM | `.K`, `NoExc`, K exit code 0; process exit 0 | `evidence/06-krun-reviewer-cases.log` |
| Haskell kompile of `GCD-VERIFICATION` | exit 0 | `evidence/07-kompile-haskell.log` |
| `euclid-step` | `#Top`, exit 0 | `evidence/08-kprove-euclid-step.log` |
| `program-correct` | `#Top`, exit 0 | `evidence/09-kprove-program-correct.log` |
| both example claims | `#Top`, exit 0 | `evidence/10-kprove-examples.log` |

The reviewer concrete suite is `evidence/k_concrete_cases.py`. It includes
normal, zero, sign, equal, divisible, coprime, and larger inputs. This stage
confirms closure under the submitted extended theory; it does not validate that
the proof-local theory is sound.

## 4. Adequacy and real-program pinning

### Plain-language claims

`euclid-step` has precondition `A >= 0` and `B > 0`. Starting with an empty heap
and a current scope containing exactly integer locals `a = A` and `b = B`, it
executes `GcdLoopBody` and requires the resulting scope to contain
`a = B` and `b = pyMod(A, B)`. This is satisfiable, for example with
`L = 1`, an empty framed scope map, `A = 6`, and `B = 4`.

`program-correct` has no restriction beyond K-sort membership
`A0:Int, B0:Int`. From the standard empty module scope plus the supplied
builtins scope, it loads the submitted function and calls it. The final K value
is constrained exactly—not existentially or by a one-way implication—to
`gcdSpec(absInt(A0), absInt(B0))`. The post-state also pins the module binding
to the expected closure, restores `scopeLoc` to 1, leaves the heap and stack
empty, and leaves `ret` at `noRet`. A satisfying initial state exists for every
integer pair, including `(0, 0)` and `(-54, 24)`.

The two example claims have the same executable entry configuration but pin
the exact results 1 and 5.

Concrete substitutions are consistent with the generated implementation:

| Input | Formal `gcdSpec(abs(a),abs(b))` | Candidate Python | Canonical Python |
|---|---:|---:|---:|
| `(-54, 24)` | 6 | 6 | 6 |
| `(0, 0)` | 0 | 0 | 0 |
| `(54, -24)` | 6 | 6 | -6 |

The last row is the sign-convention discrepancy discussed in stage 2.

### Mechanical program pinning

I parsed and macro-expanded both the trusted-regenerated `solution.mpy` and the
claim's `Module(GcdDef)` term using the freshly built verification definition.
Their normalized KORE files are byte-identical with SHA-256
`acb7fe33d7d4d7006e9a640292ffe92dfa94eb464d1046df1966ace090d4b9c7`.
See `evidence/11-program-term-comparison.log`.

Thus the entry claim pins the actual submitted binding and body; the explicit
`.Exprs`/`.Stmts` spellings are only list normalization. The function load,
callee lookup, argument binding, both `abs` calls, final `Return`, frame pop,
and module binding are real supplied-semantics execution. The material loop is
the exception: its term is real, but the proof-local rule replaces its
execution with the desired answer.

The adversarial body mutation was also mechanically checked. The trusted
translation of the altered Python function and the altered claim macro expand
to identical KORE with SHA-256
`e9be7e7eb61564d5a715fe15c332f01b9de217f872d9365a85d7450a9fe9102`.
See `evidence/15-body-mutation-program-term.log`. This confirms that the
body-sensitivity test changed the program term actually executed by the claim.

## 5. Rule-by-rule static soundness review

There is no candidate `semantic.k` or generated semantic helper: this is
supplied-semantics mode. The full index of every syntax declaration,
configuration, context, and rule in the 2,211-line trusted semantics tree is
preserved in `evidence/20-static-rule-inventory.log`. The candidate-local proof
theory consists of exactly six syntax declarations and eight rules. The same
evidence file contains its complete numbered source.

### Candidate-local inventory

| Extension | Kind and attributes | Review |
|---|---|---|
| `GcdDef` plus its rule | `Stmt` macro | Expands to the exact function name, parameters, and `GcdBody`; mechanically pinned and sound. |
| `GcdCondition` plus its rule | `Expr` macro | Exact `b != 0` constructor; sound. |
| `GcdLoopBody` plus its rule | `Stmts` macro | Exact simultaneous tuple assignment; mechanically pinned and sound as syntax. |
| `GcdBody` plus its rule | `Stmts` macro | Exact two `abs` assignments, while, return, and empty statement tail; sound as syntax. |
| `GcdClosure` plus its rule | `Val` macro | Exact two-parameter closure over `GcdBody` with defining environment 0; agrees with supplied function loading. |
| `gcdSpec(Int,Int)` | proof-local `[function, symbol(gcdSpec), no-evaluators]` result-bearing symbol | Opaque for symbolic proof. Its value directly determines the returned value and the postcondition. It is not an external primitive; it summarizes program-defined computation. |
| `gcdSpec(A,0) => A` | guarded `[concrete]` equation, `A >= 0` | Mathematically valid. |
| `gcdSpec(A,B) => gcdSpec(B,pyMod(A,B))` | guarded `[concrete]` equation, `A >= 0`, `B > 0` | Mathematically valid Euclidean recurrence. The guards are disjoint from the base rule and cover the concrete nonnegative domain. For `B > 0`, `pyMod(A,B)` is nonnegative and smaller than `B`, so concrete reduction descends. These ground equations do not establish the symbolic loop connection. |
| `<k> #while(GcdCondition,GcdLoopBody) => .K ...</k>` | ordinary operational rule with `[priority(40), symbolic(A,B)]` | Illegitimate answer-encoding bridge. It preempts fixed while execution on symbolic nonnegative locals, writes `a := gcdSpec(A,B)` and `b := 0`, and is the sole universal value connection. No bridge-free theorem justifies it. |

There are no other proof-local `total`, `functional`, simplification, priority,
ordinary semantic, or opaque declarations. `gcdSpec` is not marked `total`.
The four spec claims are `euclid-step`, `program-correct`, `example-3-5`, and
`example-25-15`; none is imported into `verification.k` as a proved lemma.

### Used-construct map through the supplied semantics

| Submitted construct | Declaration and material fixed rules |
|---|---|
| `Module`, `FuncDef`, `Params`, statement lists | `semantics/syntax.k`; `#loadAll` and statement sequencing in `core.k`; definition binding in `functions.k` |
| `Call`, `Name`, arguments | callee-first and left-to-right argument evaluation in `call.k`/`core.k`; lexical lookup through module and builtins scopes in `core.k`; closure-frame allocation and parameter binding in `call.k`/`functions.k` |
| `abs` | real builtin binding in `builtinsScope`; `applyBuiltin("abs",I) => absInt(I)` in `builtins.k` |
| ordinary assignment | RHS strictness from `syntax.k`; current-scope update in `controls.k` |
| `While` | `While => #while`, condition evaluation, truthiness branch, body, and loop continuation in `controls.k` |
| `Compare(...,"!=",0)` | explicit left/right contexts in `operators.k`; integer comparison in `int.k` |
| tuple RHS and tuple target | left-to-right element evaluation, tuple construction, then sequential unpack/binding in `tuple.k`; this preserves Python's simultaneous assignment values |
| `%` | left-to-right `BinOp` strictness, operator dispatch in `operators.k`, integer `pyMod` in `int.k` |
| `Return` | strict result evaluation, `retV`, frame pop, environment/scope restoration in `functions.k` |

The actual program allocates no heap object. After `abs`, both locals are
nonnegative; when the body executes, `b != 0` therefore means `b > 0`, so `%`
does not see a zero denominator. Fixed evaluation order, call/return control,
scope writes, and exception-free behavior are adequate for all operations used
by this program.

### Operational bridge audit and false-conclusion witness

The loop rule reads `<k>`, `<env>`, and the current `<scopes>` entry; it replaces
the loop redex, writes both local values, and frames the continuation, parent
scope, heap, allocation state, stack, return state, exception state, and exit
code. It introduces no abrupt return: `.K ...` retains the existing suffix.
For the immutable Euclidean body, finite execution checks found no arithmetic
counterexample to the summary. That is not a universal connection proof.

The decisive defects are:

1. The bridge matches before the supplied condition/body rules and directly
   injects the same opaque `gcdSpec` term demanded by the final postcondition.
   Using the same result-bearing symbol on both sides is circular.
2. No claim over fixed semantics proves that exact loop, binding, continuation,
   and state transition for the bridge's complete domain.
3. `euclid-step` proves only one assignment transition. It states neither
   preservation of `gcdSpec` nor a loop invariant, and it is not a dependency
   of the target claim.
4. `evidence/23-kprove-program-only.log` proves an exact copy of
   `program-correct` in a spec that contains no `euclid-step` claim.
5. Removing the bridge and rebuilding succeeds, but a depth-80 diagnostic of
   `program-correct` reaches a genuine stuck implication and no `#Top`
   (`evidence/21-kompile-no-bridge.log` and
   `evidence/22-kprove-no-bridge-depth80.log`). This bounded diagnostic is used
   only to show dependency, not as a claim that no honest proof can exist.

The required false-conclusion witness is `(6,4)` for the body

```python
while b != 0:
    b = 0
```

This altered program terminates and returns 6, while the claimed result is
`gcdSpec(6,4) = gcdSpec(4,2) = gcdSpec(2,0) = 2`.
`evidence/body_sensitivity_solution.py` records the witness, and both CPython
and fixed LLVM semantics accept assertions that the result is 6 and is not 2
(`evidence/13-body-mutation-fixed-execution.log`). Nevertheless, after a clean
Haskell build, the body-mutated universal claim prints `#Top`
(`evidence/14-kompile-body-mutation.log` and
`evidence/16-kprove-body-mutation-program-correct.log`). The body-mutated
`euclid-step` claim exits 1 with `WarnStuckClaimState`
(`evidence/17-kprove-body-mutation-euclid-step.log`).

I therefore do not claim that the immutable Euclidean summary has a discovered
arithmetic counterexample. The narrower and sufficient finding is that the
target proof assumes that summary as an operational rule, and the concrete
body-sensitivity witness demonstrates that this proof mechanism enables a
false theorem over a satisfying intended-domain input. Under the benchmark's
explicit rule against answer-encoding execution bypasses, Gate A fails.

## 6. Fresh non-vacuity test

I did not rely on any candidate vacuity artifact. The fresh module
`evidence/spec-vacuity.k` executes the real submitted program on `(3,5)` but
changes its exact required result from 1 to 2.

The mutation is well formed: `kprove --dry-run` exits 0
(`evidence/18-vacuity-dry-run.log`). The full proof exits 1 with
`WarnStuckClaimState`; its residual final `<k>` cell contains `1 ~> .K`, which
does not unify with the mutated destination 2
(`evidence/19-vacuity-proof.log`). This is the expected unmet result
obligation, not a parse error, missing import, timeout, or unrelated crash.

The original claims are therefore result-constraining and non-vacuous. This
does not repair the unsound source of the universal result.

## 7. Proven-versus-assumed accounting

### What the successful runs establish

Under the extended `GCD-VERIFICATION` theory, the reconstructed K runs
establish:

- fixed supplied semantics executes one real Euclidean tuple-assignment step
  as stated by `euclid-step`;
- fixed supplied semantics executes the two concrete examples to 1 and 5;
- symbolic loading, calls, `abs`, and return plumbing reduce the universal
  program call to `gcdSpec(absInt(A0),absInt(B0))` after applying the
  proof-local loop bridge.

The universal `#Top` is therefore conditional on the bridge's already-assumed
statement that the submitted while loop computes `gcdSpec`. It does not prove
that statement from the supplied semantics.

### Trust ledger

| Boundary | Role and dependents | Judgment |
|---|---|---|
| K 7.1.293 parser, Haskell/LLVM backends, SMT reasoning, mathematical `Int`/`Bool`/`Map` hooks | All executions and proofs | Ordinary toolchain trust; acceptable. |
| Supplied reference semantics | Defines the modeled Python subset | Required fixed trust boundary; byte/entry integrity verified. Relevant used rules were reviewed and concretely exercised. |
| Trusted `py2mpy.py` | Source-to-constructor bridge | Acceptable for this artifact: trusted regeneration is byte-identical, and expanded claim/program KORE is byte-identical. |
| `absInt`, `%Int`, and `pyMod` | Integer normalization and modulo | Fixed mathematical primitives/rules; guards keep used modulo denominators positive. Acceptable. |
| Proof-local concrete `gcdSpec` equations | Ground Euclidean mathematical specification | Truthful and descending on concrete nonnegative inputs; they support examples and finite ground comparison. They do not connect symbolic program execution to the value. |
| Proof-local symbolic loop rule | Replaces the material program-defined loop and supplies the result used by `program-correct` | Illegitimate. It is inside the theorem, result-bearing, has no bridge-free universal connection theorem, and the body-sensitivity witness shows it can enable a false result. |
| Differential and concrete tests | Empirical source/semantic bridge evidence | 41,404 Python cases and the K boundary suite are useful finite evidence only; they cannot prove the universal loop summary. |
| Candidate `prove.log`, generation trace, and final report | Historical claims | Untrusted and not used as proof. |

The formal domain is not materially narrowed: the universal claim ranges over
all K integers and normalizes signs with `absInt`. The failure is instead at
the core real-program soundness boundary. Because the target's result-bearing
loop computation is assumed by an operational rewrite rather than proved,
the reconstructed `#Top` is not a legitimate partial-correctness proof of the
real generated program.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
