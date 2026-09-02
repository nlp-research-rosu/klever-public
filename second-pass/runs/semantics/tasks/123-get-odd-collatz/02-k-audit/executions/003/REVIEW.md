# Independent adversarial proof audit: 123-get-odd-collatz

## Executive decision

The candidate does **not** contain a partial-correctness proof for the stated
positive-integer domain. Fresh reconstruction confirms that all seven submitted
claims close, that the four ground claims really execute the submitted program,
and that those ground claims are result-constraining and non-vacuous. That is
not the theorem required by the task.

There is no symbolic end-to-end entry claim. The only end-to-end claims fix the
argument to `1`, `5`, `6`, or `7`. The odd/even claims describe one loop
transition in an artificial configuration which is not a reachable function
loop state: their `<k>` cells omit the real loop suffix and return continuation,
their module scope omits the loaded function closure, and their call stacks are
empty. Consequently, those claims cannot be composed with the exit claim to
establish the behavior of a call on arbitrary positive `n`. The truthful
`collatzResult` equations in `verification.k` are not referenced by any claim.

This is an adequacy and domain-coverage failure, not a finding that a local rule
is mathematically false. Under the benchmark's decision boundary, finitely many
fixed cases and disconnected local transitions materially narrow the
HumanEval contract and require `FAIL / NOT_LEGIT`.

## 1. Input and provenance integrity

I treated all candidate and generation material as untrusted evidence. I read
the launcher record first and independently checked the container mounts. The
record declares:

- layout `legacy-selected-stage1`;
- condition `semantics`;
- semantics mode `SUPPLIED_SEMANTICS`;
- problem `123-get-odd-collatz`.

`/audit-campaign-lock.json` exactly matches the campaign block in
`/audit-input.json`; its actual and recorded SHA-256 are both
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
Every launcher-declared provenance mount was a readable regular file or
directory of the expected type.

For the declared layout I inspected `/run.json`, `/task.json`,
`/generation-result.json`, `invocation.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, `prompt.txt`, the structured trace, and the present
`usage.json`. The structured trace contains 481 valid JSONL records; all 107
recorded tool calls have corresponding outputs and there are no unmatched
calls. All direct recorded hashes and every per-file hash in the invocation
record match the mounted bytes. Historical runtime metrics not recorded by this
legacy layout were not reconstructed.

The independent candidate-tree digest is
`5caff917c0f322489e2a64ddc0ab29c2ae7b80521bcf11e199039828815ef4ea`.
The launcher also records a retained-tree hash using its own manifest
representation; I did not equate that representation with my independent
digest. The mounted candidate contains no forbidden symlink or special entry,
and no required proof artifact is missing.

The candidate's `prompt.py` and `py2mpy.py` are byte-identical to the trusted
mounts. Because this is `SUPPLIED_SEMANTICS`, I recursively compared the entire
candidate `reference-semantics/` tree to
`/reference/reference-semantics`. Both contain the same 25 directory/file
entries, no symlinks or special entries, and identical bytes at every path.
Their independent manifest digest is
`f0c29528ed63ff0f7ba1e3531629fc98257cb7f30b208af087ccbaeafaff4200`.
The supplied-semantics boundary is therefore intact. This comparison does not
bless the proof-local rules in `verification.k`.

Evidence:

- [integrity check](evidence/stage1-integrity-check.log)
- [recursive semantics, prompt, and translator comparison](evidence/stage1-semantics-integrity.log)
- [required-record inventory](evidence/stage1-required-records.log)
- [generation-record inspection](evidence/stage1-generation-output-inspection.log)
- [structured-trace audit](evidence/stage1-trace-summary.log)
- [reviewer integrity script](evidence/stage1_integrity.py)

No infrastructure breach was found, so a candidate verdict is appropriate.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For a positive integer `n`, repeatedly apply the Collatz transition until `1`:
replace even `n` by `n // 2`, and replace odd `n` by `3*n + 1`. Collect every
odd value encountered, including the final `1`, and return those values in
ascending order. The required theorem is partial correctness: it need not prove
the Collatz conjecture or termination, but it must constrain the returned value
on every terminating execution in the stated domain.

`solution.py` implements exactly that loop with integer `//`, appends an odd
value before its `3*n+1` transition, appends the final `1`, and calls `sorted`.
There is no empty-input case because the documented input is a scalar positive
integer; zero and negative values are outside the contract.

I copied source artifacts to `/tmp/audit-work/fresh` and regenerated
`solution.mpy` with the trusted translator:

```text
python3 py2mpy.py solution.py > regenerated-solution.mpy
cmp solution.mpy regenerated-solution.mpy
```

Both commands exited zero. The submitted and regenerated files are
byte-identical with SHA-256
`f4708dc0e8987be8a34cc414b047a61e4464be6886b3c90740dcf4e169b7e1d`.
See [translation reconstruction](evidence/stage2-translation-regeneration.log).

The independent differential harness imports the trusted canonical entry point,
the candidate entry point, and a reviewer-written exact-integer oracle. It ran
318 distinct positive values: documented examples; `1`; odd/even and branch
boundaries; 300 seeded values from `[1, 50000]`; 32-bit boundaries; and values
around and above `2**53`. The candidate had zero disagreements with the exact
contract.

The trusted canonical implementation disagreed with the exact contract on
three large integers (`2**53-1`, `2**54+1`, and `2**55+3`) because it uses true
division and thereby introduces binary floating-point behavior. The candidate
uses exact integer floor division and is correct on those inputs. I therefore
record this as a limitation of the trusted canonical implementation, not a
candidate program-fidelity defect.

Evidence:

- [differential script](evidence/differential_test.py)
- [inputs and differential results](evidence/stage2-differential.log)
- [source inspection](evidence/stage2-source-inspection.log)

## 3. Clean proof reconstruction

I used only source copied into `/tmp/audit-work/fresh`; no candidate-provided
compiled definition or cache was reused. The installed `kompile`, `krun`, and
`kprove` are K `v7.1.293`.

The concrete definition was freshly built with:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
```

It exited zero. A reviewer harness mechanically checked that its function AST
equals the submitted function AST, translated it with the trusted translator,
and used `krun` assertions for `1, 2, 3, 5, 6, 7, 27`; the command exited zero.
See [LLVM build](evidence/stage3-kompile-llvm.log),
[concrete harness](evidence/concrete_audit.py), and
[concrete execution](evidence/stage3-concrete-execution.log).

The proof definition was freshly built with:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module VERIFICATION \
  --output-definition audit-verification-kompiled
```

It exited zero. I then invoked `kprove` separately for every positive target
claim, using `--depth 2000 --smt-timeout 5000`. Each command exited zero and
printed `#Top`:

| Claim | Fresh result |
|---|---|
| `odd-step` | exit 0, `#Top` |
| `even-step` | exit 0, `#Top` |
| `exit-step` | exit 0, `#Top` |
| `case-1` | exit 0, `#Top` |
| `case-5` | exit 0, `#Top` |
| `case-6` | exit 0, `#Top` |
| `case-7` | exit 0, `#Top` |

The combined invocation also exited zero and printed `#Top`. Exact commands,
statuses, and bounded outputs are in
[the proof build](evidence/stage3-kompile-proof.log),
[odd-step](evidence/stage3-kprove-odd-step.log),
[even-step](evidence/stage3-kprove-even-step.log),
[exit-step](evidence/stage3-kprove-exit-step.log),
[case-1](evidence/stage3-kprove-case-1.log),
[case-5](evidence/stage3-kprove-case-5.log),
[case-6](evidence/stage3-kprove-case-6.log),
[case-7](evidence/stage3-kprove-case-7.log), and
[combined proof](evidence/stage3-kprove-all.log).

Thus reconstruction succeeds. The verdict does not arise from a build failure
or an unclosed submitted claim; it arises from what those claims actually say.

## 4. Adequacy and real-program pinning

### Claim meanings and satisfying states

The claims have the following literal preconditions and postconditions:

- `odd-step` (`spec.k:7-53`) assumes an isolated loop at `n=N>1`, odd `N`, an
  arbitrary list sequence `A`, empty module scope, and empty call stack. It
  proves one iteration appends `N`, changes `n` to `3*N+1`, and leaves
  `#loopLbl(loop)` in `<k>`. A satisfying witness is `N=3`, `A=.ValSeq`.
- `even-step` (`spec.k:56-100`) assumes the analogous isolated state with
  `N>1` and `N` not odd. It proves one iteration leaves `A` unchanged and sets
  `n` to Python floor-division by `2`. A witness is `N=2`, `A=[7]`.
- `exit-step` (`spec.k:104-144`) assumes `n=1`, arbitrary accumulator `A`, a
  module map `M` which does not shadow `sorted`, the actual append/return tail,
  `#endcall`, and one caller frame. It proves that `1` is appended and that a
  fresh list containing `sortVS(A ++ [1])` is returned. A witness is
  `A=[3,5]`, `M=.Map`, giving the concrete intended result `[1,3,5]`.
- `case-1`, `case-5`, `case-6`, and `case-7` start in a pristine configuration,
  execute `#getOddCollatz` at that one literal argument, install the closure,
  and constrain both the unsorted accumulator heap and the returned
  `sortVS(...)` heap. The reviewer witnesses give `[1]`, `[1,5]`, `[1,3,5]`,
  and `[1,5,7,11,13,17]`, matching both Python implementations on these four
  inputs.

The witnesses and substitutions are recorded in
[claim adequacy](evidence/stage4-claim-adequacy.log).

### Program pinning

The `#getOddCollatz` rule at `verification.k:8-22` loads a complete module and
calls its public function. The `getOddCollatzClosure` rule at
`verification.k:46-59` repeats that exact body for readable ground
postconditions. A reviewer parser extracted both terms and compared them to the
trustedly regenerated `solution.mpy` at constructor level. After only the
demonstrated empty-list surface normalization
`ListExpr(.Exprs) -> ListExpr()`, all three parsed body hashes are
`3dbf13bf583d255ae6c6a11bab357b069b18f009914f733697a6f0edc5df072e`,
and both equalities are true. See
[constructor comparison](evidence/stage4-constructor-comparison.log) and its
[script](evidence/constructor_compare.py).

I also changed the odd-branch append from `Name("n")` to `Int(1)` in both
embedded executable bodies. The mutant definition built, but `case-5` failed
with exit 1 and a reachable heap `[1,1]`. This establishes sensitivity to the
program body actually executed by the claim. See the
[mutation script](evidence/make_body_mutant.sh),
[build](evidence/stage4-body-mutant-kompile.log), and
[failed proof](evidence/stage4-body-mutant-kprove-case5.log).

### Material adequacy failure

Pinning is successful for the terms which are actually claimed, but the claimed
theorem is too narrow:

1. The only `#getOddCollatz` arguments in `spec.k` are the literals
   `1`, `5`, `6`, and `7`. There is no symbolic end-to-end entry claim.
2. No claim mentions `collatzResult`; its three recurrence rules are dead with
   respect to the proof obligations.
3. The odd/even claims are not invariants over reachable call states. A fresh
   concrete execution stopped at the loop head for input `5` has:
   - the loop followed by the real append-1, return, and `#endcall`
     continuation in `<k>`;
   - the loaded `get_odd_collatz` closure in scope `0`;
   - a nonempty caller stack.
   
   In contrast, both step claims require the loop to be the entire `<k>` cell,
   scope `0` to be exactly empty, and the stack to be exactly `.List`.
4. No formal claim bridges these artificial one-step states to `exit-step` or
   to an arbitrary public call. Candidate prose suggesting an induction is not
   a K reachability proof and cannot repair the configuration mismatch.

The reachable state was independently reconstructed from the exact function AST
and trusted translator; see
[reachable loop-head script](evidence/reachable_loop_5.py) and
[state output](evidence/stage4-reachable-loop-head.log).

Partial correctness does not require proving Collatz termination. It does,
however, require a symbolic invariant/safety theorem which relates every
terminating public execution to its result. The candidate has no such theorem.

## 5. Rule-by-rule static soundness review

The exhaustive machine-readable inventory is
[rule-inventory.tsv](evidence/rule-inventory.tsv), generated by the preserved
[reviewer script](evidence/rule_inventory.py). It enumerates every item in the
supplied K tree, `verification.k`, and `spec.k`: 230 syntax declarations, 700
rules, one configuration, five contexts, and seven claims (943 items total).
For each it records source path, line, kind, attributes, review disposition,
rationale, and normalized declaration/rule text.

Attribute coverage includes 147 `[function]`, 107 `[total]`, 22
`[no-evaluators]`, 29 priority, 26 `[owise]`, 32 `[concrete]`, four `[macro]`,
one `[macro-rec]`, two `[strict]`, and one `[seqstrict]` item. There are no
`[functional]`, `[simplification]`, or `[anywhere]` items. The complete counts
and inventory hash are in
[inventory generation](evidence/stage5-inventory-generation.log).

The dispositions cover:

| Disposition | Count |
|---|---:|
| declaration/configuration/context | 214 |
| reviewed rules on the used path | 52 |
| reviewed concrete fixed rules | 32 |
| reviewed unused fixed rules | 610 |
| used/unused fixed opaque boundaries | 2 / 21 |
| proof-local definitions | 2 |
| truthful but unused summary rules | 3 |
| local/fixed claims | 3 / 4 |

The mapping from every submitted construct to its syntax and material rules is
in [used-construct-map.md](evidence/used-construct-map.md). In particular, it
covers module loading, function closure and call/return, empty-list allocation,
scope/name lookup, assignments, while/if control, comparison, integer
`+`, `*`, `%`, and `//`, evaluation order, list `append`, `sorted`, expression
discard, heap allocation, stack frames, return, exception, and exit cells.

Static conclusions:

- `#getOddCollatz` and `getOddCollatzClosure` are exact program expansions, not
  task-answer shortcuts.
- `collatzResult` gives the ordinary Collatz recurrence under disjoint guards.
  It is not marked total and does not assume termination. It is sound but unused.
- The used assignment, lookup, call, append, guard, priority, integer, loop, and
  return rules preserve the expected evaluation order and state effects.
- No proof-local rule replaces the loop with an oracle, fabricates a result, or
  encodes the expected answer.
- The fixed supplied semantics maps `sorted(list(VS))` to the opaque,
  value-bearing function `sortVS(VS)`. Concrete insertion rules evaluate finite
  integer lists, but no symbolic theorem inside this proof establishes that
  `sortVS` is ascending sorting. The symbolic reading is therefore conditional
  on the supplied semantics' primitive contract. This is a disclosed
  low-level trust boundary, not a proof-local smuggled result.

I found no rule for which the candidate proof enables a false conclusion on the
intended domain, so I do not label any inventoried rule unsound. The narrower,
demonstrated failure is that the sound local claims do not constitute the
required entry theorem.

## 6. Fresh non-vacuity test

I did not rely on the candidate's vacuity material. In scratch I created a new
mutation of the proven `case-5` obligation while leaving its precondition and
program execution unchanged: the expected returned heap was changed from
`sortVS([5,1])` to `sortVS([5,3,1])`. This is meaningfully false for the
satisfying input `5`; both Python implementations return `[1,5]`.

The mutated spec successfully dry-built with the fresh proof definition. The
actual proof then exited 1 with `WarnStuckClaimState`: execution reached the
real accumulator `[5,1]` and returned list `[1,5]`, which could not unify with
the false postcondition. This is the expected unmet result obligation, not a
parser error, timeout, missing import, unrelated crash, or unreachable
mutation.

Evidence:

- [mutation generator](evidence/make_false_mutation.sh)
- [mutated spec](evidence/spec-vacuity-audit.k)
- [exact diff](evidence/spec-vacuity-audit.diff)
- [successful dry build](evidence/stage6-mutation-dry-run.log)
- [expected failed proof](evidence/stage6-mutation-kprove.log)

This establishes non-vacuity of the fixed `case-5` theorem. It does not create
the missing unrestricted theorem.

## 7. Proven versus assumed accounting

### What the successful K proofs establish

Subject to the fresh K definition and the supplied primitive contracts, they
establish exactly:

1. one odd Collatz loop transition for the artificial state in `odd-step`;
2. one even Collatz loop transition for the artificial state in `even-step`;
3. the append-1, `sorted`, and return tail for the state in `exit-step`;
4. complete result-constraining executions for inputs `1`, `5`, `6`, and `7`.

They do **not** establish:

- partial correctness of the public function for arbitrary positive integers;
- that the local step preconditions are reachable from the public call;
- an invariant preserved in the real continuation/scope/stack context;
- any formal relationship between `collatzResult` and the program;
- termination of Collatz (which is not required here);
- a proof-local mathematical implementation of opaque `sortVS`.

### Trust and assumption ledger

| Boundary | Accounting |
|---|---|
| K `v7.1.293`, its Haskell/LLVM backends, parser, compiler, runtime, and prover | Necessary toolchain trust; fresh independent reconstruction limits cache/artifact risk. |
| Byte-identical supplied semantics | Authorized fixed semantics boundary; every local file and rule was still inventoried and reviewed. |
| K built-in integer, Boolean, map, list, matching, and SMT behavior | Ordinary low-level framework/mathematical trust. |
| Trusted `py2mpy.py` | Authorized translation bridge; byte identity and constructor-level program identity were independently checked. |
| `sortVS` means ascending sorting | Opaque supplied-semantics value boundary. Concrete rules and tests support ground cases; the symbolic meaning remains assumed. |
| Differential testing | Empirical support for program fidelity only; 318 samples are not a K proof or domain proof. |
| Candidate `NOTES.md`, generation logs, traces, and prior `#Top` | Untrusted claims only; none were used as proof substitutes. |
| Informal induction over local claims | Invalid as the missing formal bridge, because the local claim configurations differ from reachable call states. |

### Gate assessment and verdict rationale

- Clean reconstruction gate: **passes**.
- Local soundness/result-constraint gate: **passes for the seven literal
  claims**.
- Real-program pinning gate: **passes for the four fixed entry executions**.
- Required theorem adequacy gate: **fails**; no arbitrary-input entry theorem
  exists, and the step claims do not match reachable entry execution contexts.
- Source-contract domain gate: **fails**; four fixed input sizes do not cover
  unrestricted positive integers.
- Non-vacuity gate: **passes for the fixed theorem tested**.

The candidate is best described generically as containing sound but materially
limited proof fragments. The benchmark explicitly maps material narrowing of
the HumanEval source-contract domain, fixed examples, and bounded fragments to
`FAIL / NOT_LEGIT`, rather than to `CONCERNS / LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
