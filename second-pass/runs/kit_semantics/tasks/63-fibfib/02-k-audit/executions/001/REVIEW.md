# Independent adversarial review: 63-fibfib

The candidate contains a legitimate partial-correctness proof of the submitted
program for every nonnegative integer input. I reconstructed the proof from
source, checked the submitted program against the trusted translator and
canonical implementation, inventoried the complete imported K source theory,
audited every proof-local rule, and ran fresh body-sensitivity and non-vacuity
tests. No candidate-built definition or cache was used.

## 1. Input and provenance integrity

The launcher record declares `record_layout = pipeline-v3`,
`semantics_mode = SUPPLIED_SEMANTICS`, condition `kit-semantics`, and problem
`63-fibfib`. This is consistent with the mounts: the trusted
`/reference/reference-semantics` tree is present.

I read all records required for pipeline-v3:

- `/audit-input.json` and `/audit-campaign-lock.json`;
- `/run.json`, `/task.json`, and `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`,
  `runtime-metrics.json`, `usage.json`, `codex-last.txt`,
  `codex-output.log`, and `prompt.txt`; and
- the sole 261-record JSONL trace below
  `/generation-evidence/codex-trace/`.

The structural record inspection is preserved in
[`evidence/01a-generation-records.log`](evidence/01a-generation-records.log).
It parsed all 261 trace records and read the complete 699,996-byte generation
log. The generation result and invocation report a successful stage with exit
zero, but those claims were not used as proof evidence.

The campaign object in `/audit-input.json` equals
`/audit-campaign-lock.json` as JSON, and the lock's independently measured
SHA-256 is the recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
All required regular files and real directories are readable and are not
symlinks.

Independent file hashes match the hashes recorded in `/audit-input.json`,
`/generation-result.json`, and the generation invocation. In particular:

| Mounted input | Independently measured SHA-256 |
|---|---|
| trusted canonical | `f6ef5a11fa60a8cd9598c43f4a8f1a499a750ec8ed672414c22f3744d286abdc` |
| trusted and candidate prompt | `3f6b45cdf3c576835537ba1cce2414a28f96b7a82157533ba221807ea2aa6147` |
| trusted and candidate translator | `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16` |
| run manifest | `3b99df09203880c9a59a6dcfed87c41b60e6057ebf8720421e156f1e7517bd73` |
| task manifest | `f163fd3c7098703a3525dc0cb7ec03a3ad223a9c40f25385ed31f5a38d0bf60d` |
| generation result | `7daf9b674e4e4b2c78f7aa2ae75737d16652b2ac448581f2928a25c7c705693d` |
| invocation | `40dce4655f7e346c0f00e3d8c3edcf8ed7f4307c005620b6350c7543c9467785` |
| generation trace JSONL | `4c2704c99b007077971863cda4441f0bda09dca2b4b25856dfdc5a0e7ef03fff` |

Using the launcher's `pipeline_contract.sha256_tree` algorithm, the mounted
candidate hashes to
`7392e832d2a3f56eb43a6c183c5d069860c374aa1ca685fda26456d836766372`,
which is exactly the generation invocation/result `workspace_sha256`. The trace
tree hashes to
`a71f5d3386bf6f056c668bcfe79187caece54faf1c75312d0e9d62fd092e2dd7`,
which is exactly `usage.json`'s `source_trace_sha256`.

The trusted and candidate supplied-semantics trees both independently hash to
`4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`.
A recursive, no-symlink `diff` reports no missing, additional, mistyped, or
changed entry. `cmp` likewise reports exact identity for prompt and translator.
The complete checks and exact hashes are in
[`evidence/01-provenance.log`](evidence/01-provenance.log).

There is no infrastructure breach and no candidate integrity defect.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The trusted prompt defines the FibFib sequence on its natural index domain:

- `F(0) = 0`;
- `F(1) = 0`;
- `F(2) = 1`; and
- `F(n) = F(n-1) + F(n-2) + F(n-3)` thereafter.

The requested result is the `n`th element, efficiently computed. The source
contract's meaningful domain is nonnegative integers. This interpretation is
also consistent with the trusted canonical function: its three bases are
`0,1,2`, and its recursive branch moves toward those bases only for positive
inputs.

The candidate uses a consecutive-triple loop. At index `i`, its variables
`a,b,c` are intended to hold `F(i),F(i+1),F(i+2)`. It therefore returns the
same sequence while avoiding the canonical implementation's exponential
recursion.

### Trusted regeneration

In scratch I ran:

```text
python3 py2mpy.py solution.py > solution.regenerated.mpy
cmp solution.regenerated.mpy solution.mpy
```

Both commands exited zero. The submitted and regenerated files have identical
SHA-256
`1c45dcf09ee4c7ccc9d51716f7b67bb515f33dd86160a39c745fd903f2b9c4b9`.
See [`evidence/02-program-fidelity.log`](evidence/02-program-fidelity.log).

### Independent differential test

[`evidence/differential_test.py`](evidence/differential_test.py) imports the
trusted canonical entry point and the isolated candidate entry point by
absolute path; it does not reuse the proof equations. It covers:

- lower/empty-sequence boundary `0`;
- every base/branch boundary `0,1,2,3`;
- the examples `1,5,8`;
- additional fixed values through `20`; and
- 16 pseudorandom values from `0..20` with recorded seed `630063`.

All 28 comparisons agree, including `F(0)=0`, `F(3)=1`, `F(5)=4`,
`F(8)=24`, and `F(20)=35890`; mismatch count is zero. The exact inputs and
rows are in [`evidence/02-program-fidelity.log`](evidence/02-program-fidelity.log).
This is finite implementation/canonical evidence, not the universal proof.

## 3. Clean proof reconstruction

I copied only source artifacts to `/tmp/audit-work`. The candidate's
`runtime-kompiled`, `verification-kompiled`, `__pycache__`, logs, and other
caches were neither copied nor referenced.

### Concrete definition

I translated the reviewer-authored
[`evidence/concrete_audit.py`](evidence/concrete_audit.py), whose function AST
is mechanically identical to `solution.py`, and compiled the trusted semantics
from source:

```text
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
krun concrete_audit.mpy --definition audit-runtime-kompiled
```

The build exited zero. `krun` discharged assertions for `0,1,2,3,5,8` and
ended with `.K`, `NoExc`, and exit code zero. Exact commands and bounded output
are in:

- [`evidence/03c-kompile-llvm.log`](evidence/03c-kompile-llvm.log);
- [`evidence/03d-krun-concrete.log`](evidence/03d-krun-concrete.log).

The LLVM compiler reported non-exhaustive total functions for unrelated
string/float/list operations and unused variables in `str.k`. None is reachable
from this integer-only program.

### Proof definition and claims

I independently compiled the Haskell proof definition:

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
```

It exited zero. The all-claims target command:

```text
kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC
```

printed `#Top` and exited zero. See
[`evidence/03e-kompile-haskell.log`](evidence/03e-kompile-haskell.log) and
[`evidence/03f-kprove-all.log`](evidence/03f-kprove-all.log).

The two claims have an intentional dependency: the entry claim uses the loop
claim as a circularity. I checked that composition rather than treating a
joint `#Top` as opaque:

1. The loop claim alone prints `#Top` and exits zero
   ([`evidence/03g-kprove-loop.log`](evidence/03g-kprove-loop.log)).
2. The entry claim, with only that separately proved loop theorem marked
   trusted for the modular run, prints `#Top` and exits zero
   ([`evidence/03i-kprove-entry-with-proved-loop.log`](evidence/03i-kprove-entry-with-proved-loop.log)).
3. The actual target run proves both together, without any trusted claim, and
   prints `#Top`.

For transparency, selecting the entry label alone while deleting its loop
circularity gets stuck on the `N=0`/loop branch
([`evidence/03h-kprove-entry.log`](evidence/03h-kprove-entry.log)). That is not
the submitted theorem environment and not a positive target command; it is the
expected consequence of removing a proved dependency.

Every positive target claim therefore closes in the reconstructed proof.

## 4. Adequacy and real-program pinning

### Plain-language claims

`fibfib-loop` assumes integers `I,N` with `0 <= I <= N`. It starts at the
actual internal `#while` for the submitted body with:

```text
a = F(I), b = F(I+1), c = F(I+2),
i = I, n = N, next_value = F(I+2)
```

It preserves the framed continuation and reaches loop exit with the same
relations based at `N`. The global closure, callee scope, scope allocator,
empty heap, frame stack, return state, exception state, and exit code are all
constrained.

`fibfib-entry` assumes `N >= 0`. It loads the module, binds the exact `fibfib`
closure, evaluates `Call(Name("fibfib"), Int(N))`, and reaches the exact result
`fibfibSpec(N)`. It constrains the restored caller environment, surviving
global closure, deallocated callee scope, allocator values, empty heap and
stack, `noRet`, `NoExc`, and exit code zero. The result is not a free variable,
tautology, or one-way side condition.

### Mechanical program identity

[`evidence/pinning_check.py`](evidence/pinning_check.py) extracts the balanced
`Module(...)` argument actually under the entry claim's `#loadAll`. Its
constructor normal form equals the trusted-regenerated `solution.mpy` exactly.
The only normalizations are whitespace and explicit `.Stmts` list units, which
are optional units of the same K list syntax. There is exactly one `#loadAll`
entry term. The check also confirms that the concrete K harness's function AST
equals `solution.py`'s function AST. See
[`evidence/04a-pinning.log`](evidence/04a-pinning.log).

This pins the submitted binding and body, not merely a similarly named helper.
Function creation, lookup, argument evaluation, parameter binding, each loop
operation, return, and frame pop all execute through the fixed supplied
semantics.

### Satisfiable preconditions and ground substitution

`N=0` and `N=5` are explicit satisfying witnesses for the entry precondition;
for the loop precondition, `I=0,N=0` and `I=0,N=5` are explicit witnesses.
Ground substitutions `N=0,1,2,3,5,8` give formal target values
`0,0,1,1,4,24`, respectively. The trusted canonical and generated Python
functions return exactly those values; the complete rows are in
[`evidence/04a-pinning.log`](evidence/04a-pinning.log). The concrete K run
independently covers the same boundaries.

### Body sensitivity

The fresh mutation
[`evidence/reviewer-body-mutation.k`](evidence/reviewer-body-mutation.k)
changes the constructor term actually loaded and stored in the closure:
`Return(Name("a"))` becomes `Return(Name("c"))`. It does not merely edit an
external source file. At satisfying input `N=1`, the modified execution reaches
`1`, while the original result obligation is `0`. `kprove` exits 1 with
`WarnStuckClaimState` and the concrete residual `<k> 1 ~> .K </k>`. See
[`evidence/04b-body-mutation.log`](evidence/04b-body-mutation.log).

The theorem is therefore sensitive to the executed program body.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[`evidence/rule_inventory.py`](evidence/rule_inventory.py) lexically inventories
every top-level declaration with its source span and complete normalized text.
The resulting
[`evidence/05-rule-inventory.log`](evidence/05-rule-inventory.log) covers all
26 applicable source/proof files and contains:

- 1 configuration;
- 228 syntax declaration blocks;
- 5 evaluation contexts;
- 701 rules (695 supplied plus 6 proof-local);
- 2 reachability claims;
- 146 declaration blocks bearing `function`;
- 108 bearing `total`;
- no source declaration bearing explicit `functional`;
- 25 bearing `symbol(...)`;
- 23 bearing `no-evaluators`;
- 45 priority rules;
- 40 concrete rules;
- 26 `owise` rules;
- 1 simplification rule; and
- all macro, strictness, module, import, and require declarations.

Per-file rule disposition is:

| File/module | Rules | Disposition for this theorem |
|---|---:|---|
| `semantics.k`, `syntax.k`, `iter.k` | 0 | assembly/syntax only; relevant constructors checked below |
| `core.k` | 46 | reachable load, sequencing, lookup, literals, argument collection, truthiness, and scope rules checked; other heads/guards unreachable |
| `operators.k` | 10 | integer `BinOp`/`Compare` dispatch and contexts checked; reference-only branches unreachable |
| `int.k` | 16 | integer `+`, `<`, and concrete-test `==` checked; remaining operators unreachable |
| `controls.k` | 34 | ordinary assignment and while lifecycle checked; other statements, ref paths, and loop controls unreachable |
| `functions.k` | 15 | unannotated def, parameter bind, return, and pop checked; closure-cell variants unreachable |
| `call.k` | 21 | generic call evaluation and ordinary closure call checked; builtin/method/ref variants unreachable |
| `assert.k` | 3 | true assertion rule checked for the concrete harness only |
| `bool.k` | 13 | no BoolOp is in the submitted program; fixed rules unreachable |
| `range.k` | 6 | no range/iteration term is reachable |
| `list.k` | 27 | no list/ref term is reachable |
| `tuple.k` | 21 | no tuple/unpacking term is reachable |
| `set.k` | 12 | no set term is reachable |
| `str.k` | 28 | no string term is reachable |
| `subscript.k` | 40 | no subscript/slice term is reachable |
| `comprehension.k` | 7 | no comprehension term is reachable |
| `methods.k` | 75 | no attribute or method call is reachable |
| `builtins.k` | 137 | no builtin call is reachable |
| `float.k` | 121 | no float/import/math term is reachable |
| `dict.k` | 28 | no dict term is reachable |
| `sort.k` | 19 | no sorted/sort term is reachable |
| `concrete.k` | 16 | imported only by the LLVM definition; all keyed-sort/deep-list heads are unreachable |
| `verification.k` | 6 | every proof-local rule individually justified below |

This grouping is exhaustive: every rule listed in the full inventory is either
one of the reachable rules mapped below, one of the six proof-local rules, or a
fixed-semantics rule whose constructor, value sort, callable binding, or guard
cannot occur in the pinned program states. Unreachable fixed rules cannot
change the result or make the target claim provable.

### Complete mapping for used constructs

| Submitted constructor/effect | Declaration and rules |
|---|---|
| `Module`, statement list | `syntax.k:53-61`; `core.k:124-127` |
| configuration/cells | `core.k:44-60` |
| `FuncDef`, closure binding | `functions.k:14-16` |
| `Call`, callee then arguments | `syntax.k:28`; `call.k:18-21`; `core.k:183-191` |
| ordinary closure frame creation | `call.k:69-74` |
| `Params`, binding | `functions.k:63-66` |
| `Int` | `syntax.k:9`; `core.k:193-196` |
| `Name` lookup | `syntax.k:12`; `core.k:129-154` |
| `Assign` RHS-first evaluation/write | `syntax.k:41 [strict(2)]`; `controls.k:9-18` |
| `BinOp("+",...)` left-to-right | `syntax.k:15 [seqstrict(2,3)]`; `operators.k:10-12`; `int.k:9` |
| `Compare("<",...)` left-to-right | `syntax.k:30-32`; `operators.k:14-17`; `int.k:22` |
| `While` | `syntax.k:46`; `controls.k:65-82,85` |
| integer guard truthiness | `core.k:198-205` |
| `Return` and frame restoration | `syntax.k:50 [strict]`; `functions.k:77-90` |

The order is Python-compatible for every material operation: assignment
evaluates the RHS before writing, nested addition evaluates left-to-right,
comparison evaluates both operands in order, the guard is re-evaluated each
iteration, call lookup precedes argument evaluation, and return restores and
deallocates the callee frame. The program performs no heap allocation, output,
exception, mutation through references, import, or external call.

The only applicable scope is an ordinary scope without `"$cells"`. Therefore
the higher-priority closure-cell lookup, assignment, and parameter rules have
false guards. Every other supplied priority rule requires a ref/list/dict,
tuple, float `math`/`hashlib` call, sort, method, slice, or other syntactically
disjoint head. No priority rule can preempt the used path. There is no
proof-local priority rule or operational bridge.

### Proof-local rules

`verification.k` adds one syntax declaration and exactly six rules:

1. `fibfibSpec(0) => 0` — exactly the first source-contract base.
2. `fibfibSpec(1) => 0` — exactly the second base.
3. `fibfibSpec(2) => 1` — exactly the third base.
4. For `N >= 3`, `fibfibSpec(N)` rewrites to the three prior terms — exactly
   the source recurrence.
5. For `N < 0`, `fibfibSpec(N) => 0` — a disjoint totalization convention
   outside the theorem and source domain. No reachable summary argument is
   negative, so it has no dependent conclusion here.
6. For `I >= 0`,
   `F(I)+F(I+1)+F(I+2) => F(I+3)` — substitute `N=I+3` into rule 4 and use
   associativity/commutativity of integer addition. Its domain implies
   `N>=3`; it strictly reduces three summary occurrences to one.

Rules 1-5 have pairwise-disjoint, exhaustive integer guards. Recursive rule 4
decreases its argument toward a base. Rule 6 is a truthful derived
mathematical simplification, has no cells or control effect, and cannot replace
program execution. `fibfibSpec` bears `no-evaluators`, but it is not an
unconstrained oracle: its equations uniquely determine every integer value,
and only nonnegative values influence the theorem.

The loop claim itself is a derived reachability circularity, not an ordinary
semantic rewrite. Its match fixes the real loop body, binding, local/global
scopes, allocator cells, empty heap, exact frame, return/exception state, and
exit code. Its framed continuation is sound because the body has no return,
break, continue, exception, call, heap effect, or other abrupt control.
One fixed-semantics iteration precedes reuse of the circularity and advances
`I` to `I+1`.

### Opaque and total declarations

The full inventory includes the supplied float symbols, `sortVS`,
`sortKeyVS`, `md5hexCodes`, and incomplete-but-total collection helpers. Those
are genuine trust/coverage boundaries of the broad supplied language, and the
LLVM compiler reports some of them as non-exhaustive. None can be constructed,
selected, or observed by this program or either target postcondition.
`MPY-CONCRETE` is absent from the Haskell proof module closure; the Haskell
compiled rule list contains six `verification.k` rules and no
`semantics/concrete.k` rule
([`evidence/05a-module-closure.log`](evidence/05a-module-closure.log)).

No inventoried rule encodes FibFib's answer, intercepts the program call,
introduces an unconstrained result, skips the loop, fabricates state, or
preempts material fixed execution. I found no unsound rule applicable on the
intended domain, so there is no false-conclusion witness to report.

## 6. Fresh non-vacuity test

I did not rely on the candidate's `spec-vacuity.k`. The fresh mutation is
[`evidence/reviewer-vacuity.k`](evidence/reviewer-vacuity.k). It executes the
original loaded constructor term at satisfying input `N=8` but changes the
result obligation from the true `24` to the false `25`.

First, a dry run successfully parsed and built the mutation, exiting zero:

```text
kprove reviewer-vacuity.k --definition audit-verification-kompiled \
  --spec-module REVIEWER-VACUITY --dry-run
```

See [`evidence/06a-vacuity-dry-run.log`](evidence/06a-vacuity-dry-run.log).

The actual proof command exited 1 with `WarnStuckClaimState`. Its residual is
the fully executed `<k> 24 ~> .K </k>` configuration, with normal environment,
scope, heap, stack, return, exception, and exit cells, against the demanded
`25`. This is the expected unmet result obligation, not a parse failure,
timeout, crash, or unreachable mutation. See
[`evidence/06-vacuity.log`](evidence/06-vacuity.log).

The proof is result-constraining and non-vacuous.

## 7. Proven versus assumed accounting

### Formally established

Under the reconstructed `VERIFICATION` theory, for every K integer `N >= 0`,
if the exact submitted `solution.mpy` module/call execution terminates, its
result is `fibfibSpec(N)`. The execution performs the real binding, lookup,
argument evaluation, initialization, comparison, integer additions,
assignments, loop control, return, and frame restoration. The loop claim
establishes the consecutive-triple invariant for arbitrary nonnegative `N`;
the entry claim connects that invariant to the exact loaded program. This is
partial correctness, not a resource or total-termination theorem.

### Trusted or informal boundaries

| Boundary | Influence | Assessment |
|---|---|---|
| Supplied MPY semantics | All modeled execution and cells | Required trusted baseline; byte-identical to the mounted reference and dynamically reconstructed. Used subset was audited rule by rule. |
| K v7.1.293, Haskell/LLVM backends, K builtins, and SMT reasoning | Parsing, execution, arithmetic, reachability | Standard verification machinery trust. |
| Trusted `py2mpy.py` translation | Source-to-constructor bridge | The translator itself is outside the theorem. Trusted regeneration proves byte identity of the submitted artifact; mechanical extraction proves that exact artifact is executed. |
| Interpretation of the contract domain as nonnegative integers | Theorem scope | Appropriate for an indexed sequence with bases `0,1,2`; consistent with the canonical implementation. No finite bound is imposed. |
| `fibfibSpec` bases/recurrence | Target mathematical meaning | Direct formalization of the prompt, not an empirical oracle. The shifted lemma is an ordinary mathematical consequence. |
| Negative `fibfibSpec` totalization | No reachable result | Arbitrary but disjoint and unused; acceptable, with no conclusion dependent on it. |
| Unused supplied opaque symbols | None on this program | Broad-language trust/coverage limitation only; no control, state, or result dependence here. |
| Differential and concrete tests | Finite implementation/translation support | Reproducible supporting evidence only; not substituted for the K proof. |
| Termination/performance | Excluded | The audit establishes the requested partial correctness. The source loop's informal variant is `N-i`, but no separate total-correctness theorem is claimed. |

There is no proof-local trusted primitive, operational bridge, fresh
result-bearing abstraction, empirical call interceptor, or unproved opaque
value affecting the theorem. The lack of an automatic source-to-spec generator
is only an artifact-maintenance observation; identity of this immutable
candidate is mechanically established.

## Decision

Gate A (real-program soundness), Gate B (intent adequacy), and Gate C (trust and
evidence auditability) all pass. The clean target proof closes, its formal
domain covers the material HumanEval source-contract domain without a finite
bound, the result is exact and non-vacuous, and no material adequacy or
soundness gap remains.

VERDICT: PASS
LEGITIMACY: LEGIT
