# Independent adversarial review: 153-Strongest-Extension

The K reachability claims reconstruct successfully and are non-vacuous relative
to the supplied MPY model. They also execute the submitted constructor term.
They do **not**, however, establish the HumanEval contract for the real generated
Python program. The rewrite omits the trusted canonical implementation's
`isalpha()` guard. That omission is invisible in the supplied ASCII case model
but changes CPython results for cased, non-alphabetic Unicode characters.

Concrete counterexample:

```text
class_name = "C"
extensions = ["A", "ⅠⅠ"]       # U+2160 ROMAN NUMERAL ONE twice

canonical.py  -> "C.A"
solution.py   -> "C.ⅠⅠ"
```

In CPython, `Ⅰ.isupper()` is true but `Ⅰ.isalpha()` is false. Canonical scores
the two extensions as `1` and `0`; the candidate scores them as `1` and `2`.
This is a nonempty list-of-strings input in the source-contract domain. It is
program-vs-canonical divergence, not merely model-vs-CPython divergence.

## 1. Input and provenance integrity

The launcher declares `record_layout = "pipeline-v3"`,
`condition = "kit-semantics"`, and
`semantics_mode = "SUPPLIED_SEMANTICS"`. The trusted
`/reference/reference-semantics` mount is present, so the rendered mode and
trusted mounts agree. There is no infrastructure breach.

I read `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
`/task.json`, `/generation-result.json`, and all required generation records:
`invocation.json`, `metrics.json`, `runtime-metrics.json`, `usage.json`,
`codex-last.txt`, `codex-output.log`, `prompt.txt`, and the JSONL tree below
`codex-trace/`. The structured trace contains one regular JSONL file with 1,039
records; every record parsed. These records were treated only as untrusted
generation history.

Independent checks in
[`stage1-integrity.log`](evidence/stage1-integrity.log) establish:

- The `audit_campaign` object exactly equals
  `/audit-campaign-lock.json`; the lock SHA-256 is
  `e71e1d695e6ffbbdc115800a2770522f00df366ef4b9637b1edf96107de40d0e`.
- `/audit-prompt.md` hashes to the campaign-recorded
  `cf17fc47388b7f2762ccfaa6dd7c4b2e5b3ba2694fe67dbb770ed52dfc3f3970`.
- Every required regular-file hash matches `/audit-input.json`, including the
  canonical, prompt, translator, pipeline manifests, result, invocation,
  metrics, usage, generation prompt/output/last, and runtime metrics.
- The mounted candidate tree has pipeline tree hash
  `80ef229b2f43b1b96fed636e558312340d4fbbc98de4106b1375a738768bfeb4`,
  matching `generation-result.json` and `invocation.json`.
- The structured trace tree hash is
  `f46187495903cba38063a49324e401a4000a0f1d00a87b8eea84d10855206acc`,
  matching `usage.json`; its file set and individual hash match the result
  record.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
  mounts.
- Candidate and trusted `reference-semantics/` contain the same 25 recursively
  inventoried entries with identical types and bytes. Their independently
  recomputed pipeline tree hash is
  `4495a50f2231cf6231a75f82531d6d4f9b2397fbede6509e4a6dc42c2dd29ad1`.
  Neither tree contains a symlink. There are no missing, additional, changed,
  or mistyped supplied-semantics entries.

The check is implemented in
[`check_integrity.py`](evidence/check_integrity.py). It rejects non-regular
required records and linked/unsupported tree entries instead of following
them.

## 2. Program fidelity and candidate-versus-canonical checks

### Trusted contract

`prompt.py` requires a string `class_name` and a list of extension-name strings.
Each extension's strength is:

```text
number of uppercase letters - number of lowercase letters
```

The function returns `class_name + "." + strongest_extension`; a tie is broken
in favor of the earliest list element. The trusted canonical implements
"letter" with `x.isalpha()` in addition to `x.isupper()`/`x.islower()`.
Canonical indexes `extensions[0]`, so its implementation does not define an
empty-list result.

### Translation fidelity

I regenerated the submitted MPY program from `solution.py` with the trusted
translator:

```text
python3 /reference/py2mpy.py /tmp/audit-work/rebuild/solution.py \
  > /tmp/audit-work/rebuild/regenerated-solution.mpy
```

Both the submitted and regenerated files hash to
`ffb7cb135b2b77d39e8c5199f3b3e551e61ac7e0f36ccbc84a72185b33f580c5`,
and `cmp` exits 0. See
[`stage2-translation.log`](evidence/stage2-translation.log).

### Independent differential

[`differential_audit.py`](evidence/differential_audit.py) loads the trusted
canonical and candidate entry points independently. It covers both prompt
examples, empty strings, an empty list, equal-score boundaries, positive and
negative strengths, nonletters, first-on-tie behavior, Greek/Cyrillic letters,
cased non-alphabetic Unicode characters, and 2,500 deterministic generated
cases. It scans CPython's Unicode space for characters satisfying:

```python
(ch.isupper() or ch.islower()) and not ch.isalpha()
```

The run reports 484 mismatches among 2,512 cases, 483 of them with nonempty
extension lists. The number is sample-dependent; the single directed Roman
numeral witness is already decisive. Exact inputs and the first 30 mismatches
are in [`stage2-differential.log`](evidence/stage2-differential.log).

The candidate's own `differential_test.py` does not compare against
`canonical.py`. Its purported oracle uses the same `isupper()`/`islower()`
score as the rewrite and repeats the missing `isalpha()` guard. Its claimed
zero mismatches therefore cannot support canonical fidelity.

The empty-list observation is also different—canonical raises `IndexError`,
while the candidate returns `class_name + "."`—but the final verdict does not
depend on treating empty lists as part of the canonical domain. The Roman
numeral witness is nonempty and fully specified.

### Supplied-model gap versus candidate defect

[`adequacy_witnesses.py`](evidence/adequacy_witnesses.py) distinguishes the two:

```text
["A", "ΩΩ"]: fixed MPY model -> C.A; canonical -> C.ΩΩ; candidate -> C.ΩΩ
["A", "ⅠⅠ"]: fixed MPY model -> C.A; canonical -> C.A; candidate -> C.ⅠⅠ
```

The Greek case is the documented supplied-model ASCII gap. The Roman case is
different: canonical and candidate disagree. The latter defeats campaign
amendment v2's requirement that the submitted Python program remain faithful
to canonical on the representation/behavior gap.

## 3. Clean proof reconstruction

All source needed for execution was copied to `/tmp/audit-work/rebuild`.
Candidate-provided compiled definitions, caches, logs, and `#Top` reports were
not copied or used. The semantics source came from the trusted reference mount.

Fresh commands and outcomes:

| Purpose | Definition/spec | Outcome |
|---|---|---|
| Concrete definition | LLVM `MPY-KRUN` from trusted `reference-semantics/semantics.k` | build exit 0 |
| Projection/yield/inner connections | Haskell `VERIFICATION-BASE`; `CONNECTION-SPEC` | build exit 0; `kprove` exit 0, `#Top` |
| Outer connection | Haskell `VERIFICATION`; `OUTER-CONNECTION-SPEC` | build exit 0; `kprove` exit 0, `#Top` |
| Target proof | Haskell `TARGET-VERIFICATION`; `SPEC` | build exit 0; `kprove` exit 0, `#Top` |

The full bounded logs, each containing its exact command and exit status, are:

- [`stage3-kompile-llvm.log`](evidence/stage3-kompile-llvm.log)
- [`stage3-kompile-connection.log`](evidence/stage3-kompile-connection.log)
- [`stage3-kprove-connection.log`](evidence/stage3-kprove-connection.log)
- [`stage3-kompile-outer.log`](evidence/stage3-kompile-outer.log)
- [`stage3-kprove-outer.log`](evidence/stage3-kprove-outer.log)
- [`stage3-kompile-target.log`](evidence/stage3-kompile-target.log)
- [`stage3-kprove-target.log`](evidence/stage3-kprove-target.log)

The connection run warns that `projection-identity` is proved without
rewriting. That is because candidate-local datatype simplifiers already orient
the relevant equality; it is not treated as independent justification for
those simplifiers in Stage 5.

A reviewer-authored concrete program was translated with the trusted
translator and run under the fresh LLVM definition. It exercises both prompt
examples, empty and one-character boundaries, strict improvement, tie
retention, and the candidate's empty-list extension. `krun` exits 0 with `.K`,
`NoExc`, and exit code 0. See
[`concrete_audit.py`](evidence/concrete_audit.py),
[`concrete_audit.mpy`](evidence/concrete_audit.mpy), and
[`stage3-concrete.log`](evidence/stage3-concrete.log).

Thus dynamic reconstruction succeeds. A reconstructed `#Top` proves closure
only under the supplied definition and candidate-local rules; it does not cure
the Stage 2 implementation/contract discrepancy.

## 4. Adequacy and real-program pinning

### Plain-language claims

The eight positive claims are:

1. `CONNECTION-SPEC.projection-identity`: for a `Val` known to be a `Str`, the
   candidate total projection denotes that same string value.
2. `CONNECTION-SPEC.yield-connection`: the fixed list-iteration yield step,
   with the exact target `extension`, exact outer body, and arbitrary trailing
   continuation, reaches the candidate's projected-value form.
3. `CONNECTION-SPEC.inner-loop`: in an exact seven-local plain function frame,
   the real character loop over any finite `Str` terminates its loop region,
   adds `extensionStrength` to `strength`, and leaves `character` at the last
   visited one-character string (or its old value for empty input).
4. `OUTER-CONNECTION-SPEC.outer-loop`: after `strength` exists and a best score
   has been established, the real extension tail loop over any finite
   all-string `ValSeq` updates `strongest`, `best_strength`, `extension`,
   `character`, and `strength` to the recursive summaries.
5. `SPEC.inner-loop`: repeats the inner-loop theorem in the target definition.
6. `SPEC.outer-loop`: repeats the outer-loop theorem in the target definition.
7. `SPEC.entry-empty`: from the complete initial configuration, load and call
   the submitted function on an arbitrary class string and the empty list; the
   returned `<k>` value is `expectedResult(CLASS, .ValSeq)`.
8. `SPEC.entry-nonempty`: from the same complete initial configuration, load
   and call the submitted function on an arbitrary class string and every
   nonempty finite list of finite strings; the returned `<k>` value is
   `expectedResult(CLASS, vCons(str(FIRST), RESTEXTS))`.

The entry postconditions constrain the actual returned `Str`; they are not free
variables, tautologies, or one-way implications. Entry-empty is satisfiable at
`CLASS = .IntSeq`. Entry-nonempty is satisfiable at `CLASS = [67]`,
`FIRST = [65]`, and `RESTEXTS = .ValSeq`. The loop claims likewise have
concrete exact-frame witnesses, as exercised by the concrete run.

### Mechanical program identity

The entry claims load a `FuncDef` using `STRONGEST-BODY`. I parsed both:

- trusted-regenerated `solution.mpy`; and
- a reviewer wrapper containing the same function header and
  `STRONGEST-BODY`,

with the fresh target definition using `kast --expand-macros --output json`.
The two constructor JSON files have the same SHA-256,
`c622cad2ae60bd32bac9af54e7527f000d8177015b3d08a4684598ea294e74bf`,
and `cmp` exits 0. This is constructor-level equality, not a visual/source-text
inference. See
[`program_macro_wrapper.mpy`](evidence/program_macro_wrapper.mpy) and
[`stage4-program-pinning.log`](evidence/stage4-program-pinning.log).

A second reviewer mutation changes the `FuncDef` term actually loaded and
called to `return "wrong"` while retaining the original `"."` postcondition.
It parses (`--dry-run` exit 0) and fails with a residual `"wrong"` value and
proof exit 1. See
[`audit-body-mutation-spec.k`](evidence/audit-body-mutation-spec.k) and
[`stage4-body-sensitivity.log`](evidence/stage4-body-sensitivity.log).

### Ground substitution

Four ground `expectedResult` reductions—empty, ASCII, Greek omega, and Roman
numeral—close with `#Top` in
[`ground-result-spec.k`](evidence/ground-result-spec.k); see
[`stage4-ground-results.log`](evidence/stage4-ground-results.log).
The ASCII satisfying input gives `C.A` in the formal result, canonical, and
candidate. The Greek and Roman comparisons are recorded in
[`stage4-adequacy-witnesses.log`](evidence/stage4-adequacy-witnesses.log).

The claim therefore pins and proves the submitted body in the supplied model.
Its adequacy failure is that the supplied model makes the omitted canonical
guard observationally irrelevant, while real CPython does not.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[`k-rule-inventory.tsv`](evidence/k-rule-inventory.tsv) is a
line-addressed, SHA-256-addressed inventory generated by
[`inventory_k.py`](evidence/inventory_k.py). It enumerates every `requires`,
module/import, configuration, context, syntax declaration, rule, and claim in
the supplied semantics plus all applicable candidate proof files. The summary
is:

| Scope | Configuration | Context | Syntax | Rule | Claim |
|---|---:|---:|---:|---:|---:|
| Trusted supplied semantics | 1 | 5 | 244 | 764 | 0 |
| Candidate proof files | 0 | 0 | 18 | 42 | 8 |

The supplied 764 rules are the selected read-only semantics level, not
candidate proof extensions. Recursive type/byte identity establishes that
every candidate copy is exactly the corresponding trusted rule. The relevant
program slice was then reviewed in depth below. Rules outside that slice
remain part of the explicit fixed-semantics trust boundary; the candidate
neither changes nor imports a proof-specific replacement for them.

### Every candidate-local declaration and rule family

The 18 local syntax declarations and all 42 rules are exhausted by these
families:

| Lines in `verification.k` | Declarations/rules | Classification and decision |
|---|---|---|
| 8–55 | `INNER-BODY`, `OUTER-BODY`, `STRONGEST-BODY`; 3 macro rules | Compile-time definitions. Accepted: expanded constructor equality with the regenerated program is machine-checked in Stage 4. |
| 59–70 | total `charStrength`, total `extensionStrength`; 5 equations | Definitional summaries. Accepted relative to the fixed ASCII `isUpperC`/`isLowerC` model. Upper/lower guards are disjoint; the third character case is their complement; sequence recursion strictly descends. |
| 74–86 | total `lastCharacter`, `isStringVal`, `allStrings`; 6 equations | Definitional state/domain summaries. Empty/cons and string/owise cases are exhaustive; recursive arguments strictly descend. |
| 90–135 | total `definedProjectStr`; opaque total `projectStrTotal` and `codesProject`; total `codesOf`; 11 rules, including 8 simplifiers | Derived datatype/projection lemmas. Accepted on target uses: `Str` has sole constructor `str(IntSeq)` and is disjoint from the other `Val` constructors. On strings both projections reduce to identity. On nonstrings the opaque values are not observed by any target claim. The equality and `#Ceil` simplifiers express exactly this constructor membership. No rule replaces program-defined computation. |
| 139–176 | partial `bestCodes`, `bestScore`; 6 equations, 4 marked simplification | Definitional left folds. Accepted on `allStrings`: true/false comparison guards are complementary, each call removes one `ValSeq` head, strict `>` preserves the earliest maximum, and right-hand sides agree on no overlap. |
| 179–201 | partial `lastExtension`, `lastStrength`, `lastCharacterAcross`; 6 equations | Definitional live-local summaries. Accepted on `allStrings`; every recursive call removes a head and every observed projection is guarded string-only. |
| 205–219 | partial `expectedResult`; 2 equations | Definitional result expression. Accepted on the two entry domains; empty and string-headed nonempty cases are disjoint, and nested `seqConcat` matches the two source additions. |
| 227–242 | priority-40 yield rule | Operational bridge. Accepted relative to the fixed model: it matches the exact target/body and the same arbitrary continuation as the fixed rule. Its guard makes `projectStrTotal(V) = V`. The bridge changes no state cell itself. The bridge-free yield connection imports `VERIFICATION-BASE`, not this bridge. |
| 246–272 | priority-30 inner-loop rule | Operational bridge. Accepted relative to the fixed model: exact loop/body, exact closed seven-binding scope, exact environment, arbitrary continuation, and equal framing of all other cells. It writes only `strength` and `character`. The bridge-free unbounded connection claim closes. |
| 280–313 | priority-20 outer-loop rule | Operational bridge. Accepted relative to the fixed model: exact loop/body and closed frame, `allStrings` guard, arbitrary continuation, and explicit values for all five changed locals. Its connection theorem is proved in `VERIFICATION` before this rule is imported, relying only on the previously connected yield/inner rules. |

There are 12 simplification rules: the eight projection-related rules at
96–135 and the four scan-branch rules at 141–176. There are two
`no-evaluators` symbols (`projectStrTotal`, `codesProject`), seven other total
function declarations, six partial function declarations, three syntax
macros, and three priority operational rules. There is no local
`[functional]` declaration. The exact text and attributes of each individual
rule are in the inventory rather than inferred from these group labels.

I do **not** label any candidate-local K rule unsound: each is valid on its
complete fixed-model guard, so no false-rule witness is asserted. The adverse
finding is instead a demonstrated implementation/contract adequacy failure.
This distinction avoids incorrectly calling a sound ASCII-model equation
globally false.

### Material source construct mapping

Every constructor used by `solution.mpy` has a fixed-semantics route:

| Program construct | Supplied declarations/rules |
|---|---|
| `Module`, `FuncDef`, `Params`, statement lists | `syntax.k`; `core.k` `#loadAll`/sequencing; `functions.k` closure binding |
| `Call`, `Name`, parameters, return | `core.k` lookup/argument order; `call.k` callee and closure dispatch; `functions.k` bind/frame/return/pop |
| `Assign`, `AugAssign`, `If`, `For` | `syntax.k` strictness; `controls.k` assignment, branches, and loop protocol |
| extension-list iteration | `controls.k` `#loop`; `list.k` `#iterNext`; `tuple.k` `#bindTgt` |
| string iteration | `str.k` `#iterNext`, which yields one-character strings |
| `character.isupper()` / `.islower()` | `call.k` bound methods; `methods.k` `applyMethod`, `hasUpper`, `hasLower`, and ASCII case predicates |
| `best_strength is None` and integer `>` | `operators.k`; `applyCmp("is", ..., noneV)`; `int.k` ordering |
| short-circuit `or` | `bool.k` left-to-right, value-returning short-circuit rules |
| integer `+`/`-` and augmented updates | `operators.k`, `int.k`, `controls.k` |
| final string concatenations | `operators.k`; `str.k` `applyBin("+", ...)` and total `seqConcat` |

The fixed configuration tracks control, environment, scopes, heap/allocation,
call stack, return state, exception state, and exit code. The connection claims
and bridges agree on their matched continuations and complete changed-local
footprints. Under the string/list preconditions, no material operation in this
program is fabricated or left unmodeled.

The relevant supplied limitation is explicit in `methods.k`: `isUpperC` is
`65..90` and `isLowerC` is `97..122`; `str.k` also only reduces source literals
whose code units are below 128. This is a fixed-model boundary, not a
candidate-added rule. It becomes fatal here only when combined with the
unfaithful Python rewrite demonstrated in Stage 2.

## 6. Fresh non-vacuity test

I did not rely on candidate `spec-vacuity.k`. The fresh
[`audit-vacuity-spec.k`](evidence/audit-vacuity-spec.k) executes the exact
submitted `STRONGEST-BODY` on the concrete satisfiable input
`class_name = ""`, `extensions = []`, but changes the required result from
`"."` to `"X"`.

Results in [`stage6-vacuity.log`](evidence/stage6-vacuity.log):

```text
kprove ... --dry-run
DRY_RUN_EXIT_STATUS=0

kprove ...
WarnStuckClaimState
actual <k>: str(iCons(46, .IntSeq)) ~> .K
PROOF_EXIT_STATUS=1
EXPECTED_FAILURE_CONFIRMED
```

The mutation parses and builds, reaches the result-bearing obligation, and
fails on the expected `46` (`"."`) versus `88` (`"X"`) mismatch. It is not a
parser error, timeout, missing import, unrelated crash, or unreachable claim.
The target proof is result-constraining and non-vacuous.

## 7. Proven versus assumed accounting

### What the successful K proof establishes

Conditioned on the trusted supplied MPY definition and K toolchain, the
submitted constructor program is partially correct for:

- every finite class-name `IntSeq`;
- the empty extension list, returning `class_name + "."`; and
- every nonempty finite `ValSeq` whose elements are `str(IntSeq)`.

For each fixed-model extension, it counts ASCII `A..Z` as `+1`, ASCII `a..z`
as `-1`, ignores every other integer code, selects the first strict maximum,
and returns the class, dot, and selected extension. The proof is unbounded in
list length and string length. It is a theorem about the exact submitted body,
not examples, bounded unrolling, or a substituted function.

### Trust ledger

| Boundary | Effect/dependents | Assessment |
|---|---|---|
| Read-only supplied MPY semantics | Meaning of every target and connection claim; values, control, state, and exceptions | Accepted as the campaign's fixed model after exact integrity comparison. |
| K 7.1.293, Haskell/LLVM backends, SMT/builtin reasoning, host Python | Compilation, symbolic closure, and concrete execution | Conventional toolchain trust; independently rebuilt rather than trusting candidate caches. |
| Candidate projection datatype simplifiers | Yield connection and symbolic string projections | Accepted ordinary datatype reasoning on guarded strings. Opaque nonstring interpretations cannot affect a target result. The projection claim alone is not independent because it is trivial under these simplifiers. |
| Three operational bridges | Inner and outer loop summaries used by target entries | Accepted relative to the fixed model: bridge-free/staged universal connections close over equal match domains, continuations, and state footprints. |
| MPY ASCII case model versus CPython Unicode | Score branches, strongest extension, final result | Documented model gap. Greek omega is a concrete model-vs-CPython witness. This would ordinarily support `CONCERNS` under amendment v2 only if the Python program remained canonical-faithful. |
| Python implementation versus trusted canonical | HumanEval source-contract meaning | **Illegitimate bridge.** Roman numeral `Ⅰ` is the concrete false-fidelity witness. The candidate's own differential oracle repeats the defect and supplies no independent support. |
| Termination | Liveness beyond reachability interpretation | Not separately claimed; the requested judgment is partial correctness. |

### Kit gates and benchmark mapping

- **Gate A (fixed-model real-term soundness): PASS.** Fresh `#Top`, exact body
  pinning, staged connection proofs, complete local-rule review, a satisfying
  state, body sensitivity, and false-result rejection all pass.
- **Gate B (intent adequacy): FAIL.** The real generated CPython program is not
  faithful to trusted canonical on a material nonempty list-of-strings input.
- **Gate C (trust/evidence auditability): FAIL for the claimed CPython
  bridge.** The candidate calls its self-mirroring oracle independent and
  reports Unicode fidelity, but it never tests the canonical `isalpha()` guard.

Campaign amendment v2 does not rescue the candidate:

1. The ASCII limitation does originate in the supplied model: yes.
2. The theorem covers every fixed-model `IntSeq`/all-string list without a
   candidate-added bound: yes.
3. The model boundary is documented with Greek omega: yes.
4. The submitted Python remains canonical-faithful on the gap: **no**, witnessed
   by `["A", "ⅠⅠ"]`.

There is no canonical-vs-docstring contradiction: both say uppercase/lowercase
**letters**, and canonical explicitly enforces alphabeticity. The second
campaign exception is inapplicable.

Accordingly, the reconstructed result is a sound but inadequate fixed-model
theorem. Under the benchmark's explicit mapping, a program-vs-canonical
divergence on the model gap is `FAIL / NOT_LEGIT`, not
`CONCERNS / LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
