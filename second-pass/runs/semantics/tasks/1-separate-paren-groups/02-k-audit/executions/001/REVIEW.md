# Independent adversarial review: 1-separate-paren-groups

## Overall decision

The candidate contains a legitimate, non-vacuous partial-correctness proof under
the supplied MPY semantics. The proof executes the submitted function body,
constrains the returned heap object to a recursively defined list of separated
groups, and survives clean reconstruction. I found no unsound proof-local rule,
operational bridge, result oracle, or free-result postcondition.

The result is `CONCERNS / LEGIT`, rather than `PASS / LEGIT`, for evidence and
intent-bridge limitations:

1. The candidate omitted all four requested generation/provenance records
   (`run-input.json`, `metrics.json`, `codex-last.txt`, and `codex-output.log`)
   and supplied no structured generation trace.
2. The K theorem connects execution to the task-specific structural fold
   `scanGroups`. The further statement that this fold is exactly the
   natural-language notion of separating all balanced top-level groups is
   justified by the equations, ground witnesses, and differential testing, but
   is not a separate K theorem.
3. The formal theorem deliberately covers balanced strings over exactly space,
   `(`, and `)`, in a fresh module-call state. The trusted canonical function and
   the candidate differ on non-space, non-parenthesis characters, which are
   outside that formal and intended domain.

These limitations do not enable a false conclusion on any state satisfying an
entry precondition.

## 1. Input and provenance integrity

### Mode boundary

The rendered mode is `SUPPLIED_SEMANTICS`, and
`/reference/reference-semantics` is present. I recursively compared entry type
and SHA-256 digest for the complete candidate and trusted semantics trees:

- both trees contain 25 entries;
- every relative entry has the same type and content;
- neither tree contains a symlink;
- there are no missing, additional, changed, or mistyped semantics entries.

The trusted mount is therefore consistent with the rendered mode. This is not
an infrastructure breach. The complete manifest and comparison are in
`evidence/stage1/provenance.log`; the check is implemented by
`evidence/stage1/check_provenance.py`.

The candidate `prompt.py` and `py2mpy.py` are regular files and byte-identical
to the trusted versions:

| Artifact | SHA-256 |
|---|---|
| prompt, trusted and candidate | `ba4d0641a184fb3cdd632060a25d6408a7e91fe9d79b5c341407e74b80536327` |
| translator, trusted and candidate | `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16` |

The required proof sources `solution.py`, `solution.mpy`, `spec.k`, and
`verification.k` are also regular files, not symlinks. Candidate-built
`__pycache__`, output files, and claimed `#Top` logs were not copied into the
scratch build and were not used as proof evidence.

### Missing provenance artifacts

The following are all absent:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`
- any candidate filename containing `trace`

The candidate did provide `proof-invariant.out`,
`proof-entry-and-examples.out`, and `concrete-run.out`. I read them only as
untrusted claims. Their contents did not affect reconstruction or the verdict.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

The trusted prompt asks for a function that accepts a string made of separate,
balanced parenthesis groups, possibly containing spaces, removes the spaces,
and returns each top-level balanced group as a separate string. Nested
parentheses may occur inside one group; one top-level group is not part of
another. The documented input
`"( ) (( )) (( )( ))"` must yield
`["()", "(())", "(()())"]`.

The trusted canonical implementation scans characters, tracks nesting depth,
appends only `(` and `)` to the current group, emits a group whenever depth
returns to zero, and ignores every other character. The submitted implementation
uses the same depth-and-buffer strategy on the intended alphabet. It explicitly
skips spaces and treats every other non-`(` character as a close parenthesis.
Consequently it agrees on the intended alphabet, but not on arbitrary strings
containing tabs, letters, or newlines.

### Translation identity

I ran the trusted translator directly on the submitted source:

```text
python3 /reference/py2mpy.py /candidate/solution.py \
  > /tmp/audit-work/clean/solution.regenerated.mpy
cmp /candidate/solution.mpy \
    /tmp/audit-work/clean/solution.regenerated.mpy
```

Both commands exited 0. Both MPY files have SHA-256
`a64520e2af51bed55082d485b79af9013718e530b6eb464db44cd90ff0a39144`.
See `evidence/stage2/translator-byte-identity.log`.

### Independent differential test

`evidence/stage2/differential.py` independently imports
`/reference/canonical.py` and `/candidate/solution.py`. It also uses a third,
grammar-based oracle that rejects characters outside space and parentheses and
checks balance itself.

The preserved input set contains:

- the prompt example;
- empty, spaces-only, one-group, adjacent-group, nesting, and leading/trailing
  space boundaries;
- every balanced parenthesis word through four pairs, with every placement of
  zero or one space at every gap;
- 1,000 deterministic generated balanced cases containing up to eight groups,
  deeper nesting, and runs of spaces.

There were 8,763 distinct intended-domain cases and zero mismatches among the
oracle, trusted canonical function, and submitted function. The complete cases
and results are in `evidence/stage2/differential-inputs.jsonl`, whose SHA-256
reported by the run is
`087ed4ce9084c6608f29a845dc320bd6ce5cb0439ef5a17d7d9c2cbec02adf26`.
The exact command, count, and exit status 0 are in
`evidence/stage2/differential.log`.

The same run deliberately recorded four out-of-domain probes:

| Input | Canonical | Candidate |
|---|---|---|
| `"\t()"` | `["()"]` | `["\t("]` |
| `"a()"` | `["()"]` | `["a("]` |
| `"(x)"` | `["()"]` | `["(x"]` |
| `"(\n)"` | `["()"]` | `["(\n"]` |

Those divergences are real but do not satisfy the K entry precondition and are
not described as valid inputs by the parenthesis-group contract. They are an
explicit theorem-scope limitation, not a witness against a proved rule.

## 3. Clean proof reconstruction

### Scratch isolation and toolchain

I created `/tmp/audit-work/clean`, copied only candidate source proof artifacts,
copied the trusted translator and trusted supplied semantics, and did not copy
candidate compiled definitions, caches, or logs. The independently installed
tools were:

```text
K version: v7.1.337
Build date: Thu Jun 18 07:59:56 CDT 2026
```

`kup` is absent, but `/usr/bin/kompile` and `/usr/bin/kprove` are installed and
both report that version. See `evidence/stage3/toolchain.log`.

Fresh LLVM and Haskell builds both exited 0:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled --warnings none

kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled --warnings none
```

The bounded logs are `evidence/stage3/kompile-llvm.log` and
`evidence/stage3/kompile-haskell.log`.

### Fresh concrete reconstruction

I wrote `evidence/stage3/concrete_audit.py` with the exact submitted function
body and independent assertions for empty, spaces-only, single, adjacent,
spaced, and deeply nested inputs. The trusted translator produced
`evidence/stage3/concrete_audit.mpy`. Fresh `krun` execution under the LLVM
definition exited 0, ended with `.K`, `NoExc`, an empty stack, and the expected
heap lists. See `evidence/stage3/concrete-run.log`.

### Every positive proof claim

The universal loop claim was proved first without trust. Each dependent claim
was then selected together with that invariant, with only the already-proved
invariant marked trusted. This is modular use of a separately established
claim, not an unproved axiom.

| Claim | Fresh result | Evidence |
|---|---|---|
| `all-balanced-inputs` | exit 0, `#Top` | `evidence/stage3/prove-all-balanced-inputs.log` |
| `all-balanced-calls` | exit 0, `#Top` | `evidence/stage3/prove-all-balanced-calls.log` |
| `empty` | exit 0, `#Top` | `evidence/stage3/prove-empty.log` |
| `prompt-example` | exit 0, `#Top` | `evidence/stage3/prove-prompt-example.log` |
| `adjacent-and-spaced` | exit 0, `#Top` | `evidence/stage3/prove-adjacent-and-spaced.log` |
| `deep-nesting` | exit 0, `#Top` | `evidence/stage3/prove-deep-nesting.log` |

The candidate's exact combined selection was also independently rerun and
returned exit 0 with `#Top`; see
`evidence/stage3/prove-entry-and-examples-combined.log`.
`evidence/stage3/proof-summary.log` records all six per-claim statuses.

One diagnostic command initially selected only `all-balanced-calls` while
naming the filtered-out invariant as trusted. That invocation made no progress
and I interrupted it; it is preserved as
`evidence/stage3/attempt-filtered-public-interrupted.log`. Retaining both labels
in `--claims`, while marking the invariant trusted, closed promptly. The
interrupted diagnostic is not counted as proof or as candidate failure.

The clean reconstruction gate passes.

## 4. Adequacy and real-program pinning

### Claims in plain language

`all-balanced-inputs` is the loop invariant. Its precondition says:

- execution is exactly at the submitted function's `#loop` head, with the
  submitted target and body and an arbitrary continuation `KONT`;
- `CODES` is a remaining suffix containing only spaces and parentheses;
- processing it from `DEPTH` never underflows and ends at depth zero;
- `DEPTH` is nonnegative, and a depth-zero partial state has an empty `CUR`;
- local variables contain `CUR`, `DEPTH`, a heap reference `H` for accumulated
  groups, the original input, and any old character value.

Its postcondition consumes the loop, leaves `KONT`, resets `current` and
`depth` to empty and zero, existentially allows the final loop-character value,
and changes the list at heap address `H` from `ACC` to
`scanGroups(CODES, CUR, DEPTH, ACC)`.

`all-balanced-calls` is the public entry theorem. Its precondition is an exact
fresh module state containing the submitted closure, a string argument whose
codes satisfy `balancedTail(CODES, 0)` and `parenSpaceOnly(CODES)`, an empty
heap, empty call stack, `noRet`, and `NoExc`. Its postcondition fixes:

- the returned value to `ref(0)`;
- heap address 0 to
  `list(scanGroups(CODES, .IntSeq, 0, .ValSeq))`;
- `heapLoc` to 1;
- the stack, return state, and exception state to their clean values.

The four remaining claims are ground instances for empty input, the prompt
example, adjacent/spaced groups, and deep nesting. Each fixes both the returned
reference and its complete list contents. There is no free output variable,
tautological implication, or merely one-way property.

### Satisfiable preconditions and ground substitution

`evidence/stage4/claim_witnesses.py` exhibits a complete loop-head witness:

```text
CODES = ") ()"
CUR = "("
DEPTH = 1
ACC = ["seed"]
H = 7
```

with `env = 1`, the required local bindings and normal module/builtins scopes,
and heap `7 |-> list(["seed"])`. All four invariant guards are true, and the
claimed post-list is `["seed", "()", "()"]`.

The same artifact exhibits a satisfying input for every entry/example claim.
For the universal entry it uses `"() (()) (()())"`. For every ground
substitution, the `scanGroups` result, trusted Python result, and submitted
Python result are identical. The script exits 0 with `mismatch_count=0`; see
`evidence/stage4/claim-witnesses.log`.

### Actual submitted program

The entry claims begin from a closure rather than from the outer `Module` node,
so I checked both halves of the pin:

1. The trusted translation is byte-identical to submitted `solution.mpy`
   (stage 2).
2. `solutionClosure` expands to the exact normalized `FuncDef` body: the same
   assignments, `For`, space `Continue`, string accumulation, depth updates,
   append/reset branch, and return.

For an executable check, `evidence/stage4/make_pinning_spec.py` first requires
the already-recorded submitted MPY digest, then emits the same AST using the
explicit empty-list terminators required by K's inner claim parser. The fresh
claim loads that complete `Module` through `#loadAll` and requires the resulting
scope binding to be exactly `solutionClosure`. It returns exit 0 and `#Top` in
`evidence/stage4/pinning-proof.log`.

The first spelling used external-parser abbreviations such as `ListExpr()`,
which K's inner claim parser rejects. That parser-only attempt is transparently
preserved in `evidence/stage4/pinning-proof-attempt1.log`; it was replaced by
the equivalent normalized AST, not treated as evidence.

This establishes that the closure executed in the positive claims is the real
submitted program body. The irrelevant `from typing import List` is executed
by the supplied semantics' ordinary non-math-import no-op rule.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/stage5/inventory_k.py` inventories every declaration and rule-like
sentence in the trusted supplied semantics and `verification.k`, retaining
source location, full normalized text, and attributes. The resulting
`evidence/stage5/k-inventory.jsonl` contains 1,109 entries:

- 708 `rule` entries;
- 232 `syntax` entries;
- 1 configuration;
- 5 evaluation contexts;
- 24 `requires`, 87 imports, 26 modules, and 26 endmodules.

`evidence/stage5/classify_inventory.py` assigns an explicit disposition to each
entry. `evidence/stage5/k-dispositions.jsonl` reports 1,109 classified entries
and zero review gaps. The supplied semantics entries are accepted as the exact
selected operational definition, not as candidate proof extensions. Rules in
construct families unreachable from this program are explicitly marked
unreachable; they cannot rewrite a term on the program/proof path.

Per-file declaration/rule counts are:

| File | Syntax | Rules | Other semantic items |
|---|---:|---:|---|
| `semantics.k` | 0 | 0 | assembly modules/imports |
| `syntax.k` | 16 | 0 | source AST syntax |
| `core.k` | 37 | 46 | configuration |
| `iter.k` | 1 | 0 | iterator protocol syntax |
| `range.k` | 2 | 6 | — |
| `operators.k` | 0 | 10 | 2 contexts |
| `int.k` | 1 | 16 | — |
| `bool.k` | 0 | 13 | 1 context |
| `float.k` | 34 | 121 | — |
| `str.k` | 5 | 28 | — |
| `set.k` | 6 | 12 | — |
| `list.k` | 5 | 27 | — |
| `tuple.k` | 4 | 21 | — |
| `subscript.k` | 15 | 40 | 2 contexts |
| `comprehension.k` | 3 | 7 | — |
| `methods.k` | 27 | 75 | — |
| `controls.k` | 3 | 34 | — |
| `functions.k` | 4 | 15 | — |
| `builtins.k` | 38 | 137 | — |
| `call.k` | 3 | 21 | — |
| `sort.k` | 6 | 19 | — |
| `assert.k` | 0 | 3 | — |
| `dict.k` | 12 | 28 | — |
| `concrete.k` | 5 | 16 | — |
| `verification.k` | 5 | 13 | proof-local |

There are no `[functional]` or `[simplification]` declarations/rules. The
inventory includes all `function`, `total`, `concrete`, `owise`, macro,
strictness, and priority attributes. In particular it records 41
`priority(40)`, one `priority(39)`, three `priority(45)`, 30 `owise`, and 37
`concrete` rules. Attribute locations are also preserved in
`evidence/stage5/attribute-locations.txt`.

### Used-construct map

Every submitted MPY construct maps to ordinary supplied rules:

| Submitted construct | Declaration/evaluation | State or result rule |
|---|---|---|
| `Module`, `ImportFrom` | `syntax.k`; `core.k` `#loadAll`/statement sequencing | `controls.k` non-math import no-op |
| `FuncDef`, `Params` | `syntax.k` | `functions.k` creates `closureVal` in the current scope |
| `Call(Name(...), ...)` | `call.k` callee-first routing; `core.k` left-to-right `#evalArgs` | `call.k` allocates frame; `functions.k` binds parameter and pops on return |
| `Assign`, `Name` | RHS strictness; `core.k` lexical lookup | `controls.k` writes current scope |
| `ListExpr()` | `list.k` argument evaluator | fresh `#alloc(list(.ValSeq))` in `core.k` |
| `Str`, string iteration | `str.k` codes and `#iterNext` | one-character `str` yields |
| `For` | strict iterable and `controls.k` `#loop` | `#bindTgt`, body, and loop-label continuation |
| `If`, `Continue` | strict condition, `#branch` | continue discards body suffix only up to the matching loop label |
| `Compare ==` | explicit comparison contexts in `operators.k` | `str.k`/`int.k` equality cases |
| `AugAssign +=/-=` | strict RHS | `controls.k` updates from `applyBin`; `str.k` concatenation and `int.k` arithmetic |
| `Attribute(..., "append")`, call | `call.k` bound-method routing and left-to-right argument evaluation | `list.k` priority-40 in-place heap append, returning `noneV` |
| `Expr(call)` | strict expression | `controls.k` discards the value after retaining effects |
| `Return(Name("groups"))` | strict return expression | `functions.k` records return, pops frame, restores caller, preserves escaping heap ref |

This path preserves evaluation order, current-scope updates, fresh list
allocation, heap mutation, call/return control, the loop-control delimiter,
and `NoExc`. Priority rules on the path only ensure heap references and the
mutating `append` case preempt generic value dispatch. They do not skip source
statements or fabricate the returned list.

### Proof-local rules

All five proof-local declarations and all thirteen proof-local rules are
accounted for:

| Extension | Class and domain | Static decision |
|---|---|---|
| `scanGroups` and 4 equations | total definitional summary over `IntSeq × IntSeq × Int × ValSeq` | Empty, space, open, and `owise` constructor cases are exhaustive/disjoint. Each recursive case consumes `REST`. It occurs only in claims and other summary equations, never at a running source redex. |
| `scanClose` and 2 equations | total helper for a non-space/non-open character | Guards `DEPTH - 1 == 0` and `=/= 0` are disjoint and exhaustive. The zero case appends exactly the completed string and resets state; the other preserves the partial string and decremented depth. |
| `balancedTail` and 4 equations | total precondition predicate | Empty, space, open, and guarded-other cases are disjoint. The other case admits only code 41 with positive depth. Recursion consumes `REST`; final depth must be zero. |
| `parenSpaceOnly` and 2 equations | total precondition predicate | Exhaustive structural recursion; it admits only codes 32, 40, and 41. |
| `solutionClosure` and its macro equation | exact-body macro | Compile-time naming only. It introduces no runtime rewrite and expands to the byte-checked submitted function closure. |

`scanGroups` encodes the desired mathematical output on the right-hand side,
as a specification must, but does not replace the property-bearing Python
execution. The operational loop, branches, assignments, append, and return all
execute under the fixed semantics before the reachability target is obtained.
There is no bridge of the form `Call(...) => scanGroups(...)`, no unconstrained
oracle, and no symbol shared circularly between an operational shortcut and the
postcondition.

### Opaque and unused fixed-semantics symbols

The fixed supplied semantics declares 25 symbol/no-evaluator functions in
`float.k`, `sort.k`, and `builtins.k`, including float arithmetic/conversion
symbols, `sortVS`, `sortKeyVS`, and `md5hexCodes`. None is reachable from the
submitted AST, a precondition, `scanGroups`, or a postcondition. The proof-local
module declares no opaque symbol. These fixed but unused declarations therefore
have no value, control, state, exception, or postcondition influence here.

I found no unsound inventoried rule. Accordingly there is no claimed
unsoundness for which a false-conclusion witness is owed. The concrete
out-of-domain Python divergences in stage 2 are reported only as domain
limitations and are not mislabeled as rule unsoundness.

## 6. Fresh non-vacuity test

No candidate `spec-vacuity.k` exists. I wrote a fresh mutation in scratch and
preserved it as `evidence/stage6/spec-vacuity.k`. It uses the satisfiable empty
entry state but changes the result-bearing heap obligation from the true empty
list to a one-element list containing `"()"`.

The mutation parsed and built successfully. Execution reached:

```text
<k> ref ( 0 ) ~> .K </k>
<heap> 0 |-> list ( .ValSeq ) </heap>
<heapLoc> 1 </heapLoc>
<stack> .List </stack>
<ret> noRet </ret>
<exc> NoExc </exc>
```

It then emitted `WarnStuckClaimState` because that terminal configuration does
not unify with the false destination, and `kprove` exited 1. This is the
expected unmet result obligation, not a parser failure, missing import,
timeout, unreachable mutation, or unrelated crash. The exact command, complete
bounded residual, and exit status are in
`evidence/stage6/vacuity-proof.log`.

The result constraint and non-vacuity gate passes.

## 7. Proven versus assumed accounting

### What is machine proved

Under the exact supplied MPY semantics and the proof-local equations, the
successful reachability proof establishes:

1. For every finite `IntSeq CODES` that represents a balanced sequence of only
   spaces and parentheses, the exact submitted function closure, called from
   the specified fresh state, is partially correct: if it reaches the target,
   it returns a reference whose heap object is exactly
   `scanGroups(CODES, empty, 0, empty)`, with no pending return, stack, or
   exception.
2. The universal loop claim correctly advances any satisfiable partial state
   described by its invariant to the corresponding `scanGroups` summary and
   restores empty current text and zero depth.
3. The four concrete expected results are reachability theorems.
4. The false empty-result alternative is not derivable.

This is partial correctness, not a separately claimed termination theorem.

### Trust ledger

| Boundary | Influence and dependents | Assessment |
|---|---|---|
| K v7.1.337 reachability engine, parser, SMT/backend, and built-in `INT`, `BOOL`, `STRING`, `MAP`, `LIST`, and equality theories | All builds and claims | Ordinary unavoidable toolchain trust boundary. Versions and commands are recorded. |
| `/reference/reference-semantics` | Defines all MPY execution, control, heap, call, and value behavior | Authorized fixed semantics for `SUPPLIED_SEMANTICS`; candidate copy is byte-identical. This proves behavior under MPY, not all of CPython. |
| Separately proved invariant later marked trusted | Public and concrete entry proofs | Acceptable modular composition: its own fresh run exited 0 with `#Top`; it is not merely candidate-asserted. |
| `scanGroups`, `scanClose`, `balancedTail`, `parenSpaceOnly` | Formal domain and returned list | Not opaque or assumed: exhaustive guarded recursive equations are in the proof definition and statically audited. |
| `solutionClosure` normalization | Source-to-entry theorem link | Macro expansion is exact, translator output is byte-identical, and the audit-authored module-loading claim closes. |
| Opaque symbols in float/sort/MD5 portions of supplied semantics | None on this program or claim path | Acceptable but unused fixed boundary; no dependent claim value. |
| Meaning of `scanGroups` as “the requested top-level group separation” | Natural-language adequacy | Transparent informal structural argument plus 8,763 finite differential cases and ground substitutions. It is not a universal K theorem, so it is the principal reason for `CONCERNS`. |
| Candidate generation metadata and traces | Provenance only | Missing. Independent reconstruction compensates for proof validity, but the omission remains an auditability concern. |

Differential testing is used only to support the implementation/canonical and
summary/intent bridges on the recorded finite inputs. It is not treated as a
substitute for the K reachability proof.

### Excluded behavior

The theorem does not cover unbalanced strings, code sequences containing
characters other than space and parentheses, non-string arguments, rebinding of
the function, arbitrary preexisting caller heaps/scopes, or full CPython
exception/Unicode behavior. These exclusions are explicit and do not weaken
the claimed result on the prompt's valid domain.

### Gate summary

- Dynamic clean reconstruction: **pass**.
- Real-program soundness, result constraint, and non-vacuity: **pass**.
- Intended-domain alignment: **pass with documented informal bridge and
  out-of-domain limitation**.
- Trust/evidence auditability: **pass with missing candidate provenance
  records noted**.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
