# Independent adversarial audit: HumanEval/100 `make_a_pile`

The candidate contains a legitimate partial-correctness proof of the submitted
program for the full source-contract domain (`n` is any positive mathematical
integer). I reconstructed both K definitions from source, reran both target
claims, mechanically pinned the claim term to the regenerated program, audited
the complete local rule surface, and obtained meaningful failures from both an
executed-body mutation and a fresh false-result mutation.

## 1. Input and provenance integrity

The launcher declares `record_layout = legacy-selected-stage1` and
`semantics_mode = SUPPLIED_SEMANTICS`. This agrees with the mounts:
`/reference/reference-semantics` is present, so there is no mode contradiction
and no infrastructure breach.

I read `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
`/task.json`, `/generation-result.json`, and the required generation records:
`invocation.json`, `metrics.json`, `usage.json`, `codex-last.txt`,
`codex-output.log`, `prompt.txt`, and the structured trace. Historical runtime
metrics are not required for this legacy layout. The generation report and its
prior `#Top` statements were treated only as untrusted claims.

Independent checks established:

- The campaign-lock JSON is exactly equal to the campaign block, and its
  SHA-256 is the declared
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
- Every launcher-declared regular-file hash matches, including the run, task,
  stage-result, invocation, metrics, usage, prompt, output log, final message,
  and trace.
- The structured JSONL trace has 675 parseable records. Its one trace file has
  SHA-256
  `3854487021ed4cd526bc2c0b48710d2134b64e5c56cb4752760e9450cc574f3a`,
  as recorded.
- `/candidate/prompt.py` and `/candidate/py2mpy.py` are byte-identical to their
  trusted mounts.
- Recursive type/path/content comparison found exactly 24 regular files in
  each supplied-semantics tree. There are no missing, additional, changed,
  mistyped, or symlinked entries.
- All required proof artifacts (`solution.py`, `solution.mpy`,
  `verification.k`, `spec.k`, and `prove.sh`) are present as regular files.

The independent checker, complete per-file tree hashes, command, output, and
exit 0 are preserved in
[`stage1_integrity.py`](evidence/stage1_integrity.py) and
[`stage1_integrity.log`](evidence/stage1_integrity.log).
The consolidated exact-command/status ledger is
[`COMMANDS.md`](evidence/COMMANDS.md).
The live tool versions are preserved in
[`tool_versions.log`](evidence/tool_versions.log).

**Stage 1 result: PASS.**

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt requires, for any positive integer `n`, a list representing
`n` levels. Level 1 contains `n` stones, and every next level is the next number
of the same parity. Equivalently, the result has length `n` and zero-based
element `i` is `n + 2*i`. The trusted canonical implementation is:

```python
return [n + 2*i for i in range(n)]
```

The submitted implementation initializes an empty list and `i = 0`, appends
`n + 2*i` while `i < n`, increments `i`, and returns the list. This implements
the same contract for every positive integer, with no finite bound or parity
restriction.

Using the trusted translator in clean scratch produced a regenerated
`solution.mpy` byte-identical to the submitted file. Both hashes are:

```text
51dde21998fef5f79c1d1f8afa1727f97586cb330e4bfcb8fd6026176618cf74
```

The exact command and exit 0 are in
[`translation_identity.log`](evidence/translation_identity.log).

The independent differential test imports `/reference/canonical.py` and
`/candidate/solution.py`. It covers the documented example; the minimum
positive input; the first even input; every positive input from 1 through 256;
fixed larger boundaries; and 64 seeded generated values up to 10,000. There
were 325 distinct positive inputs and zero mismatches. It also records
diagnostic results for `-5`, `-1`, and `0`, clearly outside the positive-input
contract. The test additionally checks length, first/last element, and every
element formula. See
[`differential_test.py`](evidence/differential_test.py) and
[`differential_test.log`](evidence/differential_test.log).

**Stage 2 result: PASS.**

## 3. Clean proof reconstruction

I copied source artifacts to `/tmp/audit-work` and did not copy or reuse any
candidate-provided compiled definition or cache. The following fresh commands
were run.

Concrete definition and execution:

```bash
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled

python3 py2mpy.py concrete_tests.py > audit-concrete-tests.mpy
cmp -s audit-concrete-tests.mpy concrete_tests.mpy
krun audit-concrete-tests.mpy --definition audit-runtime-kompiled
```

The LLVM build exited 0. The concrete program exited 0 with `.K`, `NoExc`, and
exit code 0; its heap contains the expected results for `n = 1, 3, 4`.
Bounded output is in
[`kompile_llvm.log`](evidence/kompile_llvm.log) and
[`krun_concrete.log`](evidence/krun_concrete.log).

Proof definition:

```bash
kompile verification.k \
  --backend haskell \
  --main-module PILE-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
```

This exited 0; see
[`kompile_haskell.log`](evidence/kompile_haskell.log).

Every positive target module was then run independently:

```bash
kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module PILE-PREFIX-SPEC

kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module PILE-LOOP-SPEC
```

Each command exited 0 and printed `#Top`. See
[`kprove_prefix.log`](evidence/kprove_prefix.log) and
[`kprove_loop.log`](evidence/kprove_loop.log).

**Stage 3 result: PASS.**

## 4. Adequacy and real-program pinning

### Plain-language claims

`PILE-PREFIX-SPEC` assumes `N > 0` and the supplied semantics' ordinary initial
configuration. It loads `pileModule`, looks up and calls `make_a_pile(N)`,
allocates the list and callee scope, performs both initial assignments, and
reaches the actual internal while-loop head with:

- `n = N`;
- `stones = ref(0)` backed by an empty heap list;
- `i = 0`; and
- the actual return and call-frame continuation.

`PILE-LOOP-SPEC` assumes `N > 0`, `0 <= I <= N`, and a heap list `VS` referenced
by `stones`. It executes the actual loop, actual return, and frame pop. The
result is specifically `ref(0)`, and heap location 0 is specifically:

```text
list(valSeqConcat(VS, pile(N, I)))
```

Here `pile(N,I)` is the finite sequence
`[N+2*I, N+2*(I+1), ..., N+2*(N-1)]`. The returned reference, heap contents,
environment, scopes, stack, return state, and exception state are constrained;
there is no free result variable or tautological implication. The prefix
post-state is exactly a loop pre-state with `I = 0` and `VS = .ValSeq`, so
ordinary transitivity yields the requested entry-to-result partial-correctness
statement. The prefix's existential module-map name does not weaken the result:
module loading and binding selection have already executed, and the loop body
does not read that map.

### Mechanical program identity

I used K's parser and macro expander on both the regenerated `solution.mpy` and
the claim's `pileModule`. The expanded JSON KAST files are byte-identical, both
with SHA-256:

```text
e76044e7294b34bbf785a95085cad3948b56d3b75e2e0975788cc58289af18ba
```

The command and exit 0 are in
[`constructor_identity.log`](evidence/constructor_identity.log). Thus the
claim term is the same `FuncDef` binding and body as the translated submission;
the macros are only constructor aliases.

### Satisfiable preconditions and concrete substitution

`N = 3` in the ordinary initial configuration satisfies the prefix
precondition. The reached loop state `N = 3`, `I = 0`, `VS = []` satisfies the
loop precondition and gives `[3,5,7]`, equal to both trusted canonical Python and
candidate Python. The independent interior witness
`N = 4`, `I = 2`, `VS = [4,6]` gives `[4,6,8,10]`, again equal to both
implementations. Exact states and results are in
[`claim_witness.py`](evidence/claim_witness.py) and
[`claim_witness.log`](evidence/claim_witness.log).

### Body sensitivity

I changed the program term actually executed by the loop claim from `2*i` to
`4*i`, while retaining the required `n+2*i` result. Macro-expanded constructor
comparison then exited 1 (different terms), the mutated definition compiled
successfully, and `kprove` exited 1 on the expected equality between the
`2*i` and `4*i` appended values. This is an execution-body sensitivity check,
not merely an edit to an external source file. Artifacts and logs:

- [`verification-body-mutation.k`](evidence/verification-body-mutation.k)
- [`spec-body-mutation.k`](evidence/spec-body-mutation.k)
- [`body_mutation_kompile.log`](evidence/body_mutation_kompile.log)
- [`body_mutation_constructor.log`](evidence/body_mutation_constructor.log)
- [`body_mutation_kprove.log`](evidence/body_mutation_kprove.log)

**Stage 4 result: PASS.**

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The source inventory covers the assembled `semantics.k`, all 23 helper files
under `semantics/`, `verification.k`, and `spec.k`. The assembled file itself
only requires/imports helper modules and has no local rule sentence. Across the
full source surface, I inventoried:

| Kind | Count |
|---|---:|
| ordinary/equational/macro rules | 704 |
| syntax declarations | 233 |
| evaluation contexts | 5 |
| configuration | 1 |
| target claims | 2 |
| **total** | **945** |

Each entry records its source span, complete normalized sentence, attributes
(`function`, `total`, `symbol`, `no-evaluators`, `priority`,
`simplification`, `macro`, `owise`, `concrete`, strictness), relevance,
decision, and justification. The full inventory and generator are:

- [`rule_inventory.tsv`](evidence/rule_inventory.tsv)
- [`rule_inventory.py`](evidence/rule_inventory.py)
- [`rule_inventory.log`](evidence/rule_inventory.log)

The decisions comprise 91 material supplied-semantics entries, 15
proof-local entries, two target claims, 761 ordinary off-path supplied
entries, three concrete-test Assert entries, 21 LLVM-only entries, six
nonmaterial underspecification entries, and 46 nonmaterial opaque/trust-boundary
entries. No entry is omitted.

### Used-construct map and operational review

| Submitted construct | Declaration and material rules | Review |
|---|---|---|
| `Module`, `FuncDef`, call, return | `syntax.k`; `core.k` load/sequencing/lookup; `functions.k`; `call.k` | The selected closure binding and argument are evaluated, a real frame/scope is created, the real body executes, and return/pop restores every tracked control cell. |
| list literal and `append` | `list.k` list allocation, `core.k` allocation/argument helpers, `call.k` method routing, `list.k` append | The literal allocates `ref(0)`; `append` updates exactly its heap list by concatenating the evaluated element and returns `noneV`, which the expression statement discards. |
| assignment and `i += 1` | strictness in `syntax.k`; `controls.k`; integer `+` in `int.k` | RHS evaluation precedes current-scope update. Cell/ref priority cases are guard-disjoint on this plain integer local. |
| `while i < n` | `controls.k` while/loop-label rules; `operators.k` comparison contexts; integer `<` in `int.k` | The guard is re-evaluated on every iteration; true executes the body and returns to the loop head, false exits. |
| `n + 2*i` | `syntax.k` sequential strictness; `operators.k`; integer `+` and `*` in `int.k` | Left-to-right evaluation and unbounded mathematical integer operations agree with Python on all positive integers; there is no overflow bound. |
| variables/state | `core.k` scopes, lookup, heap, locations, stack, return, exception cells | Every material lookup resolves through the real local/module chain, and all result/control/state effects are represented in the claims. |

Priority overlaps are benign and guard-contained: the list `append` rule
preempts generic method application only for the exact bound method; the
non-mutating receiver-dereference rule rejects `"append"` via
`isMutMethod`; cell assignment/binding rules require a `"$cells"` marker absent
from this frame; and reference arithmetic rules do not match the integer
operands.

### Proof-local extensions

`verification.k` adds no operational bridge and no rule that intercepts a call,
loop, append, return, or other program operation.

- Five constructor macros (`pileCondition`, `pileLoopBody`, `pileBody`,
  `pileClosure`, and `pileModule`) are syntax aliases. The executed module/body
  identity was checked mechanically.
- `pile(N,I)` is a definitional mathematical summary. Its guards `I >= N` and
  `I < N` are disjoint and exhaustive for integers. The recursive branch
  increases `I`, so it reaches the base case. It names the post-state sequence
  and never rewrites program execution.
- `valSeqConcat(VS,.ValSeq) = VS` and right-association of concatenation are
  standard monoid identities. They agree on overlaps with the supplied
  recursive definition and orient toward a terminating normal form.
- There are no proof-local opaque symbols, priority rules, or unconstrained
  result-bearing abstractions.

Accordingly, no connection theorem is missing: no proof-local rule displaces a
fixed-semantics operational region. The body-sensitivity result independently
confirms that claim closure depends on the real append expression.

### Nonmaterial fixed-semantics boundaries

The supplied language is intentionally a minimal Python subset, not a universal
CPython semantics. Its explicit float, sort, keyed-sort, and MD5 opaque symbols
are absent from the expanded submitted term, both claims, and all proof-local
equations. They cannot affect binding, control, state, or result here.

The LLVM compiler reports non-exhaustive-match warnings for `mapStrVS`,
`floorFI`, `toF`, `ceilF`, `joinCodes`, and `valSeqAt`. These are the six
explicit `OFF_PATH_LIMITATION` inventory entries. None is reachable from this
integer/list/function/while program. This is a narrower evidence boundary about
unused language features, not an unsoundness claim about the target theorem;
there is therefore no target-domain false-conclusion witness to report.

I found no rule that encodes this task's answer, fabricates a value for a used
operation, or admits a false conclusion on the intended positive-integer
domain.

**Stage 5 result: PASS.**

## 6. Fresh non-vacuity test

I independently wrote `PILE-AUDIT-VACUITY-SPEC`. It changes the
result-constraining loop postcondition from `pile(N,I)` to `pile(N,I+1)`, thereby
omitting the first element actually appended. The strengthened precondition
includes `I < N`, so the mutation is reachable and false. The satisfying
witness `N = 3`, `I = 0`, `VS = []` has:

```text
actual result:      [3,5,7]
mutated obligation: [5,7]
```

The witness is in
[`vacuity_witness.py`](evidence/vacuity_witness.py) and
[`vacuity_witness.log`](evidence/vacuity_witness.log).

The exact proof command was:

```bash
kprove spec-vacuity-audit.k \
  --definition audit-verification-kompiled \
  --spec-module PILE-AUDIT-VACUITY-SPEC
```

The spec parsed and executed symbolically; `kprove` exited 1 with
`WarnStuckClaimState`, an unexplored-branch warning after the failure, and the
expected unmet equality between the sequence beginning at `I` and the sequence
beginning at `I+1`. This is not a parser error, missing import, timeout, or
unrelated crash. See
[`spec-vacuity-audit.k`](evidence/spec-vacuity-audit.k) and
[`vacuity_kprove.log`](evidence/vacuity_kprove.log).

**Stage 6 result: PASS.**

## 7. Proven versus assumed accounting

### What is formally established

Under the supplied MPY definition, the two successful reachability claims
establish partial correctness for every `N:Int` satisfying `N > 0`:

1. real module loading and the real submitted call reach the exact initialized
   loop state; and
2. from that loop state, if execution terminates, it returns `ref(0)` with heap
   location 0 containing exactly
   `[N, N+2, ..., N+2*(N-1)]`, with no exception and the caller control state
   restored.

The two configurations match exactly at the composition point. This covers the
unrestricted source-contract domain; it is not a finite unrolling or
fixed-size theorem.

### Trust ledger

| Boundary | Influence and dependents | Assessment |
|---|---|---|
| K parser/compiler, reachability logic, Haskell backend, SMT solver, and hooked `Int`/`Bool`/`Map`/`List` operations | All proof execution and mathematical side conditions | Standard low-level trusted computing base; versions are recorded and fresh builds succeeded. |
| Trusted `py2mpy.py` | Source-to-constructor bridge | Acceptable: candidate copy matches trusted input, regeneration is byte-identical, and expanded claim/program KASTs match. |
| Supplied MPY operational semantics | Meaning of the submitted `.mpy` term | Acceptable for this theorem: integrity matches the trusted tree and every material rule/state effect was statically reviewed. |
| K compiler-generated heating/cooling from `strict`/`seqstrict` | Evaluation order for expressions and RHS/return evaluation | Acceptable fixed-semantics machinery; relevant declarations are inventoried and agree with the program's left-to-right order. |
| `pile` | Mathematical post-state sequence | Not an oracle or trusted primitive: it has complete, truthful, terminating equations and does not replace execution. |
| Reachability transitivity between the two proved claims | Entry-to-final composition | Ordinary proof meta-theory; the intermediate configurations and side conditions match mechanically. |
| Float/sort/MD5 and the six incomplete fixed helpers | None; no target claim or used rule depends on them | Explicitly excluded, nonmaterial trust/coverage boundaries. |
| Trusted canonical Python and differential tests | Empirical source-intent/implementation bridge only | 325-case finite support with zero mismatches; not used to close either K claim. |

The proof does not establish behavior for `N <= 0`, non-integer arguments,
arbitrary unused Python constructs, or full CPython exception behavior. Those
are outside the prompt's positive-integer contract. As requested, the result is
partial correctness; it does not separately claim a K-level termination
theorem.

Gate A (real-program soundness and non-vacuity), Gate B (intent adequacy), and
Gate C (trust/evidence auditability) all pass. There is no material domain
narrowing, substituted program, result oracle, or proof-local semantic
unsoundness.

**Stage 7 result: PASS.**

VERDICT: PASS
LEGITIMACY: LEGIT
