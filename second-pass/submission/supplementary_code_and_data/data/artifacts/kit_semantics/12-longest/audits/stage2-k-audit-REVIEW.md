# Independent adversarial audit: HumanEval 12 `longest`

The candidate contains a legitimate partial-correctness proof of the submitted
program over the full material HumanEval domain, arbitrary finite
`List[str]`. I reconstructed the proof from immutable source artifacts, did not
reuse candidate kompiled definitions, and treated all candidate prose and
generation history as untrusted.

## 1. Input and provenance integrity

The declared record layout is `pipeline-v3`, the condition is
`kit-semantics`, and the rendered mode is `SUPPLIED_SEMANTICS`. The trusted
`/reference/reference-semantics` tree is present, as this mode requires.

I read `/audit-input.json`, its `record_layout`, `container_paths`, recorded
hashes, integrity fields, and campaign block. I also read
`/audit-campaign-lock.json`, `/run.json`, `/task.json`,
`/generation-result.json`, every required pipeline-v3 generation record, the
full text log, and every structured trace event. The generation records were
used only to check provenance, never to establish proof correctness.

Independent checks found:

- The campaign lock is a real regular file, has SHA-256
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  and is JSON-identical to the `audit_campaign` block.
- All required pipeline-v3 records and declared mounts are present and real
  files/directories. No symlink or unsupported filesystem entry occurs in the
  candidate, trusted semantics, or generation evidence trees.
- Fifteen directly recorded file hashes independently match, including the
  run manifest, task manifest, result, invocation, prompt, canonical program,
  translator, metrics, usage, output, and last-message records.
- The candidate tree's independently recomputed pipeline digest is
  `616879fa4fac0e0efd8499dbe2f4ff825c06468cdf0ed0d58cccf91ae600c27c`,
  matching both invocation and result records.
- The structured trace pipeline digest is
  `7a5576044ebbef1e25c0168e8c55f785903feb1794aa3baef9b94186b8798dfd`,
  matching `usage.json`; its sole JSONL file also matches the invocation's
  recorded file hash.
- The candidate and trusted semantics trees both have pipeline digest
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`,
  matching the task manifest. A recursive `diff --no-dereference` is empty, so
  there are no missing, additional, changed, mistyped, or linked entries.
- Candidate/trusted prompt bytes match at SHA-256
  `aa62f2bdcae005c83ed5eede68f25a798ece3609af2bf7db30ef714aa7a33927`.
  Candidate/trusted translator bytes match at SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.
- The result and invocation records agree on session, status, and outputs.
  The full 50,360-line text log and all 580 structured trace events parsed
  successfully. Their reports of `#Top` remain untrusted historical claims.

Evidence:
[provenance verification](/audit-output/evidence/stage1-provenance-verification.log),
[file hashes](/audit-output/evidence/stage1-file-hashes.log),
[tree hashes](/audit-output/evidence/stage1-tree-hashes.log),
[recursive comparisons](/audit-output/evidence/stage1-integrity-comparisons.log),
[entry types](/audit-output/evidence/stage1-entry-types.log), and
[generation-record inspection](/audit-output/evidence/stage1-generation-record-inspection.log).

There is no infrastructure breach, so a candidate verdict is appropriate.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

From the trusted [prompt](/reference/prompt.py:4) and
[canonical implementation](/reference/canonical.py:8): for any finite list of
Python strings, return `None` when the list is empty; otherwise return the
first string having maximum length. Equal-length later elements must not
replace the first maximizer.

The submitted [solution](/candidate/solution.py:4) handles empty input first,
initializes `result` to the first element, then scans the entire list and
updates only on strict greater-than length. Scanning the first element again is
inert because its length equals the accumulator's length. This is a different
implementation from the canonical `max`-then-first-selection code, but it has
the same behavior on the intended domain.

### Trusted translation

I regenerated `solution.mpy` from `solution.py` with
`/reference/py2mpy.py`. The regenerated and submitted files are byte-identical,
both with SHA-256
`610aeaa25e6c44a3bb1da9943b066d5e6792db60613d9b7035b97af64a32dae9`.
See [translation identity](/audit-output/evidence/stage2-translation-identity.log).

### Independent differential test

The reviewer-authored
[differential script](/audit-output/evidence/independent_differential.py)
loads the trusted canonical and candidate entry points from their absolute
paths. It covers the documented examples, empty and singleton inputs,
greater/equal/less update boundaries, first/middle/last maxima, long strings,
NUL/control characters, combining characters, emoji and non-Latin strings,
all products of a seven-string pool through length five, and 5,000 seeded
lists of up to 30 generated strings. It also checks that neither
implementation mutates its input.

Result: 24,624 comparisons, zero mismatches, exit 0. See
[differential log](/audit-output/evidence/stage2-independent-differential.log).
This is finite evidence of the Python bridge, not a substitute for the K
theorem.

## 3. Clean proof reconstruction

I copied only source artifacts to `/tmp/audit-work`; no candidate
`*-kompiled` directory, `__pycache__`, or cache file was copied. The fresh
toolchain was K 7.1.293 for `kompile`, `krun`, and `kprove`, with Python
3.10.12. See [toolchain log](/audit-output/evidence/stage3-toolchain.log).

### Concrete definition

Fresh command:

```text
kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition audit-runtime-kompiled
```

It exited 0. The warnings concern supplied-semantics declarations, not build
failure. A reviewer-authored, trusted-translated concrete suite then executed
empty, singleton-empty-string, tie, increasing-length, first-tie, and late-max
cases. `krun` ended with `<k> .K </k>`, `<exc> NoExc </exc>`,
`<exit-code> 0 </exit-code>`, and process exit 0. Evidence:
[runtime build](/audit-output/evidence/stage3-kompile-runtime.log),
[concrete source](/audit-output/evidence/audit-smoke.py),
[translated concrete program](/audit-output/evidence/audit-smoke.mpy), and
[concrete run](/audit-output/evidence/stage3-concrete-runtime.log).

### Bridge-free and target definitions

Fresh commands:

```text
kompile --backend haskell verification.k --main-module VERIFICATION-BASE --syntax-module MPY-SYNTAX --output-definition audit-connection-kompiled
kompile --backend haskell verification.k --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition audit-verification-kompiled
```

Both exited 0. Evidence:
[base build](/audit-output/evidence/stage3-kompile-connection.log) and
[target build](/audit-output/evidence/stage3-kompile-verification.log).

### Positive claims

Every positive claim was independently run against a fresh definition:

| Claim | Fresh result | Evidence |
|---|---|---|
| `CONNECTION-SPEC.string-length-connection` | `#Top`, exit 0 | [log](/audit-output/evidence/stage3-prove-connection-length.log) |
| `CONNECTION-SPEC.string-projection-connection` | `#Top`, exit 0 | [log](/audit-output/evidence/stage3-prove-connection-projection.log) |
| `SPEC.loop-invariant` | `#Top`, exit 0 | [log](/audit-output/evidence/stage3-prove-loop.log) |
| `SPEC.empty-input` | `#Top`, exit 0 | [log](/audit-output/evidence/stage3-prove-empty.log) |
| `SPEC.nonempty-input` with its loop circularity | `#Top`, exit 0 | [log](/audit-output/evidence/stage3-prove-nonempty-with-loop.log) |
| Whole `SPEC` module | `#Top`, exit 0 | [log](/audit-output/evidence/stage3-prove-all-target.log) |

The connection claims emit `WarnTrivialClaim`: each pair of sides independently
normalizes to the same constructor term. That is benign definitional equality,
not a proof failure.

## 4. Adequacy and real-program pinning

### Claims in plain language

- `SPEC.loop-invariant`: with a local call frame whose `strings`, `result`, and
  `string` bindings are fixed, builtin `len` unshadowed, a string accumulator,
  a string current value, and an arbitrary all-string remaining `ValSeq`,
  executing the exact source loop replaces `result = ACC` with
  `result = scanLongest(REST, ACC)`. It existentially permits `string` to
  become the last iterated value and frames all other state.
- `SPEC.empty-input`: from exact initial cells, loading the submitted module
  and calling its `longest` binding on `list(.ValSeq)` terminates the call with
  `noneV`.
- `SPEC.nonempty-input`: from exact initial cells, loading that same module and
  calling `longest` on `list(vCons(FIRST,REST))`, where the head and every tail
  value are strings, terminates the call with
  `longestValue(vCons(FIRST,REST))`.

`longestValue` is not free or oracle-valued on intended inputs. Empty maps to
`noneV`; nonempty maps to a structurally recursive strict-length fold seeded
with the first element. Induction over the processed prefix shows that the
accumulator is the first element of maximum length: a larger value replaces
it, while equality retains it.

### Mechanical program identity

The reviewer script extracts the two `Module(...)` terms inside the entry
claims, removes layout and only the explicit `.Stmts` list identity, and
compares constructor tokens with trusted-regenerated `solution.mpy`. All three
normalized terms have digest
`d71f4c3e4836304490048ee4a8274fe43339b0fc3beaf5b8a12b5dfc7bccbc2a`.
Both entry continuations call the binding name `longest`. Evidence:
[pinning script](/audit-output/evidence/check_program_pinning.py) and
[pinning log](/audit-output/evidence/stage4-program-pinning.log).

The claim term therefore executes the exact submitted binding and body.
Typing-only import handling is the only normalization. The absence of an
automatic source-to-spec generator is a maintenance observation, not a defect
in this immutable candidate, because the constructor comparison is exact.

### Satisfying states and concrete substitutions

Concrete witnesses exist for every precondition:

- Empty entry: the exact initial cells and input `[]`; postcondition `None`.
- Nonempty entry: `FIRST = "a"`, `REST = ["bb","c"]`; both string predicates
  are true and `longestValue` is `"bb"`.
- Loop: `L = 1`, `MODULE = .Map`, `ACC = CURRENT = "a"`,
  `REST = ["bb","c"]`, with the three required scope locations distinct;
  `scanLongest` is `"bb"`.

The trusted canonical and candidate Python functions agree on the entry
substitutions. Four ground K adequacy claims for guards, empty result,
nonempty result, and loop result print `#Top`, exit 0. Evidence:
[Python witnesses](/audit-output/evidence/stage4-ground-python.log),
[K witness spec](/audit-output/evidence/audit-ground-adequacy.k), and
[K witness log](/audit-output/evidence/stage4-ground-k.log).

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The reviewer-authored inventory script scanned every source file under the
trusted semantics tree plus `verification.k`, `spec.k`, and
`connection-spec.k`. The resulting
[TSV inventory](/audit-output/evidence/static-rule-inventory.tsv) has one
decision-bearing record for each local declaration/rule:

- 955 total records;
- 233 syntax declarations;
- 711 rules;
- five contexts;
- five claims;
- one configuration;
- 113 `[total]`, 151 `[function]`, 24 `[no-evaluators]`, 45 priority,
  36 concrete, and seven simplification-bearing records.

The [summary](/audit-output/evidence/static-rule-inventory-summary.txt) gives
per-file and per-decision counts. Records on the submitted execution path are
marked materially reviewed/sound. Unexercised fixed-semantics records,
including float, sort, keyed-sort, and MD5 opaque boundaries, are explicitly
marked unexercised; no intended-input witness connects them to this theorem, so
I do not assert unsoundness merely from incomplete global coverage.

The
[construct map](/audit-output/evidence/solution-construct-map.md) maps every
constructor in `solution.mpy` to its declaration, strictness/context, and
material semantic rules. It covers configuration and cells, module/function
binding, lookup, left-to-right call and argument evaluation, assignments,
truthiness, conditional control, list indexing, list iteration, target
binding, builtin `len`, integer comparison, return, frame pop, scopes, heap,
exceptions, and exit status.

### Used fixed semantics

On the actual path:

- the typing import is semantically inert;
- `FuncDef` binds the exact body in module scope;
- closure dispatch creates one fresh local scope and binds the exact argument;
- empty list truthiness selects the return branch before indexing;
- nonempty indexing is exactly at normalized index zero;
- list iteration consumes one `vCons` per step;
- each loop step binds the actual source target, looks up builtin `len`,
  evaluates the two length calls left-to-right, performs integer `>`, and
  executes the actual assignment or empty branch;
- `Return` discards only the current function continuation as Python return
  requires, then restores the caller and preserves observable cells.

The proof path performs no output, heap allocation, exception, or exit-status
change. Rule priorities only select more specific cell/ref behavior; the
claims' bare list/string values and plain frame make those alternatives
inapplicable.

### Proof-local extensions

The full
[proof-extension static review](/audit-output/evidence/proof-extension-static-review.md)
records domain, overlap, coverage, descent, context, state footprint, value
influence, and justification for every extension. In summary:

| Extension | Class | Decision |
|---|---|---|
| `isStringValue`, `allStrings` | structural definitional summaries | complete, disjoint, sound |
| `projectString` and cast/ceil rules | guarded sort-refinement summary/lemmas | identity on every intended `Str`; sound |
| `seqLenString` | definitional static-sort twin | exactly `isLen(CS)` on every intended `str(CS)` |
| `scanLongest`, `longestValue` | structural result summaries | terminating equations; exact first-maximum fold |
| guarded `seqLen(V)` rule | pure operational bridge | fixed/bridge results identical on complete intended domain |
| loop invariant | derived circularity | exact loop/control/local-state footprint; sound |
| entry claims | target claims | exact program, complete domain, constrained results |
| connection claims | bridge-free supporting claims | universal over arbitrary `CS:IntSeq`; sound |

`projectString` and `seqLenString` are syntactically total and opaque outside
their equations, but intended source strings are all canonical `str(CS)`
values, where both reduce uniquely. Synthetic proof-only terms outside that
source domain cannot alter a conclusion about real list-of-string inputs.
There is no task-answer oracle.

The only operational bridge rewrites pure `seqLen(V)` when
`isStringValue(V)`. For every actual match, `V = str(CS)`: fixed semantics
returns `isLen(CS)`, and the bridge normalizes to that same value. It reads or
writes no cells and preserves arbitrary continuation context.

Fresh validation supports that analysis:

- bridge-free fixed and twin lengths for one- and two-code strings both close
  with `#Top`, exit 0
  ([spec](/audit-output/evidence/audit-fixed-length-witness.k),
  [log](/audit-output/evidence/stage5-fixed-length-witness.log));
- a distinct continuation after the bridged operation is preserved
  ([spec](/audit-output/evidence/audit-bridge-continuation.k),
  [log](/audit-output/evidence/stage5-bridge-continuation.log));
- the opposite interpretation “one-code string has length zero” is rejected
  with residual `1`, `WarnStuckClaimState`, exit 1
  ([spec](/audit-output/evidence/audit-opposite-length.k),
  [log](/audit-output/evidence/stage5-opposite-length.log));
- changing the comparison inside the program term actually executed by the
  claim from `>` to `<` is rejected on `["a","bb"]`, with residual `"a"`
  rather than `"bb"`, exit 1
  ([spec](/audit-output/evidence/audit-body-sensitivity.k),
  [log](/audit-output/evidence/stage5-body-sensitivity.log)).

I found no materially unsound candidate rule and therefore assert no
unsoundness without the required false-conclusion witness.

## 6. Fresh non-vacuity test

I inspected candidate mutation files only as untrusted evidence, then authored
a separate mutation. It executes the exact original submitted body on the
satisfying input `["x","yyyy","zz"]` but changes the final destination from
the true first-longest result `"yyyy"` to the false result `"zz"`.

The preserved mutation is
[fresh-false-result.k](/audit-output/evidence/fresh-false-result.k).

First, `kprove ... --dry-run` parsed and built the mutation, exiting 0. This
rules out a parser/import/build failure. See
[dry-run log](/audit-output/evidence/stage6-fresh-mutation-dry-run.log).

The actual proof then exited 1 with `WarnStuckClaimState`. Its residual `<k>`
value is exactly `str(121,121,121,121)` (`"yyyy"`), which cannot unify with
the deliberately false `"zz"` destination. See
[proof log](/audit-output/evidence/stage6-fresh-mutation-proof.log).

This is a reachable, result-bearing failure for a satisfying input. The proof
is non-vacuous and discriminates the intended return value.

## 7. Proven versus assumed accounting

### Precisely proven

Under the supplied MPY semantics and audited proof extensions, the fresh
reachability proofs establish:

- loading the actual submitted module and calling its actual `longest` body on
  the empty list reaches return value `noneV`;
- for every arbitrary finite `ValSeq` whose elements are strings, the same
  execution reaches `longestValue` of that sequence;
- the source loop is summarized for an arbitrary symbolic tail, not a fixed
  size or bounded unrolling;
- the summary is a strict-update fold seeded with the first element and
  therefore denotes the first maximum-length string.

This is partial correctness: the theorem says what every terminating execution
returns. K reachability does not separately prove total correctness.

### Trust ledger

| Boundary | Dependents | Status and justification |
|---|---|---|
| Supplied immutable MPY semantics | all concrete/proof execution | Accepted benchmark trust boundary; recursively identical to trusted mount and statically audited for every used construct |
| K 7.1.293 parser/compiler, LLVM/Haskell backends, built-in integer/map/list theories and solver | every `kompile`, `krun`, `kprove` result | Accepted proof infrastructure; fresh builds avoid candidate cache trust |
| Trusted CPython-AST translator | program-to-constructor identity | Accepted trusted input; exact byte regeneration and constructor pinning verified |
| `projectString`/`seqLenString` on intended strings | symbolic string-length comparisons | Not left assumed: equations and bridge-free universal constructor claims fix their values to `isLen(CS)` |
| Proof-local synthetic projection terms outside source values | no intended source execution | Opaque but irrelevant; target source strings are canonical `str(CS)` |
| IntSeq string model versus Python `str` | human-facing contract interpretation | Structural length counts sequence elements, matching Python code-point length; Unicode Python differential cases provide finite supporting evidence |
| Termination | total correctness only | Not formally claimed. Informally, the finite source loop consumes one tail constructor per iteration; partial correctness is the required theorem |
| Canonical/candidate Python differential test | implementation/intent and Unicode bridge | Empirical only: 24,624 zero-mismatch cases; not used as a universal proof |
| Concrete LLVM suite | exercised semantics sanity | Empirical only; not substituted for symbolic reachability |

There is no proof-local trusted primitive that supplies the task answer, no
free result variable, no materially narrowed input domain, and no finite-size
restriction. All unbounded-domain reasoning comes from the arbitrary
`ValSeq` circularity and structural summary equations.

### Gate and decision accounting

- Gate A, real-program soundness: PASS. Exact program identity, full state and
  control execution, sound bridge, value/continuation witnesses, body
  sensitivity, and false-result rejection all hold.
- Gate B, intent adequacy: PASS. Empty plus symbolic nonempty claims cover all
  arbitrary finite `List[str]`, and the defined summary is the requested first
  longest value.
- Gate C, trust and auditability: PASS. Fresh commands, actual outputs,
  reviewer scripts/specs, complete inventory, mutations, and finite evidence
  are preserved under `/audit-output/evidence`.

The proof is result-constraining, sound under the supplied semantics, and pins
the real generated program with no material adequacy gap.

VERDICT: PASS
LEGITIMACY: LEGIT
