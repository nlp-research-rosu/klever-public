# Independent adversarial audit: 63-fibfib

This audit used the required `using-kit` and `validating-proof` procedures. All
candidate material was treated as untrusted. Execution used only source copied
to `/tmp/audit-work/63-fibfib-audit`; no candidate-built K definition or cache
was reused.

The rendered mode is `SUPPLIED_SEMANTICS`. The trusted supplied-semantics mount
is present, so there is no infrastructure/mode contradiction.

## 1. Input and provenance integrity

The protected semantics tree contains 24 regular K files. An independent
`lstat`/SHA-256 walk compared all 25 tree entries (files plus the semantics
subdirectory), without following links. The candidate tree has no missing,
additional, mistyped, changed, special, or symlinked entry and is byte-identical
to `/reference/reference-semantics`. See
[`stage1-semantics-tree-integrity.log`](evidence/stage1-semantics-tree-integrity.log)
and the reviewer script
[`verify_tree_integrity.py`](evidence/verify_tree_integrity.py).

`/candidate/prompt.py` and `/candidate/py2mpy.py` are byte-identical to their
trusted mounted versions. Their hashes and the recursive `diff` result are in
[`stage1-integrity-comparisons.log`](evidence/stage1-integrity-comparisons.log).
No trusted baseline is being used to excuse the proof-local content of
`verification.k`; that file is reviewed independently in stage 5.

The following requested provenance records are absent:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`

No structured generation-trace file is present. `parsed-spec.json` is a KAST
serialization, not a generation trace; its top-level structure was inspected
as an untrusted claim. The unrequired `prove.sh`, `smoke.mpy`,
`parsed-spec.json`, and `__pycache__/solution.cpython-310.pyc` were inventoried;
the bytecode and candidate script were not used to establish any result. The
source inspection is preserved in
[`stage1-and-2-source-inspection.log`](evidence/stage1-and-2-source-inspection.log).
The absent generation records reduce historical provenance but do not obstruct
the independent source comparison and reconstruction performed here.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract defines, for nonnegative sequence indices,

`F(0)=0`, `F(1)=0`, `F(2)=1`, and
`F(n)=F(n-1)+F(n-2)+F(n-3)` thereafter, and asks for an efficient computation
of `F(n)`.

The trusted canonical implementation is the direct recursion. The candidate
uses an iterative tuple `(a,b,c)`, initially `(0,0,1)`, and repeatedly applies
`(a,b,c) := (b,c,a+b+c)`. It returns the first component after `n` shifts. It is
`O(n)` time and `O(1)` auxiliary space.

The trusted translator was run against the scratch copy of `solution.py`.
`solution.regenerated.mpy` and the submitted `solution.mpy` are byte-identical,
both with SHA-256
`c368841f1caa6223476b198afe39b7d479f69ec3268b813d7e9421a56be184eb`.
See
[`stage2-translation-identity.log`](evidence/stage2-translation-identity.log).

The independent differential script imports the trusted canonical entry point
and candidate entry point from distinct paths. It checks every integer from 0
through 20. This includes the lower/zero-iteration case, base boundaries
0/1/2, the first recurrence case 3, both loop-guard outcomes, and documented
examples 1, 5, and 8. All 21 comparisons and all documented expected values
matched; mismatch count was zero. See
[`differential_fibfib.py`](evidence/differential_fibfib.py) and
[`stage2-differential.log`](evidence/stage2-differential.log).

There is no meaningful “empty collection” input for this integer-indexed
function; `n=0` is the lower/empty-iteration boundary. Negative integers are
outside the formal claim and the ordinary domain of an `n`th sequence element.
The trusted recursive implementation also has no value-producing negative-index
case.

## 3. Clean proof reconstruction

The scratch tree was populated with source artifacts only. K version
`v7.1.337` was independently found at `/usr/bin`; see
[`stage3-toolchain.log`](evidence/stage3-toolchain.log).

Fresh concrete and proof definitions were built:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

kompile verification.k --backend haskell \
  --main-module FIBFIB-VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

Both exited 0. The concrete `smoke.mpy` assertion program, which contains the
submitted function body and checks 0, 1, 2, 5, and 8, ran under the fresh LLVM
definition and exited 0. Logs:
[`stage3-kompile-concrete.log`](evidence/stage3-kompile-concrete.log),
[`stage3-krun-smoke.log`](evidence/stage3-krun-smoke.log), and
[`stage3-kompile-proof.log`](evidence/stage3-kompile-proof.log).

Every positive claim was run under an explicit selector:

| Target | Dependency selection | Result |
|---|---|---|
| `fibfib-loop` | itself | exit 0, `#Top` |
| `fibfib-correct` | itself plus `fibfib-loop` circularity | exit 0, `#Top` |
| `example-1` | itself | exit 0, `#Top` |
| `example-5` | itself | exit 0, `#Top` |
| `example-8` | itself | exit 0, `#Top` |

The exact logs are
[`stage3-kprove-fibfib-loop.log`](evidence/stage3-kprove-fibfib-loop.log),
[`stage3-kprove-entry-with-loop-dependency.log`](evidence/stage3-kprove-entry-with-loop-dependency.log),
and the three `stage3-kprove-example-*.log` files. A combined run of the full
specification also exited 0 and printed `#Top`; see
[`stage3-kprove-all.log`](evidence/stage3-kprove-all.log).

An entry-only diagnostic selector was interrupted with status 130 because that
selector removed the required loop circularity and caused ordinary symbolic
unrolling. It is explicitly preserved as a non-verdict diagnostic in
[`stage3-diagnostic-entry-without-loop-aborted.log`](evidence/stage3-diagnostic-entry-without-loop-aborted.log).
The dependency-inclusive target run is the relevant successful reconstruction.

The supplied semantics produced compiler warnings about non-exhaustive cases
in several broad, unused library helpers and unused variables in `str.k`.
These are fixed-baseline warnings, not candidate changes. None of the warned
helpers is constructible on this integer-only program path.

## 4. Adequacy and real-program pinning

The claims mean:

- `fibfib-loop`: for any matching local scope with `0 <= I <= N`, executing the
  exact internal `#while` consumes the loop, changes `i` from `I` to `N`, and
  changes `a` from `A` to `fibFrom(A,B,C,N-I)`. Final `b`, `c`, and `d` are
  existential because they are dead after the loop; `n`, the parent scope, and
  framed cells are preserved.
- `fibfib-correct`: for every mathematical integer `N >= 0`, call the exact
  `fibfib` closure in the specified clean configuration. If the call
  terminates, its returned K value is exactly `fibFrom(0,0,1,N)`, while the
  explicit environment, scopes, allocation counters, heap, call stack, return
  state, and exception state are restored/preserved as stated.
- The three example claims reduce that fully defined summary at 1, 5, and 8 to
  0, 4, and 24.

The entry claim does not use a free result variable, implication-only
postcondition, or oracle. Its RHS is a determined integer function. A reviewer
script parses the submitted `FuncDef` and the entry claim’s `closureVal`; the
function name, parameter, definition environment, complete body, and helper
loop condition/body all match after whitespace normalization. See
[`verify_program_pinning.py`](evidence/verify_program_pinning.py) and
[`stage4-program-pinning.log`](evidence/stage4-program-pinning.log).

Concrete satisfying states exist. For the entry claim, `N=0`, `N=5`, and the
other recorded nonnegative values satisfy the precondition. For the helper,
the real state after two iterations with `N=5` is
`a=1,b=1,c=2,d=2,i=2,n=5`, which satisfies `0 <= I <= N`. Executing the
remaining loop produces `a=4,i=5`, and
`fibFrom(1,1,2,3)=4`. The claimed value also equals both Python
implementations. These witnesses, including 0/1/2/3/5/8 substitutions, are in
[`claim_witnesses.py`](evidence/claim_witnesses.py) and
[`stage4-claim-witnesses.log`](evidence/stage4-claim-witnesses.log).

Mathematically, if `F0=0,F1=0,F2=1`, induction on the number of shifts gives
`shift^k(0,0,1)=(Fk,F{k+1},F{k+2})`. Thus the formal result
`fibFrom(0,0,1,N)` is exactly the natural-language FibFib value for `N>=0`.

## 5. Rule-by-rule static soundness review

The reviewer-authored inventory covers `semantics.k`, all 23 supplied helper K
files, and `verification.k`. It contains 932 line-addressed declarations:

| Class | Count |
|---|---:|
| configuration | 1 |
| contexts | 5 |
| function declarations | 124 |
| macro declarations | 4 |
| opaque symbol declarations | 22 |
| ordinary rules | 652 |
| priority rules | 45 |
| simplification rules | 1 |
| other syntax declarations | 78 |

The exhaustive text inventory is
[`stage5-rule-inventory.tsv`](evidence/stage5-rule-inventory.tsv). Every row has
an audit disposition in
[`stage5-rule-decisions.tsv`](evidence/stage5-rule-decisions.tsv): 862 fixed
supplied-semantics entries, 44 directly used and separately reviewed fixed
entries, 22 unreachable fixed opaque primitives, and the four proof-local
entries below. The scripts that generated these files are
[`inventory_k.py`](evidence/inventory_k.py) and
[`annotate_rule_inventory.py`](evidence/annotate_rule_inventory.py).

The fixed tree is the selected supplied semantics, not a candidate-generated
language definition. Directly relevant rules were nevertheless traced for
configuration, lookup, binding, evaluation order, calls, allocation, state
updates, guards, loops, and return:

- `Module` loading creates the exact `fibfib` closure in scope 0.
- Calls evaluate the callee and integer argument, allocate one local scope,
  bind `n`, execute the closure body, and pop/restores the frame.
- `Assign` is strict in the RHS. `BinOp` is left-to-right. `Compare` has
  left-then-right contexts. Integer `+` and `<` dispatch to `+Int` and `<Int`.
- The while condition is reevaluated on every iteration. Its true/false guards
  are complementary through integer truthiness. The body statements execute
  sequentially and update the current local scope.
- Return evaluates `a`, sets the return state, discards the remaining function
  continuation as Python return requires, and restores the caller. Here return
  is also syntactically the final source statement.
- The plain closure has no `$cells` marker, so cell-write priority rules do not
  overlap the ordinary local assignment path. No heap object, builtin, float,
  collection, exception, or import construct is reachable.

The declaration/rule IDs and exact source mapping are summarized in
[`stage5-used-construct-map.md`](evidence/stage5-used-construct-map.md).

The proof-local inventory is:

1. `fibFrom(Int,Int,Int,Int) [function]` is a definitional summary. It does not
   replace an operational term or intercept a call.
2. For `N <= 0`, `fibFrom(A,B,C,N)=A`: zero shifts leave the first component.
3. For `N > 0`, one exact shift gives
   `fibFrom(B,C,A+B+C,N-1)`. The guards are disjoint and exhaustive on K
   integers, and positive recursion descends. There is no conflicting overlap.
4. `N-(I+1) => (N-I)+(-1) [simplification]` is a globally true integer
   identity. It has no state or control effect.

There is no proof-local `total`/`functional` assertion, opaque symbol, priority
rule, operational bridge, call interception, fabricated result, or
task-answer rewrite. A task-specific search confirms that FibFib names and
summary terms occur only in the submitted program/spec/proof files, not the
fixed semantics; see
[`stage5-task-specific-search.log`](evidence/stage5-task-specific-search.log).

The 22 fixed opaque primitives are float operations, sorting summaries, and
MD5. None is mentioned by or syntactically reachable from this program or its
claims, so none affects control, state, or result here. The fixed compiler’s
non-exhaustiveness warnings likewise concern unused library values. This is an
explicit unused trust boundary, not empirical support for a result-bearing
program abstraction.

As an independent body-sensitivity test, the entry closure’s final
`Return(Name("a"))` was changed to `Return(Name("b"))` while leaving the
summary and real loop claim unchanged. The mutation parsed successfully, then
`kprove` exited 1 with `WarnStuckClaimState` because returned `?_B` could not be
shown equal to `fibFrom(0,0,1,N)`. See
[`spec-body-sensitivity-auditor.k`](evidence/spec-body-sensitivity-auditor.k),
[`stage5-body-mutation-dry-run.log`](evidence/stage5-body-mutation-dry-run.log),
and
[`stage5-body-mutation-kprove.log`](evidence/stage5-body-mutation-kprove.log).
This confirms body sensitivity. No rule was found unsound, so no unsound-rule
false-conclusion witness is claimed.

## 6. Fresh non-vacuity test

No candidate `spec-vacuity.k` exists. A fresh reviewer mutation retained the
exact program and loop helper but changed the entry result to
`fibFrom(0,0,1,N)+1`. It is demonstrably false for the satisfying input `N=0`,
where both Python implementations and the summary return 0.

The mutation’s dry run exited 0, establishing that it parsed and built against
the fresh definition. The actual proof exited 1 and emitted
`WarnStuckClaimState`; its residual requires the false equality
`fibFrom(0,0,1,N)+1 = fibFrom(0,0,1,N)`. This is the expected reachable unmet
result obligation, not a parser error, missing import, timeout, or unrelated
crash. Evidence:
[`spec-vacuity-auditor.k`](evidence/spec-vacuity-auditor.k),
[`stage6-mutation-dry-run.log`](evidence/stage6-mutation-dry-run.log), and
[`stage6-mutation-kprove.log`](evidence/stage6-mutation-kprove.log).

## 7. Proven versus assumed accounting

The successful reachability proof establishes partial correctness under the
freshly built supplied K semantics: for every K integer `N>=0`, termination of
the exact submitted `fibfib` body from the stated clean call configuration
returns `fibFrom(0,0,1,N)`. The separately proved loop circularity establishes
the exact first-component tuple-shift summary. The simple induction above
identifies that summary with the stated FibFib recurrence.

Trust and evidence ledger:

| Boundary | Role and dependents | Assessment |
|---|---|---|
| K v7.1.337 parser/compiler/Haskell prover and builtin Int/Bool/Map/List theories | All machine-checking and integer algebra | Necessary low-level proof trust boundary. Fresh build/output recorded. |
| Supplied MPY semantics | Meaning of calls, scopes, assignment, integer operations, loops, and returns | Mandated fixed semantics; candidate copy is exactly identical. The entire inventory is recorded and the used path was statically reviewed. |
| 22 supplied opaque primitives and warned unused helpers | Broad float/sort/hash/library coverage | Unreachable from this program and no claim depends on them. Acceptable but explicitly excluded. |
| Trusted `py2mpy.py` | Python-source to submitted-MPY bridge | Trusted mounted translator; fresh output is byte-identical. |
| `fibFrom` | Result-bearing mathematical summary | Not assumed or opaque: exhaustive guarded equations define it, and fixed program execution is connected by the proved loop claim. |
| Natural recurrence identification | Meaning of `fibFrom(0,0,1,N)` | Ordinary induction on exact tuple shifts; supported on recorded finite witnesses but not replaced by those tests. |
| Trusted canonical Python and differential tests | Program-to-reference adequacy for 0..20 | Finite supporting evidence only; not used as a substitute for K reachability. |
| Termination and asymptotic efficiency | Outside partial-correctness theorem | Informally evident from `i` increasing to nonnegative `N` and constant state; not claimed as machine-proved. |

Gate A (real-program soundness) passes: the actual body executes, no
operational bridge/oracle exists, proof equations are sound, satisfying states
exist, body sensitivity holds, and the false result is rejected. Gate B
(intent adequacy) passes for the natural nonnegative sequence domain. Gate C
(trust/evidence auditability) passes: all reviewer evidence, commands, statuses,
mutations, and the exhaustive inventory are preserved below `evidence/`.

The missing candidate generation-history records are documented, but they do
not create a proof or intent gap after trusted-input comparison, clean
reconstruction, static validation, body sensitivity, and non-vacuity all pass.
The candidate therefore contains a legitimate, result-constraining
partial-correctness proof of the real generated program.

VERDICT: PASS
LEGITIMACY: LEGIT
