# Independent adversarial audit: 9-rolling-max

## Audit conclusion

The candidate contains a legitimate partial-correctness proof of the submitted
program over the full intended `List[int]` domain. I independently reconstructed
all three positive proof layers from source, checked that the two operational
bridges have bridge-free universal connection proofs over the same complete
match domains, mechanically pinned the entry claims and loop body to the trusted
translation, reviewed every local proof rule, and rejected a fresh reachable
false result obligation.

Nothing in `PROOF.md`, the candidate caches, the candidate logs, or the
generation trace was treated as authoritative.

## 1. Input and provenance integrity

The launcher record declares `record_layout = pipeline-v3` and
`semantics_mode = SUPPLIED_SEMANTICS`. The trusted
`/reference/reference-semantics` tree is present, so the mounted inputs do not
contradict the rendered mode.

The reviewer-authored integrity program and complete bounded output are:

- [stage1_integrity.py](/audit-output/evidence/stage1_integrity.py)
- [stage1-integrity.log](/audit-output/evidence/stage1-integrity.log)

Results:

- `/audit-input.json`, `/audit-campaign-lock.json`, `/candidate`, all three
  trusted source inputs, `/run.json`, `/task.json`, `/generation-result.json`,
  and every pipeline-v3 generation record required by the prompt are real,
  readable files/directories. No required record is a symlink.
- The `audit_campaign` object is structurally identical to
  `/audit-campaign-lock.json`; the lock's independently computed SHA-256 is
  `ad5dfc...d745`, exactly the value recorded in `/audit-input.json`.
- Independently computed hashes match the launcher values for the canonical
  source, prompt, translator, run/task/result/invocation manifests, generation
  metrics, runtime metrics, usage, prompt, last message, and full output log.
- The only structured trace contains 521 valid JSON objects and no malformed
  line. Its sole JSONL file hashes to `16e287...8fe`, as both the invocation and
  result records say. The independently computed pipeline tree digest is
  `1f7e95...029`, matching `usage.json`.
- The mounted candidate tree's independently computed pipeline-v3 digest is
  `5e0fc9...429`, matching `generation-result.json`.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical regular files to the
  trusted mounts.
- A recursive entry-type/path/content comparison of candidate and trusted
  `reference-semantics/` found no missing, additional, changed, mistyped,
  unsupported, or symlinked entry. Both independently hash to the trusted
  pipeline tree digest `4e0639...9f`.
- The six required proof artifacts are present as readable regular files.

The generation records claim success, three `#Top` results, differential tests,
and mutations. Those claims were only provenance evidence; every material point
was rerun independently below. There is no infrastructure breach requiring
`AUDIT_ERROR`.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract is: for any finite list of mathematical integers, return a
list of the same length whose element at index `i` is the maximum of the input
prefix through index `i`. The empty list returns the empty list. The documented
example is:

```text
[1,2,3,2,3,4,2] -> [1,2,3,3,3,4,4]
```

The canonical implementation keeps a `None`-initialized running maximum. The
candidate initializes from `numbers[0]` inside a nonempty guard and iterates
over the first element again. That first comparison is false/equal, so the
algorithms are equivalent. The candidate neither mutates the input nor imposes
a value or length bound.

Trusted regeneration and differential evidence are recorded in:

- [stage2_run.sh](/audit-output/evidence/stage2_run.sh)
- [stage2-fidelity-and-differential.log](/audit-output/evidence/stage2-fidelity-and-differential.log)
- [differential_audit.py](/audit-output/evidence/differential_audit.py)

`python3 /reference/py2mpy.py .../solution.py` exited 0. The regenerated and
submitted `solution.mpy` files are byte-identical, both SHA-256
`0cbccb...601`.

The independent differential program imports `/reference/canonical.py` and the
scratch copy of the submitted `solution.py`; it does not use candidate test
code or proof equations. It checked:

- the documented example, empty/singleton cases, comparison false/equal/true
  boundaries, increasing/decreasing/duplicate/negative lists, and
  arbitrary-precision extremes;
- all 19,531 lists of lengths 0 through 6 over `{-3,-1,0,1,3}`; and
- 2,000 deterministically generated lists of lengths 0 through 100, including
  large positive and negative integers.

All 21,545 cases agreed, with zero mismatches. This is finite fidelity evidence,
not a replacement for the K proof.

## 3. Clean proof reconstruction

All source needed for execution was copied to the new directory
`/tmp/audit-work/rolling-max-20260729`. The reference semantics came from the
trusted mount. No candidate `*-kompiled` directory, binary, cache, or prior log
was copied or used. K reports version `7.1.293`.

Fresh concrete reconstruction:

| Command | Result | Evidence |
|---|---:|---|
| `kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition audit-runtime-kompiled` | 0 | [LLVM build log](/audit-output/evidence/stage3-kompile-llvm.log) |
| trusted translation of the independent concrete program | 0; function AST identical to submitted function | [preparation log](/audit-output/evidence/stage3-concrete-preparation.log), [source](/audit-output/evidence/concrete_audit.py) |
| `krun concrete-audit.mpy --definition audit-runtime-kompiled` | 0; final `.K`, `NoExc`, exit code 0 | [krun log](/audit-output/evidence/stage3-krun-concrete.log) |

Fresh positive proof reconstruction:

| Definition/claim command | Build | Proof result | Evidence |
|---|---:|---:|---|
| `BIND-BASE`; `kprove bind-spec.k --definition audit-bind-kompiled --spec-module BIND-SPEC` | 0 | `#Top`, exit 0 | [build](/audit-output/evidence/stage3-kompile-bind.log), [proof](/audit-output/evidence/stage3-kprove-bind.log) |
| `LOOP-BASE`; `kprove loop-spec.k --definition audit-loop-kompiled --spec-module LOOP-SPEC` | 0 | `#Top`, exit 0 | [build](/audit-output/evidence/stage3-kompile-loop.log), [proof](/audit-output/evidence/stage3-kprove-loop.log) |
| `VERIFICATION`; `kprove spec.k --definition audit-verification-kompiled --spec-module SPEC` | 0 | `#Top`, exit 0 | [build](/audit-output/evidence/stage3-kompile-verification.log), [proof](/audit-output/evidence/stage3-kprove-spec.log) |

The warnings are fixed-semantics non-exhaustive/unused-variable warnings in
unreached generic features. No positive target emitted a stuck claim or exited
nonzero.

## 4. Adequacy and real-program pinning

### Plain-language claims

`rolling-max-empty` starts from a call through a module binding whose closure
contains the exact translated function body. Its input is `.ValSeq`. It proves
that the call returns `ref(0)`, allocates exactly heap object 0 containing the
empty result, advances `heapLoc` from 0 to 1, and restores/preserves the
environment, scopes, stack, return, exception, and exit-code cells.

`rolling-max-nonempty` has input `vCons(H,T)` where `H:Int` and
`allInts(T)`. Thus it covers every nonempty finite integer list, without a
length or magnitude bound. It proves the same call/frame facts and fixes heap
object 0 to `list(rollingMax(vCons(H,T)))`.

`rolling-loop` starts at the actual translated `#loop` with arbitrary remaining
integer sequence `IS`, current maximum `M`, prior target value `D`, and
accumulator `A`, under the exact active call continuation. It proves:

- `current` becomes `foldMax(M,IS)`;
- `number` becomes `lastOr(D,IS)`; and
- heap result sequence becomes `rollAcc(A,M,IS)`;

while preserving the input binding, module/builtin scopes, allocation counters,
frame, return, exception, and exit state.

### Mechanical identity

I parsed trusted-regenerated `solution.mpy` with the fresh definition, emitted
the expanded spec JSON, and compared normalized K constructor trees:

- [program-pinning script](/audit-output/evidence/stage4_program_pinning.py)
- [program-pinning result](/audit-output/evidence/stage4-program-pinning.log)
- [solution parse command](/audit-output/evidence/stage4-kast-solution.log)
- [spec parse command](/audit-output/evidence/stage4-emit-spec-json.log)

Both entry closures have parameters and body exactly equal to the translated
`FuncDef`; all three body hashes are
`7ba411...701`. The loop claim target and body exactly equal the sole translated
`For` target/body; both body hashes are `a94cc3...9bc8`. The omitted
`ImportFrom("typing","List")` setup is semantically inert under the fixed
`owise` import rule, and the fixed `FuncDef` rule creates precisely the closure
used by the claims. This pins the immutable submitted program without trusting
manual transcription.

### Satisfiable ground states and result substitution

The auditor-authored [ground K witnesses](/audit-output/evidence/stage4-witness.k)
instantiate every entry precondition and the loop precondition. All three prove
together with `#Top`, exit 0:
[witness proof log](/audit-output/evidence/stage4-kprove-witnesses.log).

The corresponding Python substitutions are in
[stage4_witness_python.py](/audit-output/evidence/stage4_witness_python.py) and
[its log](/audit-output/evidence/stage4-python-witnesses.log):

- `[]` gives `[]`;
- `[1,-2,3,2]` gives `[1,1,3,3]` in both trusted canonical and candidate
  Python; and
- loop state `A=[1], M=1, D=1, IS=[2,-1,3]` ends with
  `A=[1,2,2,3], M=3, D=3`.

The return reference is not free: the postcondition fixes its exact heap
payload and all relevant allocation/call state. The theorem is neither a
tautology nor a one-way implication standing in for equality.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The reviewer-authored inventory is:

- [rule_inventory.py](/audit-output/evidence/rule_inventory.py)
- [complete inventory](/audit-output/evidence/rule-inventory.tsv)
- [inventory command/status](/audit-output/evidence/rule-inventory.stderr)

It enumerates every module/import/require, configuration, syntax declaration,
context, rule, and positive claim in `semantics.k`, all supplied helper K files,
`verification.k`, and the positive connection/spec files. Totals are 1,148
entries: 233 syntax declarations, one configuration, five contexts, 714 rules,
and five positive claims. Source attributes include 113 `total` declarations,
22 `no-evaluators` opaque declarations, 47 priority entries, one
simplification rule, and no local source `[functional]` declaration (the K
compiler generates functional axioms for function symbols).

Every inventory row has an exact location, normalized source, block hash, and
one of these dispositions:

- reviewed on the intended integer-list execution path;
- reviewed proof-local definition/lemma/bridge;
- positive claim/module wiring; or
- fixed rule with no constructor match on any intended execution, explicitly
  not globally blessed.

The 22 opaque declarations are float, sort, or MD5 primitives. None of their
constructors/callees occurs in the exact submitted body or any proof summary, so
none can affect a branch, state, returned value, or postcondition here.

The exact mapping from every submitted constructor to declarations, execution
rules, evaluation order, cells, and proof role is
[construct-map.md](/audit-output/evidence/construct-map.md). The reviewed path
accounts for module loading and the inert typing import, closure binding/call,
left-to-right lookup/evaluation, list allocation/truthiness/indexing/iteration,
integer comparison, assignments, in-place append, return, call-frame unwind,
all allocation/state cells, and priorities.

### Proof-local equations and lemma

`verification.k` contributes exactly 19 rules:

1. `allInts` has empty/cons structural cases. It says exactly that every
   element is in K's `Int` subsort.
2. The sole simplification inverts `isInt(V) = true` into an existential
   integer injection. The fresh compiled KORE contains exactly two generated
   sort-predicate cases: `isInt(inj{Int,KItem}(I)) = true` and an `owise`
   false case. The evidence excerpt is
   [stage5-isint-kore-axioms.log](/audit-output/evidence/stage5-isint-kore-axioms.log).
   Therefore the inversion cannot manufacture a non-integer or choose an
   integer value; it only exposes the existing injected one.
3. `stepMax`'s `I > M` and `I <= M` guards are disjoint and exhaustive over
   mathematical integers, and their right sides are exactly the source branch.
4. `rollAcc` has empty, integer-cons, and `owise` non-integer cases; the
   intended bridge domain reaches only the first two. Recursion strictly
   descends on the tail. Its update is the fixed append equation
   `valSeqConcat(A, singleton(stepMax(...)))`.
5. `rollingMax` has empty, integer-head, and off-domain `owise` cases. On the
   formal domain it starts `rollAcc` at the first integer and processes that
   integer once, yielding it unchanged as the first output.
6. `foldMax` and `lastOr` have exhaustive structural totalizations and descend
   on the tail. Their intended-domain equations exactly track final
   `current`/`number`.

The arbitrary off-domain totalizations do not replace execution: both entry
claims exclude non-integer elements, and the loop bridge is guarded by
`allInts(IS)`. No false global Python equation is used as a rewrite of program
execution.

An audit-only attempt to prove the sort inversion without the simplification
does not close—the fixed theory does not automatically derive the existential,
which is why the explicit lemma is operationally useful. One bare predicate
form also exposed a backend sort-variable diagnostic. These were supplemental
diagnostics, not target claims; their exact nonzero outcomes are retained in
the three `stage5-kprove-isint*.log` files, with the corresponding
[bare existential](/audit-output/evidence/isint-spec-bare-existential.k),
[unbound-RHS diagnostic](/audit-output/evidence/isint-spec-unbound-rhs.k), and
[existential reachability form](/audit-output/evidence/isint-spec-existential-reachability.k)
preserved. Static inspection of the generated
true/false `isInt` axioms establishes the lemma's truth.

### Operational bridges

The two priority-40 operational rules are not oracles:

- The `#bindTgt(Name(X), I:Int)` specialization changes only the active scope
  map entry and preserves the arbitrary continuation and every omitted cell.
  `BIND-SPEC` proves that universally framed transition using only
  `VERIFICATION-SUMMARIES` plus fixed semantics.
- The `#loop` bridge accepts the exact translated target/body, exact
  `.Stmts ~> Return(Name("result")) ~> #endcall` continuation, exact call
  frame/scopes/heap/counters/control cells, and `allInts(IS)`. Its right side
  introduces no abrupt return or unwinding; it only removes the completed loop
  and updates the three explicitly tracked values.

[stage5_bridge_context.py](/audit-output/evidence/stage5_bridge_context.py) and
[its log](/audit-output/evidence/stage5-bridge-context.log) show:

- the complete normalized loop rule domain/transition is text-identical to the
  bridge-free connection claim;
- binding term/frame, environment, scope update, and guard agree;
- the fresh bind definition excludes both bridges;
- the fresh loop definition includes the separately proved binding bridge but
  excludes the loop bridge; and
- only the final verification definition includes both.

The bridge-free binding and loop connection proofs are the first two fresh
`#Top` results in Stage 3. There is no circular use of the rule being justified
and no opaque value shared circularly between execution and postcondition.

Operational body sensitivity was rerun against the clean loop definition:
replacing the actual loop comparison term `>` with `<` while keeping the
rolling-maximum obligation exits 1 with a meaningful inductive residual
relating different `foldMax` and `rollAcc` values:
[body-mutation log](/audit-output/evidence/stage5-kprove-body-mutation.log).
For the satisfying substitution `M=0, I=1, R=.ValSeq`, the mutated body keeps
0 while the claimed `stepMax` value is 1. The mutated constructor cannot match
the `>` bridge.

No reviewed rule enables a false conclusion on the intended input domain, so
there is no unsoundness claim requiring a false-conclusion witness. Unreached
generic rules are reported as a narrower global evidence gap, not mislabeled
unsound.

## 6. Fresh non-vacuity test

I did not rely on candidate `spec-vacuity.k`. The fresh mutation is
[fresh-false-result.k](/audit-output/evidence/fresh-false-result.k). It uses the
satisfying ground input `[1,-2,3,2]`, keeps the exact submitted closure/call,
and changes only the result-bearing heap obligation from the real
`[1,1,3,3]` to `[1,1,4,4]`.

- `kprove ... --dry-run` exits 0, proving the mutation parses, imports, and
  builds: [dry-run log](/audit-output/evidence/stage6-false-mutation-dry-run.log).
- The real `kprove` exits 1 with `WarnStuckClaimState`. The terminal
  configuration has `ref(0)` and heap payload exactly `[1,1,3,3]`, which does
  not unify with the demanded result:
  [proof log](/audit-output/evidence/stage6-false-mutation-kprove.log).

This is the expected unmet result obligation, not a parser error, missing
import, timeout, unrelated crash, or unreachable mutation.

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Under the supplied MPY semantics, for every finite K `ValSeq` consisting of
mathematical integers:

- calling the exact submitted `rolling_max` closure terminates symbolically to
  a returned fresh reference in the proved reachability relation;
- that reference's heap object is exactly the transparent `rollingMax` fold of
  the input;
- `rollingMax` appends, at every position, the larger of the preceding maximum
  and current integer; and
- the empty/nonempty claims together cover the entire unbounded source-contract
  domain, while constraining observable call/allocation/exception state.

As a Kit reachability theorem, this is reported as partial correctness: no
separate liveness, complexity, resource-exhaustion, or CPython implementation
theorem is claimed.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| Byte-identical supplied MPY semantics | All K execution/proofs | Required trusted execution model. Used constructors and effects were statically reviewed; unused opaque/generic features cannot match this program. |
| K 7.1.293 parser/compiler/Haskell/LLVM backends and builtin mathematical Int/Bool/Map/List theories | Machine checking and primitive arithmetic/data structures | Normal low-level proof checker trust boundary. Fresh dual-backend reconstruction reduces, but cannot eliminate, toolchain trust. |
| Trusted `py2mpy.py` and CPython AST parsing | Source-to-`solution.mpy` identity | Required empirical/mechanical bridge. Regeneration is byte-identical; expanded constructor comparison pins the claims to that term. |
| K generated `isInt` sort predicate | `allInts` inversion during loop proof | Acceptable generated sort boundary. Fresh KORE shows true exactly on injected `Int` and false otherwise; the proof-local simplification adds no oracle value. |
| Modeling an external read-only `List[int]` argument as unboxed `list(ValSeq)` | Entry claim domain | Explicit convention of the supplied semantics. It preserves all behavior used here because the program does not mutate or return the input object; concrete heap-backed arguments follow the same dereference rules. |
| Transparent `stepMax`/`rollAcc` definitions and ordinary induction identifying them as prefix maxima | Human-language property | Acceptable ordinary mathematics, not an opaque assumption. Equations are exhaustive on the formal domain and were checked with ground K/Python witnesses and broader differential evidence. |
| Trusted canonical Python during differential tests | Finite implementation-to-intent evidence only | Not used to close any K claim and not promoted to universal proof. |

There is no program-derived opaque symbol, empirical result oracle, task-answer
rewrite, bounded unrolling, fixed-size restriction, unconstrained returned
value, or unconnected operational shortcut in the theorem.

### Gate and verdict rationale

- Gate A (real-program soundness): PASS. Exact program/body pinning, complete
  state footprints, bridge-free context-contained connections, logical
  consistency, body sensitivity, satisfiable witnesses, and fresh
  non-vacuity all pass.
- Gate B (intent adequacy): PASS. Empty plus unrestricted nonempty integer-list
  claims cover the complete HumanEval domain, and the transparent result is
  exactly the prefix/rolling maximum.
- Gate C (trust/evidence auditability): PASS. Commands, source artifacts, exact
  statuses, outputs, assumptions, and finite-evidence limits are preserved.

VERDICT: PASS
LEGITIMACY: LEGIT
