# Independent adversarial audit: 29-filter-by-prefix

The candidate contains a legitimate, result-constraining partial-correctness
proof of the submitted program over arbitrary finite abstract string lists and
prefixes. Fresh reconstruction closed both claims, the theorem is pinned to the
trusted regeneration of `solution.mpy`, and independent body and postcondition
mutations failed for the expected semantic reasons.

The verdict is `CONCERNS / LEGIT`, rather than `PASS`, because this individually
generated language definition has several rules whose match domains are wider
than the exact contexts justified here (`ImportFrom`, append binding/mutation,
and return continuation handling). They do not enable a false conclusion for
this pinned program on its intended plain-`list[str]`/`str` domain, but they are
not a generally validated Python semantics. The Python-to-K intent bridge also
remains an audited and extensively tested informal bridge, not a separate
machine-checked CPython connection theorem.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout =
legacy-selected-stage1`, condition `bare`, and
`semantics_mode = GENERATED_SEMANTICS`. The trusted
`/reference/reference-semantics` tree is absent, as this mode requires; no
hidden or inferred reference semantics was used.

The audit campaign object in `/audit-campaign-lock.json` is exactly equal to
the campaign object in `/audit-input.json`, and the lock's independent SHA-256
is the recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
All required records for this legacy layout are present as real regular files:
`/run.json`, `/task.json`, `/generation-result.json`,
`invocation.json`, `metrics.json`, `usage.json`, `codex-last.txt`,
`codex-output.log`, `prompt.txt`, and the one JSONL file under
`codex-trace/`. Historical `runtime-metrics.json` is not required for this
layout and was not reconstructed.

Every recorded per-file digest was recomputed and matched. The mounted
candidate's canonical pipeline tree digest is
`12c02e9aacde66dfeb724fcbb166d582e1caebc8bf2325940f085e7e8c57b032`,
equal to the retained workspace digest in both the invocation and stage result.
The trace's independently recomputed pipeline tree digest is
`96115c1bebdfe50ff1cf7892286db77bf32fe20fc386098bb13d3d53a1821c41`,
equal to `usage.json`'s source-trace digest; its single JSONL file also matches
the per-file digest in the stage result. The full trace has 347 valid JSON
records, and the complete 943,397-character generation log was read. These
generation materials claim success but were not used as proof authority.

`/candidate/prompt.py` and `/candidate/py2mpy.py` are byte-identical to the
trusted `/reference` mounts. The candidate contains real regular files for
`solution.py`, `solution.mpy`, `semantic.k`, `verification.k`, `spec.k`, and
`prove.sh`; its tree has no linked or unsupported entry. The candidate's
`__pycache__` was ignored. There is no infrastructure breach.

Evidence: [provenance script](/audit-output/evidence/provenance_check.py) and
[complete provenance log](/audit-output/evidence/01-provenance.log).

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract is: for a finite list of strings and a string prefix,
return, in original order and with duplicates preserved, exactly those input
strings whose beginning equals the prefix. The documented cases require
`([], "a") -> []` and
`(["abc","bcd","cde","array"], "a") -> ["abc","array"]`.
The trusted canonical implementation is the corresponding stable list
comprehension.

The submitted `solution.py` initializes a fresh result list, visits every input
string in order, appends it exactly when `string.startswith(prefix)` is true,
and returns the accumulator. This is extensionally the canonical algorithm on
the intended domain.

Running the trusted translator on the scratch copy of `solution.py` reproduced
the submitted `solution.mpy` byte-for-byte. Both have SHA-256
`7d10644743b0d635231400e73ff58c5755e17dd09b7a73f64b79fd8fa0a12269`;
see [regeneration log](/audit-output/evidence/02-regeneration.log).

The independent differential test imports the trusted canonical and candidate
functions under distinct module names. It checks 14 documented/boundary cases,
all 7,225 singleton combinations from 85 strings over
`a`, `b`, `é`, and `🙂` of length at most three, and 1,000 seeded lists of
length at most 12. It includes empty prefixes, equal and longer-prefix
boundaries, both conditional outcomes, duplicates/order, composed and
decomposed Unicode, astral characters, and embedded NUL. All 8,239 cases
matched, with no input mutation. See
[test source](/audit-output/evidence/differential_test.py) and
[result log](/audit-output/evidence/02-differential.log).

## 3. Clean proof reconstruction

Only source artifacts were copied to
`/tmp/audit-work/29-filter-by-prefix/candidate-src`; no candidate-built
definition or cache was copied or used. K reports version 7.1.293.

Fresh definitions were built successfully:

```text
kompile --backend llvm semantic.k --main-module SEMANTIC \
  --syntax-module VERIFICATION --output-definition concrete-kompiled
EXIT_STATUS: 0

kompile --backend haskell semantic.k --main-module SEMANTIC \
  --syntax-module VERIFICATION --output-definition verification-kompiled
EXIT_STATUS: 0
```

Logs:
[LLVM](/audit-output/evidence/03-kompile-llvm.log) and
[Haskell](/audit-output/evidence/03-kompile-haskell.log).

The fresh LLVM semantics executed the empty input, prompt example, empty
prefix, prefix-longer-than-string, duplicates/order, Unicode/astral, and
embedded-NUL cases to `.K` with the same result as Python. In particular, the
prompt example returns `listVal(cons("abc",cons("array",nil)))`; the empty
prefix retains every element; and `["a"]` with prefix `"aa"` returns `nil`.
The concrete logs are
[empty](/audit-output/evidence/03-krun-empty.log),
[prompt](/audit-output/evidence/03-krun-prompt.log),
[empty-prefix](/audit-output/evidence/03-krun-empty-prefix.log),
[long-prefix](/audit-output/evidence/03-krun-long-prefix.log),
[Unicode](/audit-output/evidence/03-krun-unicode.log),
[duplicates](/audit-output/evidence/03-krun-duplicates.log), and
[NUL](/audit-output/evidence/03-krun-nul.log).

A broader executable K-to-CPython bridge ran 20 whole-program K executions:
ten systematic prefixes against all 31 binary-alphabet strings of length at
most four (310 prefix decisions), plus ten seeded lists. Every K output cell
equaled both Python implementations. This is finite evidence, not a universal
replacement for the K proof. See
[bridge source](/audit-output/evidence/k_semantics_differential.py) and
[bridge log](/audit-output/evidence/05-k-semantics-differential.log).

Every positive proof target closed on the fresh Haskell definition:

```text
kprove spec.k --definition verification-kompiled --claims loop-correct
#Top
EXIT_STATUS: 0

kprove spec.k --definition verification-kompiled \
  --claims loop-correct,program-correct --trusted loop-correct
#Top
EXIT_STATUS: 0

kprove spec.k --definition verification-kompiled
#Top
EXIT_STATUS: 0
```

The first run independently proves the helper. The second proves the entry
claim using that separately established helper. Most importantly, the third
run retains both claims and trusts neither. Logs:
[loop](/audit-output/evidence/03-kprove-loop.log),
[entry after proved loop](/audit-output/evidence/03-kprove-program-with-proved-loop.log),
and [combined untrusted](/audit-output/evidence/03-kprove-all.log).

One diagnostic command selected only `program-correct` while naming the
excluded `loop-correct` label trusted; it did not progress and was manually
interrupted. It is not a required proof path, and the corrected and stronger
commands above succeeded. The exact record is
[selector diagnostic](/audit-output/evidence/03-selector-diagnostic-note.md).

## 4. Adequacy and real-program pinning

### Claims in plain language

`loop-correct` (`/candidate/spec.k:5`) says: for every remaining `StrList`,
prefix `String`, and accumulated `StrList`, if the environment binds
`prefix` and `result` to those values and the exact submitted loop body is
followed by `return result` and function end, then termination produces
`filterAcc(remaining,prefix,accumulator)`. It preserves the fixed input/prefix
cells and does not claim a particular final local environment.

`program-correct` (`/candidate/spec.k:19`) says: from empty environment and
function maps, arbitrary `INPUT:StrList` and `PREFIX:String`, and `noOutput`,
executing `solutionProgram()` to completion returns
`listVal(filterByPrefix(INPUT,PREFIX))`. The returned value is an equality in
the post-state, not a free variable, tautology, or one-way implication.

Both preconditions are satisfiable. A program witness is empty maps,
the prompt-example input, prefix `"a"`, and `noOutput`. A loop witness is
`INPUT=["abc","bcd"]`, `PREFIX="a"`, `ACC=["seed"]`, empty remaining
environment/function maps, and `noOutput`; its claimed result is
`["seed","abc"]`. The explicit witness and both Python results are in
[ground-witness log](/audit-output/evidence/04-ground-witness.log). The
program witness's K execution is the prompt `krun` log cited above.

### Mechanical program identity

There are two independent links:

1. Trusted regeneration proves byte identity between `solution.py`'s
   translated constructor term and the submitted `solution.mpy`.
2. An auditor-written constructor-only expansion of the
   `solutionProgram()` and `loopBody()` rule right-hand sides parses to
   byte-identical KAST JSON with submitted `solution.mpy`. Both JSON files
   have SHA-256
   `81554ff637935d66aad6f107187a12b6c76a8586029c9b1d6eea0fef5bb88333`.

See [expanded term](/audit-output/evidence/solutionProgram-expanded.mpy),
[submitted KAST](/audit-output/evidence/04-submitted.kast.json),
[expanded KAST](/audit-output/evidence/04-expanded.kast.json), and
[comparison log](/audit-output/evidence/04-constructor-compare.log).
The only normalization is explicit empty-list constructors (`.Strings` and
`.Stmts`) and the two nullary naming functions that expand to the compared
constructors. No material statement or control effect is omitted. The typing
import/annotations do not influence this function's returned contents.

The proof is body-sensitive. In a fresh definition, the executed
`solutionProgram()` term was changed so the real `For` body became `.Stmts`,
while the postcondition stayed unchanged. The mutation compiled, then
`kprove` exited 1 with a `WarnStuckClaimState` whose one-element residual has
actual `listVal(nil)` but requires
`filterAcc(cons(H,nil),PREFIX,nil)`. The ground witness
`INPUT=["a"], PREFIX="a"` returns `[]` in the mutation but requires `["a"]`.
See [mutated definition](/audit-output/evidence/04-verification-body-mutation.k),
[build log](/audit-output/evidence/04-body-mutation-kompile.log), and
[proof log](/audit-output/evidence/04-body-mutation-kprove.log).

There is no automated source-to-proof regeneration in the immutable candidate,
but the trusted byte regeneration, constructor comparison, and body
sensitivity establish pinning for this artifact. Lack of automation is an
artifact-maintenance observation, not a theorem defect.

## 5. Rule-by-rule static soundness review

The complete line-addressed inventory and assessments are preserved in
[05-rule-inventory.md](/audit-output/evidence/05-rule-inventory.md). The local
inventory is exhaustive:

- Syntax: `StrList`, `Module`, statement/string lists, `Params`, seven
  statement forms, five expression forms including the `Val` subsort, six
  value forms, `Function`, `Output`, eleven administrative `KItem`s, and the
  six functions `appendOne`, `startsWith`, `filterAcc`,
  `filterByPrefix`, `loopBody`, and `solutionProgram`.
- Configuration: `k`, environment map, function map, fixed input list, fixed
  prefix, and output.
- Attributes: only `startsWith` is `[total]`; only the two recursive
  `filterAcc` branches are `[simplification]`.
- There are no local aliases, contexts, priority rules, `owise` rules, opaque
  symbols, or `[functional]` declarations.

### All 33 `semantic.k` rules

1. Lines 71 and 72 are the base and structurally recursive equations for
   append-at-end.
2. Lines 75-78 are the disjoint and exhaustive
   `|P|>|S|`/`|P|<=|S|` definitions of prefix comparison. The substring
   bounds are valid.
3. Lines 81-86 unpack a module, sequence statements, eliminate the empty
   sequence, ignore the target's typing import, and register function bodies.
4. Lines 89-93 select the exact two-argument `filter_by_prefix`, bind both
   formal names to the supplied cells, and start its body.
5. Lines 96-108 implement name lookup, empty-list creation, left-to-right
   method binding/call argument evaluation, string prefix testing, and
   accumulator append.
6. Lines 111-119 implement RHS-first assignment, one-time iterable evaluation,
   empty/nonempty loop cases, loop-variable binding, and ordered body
   execution.
7. Lines 121-125 implement guard-first `if` and disjoint Boolean branches.
8. Lines 127-128 evaluate then discard expression statements.
9. Lines 130-134 evaluate return expressions, write the output, unwind the
   continuation, and provide the no-explicit-return fallback.

That enumeration accounts for every rule: 2 append rules, 2 prefix rules,
6 module/function-launch rules, 9 expression/call rules, 10
assignment/loop/conditional rules, 2 expression-statement rules, and 2 return
rules (33 total).

Every submitted constructor is mapped: `Module` to line 81, `ImportFrom` to
84, `FuncDef` to 85-93, `Assign`/`ListExpr` to 98 and 111-113, `For` to
115-119, `Name` to 96, `If` to 121-125, calls/attributes to 99-108,
expression statement to 127-128, and `Return` to 130-132. On the pinned
program, evaluation is left-to-right, the source list is evaluated once, the
result accumulator is unaliased, loop order and duplicates are preserved, and
the return continuation is exactly `functionEnd ~> .K`.

### All 6 `verification.k` rules

1. Line 9 defines `filterByPrefix` by initializing `filterAcc` with `nil`.
2. Line 10 returns the accumulator on empty input.
3. Lines 11-13 append a matching head and structurally recurse.
4. Lines 14-16 skip a nonmatching head and structurally recurse.
5. Lines 24-27 expand `loopBody()` to the exact submitted conditional append.
6. Lines 29-35 expand `solutionProgram()` to the exact submitted module.

The guarded filter rules cannot overlap with disagreeing right-hand sides:
`startsWith` is a total Boolean, so true and false are disjoint and exhaustive.
All recursive functions descend on a `StrList`. `filterAcc` and
`filterByPrefix` occur in postconditions, not in the program's `<k>` execution.
`loopBody` and `solutionProgram` are transparent syntax names, not result
oracles or execution-skipping summaries.

The imported `BOOL`, `INT`, `STRING`, and `MAP-SYMBOLIC` hooks are the
low-level K trust boundary for Boolean equality, integer order, string
length/substrings/equality, and finite map lookup/update. `startsWith` is fully
defined over those primitives; it is neither fresh nor opaque. K strings can
represent embedded NUL and arbitrary byte sequences; Unicode, NUL, and
surrogate-pass byte encodings were exercised
([Unicode](/audit-output/evidence/03-krun-unicode.log),
[NUL](/audit-output/evidence/03-krun-nul.log), and
[surrogate bytes](/audit-output/evidence/05-krun-surrogate-bytes.log)).

No rule was found that encodes the task answer into execution, fabricates a
result for an unmodeled used construct, or replaces a program-defined
computation with an unconstrained oracle. No local rule can enable a concrete
or symbolic false target conclusion on the intended input domain.

There is a narrower reuse gap, not a target unsoundness claim. Line 84 matches
imports beyond the inert typing import; line 102 does not implement general
descriptor/receiver lookup; line 107 models append by updating an unaliased
environment binding rather than a heap object; and line 131 accepts an
arbitrary continuation although only the exact final-function continuation is
validated. Side-effecting imports, aliases/descriptors, caller frames, and
cleanup continuations provide out-of-scope countercontexts for a *general*
Python semantics, but none is reachable by any intended input to the pinned
program. Per the required witness rule, these are reported as
over-broad-but-target-sound limitations, not labeled materially unsound.

## 6. Fresh non-vacuity test

No candidate vacuity artifact was relied upon. The fresh
`SPEC-VACUITY` mutation changes the entry output obligation from
`filterByPrefix(INPUT,PREFIX)` to
`cons("__AUDIT_FALSE__", filterByPrefix(INPUT,PREFIX))`. With the satisfiable
empty-input state and prefix `"a"`, actual and original claimed output are
`[]`, while the mutation demands `["__AUDIT_FALSE__"]`.

The mutated spec successfully parsed and generated KORE:

```text
kprove spec-vacuity.k --definition .../verification-kompiled \
  --spec-module SPEC-VACUITY --dry-run
EXIT_STATUS: 0
```

The actual proof exited 1 with `WarnStuckClaimState`; its residual explicitly
requires the impossible equality
`cons("__AUDIT_FALSE__", filterAcc(...)) = filterAcc(...)`. Thus the failure is
the expected reachable unmet result obligation, not a parser error, missing
import, timeout, or unrelated crash.

Evidence:
[mutation](/audit-output/evidence/06-spec-vacuity.k),
[successful dry-run](/audit-output/evidence/06-vacuity-dry-run.log), and
[expected proof failure](/audit-output/evidence/06-vacuity-kprove.log).

## 7. Proven-versus-assumed accounting

### Formally established

Conditional on the compiled local theory, the combined untrusted reachability
proof establishes: for every finite `StrList INPUT` and `String PREFIX`, if
the exact pinned module starts from empty maps and terminates, its output is
the stable list of precisely those elements for which the defined
`startsWith(element,PREFIX)` is true. List length is not bounded; this is not
finite unrolling or proof of examples. The progressing loop circularity covers
arbitrary finite constructor lists. Order and duplicates are part of
`filterAcc`'s equations.

This is partial correctness. The report does not upgrade it to a formal
termination theorem, although concrete semantics and structurally finite
execution make termination evident for finite well-typed inputs.

### Assumptions and boundaries

| Boundary | Influence | Assessment |
|---|---|---|
| K 7.1.293 parser, compiler, Haskell prover, LLVM executor | All formal results | Standard unavoidable toolchain trust; both backends were rebuilt from source. |
| Imported Boolean, integer, string, and map hooks | Guards, prefix value, state | Acceptable low-level primitives. Their use is direct and the candidate adds no opaque equation. |
| Trusted `py2mpy.py` | Python AST to submitted constructor term | Authorized trusted input; byte regeneration proves this candidate was translated by it, but not the translator's metatheory. |
| Generated target-language rules versus CPython | Binding, calls, loop, mutation, return | Audited construct-by-construct and tested, but the correspondence is informal rather than a universal CPython connection theorem. This is a non-fatal concern. |
| `startsWith` as the modeled external string method | Branches and final filtered value | Fixed by exhaustive K equations over string primitives, not an oracle. Unicode/NUL and broader whole-program differential evidence support the CPython bridge. |
| Plain finite `list[str]` and `str` execution | The theorem domain | Matches the HumanEval type/intent. Subclasses with overridden descriptors, mutation through aliases, exceptional imports, resource exhaustion, and reflective observation of annotations/object identity are outside this minimal semantics and are not material to the requested extensional result. |
| Candidate differential and generation records | Empirical support only | Never used as a substitute for `kprove`; all audit tests were independently authored and rerun. |

There are no proof-local opaque symbols, trusted candidate claims, priority
bridges, or empirical values injected into the postcondition. The same
`startsWith` symbol affects execution and the summary, but this is not circular:
it has complete guarded equations in `semantic.k` and is an external language
primitive, not a program-derived unknown.

Gate A (real-program soundness) passes: exact body pinning, full rule review,
positive proof reconstruction, body sensitivity, satisfiable witnesses, and
false-postcondition rejection all pass. Gate B (intent adequacy) passes for the
material unrestricted HumanEval domain: arbitrary finite string lists and
prefixes, with no fixed size or example bound. Gate C (trust/evidence
auditability) passes: every assumption and empirical bridge is named and its
reproducible evidence is present. The non-fatal concerns are the informal
generated-semantics bridge and rules broader than the exact target context;
neither admits a false conclusion for the theorem actually claimed.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
