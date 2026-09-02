# Independent adversarial review: 3-below-zero

The proof is legitimate under the supplied semantics, but the candidate package
has a provenance-integrity defect: four required generation artifacts are
missing. Independent reconstruction overcame that evidentiary gap. The formal
claims are non-vacuous, result-constraining, and pinned to the submitted
translated program; the only operational summary is justified by a separately
proved, bridge-free claim over exactly the same configuration.

This review used the required `using-kit` and `validating-proof` workflows. All
candidate prose, scripts, caches, archives, and claimed results were treated as
untrusted. All execution occurred in `/tmp/audit-work/rebuild`; no
candidate-provided compiled definition or cache was copied or used.

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `SUPPLIED_SEMANTICS`, and
`/reference/reference-semantics` is present, so the trusted mounts do not
contradict the rendered mode. The auditor's non-following recursive comparison
found 25 entries in the candidate semantics tree, all regular files or
directories, with identical names, types, and SHA-256 contents and no symlinks:
`RESULT exact_tree_match entries=25 symlinks=0`. See
[01_integrity.log](/audit-output/evidence/01_integrity.log) and the
[comparison script](/audit-output/evidence/compare_trees.py).

The following candidate inputs are regular files:
`solution.py`, `solution.mpy`, `spec.k`, `verification.k`, `prompt.py`, and
`py2mpy.py`. The candidate [prompt.py](/candidate/prompt.py:1) is byte-identical
to the trusted [prompt.py](/reference/prompt.py:1), and the candidate translator
is byte-identical to the trusted [py2mpy.py](/reference/py2mpy.py:1).

### Integrity failures

The following required untrusted-claim artifacts are absent:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`

No structured generation trace is present. These are provenance and
auditability failures, not an infrastructure breach: the trusted prompt,
canonical program, translator, and required supplied-semantics mount are all
present and usable. They are the reason for `CONCERNS` rather than `PASS`.

Candidate-provided `__pycache__`, `kore-exec.tar.gz`, `prove.sh`, and concrete
tests were ignored as proof authority. The exact scratch-copy procedure, which
copied only source artifacts needed for the audit, is recorded in
[02_prepare_scratch.log](/audit-output/evidence/02_prepare_scratch.log).
Tool versions and mode checks are in
[00_environment.log](/audit-output/evidence/00_environment.log): K
v7.1.337 and Python 3.10.12 were available.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

For an intended input `operations: List[int]`, begin with balance zero, process
the operations in order, and return `True` as soon as a running balance is
strictly negative. Return `False` if no prefix has negative sum. This is the
contract in trusted [prompt.py](/reference/prompt.py:4), and trusted
[canonical.py](/reference/canonical.py:8) implements exactly that loop.

Candidate [solution.py](/candidate/solution.py:4) has the same behavior. Its
extra initialization `operation = 0` is overwritten before each loop-body use
and is observationally irrelevant. Every path then performs the same addition,
strict-negative check, early `True`, and final `False` as the canonical
implementation.

### Translator identity

The trusted translator regenerated the submitted source successfully. The
regenerated and submitted MPY files were byte-identical, both with SHA-256
`5e9e907167be11a2f30b29f110fb940b866c050c1efacbb6f638a39bfc96bab5`.
The commands, exit statuses, and hashes are in
[02_fidelity.log](/audit-output/evidence/02_fidelity.log).

### Independent differential test

The reviewer-authored
[differential_test.py](/audit-output/evidence/differential_test.py) independently
imports the trusted canonical entry point and submitted generated entry point.
It exercised:

- both documented examples;
- empty input;
- immediate and delayed negative balances;
- cumulative-balance boundaries at `-1`, `0`, and `1`;
- exact-zero, one-above, and one-below boundaries;
- early negative followed by recovery;
- arbitrary-precision integer cases;
- every one of the 781 lists of length 0 through 4 over
  `[-2, -1, 0, 1, 2]`;
- 2,000 deterministic generated lists of length 0 through 40 with values from
  `[-10000, 10000]`, seed `0x3B310`.

All 2,795 executed cases are preserved in
[differential-inputs.jsonl](/audit-output/evidence/differential-inputs.jsonl).
The run exited 0 with `mismatches=0 canonical_errors=0 generated_errors=0`.
This is finite evidence for the Python-to-intent bridge, not a substitute for
the K proof.

## 3. Clean proof reconstruction

The audit built all definitions from the scratch source copy. It did not copy
candidate compiled directories, archives, or caches.

### Concrete definition

The LLVM definition was freshly built from
`reference-semantics/semantics.k` with main module `MPY-KRUN` and syntax module
`MPY-SYNTAX`; `kompile` exited 0. Running the actual submitted
[solution.mpy](/candidate/solution.mpy:1) exited 0 and ended with `.K`, the exact
closure body loaded in module scope, no exception, and exit code 0.

The reviewer-authored
[audit-concrete.py](/audit-output/evidence/audit-concrete.py) was translated
with the trusted translator and executed under the new LLVM definition. Its 11
normal, empty, branch-boundary, early-return, and large-integer assertions all
completed with `.K`, `NoExc`, and exit code 0. The concrete build and both runs
are recorded in
[03_reconstruct.log](/audit-output/evidence/03_reconstruct.log).

### Proof definitions and every positive target

Two proof definitions were built independently:

1. `MPY-VERIFICATION`, which contains the fixed supplied semantics plus the
   typed-list and mathematical definitions but no loop-summary bridge.
2. `MPY-VERIFICATION-LEMMA`, which additionally contains the separately proved
   loop-summary rule.

Both Haskell `kompile` commands exited 0. The only two positive target claims
in [spec.k](/candidate/spec.k:3) were then run:

- `AUX-SPEC` against the bridge-free base definition: exit 0 and `#Top`.
- `MAIN-SPEC` against the lemma definition: exit 0 and `#Top`.

Thus every positive target closes with the required success signal. Full
commands, bounded outputs, warnings, and exit statuses are in
[03_reconstruct.log](/audit-output/evidence/03_reconstruct.log).

LLVM emitted non-exhaustive-match warnings for broad supplied-semantics
functions unrelated to this program (`mapStrVS`, `floorFI`, `toF`, `ceilF`,
`joinCodes`, and `valSeqAt`). None is syntactically or dynamically reachable
from the submitted integer-list program or either proof claim. They therefore
do not establish a false conclusion witness on the intended domain.

## 4. Adequacy and real-program pinning

### `AUX-SPEC`

The precondition is a real function-frame loop head. The remaining iterator is
an arbitrary finite integer list `IS`; local `balance` is an arbitrary integer
`B`; local `operation`, the original `operations` binding, module map, builtins
scope, heap, and allocation counter are universally framed; the continuation is
exactly the submitted function's final `Return(false)` followed by `#endcall`;
the stack contains exactly its caller frame; and return, exception, and exit
states are normal.

The postcondition is the exact Boolean `prefixBelow(B, IS)`, with the call frame
popped and caller environment/scopes restored. In plain language: executing the
real remaining loop and final return produces `True` exactly when adding the
remaining operations to starting balance `B` first crosses below zero.

### `MAIN-SPEC`

The precondition is the canonical initial MPY configuration: empty module
scope, fixed builtins scope, no heap, no stack, normal return/exception state,
and the `<k>` computation
`#loadAll(solutionProgram) ~> Call(Name("below_zero"), list(asValSeq(IS)))`
for an arbitrary finite integer list `IS`.

The postcondition is exactly `prefixBelow(0, IS)`, not a free variable,
tautology, implication, or one-way relation. It also pins the loaded
`below_zero` binding to the exact submitted closure body and constrains all
observable configuration cells shown in the claim.

### Program identity and satisfying states

The trusted translator already established byte identity of `solution.mpy`.
Independently, `kast --expand-macros` produced byte-identical KORE for submitted
`solution.mpy` and proof-local `solutionProgram`; both had SHA-256
`63152660ba0e1143764d8d99dd1c5d29e44ecb5de982b0f99e865113e698f755`.
See [04_adequacy.log](/audit-output/evidence/04_adequacy.log). Therefore the main
claim executes the actual submitted translated program, not a substituted
algorithm.

Concrete satisfying witnesses exist:

- Main: `IS = [1, 2, -4, 5]` in the exact initial cells. The claim, trusted
  canonical Python, and submitted Python all return `True`.
- Main boundary: `IS = []`. All three return `False`.
- Auxiliary reachable loop head: full input `[5, -5]`, after consuming `5`,
  with `B=5`, remaining `IS=[-5]`, `operation=5`, empty module/heap, and the
  exact call frame. `prefixBelow(5,[-5])` and both Python functions return
  `False`.
- Auxiliary early-return head: `B=0`, remaining `[-1,100]`. The claim and both
  Python functions return `True`.

The exact symbolic witnesses and comparisons are in
[adequacy_witness.py](/audit-output/evidence/adequacy_witness.py) and
[04_adequacy.log](/audit-output/evidence/04_adequacy.log).

The formal domain is every finite list of K mathematical integers. This matches
the intended `List[int]` domain and Python's arbitrary-precision integer model.
The program only reads its input, so the semantics' permitted unboxed
read-only-list representation introduces no mutation or aliasing gap.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The reviewer rebuilt an inventory directly from the exact supplied source tree
and `verification.k`. The
[complete inventory](/audit-output/evidence/05_rule_inventory.md) contains
1,111 top-level entries: 703 rules, 233 syntax declarations, 5 contexts, 1
configuration, 28 modules, 28 end-module markers, 89 imports, and 24
file-level requirements. Multiline bodies and attributes—including
`function`, `total`, `macro`, `concrete`, `owise`, `symbol`,
`no-evaluators`, and priorities—are retained. There are no local
`functional` or simplification declarations.

The inventory distinguishes actual-program-path rules from unused parts of the
selected supplied baseline. The detailed
[construct map](/audit-output/evidence/05_construct_map.md) maps every AST
construct used by `solution.mpy` to its declarations and rules. The exercised
path was checked for configuration shape, left-to-right call/argument
evaluation, lookup and binding, local writes, integer addition and comparison,
loop iteration, early return, frame popping, exceptions, and all other cells.

### Proof-local rules

The three macro aliases in [verification.k](/candidate/verification.k:7) are
definitional only. Their fully expanded program term exactly matches submitted
KORE, as established above.

`IntVals` and `asValSeq` are a typed inductive representation of every finite
integer list. Their two iterator rules are disjoint, exhaustive over the
representation, and identical to the fixed list iterator's empty/cons behavior:
they expose one integer head and the exact remainder without changing any cell.
They do not introduce an oracle.

`prefixBelow` is the only proof-local `[function,total]` result-bearing symbol.
Its empty and cons equations are disjoint and exhaustive, and recursion strictly
descends the `IntVals` tail. The cons equation is ordinary mathematics: add the
head, return true when the new balance is negative, otherwise recurse with that
new balance. No overlap, uncovered constructor, non-descent, or unconstrained
interpretation exists.

The priority-40 loop rule is an operational bridge, but it is not an
unjustified answer rule:

- Its normalized full configuration is exactly the normalized `AUX-SPEC`
  reachability claim (611 characters each, exact match).
- `AUX-SPEC` imports only `MPY-VERIFICATION`, which contains no loop-summary
  bridge. Thus its universal connection theorem is bridge-free.
- The match and theorem have the same exact loop body, exact
  `Return(false) ~> #endcall` suffix, environment, complete scopes and sorts,
  `scopeLoc`, arbitrary preserved heap and heap counter, exact stack frame,
  return state, exception state, and exit code.
- Its arbitrary `INPUT`, module, builtins, heap, and counter do not broaden it
  beyond the theorem: the bridge-free claim universally quantifies those same
  values. The loop body reads only the bound iterator head and local balance.
- Priority changes which equivalent step is selected; it does not broaden the
  LHS.

The bridge-free auxiliary proof returned `#Top`, and
[compare_aux_bridge.py](/audit-output/evidence/compare_aux_bridge.py) records
`bridge_free=true` and `exact_match=true`.

### Operational sensitivity and context containment

The independent body mutation changed `balance += operation` to
`balance -= operation` at the satisfying state `B=0`, remaining `[1]`. The
mutated claim parsed successfully (`--dry-run` exit 0), fixed execution reached
`true`, and the old `prefixBelow(0,[1]) = false` destination became a genuine
stuck claim (exit 1). This shows the bridge-free theorem is sensitive to the
displaced program body.

The immediate continuation was separately changed from `Return(false)` to
observable `Return(true)` on an empty remainder. The bridge-free and
bridge-enabled definitions both proved `#Top` with result `true`. Therefore the
summary does not match a broader return suffix. Artifacts and exact outputs are
in [05_operational_sensitivity.log](/audit-output/evidence/05_operational_sensitivity.log),
with preserved
[body mutation](/audit-output/evidence/spec-body-sensitivity.k),
[base context test](/audit-output/evidence/spec-context-sensitivity-base.k),
and [lemma context test](/audit-output/evidence/spec-context-sensitivity-lemma.k).

### Opaque and unused supplied features

The supplied fixed semantics declares these `symbol(...)` operations:
`sortVS`, `sortKeyVS`, `md5hexCodes`, `intFloatDiv`, `divII`, `floatMod`,
`floatLt`, `absF`, `floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`,
`mulF`, `powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `intToF`,
`truncF`, `roundF`, `roundFN`, and `sqrtF`. Most are explicitly
`no-evaluators`; the remaining float conversion symbols have only restricted
equations and can remain symbolic. The structurally defined `strLt` can also
remain symbolic for non-constructor sequences.

None appears in the submitted AST, proof-local definitions, preconditions,
postconditions, or any reachable rule on this integer-list path. They influence
no branch, result, state, exception, or termination fact in either target
claim. The candidate did not add or modify them: the entire semantics tree is
the byte-identical selected supplied baseline. No rule was labelled unsound
without an intended-domain false-conclusion witness; for these unused broad
features, the narrower finding is only that their global Python fidelity is
outside this theorem and unnecessary to its legitimacy.

## 6. Fresh non-vacuity test

The fresh reviewer mutation changed the full `MAIN-SPEC` result from
`prefixBelow(0, IS)` to `notBool prefixBelow(0, IS)`. Empty input is a
satisfying, demonstrably false witness: the real result is `false`, whereas the
mutated destination is `true`.

The preserved [spec-vacuity.k](/audit-output/evidence/spec-vacuity.k) built
successfully with `--dry-run` (exit 0). Actual proof then exited 1 with
`WarnStuckClaimState`; the residual explicitly shows the unmet equality between
`notBool prefixBelow(0, IS)` and `prefixBelow(0, IS)`. This was not a parser
error, missing import, timeout, crash, or unreachable mutation. Commands and
the bounded residual are in
[06_nonvacuity.log](/audit-output/evidence/06_nonvacuity.log).

This establishes that the main proof genuinely constrains the returned Boolean.

## 7. Proven versus assumed accounting

### Precisely proven

Under the selected supplied MPY semantics, for every finite `IntVals` sequence
`IS`, starting from the exact initial configuration in `MAIN-SPEC`, loading the
actual submitted translated module and calling its actual `below_zero` closure
with `list(asValSeq(IS))` reaches the Boolean `prefixBelow(0, IS)` while
producing the stated final environment, scopes, heap, stack, return, exception,
and exit-code cells.

The bridge-free auxiliary reachability proof establishes that, from every
matching real loop-head frame and every integer balance `B`, the actual
remaining loop body, early returns, final false return, and frame cleanup reach
exactly `prefixBelow(B, IS)`. The defining equations make that Boolean true
exactly when some processed running balance is strictly negative. This is a
partial-correctness statement over the stated finite integer-list domain; it
does not claim behavior for inputs outside that domain.

### Trust and evidence ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| The byte-identical `/reference/reference-semantics` tree as the selected fixed MPY semantics | Both target claims and all concrete runs | Required trusted input in `SUPPLIED_SEMANTICS` mode. Its actually exercised integer/list/call/control subset was also statically and concretely checked. Acceptable. |
| K v7.1.337 parser, compiler, LLVM/Haskell backends, reachability logic, and built-in `Int`/`Bool` mathematics (`+Int`, `<Int`, Boolean conditionals, maps/lists) | Machine-checking and mathematical reduction | Ordinary toolchain/meta-theory trust boundary. Acceptable and explicitly versioned. |
| `IntVals`/`asValSeq` typed representation | Universal input domain and loop iteration | Not opaque or assumed: constructors and iterator equations are exhaustive and faithful. Acceptable. |
| `prefixBelow` | Auxiliary and main results | Not opaque or assumed: two exhaustive, disjoint, descending equations define the contract. Acceptable. |
| Loop-summary operational rule | Closure of `MAIN-SPEC` | Conditional on the prior auxiliary theorem, which was independently proved bridge-free over the rule's exact complete match domain. Body and continuation sensitivity passed. Acceptable derived lemma. |
| Proof macros for program/body terms | Program identity | Mechanical expanded-KORE identity with submitted `solution.mpy`, in addition to trusted-translator byte identity. Acceptable. |
| Supplied opaque symbols listed in Stage 5 | None | Unreachable and result-independent for this theorem. They remain part of the broad language trust boundary but do not support the proof conclusion. |
| Python differential testing | Candidate-to-canonical adequacy bridge on 2,795 recorded inputs | Finite empirical support only. It is not used as a universal K lemma. Static source inspection and the formal `prefixBelow` theorem supply the universal reasoning. |
| Concrete K assertions | Selected-semantics execution on 11 normal/boundary inputs | Finite evidence that the rebuilt concrete semantics follows the expected path. It does not replace either reachability proof. |
| Natural-language identification of `prefixBelow` with “some running balance is negative” | Human-facing intent | Direct structural reading of the two equations and the trusted canonical loop; informal but exact on finite integer lists. No material adequacy gap. |

### Excluded behavior and final assessment

The theorem excludes non-list inputs, non-integer elements, Python features
outside the supplied MPY subset, and behavior of unused float/sort/hash/string
primitives. It proves the submitted function, not Python's unrestricted dynamic
type behavior. Those exclusions agree with the stated `List[int]` task domain.

Gate A (real-program soundness and non-vacuity) passes. Gate B (intent adequacy)
passes. The reconstructed reviewer evidence is reproducible and complete, but
the candidate's four required provenance artifacts are missing. That packaging
defect warrants `CONCERNS`; it does not make the independently reconstructed,
sound, real-program proof illegitimate. The evidence manifest and source-copy
identity checks are in
[07_evidence_manifest.log](/audit-output/evidence/07_evidence_manifest.log).

VERDICT: CONCERNS
LEGITIMACY: LEGIT
