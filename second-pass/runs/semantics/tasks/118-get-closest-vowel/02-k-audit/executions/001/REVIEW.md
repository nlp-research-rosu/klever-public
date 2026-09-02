# Independent adversarial review: 118-get-closest-vowel

The candidate rebuilds and its four submitted claims print `#Top`, but it is not
a legitimate proof of the generated program. The decisive defect is the
proof-local rule at `verification.k:87`: it replaces every recursive call with
the postcondition function `closestVowelSpec` instead of deriving that result
from execution. The rule is both circular and globally false over its own match
domain. Fresh bridge-removal, control-state, and body-sensitivity experiments
confirm that this rule is doing the essential proof work and can prove a false
program result.

## 1. Input and provenance integrity

The rendered mode and trusted mounts are consistent:

- The mode is `SUPPLIED_SEMANTICS`.
- `/reference/reference-semantics` exists as a real directory.
- `/candidate/reference-semantics` is also a real directory, contains no
  symlinks, and is recursively byte- and type-identical to the trusted tree.
  There are no missing, additional, changed, mistyped, or symlinked entries
  inside that tree.
- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`
  (SHA-256 `0eec1170...a296d`).
- `/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`
  (SHA-256 `406485ea...db16`).

The expected provenance records `/candidate/run-input.json`,
`metrics.json`, `codex-last.txt`, and `codex-output.log` are all missing. No
top-level structured trace was present. `PROOF.md` is also absent. These are
provenance/auditability omissions, not an infrastructure breach. The top-level
candidate additionally contains `__pycache__/solution.cpython-310.pyc`; it was
ignored and never copied into or used by the reconstruction.

The exact inventories, comparisons, hashes, filesystem types, and exit statuses
are in [stage1_integrity.log](/audit-output/evidence/stage1_integrity.log), produced
by [stage1_integrity.sh](/audit-output/evidence/stage1_integrity.sh).

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For a case-sensitive string containing English letters only, return the
rightmost internal vowel whose immediate neighbors are both consonants. The
first and last characters cannot qualify. Return `""` when there is no such
vowel. The prompt gives no maximum length.

The trusted canonical implementation scans indices `len(word)-2` down to `1`
and returns the first qualifying vowel encountered. The candidate instead
recursively solves `word[1:]`; if the tail has no answer, it checks the
leftmost three-character window. Ignoring interpreter recursion limits, that is
an extensionally equivalent right-to-left algorithm.

### Translator fidelity

In scratch, the trusted translator was run as:

```text
python3 trusted-py2mpy.py solution.py > regenerated-solution.mpy
```

It exited 0. `cmp` and `diff` both exited 0, and regenerated and submitted MPY
files share SHA-256 `6ffc5212...a6b6`. Thus the submitted `solution.mpy` is the
exact trusted translation of `solution.py`.

### Independent differential

[differential_test.py](/audit-output/evidence/differential_test.py) imports the
trusted canonical file and the scratch-copied candidate file independently. It
tested:

- all four documented examples;
- empty, lengths 1 and 2, qualifying/nonqualifying triples, rightmost-choice,
  and upper/lower-case branch boundaries;
- every string of lengths 0 through 5 over `aAEbBy`;
- 10,000 deterministic random ASCII-letter strings of lengths 0 through 40
  with seed 118;
- two patterns at each of lengths 900, 950, 975, 990, 995, 1000, 1001, 1100,
  and 2000.

There were 18,961 unique inputs and eight mismatches. Every short and generated
branch test agreed. The eight mismatches were the two length patterns at 1000,
1001, 1100, and 2000. On CPython 3.10 with recursion limit 1000, the candidate
raises `RecursionError`; the canonical function returns either `""` or `"a"`.
For example, on `"b" * 1000`, canonical returns `""`, while the candidate
raises `RecursionError`.

This is a real implementation-to-contract discrepancy because arbitrary-length
English-letter strings are in the stated domain. The supplied K model has
unbounded recursive call depth and therefore does not capture this CPython
boundary. Full commands, exit 1 for the detected mismatch, and the complete
bounded result record are in
[stage2_fidelity.log](/audit-output/evidence/stage2_fidelity.log). Every actual
input is preserved in
[differential_inputs.jsonl](/audit-output/evidence/differential_inputs.jsonl)
(18,961 lines, SHA-256
`b18b4028e111f9472e9611648fee01ca0262aa59749b6c484521816a78e986dc`).

## 3. Clean proof reconstruction

All source artifacts needed for execution were copied to
`/tmp/audit-work/run-118`. No candidate definition, cache, `.pyc`, or compiled
artifact was copied or reused. K was independently available as v7.1.337.

The concrete supplied semantics was freshly built with:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
krun concrete-tests.mpy --definition audit-runtime-kompiled
```

Both commands exited 0. `krun` ended in `.K`, `NoExc`, and exit code 0.

The proof definition was freshly built with:

```text
kompile verification.k --backend haskell \
  --main-module HUMAN-EVAL-118-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-proof-kompiled
```

It exited 0. The four positive claims were copied into distinct spec modules in
[independent-positive-claims.k](/audit-output/evidence/independent-positive-claims.k)
and run independently:

```text
kprove independent-positive-claims.k --definition audit-proof-kompiled \
  --spec-module AUDIT-CLAIM-EMPTY
kprove independent-positive-claims.k --definition audit-proof-kompiled \
  --spec-module AUDIT-CLAIM-ONE
kprove independent-positive-claims.k --definition audit-proof-kompiled \
  --spec-module AUDIT-CLAIM-TWO
kprove independent-positive-claims.k --definition audit-proof-kompiled \
  --spec-module AUDIT-CLAIM-THREE-PLUS
```

Each command exited 0 and printed `#Top`. This is successful verification under
the submitted extended theory, not yet evidence that the theory is sound. The
full bounded build and proof output is in
[stage3_reconstruction.log](/audit-output/evidence/stage3_reconstruction.log).

The LLVM build warned about nonexhaustive total functions in unrelated
`mapStrVS`, float, `joinCodes`, and `valSeqAt` cases. None is reached by this
program: it uses strings, integer lengths/indices, boolean control, and calls,
not floats, list mapping/joining/sorting, MD5, or `ValSeq` indexing. The
Haskell build warnings were unused variables only.

## 4. Adequacy and real-program pinning

### Claims in plain language

All claims start from a fully specified standard state: environment 0, the
function closure bound in module scope 0, the supplied builtins at scope -1,
fresh scope/heap locations, empty heap and stack, `noRet`, `NoExc`, and exit
code 0. There are no additional `requires` clauses.

1. The empty input returns the empty string.
2. Every one-code `IntSeq` returns the empty string.
3. Every two-code `IntSeq` returns the empty string.
4. Every sequence with at least three codes returns exactly
   `closestVowelSpec` of the entire sequence.

The four constructor patterns exhaust the algebraic `IntSeq` domain. The
postconditions constrain the returned string; the three-plus result is not a
free variable, tautology, or one-way implication. The formal domain is broader
than the prompt because its codes are arbitrary mathematical integers, not only
English-letter ASCII codes. On the intended English-letter subdomain that
broadening does not invalidate the stated result.

Concrete satisfying witnesses were independently substituted:

| Claim shape | Input | Formal result | Canonical | Candidate |
|---|---:|---:|---:|---:|
| empty | `""` | `""` | `""` | `""` |
| one | `"b"` | `""` | `""` | `""` |
| two | `"ba"` | `""` | `""` | `""` |
| three-plus qualifying | `"bab"` | `"a"` | `"a"` | `"a"` |
| three-plus empty | `"bbb"` | `""` | `""` | `""` |

Additional rightmost and documented witnesses also agree. The executable record
is [adequacy_witnesses.py](/audit-output/evidence/adequacy_witnesses.py), with
output in [stage4_5_static.log](/audit-output/evidence/stage4_5_static.log).

### Program pinning

The `<k>` cell does not load `solution.mpy`; it starts at a `Call` whose closure
is manually installed in `<scopes>`. The `getClosestBody` macro is, however, a
constructor-for-constructor match for the regenerated `solution.mpy` body:
the length guard, tail slice, recursive call, truthy result test, three string
membership tests, and returns all match in order. Therefore the outer call is
textually pinned to this submitted snapshot, albeit through duplicated K text
rather than direct loading.

The fatal gap is that the same is not true of recursive control flow. The outer
body executes only until it reaches `#applyK` for the recursive call. At that
point `verification.k:87-93` preempts the supplied function-call semantics and
returns the specification value directly. There is no helper reachability
claim executing the shorter body and no loop/recursion circularity in the spec.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[rule_inventory.tsv](/audit-output/evidence/rule_inventory.tsv), generated by
[rule_inventory.py](/audit-output/evidence/rule_inventory.py), contains every
top-level configuration, syntax declaration, context, rule, and claim from the
supplied semantics tree, `verification.k`, and `spec.k`, including complete
guards, cell patterns, and attributes. Excluding the header it contains:

- 232 syntax declarations;
- 713 rules;
- 5 evaluation contexts;
- 1 configuration;
- 4 reachability claims.

The supplied fixed baseline contributes 227 syntax declarations, 695 rules, 5
contexts, and the configuration. The proof module contributes 5 declarations
and 18 rules. There are no `[functional]` declarations. All `function`,
`total`, `macro`, `priority`, `owise`, `concrete`, `no-evaluators`, and
`simplification` attributes are recorded in the TSV. Each row has an explicit
review disposition.

Because the candidate semantics tree is byte-identical to the trusted supplied
tree, its baseline rules are the selected fixed operational model rather than
candidate proof extensions. Static tracing of the used path found:

| Submitted construct | Declaration and operative fixed rules |
|---|---|
| `Module`, `FuncDef`, `Params` | `syntax.k:56-61`; `core.k:124-127`; `functions.k:14-16` |
| `Call`, `Name` | `syntax.k:9-30`; lookup in `core.k:130-152`; argument evaluation in `core.k:185-191`; routing/frame allocation in `call.k:17-28,68-75` |
| `len(word)` | builtins binding in `core.k:157-181`; `builtins.k:20-24` |
| `If`, `Assign`, `Return` | strict declarations in `syntax.k:41-54`; `controls.k:7-15,45-48`; return/pop in `functions.k:78-91` |
| integer `<` | comparison evaluation in `operators.k:13-17`; integer case in `int.k:20` |
| string literals/truthiness | `str.k:13-17`; `core.k:207-213` |
| `and` | short-circuit contexts/rules in `bool.k:10-26` |
| string `in` / `not in` | dispatch in `str.k:28-29`; prefix/contains equations in `str.k:32-42` |
| `word[i]` and `word[1:]` | evaluation/index/slice rules in `subscript.k:11-120` |

This path evaluates left-to-right where required, resolves `len` and the
recursive function through ordinary scopes, allocates a call frame, binds
`word`, writes only the local `result`, and normally restores the environment,
scope location, stack, return state, and scopes on pop. The length guard protects
all three indices. No fixed opaque primitive influences this program.

The fixed semantics does declare opaque or totalized boundaries for other
programs: `sortVS`, `sortKeyVS`, `md5hexCodes`, and the float-family symbols
`intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `subF`, `divF`, `addF`,
`mulF`, `powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`,
`roundF`, `roundFN`, and `sqrtF`. They are exhaustively recorded in the
inventory and are unreachable here.

### Proof-local rules

The 18 proof-local rules were reviewed as follows:

- `getClosestBody` is an exact program-body macro.
- `isVowelCode` and `qualifyingTriple` are total, truthful equations over K
  integers.
- The seven `closestVowelSpec` equations are a terminating structural
  definition. The length-under-three overlaps agree on `.IntSeq`; the
  length-at-least-three guards split between nonempty tail result and empty tail
  result, then between qualifying and nonqualifying triples. They encode the
  desired mathematical result but do not by themselves prove program
  execution.
- The `Subscript(str(iCons(_,R)), Slice(1,None,None)) => str(R)` rule preempts
  the general slice machinery. Its result follows from `slStart=1`,
  `slStop=isLen(iCons(_,R))`, `slStep=1`, and `buildIS`, and it changes no
  state. The candidate supplies no separate bridge-free machine-checked
  connection theorem, so this is an evidence gap, not a claimed false rule.
- `vowelCodes` expands to exactly the ten ASCII vowel codes. The singleton
  `strContains` equation agrees with the fixed recursive substring rules on
  every integer code, including their overlaps.
- The three `isLen` simplifications are true for structural finite `IntSeq`
  values. The freshness-guarded Map update normalization is the corresponding
  Map equality. Their overlaps do not produce inconsistent right-hand sides.
- The recursive `#applyK` rule is rejected, as detailed next.

### Unsound recursive-call bridge and witnesses

The rule at `verification.k:87-93` matches:

```text
#applyK(toCall(closureVal("word", getClosestBody, 0)),
        (str(CS), .Vals))
```

inside any environment `L > 0`, under an arbitrary trailing continuation. It
immediately yields `str(closestVowelSpec(CS))`. It omits `<scopes>`,
`<scopeLoc>`, `<stack>`, `<ret>`, `<exc>`, heap cells, and any guard tying the
call to a normal active frame. It bypasses lookup/frame allocation, parameter
binding, the entire recursive body, return, and pop. Its value flows directly
into the caller's truthy branch and final postcondition.

There is no bridge-free universal connection theorem. The same
`closestVowelSpec` symbol is introduced both by this operational axiom and by
the destination of the target claim, so the purported induction is circular.
Removing only this rule and rebuilding succeeds, but the symbolic three-plus
proof fails with `WarnStuckClaimState`; see
[verification-no-recursive-bridge.k](/audit-output/evidence/verification-no-recursive-bridge.k)
and [stage5_bridge_audit.log](/audit-output/evidence/stage5_bridge_audit.log).

Two independent false-conclusion/sensitivity witnesses were preserved:

1. **Exact-rule control-state witness.** For the intended English input
   `"bbb"`, start the exact matched `#applyK` term at `env=1` with
   `<ret> retV(7) </ret>`. The candidate rule does not inspect `<ret>` and
   proves `#Top` for a fabricated empty-string result. With only the rule
   removed, fixed execution reaches `Return(str(.IntSeq))` but cannot apply
   `Return` or `#endcall`, because both require `noRet`; it is stuck with
   `retV(7)` and exits 1. This is a concrete false conclusion over the bridge's
   complete declared match domain. The artifacts and outputs are
   [bridge-retstate-witness.k](/audit-output/evidence/bridge-retstate-witness.k),
   [bridge-retstate-witness-no-bridge.k](/audit-output/evidence/bridge-retstate-witness-no-bridge.k),
   and [stage5_retstate_witness.log](/audit-output/evidence/stage5_retstate_witness.log).
   The witness is not a standard entry state, but a globally installed semantic
   rule must be valid on every state admitted by its own guard; unreachability
   from this spec cannot justify the false broader rule.
2. **Standard-entry body sensitivity.** A fresh mutation changes only the
   recursive base return from `""` to `"a"`. Real Python and fresh supplied
   `krun` execution both show that mutated `"bbb"` returns `"a"`. Nevertheless,
   the correspondingly body-pinned bridge theory still proves `#Top` for the
   false standard-entry claim that mutated `"bbb"` returns `""`, because the
   recursive base body is never executed. See
   [mutated-body-witness.py](/audit-output/evidence/mutated-body-witness.py),
   [verification-mutated-base.k](/audit-output/evidence/verification-mutated-base.k),
   [bridge-body-sensitivity-mutated.k](/audit-output/evidence/bridge-body-sensitivity-mutated.k),
   and [stage5_bridge_audit.log](/audit-output/evidence/stage5_bridge_audit.log).

Thus this is not merely a missing explanatory lemma. It is a result-bearing,
control-insensitive execution axiom that can make a false claim provable and
that assumes the essential recursive correctness conclusion.

## 6. Fresh non-vacuity test

The reviewer-authored [spec-vacuity.k](/audit-output/evidence/spec-vacuity.k)
uses the standard satisfiable entry state and the ground input `"bab"`. The
real, canonical, and formal result is `"a"` (code 97); the mutation asks for
the empty string.

First:

```text
kprove spec-vacuity.k --definition audit-proof-kompiled \
  --spec-module AUDIT-SPEC-VACUITY --dry-run
```

exited 0 and emitted the backend command, proving that the mutation parses and
lowers successfully. The actual proof command without `--dry-run` exited 1 with
`WarnStuckClaimState`. Its residual is exactly
`str(iCons(97,.IntSeq))`, which does not unify with the mutated empty result.
This is the expected unmet result obligation, not a parser error, missing
import, timeout, or unrelated crash.

The exact commands and residual are in
[stage6_nonvacuity.log](/audit-output/evidence/stage6_nonvacuity.log). This shows
that the final claim is discriminating; it does not establish that the
recursive computation used to reach the result is honest.

## 7. Proven versus assumed accounting

What the reconstructed `#Top` runs actually establish is:

> In the submitted **extended** transition system—which includes the
> recursive-call axiom—calls from the four standard symbolic entry shapes reach
> the result defined by `closestVowelSpec`.

They do not establish that supplied fixed execution of the submitted recursive
body produces that result.

| Boundary | Role and dependents | Assessment |
|---|---|---|
| K v7.1.337, Haskell backend, SMT/K builtins | Parses, rewrites, and discharges all claims | Ordinary machine-checking trust boundary |
| Byte-identical supplied reference semantics | Models MPY calls, strings, control, scopes, and state | Authorized fixed model; CPython recursion limits are outside it |
| Unused opaque float/sort/MD5 symbols | Trusted operations in the supplied language | Acceptable here because no submitted path or claim depends on them |
| `getClosestBody` duplicated macro | Pins the outer closure to this `solution.mpy` snapshot | Textually checked, but not direct file execution |
| `closestVowelSpec`, vowel predicates | Mathematical postcondition | Truthful structural definition; not an execution theorem |
| Tail-slice and singleton-membership rules | Accelerate fixed string operations | Mathematically consistent on the used domain; slice bridge lacks a submitted connection proof |
| Recursive `#applyK` rule | Supplies every recursive result and hence the final theorem | Illegitimate: circular, execution-bypassing, control-insensitive, and witnessed false |
| Differential and ground tests | Support implementation/intent and summary bridges on tested cases | Finite evidence only; they cannot replace the missing reachability proof |
| CPython recursion behavior | Connects the K model to the real generated Python | Material limitation: the candidate raises on valid long inputs while the model does not |

The successful positive reconstructions and successful false-postcondition
rejection therefore cannot support legitimacy. The proof closes only after
adding an unsound axiom that assumes the recursive result it is meant to prove.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
