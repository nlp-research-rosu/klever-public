# Independent adversarial review: HumanEval 12 `longest`

## Executive finding

The candidate contains a legitimate, result-constraining partial-correctness
proof of the submitted program, but it has one material auditability
limitation. The universal claims use an unbounded proof-only sequence
representation, `seqVal(ID,I,N)`, whereas concrete execution uses
`listVal(Values)`. The sequence rules are transparent, preserve the loop’s
control and state effects, and range over arbitrary lengths and arbitrary K
strings; they do not encode the answer. Thus this is not a finite-size or
material source-domain restriction. However, the candidate does not provide a
bridge-free universal K theorem connecting the two representations.

That gap prevents `PASS`, but it does not justify `FAIL`: for every finite
Python `list[str]`, `N` can be its length and the opaque total `stringAt`
function can supply its elements, and the proof executes the real loop body
once per element. Two distinct ground interpretations were also checked
against the fixed `listVal` semantics. This is an informal representation
bridge of the kind allowed by the benchmark’s `CONCERNS / LEGIT` category, not
a bounded HumanEval-domain narrowing.

## 1. Input and provenance integrity

The launcher record declares:

- problem `12-longest`;
- condition `bare`;
- `record_layout` `legacy-selected-stage1`;
- `semantics_mode` `GENERATED_SEMANTICS`.

I independently inspected `/audit-input.json` before using candidate evidence.
The mounted `/audit-campaign-lock.json` is structurally identical to the
campaign block in `/audit-input.json`, and its SHA-256 is the recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
The independently computed hashes of `/run.json`, `/task.json`,
`/generation-result.json`, the invocation and metrics records, usage record,
prompt record, `codex-last.txt`, `codex-output.log`, and all three trusted
reference files match their launcher-declared values. See
[`stage1-provenance.log`](evidence/stage1-provenance.log).

The required legacy-selected records are present, readable regular files.
Historical runtime metrics are absent, which is permitted for this legacy
layout. The sole structured trace file has SHA-256
`c231436b55c6a7c394de156c57f4d4f7531f9fe66fc0ea4b33c109fa4338ebd2`,
matching the per-file generation manifest. I parsed all 405 JSONL events; the
trace has no malformed event or recorded error. The bounded structural
inspection, including all 79 custom tool calls and outputs, is in
[`stage1-trace-inspection.log`](evidence/stage1-trace-inspection.log).
The separately hashed 1,396,514-byte text log and its relevant proof history
are recorded in
[`stage1-generation-output-inspection.log`](evidence/stage1-generation-output-inspection.log).
These records were treated only as untrusted historical claims.

The candidate mount has no symlinked entries. All required proof artifacts are
present as regular files: `solution.py`, `solution.mpy`, `semantic.k`,
`verification.k`, `spec.k`, and `prove.sh`. The provenance script records the
SHA-256, mode, and size of every candidate entry and an independently encoded
tree manifest. Candidate `prompt.py` and `py2mpy.py` are byte-identical to
their trusted mounted versions.

The generated-semantics boundary is internally consistent:
`/reference/reference-semantics` does not exist and is not a symlink. I did not
seek or use a hidden reference semantics. There is no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

For a finite `List[str]`, return:

1. `None` if the list is empty;
2. otherwise, a string of maximum Python length;
3. on equal maximum lengths, the first such string.

The trusted canonical implementation computes the maximum length and returns
the first element with that length. The candidate initializes `result` from
the first element, scans in order, and replaces it only on a strict length
increase. These algorithms are extensionally equivalent on the full stated
domain.

### Translation identity

I regenerated the MPY term from the copied `solution.py` using the trusted
`/reference/py2mpy.py`. `cmp` exited 0; both submitted and regenerated files
have SHA-256
`17a16c7a8e00f962ce09491dd097b415eb98b18d7e92302eedd9dc792bbb0b16`.
The exact command and result are in
[`stage2-translation.log`](evidence/stage2-translation.log).

### Independent differential testing

[`differential_test.py`](evidence/differential_test.py) imports the trusted
canonical function and candidate function independently. It checks:

- all three documented examples;
- empty and singleton boundaries;
- strict-growth true, shorter false, and equal-length false branches;
- late maxima and late ties;
- empty strings, combining Unicode, emoji, embedded NUL, newline, and tab;
- all lists of lengths 0 through 4 over a nine-string pool (7,381 cases);
- 2,500 seeded generated lists with lengths through 24 and strings through 30
  generated code points.

All 9,893 cases matched. The command, named inputs, exit 0, and mismatch count
zero are in
[`stage2-differential.log`](evidence/stage2-differential.log). These finite
tests support implementation fidelity; they are not substituted for the K
proof.

## 3. Clean proof reconstruction

All candidate-built definitions and caches were excluded. Source artifacts
were copied to `/tmp/audit-work/12-longest/run`, and both definitions were
built afresh with K 7.1.293.

### Fixed generated semantics

The command

```text
kompile semantic.k --backend haskell --main-module MPY-SEMANTICS --syntax-module MPY-SYNTAX --output-definition semantic-kompiled
```

exited 0; see
[`stage3-semantic-build.log`](evidence/stage3-semantic-build.log).
Using this definition, which does not import `verification.k`, I ran the
translated `solution.mpy` on:

- the empty list;
- one empty string;
- strict length growth;
- a shorter later string;
- a later equal-length tie.

Every `krun` exited 0 and produced `#Top` against the independently computed
Python result. These five exact commands and results are in
[`stage3-concrete-semantics.log`](evidence/stage3-concrete-semantics.log).
Together they exercise imports, function storage/invocation, empty and
nonempty guards, indexing, assignment, both comparison outcomes, zero and
positive loop iterations, and return unwinding.

### Proof definition and positive claims

The fresh proof build

```text
kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-kompiled
```

exited 0; see
[`stage3-proof-build.log`](evidence/stage3-proof-build.log).

Each of the seven positive targets was then selected independently by its
fully qualified label. The nonempty entry target was selected together with
only its required `longest-loop` circularity. Every command exited 0 and
printed one aggregate `#Top`:

| Target | Exit | Result |
|---|---:|---|
| `SPEC.longest-loop` | 0 | `#Top` |
| `SPEC.longest-empty` | 0 | `#Top` |
| `SPEC.longest-nonempty` with `SPEC.longest-loop` | 0 | `#Top` |
| `SPEC.concrete-empty` | 0 | `#Top` |
| `SPEC.concrete-first-tie` | 0 | `#Top` |
| `SPEC.concrete-increasing` | 0 | `#Top` |
| `SPEC.concrete-late-tie` | 0 | `#Top` |

The summary is
[`stage3-positive-claims-summary.log`](evidence/stage3-positive-claims-summary.log);
the individual command/output logs are under
[`evidence/proof`](evidence/proof/).

The evidence directory also retains two reviewer diagnostics. An unqualified
filter label was rejected with exit 113, and selecting the nonempty entry
claim while removing its circularity was interrupted after it unrolled for
3m31s. Neither is a candidate proof failure; the successful qualified commands
above use the claim dependency present in the submitted spec.

## 4. Adequacy and real-program pinning

### Constructor-level program identity

The entry claims execute the macro `longestProgram`. I parsed both the
regenerated `solution.mpy` and `longestProgram` with `kast
--expand-macros --output kore`. `cmp` exited 0; both expanded constructor terms
have SHA-256
`9852f2fc207637091522a41a52f53a4507a745deaa97b667e7e473ed26e8f9f4`.
This is a mechanical constructor-level identity check, not a visual
similarity judgment. See
[`stage4-program-term-identity.log`](evidence/stage4-program-term-identity.log).
The typing-only import is present in both terms.

### Plain-language claim meanings

- `longest-loop`: from an environment whose current result is `BEST`, iterate
  `N >= 0` symbolic strings starting at `(ID,I)`, execute the actual loop body,
  then execute the submitted return and function end. The output must be the
  transparent fold `firstInSeq(BEST,ID,I,N)`.
- `longest-empty`: on `seqVal(ID,0,0)`, the actual program must return
  `noneVal`.
- `longest-nonempty`: for every `N > 0`, on `seqVal(ID,0,N)`, the actual
  program must return the first-longest fold of those `N` symbolic strings.
  The initial head is included again in the source `for` loop; the fold
  likewise starts at index zero. Strict `>` makes that duplicate comparison
  idempotent.
- The four concrete claims execute the same program on an empty `listVal` and
  the three stated ground lists, constraining the output respectively to
  `None`, `"a"`, `"ccc"`, and `"aa"`.

The entry configurations are satisfiable. For the empty entry, the ground
state `seqVal("case",0,0)` executes to `noneVal`. For the nonempty entry,
[`seqval-ground-interpretations.k`](evidence/seqval-ground-interpretations.k)
sets indices 0, 1, and 2 to `"a"`, `"bb"`, and `"ccc"`; the state
`seqVal("case",0,3)` executes the exact entry term and returns `"ccc"`.
The build and run are recorded in
[`stage4-seqval-witness-build.log`](evidence/stage4-seqval-witness-build.log),
[`stage4-seqval-empty-witness.log`](evidence/stage4-seqval-empty-witness.log),
and
[`stage4-seqval-witness-run.log`](evidence/stage4-seqval-witness-run.log).
Both Python implementations return the same values for `[]` and
`["a","bb","ccc"]` in the differential record.

A satisfying loop state is obtained with `ID = "case"`, `I = 1`, `N = 2`,
`BEST = "aa"`, any old loop-variable value, and a remainder map containing
the parameter binding. Its claimed fold yields `"ccc"` under the recorded
interpretation. Each concrete claim’s literal input is itself a satisfying
precondition, and its substituted result agrees with both Python
implementations.

Every entry postcondition rewrites `<out>` to a specific value or to the
fully defined `firstInSeq` fold. The existential final environment and
function cell do not weaken the observable return result.

### Body sensitivity

I made a scratch mutation to the program term actually executed by the
claims: the macro’s loop body no longer assigns a newly longer string. The
mutant definition built successfully, but the increasing-case proof exited 1
with `WarnStuckClaimState`; the residual output is `"a"` while the required
output is `"ccc"`. See
[`body-sensitivity-verification.k`](evidence/body-sensitivity-verification.k),
[`stage4-body-sensitivity-build.log`](evidence/stage4-body-sensitivity-build.log),
and
[`stage4-body-sensitivity-proof.log`](evidence/stage4-body-sensitivity-proof.log).
This demonstrates dependence on the submitted body rather than merely on an
external source filename.

### Representation adequacy

The universal claims do not use the candidate’s declared
`stringList(Strings) => listVal(stringValues(Strings))`; nor do they use
`expectedLongest`. Instead they use `seqVal`. The concrete `listVal` claims
alone are only examples and would not prove the unrestricted contract.

The universal `seqVal` theorem, however, is not bounded: `N` ranges over all
nonnegative integers and `stringAt(ID,I)` has sort `String` with arbitrary
contents. The operational rule consumes one element, executes the real loop
body, increments the index, and decrements the remaining length. Therefore
every finite `list[str]` has an extensional sequence representation. This is
why the finding is not `SOUND-BUT-LIMITED` and not the benchmark-mandated
`FAIL` for domain narrowing.

The missing artifact is a universal, bridge-free K theorem that fixed
`listVal` execution and `seqVal` execution agree. This is the principal
reason for `CONCERNS`.

## 5. Rule-by-rule static soundness review

[`RULE-INVENTORY.md`](evidence/RULE-INVENTORY.md) is the exhaustive inventory.
It enumerates:

- every local syntax production and configuration cell;
- all 40 rules in `semantic.k`;
- every proof-local macro, function, `[total]`/opaque declaration, operational
  rule, and fold rule in `verification.k`;
- all seven claims;
- the rule mapping for every construct used by `solution.mpy`.

There are no local priority rules and no explicit `[functional]`
declarations. The only simplification rules are the two guarded Map-update
lookup equations. `stringAt` is the sole opaque `[function,total]` symbol.

### Generated semantics

For the exact submitted program:

- statement sequencing is ordered;
- the typing import is inert;
- the sole function body and argument binding are preserved;
- RHS expressions are evaluated in the old environment before assignment;
- list iteration binds and processes elements left-to-right;
- return discards remaining statement/loop continuations and writes `<out>`;
- the empty check, head, string/list lengths, integer comparison, and Map
  lookup equations agree on their overlaps;
- empty-list indexing and unsupported values remain visibly stuck rather than
  fabricating results.

The model is deliberately specialized. It ignores general import effects,
stores only one function, preallocates the two known locals, and has no Python
exception machinery. These choices are sound on the exact target control
paths and intended `List[str]` domain; missing semantics for unused Python
constructs is permitted in `GENERATED_SEMANTICS` mode.

### Proof-local extensions

The two macros are exact by the KORE identity check. `stringList`,
`stringValues`, `expectedLongest`, and `firstLongest` are truthful,
terminating equations, although the universal claims do not use them.

`firstInSeq` has three guarded cases: zero remaining elements, a strictly
longer next element, and a shorter/equal next element. The guards are
disjoint and exhaustive for `N >= 0`, and recursive cases decrease `N`.
It is not used in operational execution, only in the result obligation, so it
does not bypass the program.

`stringAt` is result-bearing, but it denotes external input contents rather
than a computed answer. The theorem remains parametric in it. In one ground
interpretation the sequence `["a","bb","ccc"]` returns `"ccc"`; in a distinct
interpretation `["zzzz","b","ccc"]` returns `"zzzz"`. The corresponding
fixed-`listVal` executions produce the same two different outcomes. See
[`stage5-seqval-opposite-run.log`](evidence/stage5-seqval-opposite-run.log) and
[`stage5-listval-opposite-run.log`](evidence/stage5-listval-opposite-run.log).
This value sensitivity refutes the hypothesis that `stringAt` is a fixed
answer oracle.

The five `seqVal` operational cases are disjoint from concrete `listVal`
rules. On their stated `N == 0` or `N > 0` domains, they faithfully implement
empty testing, head, and ordered iteration and preserve the same environment
and continuation footprint. They do not introduce return, skip the real loop
body, or constrain elements to a desired answer.

I found no local rule that enables a concrete false conclusion on the
intended domain, so I make no unsound-rule allegation requiring a false
conclusion witness. The narrower evidence gap is the absent universal
`listVal`/`seqVal` connection theorem; the recorded ground comparisons do not
replace it.

## 6. Fresh non-vacuity test

I created a new spec module that changes the result-constraining
`concrete-increasing` postcondition from `"ccc"` to `"bb"` while retaining the
satisfiable input `["a","bb","ccc"]`. The mutation is
[`mutation/spec-vacuity-audit.k`](evidence/mutation/spec-vacuity-audit.k).

The dry-run build exited 0, proving the mutation parses and compiles; see
[`mutation/build.log`](evidence/mutation/build.log). The actual proof exited 1
with `WarnStuckClaimState`. Its residual configuration has
`"result" |-> strVal("ccc")` and `<out> strVal("ccc")`, so failure is caused
by the expected unmet result obligation, not a parser error, missing import,
timeout, or unreachable mutation. See
[`mutation/proof.log`](evidence/mutation/proof.log).

The proof is non-vacuous and discriminates a false return value.

## 7. Proven versus assumed accounting

### Precisely proven

Under the rebuilt K theory:

- the exact constructor term regenerated from `solution.py` returns `noneVal`
  on the empty symbolic sequence;
- for every `N > 0`, every identifier, and every total interpretation of
  `stringAt`, the exact program returns
  `firstInSeq(stringAt(ID,0),ID,0,N)`;
- the loop circularity establishes the corresponding fold for every
  `N >= 0`;
- the four ground `listVal` executions have their claimed results.

The reachability theorem is a partial-correctness theorem. It does not by
itself claim CPython termination or behavior outside the modeled subset,
although the symbolic loop decreases nonnegative `N` and the concrete Python
loop ranges over a finite list.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K 7.1.293 parser, Haskell backend, reachability logic, and imported `INT`, `STRING`, `BOOL`, `MAP` definitions | All builds and proofs | Standard accepted tool/library trust boundary. |
| Trusted `py2mpy.py` | Program identity | Accepted launcher-owned input; regeneration is byte-identical. |
| `longestProgram`/`longestLoopBody` macros | Every claim | Not merely trusted: expanded term is mechanically identical to `solution.mpy`. |
| Candidate-generated `semantic.k` | All executions and proofs | Audited rule by rule; five fixed-semantics branch tests agree with both Python implementations. The Python correspondence remains an informal generated-semantics bridge rather than a separately proved CPython theorem. |
| `lengthString`, integer arithmetic/comparison, K Lists and Maps | Guards, lengths, fold, state | Standard K primitives. Unicode differential cases provide finite bridge evidence. |
| Inert handling of `typing` import | Entry execution | Acceptable for this exact typing-only import; general import effects are excluded. |
| Opaque total `stringAt` | Universal input elements, branches, result fold | Acceptable as external symbolic input. It is interpretation-parametric and value-sensitive, not an answer oracle. |
| `seqVal` representation and its five operational rules | Universal loop and nonempty entry claims | Concerning but not illegitimate. Rules are transparent and cover arbitrary finite sequences, but no bridge-free universal K connection to concrete `listVal` is supplied. |
| Python differential testing | Implementation and finite semantic bridge evidence | 9,893 zero-mismatch cases; empirical only, not a universal proof. |

### Decision

Fresh verification, result constraint, program identity, body sensitivity,
non-vacuity, and static rule validity all pass. The universal theorem is
unbounded and covers arbitrary string contents, so it does not materially
narrow the HumanEval contract. The missing machine-checked representation
connection and the finite-only Python/generated-semantics bridge are
documented non-fatal trust-boundary limitations.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
