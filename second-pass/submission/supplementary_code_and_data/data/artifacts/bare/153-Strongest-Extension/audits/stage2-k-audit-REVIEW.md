# Independent adversarial audit: 153-Strongest-Extension

The reconstructed K proof closes, executes the submitted constructor tree, and
is non-vacuous for seven fixed extension lists. It is not a legitimate proof of
the HumanEval contract. The formal domain is materially narrowed to those seven
lists, the submitted Python differs from the trusted canonical on valid string
inputs, and the generated semantics gives observably wrong results for Python
Unicode case predicates.

## 1. Input and provenance integrity

`/audit-input.json` declares `legacy-selected-stage1`,
`GENERATED_SEMANTICS`, problem `153-Strongest-Extension`, and condition `bare`.
I used its `container_paths` rather than its host provenance paths.

The audit mount is internally intact:

- `/audit-input.json` and `/audit-campaign-lock.json` are regular,
  non-symlinked files. The campaign lock object exactly equals the
  `audit_campaign` block and its SHA-256 is
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  matching the recorded hash.
- All launcher-declared mounts exist and are non-symlinked. All records required
  for `legacy-selected-stage1` are regular files: `/run.json`, `/task.json`,
  `/generation-result.json`, `invocation.json`, `metrics.json`,
  `codex-last.txt`, `codex-output.log`, and `prompt.txt`. The historical
  `usage.json` is present and was inspected. Historical runtime metrics are not
  required for this layout.
- Every individually recorded SHA-256 checked in `/audit-input.json` matches
  the mounted bytes, including the run/task/result/invocation records,
  generation prompt/output/metrics/usage, canonical source, trusted prompt,
  translator, and campaign lock.
- The structured trace is one regular JSONL file with the recorded hash
  `514e10b260d5a6c47bf8fac049fe53114dda41f4273de73fb05bb162db0d5d7b`.
  All 273 records parse: 1 session record, 84 event messages, 186 response
  items, 1 world-state record, and 1 turn-context record. The generation
  records claim `KPROVE_PASSED`; I treated that solely as an untrusted claim.
- The candidate tree has only regular files and directories. I independently
  hashed every candidate file; the proof-source hashes agree with hashes
  visible in the structured generation record. The launcher aggregate tree
  hash and a separate reviewer manifest digest are both retained in
  [integrity.log](evidence/stage1/integrity.log); no cross-algorithm equality
  was assumed.
- `/candidate/prompt.py` and `/candidate/py2mpy.py` are byte-identical to
  `/reference/prompt.py` and `/reference/py2mpy.py`.
- Consistent with `GENERATED_SEMANTICS`,
  `/reference/reference-semantics` is absent. I did not infer or use a hidden
  semantics.

There is no audit-infrastructure breach. The complete independent check and
commands are in [stage 1 evidence](evidence/stage1/).

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

On the intended successful domain, `class_name` is a string and `extensions`
is a nonempty list of string names. For each name, its strength is:

```text
number of alphabetic uppercase characters
- number of alphabetic lowercase characters
```

The function selects the first extension attaining the maximum strength and
returns `class_name + "." + selected_extension`. The trusted canonical makes
“letter” explicit with `x.isalpha()` before `x.isupper()` or `x.islower()`.
Both Python implementations raise `IndexError` on an empty extension list.

### Translation identity

I regenerated the constructor program from the scratch copy using the trusted
translator:

```bash
python3 trusted-py2mpy.py solution.py > regenerated-solution.mpy
cmp regenerated-solution.mpy solution.mpy
```

Both commands exited 0. Both files have SHA-256
`d9f8d0fa5709221787385385e4d65fe81e32148f33399f3a28c14dec786b1184`.
Thus `solution.mpy` is the authentic translation of the submitted
`solution.py`.

### Differential result

The submission omits the canonical `isalpha()` guard. That is observable for
Unicode cased non-letters. The fixed witness

```python
Strongest_Extension("C", ["A", "ⅣⅣ"])
```

returns `C.A` in the trusted canonical because Roman numeral four is not
alphabetic, but returns `C.ⅣⅣ` in the submitted implementation because
`"Ⅳ".isupper()` is true.

The independent test covers both prompt examples, an empty input list,
singleton and empty-name boundaries, greater/equal/less comparison branches,
uppercase/lowercase/uncased character branches, negative strengths, Unicode
letters, Unicode cased non-letters, and 500 deterministic generated cases.
It found 94 mismatches among 514 cases (seed `1532026`; corpus SHA-256
`8b8a108c38cb5520cf6ea6367c9c1066145296488e9c507bc6941cf92c27efda`).
See [differential.py](evidence/stage2/differential.py) and
[stage2.log](evidence/stage2/stage2.log). Its exit 1 intentionally records the
found divergences.

This is a material implementation-versus-canonical failure on the unrestricted
string domain.

## 3. Clean proof reconstruction

I copied only source artifacts into
`/tmp/audit-work/153-strongest-extension`. No candidate compiled definition,
cache, or trace was copied. K reports version `7.1.293`.

### Fresh builds

```bash
kompile --backend llvm semantic.k \
  --main-module SEMANTIC --syntax-module MPY-SYNTAX \
  --output-definition semantic-kompiled
# exit 0

kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module VERIFICATION \
  --output-definition verification-kompiled
# exit 0
```

The bounded logs are
[kompile-llvm.log](evidence/stage3/kompile-llvm.log) and
[kompile-haskell.log](evidence/stage3/kompile-haskell.log).

### Concrete execution

The fresh LLVM definition executes the prompt example, singleton, empty
extension name, greater and equal comparison cases, and Unicode witnesses.
The ordinary ASCII and boundary results agree with Python. An empty list
reaches the unmodeled residual `Subscript(listVal(.Values), Int(0))`; both
Python implementations instead raise `IndexError`. Since the successful source
domain is nonempty, this exception-model omission is not a separate verdict
driver.

The generated semantics fails on material non-ASCII strings:

```text
input:       ("C", ["A", "ÉÉ"])
canonical:   C.ÉÉ
submission:  C.ÉÉ
fresh K:     C.A
```

The exact K configurations and Python oracle results are in
[concrete-execution.log](evidence/stage3/concrete-execution.log).

### Positive claims

The original combined target command was:

```bash
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

It printed `#Top` and exited 0. I then made a mechanically identical
specification copy with labels only and independently selected all seven
claims. Every selected command printed `#Top` and exited 0:

1. `prompt_worked`
2. `prompt_tie`
3. `later_stronger`
4. `uncased_characters`
5. `empty_first`
6. `all_negative`
7. `singleton`

The original combined log, labeled spec, per-claim commands, outputs, and exit
statuses are in [stage 3 evidence](evidence/stage3/).

Therefore the dynamic reconstruction gate passes for the candidate's seven
formal claims. It does not establish that those claims are adequate or that
the generated semantics represents Python.

## 4. Adequacy and real-program pinning

### Plain-language claims

All seven claims share this precondition: `<k>` contains the submitted module
followed by `#start`; `<env>` and `<functions>` are initially empty; `<result>`
is `noResult`; and the two input cells contain the stated class and extension
values. Each postcondition requires `<k>` to be empty and `<result>` to contain
one exact returned string. The final environment and function map are
existentially framed but the returned value is not.

| Claim | Input scope | Required returned value |
|---|---|---|
| Prompt worked example | exact class `Slices`; exact three-name list | `Slices.SErviNGSliCes` |
| Prompt tie | every `C:String`; exact `["AA","Be","CC"]` | `C + ".AA"` |
| Later stronger | every `C:String`; exact `["abc","AB","A-b"]` | `C + ".AB"` |
| Uncased characters | every `C:String`; exact `["a-1","--","A!"]` | `C + ".A!"` |
| Empty first name | every `C:String`; exact `["","123","!"]` | `C + "."` |
| All negative | every `C:String`; exact `["abcd","a","xy"]` | `C + ".a"` |
| Singleton | every `C:String`; exact `["Zz"]` | `C + ".Zz"` |

Every precondition is satisfiable. For symbolic class names I used
`C = "Witness"`; the prompt claim uses its fixed class. The independent
contract oracle, canonical Python, and submitted Python agree on the concrete
result for every one of these seven states. See
[pinning-and-witnesses.log](evidence/stage4/pinning-and-witnesses.log).

### Program pinning

Fresh `kast --output kore` results for the trusted-regenerated
`solution.mpy` and candidate `StrongestProgram` macro are byte-identical, both
with SHA-256
`dc36b7af44a15073a25d03ecb3a267255173fbbcfbc362ec3f11fa8ac06b734c`.
The macro therefore expands to the same function binding and constructor body;
the claims do not execute a substituted program.

A body-sensitivity mutation changed the delimiter in the macro-expanded return
from `"."` to `":"`, rebuilt successfully, and made `kprove` exit 1. Its
residual shows the executed mutated body returning
`Slices:SErviNGSliCes` against the required dotted result. See
[body-mutation.diff](evidence/stage4/body-mutation.diff) and
[body-mutation-kprove.log](evidence/stage4/body-mutation-kprove.log).

### Material adequacy failure

No claim quantifies over `extensions` or over extension-name strings. There is
no general loop claim, invariant, or summary theorem. Six claims quantify only
over the class name; all seven extension lists are finite constants.

Consequently, even ignoring the implementation and semantic divergences, the
proof establishes seven examples/boundaries rather than the unrestricted
HumanEval domain. This is a material source-contract narrowing and maps to
`FAIL / NOT_LEGIT` under the benchmark's explicit decision rule.

## 5. Rule-by-rule static soundness review

The exhaustive inventory is
[rule-inventory.md](evidence/stage5/rule-inventory.md). The source contains:

- all syntax productions required by `solution.mpy`;
- 31 local operational/function rules in `semantic.k`;
- 11 rules in `verification.k`, including the exact-body macro and ten `ref*`
  equations;
- seven entry claims;
- two local `[function,total]` declarations (`isUpperChar` and
  `isLowerChar`);
- no local priority rule, simplification rule, opaque symbol, helper
  reachability claim, or operational execution summary.

Every used constructor maps to explicit syntax and behavior: module/function
loading, parameter binding, name lookup, assignments, integer updates, the two
subscripts, list/string loops, string-method calls, conditionals, comparison,
concatenation, and return. Evaluation-order looseness for binary operands is
unobservable in this body because those operands are pure lookups and
literals. The task-specific `#start` rule selects the exact installed binding.
The simple return rule is overly broad for arbitrary continuations, but the
submitted return is terminal and no concrete or symbolic false result is
enabled on this program's control-flow path; I therefore record that as a
reuse limitation, not an unsoundness.

The `ref*` functions do not replace program execution. They are terminating
definitional postcondition computations on the seven ground lists. The full
submitted body executes separately. Thus the positive `#Top` is not produced
by an unconstrained result oracle or an operational bridge that skips the body.

### Witnessed unsound used rules

`semantic.k` lines 132–141 identify Python `str.isupper()` and
`str.islower()` with ASCII ordinal ranges:

```k
isUpperChar(S) => 65 <= ordChar(S) <= 90
isLowerChar(S) => 97 <= ordChar(S) <= 122
```

These predicates then directly determine the source method-call results. This
is false over the stated string domain:

- Uppercase witness: `"É".isalpha()` and `"É".isupper()` are true. Both Python
  implementations return `C.ÉÉ` for `("C", ["A","ÉÉ"])`, while fresh K
  execution returns `C.A`.
- Lowercase witness: `"é".isalpha()` and `"é".islower()` are true. Both Python
  implementations return `C.a` for `("C", ["a","éé"])`, while fresh K
  execution gives `"éé"` score zero and returns `C.éé`. See
  [unicode-lower-witness.log](evidence/stage5/unicode-lower-witness.log).

These are concrete false observable conclusions on intended inputs, not gaps
for unused syntax. There is no bridge-free universal theorem connecting the
ASCII rules to CPython Unicode behavior. The `refDelta` postcondition
definitions inherit the same restricted classification.

## 6. Fresh non-vacuity test

There was no candidate `spec-vacuity.k` to rely on. I created a distinct fresh
claim using the satisfiable prompt input but requiring the false return
`Slices.Cheese` instead of `Slices.SErviNGSliCes`.

```bash
kprove spec-vacuity-audit.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY-AUDIT --dry-run
# exit 0

kprove spec-vacuity-audit.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY-AUDIT
# exit 1
```

The proof failure is meaningful: `WarnStuckClaimState` shows `<k> .K` and the
actual returned value `Slices.SErviNGSliCes`, which cannot unify with the false
postcondition. It is not a parser error, import error, timeout, or unreachable
mutation. The mutation and bounded log are in
[stage 6 evidence](evidence/stage6/).

The seven finite claims are therefore result-constraining and non-vacuous.
Non-vacuity does not expand their domain or validate the language model.

## 7. Proven versus assumed accounting

### What is actually proven

Conditional on K 7.1.293 and the candidate's generated semantics, executing the
exact translated submitted body from the seven listed initial configurations
terminates with the seven exact listed results. Six claims allow an arbitrary K
string as `class_name`; their extension lists remain fixed. The proof unfolds
all finite loops and separately reduces the ground `ref*` definitions. It does
not prove a theorem for an arbitrary extension list.

### Trust and assumption ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K parser/compiler, Haskell prover, LLVM executor, and built-in `Int`, `Bool`, `String`, and `Map` operations | all build, execution, and proof results | Ordinary low-level trust boundary; versions and fresh commands are recorded. |
| Trusted `py2mpy.py` translation | source-to-constructor identity | Acceptable here: trusted regeneration is byte-identical and the claim macro is mechanically KORE-identical. |
| `StrongestProgram` macro | all claims | Acceptable syntactic abbreviation; it expands to the real submitted body and the body-sensitivity mutation fails as expected. |
| `refDelta`, `refStrength*`, and `refSelect` equations | exact postconditions | Acceptable only as transparent definitions for the seven fixed ASCII lists. They are not opaque and do not replace execution, but they do not establish the unrestricted contract. |
| Generated `isUpperChar`/`isLowerChar` as interpretations of Python methods | branch choices, strengths, selected extension, all returned values | Illegitimate over the intended string domain; both uppercase and lowercase Unicode result divergences are witnessed. |
| Submitted `solution.py` as an implementation of the trusted canonical | the requested real-program theorem | Illegitimate over the intended string domain; omission of `isalpha()` yields 94 recorded differential mismatches, including `["A","ⅣⅣ"]`. |
| Seven fixed extension lists as coverage of arbitrary nonempty `list[str]` | theorem adequacy | Illegitimate material domain narrowing. Examples and finite unrolling cannot prove the unrestricted HumanEval contract. |
| Empty-list exception and general Python call/return machinery | excluded behavior | Not formally modeled. Empty list is outside the successful nonempty domain; the broader reusable-language gaps are not needed for the actual successful paths. |

Generation prose, prior traces, `codex-last.txt`, and the historical `#Top`
were not used as proof. Differential testing supports the concrete bridge
findings only; it is not a substitute for the K reachability proof.

### Gate and decision summary

- Clean dynamic reconstruction of the submitted seven claims: **pass**.
- Real-program semantic soundness: **fail**, due to witnessed used Unicode
  method-rule divergences.
- Intent/domain adequacy: **fail**, because only seven fixed extension lists
  are proved.
- Evidence auditability and false-result discrimination: **pass**.

Any one of the first two failures prevents a legitimate proof of the requested
program. Together with the independent implementation/canonical divergence,
the required benchmark classification is unambiguous.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
