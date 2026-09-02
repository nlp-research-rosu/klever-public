# Independent adversarial review: 28-concatenate

The candidate's recorded `#Top` is reproducible, its implementation is correct
on the Python `List[str]` contract, and its proof-local rules do not expose a
concrete false conclusion on that domain. The submitted proof nevertheless does
not contain a universal reachability claim for the actual function entry and
return. Its only universal claim starts at an already-established internal
`#loop` state; its only claims that load and call the submitted function use two
fixed inputs. That missing program-level obligation materially limits what the
immutable candidate proves and is decisive under this audit's decision
boundary.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout =
"legacy-selected-stage1"` and `semantics_mode = "SUPPLIED_SEMANTICS"`. The
trusted `/reference/reference-semantics` mount is present, as that mode
requires.

I independently checked the launcher-owned records rather than following their
host-only provenance paths:

- `/audit-campaign-lock.json` is a regular readable file. Its SHA-256 is
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  exactly the value in `/audit-input.json`, and its parsed object equals the
  `audit_campaign` block.
- `/run.json`, `/task.json`, `/generation-result.json`,
  `/generation-evidence/invocation.json`, `metrics.json`, `codex-last.txt`,
  `codex-output.log`, `prompt.txt`, and the structured trace are present,
  readable, non-symlinked, and match their recorded direct hashes. The optional
  `usage.json` is present and matches its hash. The absent
  `runtime-metrics.json` is not required for this legacy layout.
- All 278 lines of the one structured trace file parse as JSON. The trace file
  hash is
  `d846dd344a283d2bfb91a591aae0cb660aafc3eb729d91391bc723f2cae271eb`,
  matching `/generation-result.json`; the trace contains 25 generation-time
  shell calls and one final-answer event. The complete 14,089-line
  `codex-output.log`, `codex-last.txt`, and generation prompt were read and
  hashed. Their claims of success were treated only as untrusted history.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to
  `/reference/prompt.py` and `/reference/py2mpy.py`.
- A recursive path/type/content comparison of the candidate and trusted
  `reference-semantics/` trees found the same 24 regular files, no missing or
  additional entry, no type difference, no symlink, and identical bytes for
  every file.
- The required candidate proof artifacts `solution.py`, `solution.mpy`,
  `verification.k`, `spec.k`, and `prove.sh` are regular files.

The reproducible check and per-file supplied-semantics manifest are in
`evidence/01-integrity/audit_integrity.py` and
`evidence/01-integrity/integrity.log`. There is no audit infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt requires:

> Given a finite `List[str]`, return the strings concatenated in list order.

Thus `[]` maps to `""`, `["a", "b", "c"]` maps to `"abc"`, empty elements are
identities, and neither list length nor Python string contents are bounded by
the contract. The trusted canonical implementation is `return ''.join(strings)`.

The candidate uses:

```python
result = ""
string = ""
for string in strings:
    result += string
return result
```

For every `List[str]`, its loop invariant is that `result` is the concatenation
of the processed prefix. The extra initialization of `string` only determines
the loop variable after an empty loop and does not affect the returned value.

In the clean scratch copy, trusted regeneration used:

```text
python3 /reference/py2mpy.py solution.py > solution.regenerated.mpy
```

Both submitted and regenerated files have SHA-256
`76f72a295e084927590a18af5a031a11a16dad65c5673d5fd10d1d29ce127456`;
`cmp` exited 0. See `evidence/02-fidelity/translation.log`.

The independent differential script imports
`/reference/canonical.py:concatenate` and the scratch copy of candidate
`solution.py:concatenate`. It covers the two examples, zero/one/many loop
iterations, empty elements, long strings and lists, embedded control/NUL
characters, Unicode, and 5,000 seeded generated cases. Command and result:

```text
python3 /audit-output/evidence/02-fidelity/differential_test.py
total_cases=5013
mismatches=0
DIFFERENTIAL_PASS
EXIT_STATUS: 0
```

The preserved case generator and result are
`evidence/02-fidelity/differential_test.py` and
`evidence/02-fidelity/differential.log`. This finite evidence supports program
fidelity; it is not substituted for a universal K claim.

## 3. Clean proof reconstruction

I copied candidate source artifacts and the trusted supplied semantics to
`/tmp/audit-work/28-concatenate-audit`. No candidate-compiled definition or
cache was copied or used. The live tools are K `v7.1.293`.

Fresh concrete build:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
EXIT_STATUS: 0
```

An independently authored ASCII normal/boundary program then ended with `.K`,
`NoExc`, exit code `0`, and process status 0. See
`evidence/03-reconstruction/kompile-llvm.log`,
`concrete_boundary_ascii.py`, and `krun-boundary-ascii.log`.

A separate test with a Unicode source literal stopped at
`strToCodes("\xce\xbb")` and exited 113. This is the supplied semantics'
documented ASCII-only literal boundary, not a transient container failure:
normal ASCII execution works and `semantics/str.k` guards literal conversion
with code point `< 128`. The exact failure is preserved in
`evidence/03-reconstruction/krun-boundary.log`.

Fresh proof build:

```text
kompile verification.k --backend haskell \
  --main-module CONCATENATE-VERIFICATION \
  --syntax-module CONCATENATE-VERIFICATION \
  --output-definition verification-kompiled
EXIT_STATUS: 0
```

The immutable candidate proof as a whole reconstructed:

```text
kprove spec.k --definition verification-kompiled \
  --spec-module CONCATENATE-SPEC
#Top
EXIT_STATUS: 0
```

I also copied the three claims without semantic changes into a labeled audit
spec and selected each independently:

```text
kprove spec-labeled.k --definition verification-kompiled \
  --spec-module CONCATENATE-SPEC-LABELED \
  --claims CONCATENATE-SPEC-LABELED.loop
#Top
EXIT_STATUS: 0

... --claims CONCATENATE-SPEC-LABELED.empty
#Top
EXIT_STATUS: 0

... --claims CONCATENATE-SPEC-LABELED.abc
#Top
EXIT_STATUS: 0
```

The exact source, commands, complete bounded outputs, and statuses are under
`evidence/03-reconstruction/`. Fresh reconstruction therefore confirms the
candidate's positive execution marker. It does not by itself establish that
the claim set states the required theorem.

## 4. Adequacy and real-program pinning

### Plain-language claim accounting

The first claim says:

- start at an internal `#loop(list(VS), Name("string"),
  concatenateLoopBody)` with any continuation `CONT`;
- in the current unannotated function scope, `result` is `str(A)`, the loop
  variable is `OLD_STRING`, and `strings` has arbitrary saved value `ARGUMENT`;
- require every element of `VS` to be a K string;
- reach the same `CONT`, preserving the argument binding, changing `result` to
  `str(concatenateValues(A, VS))`, and changing the loop variable to the last
  element (or preserving its old value for the empty sequence).

This is an unrestricted, satisfiable loop-summary theorem. For example,
`VS=.ValSeq`, `A=.IntSeq`, `OLD_STRING=str(.IntSeq)`, a local scope at `L=1`,
and the ordinary framed cells satisfy its precondition. A nonempty satisfying
example uses `VS=["a","b","c"]`; its claimed accumulator is `"abc"` and its
final loop variable is `"c"`.

The second claim loads the candidate module and calls `concatenate([])` from a
fresh module configuration. It constrains the result to the empty K string,
with no exception and exit code 0.

The third does the same for `concatenate(["a","b","c"])` and constrains the
result to the code sequence for `"abc"`.

Ground substitutions for `[]`, `["a","b","c"]`, `["x","","y"]`, and Unicode
strings agree among the loop fold, candidate Python, and canonical Python; see
`evidence/04-adequacy/ground_witnesses.py` and `ground-witnesses.log`.

### Constructor identity and body sensitivity

Trusted regeneration pins `solution.py` to `solution.mpy`. Candidate
`concatenateLoopBody`, `concatenateBody`, and `concatenateModule` normalize to
the exact constructor sequence in that regenerated module. A configuration
reachability comparison normalized both sides identically and closed with
`#Top` (`WarnTrivialClaim`), as recorded in
`evidence/04-adequacy/pinning-config.k` and
`kprove-pinning-config.log`. An earlier bare functional form was rejected by
the backend as an unsupported functional claim; it is preserved separately and
is not relied upon.

The actual fixed semantics covers all material operations: module loading,
typing-only import, function binding, argument evaluation and allocation,
parameter binding, both initial assignments, one-time list dereference, list
iteration, target binding, augmented string addition, return, and frame pop.
The general loop precondition matches the real function frame immediately
before each loop: parent scope 0, the three exact locals, and an arbitrary
framed heap containing the input list.

A body-sensitivity experiment changed the program term actually expanded by
`concatenateModule`: `result += string` became `result = string`. The mutated
definition built successfully, but the real `abc` entry claim exited 1 with a
reachable final value `"c"` rather than `"abc"`. See
`evidence/04-adequacy/verification-body-mutated.k`,
`body-mutation-kompile.log`, and `body-mutation-kprove-abc.log`. The theorem is
therefore sensitive to the executed body, not merely to an external
`solution.py` file.

### Decisive missing target obligation

No claim in candidate `spec.k` both:

1. starts from (or is mechanically connected within that claim to) arbitrary
   real `concatenate` arguments, and
2. reaches the function's returned concatenation.

The universal claim begins only after module loading, lookup, call/frame
creation, parameter binding, the two initial assignments, and iterable
dereference have already happened; it ends before the return and frame pop.
Those fixed-semantics steps are exercised end-to-end only by the two concrete
entry claims. The loop lemma makes the missing universal entry proof
straightforward, but a paper composition of an internal lemma with two examples
is not the submitted K reachability theorem for arbitrary `List[str]`.

To rule out a tool or semantics blocker, I authored a separate audit spec that
copies the loop lemma and adds the omitted claim

```text
#loadAll(concatenateModule)
~> Call(Name("concatenate"), (list(VS), .Exprs))
=> str(concatenateValues(.IntSeq, VS))
requires allStringValues(VS)
```

It closed with `#Top` and exit 0
(`evidence/04-adequacy/missing-universal-entry.k` and
`missing-universal-entry-kprove.log`). This shows that the defect is exactly an
omitted target obligation, not an inability to prove it. The reviewer-authored
claim is not part of immutable candidate `spec.k` and cannot retroactively be
credited as a submitted positive target claim.

Consequently, the complete-function theorem in the candidate is limited to two
fixed examples. Under the benchmark's explicit rule that finite examples do
not prove the unrestricted HumanEval domain, this is a material adequacy
failure rather than a non-fatal maintenance observation.

## 5. Rule-by-rule static soundness review

`evidence/05-static/rule_inventory.py` and `rule-inventory.txt` enumerate every
declaration from the 24 supplied K files, `verification.k`, and `spec.k`: 708
rules, 235 syntax declarations, five contexts, one configuration, and three
claims. They also list all `function`, `total`, `owise`, `concrete`, priority,
opaque `symbol`, and `no-evaluators` occurrences. There is no local
`simplification` rule and no `functional` claim. The exhaustive disposition,
including the imported-but-inert partition, is in
`evidence/05-static/rule-assessment.md`.

### Material syntax and fixed rules

The constructor vocabulary used by `solution.mpy` maps to:

- `Module`, `ImportFrom`, `FuncDef`, `Params`, `Assign`, `Name`, `Str`, `For`,
  `AugAssign`, `Return`, `ListExpr`, and `Call` in `semantics/syntax.k`;
- configuration, load/sequencing, lookup, allocation, and left-to-right
  argument machinery in `core.k`;
- list construction and iterator base/step in `list.k`;
- binary dispatch in `operators.k`;
- ASCII literals, `seqConcat`, and supplied string addition in `str.k`;
- assignment, import no-op, `For`, `#loop`, and loop continuations in
  `controls.k`;
- name-target binding in `tuple.k`;
- function binding, parameter binding, return, and pop in `functions.k`;
- call routing and unannotated closure frame creation in `call.k`.

Evaluation order comes from the syntax strictness attributes plus the explicit
left-to-right argument loop. Allocation is fresh and monotone. The function
call saves/restores its continuation and environment; the loop summary does not
discard `CONT`. This program has no exceptional, output, mutation, break, or
continue behavior that is skipped by the claim.

All other supplied rules are rewrite-head-inert for this term. This includes
all imported opaque float, sorting, and MD5 symbols: none affects the result,
branching, state, exception, or control of any candidate claim. Compiler
non-exhaustiveness warnings for unrelated total functions are recorded but do
not become proof defects for this program. The one material language limitation
is ASCII-only source-literal conversion, witnessed dynamically above; abstract
input `str(IntSeq)` values are not restricted by that literal parser.

### Candidate extensions

The proof-local inventory has thirteen rules:

- `isStringValue` has a string case and disjoint `owise` fallback.
- `allStringValues`, `concatenateValues`, and `finalLoopValue` have exhaustive
  empty/cons cases and strict structural descent.
- `stringCodes(str(S)) = S` is a truthful projection. Its declaration is
  over-broadly marked `[total]` although its equations do not cover non-string
  `Val`; every result-bearing theorem use is under `allStringValues`, so this
  does not admit a false intended-domain conclusion.
- The three zero-argument constructor functions expand exactly to the
  translated loop body, function body, and module.
- The added guarded `applyBin("+", str(A), V)` rule is an operational symbolic
  bridge and is genuinely proof-relevant. Removing it makes the loop claim
  exit 1 with symbolic `applyBin("+", str(A), V)` left in the residual
  (`main-no-bridge-kprove-loop.log`).

For every ground state in its guard, `isStringValue(V)` is true exactly when
`V=str(B)`. Then `stringCodes(V)=B`, so the bridge gives
`str(seqConcat(A,B))`, identical to the supplied string-addition rule. It reads
or writes no cell and preserves the surrounding continuation. A definition
without the bridge proved both ground witnesses and the universal constructor
form with `#Top`
(`bridge-constructor-connection-kprove.log` and
`bridge-ground-kprove.log`). The syntactically broader guard-form connection
claim remained stuck because the backend did not invert the symbolic
discriminator (`bridge-connection-kprove.log`).

The candidate itself should have supplied a bridge-free connection theorem
over its exact guard form. Its absence is a proof-audit limitation. It is not
labeled unsound: there is no intended-domain ground witness producing a wrong
value, branch, cell, exception, or continuation, and the exhaustive predicate
equations plus constructor theorem establish the ordinary mathematical
justification. No proof-local rule encodes a free oracle or fabricates the task
answer; `concatenateValues` is a transparent sequence-append fold while the
real loop still executes.

## 6. Fresh non-vacuity test

The candidate contains no `spec-vacuity.k`. I created
`evidence/06-nonvacuity/spec-vacuity.k` from the real `abc` entry claim and
changed only its required last code point from 99 (`c`) to 100 (`d`). The
starting state is the same satisfiable fresh module configuration as the
positive claim.

The mutation first built through the proof frontend:

```text
kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module CONCATENATE-SPEC-VACUITY --dry-run
EXIT_STATUS: 0
```

The actual proof then exited 1 with `WarnStuckClaimState`. Its residual contains
the fully executed real module and actual result
`str(iCons(97,iCons(98,iCons(99,.IntSeq))))`, which does not unify with the
mutated `...100...` destination. See `vacuity-dry-run.log` and
`vacuity-kprove.log`. This is the expected unmet result obligation, not a parse,
import, timeout, or unrelated backend failure.

The mutation establishes non-vacuity of the fixed `abc` entry claim. Together
with the separate body mutation, it also shows execution and result sensitivity.
It does not broaden that claim's fixed input domain.

## 7. Proven versus assumed accounting

What the immutable candidate successfully proves under the supplied theory is
precisely:

1. the isolated loop summary for every finite K `ValSeq` satisfying
   `allStringValues`;
2. complete execution of `concatenate([])` returning `""`; and
3. complete execution of `concatenate(["a","b","c"])` returning `"abc"`.

This is partial-correctness reachability. The candidate comment calling the
loop claim “total-correctness” is not credited as a termination theorem.

The trust/assumption ledger is:

| Boundary | Dependents | Assessment |
|---|---|---|
| Supplied MPY operational rules listed in the material slice | All three candidate claims | Acceptable fixed semantics for the constructs actually used; freshly built and concretely exercised. |
| K built-in integers, booleans, strings, maps, lists, equality, and reachability/circularity engine | All claims and helper equations | Ordinary low-level K trust boundary. |
| `str(IntSeq)` as the abstract Python-string model and `seqConcat` as append | Loop postcondition and both entry results | `seqConcat` is defined by exhaustive equations. Mapping the abstract code sequence to Python `str` is an intended-model bridge, supported by the canonical differential test. |
| ASCII-only `Str(String)` conversion | Concrete literals in the module and example claims | Correct for the submitted empty literal and `a,b,c`; materially incomplete for Unicode source literals, as the fresh exit-113 witness shows. It does not constrain abstract `str(IntSeq)` loop inputs. |
| Guarded proof-local `applyBin` bridge | Universal loop closure | Value- and control-preserving on intended ground states; constructor theorem and ground witnesses close. Exact symbolic guard-form connection is an auditability limitation, not a witnessed false rule. |
| Constructor abbreviations for loop/body/module | All claims | Mechanically normalize to trusted-translator output; body mutation is detected. |
| Python differential testing | Implementation-to-canonical bridge only | 5,013 finite cases with zero mismatches; not a universal proof and not used as a replacement for K reachability. |
| Arbitrary-input function-entry/return composition | The HumanEval contract | **Not a candidate theorem.** It is only an informal composition of the universal internal loop lemma with fixed semantics and two concrete entry examples. The audit-only universal entry claim closes, but it is excluded from candidate proof accounting. |

Thus the candidate's theory is discriminating and appears sound for its stated
claims, but its submitted positive target set omits the unrestricted
program-level result theorem. The benchmark directs that this material
source-contract scope gap be reported as `FAIL / NOT_LEGIT`, even though a
reviewer-authored repair claim demonstrates that the missing obligation is
provable.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
