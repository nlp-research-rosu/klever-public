# Independent adversarial audit: 95-check-dict-case

## Executive finding

The candidate is **not a legitimate proof of the requested partial-correctness
property**, even though its proof reconstructs cleanly and both submitted claims
independently print `#Top`.

There are two independent, material defects:

1. `verification.k:67-71` adds a priority-30 `isinstance` rule that is not
   equivalent to the supplied semantics. On a satisfiable state admitted by
   `loop-and-return`, fixed semantics dereferences `ref(0)` to the string `"a"`
   and returns `true`; the candidate rule preempts dereference and returns
   `false`. Ground fixed and extended executions prove the opposite outcomes.
   Thus the rule enables a false auxiliary theorem.
2. The proof's case model is ASCII-only. Python's `str.islower` and
   `str.isupper` are Unicode-aware, and the prompt does not restrict keys to
   ASCII. For `{"é": 0}`, both Python implementations and the prompt contract
   return `True`, while the candidate's formal result reduces to `false`.
   This materially excludes part of the source-contract domain.

The fresh false-result mutation did fail for the expected unmet obligation, so
the proof is result-constraining rather than vacuous. That does not repair the
unsound proof extension or the domain gap.

## 1. Input and provenance integrity

The launcher declares `record_layout = legacy-selected-stage1` and
`semantics_mode = SUPPLIED_SEMANTICS`. The trusted
`/reference/reference-semantics` mount is present, so the rendered condition and
mount layout agree.

I read and checked:

- `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`, `/task.json`,
  and `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`, `usage.json`,
  `codex-last.txt`, `codex-output.log`, and `prompt.txt`;
- the one JSONL file under `/generation-evidence/codex-trace/`.

Historical runtime metrics are not required for this legacy layout. The
structured trace contains 355 valid JSON events and no malformed line.

Independent checks found:

- the campaign lock is JSON-identical to the `audit_campaign` block and has the
  recorded SHA-256;
- all recorded hashes for the canonical, prompt, translator, manifests,
  generation files, and trace file match;
- the mounted candidate manifest-tree hash is
  `55fa6fd2351c7fdab08319fe115ca88310669945ad8c0db11a2a8baa6796093f`,
  matching the finalized generation workspace hash;
- the trusted supplied-semantics manifest-tree hash is
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`,
  matching the recorded manifest hash;
- candidate and trusted semantics each contain the same 24 regular files,
  byte-for-byte, with no missing, extra, changed, non-regular, or symlinked
  entry;
- candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
  mounts;
- every required candidate source/proof artifact is present.

There is no infrastructure breach. Full commands, hashes, and checks are in
`evidence/01b-integrity-with-tree.log`; structured-trace inspection is in
`evidence/02-trace-summary.log`. Generation prose and prior build artifacts were
treated only as untrusted historical claims.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

From `/reference/prompt.py`, the intended function:

- returns `False` for an empty dictionary;
- otherwise returns `True` exactly when every key is a string and either every
  key satisfies Python `str.islower()` or every key satisfies Python
  `str.isupper()`;
- returns `False` for non-string, uncased-only, mixed-case, or mixed
  lower/upper key sets.

Digits and punctuation may occur inside a valid cased string, as in `"a1"` or
`"A1"`, because Python's case predicates inspect cased characters. Unicode
letters are also in the stated Python-string domain.

`solution.py` implements that contract by maintaining `has_key`, `all_lower`,
and `all_upper` across every dictionary key. It does not adopt the canonical's
early-exit bug.

### Translation identity

Fresh translation used the trusted copied translator:

```text
python3 /tmp/audit-work/trusted/py2mpy.py \
  /tmp/audit-work/work/solution.py \
  > /tmp/audit-work/work/regenerated-solution.mpy
```

The submitted and regenerated files are byte-identical, both with SHA-256
`02c470fff3f9967c3a4af5071971b6d09d8a48fd940ecb3a4e0888c7390fef04`.
The command exited 0; see `evidence/03-translator-byte-identity.log`.

### Independent differential testing

`evidence/differential_test.py` imports the trusted canonical and generated
entry points independently. It covers:

- all five documented examples;
- 19 empty, branch-boundary, non-string, cased/uncased, and Unicode cases;
- all key subsets of sizes 0 through 4 from a documented 15-key pool;
- 2,000 deterministic generated dictionaries with seed `950026`.

The 3,965 input/result records are in
`evidence/differential_cases.json` (SHA-256
`a008f571b4b05f69d7ab96cbf92fea3de8de1170def6a68d3fdc58122e4fcac4`).
There were zero generated-versus-prompt-contract mismatches, but 244
generated-versus-canonical mismatches. The differential command therefore
exited 1 and preserved the disagreements; see
`evidence/04b-differential-with-contract.log`.

The discrepancy is in the trusted canonical. Once it sees two same-case keys,
its final `else: break` can ignore all later keys. For example:

```text
{"a": 0, "b2": 1, "A": 2}
canonical=True, generated=False, prompt_contract=False
```

The generated result is correct under the natural-language contract. This
canonical/contract disagreement is recorded, not hidden or charged as a
candidate implementation bug. Concrete witness outputs are in
`evidence/32-python-witnesses.log`.

## 3. Clean proof reconstruction

All source needed for execution was copied to `/tmp/audit-work`. Candidate
`.build` and `__pycache__` content was not copied or reused. The copied
`reference-semantics` came from the trusted mount.

The available tools are K `v7.1.293`
(`evidence/06-k-toolchain.log`).

### Concrete definition

Fresh LLVM build:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition .audit-build/runtime-kompiled
```

Exit: 0 (`evidence/07-kompile-llvm.log`).

Fresh translation and execution of the inspected ASCII smoke program:

```text
krun .audit-build/smoke.mpy \
  --definition .audit-build/runtime-kompiled
```

Exit: 0, final `<k> .K </k>`, `<exc> NoExc </exc>`, and
`<exit-code> 0 </exit-code>` (`evidence/09-krun-ascii.log`).

An additional Unicode source witness executes successfully in CPython but
causes the supplied LLVM semantics to exit 113 at
`strToCodes("\xc3\xa9")` (`evidence/10-krun-unicode-witness.log`). This parser/
runtime failure is **not** used as non-vacuity evidence or as a failed positive
proof. It only corroborates the separately established Unicode modeling gap in
Stages 4 and 5.

### Proof definition and every positive claim

Fresh Haskell build:

```text
kompile verification.k --backend haskell \
  --main-module CHECK-DICT-CASE-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition .audit-build/verification-kompiled
```

Exit: 0 (`evidence/11-kompile-verification.log`).

All claims together:

```text
kprove spec.k --definition .audit-build/verification-kompiled \
  --spec-module CHECK-DICT-CASE-SPEC
```

Exit: 0, output `#Top` (`evidence/13-kprove-all.log`).

Each labeled claim was then selected independently:

```text
kprove spec.k --definition .audit-build/verification-kompiled \
  --spec-module CHECK-DICT-CASE-SPEC \
  --claims CHECK-DICT-CASE-SPEC.entry-reaches-loop

kprove spec.k --definition .audit-build/verification-kompiled \
  --spec-module CHECK-DICT-CASE-SPEC \
  --claims CHECK-DICT-CASE-SPEC.loop-and-return
```

Both commands exited 0 and printed `#Top`; see
`evidence/14-kprove-entry.log` and `evidence/15-kprove-loop.log`.

Removing only `verification.k:58-89`, which contains the six proof-only call
splitters, still built successfully, but `loop-and-return` exited 1 with
`WarnStuckClaimState` at symbolic `isStrV(V)`. Thus the positive proof
materially depends on those extensions
(`evidence/16-make-no-bridges.log` through
`evidence/19-kprove-loop-no-bridges.log`).

## 4. Adequacy and real-program pinning

### Plain-language claims

`entry-reaches-loop` has no side condition. It starts from the initial MPY
configuration, loads the submitted function binding, calls it with
`dictV(KS, VS)`, initializes the four locals, invokes `dict.keys()`, allocates
`list(KS)` at heap location 0, pushes the exact call frame, and stops at the
generalized loop head. It does not itself reach a returned result.

`loop-and-return` also has no side condition. From an arbitrary remaining key
sequence `KS`, prior flags `SEEN`, `LOWER`, `UPPER`, arbitrary prior local
`dict`/`key`, arbitrary heap and heap location, and an exact active call frame,
it claims the loop and return produce:

```text
keySeenAfter(KS, SEEN)
and ((LOWER and allLowerKeys(KS))
     or (UPPER and allUpperKeys(KS)))
```

while popping the frame and restoring the caller.

The right-hand state of the entry claim mechanically matches an instance of the
loop claim with `SEEN=false`, `LOWER=true`, `UPPER=true`, `OLDKEY=noneV`,
`DICT=dictV(KS,VS)`, heap `0 |-> list(KS)`, and heap location 1. Hence the two
claims are meta-level composable by reachability transitivity. There is no
single submitted end-to-end entry-to-result claim, but that omission alone
would be an evidence/packaging limitation, not the decisive defect.

Both preconditions are satisfiable. For example, take
`KS = vCons(str(iCons(97,.IntSeq)),.ValSeq)`, one arbitrary value in `VS`, and
the concrete cells shown above. The loop claim also admits its empty witness
`KS=.ValSeq`, `SEEN=false`, `LOWER=true`, `UPPER=true`.

### Constructor-level program identity

The submitted `.mpy` is trusted-regeneration-identical. Separately,
`evidence/pinning_check.py` recursively represents the four zero-argument helper
equations and normalizes only the supplied list-syntax forms (`.Exprs`,
`.Stmts`, and explicit list parentheses). Its expanded constructor token stream
is identical to `solution.mpy`: 240 tokens on each side
(`evidence/05b-pinning-normalized.log`).

Therefore the claims execute the same function binding and body as the
submitted program, rather than a substituted algorithm.

Body sensitivity was also checked by changing the executed helper's outer
result `BoolOp` from `"and"` to `"or"`, rebuilding that modified proof
definition, and retaining the original postcondition. The build exited 0; the
loop proof exited 1 with `WarnStuckClaimState` and a residual showing the
mutated returned `true` cannot imply the required result. See
`evidence/23-make-body-mutant.log` through
`evidence/25-kprove-body-mutant.log`.

### Ground substitutions and source-domain gap

Ground reductions for empty, one lowercase ASCII key, one uppercase ASCII key,
mixed ASCII keys, a non-string key, U+00E9, and the canonical early-break
witness all close in `evidence/22-kprove-ground-results.log`.

The key mismatch is:

```text
Python: {"é": 0} -> True
formal checkDictCaseResult([str([233])], false, true, true) -> false
```

The Python result is recorded in `evidence/32-python-witnesses.log`; the formal
result is the `unicode-lower-formal` claim in
`evidence/ground-result-spec.k`. This is not a free variable or tautological
postcondition—the K result is exact—but it is the wrong property for an
unrestricted Python-string contract.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory and used-construct map

`evidence/k_inventory.py` inventories every top-level declaration and complete
multiline rule block in the 24 supplied `.k` files, `verification.k`, and
`spec.k`. The 1,129-record inventory is
`evidence/rule-inventory.md`. It contains:

- 235 syntax declarations;
- 719 rules (475 equational and 244 operational `<k>` rules);
- 119 `total` declarations, 153 function-bearing declarations, 26
  `no-evaluators`/opaque declarations, 32 `owise` rules;
- all priorities, contexts, modules, imports, configuration, and both claims.

The supplied files are the fixed semantics selected by this condition. Unused
fixed rules are part of that trusted baseline rather than candidate proof
extensions. The real program's constructs use these fixed paths:

| Program construct | Fixed declaration/execution path |
|---|---|
| `Module`, `FuncDef`, `Params` | `syntax.k:53-61`; `core.k:123-127`; `functions.k:14-16` |
| `Name`, `Bool`, `NoneVal` | `syntax.k:9-13,27`; `core.k:129-154,193-205` |
| `Assign` | `syntax.k:41`; `controls.k:8-18` |
| `dict.keys()` | `dict.k:19-33,56-60`; `core.k:117-121` |
| `For` and key iteration | `syntax.k:45`; `controls.k:62-74`; `list.k:8-10` |
| `Call`/`Attribute` | `syntax.k:28-29`; `call.k:15-32,69-75`; `core.k:183-191` |
| `isinstance(..., str)` | `builtins.k:287-297`, plus call-layer dereference |
| `islower`/`isupper` | `methods.k:10-16,111-130` |
| `If`, unary `not` | `controls.k:50-60`; `operators.k:10`; `bool.k:8` |
| `BoolOp` | `bool.k:13-25` |
| `Return`/frame pop | `functions.k:77-90` |

Every material operation, order, allocation, binding, call, branch, loop, and
return in the submitted term is represented on this path. No fixed opaque
`sortVS`, float, digest, or other `no-evaluators` symbol influences this
program's result.

The material language-model discrepancy is in `methods.k:112-130`:
`isUpperC` recognizes only code points 65–90 and `isLowerC` only 97–122.
That is internally consistent with the supplied semantics, but not adequate for
Python's unrestricted Unicode case predicates.

### Complete candidate-local inventory

There is no local `[functional]`, `[simplification]`, or opaque/
`no-evaluators` declaration. All candidate-local syntax is listed below:

- four total function symbols for the exact AST:
  `checkDictLoopBody` (line 8), `checkDictResultExpr` (21),
  `checkDictBody` (28), and `checkDictCaseModule` (39);
- total Boolean symbols `stringCaseKey`, `lowerCaseKey`,
  `upperCaseKey` (46-48), `allLowerKeys`, `allUpperKeys` (91-92),
  `keySeenAfter` (104), and `checkDictCaseResult` (111-112).

All 24 candidate-local rules are accounted for:

| Rules | Class and decision |
|---|---|
| Lines 9-19, 22-26, 29-37, 40-42 (4 rules) | Definitional AST summaries. Exact recursive expansion of the regenerated `.mpy`; terminating and sound. |
| Lines 49-56 (6 rules) | Equations for string/type/case observations. Constructor guards are disjoint via `owise`; the string equations exactly copy fixed `isStrV` and fixed ASCII `hasLower`/`hasUpper`. Terminating and internally sound, but the case meaning has the Unicode adequacy gap above. |
| Lines 62-66 (1 rule) | `isinstance` true bridge. For direct `str(CS)` values, it agrees with fixed dispatch and preserves every cell/continuation. |
| Lines 67-71 (1 rule) | `isinstance` false bridge. **Unsound over its complete match domain** because priority 30 preempts fixed priority-40 heap dereference; concrete false-conclusion witness below. |
| Lines 73-80 (2 rules) | `islower` true/false bridges. Guards require a direct syntactic string and equal fixed `applyMethod(str(CS),"islower",.Vals)`. They preserve continuation and all state. No false witness was found on their guard. |
| Lines 82-89 (2 rules) | Corresponding `isupper` bridges; same assessment. |
| Lines 93-102 (4 rules) | Empty/cons equations for `allLowerKeys` and `allUpperKeys`. Each cons equation descends structurally and exactly conjoins string and case membership. Sound. |
| Lines 105-107 (3 rules) | `keySeenAfter`: prior `true` stays true; empty with prior false is false; nonempty is true. The only overlap is nonempty/prior-true, and both rules return true. Sound and total. |
| Lines 113-116 (1 rule) | Exact generalized result equation. It preserves prior flags and conjoins classifications of the remaining keys. Sound relative to the candidate's ASCII case functions. |

All six operational bridges read and rewrite only the active `<k>` redex and
preserve the arbitrary continuation and every other cell. The four string
method rules and the direct-string `isinstance` true rule match the fixed value
equations. However, there is no candidate-supplied bridge-free universal
connection theorem. An auditor-authored attempt over the complete symbolic
guards fails at unresolved `isStrV(V)` rather than proving equivalence
(`evidence/20-kprove-bridge-connections.log`). This failure alone would be an
evidence gap, not an unsoundness finding. The following ground divergence is
the decisive soundness failure.

### Concrete false-conclusion witness for the priority-30 rule

Consider:

```text
<k> #applyK(toCall(builtinV("isinstance")),
             (ref(0), typeV("str"), .Vals)) </k>
<heap> 0 |-> str(iCons(97,.IntSeq)) </heap>
```

Under fixed semantics, `call.k:38-41` dereferences the first builtin argument at
priority 40. Dispatch then reaches `isStrV(str(...)) => true`.
`evidence/ref-dereference-fixed-spec.k` proves this result with `#Top`
(`evidence/26-ref-fixed.log`).

With the candidate extension, `stringCaseKey(ref(0)) => false`, so the
priority-30 rule at `verification.k:67-71` fires first and concludes `false`.
`evidence/ref-dereference-extended-spec.k` proves that opposite result with
`#Top` (`evidence/27-ref-extended.log`).

This divergence affects a complete ground instance of the submitted
`loop-and-return` precondition: let the one remaining key and current heap
reference be `ref(0)`, with heap object 0 equal to string `"a"`, and take the
initial flags. The fixed loop suffix returns `true`
(`evidence/ref-loop-fixed-spec.k`, `evidence/28-ref-loop-fixed.log`); the same
suffix under the candidate theory returns `false`
(`evidence/ref-loop-extended-spec.k`,
`evidence/29-ref-loop-extended.log`). Both commands exit 0 with `#Top`.

This heap shape is broader than the state produced by the submitted entry claim
from its initially empty heap, but it is explicitly admitted by the universally
quantified `HEAP:Map` and `KS:ValSeq` in the loop claim. More importantly, a
globally false operational rule cannot be justified by an asserted
unreachability argument; its guard must preserve the fixed dereference behavior
or be narrowed. The candidate therefore proves a false auxiliary theorem over
its own formal domain.

Gate A (real-program soundness): **FAIL**.

## 6. Fresh non-vacuity test

I did not rely on any candidate vacuity artifact. The fresh
`evidence/spec-vacuity.k` negates the exact loop result:

```text
notBool checkDictCaseResult(KS, SEEN, LOWER, UPPER)
```

The mutation is demonstrably false at the satisfiable empty-loop state
`KS=.ValSeq`, `SEEN=false`, `LOWER=true`, `UPPER=true`, with any well-sorted
`DICT`, `OLDKEY`, heap, and heap location satisfying the displayed claim
cells. Real execution returns `false`, while the mutation requires `true`.

Parsing/building the mutated specification:

```text
kprove spec-vacuity.k \
  --definition .audit-build/verification-kompiled \
  --spec-module SPEC-VACUITY --dry-run
```

Exit: 0 (`evidence/30-vacuity-dry-run.log`).

Actual mutation proof:

```text
kprove spec-vacuity.k \
  --definition .audit-build/verification-kompiled \
  --spec-module SPEC-VACUITY
```

Exit: 1 with `WarnStuckClaimState`. The residual contains final
`<k> false ~> .K </k>`, `KS = .ValSeq`, and `SEEN = false`, exactly the unmet
result obligation (`evidence/31-vacuity-proof.log`).

The submitted claim is therefore discriminating and result-constraining.
Non-vacuity passes, but it does not make the proof theory sound.

## 7. Proven versus assumed accounting

### What the successful `#Top` establishes

Under the supplied semantics **plus all rules in candidate `verification.k`**,
K establishes:

1. the exact regenerated function body reaches the displayed loop-head state;
2. the generalized loop-and-return state reaches the exact Boolean
   `checkDictCaseResult`;
3. the two states are mechanically composable for the entry claim's initialized
   flags and cells.

It does not establish that the candidate operational rules are conservative
over the supplied semantics. The fixed-versus-extended witness proves that one
is not. It also does not establish that the ASCII case model equals Python's
Unicode case predicates.

### Trust and assumption ledger

| Boundary | Influence | Assessment |
|---|---|---|
| K 7.1.293 parser/compiler/Haskell/LLVM backends | Build, execution, and reachability checking | Ordinary toolchain trust; versions and fresh builds recorded. |
| Supplied 24-file MPY semantics | All program execution | Required fixed trust boundary and integrity-verified. Internally selected semantics is authoritative, but its ASCII string model is inadequate for the unrestricted Python contract. |
| Trusted `py2mpy.py` | Source-to-constructor bridge | Byte-identical translator and regenerated `.mpy`; acceptable. |
| Four AST helper equations | Program identity | Mechanically expanded to the exact regenerated constructor term; acceptable. |
| Case and fold equations | Formal result meaning | Mathematically truthful for the supplied ASCII predicates; not a valid universal bridge to Python Unicode behavior. |
| Six priority-30 observation splitters | Symbolic calls and final result | Proof-critical. Five are sound on their direct-string guards; the `isinstance` false rule changes fixed behavior and is illegitimate. |
| Fixed opaque symbols (`sortVS`, float/digest symbols, etc.) | None on this program path | Inventoried but irrelevant to these claims. |
| Differential evidence | Implementation/contract and canonical comparison | Finite evidence only; not used as a replacement for K proof. It exposes both the canonical early-break discrepancy and the Unicode domain witness. |
| Meta-level composition of two claims | Entry-to-result theorem | Cell matching is mechanical; absence of a submitted combined claim is secondary to the soundness and adequacy failures. |

Gate B (intent adequacy): **FAIL** because the unrestricted Python-string
contract includes Unicode case behavior and the theorem does not.

Gate C (auditability): the evidence is reproducible and bounded command logs
record exact statuses, but the trust ledger contains a proven-bad extension.
Passing evidence hygiene cannot rescue Gates A or B.

### Decision

The reconstructed `#Top` is genuine only for an extended theory containing a
false operational rule. Additionally, the theorem materially omits Unicode
inputs allowed by the source contract. Under the benchmark decision boundary,
either defect prevents `LEGIT`, and the source-domain narrowing specifically
maps to `FAIL / NOT_LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
