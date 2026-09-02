# Independent adversarial review: 141-file-name-check

The candidate is **not a legitimate proof of the submitted program under the
supplied semantics**. A clean build does produce `#Top`, the claims constrain
their return values, and the executed body is constructor-identical to the
regenerated program. The fatal defect is narrower and decisive: six
proof-local priority rules replace fixed string computations with four
uninterpreted, result-bearing observations. No equations or bridge-free
connection theorem relate those observations to the displaced computations.
The claim preconditions then reuse the same observations, making the proof
circular.

## 1. Input and provenance integrity

The launcher declares:

- problem `141-file-name-check`;
- condition `semantics`;
- semantics mode `SUPPLIED_SEMANTICS`;
- record layout `legacy-selected-stage1`;
- complete input provenance.

I read `/audit-input.json`, its `record_layout`, `container_paths`, hashes, and
integrity fields before inspecting candidate claims. I also read
`/audit-campaign-lock.json`, `/run.json`, `/task.json`,
`/generation-result.json`, all required `legacy-selected-stage1` records under
`/generation-evidence`, the optional `usage.json`, and all 272 JSON objects in
the one structured JSONL trace. Generation prose, logs, traces, and prior
`#Top` outputs were treated only as untrusted claims.

The independent checker and complete bounded result are
[`provenance_check.py`](evidence/provenance_check.py) and
[`01-provenance-check.log`](evidence/01-provenance-check.log). Results:

- The campaign lock JSON exactly equals the campaign block in
  `/audit-input.json`; its SHA-256 is the recorded
  `ad5dfc...78d745`.
- Every launcher-declared mount and every record required for
  `legacy-selected-stage1` is present with the required regular-file or
  directory type. `usage.json` is present and valid. Historical runtime
  metrics are not required for this layout.
- The recorded SHA-256 values match the mounted campaign lock, canonical
  program, trusted/candidate prompts, trusted/candidate translators,
  invocation, metrics, usage, generation prompt, Codex last/output files,
  run/task/result manifests, and the structured trace file.
- The structured trace has the recorded file hash
  `a953de...4f755` and all 272 lines parse as JSON.
- The candidate prompt and translator are byte-identical to their trusted
  mounts.
- `/reference/reference-semantics` is present, as required by
  `SUPPLIED_SEMANTICS`. Recursive path, entry-type, and byte comparison of all
  25 entries against `/candidate/reference-semantics` is exact. Neither tree
  contains a symlink. There are no missing or additional candidate semantics
  entries.
- The full candidate mount has 39 inventoried entries (36 regular files and
  three directories) and no symlinks. All required proof artifacts are regular
  files.

I also computed reviewer-defined deterministic tree manifests and common
tree-hash encodings in
[`01-tree-hash-probe.log`](evidence/01-tree-hash-probe.log). These are
independent checks, not substitutes for the launcher’s private tree-hash
format. The authoritative file hashes and recursive byte/type comparison
above all agree.

There is no provenance or semantics-mode infrastructure breach, so a candidate
verdict is appropriate.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

From `/reference/prompt.py`, a filename returns `"Yes"` iff:

1. it contains at most three ASCII digits `0` through `9`;
2. it contains exactly one dot;
3. the substring before the dot is nonempty and begins with an ASCII Latin
   letter `A` through `Z` or `a` through `z`; and
4. the substring after the dot is exactly `txt`, `exe`, or `dll`.

Otherwise it returns `"No"`.

`/candidate/solution.py` implements this contract by checking dot count,
minimum possible valid length, the first code point against the explicit ASCII
ranges, the last four characters against `.txt/.exe/.dll`, and the sum of ten
single-character counts. Counting digits in the whole name is equivalent to
counting them in the base because every permitted suffix contains no digit.

### Trusted regeneration

Using only the copied source and trusted `/reference/py2mpy.py`:

```text
python3 py2mpy.py solution.py > solution.regenerated.mpy
cmp -s solution.regenerated.mpy solution.mpy
```

Both commands exited zero. The submitted and regenerated `.mpy` files are byte
identical with SHA-256
`fbf977102870b192415a1efc8f17c21adba0b8aeb4667595e7bc8ab41e58777a`.
See [`02-translation-identity.log`](evidence/02-translation-identity.log).

### Independent differential evidence

[`differential_test.py`](evidence/differential_test.py) imports both the
trusted canonical entry point and the generated candidate entry point. It uses
an independently written literal contract oracle, 31 named example/boundary
cases, exhaustive strings of lengths zero through five over a mixed alphabet,
and 20,000 deterministic generated strings up to length 40.

The run covered 130,226 distinct inputs:

- candidate versus prompt-contract mismatches: **0**;
- candidate versus trusted canonical mismatches: **3**;
- canonical versus prompt-contract mismatches: **3**.

The three mismatches are `é.txt`, `α.exe`, and `a١٢٣٤.dll`. They arise because
the canonical implementation uses Python’s Unicode-wide `isalpha()` and
`isdigit()`, while the prompt explicitly names ASCII Latin letters and digits
`0` through `9`. I judge the generated implementation to follow the written
contract on these cases; the discrepancy is recorded rather than hidden.
Complete scope and results are in
[`03-differential-test.log`](evidence/03-differential-test.log). This finite
evidence supports implementation fidelity only; it is not a universal K proof.

## 3. Clean proof reconstruction

No candidate-provided definition or cache was used. Source artifacts were
copied to `/tmp/audit-work/reconstruction`, with the supplied semantics copied
from the trusted reference mount. Tool versions are recorded in
[`00-toolchain.log`](evidence/00-toolchain.log): K `v7.1.293` and Python
`3.10.12`.

### Concrete definition

[`make_concrete_driver.py`](evidence/make_concrete_driver.py) appended 19
independent example, empty, dot-count, length, first-character, suffix, and
digit-boundary assertions to the exact submitted source. CPython passed them.
The trusted translator generated the driver, and this fresh command succeeded:

```text
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

The subsequent fresh `krun` ended with `.K`, `NoExc`, and exit code `0`.
Commands, compiler status, and output are in
[`04-concrete-build.log`](evidence/04-concrete-build.log) and
[`05-concrete-krun.log`](evidence/05-concrete-krun.log).

### Proof definition and every target claim

The fresh proof build was:

```text
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

It exited zero; see [`06-proof-build.log`](evidence/06-proof-build.log).

The aggregate target command:

```text
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

printed `#Top` and exited zero
([`07-kprove-all.log`](evidence/07-kprove-all.log)).

To prevent an aggregate result from hiding an individual target,
[`split_claims.py`](evidence/split_claims.py) mechanically produced six
one-claim modules. All six independent `kprove` commands printed `#Top` and
exited zero. Exact commands and outputs are in
`evidence/08-kprove-claim-{1..6}.log`.

Thus the clean dynamic reconstruction gate succeeds. This establishes closure
only under the candidate’s extended theory; it does not establish that the
extensions are truthful.

## 4. Adequacy and real-program pinning

### Plain-language formal claims

The claims partition inputs according to terms that are *intended* to denote
string observations:

1. `charCount(CS,46) != 1` returns `"No"`.
2. Dot count is one and `isLen(CS) < 5` returns `"No"`.
3. Dot count is one, length is at least five, and
   `latinCode(headCode(CS))` is false returns `"No"`.
4. The prior checks pass and `allowedSuffix(CS)` is false returns `"No"`.
5. The structural checks and suffix pass and `digitCount(CS) > 3` returns
   `"No"`.
6. The structural checks and suffix pass and `digitCount(CS) <= 3` returns
   `"Yes"`.

Formally, however, `charCount`, `headCode`, and `suffixIs` are total
uninterpreted functions, while `suffix4` is an opaque constructor. Therefore
these preconditions do **not** say “actual count/head/suffix” under the
submitted theory; they say “the corresponding opaque term has this value.”
That distinction is the central soundness failure in Stage 5.

### Satisfiable states and concrete substitution

Every claim has a concrete satisfying input under the intended observations:

| Claim | Witness | Expected/post value | Candidate | Canonical |
|---|---|---:|---:|---:|
| 1 | `""` | `No` | `No` | `No` |
| 2 | `.txt` | `No` | `No` | `No` |
| 3 | `1.txt` | `No` | `No` | `No` |
| 4 | `a.bin` | `No` | `No` | `No` |
| 5 | `a1234.txt` | `No` | `No` | `No` |
| 6 | `a123.txt` | `Yes` | `Yes` | `Yes` |

The exact code-point sequences, observation values, precondition evaluations,
and both Python results are in
[`claim_witnesses.py`](evidence/claim_witnesses.py) and
[`10-claim-witnesses.log`](evidence/10-claim-witnesses.log).

Each claim begins from a realizable initial configuration: module environment
0, the exact empty module scope with parent `-1`, the supplied builtin scope,
empty heap and stack, `noRet`, `NoExc`, and exit code 0.

### Program term and result constraint

The claim does not merely call an unconstrained result function.
`runFileNameCheck` constructs a closure and executes the body through the
ordinary supplied call/frame/return rules. The postcondition fixes the return
to the exact code sequence for `"No"` or `"Yes"` and fixes all observable
configuration cells.

To check source pinning mechanically, I extracted the balanced
`solutionModule` RHS, normalized five explicit `.Stmts` units to the trusted
translator’s omitted trailing-list syntax, and parsed both that term and
regenerated `solution.mpy` with `kast`. Their constructor JSON files are byte
identical, both with SHA-256
`d947d699dc382b5e3fa6c299b3a614331e776ead3b61e204e9e36f0a4f4008cb`.
See [`extract_solution_module.py`](evidence/extract_solution_module.py) and
[`09-program-term-pinning.log`](evidence/09-program-term-pinning.log).

A body-sensitivity mutation changed the actually executed final
`Return("Yes")` inside `solutionModule` to `Return("No")`. The mutated
definition built successfully, but the acceptance claim then exited nonzero
with a stuck final `"No"` configuration against the required `"Yes"`.
See [`body-mutated-verification.k`](evidence/body-mutated-verification.k),
[`16-body-mutation-build.log`](evidence/16-body-mutation-build.log), and
[`17-body-mutation-kprove.log`](evidence/17-body-mutation-kprove.log).

There are no helpers or loops and no auxiliary loop claims. Real-program
pinning and result constraint therefore pass; they do not cure the false
operational bridges.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[`rule_inventory.py`](evidence/rule_inventory.py) reconstructed an exhaustive
textual inventory from every `.k` file in the supplied semantics,
`verification.k`, and `spec.k`. The full 956-row inventory is
[`11-static-inventory.tsv`](evidence/11-static-inventory.tsv), with file,
line span, kind, attributes, disposition, rationale, and normalized statement.
The summary is
[`11-static-inventory-summary.log`](evidence/11-static-inventory-summary.log).

The rows comprise:

- 928 supplied-semantics configurations, syntax declarations, contexts, and
  rules;
- 22 proof-local declarations/rules in `verification.k`;
- six target claims.

Under `SUPPLIED_SEMANTICS`, the byte-verified reference tree is the selected
fixed language model. Every supplied row is marked as that fixed model rather
than incorrectly treating it as candidate-authored evidence. Its 22 explicit
`no-evaluators` boundaries concern float operations, sort, and MD5; none is
reachable from this submitted program. I nevertheless followed every material
used execution path through configuration, lookup, calls, frames, returns,
conditionals, evaluation order, integers, strings, count, indexing, and
slicing. The complete constructor-to-rule mapping is
[`12-used-construct-map.md`](evidence/12-used-construct-map.md).

The fixed used path has:

- left-to-right callee and argument evaluation;
- normal lexical lookup with an actual builtin scope;
- a real closure frame, parameter binding, return, frame pop, and cell
  restoration;
- pure fixed implementations of string count, first indexing, `[-4:]`
  slicing, and string equality;
- in-bounds first indexing because the source reaches it only after length at
  least five;
- no mutation, allocation, exception, output, or abrupt control in the
  operations displaced by the candidate bridges.

The proof-local inventory contains no simplification lemma or auxiliary
reachability claim. `latinCode`, `allowedSuffix`, and `digitCount` are truthful
compositions conditional on their operands. `solutionModule`, `moduleBody`,
and `runFileNameCheck` are acceptable exact pinning helpers for this immutable
ground program. The remaining ten items are four unjustified result-bearing
symbols and six unsound priority bridges.

### Unsound operational bridges and false-conclusion witnesses

The six bridges all match an arbitrary continuation via `<k> ... ... </k>` and
omit other cells. Because the displaced operations are pure, this broad frame
does not itself produce a state/control counterexample here. Binding is also
already resolved for count. The concrete defect is value fidelity: every
bridge returns a program-derived value that is neither defined nor connected
to fixed execution.

| Candidate rule | Fixed behavior displaced | Concrete/symbolic false conclusion witness |
|---|---|---|
| `/candidate/verification.k:19` | `applyMethod(...,"count",...)` and `cntSub` | Actual `a.txt`.count(".") is 1. The admitted ground interpretation `charCount(aTxt,46)=0` makes the extended program prove `"No"`. |
| `/candidate/verification.k:27` | `applyIndex`, `normIdx`, and `intSeqAt` | Actual first code of `b.txt` is 98. Keeping the dot observation correct but setting `headCode(bTxt)=49` makes the extended program prove `"No"`. |
| `/candidate/verification.k:34` | evaluation of `-4`, slice-bound normalization, `doSlice`, and `buildIS` | Actual `c.txt[-4:]` is `.txt`. An admitted observer for the opaque yielded term maps it to `.bin`; both the direct false slice result and whole-program `"No"` close. |
| `/candidate/verification.k:42` | `.txt` code-sequence equality | Actual `d.txt[-4:] == ".txt"` is true. Setting all `suffixIs(dTxt,*)` flags false makes the extended program prove `"No"`. |
| `/candidate/verification.k:48` | `.exe` code-sequence equality | Actual `e.exe[-4:] == ".exe"` is true. Setting the `.exe` flag false, with earlier observations correct, makes the extended program prove `"No"`. |
| `/candidate/verification.k:54` | `.dll` code-sequence equality | Actual `f.dll[-4:] == ".dll"` is true. Setting the `.dll` flag false, with earlier observations correct, makes the extended program prove `"No"`. |

The reviewer interpretation is preserved in
[`unsound-interpretation.k`](evidence/unsound-interpretation.k); its six claims
are generated from
[`unsound-interpretation-spec.k`](evidence/unsound-interpretation-spec.k).
The final fresh definition built successfully
([`13-unsound-witness-build-3.log`](evidence/13-unsound-witness-build-3.log)).
Each of the six isolated wrong-result claims printed `#Top` and exited zero in
`evidence/14-unsound-witness-{1..6}-v3.log`. The direct wrong slice claim also
printed `#Top`
([`14-unsound-slice-kprove-v3.log`](evidence/14-unsound-slice-kprove-v3.log)).

These added ground rules are deliberately false; their purpose is to exhibit
values the candidate left unconstrained. They do not purport to repair or
extend the trusted semantics. Their successful compilation and proof show
that the candidate supplied no universal equation preventing those opposite
interpretations.

Conversely, the actual submitted source and the fresh fixed LLVM semantics
both accept all six filenames. CPython assertions and `krun` both exited zero
in
[`15-false-conclusion-fixed-execution.log`](evidence/15-false-conclusion-fixed-execution.log).
Thus each claimed unsound bridge has the required false-conclusion witness on
the intended input domain.

The earlier exploratory witness encodings and their failures are retained in
the `13-*` and non-`v3` `14-*` logs. One attempted to mark a non-function
symbol as a simplification rule; another did not yet expose the opaque suffix
at a K observation point. Neither is used for the verdict. The final `v3`
artifacts build and close all six witnesses.

No bridge-free universal connection theorem exists for any of the six rules.
Finite concrete tests cannot supply that missing theorem. Rule priority only
ensures the opaque bridge preempts fixed semantics; it does not justify the
returned value.

**Static soundness result: FAIL.** This is a Gate A real-program soundness
failure, not a thin-evidence concern.

## 6. Fresh non-vacuity test

The candidate supplied no trusted non-vacuity evidence. I created a fresh
mutation
[`spec-vacuity-review.k`](evidence/spec-vacuity-review.k) that keeps the
acceptance precondition but changes its result obligation from `"Yes"` to
`"No"`. The intended observations for `a123.txt` satisfy that precondition,
and both Python implementations return `"Yes"` for it.

Command:

```text
kprove spec-vacuity-review.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY-REVIEW
```

The mutation parsed and executed, exited `1`, and produced the expected
`WarnStuckClaimState`: the final `<k>` held exact `"Yes"` while the destination
required `"No"`. It was not a parser error, timeout, missing import, or
unreachable mutation. Full bounded output is in
[`18-nonvacuity-kprove.log`](evidence/18-nonvacuity-kprove.log).

**Non-vacuity result: PASS.** The theorem is result-discriminating within the
unsound extended theory. Passing this test does not establish that the
observations denote real string operations.

## 7. Proven versus assumed accounting

### What the successful reachability proof actually establishes

Under the candidate’s extended semantics, for any `CS` whose *opaque*
`charCount`, `headCode`, and `suffixIs` observations satisfy one of the six
preconditions, executing the exact submitted function body returns the
corresponding exact `"No"` or `"Yes"` value and restores the claimed cells.
It also establishes that the ordinary control-flow code correctly propagates
those observation values through comparisons, Boolean short-circuiting,
addition, conditionals, and returns.

It does **not** establish that:

- `charCount(CS,C)` equals the fixed semantics’ `cntSub` result;
- `headCode(CS)` equals fixed first-element indexing;
- `suffix4(CS)` equals fixed `CS[-4:]`; or
- `suffixIs(CS,i)` equals the fixed equality test for the corresponding
  extension.

Those missing facts are exactly the facts needed to turn the conditional
opaque theorem into the HumanEval property.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K `v7.1.293` and its reachability backend | All dynamic results | Ordinary machine-checking trust boundary; versions recorded. |
| Byte-verified supplied semantics | All concrete and proof execution | Authorized fixed semantics for this condition. Its unused float/sort/MD5 opaque primitives do not affect this theorem. |
| Trusted translator plus constructor-level `kast` comparison | Source-to-`.mpy` and embedded-body pinning | Acceptable and independently reproduced. |
| `charCount` | Dot branch and all ten digit counts | Illegitimate program-derived oracle; result-bearing, unaxiomatized, and contradicted by W1. |
| `headCode` | ASCII-first-character branch | Illegitimate program-derived oracle; unaxiomatized and contradicted by W2. |
| `suffix4` | Value stored in `suffix` | Illegitimate program-derived opaque value; no connection to fixed slicing and contradicted by W3. |
| `suffixIs` | All suffix branches and `allowedSuffix` claim preconditions | Illegitimate program-derived oracle; unaxiomatized and contradicted by W4–W6. |
| `latinCode`, `allowedSuffix`, `digitCount` definitions | Claim partition and control flow | Ordinary truthful compositions, but `allowedSuffix` and `digitCount` inherit the illegitimate observations. |
| Differential and concrete tests | Implementation/contract and finite fixed-execution evidence | Reproducible finite evidence only; not a universal bridge theorem. |

### Decision

- Clean reconstruction: pass.
- Real-program constructor pinning: pass.
- Exact result constraint and fresh non-vacuity: pass.
- Gate A proof-extension soundness: **fail**.
- Source-contract implementation evidence: favorable but finite.
- Evidence auditability: pass.

Because materially unsound operational rules replace result-bearing
computations and make false conclusions provable for valid filenames, the
candidate meets the benchmark’s `FAIL / NOT_LEGIT` boundary. This is not a
`CONCERNS` case: the missing universal connections are the correctness
argument itself.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
