# Independent adversarial audit: 26-remove-duplicates

This review treats every candidate artifact as untrusted and uses the supplied
semantics boundary requested for `SUPPLIED_SEMANTICS`. All execution was from a
source-only copy below `/tmp/audit-work/26-remove-duplicates`; no
candidate-built definition or cache was present or reused. K was
`v7.1.337`.

## 1. Input and provenance integrity

The rendered mode and trusted mounts agree. `/reference/reference-semantics`
exists. A recursive `diff --no-dereference -r` against
`/candidate/reference-semantics` exited 0, every candidate semantics entry has
the same regular-file/directory type as the trusted tree, and the candidate
tree contains no symlink. Thus there is no infrastructure breach and no
candidate semantics integrity failure. See
[01-inventory-and-mode-rerun.log](evidence/01-inventory-and-mode-rerun.log).

The candidate prompt and translator are regular files and byte-identical to
their trusted counterparts:

- `prompt.py`: SHA-256
  `7823eea9be9599563c786fa16e792f3da2482016607d75ee06ca40b2d33c7dca`.
- `py2mpy.py`: SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.

The candidate's `solution.py`, `solution.mpy`, `spec.k`, `verification.k`,
`prove.sh`, and concrete-test files are regular files; there are no candidate
symlinks anywhere in the submitted tree. The complete types, hashes, diffs,
and source dump are in
[02-provenance-and-sources.log](evidence/02-provenance-and-sources.log).

Four named provenance artifacts are missing:
`/candidate/run-input.json`, `/candidate/metrics.json`,
`/candidate/codex-last.txt`, and `/candidate/codex-output.log`. No structured
generation trace is present. Consequently, there is no generation chronology,
metrics record, or final-generation report to corroborate or contradict. This
does not substitute for or invalidate the fresh proof reconstruction, but it
is a real provenance/auditability limitation.

The first inventory wrapper in
[01-inventory-and-mode.log](evidence/01-inventory-and-mode.log) exited 2 before
performing checks because `script` invoked `sh`, where `set -o pipefail` was
unsupported. The corrected Bash rerun above exited 0. This was a reviewer
wrapper error, not candidate or infrastructure evidence.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementation

For every finite `List[int]`, return a new list containing exactly those input
elements whose value occurs exactly once in the whole original list, retaining
their original relative order. For example, `[1, 2, 3, 2, 4]` becomes
`[1, 3, 4]`. This is the common meaning of the trusted prompt and the trusted
canonical `Counter`/list-comprehension implementation.

The submitted implementation loops over the original list and appends a value
to a fresh result list exactly when `numbers.count(value) == 1`. On the stated
integer-list domain this is the same algorithmic predicate. Its quadratic
complexity is irrelevant to functional partial correctness.

### Translation identity

I regenerated the MPY program from the submitted Python with the trusted
translator. The regenerated and submitted files are byte-identical, both with
SHA-256
`28e2c81f975de56588d6d8da06d0630811bd0846298e9451cacf91ea6474850e`.
The translator and `cmp` both exited 0. See
[03-translation-and-differential.log](evidence/03-translation-and-differential.log).

### Independent differential evidence

The independent script
[03-differential.py](evidence/03-differential.py) imports the trusted canonical
entry point and submitted entry point separately and also uses a direct
contract oracle. Its input manifest is
[03-differential-inputs.json](evidence/03-differential-inputs.json). It covers:

- the documented example, empty and singleton lists;
- count-one versus count-two/greater branch boundaries, repeated runs, and
  order-sensitive placements;
- signed 64-bit endpoints and much larger positive/negative Python integers;
- every list of length 0 through 6 over `[-2, -1, 0, 1, 2]` (19,531 inputs);
- 2,000 deterministic, duplicate-heavy generated lists of length up to 40.

All 21,546 comparisons agreed; mismatch count was zero and the command exited
0. This is finite evidence for the Python-to-contract bridge, not a replacement
for the K proof.

## 3. Clean proof reconstruction

The scratch source tree was copied before any build. The submitted candidate
contained no kompiled definition or cache. I freshly built:

1. the supplied semantics with LLVM using main module `MPY-KRUN` and syntax
   module `MPY-SYNTAX`; exit 0
   ([04-kompile-llvm.log](evidence/04-kompile-llvm.log));
2. the proof definition with Haskell using main module
   `REMOVE-DUPLICATES-VERIFICATION` and syntax module `MPY-SYNTAX`; exit 0
   ([04-kompile-haskell.log](evidence/04-kompile-haskell.log)).

The LLVM compiler emitted non-exhaustiveness warnings for several unrelated
helpers (`mapStrVS`, float conversions, `joinCodes`, and out-of-bounds
`valSeqAt`). None occurs on this program's proof path. The Haskell build emitted
only unused-variable warnings in the supplied string comparison rules.

The submitted concrete assertions were re-executed on the fresh LLVM
definition and exited 0
([04-krun-concrete.log](evidence/04-krun-concrete.log)).

Every positive proof target was selected separately. The loop claim was proved
without trust; the entry claims use the already independently proved loop
claim as a trusted lemma for that invocation, matching the candidate's intended
two-phase proof:

| Claim | Reconstruction | Result |
|---|---|---|
| `loop-invariant` | `kprove ... --claims REMOVE-DUPLICATES-SPEC.loop-invariant` | exit 0, `#Top` |
| `entry-empty` | selected alone with the loop label trusted | exit 0, `#Top` |
| `entry-keep` | selected together with the loop claim, with only the loop label trusted | exit 0, `#Top` |
| `entry-drop` | selected together with the loop claim, with only the loop label trusted | exit 0, `#Top` |

The completed logs are
[05-kprove-loop-invariant.log](evidence/05-kprove-loop-invariant.log),
[05-kprove-entry-empty.log](evidence/05-kprove-entry-empty.log),
[05-kprove-entry-keep.log](evidence/05-kprove-entry-keep.log), and
[05-kprove-entry-drop.log](evidence/05-kprove-entry-drop.log).

There was one reviewer-command correction. My first parallel nonempty commands
selected only the entry label and also named the loop label under `--trusted`.
In this K frontend, `--claims` filtering removed the loop claim before it could
be retained as the trusted lemma, causing open-ended symbolic unrolling. I
identified this from the emitted `spec.kore`, attempted to terminate those
reviewer-launched sibling-namespace backends, and preserved the superseded
artifacts as
`05-superseded-entry-{keep,drop}-filtered-without-loop.log` plus
[05-superseded-filtered-runs-termination.log](evidence/05-superseded-filtered-runs-termination.log).
The sandbox could inspect but not signal sibling PID namespaces. These runs are
not proof or timeout evidence. The corrected independent commands selected the
pair `loop-invariant,entry-{keep|drop}` and marked only `loop-invariant`
trusted; each then closed in about six seconds. The exact corrected commands
are in [COMMANDS.md](evidence/COMMANDS.md).

## 4. Adequacy and real-program pinning

### Claims in plain language

- `loop-invariant`: in a local frame where `numbers` is the immutable bare-list
  representation `ALL`, `result` points to heap list `ACC`, and the remaining
  iterator is `REST`, executing the exact loop body transforms that heap list
  to `ACC` followed by every element of `REST` whose count in `ALL` is one.
  Other framed heap/scope state is preserved and execution resumes at the
  arbitrary continuation. Both `ALL` and `REST` must contain only integers.
- `entry-empty`: calling the exact function closure on the empty list from the
  canonical initial scope/heap returns reference 0, whose newly allocated heap
  object is the empty list.
- `entry-keep`: for a nonempty all-integer input `V :: REST` where the total
  count of `V` is one, the first iteration keeps `V`; the returned heap list is
  `keepSinglesAcc([V], REST, V :: REST)`.
- `entry-drop`: for a nonempty all-integer input `V :: REST` where the total
  count of `V` is not one, the first iteration drops `V`; the returned heap
  list is `keepSinglesAcc([], REST, V :: REST)`.

The empty/cons split is exhaustive for `ValSeq`, and the equality/not-equality
guards on the first value are complementary. The output is not free: each
entry returns the specific `ref(0)` and fixes the heap content at 0 to a
recursive result term. That term appends an element if and only if its original
total count is one.

### Real submitted body

The entry `<k>` cell calls a macro that expands to a normal fixed-semantics
`closureVal`; it does not replace a call with an answer. The closure executes
ordinary `Assign`, `For`, `If`, `Call`, `append`, and `Return` rules. I parsed
both the actual submitted `solution.mpy` and expanded macro with `kast` from the
fresh proof definition. The parameter ASTs are equal, the complete body ASTs
are equal, and both body encodings have SHA-256
`de10b3f96a6fb4a2e353ff0817c25052f226c0c4fa145e6229172699063e8121`.
The defining scope is module scope 0. See the independent checker
[07-kast-program-pinning.py](evidence/07-kast-program-pinning.py) and
[07-kast-program-pinning.log](evidence/07-kast-program-pinning.log).

The claims start at function invocation rather than replaying the harmless
module-level `from typing import List` and `FuncDef`. Under the supplied
semantics that import is a no-op and executing the `FuncDef` creates exactly
the checked closure at scope 0. This is an invocation theorem for the actual
translated function body, not a substituted program.

The input is represented as the supplied semantics' bare read-only list value.
Concrete list constructors normally allocate a reference, but the fixed
semantics expressly supports bare lists for read-only claim inputs. This
function never mutates or returns `numbers`, and the `For` and nonmutating
`count` paths observe the same `ValSeq`; output `result` is separately allocated
and mutated by reference. No alias-sensitive behavior is omitted.

### Satisfiable states and ground substitution

The independent witness script
[07-claim-witnesses.py](evidence/07-claim-witnesses.py) supplies one realizable
state for every claim:

- loop: `ALL=[1,2,2,3]`, `REST=[2,2,3]`, `ACC=[1]`, giving `[1,3]`;
- empty entry: `[]`, giving `[]`;
- keep entry: `[1,2,2,3]`, giving `[1,3]`;
- drop entry: `[1,1,2]`, giving `[2]`.

All preconditions evaluate true, and each claimed concrete result agrees with
both trusted and submitted Python implementations. The command exited 0; see
[07-claim-witnesses.log](evidence/07-claim-witnesses.log).

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[06-rule-inventory.txt](evidence/06-rule-inventory.txt) enumerates, with file
and source line, all 231 syntax-declaration starts, 702 rules, four claims, five
contexts, the configuration, 45 priority sites, 116 total declarations, all
three simplification rules, macros, guards, and attributes. The complete
numbered K source used for the audit is preserved in
[06-full-numbered-k-sources.txt](evidence/06-full-numbered-k-sources.txt).
The generator and its command log are
[06-build-rule-inventory.sh](evidence/06-build-rule-inventory.sh) and
[06-inventory-command-rerun.log](evidence/06-inventory-command-rerun.log).
There are no `[functional]` declarations; every `[function]`, `[total]`,
priority, `owise`, macro, simplification, symbol, and `no-evaluators`
attribute is present in that inventory and the numbered source.

The following table assigns every inventoried rule/declaration to a reviewed
file group. Counts and attribute totals are independently recorded in
[06-per-file-counts.log](evidence/06-per-file-counts.log).

| File | Syntax / rules | Review disposition |
|---|---:|---|
| `semantics.k` | 0 / 0 | Assembly only: `MPY` imports the fixed proof modules; `MPY-KRUN` additionally imports concrete-only rules. |
| `assert.k` | 0 / 3 | Only runtime tests use it; true assertions continue and false assertions set the modeled exception/exit. No proof claim depends on it. |
| `bool.k` | 0 / 13 | Guarded Boolean operator/truthiness cases; compatible with the Boolean produced by integer equality. No conflicting used-path overlap. |
| `builtins.k` | 38 / 137 | Only `isIntV` is proof-relevant: Int gives true and the `owise` Val case gives false. Opaque MD5 and other builtins are unreachable. |
| `call.k` | 3 / 21 | Relevant call route evaluates callee then arguments left-to-right, retains refs for mutators, dereferences a ref receiver for `count`, and creates/restores an ordinary closure frame. Priority guards separate these cases. |
| `comprehension.k` | 3 / 7 | Unused syntax/macros/rules; none unifies with the submitted AST. |
| `concrete.k` | 5 / 16 | Imported only by `MPY-KRUN`, not the proof definition; exercised by fresh concrete tests. |
| `controls.k` | 3 / 34 | Relevant assignment, `If`, `For`, loop step, and list-input dereference preserve ordering and state. Loop-control/while/import alternatives are either disjoint or unused. |
| `core.k` | 37 / 46 | Configuration, values, module/frame scopes, name lookup, left-to-right argument/list evaluation, allocation, literals, and sequence helpers match the used execution. Fresh allocation at heap 0 and framed state explain the exact entry posts. |
| `dict.k` | 12 / 28 | Unused; dict constructors cannot unify with any value/operation on the proof path. |
| `float.k` | 34 / 121 | Unused. All float symbols and rules, including opaque ones, are unreachable from `allInts` inputs and the submitted AST. |
| `functions.k` | 4 / 15 | Relevant plain parameter binding, return, and pop rules preserve result, caller continuation, stack, environment, and allocation state. Annotated closures are disjoint and unused. |
| `int.k` | 1 / 16 | Relevant `applyCmp("==", Int, Int)` is exact unbounded integer equality. Other operator-name cases are disjoint. |
| `iter.k` | 1 / 0 | Declares the iterator protocol terms used by list/loop rules; no independent equations. |
| `list.k` | 5 / 27 | Relevant list iteration, empty-list construction, concatenation, and priority-40 `append` are exact. `append` writes only the result heap object and returns `noneV`. |
| `methods.k` | 27 / 75 | Relevant `list.count` delegates to total `cntOccVS`; base/cons rules descend and equality/not-equality guards partition integer values. All string helpers are constructor-disjoint. |
| `operators.k` | 0 / 10 | Comparison contexts enforce left then right evaluation; used integer equality dispatches to `int.k`. Ref-deref priorities are sound and do not intercept integer elements. |
| `range.k` | 2 / 6 | Unused constructor-specific iterator/math rules. |
| `set.k` | 6 / 12 | Unused constructor-specific rules. |
| `sort.k` | 6 / 19 | Unused; both opaque sorting symbols and priority sort rules are unreachable. |
| `str.k` | 5 / 28 | Unused except fixed namespace availability; string constructors do not overlap integer/list used terms. |
| `subscript.k` | 15 / 40 | Unused; no `Subscript` occurs in the submitted AST. |
| `syntax.k` | 16 / 0 | Declares every submitted constructor. Relevant strictness is RHS-first assignment, iterable-before-loop, condition-before-branch, expression-before-return, and receiver-before-attribute. |
| `tuple.k` | 4 / 21 | The `#bindTgt(Name,V)` rule is relevant and updates only the loop variable in the current frame. Tuple alternatives are constructor-disjoint. |
| `verification.k` | 4 / 7 | Fully analyzed individually below. |
| `spec.k` | 0 / 0 plus 4 claims | Claims are analyzed in Sections 3–4; no semantic rule is declared here. |

The supplied tree contains 22 `no-evaluators` opaque declarations: float
operations/conversions, `sortVS`, `sortKeyVS`, and `md5hexCodes`. None can
influence control, heap, return value, summary, or postcondition for this
integer/list-only program. There is no proof-local opaque symbol.

### Used construct map and state/control review

The submitted AST's relevant chain is:

`closureVal` call → parameter bind → fresh empty `ListExpr` allocation →
assignment to `result` → evaluate `numbers` → list loop → bind `number` →
evaluate `numbers.count(number)` → integer equality with 1 → branch → optional
priority-preserving heap `append` → next iterator tail → `Return` → frame pop.

Each link has a fixed rule listed in the inventory. The call rules preserve the
caller continuation and stack; allocation changes only `<heap>`/`<heapLoc>`;
lookup and assignment use the current local scope; list iteration consumes the
tail in order; `count` reads `ALL` without mutation; `append` changes only the
result object's list; return restores the caller state and returns the same
reference. No exception, output, or hidden allocation is on this path.

The priority rules on the path are not proof shortcuts. In particular,
mutating-method dispatch retains `ref(H)` so `append` can update heap `H`,
whereas nonmutating `count` dereferences the receiver to its list value. The
guards are complementary through `isMutMethod`. Generic call/operator rules are
`owise` or lower priority and agree after the intended dereference; no priority
rule fabricates a result or skips the function body.

### Every proof-local declaration/rule

1. `allInts : ValSeq -> Bool` is a total definitional predicate. `.ValSeq`
   gives true; `vCons(V,REST)` gives `isIntV(V) and allInts(REST)`. The
   constructors are exhaustive/disjoint and recursion strictly descends.
2. `keepSinglesAcc : ValSeq × ValSeq × ValSeq -> ValSeq` is a total
   definitional summary, not an operational bridge. Empty `REST` returns
   `ACC`. On a head, the `cntOccVS(ALL,V)==1` case appends `V`; its Boolean
   negation case does not. Guards are exhaustive and disjoint, both recursive
   calls strictly descend on `REST`, and `valSeqConcat` is the ordinary
   append-to-accumulator definition. The `[simplification]` annotations add no
   false equality.
3. `#removeDuplicatesBody` is a macro only. Expansion is the exact translated
   loop body; it never rewrites a running computation to a summary.
4. `#removeDuplicatesClosure` is a macro only. It expands to the exact
   parameter/body AST in defining scope 0 and then executes through the fixed
   call semantics. The KAST pinning check establishes exact structural
   identity.

There are no proof-local ordinary operational rules, priority rules, opaque
symbols, or result-bearing oracles. Nothing encodes the answer in an
execution-bypassing rule. I found no materially unsound rule on the complete
intended-domain execution path and therefore make no unsupported unsoundness
claim or false-conclusion witness.

## 6. Fresh non-vacuity test

There was no candidate `spec-vacuity.k` to trust. I created
[08-spec-vacuity.k](evidence/08-spec-vacuity.k) in scratch as a fresh mutation
of the empty entry: it leaves the actual call and all initial cells unchanged
but requires the returned heap object to be `[0]` instead of `[]`. The empty
input satisfies the original precondition, and both Python implementations
demonstrably return `[]`, so the mutation is meaningfully false.

`kprove --dry-run` on the mutation exited 0, proving it parsed and built against
the fresh definition. The real proof then exited 1 with
`WarnStuckClaimState`. The residual is the expected completed execution:
`<k> ref(0) ~> .K </k>` and heap `0 |-> list(.ValSeq)`, which cannot unify with
the false `[0]` target. This is an unmet result obligation, not a parser error,
timeout, unreachable mutation, or unrelated crash. Exact command, statuses,
and bounded residual are in
[08-vacuity-build-and-proof.log](evidence/08-vacuity-build-and-proof.log).

## 7. Proven versus assumed accounting

Subject to the fixed supplied MPY semantics and K toolchain, the reconstructed
reachability proof establishes: for every finite MPY `ValSeq` consisting only
of `Int` values, a call to the exact submitted `remove_duplicates` closure from
the stated initial configuration, if it terminates, returns a fresh list
containing in original order precisely the values whose total occurrence count
in the original input is one. The proof also constrains the returned reference,
heap content, frame restoration, absence of modeled exception, and exit code.

Trust/assumption ledger:

- **K implementation and mathematical hooks:** K parsing/kompilation,
  Haskell/LLVM backends, built-in unbounded Int/Bool/Map/List/K-equality hooks,
  and reachability/circularity machinery are foundational trusted primitives.
  They affect all claims and were exercised by clean build/proof/mutation runs,
  but are not proved inside this submission.
- **Supplied MPY semantics:** the fixed semantics is the theorem's operational
  model. Its candidate copy is exactly the trusted mount. I statically audited
  all declarations/rules and the complete used path. Language features not
  used here have no dependent proof term; the 22 opaque symbols are explicitly
  outside the dependency cone.
- **Loop lemma:** entry proofs pass `loop-invariant` via `--trusted` only after
  that exact claim independently exited 0 with `#Top`. It is a discharged
  separately checked lemma, not an unproved external oracle.
- **Proof-local mathematics:** `allInts`, `keepSinglesAcc`, and their
  simplifications are assumed as equations in the proof definition. Their
  exhaustive, disjoint, descending definitions are ordinary mathematics and
  were checked rule by rule. They summarize the result but never replace
  operational execution.
- **Program identity bridge:** the formal claim embeds a closure macro rather
  than reading `solution.mpy` at proof time. Exact trusted translation and an
  independent KAST structural comparison establish that its parameter/body and
  defining scope are exactly those of the submitted function. This bridge is
  machine-checked structural evidence, not a separate reachability theorem.
- **Intent bridge:** interpreting `cntOccVS == 1` as “occurs exactly once” and
  recursive accumulator concatenation as stable filtering is a direct
  mathematical reading of the definitions. The 21,546-case independent
  differential run supports, but does not universally prove, the Python
  canonical/candidate bridge.
- **Opaque/trusted values:** no opaque float, sort, or MD5 value reaches a
  branch, state update, return, summary, or postcondition. There is no
  proof-local opaque value.

Excluded from the theorem are non-integer elements, Python `bool` values
(modeled separately from `Int`), concurrent/external mutation of the input,
resource exhaustion, performance, and behavior outside the supplied MPY
subset. These exclusions agree with the prompt's `List[int]` functional
contract.

The final integrity, positive-log, mutation-log, evidence-link, and exact
terminator checks all passed; see
[09-final-validation.log](evidence/09-final-validation.log).

The proof itself is sound, result-constraining, and pinned to the real generated
function. The missing four provenance artifacts prevent a fully auditable
generation record, so the appropriate completed-audit category is
`CONCERNS / LEGIT` rather than `PASS / LEGIT`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
