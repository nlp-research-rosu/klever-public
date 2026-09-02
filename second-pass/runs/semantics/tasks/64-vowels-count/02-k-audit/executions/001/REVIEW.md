# Independent adversarial audit: 64-vowels-count

The candidate is **not a legitimate proof**. Both submitted positive claims can
be reconstructed and the final claim is result-constraining, but the main proof
uses a globally unsound operational bridge. The auxiliary loop theorem is proved
only for `<env> 1`; the reusable rule omits the `<env>` cell and rewrites the
variables in frame 1 regardless of the active environment. A ground `"a"`
counterexample proves that the extended theory admits a false state transition
which the bridge-free supplied semantics rejects.

This is a candidate failure, not an infrastructure failure. K 7.1.337 and
Python 3.10.12 were available and all required rebuilds and diagnostic proofs
ran to completion. Tool versions and source hashes are in
[environment-and-hashes.log](/audit-output/evidence/environment-and-hashes.log).

## 1. Input and provenance integrity

The rendered mode is `SUPPLIED_SEMANTICS`, and the trusted mount is consistent
with that mode: `/reference/reference-semantics` exists.

I recursively compared `/candidate/reference-semantics` with the trusted tree.
Both contain the same 24 regular source files and directory layout, there are
no symlinks, and `diff -r --no-dereference` exited 0. Thus there is no missing,
additional, changed, mistyped, or symlinked entry in the candidate semantics
tree. The check and both typed manifests are recorded in
[stage1-integrity.log](/audit-output/evidence/stage1-integrity.log).

`/candidate/prompt.py` is byte-identical to `/reference/prompt.py`, and
`/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`. Their
respective SHA-256 hashes are:

- prompt: `bc81b28f391ede1728b9b45d174a5a8953119ebc8f98908735202a05f839c5d8`
- translator: `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`

The requested untrusted provenance files `run-input.json`, `metrics.json`,
`codex-last.txt`, and `codex-output.log` are all absent. No structured
generation trace is present. These omissions limit provenance auditability but
do not prevent independent source reconstruction. The candidate's `prove.log`,
`prove.sh`, and smoke artifacts were read only as untrusted claims; no
candidate-built definition or cache was used.

All candidate proof sources needed for execution are present as regular files:
`solution.py`, `solution.mpy`, `spec.k`, `verification.k`, and the supplied
semantics tree. The candidate also contains an untrusted `__pycache__`, which
was ignored.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

From `/reference/prompt.py` and `/reference/canonical.py`: for a string
representing a word, count occurrences of `a`, `e`, `i`, `o`, and `u`,
case-insensitively as demonstrated by `"ACEDY"`, and add one when the final
character is ASCII `y` or `Y`. The trusted canonical implementation indexes
`s[-1]`, so it raises `IndexError` on the empty string.

The candidate lowercases the whole string, counts ASCII `aeiou` in a loop, and
adds the final iteration's Boolean `char in "y"`. This is equivalent to the
canonical algorithm for tested nonempty ASCII strings. It differs for the empty
string and for at least one Unicode letter because CPython `lower()` is a
Unicode transformation, while the canonical membership tests only the ten
literal ASCII vowels.

### Translation fidelity

I regenerated the program using the trusted translator:

```text
python3 /reference/py2mpy.py /tmp/audit-work/fresh/solution.py \
  > /tmp/audit-work/fresh/solution.regenerated.mpy
```

The command exited 0, and `cmp -s` against `/candidate/solution.mpy` exited 0.
Both files have SHA-256
`613db029a69382d157e1c7b5ddcf7b0c6a560c49a5cdb7ebd830239503136b51`.
See
[stage2-program-fidelity.log](/audit-output/evidence/stage2-program-fidelity.log).

### Independent differential test

[differential_test.py](/audit-output/evidence/differential_test.py) imports the
trusted canonical entry point and the scratch copy of the generated entry
point independently. It covers:

- both documented examples;
- the empty boundary;
- 24 branch and position boundaries;
- every string of lengths 1 through 5 over `aeybAEYB` (37,448 cases);
- 9,912 unique seeded random ASCII strings of lengths 1 through 64;
- targeted Unicode inputs; and
- all 131,241 single-code-point strings for which `str.isalpha()` is true.

There were no mismatches on the documented examples, branch boundaries,
exhaustive nonempty ASCII set, or random ASCII set. The script deliberately
exited 1 after finding these observable divergences:

- `""`: canonical raises `IndexError`; candidate returns `0`.
- `"İ"` (U+0130): canonical returns `0`; candidate returns `1` because
  `"İ".lower()` is `"i\u0307"`.
- The same Unicode cause gives candidate/canonical results `2/1` on `"İy"` and
  `1/0` on `"xİ"`.

The exact inputs, scopes, exit status, and bounded output are in
[stage2-program-fidelity.log](/audit-output/evidence/stage2-program-fidelity.log).
These are adequacy limitations. They are not the reason for the final `FAIL`;
the proof-rule counterexample in Stage 5 is independently decisive.

## 3. Clean proof reconstruction

I copied only source artifacts to `/tmp/audit-work/fresh`, used the trusted
semantics tree, and created all compiled definitions afresh. No compiled
candidate directory existed in or was copied to scratch.

The fresh commands and results were:

| Purpose | Command summary | Exit/result |
|---|---|---|
| Concrete definition | `kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-kompiled` | 0 |
| Bridge-free proof definition | `kompile verification.k --backend haskell --main-module VOWELS-BASE --syntax-module MPY-SYNTAX --output-definition proof-base-kompiled` | 0 |
| Positive loop claim | `kprove spec.k --definition proof-base-kompiled --spec-module LOOP-SPEC --output pretty` | 0, `#Top` |
| Extended proof definition | `kompile verification.k --backend haskell --main-module VOWELS-VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-kompiled` | 0 |
| Positive main claim | `kprove spec.k --definition verification-kompiled --spec-module MAIN-SPEC --output pretty` | 0, `#Top` |

The per-command records are
[stage3-kompile-runtime.log](/audit-output/evidence/stage3-kompile-runtime.log),
[stage3-kompile-proof-base.log](/audit-output/evidence/stage3-kompile-proof-base.log),
[stage3-kprove-loop.log](/audit-output/evidence/stage3-kprove-loop.log),
[stage3-kompile-verification.log](/audit-output/evidence/stage3-kompile-verification.log),
and [stage3-kprove-main.log](/audit-output/evidence/stage3-kprove-main.log).

The compiler reported pre-existing non-exhaustive-match warnings for some
supplied, unused total functions (including float, join, and subscript
operations). None is reachable from this program. Both required success signals
were independently observed; they establish closure under their respective K
theories, not the soundness of the added bridge.

## 4. Adequacy and real-program pinning

### Claims in plain language

`LOOP-SPEC.loop-summary` starts with the actual `#loop` over a string `S`, the
actual target `Name("char")`, and the actual loop body. Its precondition fixes:

- active environment 1;
- scope location 2;
- frame 1 with `s`, integer `count`, one-character prior `char`, and Boolean
  prior `last_y`;
- no return, no exception, exit code 0; and
- a remainder map `SC` which does not already contain key 1.

It allows arbitrary heap, heap location, stack, and continuation values but
preserves them. Its postcondition resumes the same continuation after adding
the ordinary vowels of `S` to `count`, setting `char` to the final character
(or preserving the previous one for empty `S`), and setting `last_y` to whether
the final character is `y` (or preserving the prior Boolean for empty `S`).

This precondition is satisfiable. One witness is `S = iCons(97,.IntSeq)`
(`"a"`), `COUNT = 0`, `PREVIOUS = .IntSeq`, `PREVIOUSY = false`,
`ORIGINALS = str(iCons(97,.IntSeq))`, `SC` containing only frame 0,
`<env> 1`, `<scopeLoc> 2`, empty heap/stack, `noRet`, `NoExc`, and exit code 0.
The fresh bridge-free loop proof establishes this claim universally.

`MAIN-SPEC.vowels-count-correct` starts from the exact initial module
configuration and, for any `S:IntSeq`, loads the function and calls it with
`str(S)`. It requires no side condition on `S`. Its postcondition fixes the
returned value to:

```text
ordinaryVowels(mapLower(S))
+ boolToInt(finalIsY(mapLower(S), false))
```

It also pins the final module binding and all non-result cells. This is a
genuine result constraint, not a free variable, tautology, or implication. A
satisfying entry witness is the exact stated initial configuration with
`S = iCons(97,.IntSeq)`.

### Program identity

The main claim uses the macro `vowelsModule` rather than opening
`solution.mpy` at proof time. I therefore parsed both the submitted
`solution.mpy` and the macro expression with the fresh base definition,
expanded macros, emitted KORE, and compared the outputs. They are byte-identical
and both have SHA-256
`b3edde789dcb260b94f6accac451768f066eaaa02321d76306c178e8f69385da`.
The commands are in
[stage4-adequacy-ground.log](/audit-output/evidence/stage4-adequacy-ground.log).
This mechanically pins `vowelsModule`, `vowelsBody`, and `vowelLoopBody` to the
submitted translated program.

### Concrete satisfying instances

The fresh LLVM definition executed the exact function body for `""`, `"a"`,
`"y"`, `"by"`, `"abcde"`, `"ACEDY"`, and `"yellowy"`. Its results were,
respectively, `0, 1, 1, 1, 2, 3, 3`; the generated Python implementation
returned the same values. The canonical returned the same values except that
it raised on `""`. Sources and output are in
[ground_checks.py](/audit-output/evidence/ground_checks.py),
[ground_checks.mpy](/audit-output/evidence/ground_checks.mpy), and
[stage4-adequacy-ground.log](/audit-output/evidence/stage4-adequacy-ground.log).

For the satisfying formal input `S = "a"`, the claimed expression evaluates to
1, both Python implementations return 1, and a separate ground reachability
claim executed the actual function against `VOWELS-BASE` with no loop bridge
and closed with `#Top`. See
[ground-main-base.k](/audit-output/evidence/ground-main-base.k) and
[stage4-ground-main-base.log](/audit-output/evidence/stage4-ground-main-base.log).

Thus the submitted program and result are pinned syntactically, and concrete
ASCII instances are correct. The defect is that the universal main derivation
uses an inference rule broader than its proved auxiliary theorem.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[rule-inventory.tsv](/audit-output/evidence/rule-inventory.tsv) contains one
record for every source configuration, context, syntax declaration, rule, and
claim in `reference-semantics/semantics.k`, all supplied helper K files,
`verification.k`, and `spec.k`. It has 950 source sentences:

- 1 configuration;
- 5 contexts;
- 235 syntax declarations;
- 707 rules; and
- 2 claims.

Each record includes source location, attributes, complete normalized source
sentence, path relevance, decision, and rationale. There are no local
`[functional]` or `[simplification]` declarations. All `total`, `function`,
`macro`, `concrete`, `owise`, `priority`, and symbolic/opaque annotations are
visible in the inventory. The generating script and count log are
[rule_inventory.py](/audit-output/evidence/rule_inventory.py) and
[stage5-inventory.log](/audit-output/evidence/stage5-inventory.log).

The 25 supplied semantics files are byte-identical to the trusted mount. Of the
950 sentences, 99 fixed-semantics sentences are on the program path, 11
document the ASCII string-model boundary, and 818 fixed sentences are off the
path (including 22 inventory entries concerning fixed opaque primitives).
The opaque symbols are the supplied float primitives
`intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `floorFI`, `toF`,
`ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`,
`decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`, and
`sqrtF`, plus `sortVS`, `sortKeyVS`, and `md5hexCodes`. No opaque symbol is
reachable from `solution.mpy` or influences either target result.

### Used-construct map

| Submitted construct | Declaration/evaluation rules |
|---|---|
| `Module`, statement sequence, `FuncDef` | `syntax.k`; `core.k` `#loadAll`/statement sequencing; `functions.k` function binding |
| `Call(Name("vowels_count"), str(S))` | `core.k` lookup and argument order; `call.k` callee dispatch/frame creation; `functions.k` parameter bind/return/pop |
| `Attribute(Name("s"),"lower")` | strict attribute evaluation in `syntax.k`; `call.k` bound method routing; `methods.k` `applyMethod(...,"lower",...)` |
| `Assign`, `AugAssign` | strict declarations in `syntax.k`; current-environment updates in `controls.k` |
| `For` / internal `#loop` | `controls.k` loop protocol; `tuple.k` target binding; `str.k` iterator rules |
| `If` | strict test plus `truthy` in `core.k`; branch rules in `controls.k` |
| `Compare(...,"in",...)` | comparison contexts/dispatch in `operators.k`; `str.k` `strContains`/`strPrefix` |
| integer/Boolean literals and `+` | literal rules in `core.k`; integer and integer-plus-Boolean rules in `int.k` |
| ASCII string literals and lowercasing | `str.k` `strToCodes`; `methods.k` `lowerC`/`mapLower` |

These fixed rules preserve left-to-right evaluation, current-frame lookup and
updates, loop control, call/return stack behavior, and the cells used by this
program. The ASCII lowercasing equations are sound for the selected documented
code-sequence model and every submitted literal, but they are not a complete
model of CPython Unicode lowercasing; Stage 2 supplies the concrete U+0130
witness.

### Candidate mathematical definitions and macros

The candidate adds:

- `boolToInt`: a total and exact Boolean-to-0/1 equation.
- `ordinaryVowels`: disjoint empty/cons equations, structurally descending and
  exactly testing a one-code string against ASCII `aeiou`.
- `finalIsY`: disjoint empty/cons equations, structurally descending and
  correctly modeling the overwritten loop Boolean.
- `finalLowerChar`: disjoint empty/cons equations, structurally descending and
  correctly retaining the final loop target.
- `specifiedVowels`: a definitional composition of those summaries with
  supplied `mapLower`.
- three macros reproducing the exact loop, function body, and module.

All of these declarations/equations are conservative, covered at every used
constructor, and pairwise non-conflicting. `ordinaryVowels`, `finalIsY`, and
`finalLowerChar` are connected to real loop execution by the fresh
bridge-free `LOOP-SPEC` proof; they are not unconstrained oracles.

### Rejected operational bridge

The only rule in `VOWELS-VERIFICATION` rewrites the program's real `#loop`
directly to its summary at priority 40. It is therefore an operational bridge.
Its available connection theorem is `LOOP-SPEC.loop-summary`.

The theorem fixes `<env> 1`, `<scopeLoc> 2`, `noRet`, `NoExc`, and exit code 0,
and explicitly frames heap, heap location, stack, and continuation. The bridge
matches only the `<k>` and `<scopes>` cells. Its continuation is adequately
covered because the theorem quantifies `CONTINUATION:K`, but its state match
domain is not contained in the theorem domain. Most importantly, the bridge
omits `<env> 1` even though the fixed `Assign`, `AugAssign`, lookup, and
`#bindTgt` rules read `<env>` to choose the frame they modify.

This is materially false, with the required ground witness:

1. Use intended input code sequence `"a"` (`iCons(97,.IntSeq)`).
2. Put complete vowel-loop variable maps in frames 0 and 1, but set
   `<env> 0`.
3. Ask for the candidate bridge's conclusion: frame 0 unchanged and frame 1
   summarized to count 1 / final character `"a"`.
4. Under fixed semantics, the real loop instead updates active frame 0 and
   leaves frame 1 unchanged. The bridge-free proof exits 1 with a stuck final
   state showing frame-0 count 1 and frame-1 count 0.
5. Under `VOWELS-VERIFICATION`, the same false claim exits 0 and prints
   `#Top`, because the candidate bridge updates frame 1 without checking the
   active environment.

The exact paired claims are in
[bridge-context-witness.k](/audit-output/evidence/bridge-context-witness.k).
The bridge-free rejection is
[stage5-bridge-base.log](/audit-output/evidence/stage5-bridge-base.log), and the
false bridge-enabled proof is
[stage5-bridge-extended.log](/audit-output/evidence/stage5-bridge-extended.log).

This witness is a false conclusion enabled by the rule on the ordinary input
`"a"`. It also demonstrates body/control sensitivity: fixed execution and the
bridge disagree about observable scope state. Priority 40 makes the invalid
bridge preempt real loop execution; it does not supply the missing
justification. A sound reusable rule would at minimum need to include the
theorem's active-environment constraint and must not accept cells outside the
connection theorem without an independent irrelevance theorem.

No other candidate rule was found unsound. This single rejected rule is enough
to contaminate `MAIN-SPEC`, which imports `VOWELS-VERIFICATION` and relies on
that rule to summarize the symbolic loop.

## 6. Fresh non-vacuity test

I created a new mutation, independent of any candidate vacuity artifact:
[spec-vacuity-audit.k](/audit-output/evidence/spec-vacuity-audit.k). It changes
the result-constraining main postcondition from `specifiedVowels(S)` to
`specifiedVowels(S) +Int 1` and changes nothing else.

The mutation is demonstrably false for the satisfying input `"a"`: the
bridge-free ground execution and both Python functions return 1, while the
mutation requires 2.

`kprove --dry-run` compiled the mutated specification successfully and exited
0; see
[stage6-vacuity-dry-run.log](/audit-output/evidence/stage6-vacuity-dry-run.log).
The actual proof exited 1 with `WarnStuckClaimState`. Its residual is the
expected unmet arithmetic obligation equating the original summary with that
summary plus 1, not a parser error, timeout, missing import, or unrelated crash.
See
[stage6-vacuity-proof.log](/audit-output/evidence/stage6-vacuity-proof.log).

Therefore the main claim is non-vacuous and result-constraining. Non-vacuity
does not make the operational bridge sound.

## 7. Proven versus assumed accounting

### What the successful runs establish

The bridge-free `#Top` establishes, under the supplied K semantics, that the
actual submitted loop body has the stated summary whenever the full
`LOOP-SPEC` precondition holds, including `<env> 1`.

The main `#Top` establishes only that the macro-identical submitted program
reaches `specifiedVowels(S)` in the **extended theory that contains the rejected
bridge**. Because that theory proves the false environment-mismatch witness,
this closure is not a legitimate reachability proof of the program.

The proof is for partial correctness: it does not separately prove Python
termination. Concrete testing, source comparison, and the differential test
support only their stated finite or syntactic bridges; none substitutes for the
K reachability proof.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K 7.1.337 parser, compiler, Haskell/LLVM backends, and builtin Int/Bool/String/Map/List hooks | All builds and proofs | Ordinary machine-checking trust boundary; versions recorded |
| Byte-identical supplied semantics | All operational execution | Authorized fixed semantics; used subset reviewed, with explicit ASCII model limitation |
| Candidate structural summary functions | Loop and main result | Acceptable: truthful equations plus bridge-free universal loop theorem |
| Macro-to-program identity | Both formal claims | Acceptable: regenerated translation and expanded KORE are byte-identical |
| ASCII K strings versus CPython strings | Intent bridge | Limited: U+0130 differential witness shows Unicode lowercasing mismatch |
| Candidate versus canonical behavior | Natural-language adequacy | Finite support only; zero nonempty ASCII mismatches in tested scope, but empty and Unicode divergences exist |
| Unused float/sort/MD5 opaque primitives | None | Irrelevant to this proof path |
| Priority-40 loop bridge | Universal main claim | **Illegitimate**: its match domain exceeds its connection theorem and it proves the concrete false frame-update witness |
| Missing run metadata and generation trace | Provenance only | Evidence limitation; not the cause of the proof failure |

### Decision

The reconstruction and non-vacuity gates succeed, and the loop auxiliary
theorem itself is sound over its stated precondition. Nevertheless, the
universal main proof depends on a materially unsound operational rule. The
paired ground witness meets the required false-conclusion standard and makes
this a candidate defect rather than a mere evidence gap or concern. Under the
stated decision boundary, the result is `FAIL / NOT_LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
