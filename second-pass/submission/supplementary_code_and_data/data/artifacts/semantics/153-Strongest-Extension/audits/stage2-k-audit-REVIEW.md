# Independent adversarial review — 153-Strongest-Extension

The candidate is **not a legitimate partial-correctness proof of the full
generated program contract**. Fresh reconstruction does reproduce all four
reported `#Top` results, the submitted Python implementation is correct, the
claim pins that implementation's constructor body, and a false-postcondition
mutation is rejected. Those positive facts do not overcome three material
defects:

1. the only entry claim accepts exactly three extensions, while the source
   contract and canonical implementation accept every nonempty list length;
2. the claimed ASCII strength summary disagrees with Python on valid Unicode
   strings; and
3. a contributing priority rule bypasses name lookup and can prove a concretely
   false helper result.

The first defect alone is a material narrowing and therefore maps to
`FAIL / NOT_LEGIT` under the benchmark-specific decision boundary.

## 1. Input and provenance integrity

### Layout and required records

`/audit-input.json` declares:

- problem `153-Strongest-Extension`;
- condition `semantics`;
- `semantics_mode = SUPPLIED_SEMANTICS`;
- `record_layout = legacy-selected-stage1`; and
- complete input provenance.

The mounted `/reference/reference-semantics` tree is present as required for
this mode. The campaign object in `/audit-input.json` equals
`/audit-campaign-lock.json` exactly, and the lock's SHA-256 is the recorded
`ad5dfc...d745`.

I read and independently checked the required records:

- `/run.json`, `/task.json`, `/generation-result.json`;
- `/generation-evidence/invocation.json`,
  `/generation-evidence/metrics.json`,
  `/generation-evidence/usage.json`,
  `/generation-evidence/codex-last.txt`,
  `/generation-evidence/codex-output.log`,
  `/generation-evidence/prompt.txt`; and
- the one structured trace file below
  `/generation-evidence/codex-trace/`.

Runtime metrics are not present, but this legacy layout explicitly does not
require reconstructing them. `usage.json` is present and was checked. All
required paths have the expected regular-file/directory type; none of
`/candidate`, `/reference`, or `/generation-evidence` contains a symlink.

Every recorded individual file hash checked in
[integrity.log](evidence/integrity.log) matches. Independent pipeline tree
digests also match the retained candidate workspace hash
`d65918...c6cd`, the supplied-semantics manifest hash
`4e0639...789f`, and the trace usage-source hash `1ad79b...f570`.
The candidate prompt and translator are byte-identical to their trusted
mounts.

### Supplied-semantics boundary

A recursive entry/type/content comparison found the same 25 entries in
`/candidate/reference-semantics` and
`/reference/reference-semantics`, with no missing, additional, changed,
mistyped, or linked entry. This is recorded in
[integrity.log](evidence/integrity.log). The trusted equality does not extend
to the proof-specific rules in `/candidate/verification.k`.

### Generation records

The complete 1,206,177-byte JSONL trace has 642 valid JSON records and zero
malformed lines. The complete 2,838,871-byte output log has 70,067 lines.
Counts, event types, tool calls, timestamps, and bounded head/tail excerpts are
in [generation-inspection.log](evidence/generation-inspection.log). The
generation's statements about `#Top` are treated only as claims; none is used
as reconstruction evidence.

**Stage result:** integrity passes. There is no audit infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

From `/reference/prompt.py` and `/reference/canonical.py`, the function takes
a class-name string and a nonempty list of extension-name strings. An
extension's strength is:

```text
number of uppercase letters - number of lowercase letters
```

The result is `class_name + "." + strongest_extension`; a tie keeps the first
list element. The canonical implementation's `extensions[0]` makes the empty
list exceptional rather than a normal result case. Nothing restricts a
nonempty list to length three or restricts Python strings to ASCII.

### Submitted implementation and trusted regeneration

`/candidate/solution.py` computes the same stable first maximum using the
helper `_extension_strength`. Omitting the canonical implementation's explicit
`isalpha()` conjunction is behaviorally neutral because a Python character
cannot satisfy `isupper()` or `islower()` without being alphabetic.

In clean scratch, the exact command

```bash
python3 /tmp/audit-work/trusted/py2mpy.py solution.py > solution.regenerated.mpy
cmp solution.regenerated.mpy solution.mpy
```

exited zero: the trusted translator regenerates `/candidate/solution.mpy`
byte-for-byte. See
[program-fidelity.log](evidence/program-fidelity.log).

### Independent differential testing

[differential.py](evidence/differential.py) independently loads the trusted
canonical entry point and the scratch-copied candidate, and uses a separately
implemented stable-first-maximum oracle. It covers:

- both documented examples;
- empty list, singleton list, empty extension names, punctuation, and ties;
- greater/equal/lower branch boundaries;
- Unicode characters;
- deterministic lists of every length from 1 through 8; and
- 1,320 generated cases with seed 153.

All three implementations agreed on 1,334 cases, including the common
`IndexError` outcome for the empty-list boundary. There were zero mismatches;
the exact scope and counts are in
[program-fidelity.log](evidence/program-fidelity.log).

**Stage result:** source fidelity passes. This finite test is evidence about
the Python implementation, not a K proof and not evidence that the K theorem
covers all tested list lengths or Unicode.

## 3. Clean proof reconstruction

I copied source artifacts only to `/tmp/audit-work`, used the trusted
supplied-semantics copy, and did not copy or reuse any candidate compiled
definition or cache. The observed toolchain is K 7.1.293.

### Concrete definition

I freshly compiled `MPY-KRUN` with the LLVM backend and ran a reviewer-authored
translated program containing the exact two submitted function definitions and
assertions for list lengths 1, 2, 3, and 4, ties, an empty extension name, and
nonletters. The definition built with exit 0; `krun` exited 0 with `.K`,
`NoExc`, and exit code 0. Sources, exact commands, and output are in
[concrete-audit.py](evidence/concrete-audit.py) and
[concrete-reconstruction.log](evidence/concrete-reconstruction.log).

### Proof definitions and target claims

Four Haskell definitions were built from `verification.k`, one for each staged
module. Each selected positive claim was then run independently:

| Claim | Definition main module | Build | `kprove` |
|---|---|---:|---:|
| `character-loop-correct` | `STRONGEST-EXTENSION-VERIFICATION` | 0 | 0, `#Top` |
| `extension-strength-correct` | `STRONGEST-EXTENSION-WITH-CHAR-LOOP-LEMMA` | 0 | 0, `#Top` |
| `selection-loop-correct` | `STRONGEST-EXTENSION-WITH-STRENGTH-LEMMA` | 0 | 0, `#Top` |
| `strongest-extension-correct` | `STRONGEST-EXTENSION-WITH-LOOP-LEMMAS` | 0 | 0, `#Top` |

The exact commands and bounded outputs are in
[reconstruct.sh](evidence/reconstruct.sh) and
[reconstruction.log](evidence/reconstruction.log). The compiler's warnings
are unused-variable warnings in fixed `str.k` and framed-cell warnings in the
spec; no target failed or timed out.

**Stage result:** clean dynamic reconstruction passes. This establishes closure
under the supplied definition plus candidate proof extensions; it does not by
itself validate those extensions or theorem scope.

## 4. Adequacy and real-program pinning

### Claims in plain language

1. **Character-loop claim (`spec.k:8`):** from a nonempty remaining character
   sequence, the helper loop updates `score` by the recursive ASCII
   contribution, stores the final one-character string, and resumes the
   arbitrary continuation.
2. **Helper-call claim (`spec.k:48`):** when the local scope does not shadow
   `_extension_strength`, calling the submitted helper on any `IntSeq` string
   returns `extensionStrength(CS)` and resumes the continuation.
3. **Selection-loop claim (`spec.k:73`):** from an accumulator state whose
   score matches its last extension, iterating **exactly three** string values
   produces the stable first-maximum fold state and resumes the continuation.
4. **Entry claim (`spec.k:137`):** from a fixed fresh configuration, calling
   `Strongest_Extension` on a class value and **exactly three** extension
   values returns class, dot, and the first extension with maximal ASCII
   strength.

Each precondition is satisfiable. Concrete witnesses for all four, including
the entry witness `("my_class", ["AA", "Be", "CC"])`, are recorded in
[pinning.log](evidence/pinning.log). For that entry witness, the claimed
summary, canonical implementation, and candidate implementation all equal
`"my_class.AA"`.

### Real-program pinning

[pinning_check.py](evidence/pinning_check.py) mechanically extracts both
`FuncDef` bodies from the trusted-regenerated `solution.mpy`, expands the
proof's statement aliases, normalizes only explicit empty-list constructor
identities, and compares constructor terms. Both parameter lists and both
bodies match. It also checks that `solutionScope` binds the two exact bodies
and that the entry claim calls that scope's `Strongest_Extension`.

This is a legitimate semantically inert normalization: the claim need not load
the whole module because the same two function bindings and bodies are
mechanically present in its module scope.

Body sensitivity was checked by changing the bound submitted return body from
`class_name + "." + strongest` to `class_name + "!" + strongest` while leaving
the theorem unchanged. The mutated definition built, and the entry proof
failed with `WarnStuckClaimState` on code 33 versus code 46. See
[verification-body-mutated.k](evidence/verification-body-mutated.k) and
[body-sensitivity.log](evidence/body-sensitivity.log).

### Material adequacy failures

**Exactly-three restriction.** The source contract permits every nonempty
extension list, but the entry term at `spec.k:142-145` contains exactly three
`vCons` constructors ending in `.ValSeq`. There is no symbolic tail and no
entry claim for any other length. For the valid four-element input

```python
Strongest_Extension("C", ["a", "A", "zz", "ZZZ"])
```

both Python implementations return `"C.ZZZ"`, while no entry precondition
exists. The fresh LLVM test also executes a length-four list successfully.
See [domain-gap.log](evidence/domain-gap.log). This is not a minor
maintenance limitation; it excludes most of the unrestricted nonempty source
domain.

**Unicode disagreement.** The supplied MPY semantics implements
`isUpperC/isLowerC` only for ASCII code ranges, and the candidate summary uses
those functions. Yet the formal entry variables are arbitrary `IntSeq`s, with
no ASCII precondition, while real Python strings support Unicode case
predicates. For the satisfying exactly-three input

```python
Strongest_Extension("C", ["A", "ΩΩ", "BB"])
```

both Python implementations return `"C.ΩΩ"`: Python scores the three names
1, 2, and 2. The K summary scores them 1, 0, and 2 and therefore claims
`"C.BB"`. The independently executable witness is in
[domain_gap.py](evidence/domain_gap.py) and
[domain-gap.log](evidence/domain-gap.log).

**Stage result:** real-body pinning passes, but intent/domain adequacy fails
materially. Under the benchmark rule, the exactly-three restriction is
`FAIL / NOT_LEGIT`, not a nonfatal concern.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory and construct coverage

[rule-inventory.tsv](evidence/rule-inventory.tsv) inventories every local
module/import, configuration, context, syntax declaration, function/total
attribute, ordinary rule, priority/owise/concrete/opaque attribute, and claim
in:

- all 24 supplied semantics files;
- `/candidate/verification.k`; and
- `/candidate/spec.k`.

It contains 1,137 records: 718 rules, 233 syntax declarations, five contexts,
one configuration, and four claims. The complete per-file/per-rule assessment
and submitted-constructor mapping is in
[static-assessment.md](evidence/static-assessment.md).

The relevant fixed rules implement module/function binding, lexical lookup,
left-to-right call and binary evaluation, function frames, assignment,
integer augmented assignment/comparison, list and string iteration, `if`,
return, list index 0, and string concatenation. Every constructor in
`solution.mpy` maps to a declaration and a used rule. The heap, allocation,
stack, return, exception and exit cells are either executed by fixed call
semantics or explicitly framed. Unused fixed opaque float/sort/md5 symbols are
term-disjoint and do not influence any result or branch.

The candidate adds:

- truthful recursive ASCII strength, stable-best, best-strength, and
  last-element functions;
- four exact body aliases and the exact `solutionScope`; and
- four priority-40 operational bridges.

The stable-best guards `>` and `<=` are disjoint and exhaustive for integers,
and recursion descends. Three functions are marked total despite lacking a
non-`str` `ValSeq` equation, but every claimed use explicitly contains only
`str` heads, so that broader declaration does not select a fabricated value on
the claimed path.

### Concrete false-conclusion witness for the named-call bridge

The bridge at `verification.k:142-154` rewrites

```text
Call(Name("_extension_strength"), Name(X))
```

directly to `extensionStrength(CS)` whenever local `X` is a string. It does not
require name lookup to select the submitted helper. It therefore preempts
fixed callee lookup, argument evaluation, binding, call and return on a
strictly broader domain than the helper theorem.

[spec-binding-witness.k](evidence/spec-binding-witness.k) supplies a concrete
state with valid extension string `"A"` but a local binding of
`_extension_strength` to an exact function returning 999:

- with the bridge-enabled definition, the false destination `1` proves with
  exit 0 and `#Top`;
- with the fixed base definition, the same claim exits 1 with
  `WarnStuckClaimState` and residual result 999.

Exact commands and outputs are in
[binding-bridge-witness.log](evidence/binding-bridge-witness.log). This is a
concrete false conclusion over the rule's stated match domain. The shadowed
state is not reachable from the pinned entry precondition, so it is not used
to claim that the three-name entry result itself is false; it nevertheless
violates the required global rule-validity and complete-binding contract, and
the shortcut syntactically contributes at every helper call in the selection
loop.

The character-loop, exact-closure application, and selection-loop bridges
have truthful summaries on the pinned entry path. Their raw match domains
frame more context/state than their preceding claims establish, so they lack
bridge-free universal connection theorems over every accepted configuration.
I found no separate false conclusion witness for those three and therefore
record them as context-containment evidence gaps rather than labeling them
unsound.

**Stage result:** the mathematical equations and used fixed semantics are
sound on the limited ASCII/three-name path, but Gate A fails because the named
helper-call bridge is demonstrably false over its complete match domain. The
source-domain Unicode counterexample from Stage 4 independently demonstrates
a false real-program interpretation on a satisfying entry input.

## 6. Fresh non-vacuity test

The candidate did not supply a `spec-vacuity.k`; none was trusted or reused. I
created [spec-vacuity.k](evidence/spec-vacuity.k), changing only the entry
result's separator obligation from dot (ASCII 46) to exclamation mark
(ASCII 33). The original precondition remains satisfiable, for example
`("my_class", ["AA", "Be", "CC"])`, whose true result is `"my_class.AA"` and
whose mutated required result is `"my_class!AA"`.

Using the fresh final definition:

- `kprove ... --dry-run` exited 0, showing that the mutation parses and builds;
- the actual mutated proof exited 1 with `WarnStuckClaimState`; and
- the residual explicitly contains the unmet equality between code 33 and
  code 46.

The exact artifact, commands, exits and bounded residual are in
[non-vacuity.log](evidence/non-vacuity.log).

**Stage result:** non-vacuity passes. The original entry claim constrains its
result; its failure is scope/soundness, not a tautological postcondition.

## 7. Proven versus assumed accounting

### What the successful reachability run establishes

Taken literally, the successful entry proof establishes the following
conditional theorem:

> Under the supplied MPY definition plus all candidate priority bridges, from
> the fixed fresh configuration, calling the constructor-level submitted
> function with one `IntSeq` class and exactly three `IntSeq` string
> extensions reaches class, ASCII dot, and the stable first maximum computed
> by the candidate's ASCII strength equations, if execution terminates.

The helper and loop claims establish their corresponding ASCII recursive
summaries under their stated cells. This is partial correctness only; no
termination theorem is claimed.

It does **not** establish correctness for arbitrary nonempty list lengths, and
it does not establish the Python/Unicode meaning of uppercase and lowercase.
Because a contributing bridge is false on its full match domain, even the
formal closure is conditional on an invalid proof extension rather than a
sound extension theory.

### Trust ledger

| Boundary | Influence | Accounting |
|---|---|---|
| K 7.1.293 backend and hooked integer/Boolean/map/list primitives | All proof execution and mathematics | Ordinary low-level toolchain trust; version recorded and all runs reconstructed. |
| Trusted `py2mpy.py` | Source-to-constructor bridge | Byte identity of candidate/trusted translator plus byte-identical regeneration; acceptable mechanical bridge. |
| Supplied `MPY` semantics | Evaluation, scopes, calls, control and ASCII string behavior | Fixed benchmark trust boundary. Adequate for the used ASCII subset, but materially narrower than Python's Unicode source contract. |
| Candidate recursive summary functions | Final best extension and loop state | Equationally defined, terminating on used constructor inputs, no opaque result oracle. |
| Character-loop / exact-closure / selection-loop bridges | Skip material program execution | Empirically and locally aligned on the entry path, but their complete raw contexts exceed their connection claims; documented limitation. |
| Named helper-call bridge | Helper result, every selection iteration, final choice | Illegitimate: fixed-versus-extended witness proves it can override the selected binding and fabricate result 1 instead of 999. |
| Canonical/candidate differential tests | Python implementation fidelity | 1,334 finite cases, zero mismatches; supports only source fidelity, never substitutes for the K proof. |
| Constructor pinning and body mutation | Identity/sensitivity of executed body | Mechanical comparison plus a failed mutated-body theorem; acceptable evidence that the limited entry claim binds the submitted body. |
| Unicode and length witnesses | Intent adequacy | Direct executable counterexamples/exclusions; decisive evidence against full-contract coverage. |

No supplied opaque md5, float, sort, external I/O, allocation oracle, or other
uninterpreted primitive affects this theorem.

### Gate and decision accounting

- **Dynamic reconstruction:** pass — four independent `#Top` results.
- **Result constraint/non-vacuity:** pass.
- **Real-body pinning:** pass.
- **Proof-extension soundness (Gate A):** fail — false named-call bridge with
  a fixed-versus-extended witness.
- **Intent/domain adequacy (Gate B):** fail — exactly three rather than every
  nonempty list, plus a concrete Unicode result disagreement.
- **Evidence auditability (Gate C):** pass for the claims made in this review;
  all scripts, mutations and bounded logs are preserved below `evidence/`.

The generation report and prior `#Top` outputs are not relied upon. The
candidate's Python program is correct, and the limited formal target is
non-vacuous and body-sensitive, but the submitted theorem is not the required
unrestricted HumanEval theorem and its proof theory contains a demonstrated
unsound bridge.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
