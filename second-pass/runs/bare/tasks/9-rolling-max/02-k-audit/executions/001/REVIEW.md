# Independent adversarial review: 9-rolling-max

The candidate's positive claims reconstruct and print `#Top`, and the submitted
Python program is correct. The K proof is nevertheless **not legitimate**. Its
only universal loop reasoning is a high-priority ordinary rule that replaces the
real loop with the desired rolling-maximum result. That rule has no connection
proof and is observably false about the loop's state and accepted
continuations. It can prove a concrete false reachability conclusion for the
real loop head on input `[2, 1]`.

Audit workspace: `/tmp/audit-work/9-rolling-max/build`. Only source files were
copied there; no candidate definition or cache was reused. Reviewer artifacts
and bounded logs are under `/audit-output/evidence`.

## 1. Input and provenance integrity

The rendered mode and trusted mounts agree. This is
`GENERATED_SEMANTICS`, and `/reference/reference-semantics` does not exist
([mode-boundary log](evidence/stage1_mode_boundary.log), exit 0). There is no
infrastructure breach.

The candidate prompt and translator are regular files and are byte-identical to
their trusted counterparts:

- `/candidate/prompt.py` equals `/reference/prompt.py`
  ([comparison](evidence/stage1_prompt_cmp.log), exit 0).
- `/candidate/py2mpy.py` equals `/reference/py2mpy.py`
  ([comparison](evidence/stage1_translator_cmp.log), exit 0).
- Hashes are preserved in [stage1_hashes.log](evidence/stage1_hashes.log).
- No symlink occurs anywhere under `/candidate` or `/reference`
  ([stage1_symlinks.log](evidence/stage1_symlinks.log)); top-level object types
  are recorded in
  [stage1_top_level_types.log](evidence/stage1_top_level_types.log).

All generation-required source artifacts are present as regular files:
`solution.py`, `solution.mpy`, `semantic.k`, helper `solution-ast.k`,
`verification.k`, `spec.k`, and `prove.sh`. No required artifact is missing,
changed, mistyped, or symlinked. Extra candidate artifacts include
`operational-spec.k`, `mutation-spec.k`, three generated case files,
`make_case.py`, `__pycache__`, and candidate-built `*-kompiled` directories.
They are not integrity failures, but all were treated as untrusted; the built
definitions and caches were excluded from reconstruction.

I read `run-input.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, and all 250 JSONL records in the structured trace as
untrusted claims. Their bounded structural summary and hashes are in
[stage1_untrusted_generation_summary.log](evidence/stage1_untrusted_generation_summary.log).
They claim two successful positive proof commands, three concrete cases, an
expected mutation failure, and 8,000 inline Python checks. None was accepted as
proof evidence. In particular, the 8,000-check script was not a submitted
artifact, so it was replaced with the independent preserved test in Stage 2.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt and canonical implementation require: for every integer
input list, return a list of equal length whose element at index `i` is the
maximum of the input prefix through `i`. The empty input returns `[]`. The
documented example maps `[1,2,3,2,3,4,2]` to
`[1,2,3,3,3,4,4]`.

`/candidate/solution.py` implements a different but equivalent algorithm. A
`first` flag initializes `maximum` from the first element, later elements update
it only on strict increase, and each current maximum is appended. The initial
zero is never observed for a nonempty list, so all-negative inputs are handled
correctly; the loop is skipped for an empty list.

Running the trusted translator over the scratch copy of `solution.py` produces
output byte-identical to the submitted `solution.mpy`
([stage2_translator_byte_identity.log](evidence/stage2_translator_byte_identity.log),
exit 0). The regenerated constructor text is preserved in
[stage2_translator_render.log](evidence/stage2_translator_render.log).

The reviewer-authored
[differential_test.py](evidence/differential_test.py) independently imports
`/reference/canonical.py:rolling_max` and the scratch copy of the generated
entry point. It also uses an independently written prefix-maximum oracle and
checks that the input is not mutated. The exact scope is preserved in
[differential_inputs.txt](evidence/differential_inputs.txt):

- ten named cases, including the documented example, empty and singleton
  boundaries, each `first`/comparison branch, equality, all-negative values,
  duplicates, and arbitrary-precision extremes;
- all 19,531 lists of lengths 0 through 6 over `{-3,-1,0,1,3}`;
- 2,000 deterministic generated lists of lengths 0 through 30.

The run tested 21,541 inputs and found zero mismatches
([stage2_differential.log](evidence/stage2_differential.log), exit 0).
Thus the Python implementation-to-contract bridge has strong finite support,
although testing is not a universal proof.

## 3. Clean proof reconstruction

Tool versions are recorded in [tool_versions.log](evidence/tool_versions.log):
K `v7.1.293` and Python `3.10.12`.

I copied only the candidate K/Python source artifacts and the trusted reference
inputs to `/tmp/audit-work/9-rolling-max`. The following fresh builds all exited
0:

- LLVM concrete semantics:
  `kompile semantic.k --main-module MPY --syntax-module MPY-SYNTAX
  --backend llvm --output-definition audit-semantic-kompiled`
  ([build log](evidence/stage3_kompile_semantic_llvm.log)).
- Haskell fixed operational definition:
  `kompile solution-ast.k --main-module SOLUTION-AST
  --syntax-module MPY-SYNTAX --backend haskell
  --output-definition audit-operational-kompiled`
  ([build log](evidence/stage3_kompile_operational_haskell.log)).
- Haskell proof-extended definition:
  `kompile verification.k --main-module VERIFICATION
  --syntax-module MPY-SYNTAX --backend haskell
  --output-definition audit-verification-kompiled`
  ([build log](evidence/stage3_kompile_verification_haskell.log)).

The candidate's full fixed-operational proof command and target proof command
both exited 0 and printed exactly `#Top`
([operational](evidence/stage3_kprove_operational_all.log),
[target](evidence/stage3_kprove_target_all.log)). I also placed each target
claim in a separate reviewer-authored spec and ran it independently. The
universal, empty, prompt-example, and all-negative claims each exited 0 and
printed `#Top`:

- [universal](evidence/stage3_kprove_target_universal.log)
- [empty](evidence/stage3_kprove_target_empty.log)
- [prompt](evidence/stage3_kprove_target_prompt.log)
- [negative](evidence/stage3_kprove_target_negative.log)

For generated-semantics validation, the fresh LLVM definition executed eight
cases: empty, singleton negative, strict-decrease, strict-increase, equality,
the prompt example, all-negative, and very large integers. Every final K
configuration contained the same list as both Python implementations and the
independent oracle
([concrete_semantics_test.sh](evidence/concrete_semantics_test.sh),
[run log](evidence/stage3_concrete_semantics.log), exit 0).

These results establish fresh proof closure and useful concrete-semantic
agreement. They do not establish the soundness of `verification.k`.

## 4. Adequacy and real-program pinning

### Entry claims in plain language

All four claims require the exact initial configuration:
`<functions> .Map`, `<env> .Map`, and `<stack> .List`. None has an explicit
`requires` clause.

1. **Universal claim.** For any K value of sort `List` bound to `XS`, running
   `VerifyRunList(SOLUTION, XS)` must consume the computation and return
   `ListVal(#rollingMax(XS))`, with all three state cells empty.
2. **Empty claim.** The same initial state with `.List` must return
   `ListVal(.List)`.
3. **Prompt claim.** The documented seven-element input must return the exact
   documented seven-element rolling-max list.
4. **Negative claim.** `[-5,-9,-3,-4]` must return `[-5,-5,-3,-3]`.

The special claims are ground instances of the universal claim. The universal
precondition is satisfiable, for example with the exact initial cells and
`XS = ListItem(2) ListItem(1)`. The other three entry states are satisfiable by
their displayed ground inputs. Substitution at `[2,1]` yields
`#rollingMax([2,1]) = [2,2]`; both Python implementations, the independent
oracle, and fixed K execution return `[2,2]`
([stage3_concrete_semantics.log](evidence/stage3_concrete_semantics.log),
[stage6_mutation_python_witness.log](evidence/stage6_mutation_python_witness.log)).
The displayed empty, prompt, and negative substitutions likewise agree in the
same concrete log.

The exact internal `[2,1]` loop-head state later used as a soundness witness is
itself reached by the submitted program under fixed semantics: the
reviewer-authored reachability claim closes with `#Top`
([spec](evidence/loop-head-reachable.k),
[log](evidence/stage4_loop_head_reachable.log)).

`XS:List` is formally broader than the intended `List[int]`: K's generic
`List` sort is not accompanied by a predicate requiring every item to be an
integer, while the operational loop and `#rollingMax` equations cover
integer-item lists. This is an over-broad formal claim outside the intended
input domain, not a restriction on intended inputs.

### Pinning to the submitted program

The entry term does not parse `solution.mpy` at proof time; it uses the
`SOLUTION` macro in `solution-ast.k`. I therefore compared normalized,
macro-expanded KORE for the submitted `solution.mpy` with normalized,
macro-expanded KORE for `SOLUTION`. They are byte-identical
([stage4_solution_macro_identity.log](evidence/stage4_solution_macro_identity.log),
exit 0); human-readable renderings are in
[stage4_solution_mpy_kast.log](evidence/stage4_solution_mpy_kast.log) and
[stage4_solution_macro_kast.log](evidence/stage4_solution_macro_kast.log).
Together with trusted translator byte identity, this pins `SOLUTION` to the
current submitted Python program's constructor AST.

The helper macros `ROLLING-BODY` and `ROLLING-LOOP` also match the actual
function and loop constructors. Thus there is no substituted-program defect.
The fatal problem is semantic: the proof recognizes that exact real loop and
then bypasses its execution with an assumed result.

## 5. Rule-by-rule static soundness review

The exhaustive declaration and 48-rule inventory is
[rule_inventory.md](evidence/rule_inventory.md). It enumerates:

- every local syntax production in `semantic.k`, `solution-ast.k`, and
  `verification.k`;
- the `<py>/<k>/<functions>/<env>/<stack>` configuration;
- all macros, functions, attributes, ordinary semantic rules, and the sole
  priority rule;
- every construct in `solution.mpy` and the rules that execute it.

There are no local opaque, `[functional]`, `[simplification]`, or `[concrete]`
symbols/rules. `intsToList` is the only `[total]` function; its three equations
are disjoint, exhaustive on `Ints`, and structurally descending.
`#rollingMax` and `#scanMax` are non-total K functions whose equations are
disjoint, exhaustive, and descending on integer-item lists. Their two
`#scanMax` guards are complementary for integers.

The generated semantics is a deliberately small Python subset. Every construct
used by `solution.mpy` has a declaration and execution path: module/statement
sequencing, the inert `typing` import, function registration and one call
frame, literal/name evaluation, assignments, integer `>`, branches,
named-list append, integer-list iteration, and the trailing return. Evaluation
order and the relevant environment, function-map, stack, and list mutations
agree with the submitted program. Some rules are deliberately over-broad for
unused Python contexts—for example `Return(E) => E ...` does not discard a
following statement—but the submitted return is last. I found no
intended-domain false conclusion witness for those unused shapes and therefore
do not label them unsound.

### Materially unsound proof-local rule

`verification.k:17-28` is an **operational bridge**, not a loop invariant or
derived lemma. At the reachable loop head it matches:

- the exact submitted `ROLLING-LOOP` body;
- initial locals `first=true`, `maximum=0`, `numbers=ListVal(XS)`,
  `result=[]`;
- any `XS:List`;
- an arbitrary trailing `<k>` continuation because of `...`;
- arbitrary framed `<functions>` and `<stack>` cells because they are omitted.

It then skips every fixed `For`/`Loop` step, writes
`result=#rollingMax(XS)`, retains `numbers`, and deletes `first`, `maximum`,
and the eventual loop variable `number`. Priority 40 makes it preempt the
ordinary `For` rule. The bridge's value is exactly the result used by the final
postcondition. There is no auxiliary universal reachability claim connecting
the fixed loop to this summary, and a priority annotation supplies no such
theorem. The three ground claims in `operational-spec.k` and finite concrete
tests do not prove universal equivalence.

This rule has a concrete false-conclusion witness on an intended input:
`[2,1]`. The witness starts at the actual loop-head environment reached after
the three assignments, with the actual function binding, call frame, and
actual statement-tail suffix
`Return(result) .Stmts ~> EndCall ~> Cleanup`. Fixed execution produces
`result=[2,2]` but also retains `first=false`, `maximum=2`, and `number=1` at
the loop boundary. The bridge fabricates an exact map containing only
`numbers` and `result`.

Reachability of that exact starting configuration from
`OpRunList(SOLUTION,[2,1])` is independently machine-checked in
[stage4_loop_head_reachable.log](evidence/stage4_loop_head_reachable.log)
(`#Top`, exit 0).

- Fixed execution at the actual suffix reaches the complete retained map
  (`first=false`, `maximum=2`, `number=1`, `numbers=[2,1]`,
  `result=[2,2]`) with `#Top`, exit 0
  ([spec](evidence/bridge-true-footprint-operational.k),
  [log](evidence/stage5_bridge_true_footprint_operational.log)).
- With the proof bridge, the false footprint claim prints `#Top` and exits 0
  ([spec](evidence/bridge-false-footprint-verification.k),
  [log](evidence/stage5_bridge_false_footprint_verification.log)).
- With only fixed operational rules, the identical false footprint obligation
  is rejected with `WarnStuckClaimState` and exit 1
  ([spec](evidence/bridge-false-footprint-operational.k),
  [log](evidence/stage5_bridge_false_footprint_operational.log)).

The bridge also fails the required continuation-containment check. Because its
ellipsis admits `Name("first")` immediately after the loop:

- fixed execution returns `BoolVal(false)` with the complete retained
  environment (`#Top`, exit 0:
  [spec](evidence/bridge-continuation-operational.k),
  [log](evidence/stage5_bridge_continuation_operational.log));
- bridge-enabled execution preempts the loop, deletes `first`, and gets stuck
  at `Name("first")` (`WarnStuckClaimState`, exit 1:
  [spec](evidence/bridge-continuation-verification.k),
  [log](evidence/stage5_bridge_continuation_verification.log)).

This is both a concrete false state conclusion enabled by the rule and a
concrete control-context disagreement. The rule directly assumes the
property-bearing computation whose correctness the theorem is supposed to
prove. It is not an acceptable low-level primitive or mathematical lemma.
Gate A therefore fails.

## 6. Fresh non-vacuity test

I did not rely on the candidate's mutation. The fresh
[fresh-vacuity.k](evidence/fresh-vacuity.k) changes a result-constraining
obligation for satisfying input `[2,1]`: it demands false output `[2,1]`
instead of true output `[2,2]`.

- `kprove ... --dry-run --output none` successfully parsed and built the
  mutation, exit 0
  ([stage6_mutation_build.log](evidence/stage6_mutation_build.log)).
- The real proof run reached `ListVal([2,2])`, emitted
  `WarnStuckClaimState`, and exited 1 because that does not unify with the
  mutated destination
  ([stage6_mutation_proof.log](evidence/stage6_mutation_proof.log)).
- Both Python implementations independently return `[2,2]`, demonstrating that
  the mutation is false for the satisfying input
  ([stage6_mutation_python_witness.log](evidence/stage6_mutation_python_witness.log)).

The entry postcondition is therefore result-constraining and non-vacuous. This
does not repair the unsound operational bridge: the proof discriminates among
postconditions only after the bridge has assumed the real loop's desired
result.

## 7. Proven versus assumed accounting

What `#Top` establishes precisely is conditional closure in the
proof-extended `VERIFICATION` theory: starting from the displayed initial
configuration, the macro-transcribed program reaches
`ListVal(#rollingMax(XS))` after the high-priority loop-summary rule is allowed
to replace the submitted loop. It does **not** establish that fixed execution
of that loop universally produces the summary or preserves its operational
state.

| Boundary | Status | Dependents and assessment |
|---|---|---|
| K's built-in mathematical integers, Booleans, `List`, `Map`, and the K rewrite/proof engine | Trusted primitive | Normal K trust base; affects all semantics and claims. Acceptable. |
| `/reference/py2mpy.py` | Trusted mounted translator | Connects `solution.py` to `solution.mpy`; byte identity was checked. Acceptable trusted input. |
| `SOLUTION`/body/loop macros | Constructor transcription | Connects the spec to the submitted AST; normalized KORE identity was checked. Acceptable for the current artifacts. |
| Generated `semantic.k` small-step rules | Individually generated language semantics | Static construct/rule review plus eight fixed-semantics comparisons supports the used subset. Unused Python behavior is excluded. Acceptable for the submitted program. |
| `#rollingMax` and `#scanMax` | Mathematical definitional summaries | Truthful, guarded, descending equations on integer-item lists. Acceptable. |
| `verification.k:17-28` loop rule | Program-derived, result-bearing operational bridge | Determines the universal claim's returned value and state. No connection theorem; concrete false footprint and continuation witnesses exist. **Illegitimate.** |
| Canonical/generated Python differential tests | Empirical intent bridge | 21,541 zero-mismatch inputs support source-program equivalence and contract alignment only on tested inputs. They do not prove the K loop bridge. |
| Concrete K/Python comparisons and three fixed-operational ground claims | Empirical/ground semantic bridge | Support the generated semantics on selected inputs; do not establish the missing universal loop theorem. |
| Partial-correctness interpretation | Theorem scope | No separate termination theorem is claimed. This is acceptable for the requested partial-correctness scope, but the conditional reachability theorem is still invalidated by the bridge. |

Gate summary:

- **Gate A, real-program soundness: FAIL.** The bridge is an unproved,
  result-bearing replacement and can prove a concrete false loop-state
  conclusion.
- **Gate B, intent adequacy: PASS on the intended integer-list domain.** The
  Python program, `#rollingMax`, examples, and current AST agree. The raw K
  `List` sort is formally broader than that domain.
- **Gate C, auditability: PASS for this reconstruction.** Commands, sources,
  statuses, and bounded outputs are preserved. All differential and concrete
  results are explicitly treated as finite evidence.

The earliest and decisive failure is Gate A. A clean `#Top`, correct Python
behavior, and a successful non-vacuity probe cannot legitimize an axiom that
assumes and operationally misstates the loop being verified.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
