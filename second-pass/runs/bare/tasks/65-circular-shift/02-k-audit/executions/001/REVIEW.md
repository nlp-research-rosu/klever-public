# Independent adversarial audit: 65-circular-shift

Headline decision: **CONCERNS / LEGIT**.

The proof was reconstructed from source and is a legitimate,
result-constraining reachability proof of the submitted translated program on
its stated formal domain. The concerns are scope and guard hygiene rather than
a false proved program result:

1. The two universal claims cover every **nonnegative** shift but no negative
   shift, while the natural-language prompt does not explicitly impose that
   precondition.
2. `clipIndex` is declared `[total]` over two arbitrary K integers, although
   its four equations are justified and nonoverlapping only when the second
   argument is a nonnegative string length. Every real call supplies such a
   length, so this does not create a false conclusion for a satisfying program
   input, but the declaration is wider than its audited contract.

Candidate-provided `#Top` output, compiled definitions, logs, trace, and final
report were not trusted. All material execution evidence below came from
reviewer-controlled scratch builds.

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `GENERATED_SEMANTICS`.
`/reference/reference-semantics` is absent, including as a symlink, as this
mode requires. There is therefore no infrastructure contradiction and no
hidden reference semantics was sought or used. See
[03-integrity-hashes.log](/audit-output/evidence/03-integrity-hashes.log).

### Candidate claims inspected as untrusted evidence

I read:

- `/candidate/run-input.json`, which claims problem
  `65-circular-shift`, condition `bare`, `kit: false`, and
  `semantics: false`;
- `/candidate/metrics.json`, which claims a zero generator exit without a
  timeout;
- `/candidate/codex-last.txt` and `/candidate/codex-output.log`, which claim
  AST identity, successful concrete runs, and `#Top`;
- the JSONL generation trace at
  `/candidate/codex-trace/2026/07/22/rollout-2026-07-22T05-22-20-019f8959-05b4-7bd2-96cf-31e5d75f4340.jsonl`;
- `/candidate/prove.sh`.

The bounded provenance excerpts and relevant markers are preserved in
[02-provenance-claims.log](/audit-output/evidence/02-provenance-claims.log)
and
[02b-provenance-markers.log](/audit-output/evidence/02b-provenance-markers.log).
None was used as proof evidence.

### Trusted-input comparisons and artifact inventory

The candidate prompt is byte-identical to `/reference/prompt.py`, SHA-256
`2751ca433b3ea9f4f348dd18f65c357482e140739e26ec98b1e056e55b491dc0`.
The candidate translator is byte-identical to `/reference/py2mpy.py`, SHA-256
`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.
Both values also match `run-input.json`.

All required candidate source artifacts are present as regular files:
`solution.py`, `solution.mpy`, `semantic.k`, `verification.k`, `spec.k`, and
`prove.sh`. There are no candidate symlinks, no helper K files, and no missing,
mistyped, or changed trusted prompt/translator artifact. A candidate
`PROOF.md` and candidate vacuity spec are absent, but neither was a required
generation deliverable.

The candidate additionally contains `semantic-kompiled/` and
`verification-kompiled/`, generator logs, metrics, and the structured trace.
These are additional untrusted evidence artifacts, not source-integrity
failures. The compiled trees were neither copied nor used. Full type/path
inventory is in
[01-artifact-inventory.log](/audit-output/evidence/01-artifact-inventory.log);
source hashes and comparisons are in
[03-integrity-hashes.log](/audit-output/evidence/03-integrity-hashes.log).

**Stage result: PASS.**

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and canonical behavior

The trusted prompt requires `circular_shift(x, shift)` to render integer `x`
as a string, rotate that string right by `shift`, and return a string. If
`shift` is greater than the rendered length, it must instead return the
rendering reversed. The examples are `(12, 1) -> "21"` and
`(12, 2) -> "12"`.

The trusted canonical implementation:

1. assigns `s = str(x)`;
2. returns `s[::-1]` when `shift > len(s)`;
3. otherwise returns
   `s[len(s)-shift:] + s[:len(s)-shift]`.

The candidate source is the same algorithm. Its `if` branch returns, so
omitting the canonical source's explicit `else` does not alter control flow.
For negative integers, both implementations treat the minus sign as part of
the string. For negative shifts, both ordinary-slice endpoints clip and the
result is the original string.

Numbered trusted and candidate source listings are in
[04-source-listings.log](/audit-output/evidence/04-source-listings.log).

### Trusted regeneration

Running the trusted translator on the copied candidate `solution.py` produced
a file byte-identical to the submitted `solution.mpy`; both have SHA-256
`35634b176f0c836959a648ca033f8fa84aa595d497afabf272920386b40de8d3`.
The exact command, hashes, comparison status zero, and exit status zero are in
[05-translation-identity.log](/audit-output/evidence/05-translation-identity.log).

### Independent differential test

The reviewer-authored
[differential_test.py](/audit-output/evidence/differential_test.py) loads the
trusted canonical entry point and the copied candidate entry point through
separate module loaders. It does not reuse K equations.

The test ran 158 distinct cases:

- both documented examples;
- `x = 0`, one-digit values, powers/boundaries around digit-length changes,
  negative integers, and multi-digit values;
- `shift = 0`, `1`, `len-1`, `len`, `len+1`, and `len+2`;
- negative shifts, because the prompt states no nonnegative precondition;
- 64 deterministic seeded large-integer cases.

No integer input has an empty decimal rendering; `x = 0` and one-character
renderings are the valid minimal boundaries. The run found zero mismatches and
exited zero. Every input and both results are in
[06-differential.log](/audit-output/evidence/06-differential.log).

Finite differential testing supports the source-to-canonical bridge but is not
treated as a universal K proof.

**Stage result: PASS, with the negative-shift specification scope carried
forward to Stage 4.**

## 3. Clean proof reconstruction

### Scratch isolation and toolchain

Only source artifacts were copied to `/tmp/audit-work/candidate-src`.
Reviewer build outputs were created under `/tmp/audit-work/build`. No
candidate compiled definition or cache was reused.

The available live toolchain is K `v7.1.293` with `kompile`, `krun`, `kprove`,
and `kast` in `/usr/bin`, plus Python 3.10.12. See
[07-toolchain.log](/audit-output/evidence/07-toolchain.log).

### Fresh builds

The generated language semantics was built independently:

```text
kompile --backend haskell semantic.k --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/build/semantic-kompiled
```

It exited zero:
[08-kompile-semantics.log](/audit-output/evidence/08-kompile-semantics.log).

The proof definition was separately built:

```text
kompile --backend haskell verification.k --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/build/verification-kompiled
```

It exited zero:
[09-kompile-proof.log](/audit-output/evidence/09-kompile-proof.log).

### Positive proof claims

The untouched submitted `spec.k` was proved as module `SPEC`; `kprove` exited
zero and printed exactly `#Top`. See
[10-kprove-all-original.log](/audit-output/evidence/10-kprove-all-original.log).

For independent per-claim execution, I made a reviewer-owned copy that adds
labels without altering any claim body, precondition, or postcondition:
[spec-audit-labeled.k](/audit-output/evidence/spec-audit-labeled.k).
All six claims independently exited zero and printed `#Top`:

| Claim | Evidence |
|---|---|
| Universal normal branch | [11-kprove-entry-normal.log](/audit-output/evidence/11-kprove-entry-normal.log) |
| Universal oversized branch | [12-kprove-entry-oversized.log](/audit-output/evidence/12-kprove-entry-oversized.log) |
| `(12,1) -> "21"` | [13-kprove-example-12-1.log](/audit-output/evidence/13-kprove-example-12-1.log) |
| `(12,2) -> "12"` | [14-kprove-example-12-2.log](/audit-output/evidence/14-kprove-example-12-2.log) |
| `(1234,2) -> "3412"` | [15-kprove-example-1234-2.log](/audit-output/evidence/15-kprove-example-1234-2.log) |
| `(1234,5) -> "4321"` | [16-kprove-example-1234-5.log](/audit-output/evidence/16-kprove-example-1234-5.log) |

Three initially parallel reviewer invocations failed before parsing because
the K launcher transiently failed to detect Java. Those infrastructure-only
outputs were preserved as
`14a-parallel-java-transient-example-12-2.log`,
`15a-parallel-java-transient-example-1234-2.log`, and
`16a-parallel-java-transient-example-1234-5.log`. Sequential reruns produced
the successful evidence above. This transient was not converted into a
candidate judgment.

### Fresh concrete semantics execution

The reviewer-authored
[concrete_semantics_test.py](/audit-output/evidence/concrete_semantics_test.py)
ran the submitted translated program against the separately rebuilt
`semantic-kompiled` definition and compared each final result with independent
trusted Python.

Twelve normal and boundary cases all consumed `<k>` to `.K`, produced the
expected `VString`, and exited zero. The cases cover both examples, zero shift,
`shift = len`, first oversized shift, reversal, `x = 0`, a negative integer,
and a negative shift. Full commands/configurations/results are in
[18-concrete-semantics-vs-python.log](/audit-output/evidence/18-concrete-semantics-vs-python.log);
an additional isolated smoke run is in
[17-krun-smoke-12-1.log](/audit-output/evidence/17-krun-smoke-12-1.log).

**Stage result: PASS.**

## 4. Adequacy and real-program pinning

### Plain-language statement of every entry claim

`spec.k` contains no loop or helper claims. Its six claims are:

1. For every K integer `X` and every integer `SHIFT` satisfying
   `0 <= SHIFT <= len(str(X))`, executing `circular_shift(X, SHIFT)` returns
   exactly the suffix beginning at `len(str(X))-SHIFT` followed by the prefix
   ending there.
2. For every K integer `X` and every integer `SHIFT` satisfying
   `len(str(X)) < SHIFT`, execution returns exactly the reverse of `str(X)`.
3. For `(12,1)`, execution returns exactly `"21"`.
4. For `(12,2)`, execution returns exactly `"12"`.
5. For `(1234,2)`, execution returns exactly `"3412"`.
6. For `(1234,5)`, execution returns exactly `"4321"`.

The two symbolic preconditions are satisfiable. For example:

- `X=1234, SHIFT=2` satisfies the normal precondition and the claimed summary,
  candidate Python, canonical Python, and fresh K execution all give
  `"3412"`.
- `X=1234, SHIFT=5` satisfies the oversized precondition and all four views
  give `"4321"`.

These substitutions appear in
[06-differential.log](/audit-output/evidence/06-differential.log),
[15-kprove-example-1234-2.log](/audit-output/evidence/15-kprove-example-1234-2.log),
[16-kprove-example-1234-5.log](/audit-output/evidence/16-kprove-example-1234-5.log),
and
[18-concrete-semantics-vs-python.log](/audit-output/evidence/18-concrete-semantics-vs-python.log).

### Exact program pinning

The `<k>` cell in each claim contains the `solutionProgram` macro. It is not an
unconstrained program variable. Using the freshly built proof definition, I
parsed the copied submitted `solution.mpy` and independently expanded
`solutionProgram`. The resulting KAST files are byte-identical, with the same
SHA-256
`804ec443c06fa8ddffe126572bb0e2c5aadcebd15731d25c80b451a68dabafb4`.
See
[19-program-ast-identity.log](/audit-output/evidence/19-program-ast-identity.log),
[solution-actual.kast](/audit-output/evidence/solution-actual.kast), and
[solution-macro.kast](/audit-output/evidence/solution-macro.kast).

Thus the claims execute the exact submitted translator tree. The top semantic
rule consumes that tree only after placing
`runProgram(P, entry, args)` in the result, and the recursive interpreter then
selects and executes its real function body.

The postconditions are not free variables or implications. Every claim
requires `<k>` to become `.K` and rewrites `<result>` from `VNone` to a
specific `VString`. A false result cannot satisfy the destination.

### Scope limitation

The symbolic preconditions partition all nonnegative shifts:
`0 <= SHIFT <= length` or `length < SHIFT`. They do not cover `SHIFT < 0`.
The prompt says “shift the digits right by shift” but gives no explicit
`shift >= 0` precondition. Both Python implementations and the generated
semantics do have concrete, agreeing behavior for negative shifts, as shown by
the differential and `krun` evidence, but that behavior is not universally
proved.

This is an intent-coverage limitation, not substitution, vacuity, or an
unsound result on the formal domain. It supports `CONCERNS / LEGIT` rather
than `PASS / LEGIT`.

**Stage result: PASS for real-program pinning and result constraint;
CONCERN for negative-shift intent coverage.**

## 5. Rule-by-rule static soundness review

The exhaustive reviewer inventory is
[rule-inventory.md](/audit-output/evidence/rule-inventory.md). It enumerates
every local syntax/data declaration, configuration cell, function,
`[total]` annotation, and all 45 local rules (42 in `semantic.k`, three in
`verification.k`) with individual decisions.

### Declaration inventory

The generated syntax models exactly the submitted AST subset:

- `Module`, statement lists, `FuncDef`, `Assign`, `If`, and `Return`;
- parameter and expression lists;
- `Name`, integer literal, binary/unary operations, comparison, call, and
  subscript;
- comparison operator, three-bound slice, `NoBound`;
- integer/string/Boolean/None values and statement execution results.

The configuration has only `<k>`, `<entry>`, `<args>`, and `<result>`.
The program requires no heap, object identity, I/O, allocation, exception,
or external-state cell.

The 19 semantic functions are `runProgram`, `bind`, `exec`, `branch`,
`continue`, `resultOf`, `eval`, `lookupVal`, `pyStr`, `pyLen`, `unary`,
`binary`, `compare`, `sliceFrom`, `sliceTo`, `reverseValue`, `clipIndex`,
`reverseString`, and `reverseFrom`.

`verification.k` adds the `solutionProgram` macro, unused `runSolution`
function, and mathematical `normalCircularShift` function. There are:

- no `[functional]` declarations;
- no local opaque/fresh symbols;
- no priority rules;
- no simplification rules;
- no ordinary proof-local operational bridges;
- no imported helper K files;
- exactly one `[total]` declaration, on `clipIndex`.

### Exhaustive rule groups and decisions

The inventory IDs make every rule explicit:

| IDs | Complete rule group | Static decision |
|---|---|---|
| S01-S03 | Top-level program consumption and function-name lookup | Sound for the real one-function module; matching/nonmatching guards are disjoint and all observable cells are explicit. |
| S04-S05 | Positional argument binding | Sound for the real equal-arity, distinct-name parameters `x` and `shift`. Mismatched arity remains visibly stuck rather than fabricating a result. |
| S06-S15 | Empty execution, assignment, conditional dispatch, return, continuation, result extraction | Sound control flow. `returned(V)` prevents following statements from executing; normal branches continue with the suffix. |
| S16-S18 | Name lookup and integer literal evaluation | Sound for the environment built from the submitted parameters/local assignment. |
| S19-S23 | Unary, binary, comparison, `str`, and `len` expression dispatch | Sound for used pure expressions. Recursive operand evaluation does not expose an order difference because the supported operands have no side effects. The actual source does not rebind `str` or `len`. |
| S24-S26 | Exact reverse, lower-only, and upper-only slice forms | Each pattern matches one of the three slice forms actually emitted by `solution.mpy`; they do not silently cover an unmodeled used form. |
| S27-S32 | Integer-to-decimal-string, ASCII string length, integer minus, string concatenation, integer greater-than | Sound ordinary primitive bridges for the claimed `VInt` inputs. |
| S33-S36 | Python-style endpoint clipping | Disjoint, exhaustive, and correct on every reachable `L=lengthString(S) >= 0`. See the guard-scope concern below. |
| S37-S38 | Lower/upper slices through clipped `substrString` | Sound; fresh concrete boundary tests agree with Python. |
| S39-S42 | Reverse wrapper, seed, base, and descending recursive character append | Sound reversal on the reachable range. The index strictly decreases, the base is exhaustive below zero, and every selected index is in the source string. |
| V01 | Fixed-program macro | Sound pinning; independently byte-identical to parsed submitted KAST. |
| V02 | `runSolution` wrapper | Sound but unused, so it contributes nothing to claim closure. |
| V03 | Suffix-plus-prefix summary | A truthful definitional summary under the normal claim guard; it does not replace execution. |

Every constructor used by `solution.mpy` maps to both a syntax declaration and
the listed execution rules. Calls and returns preserve bindings and control.
The only state change is the map update for local `s`. There is no omitted
observable state. Ordinary function-rule guards used by the real execution
are disjoint and cover every reachable case.

### Result-bearing abstractions and bridge audit

There is no unconstrained oracle:

- `normalCircularShift` has an explicit suffix-plus-prefix equation, appears
  only in the postcondition, and the universal entry claim itself connects
  real execution to it.
- `reverseString` is used by both reverse execution and the postcondition, but
  it is not opaque: `reverseString`/`reverseFrom` have exhaustive,
  descending equations that fix every reachable character and result.
- `Int2String`, `lengthString`, `substrString`, `+String`, integer arithmetic,
  comparison, and K maps are imported K primitives, not task-answer symbols.

The reverse and clipping rules summarize Python primitives, not
program-defined task logic. Their equations were checked against their exact
matched forms and observable state. The submitted function body itself
executes through `runProgram`/`exec`/`eval`.

As an additional body-sensitivity check, I swapped the ordinary branch's
suffix/prefix order in a reviewer-owned source mutant and translated it with
the trusted translator. For `(1234,1)`, canonical/original behavior is
`"4123"`, the mutant Python result is `"1234"`, and the fresh generated
semantics also returns `"1234"`. This shows that the interpreter result is
sensitive to the submitted body rather than a hidden circular-shift answer.
See
[solution-body-mutant.py](/audit-output/evidence/solution-body-mutant.py),
[solution-body-mutant.mpy](/audit-output/evidence/solution-body-mutant.mpy),
and
[22-body-sensitivity.log](/audit-output/evidence/22-body-sensitivity.log).

### `clipIndex` guard/totality concern

For every real call, `L = lengthString(S) >= 0`; on that domain S33-S36 are
pairwise disjoint, exhaustive, and match Python endpoint clipping.

The declaration nevertheless says `[function, total]` over all `Int, Int`.
Outside the reachable domain, the guards overlap. The symbolic witness
`clipIndex(0, -1)` satisfies both:

- S33: `0 < -(-1)`, yielding `0`;
- S36: `-1 < 0`, yielding `-1`.

Negative string length cannot be induced by any intended `x`/`shift` input,
the helper is absent from every claim interface, and the meaningful false
program-result mutation in Stage 6 remains rejected. Per the audit's decision
boundary, this is recorded as an over-broad-but-sound-on-the-intended-domain
rule concern. It is not used as an unsupported claim that a false real-program
conclusion is provable. Narrowing the declaration/rules with `L >= 0` would
remove the concern.

**Stage result: PASS for real-program soundness, with a nonmaterial global
guard/`[total]` concern.**

## 6. Fresh non-vacuity test

I did not rely on any candidate vacuity artifact. The fresh reviewer mutation
is
[spec-vacuity-audit.k](/audit-output/evidence/spec-vacuity-audit.k).
It uses the realizable input `(12,1)` and changes only the result obligation
from the true `"21"` to the false `"12"`.

First, `kprove --dry-run` parsed and built the mutation successfully and exited
zero:
[20-vacuity-dry-run.log](/audit-output/evidence/20-vacuity-dry-run.log).

The actual mutated proof then exited one with
`WarnStuckClaimState`. Its reachable residual has `<k> .K </k>` and
`<result> VString("21") </result>`, which does not unify with the mutated
destination `VString("12")`. This is the expected unmet result obligation, not
a parser error, missing import, timeout, unrelated crash, or unreachable
mutation. See
[21-vacuity-expected-failure.log](/audit-output/evidence/21-vacuity-expected-failure.log).

The original positive `(12,1)` claim independently closes with `#Top`, so the
mutation distinguishes the true and false results.

**Stage result: PASS.**

## 7. Proven-versus-assumed accounting

### What the K proof establishes

Under the rebuilt generated MPY semantics, the successful reachability proof
establishes partial correctness of the exact submitted translated AST:

- for all K integers `X` and `SHIFT` with
  `0 <= SHIFT <= lengthString(Int2String(X))`, terminating execution consumes
  the program and returns the mathematically specified suffix plus prefix;
- for all K integers `X` and `SHIFT` with
  `lengthString(Int2String(X)) < SHIFT`, terminating execution consumes the
  program and returns the recursively defined reverse;
- the four concrete results in `spec.k` follow as special cases.

The proof does not establish a theorem for negative shifts. It does not by
itself prove that the generated MPY semantics is full CPython, and it does not
model unused Python constructs or exceptional inputs with non-integer
arguments.

### Trust ledger

| Boundary | Dependents | Status |
|---|---|---|
| K toolchain, Haskell backend, reachability engine, SMT support | All machine-checked claims | Standard trusted proof infrastructure; rebuilt execution and exact exit/output are recorded. |
| Imported `DOMAINS` integers, strings, maps, `Int2String`, `lengthString`, `substrString`, arithmetic, comparison, concatenation | All semantic execution and summaries | Acceptable low-level K primitive boundary. For this program strings are decimal ASCII, avoiding Unicode/byte-length ambiguity. |
| Trusted `/reference/py2mpy.py` | Source-to-`solution.mpy` identity | Explicit trusted input; fresh output is byte-identical. This is provenance, not a proof of Python semantics. |
| Candidate-generated MPY operational semantics | Link from translated AST execution to result | Audited rule by rule. It is minimal but covers every used constructor. The Python-subset correspondence is an informal semantic argument supported by fresh concrete comparisons, not a separately machine-checked compiler-correctness theorem. |
| Recursive `reverseString`/`reverseFrom` equations | Oversized-branch result | Acceptable program-independent mathematical definition: exhaustive on reachable indices and strictly descending; no opaque value remains. |
| `normalCircularShift` equation | Normal-branch postcondition | Acceptable definitional summary under the claim guard; the universal entry proof connects execution to it. |
| Canonical Python implementation | Natural-language intent bridge and differential oracle | Trusted input and independent executable oracle. The 158-case differential run is finite support only. |
| Nonnegative-shift formal precondition | Scope of universal theorem | Concerning because not explicit in the prompt; negative behavior is tested but not universally proved. |
| `clipIndex` totality outside `L >= 0` | No reachable real-program execution | Concerning guard hygiene; overlap witness documented, but it cannot arise from a string length or satisfying program input. |

There are no other opaque symbols, fresh result variables, empirical
replacement rules, assumed loop invariants, or proof-local execution bridges.
Candidate prose, generation traces, and candidate `#Top` output contribute no
trust.

### Gate accounting and decision

- **Real-program soundness:** pass. Exact AST pinning, full result constraint,
  body sensitivity, rule audit, and false-result rejection all hold on every
  satisfying formal input.
- **Intent adequacy:** concern. The universal claims omit negative shifts even
  though the prompt gives no explicit nonnegative restriction.
- **Evidence auditability:** pass. Reviewer scripts, exact commands, bounded
  outputs, exit statuses, and negative-test residual are preserved under
  `/audit-output/evidence/`.

The proof is therefore legitimate but not a clean `PASS`: its stated theorem
soundly pins the real generated program, while the negative-shift scope and
over-broad helper totality declaration are documented limitations that do not
make a false result provable for the intended program domain.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
