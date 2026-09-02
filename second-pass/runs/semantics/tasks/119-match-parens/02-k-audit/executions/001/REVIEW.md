# Adversarial audit: 119-match-parens

This is an independent audit in `SUPPLIED_SEMANTICS` mode. I treated every
candidate artifact as untrusted, copied source-only inputs to
`/tmp/audit-work/audit-119-match-parens`, rebuilt from scratch, and did not use
the candidate's `kore-exec.tar.gz`, `__pycache__`, or any candidate-built
definition.

The reconstructed claims do print `#Top`, and the Python implementation is
correct on extensive differential tests. Nevertheless, the K proof is not
legitimate. A proof-local control rule accepts an arbitrary returned value and
then ignores it, selecting the branch from a separately supplied mathematical
sequence. A fresh machine-checked witness shows this extension chooses THEN
for an empty/falsey returned string while the supplied semantics' native `If`
chooses ELSE for that exact value. The entry claim also invokes manually
defined closure/body aliases rather than executing the submitted
`solution.mpy` module; the proof still closes while that file is absent.

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode and mounts are consistent:

- `/reference/reference-semantics` exists.
- `diff -ruN --no-dereference` between the trusted and candidate
  `reference-semantics/` trees exited 0.
- Both trees contain the same directory and 25 regular-file entries. Neither
  tree contains a symlink. There are no missing, additional, mistyped, or
  changed entries in the candidate semantics tree.
- The candidate's `prompt.py` and `py2mpy.py` are byte-identical to the trusted
  mounted versions.

The exact checks, inventories, file types, tool versions, and exits are in
`/audit-output/evidence/stage1_integrity.log` and
`/audit-output/evidence/stage1_sources.log`. K was independently available as
version `v7.1.337`.

### Provenance artifacts

All four specifically requested generation records are absent:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`

No structured trace or JSONL trace was present. These are provenance failures
and leave no generation narrative to corroborate, but they did not prevent
source-level reconstruction. `PROOF.md` and a candidate vacuity spec were also
absent. The candidate did include `prove.sh`, which was read only as an
untrusted claim about the intended commands.

`semantic.k`/`semantics.k` is correctly absent at the candidate root for this
mode; the applicable supplied entry file is
`reference-semantics/semantics.k`.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The trusted prompt and canonical implementation specify a list containing
exactly two strings, each made only of `(` and `)`. Return `"Yes"` exactly when
one of the two concatenation orders is balanced: every prefix has nonnegative
balance and the final balance is zero. Otherwise return `"No"`.

`solution.py` implements that contract. `is_good` scans a concatenated string,
adds one for `(`, subtracts one otherwise, rejects a negative prefix, and
returns truthy `"T"` exactly at final balance zero. `match_parens` tries both
orders and returns the required `"Yes"`/`"No"`. Its “otherwise is a closing
parenthesis” behavior is adequate because the intended domain contains only
the two parenthesis characters.

### Translator identity

I ran the trusted `/reference/py2mpy.py` over the scratch copy of
`solution.py`. The regenerated output is byte-identical to submitted
`solution.mpy`; both have SHA-256
`a6071588cfead0d98f814794ceb72ffda603737241e408b1bbee3a57d0e71b03`.
Commands and exits are in `/audit-output/evidence/stage2_fidelity.log`.

### Independent differential test

`/audit-output/evidence/differential_match_parens.py` independently imports
`/reference/canonical.py` and the scratch candidate implementation. It also
uses a separately written balance oracle. The test covers:

- both documented examples;
- targeted empty, long, prefix-negative, unmatched, first-order-only,
  second-order-only, both-order, and neither-order cases;
- every pair drawn from all 255 parenthesis strings of length 0 through 7;
- 5,000 deterministic random pairs with component lengths 0 through 128.

It checked 70,012 distinct pairs with zero mismatches. All four behavioral
buckets were exercised: 83 both-order, 1,107 first-only, 1,105 second-only,
and 67,717 neither-order cases. The command exited 0; complete output is in
`stage2_fidelity.log`. This is strong finite evidence for implementation
fidelity, not a substitute for the K proof.

## 3. Clean proof reconstruction

The scratch target did not exist before this audit. I copied:

- candidate `solution.py`, `solution.mpy`, `spec.k`, `verification.k`, and
  concrete test source;
- trusted `py2mpy.py`, prompt, canonical implementation, and supplied semantics.

No compiled candidate directory or cache was copied.

Fresh build results:

- LLVM compilation of trusted `reference-semantics/semantics.k`: exit 0.
- `krun concrete-tests.mpy --output none`: exit 0.
- `krun solution.mpy --output pretty`: exit 0; the final module scope contains
  closures whose printed bodies match the translated functions.
- Haskell compilation of `verification.k`: exit 0.

The complete commands and bounded outputs are in
`/audit-output/evidence/stage3_build.log`.

Every positive claim was then run independently in the candidate's modular
order:

| Claim under proof | Previously proved claims supplied as trusted lemmas | Result |
|---|---|---|
| `loopCorrect` | none | exit 0, `#Top` |
| `loopFirstCorrect` | `loopCorrect` | exit 0, `#Top` |
| `isGoodCorrect` | `loopCorrect`, `loopFirstCorrect` | exit 0, `#Top` |
| `goodBranchCorrect` | none | exit 0, `#Top` |
| `matchParensCorrect` | the four preceding claims | exit 0, `#Top` |

The exact five commands and outputs are in
`/audit-output/evidence/stage3_claims.log`. Thus clean verification succeeds
under the candidate-extended theory. The later static audit shows that theory
is unsound.

## 4. Adequacy and real-program pinning

### Claims in plain language

1. `loopCorrect` says that, from a real `#loop` state with an existing `char`
   local and nonnegative balance `B`, scanning remaining string `S` and then
   running the helper epilogue returns `goodValue(S,B)`, pops the helper frame,
   and restores the caller continuation, environment, scope allocation, and
   stack.
2. `loopFirstCorrect` states the same fact at loop entry before the first
   iteration has created `char`.
3. `isGoodCorrect` says applying the manually defined `isGoodClosure` to any K
   string produces `goodValue(S,0)` while preserving the caller's framed state,
   provided the next scope location is fresh.
4. `goodBranchCorrect` says the synthetic `#forceGood` driver, when followed by
   `goodValue(S,B)` and `#goodBranch`, chooses the same supplied branch as
   mathematical `goodFrom(S,B)`.
5. `matchParensCorrect` says applying the manually defined
   `matchParensClosure` to a bare two-string K list returns
   `expectedAnswer(A,B)`. Its input strings are restricted by `parensOnly`;
   the module binding of `is_good` is pinned to `isGoodClosure`; and scope
   freshness is required.

The entry postcondition is result-constraining. `expectedAnswer` has disjoint
Yes/No equations guarded by a Boolean condition and its negation. Stage 6
confirms a false result is rejected.

### Satisfiable precondition and ground substitutions

A concrete entry state exists with:

- `BASE = .Map`, `MODULELOCALS = .Map`, `CALLER = 0`, and `N = 1`;
- scope 0 containing only `is_good |-> isGoodClosure`;
- empty heap and stack, `noRet`, `NoExc`, and exit code 0.

Then `N >= 1`, `N+1` is absent from `BASE`, and `N` is absent from
`BASE` plus scope 0. With `A=B=.IntSeq`, `parensOnly` is true. This witnesses
all entry guards.

`/audit-output/evidence/concrete_claim_witnesses.py` substitutes six ground
inputs, including `["",""]`, both one-way orders, both documented examples,
and No cases. For each, the claimed `expectedAnswer`, trusted canonical Python,
and generated Python agree. The state and results are recorded in
`stage4_adequacy.log`.

### Failure to execute/pin the submitted MPy artifact

The entry `<k>` cell does not contain the submitted `Module(...)` term or load
`solution.mpy`. It starts at:

`#applyK(toCall(matchParensClosure), ...)`

`matchParensClosure`, `matchParensBody`, `isGoodClosure`, and `isGoodBody` are
proof-local definitions manually transcribed in `verification.k`. Static
comparison and the concrete module-load output show that these aliases match
the current translated bodies, so I found no current behavioral mismatch.
However, there is no K claim connecting module loading from the submitted MPy
term to these aliases, and no build input reads `solution.mpy`.

As a direct sensitivity check, I temporarily moved the scratch
`solution.mpy` out of the directory and reran the complete positive proof. It
still exited 0 with `#Top`; the file was then restored and rechecked against
the submission. See
`/audit-output/evidence/stage4_program_file_sensitivity.log`.

Under the audit's explicit requirement that the `<k>` cell execute the actual
submitted MPy program, this is a substituted-closure proof with an informal
transcription bridge, not formal real-artifact pinning.

## 5. Rule-by-rule static soundness review

### Exhaustive inventories and selected semantics

The raw line-by-line inventory is in
`/audit-output/evidence/stage5_inventory_and_witness.log`. It enumerates every
syntax declaration, configuration, context, rule, claim, and relevant
attribute in all supplied semantics files, `verification.k`, and `spec.k`.

The supplied tree contains 227 syntax-declaration lines, 695 rule lines, five
context lines, and one configuration. Because this is
`SUPPLIED_SEMANTICS`, those rules are the fixed selected semantics rather than
candidate proof extensions. The candidate tree is byte-identical to that
trusted baseline; all 695 are therefore accepted at the selected semantics
level. Unused float, sorting, digest, dictionary, and other opaque/total
primitives are present in the fixed definition but are not reached by this
program's positive proof.

The used program constructs map to the supplied semantics as follows:

| MPy construct | Declaration and behavior used |
|---|---|
| `Module`, statement lists | `syntax.k`; load/sequencing in `core.k` |
| `FuncDef`, `Call`, `Return` | `functions.k` and `call.k`; closure creation, left-to-right callee/argument evaluation, frame push/pop |
| `Name`, `Int`, `Str` | declarations in `syntax.k`; lookup/literals in `core.k` and `str.k` |
| `Assign`, `AugAssign` | `controls.k`, with integer `+`/`-` in `int.k` |
| `For` | `controls.k`'s `#loop`; string iteration in `str.k` through `iter.k` |
| `If` | strict declaration plus `truthy`/`#branch` in `core.k` and `controls.k` |
| `Compare` | contexts/dispatch in `operators.k`; string and integer cases in `str.k`/`int.k` |
| `Subscript` | contexts and `applyIndex` in `subscript.k`; the entry list is exactly two elements, so indices 0 and 1 reduce in bounds |
| string `BinOp("+")` | strict `BinOp` dispatch in `operators.k`, `seqConcat` in `str.k` |

The configuration accounts for `<k>`, current environment, scope map and
allocator, heap and allocator, call stack, return state, exception state, and
exit code. The positive claim frames or explicitly transforms all of them.

### Candidate-local declaration inventory

`verification.k` has 11 syntax-declaration lines and 45 rules. It has nine
function declarations, three of them `[total]`; no candidate-local
`functional`, `concrete`, `symbol`, or opaque declaration; 20 priority-40
rules; and two simplification rules.

The declarations are exhaustive by source range:

- lines 96-99: four synthetic call/branch K items;
- line 156: `#expectedBranch`;
- lines 336, 346, 356: three statement-body functions;
- lines 373, 377: two closure functions;
- lines 384, 395, 410, 415: `goodFrom`, `goodValue`, `parensOnly`, and
  `expectedAnswer`.

### Candidate-local rule decisions

The following groups account for every one of the 45 candidate rules:

| Rules in `verification.k` | Count | Class and decision |
|---|---:|---|
| lines 8 and 15 | 2 | Fresh map insertion/deletion simplifications. True under their freshness guards. |
| lines 21, 31, 44, 57 | 4 | Fused literal assignment, integer updates, and `For` lookup. Each is the exact supplied strictness/lookup/operator sequence in a plain frame. Sound on its full guard. |
| line 69 | 1 | Operational frame-entry bridge. With `GOOD == isGoodClosure` and fresh `N`, it is the exact closure-call, parameter-bind, balance-assignment, frame, and allocator transition. Static expansion preserves every affected cell. Sound, though no separate bridge-free connection artifact was supplied. |
| lines 101 and 122 | 2 | Operational call/branch bridges. They pin the list and global binding, but skip argument evaluation and the helper call, replacing it with `#runIsGood`. They also omit the helper allocator's freshness/state footprint. Not sound on their complete match domain. Concrete symbolic witness: let the omitted `<scopeLoc>` be 2 and let scope key 2 already contain a sentinel. Fixed `call.k` overwrites key 2 for the helper and `functions.k` then deletes it at pop; these rules leave the sentinel scope unchanged. Their arbitrary continuation can observe that difference. The standard initial-state invariant avoids this witness, but the global rules have no such guard, and globally false proof rules cannot be justified as “unreachable.” |
| line 144 | 1 | Program-derived result summary `#runIsGood(S) => goodValue(S,0)`. `goodValue` is truthfully defined, and `isGoodCorrect` separately proves the helper result under the same extended module. But this rule is an axiom-like operational bridge, not an application of a bridge-free universal connection theorem. It is at least an unclosed connection obligation. |
| line 146 | 1 | **Unsound control bridge.** It accepts arbitrary `V:Val` and moves to a driver that chooses from `S`, without requiring `V == goodValue(S,0)` or even requiring `truthy(V) == goodFrom(S,0)`. |
| lines 149, 152, 157, 160 | 4 | The two literal-string `#goodBranch` rules and two Boolean `#expectedBranch` rules are individually faithful. |
| lines 167, 172, 180, 188 | 4 | **Unsound as globally installed branch-driving rules.** Every left side accepts `_V` and discards/replaces it. Their equations for scanning `S,B` are mathematically correct, but their conclusion about which continuation to execute need not agree with the actual supplied `V`. |
| line 201 | 1 | Literal-return fusion. It is the supplied strict literal evaluation followed by the supplied abrupt `Return` rule; it sets the same return cell and `#pop`. Sound. |
| lines 210-269 | 6 | Three true/false comparison pairs. Exact local bindings and guards make them equivalent to lookup, string/int literal evaluation, and supplied comparison hooks. Sound. |
| lines 272-332 | 6 | The corresponding direct `If` pairs. Same exact binding/guard reasoning and same selected branch as supplied strict `If`. Sound. |
| lines 337, 347, 357 | 3 | Statement-body definitions. They exactly transcribe the current `solution.mpy` bodies, but are only manually tied to that artifact. Their equations themselves are truthful definitions. |
| lines 374 and 378 | 2 | Closure definitions over those exact body aliases and definition scope 0. Truthful definitions, subject to the program-pinning gap above. |
| lines 385-386 | 2 | `goodFrom`. Exhaustive, disjoint by sequence shape, structurally decreasing, and mathematically equal to the implementation's scan. Sound. |
| lines 396 and 401 | 2 | `goodValue`. Exhaustive and structurally decreasing; returns `"T"`/empty exactly as `is_good`. Sound. |
| lines 411 and 412 | 2 | `parensOnly`. Exhaustive, decreasing, and equal to the intended character-domain predicate. Sound. |
| lines 416 and 419 | 2 | `expectedAnswer`. Guards are a Boolean and its negation, hence disjoint and exhaustive; results match the contract. Sound. |

Counts in the table sum to all 45 rules.

### Required false-conclusion witness for the unsound branch rules

I created `/audit-output/evidence/force-branch-witness.k` and
`force-branch-witness-spec.k`, rebuilt a fresh Haskell definition, and checked
two ground claims:

1. Candidate extension:
   `str(.IntSeq) ~> #forceBranch(.IntSeq, THEN, ELSE)` reaches THEN.
2. Supplied native behavior:
   `If(str(.IntSeq), THEN, ELSE)` reaches ELSE.

Both claims exit 0 with `#Top`; see
`/audit-output/evidence/stage5_force_branch_witness_v2.log`.

This is a concrete false conclusion witness. `S=""` makes the mathematical
scan true, but the actual `V=""` is falsey. Lines 146 and 167 ignore `V` and
select THEN; native `truthy(str(.IntSeq))` selects ELSE. The rule can therefore
enable a false control-flow conclusion over its admitted domain. The fact that
the target path normally places the matching `goodValue` beside it does not
repair a globally installed false rule.

This is a Gate A failure under the required proof-extension soundness
contract.

## 6. Fresh non-vacuity test

There was no candidate `spec-vacuity.k`.

I first tried a universal mutation replacing the entry result with `"Wrong"`.
It parsed and dry-ran successfully, but live proof search reached an unrelated
unsupported Haskell float hook. Per the audit instructions, I discarded that
run as non-vacuity evidence; it is retained transparently in
`/audit-output/evidence/stage6_nonvacuity.log`.

I then created the ground mutation
`/audit-output/evidence/spec-vacuity-ground.k` at the satisfying intended input
`["", ""]`. It keeps the real entry invocation and deliberately changes only
the result obligation to `"Wrong"`.

- `kprove --dry-run`: exit 0, so the mutation builds and the claim is reachable.
- Live `kprove`: exit 1 with `WarnStuckClaimState`.
- The residual is the actual value `"Yes"` as codes `89,101,115`, with all
  other ground state restored. It cannot unify with the `"Wrong"`
  postcondition.

Commands and the complete residual are in
`/audit-output/evidence/stage6_nonvacuity_ground.log`. This is valid
non-vacuity evidence: the entry result is constrained and a false result is
rejected for a satisfiable input. It does not cure the unsound proof rules.

## 7. Proven versus assumed accounting

### What the successful `#Top` establishes

Only under the theory consisting of the supplied MPy semantics plus all 45
rules in `verification.k`, the modular reachability run establishes:

- the two loop-summary claims;
- the helper-closure summary;
- the synthetic mathematical branch claim; and
- the manual `matchParensClosure` returns `expectedAnswer(A,B)` for
  parenthesis-only sequences and the stated scope conditions.

Because that extended theory contains the demonstrated false control bridge,
this closure is not a sound partial-correctness proof of the real program.

### Trust and assumption ledger

| Boundary | Influence | Assessment |
|---|---|---|
| Supplied, byte-matched MPy semantics | All execution, state, call, and value behavior | Authorized fixed semantics for this audit. Relevant rules were mapped above. |
| K integer, Boolean, string, map, and list hooks | Balance arithmetic, character codes, maps, sequences | Ordinary low-level trust boundary. All target uses are ground or structurally constrained. |
| Unused supplied opaque/total float, sort, digest, and collection helpers | None on the positive target path | Present in the imported fixed theory but not a value/control dependency of the target proof. |
| Four claims marked `--trusted` during the final modular run | Final entry closure | Not merely assumed overall: each was independently rerun and closed with `#Top`. Their proofs still inherit the unsound global extension. |
| `goodFrom`, `goodValue`, `parensOnly`, `expectedAnswer` | Final result and domain | Fully defined by exhaustive, decreasing, disjoint equations; mathematically acceptable. |
| Operational bridges at lines 69, 101, 122, 144, 146-196 | Calls, result, and branch control | Material proof-local trust. Lines 146-196 are concretely false on their match domain; lines 101/122 also omit an admitted allocator/state case. Illegitimate. |
| Manual body/closure aliases | Identity of the theorem's program | Static audit shows current textual equivalence, but no K module-load/connection claim pins them to submitted `solution.mpy`. Material real-program gap. |
| Differential test | Python rewrite-to-canonical intent bridge on 70,012 cases | Strong finite evidence only; it neither proves the universal bridge nor validates false K rules. |
| Informal “balanced parentheses” reading of `goodFrom` | Natural-language intent | Direct structural mathematical correspondence and finite evidence, but not a separate K theorem. This would be acceptable if Gate A and pinning passed. |

The proof is non-vacuous and the generated Python is behaviorally correct, but
those facts cannot replace sound K execution. The concrete opposite-branch
witness and substituted-closure entry violate the decision boundary for a
legitimate proof.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
