# Independent adversarial review: 86-anti-shuffle

## Executive decision

The candidate's K claims do reconstruct cleanly: both definitions compile from
source, every one of the seven positive claims independently prints `#Top` and
exits 0, the named `solutionProgram` is the submitted translated program, and
a fresh false-result mutation is correctly rejected.

That machine closure is not a legitimate proof of the real Python program over
the claim's domain. The generated semantics interprets Python string indexing
and slicing with K byte-oriented `substrString`/`lengthString`. On the
satisfying input U+03A9 (`"Ω"`), a fresh identity baseline preserves bytes
`CE A9`, the actual K execution of `anti_shuffle` returns `A9 CE`, and both the
submitted Python entry point and the trusted canonical return the unchanged
Python character. A separately built K fidelity claim requiring `CE A9` is
stuck with actual result `A9 CE`. The formal entry claim has no ASCII or other
domain restriction. This is a concrete false-result witness for the semantics
rules actually used by the submitted program, not a timeout or untested
speculation.

There is also an ASCII real-execution gap: on this Python 3.10.12 runtime the
canonical returns normally for `"a" * 996`, while the submitted recursive
implementation raises `RecursionError`; the K configuration has neither
recursion-depth nor exception state. Partial correctness does not establish
termination, but hiding a reachable real-program exception further limits the
claimed program pinning.

Accordingly, the earliest validation gate—real-program soundness—fails. The
positive `#Top` results prove an internally coherent theorem about the
candidate's byte-string model, not the required theorem about the real
generated Python program.

## 1. Input and provenance integrity

### Rendered-mode boundary

The rendered mode is `GENERATED_SEMANTICS`. `/reference` contains exactly the
three trusted regular files `canonical.py`, `prompt.py`, and `py2mpy.py`;
`/reference/reference-semantics` is absent. This is the required boundary, so
there is no infrastructure-mode breach and candidate verdict markers are
appropriate. See `evidence/integrity.log`.

The candidate has regular-file source artifacts:

- `prompt.py`, `py2mpy.py`, `solution.py`, and `solution.mpy`;
- `semantic.k`, `verification.k`, `spec.k`, and `prove.sh`;
- `run-input.json`, `metrics.json`, `codex-last.txt`,
  `codex-output.log`, and one structured JSONL generation trace.

There are no symlinks anywhere below `/candidate`. There are candidate-built
`semantic-kompiled/`, `verification-kompiled/`, and `__pycache__/` trees. Those
are extra untrusted caches, not source inputs; none was copied into or used by
the audit reconstruction. No additional helper K source file exists.

### Trusted comparisons and untrusted claims

`/candidate/prompt.py` is byte-identical to `/reference/prompt.py` (SHA-256
`f8a02b...a972`), and `/candidate/py2mpy.py` is byte-identical to the trusted
translator (SHA-256 `406485...b16`). Full hashes are recorded in
`evidence/integrity.log`.

The untrusted metadata is structurally readable and consistent with problem
`86-anti-shuffle`, condition `bare`, and the same prompt/translator hashes.
`metrics.json` claims a successful, non-timeout 903-second run.
`codex-last.txt` and `codex-output.log` claim three `#Top` stages, concrete
tests, and 2,000 Python differential cases. The one structured trace has 320
valid JSONL records and the same terminal claim. These records were treated
only as claims; their hashes, sizes, bounded first/last lines, and event counts
are in `evidence/provenance-summary.log`. Nothing in those reports substitutes
for the reconstruction below.

No required source artifact is missing, changed at the trusted prompt/
translator boundary, mistyped, or symlinked.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The prompt requires `anti_shuffle(s)` to preserve the sequence of words and
literal space separators while sorting the characters within each word in
ascending character/ASCII order. The trusted canonical implements:

1. split on the literal one-character separator `" "`;
2. sort every resulting word with Python `sorted`;
3. concatenate each sorted word and join the list with `" "`.

Consequently, leading, trailing, and repeated literal spaces are preserved
exactly. The signature states only that `s` is a string; it supplies no
ASCII-only or length precondition. The trusted canonical also defines the
observable result for Python Unicode strings.

### Submitted implementation and translation

`solution.py` implements insertion sort recursively:

- `insert_char` inserts one character into a growing sorted word;
- `process_words` consumes the source left-to-right, emits a word on each
  literal space, and recurses;
- `anti_shuffle` calls `process_words(s, "", "")`.

The branch boundaries are the empty word, `char <= word[0]`, empty remaining
text, literal-space text head, and ordinary-character text head.

The trusted command

`python3 /reference/py2mpy.py /candidate/solution.py`

generated `solution.regenerated.mpy` with SHA-256
`5fa109...31df`, byte-identical to `/candidate/solution.mpy`. Exact command and
exit 0 are in `evidence/translator-regeneration.log`.

### Independent differential

`evidence/differential_test.py` imports the trusted canonical and scratch copy
of the submitted entry point independently. The preserved deterministic corpus
in `evidence/differential-inputs.jsonl` contains 10,349 inputs (SHA-256
`cde4ed...82e5`):

- all documented examples;
- empty, one/multiple space, leading/trailing/repeated-space cases;
- equality and both sides of insertion/scan branch boundaries;
- exhaustive strings of lengths 0 through 5 over `" aB!0é"`;
- 1,000 seeded random strings of lengths 0 through 80 over ASCII, whitespace,
  punctuation, and selected Unicode;
- explicit Unicode and Python recursion-boundary cases.

The exact test command exited 1 with eight visible divergences, all normal
canonical return versus submitted `RecursionError`: repeated `"a"` at lengths
996 through 1001 and 1100, plus a length-1040 alphabetic word. Length 995
returns normally from both. The focused record is
`evidence/recursion-boundary.log`; the complete deterministic run is
`evidence/differential-test.log`. All 10,341 other cases, including the Unicode
cases, agree between the two Python implementations.

This result supports the mathematical equality of returned values over the
tested normal executions. It also demonstrates that the submitted recursive
Python entry point is not behaviorally identical to the canonical over all
unrestricted Python strings. Since the requested proof is partial correctness,
the recursion witness is accounted as a normal-termination/exception boundary,
not used as a substitute for the result-soundness counterexample in Stage 5.

## 3. Clean proof reconstruction

### Isolation and toolchain

Only regular source files were copied to
`/tmp/audit-work/reconstruction`. Neither candidate `*-kompiled` directory nor
candidate cache was copied. The source hashes in
`evidence/reconstruction-sources.log` match Stage 1, including the independently
regenerated `solution.mpy`.

The live toolchain is `/usr/bin/{kompile,krun,kprove}`, K v7.1.293, recorded in
`evidence/toolchain.log`.

### Fresh builds

Both source builds used distinct, previously absent scratch outputs:

- Haskell `kompile semantic.k --main-module MPY --syntax-module MPY-SYNTAX
  --output-definition semantic-fresh-kompiled`: exit 0
  (`evidence/kompile-semantic.log`);
- Haskell `kompile verification.k --main-module VERIFICATION
  --syntax-module MPY-SYNTAX
  --output-definition verification-fresh-kompiled`: exit 0
  (`evidence/kompile-verification.log`).

### Fresh concrete executions

Fresh `krun` executions on `""`, `" "`, `"Hi"`, `"ba"`, `"aa"`,
`"Hello World!!!"`, `"  ba  dc "`, and `"zA9! 0b?"` all exited 0.
Their K results equal both Python implementations:

- `""`, `" "`, and `"Hi"` remain unchanged;
- `"ba"` becomes `"ab"` and the equality branch `"aa"` remains `"aa"`;
- the prompt example becomes `"Hello !!!Wdlor"`;
- repeated spaces become `"  ab  cd "`;
- the mixed case becomes `"!9Az 0?b"`.

The commands and full final configurations are in the corresponding
`evidence/krun-*.log` files; the independent cross-check is
`evidence/concrete-result-check.log`.

Unicode concrete executions expose the material failure detailed in Stage 5.
The compact byte-level comparison is `evidence/unicode-byte-witness.log`.

### Every positive target claim

Each target was invoked independently from the fresh proof definition. The
helper claims were supplied as trusted only after their own independent
successful run:

| Target | Modular dependency | Result |
|---|---|---|
| `SPEC.insert-correct` | none | `#Top`, exit 0 |
| `SPEC.process-correct` | independently closed `insert-correct` | `#Top`, exit 0 |
| `SPEC.universal-correct` | independently closed helpers | `#Top`, exit 0 |
| `SPEC.example-hi` | independently closed helpers | `#Top`, exit 0 |
| `SPEC.example-hello` | independently closed helpers | `#Top`, exit 0 |
| `SPEC.example-prompt` | independently closed helpers | `#Top`, exit 0 |
| `SPEC.spaces-preserved` | independently closed helpers | `#Top`, exit 0 |

Exact commands, output, and status are preserved as
`evidence/kprove-<target>.log`. These fresh successes establish closure under
the submitted K theory; they do not validate that theory as Python semantics.

## 4. Adequacy and real-program pinning

### Plain-language claims

`insert-correct` has no `requires` clause. For any K strings `C`, `W`, and `B`,
any continuation `K`, any caller environment, and any current result, it says
that invoking the exact submitted `insert_char` body reaches
`val(refInsert(C,W,B)) ~> K`, restores the environment, preserves the function
table, and leaves the result cell unchanged.

`process-correct` analogously says that the exact `process_words` body, for any
`T`, `W`, and `R`, reaches `val(refProcess(T,W,R)) ~> K` with caller state
restored. It uses the independently closed insertion summary.

`universal-correct` has no domain guard. For every K `String S`, it starts from
the initial cells, runs `solutionProgram`, consumes `<k>`, installs the exact
function list, restores the empty environment, and changes `<result>` from
`""` to `antiShuffleSpec(S)`.

The four fixed claims make the same complete-state assertion for `"Hi"`,
`"hello"`, the prompt example, and the repeated-space example, with concrete
result strings.

### Program identity and control flow

The entry claims do not parse `solution.mpy` at proof time; they execute the
zero-argument function constant `solutionProgram`. Its two defining equations
expand to the complete constructor tree. A separate reviewer claim places the
trusted-translator constructor tree on the right of the same configuration
rewrite. It builds and closes with `#Top` in
`evidence/kprove-program-identity.log`; the literal is preserved in
`evidence/program-identity-spec.k`. Together with byte-identical translator
regeneration, this pins the named constant to the submitted program rather
than a substituted implementation.

The helper claims match real call control: function lookup, parameter binding,
body execution, nested recursive continuations, `returnValue`, and exact caller
environment restoration. Their arbitrary `K` is broad enough for the actual
recursive and caller suffixes, and the claim's destination retains rather than
discards that suffix. No ordinary operational bridge rewrites an invocation
directly to an oracle; the helper summaries are reachability claims proved
from the exact invocation states.

### Satisfying states and ground substitution

Every claim precondition is satisfiable:

- insertion: `C="a"`, `W="b"`, `B=""`, `K=.K`, `ENV=.Map`, result `""`;
- processing: `T="ba"`, `W=""`, `R=""`, `K=.K`, `ENV=.Map`, result `""`;
- universal entry: `S="ba"` and the explicit empty initial cells;
- each example: its displayed concrete initial configuration.

The ground reference results are
`refInsert("a","b","") = "ab"`,
`refProcess("ba","","") = "ab"`, and
`antiShuffleSpec("ba") = "ab"`. Fresh K, submitted Python, and canonical Python
all return `"ab"` for the entry witness; the fixed-entry results also match in
`evidence/concrete-result-check.log`.

Thus the claims are not free-variable, tautological, or one-way
result-unconstrained statements. Their weakness lies instead in what
`antiShuffleSpec` and the generated string semantics mean.

## 5. Rule-by-rule static soundness review

The exhaustive inventory, including every local syntax production, attribute,
configuration component, all 35 `semantic.k` rules, all 9 `verification.k`
rules, all 7 claims, construct coverage, guards, state footprints, and imported
primitive boundary, is in `evidence/rule-inventory.md`.

### Inventory summary

`semantic.k` has 13 syntax declaration groups, one four-cell configuration,
three local functions (`findFun`, `bindParams`, `appendStmts`), one local
`[total]` declaration (`bindParams`), and 35 ordinary rules. `verification.k`
adds five function symbols, three marked `[total]`, and nine defining rules.
`spec.k` has seven claims. There are no local `[functional]`,
`[simplification]`, `[concrete]`, priority, `[owise]`, macro, or explicitly
opaque declarations.

Every constructor in `solution.mpy` is declared and operationally covered:
module/function definitions, one- and three-parameter calls, statement lists,
`If`, `Return`, names/strings, string `+`, `==`, `<=`, index `0`, slice `[1:]`,
and the integer literals used as those bounds. Evaluation order is
left-to-right. Calls save and restore the caller environment; return discards
the remaining function body but preserves the caller continuation; the final
value alone writes `<result>`. Bool branch guards are disjoint and complete.
Function lookup and all recursive reference guards are disjoint and
descending on their used domains.

The program constant rules exactly describe the translated program.
`refInsert`, `refProcess`, and `antiShuffleSpec` have explicit, guarded,
recursive equations; they are not unconstrained result-bearing oracles. The
helper claims execute the real bodies to connect them to those references.

### Materially invalid used rules and witness

The defect is the interpretation of Python strings:

- semantic rule S22 (`semantic.k:115`) implements `s[i]` as
  `substrString(S,I,I+1)`;
- S24 (`semantic.k:119-120`) implements `s[i:]` with
  `substrString`/`lengthString`;
- S28 (`semantic.k:130`) then compares the extracted K byte fragments with
  `<=String`.

Those K primitives operate on the byte representation exposed by this
toolchain, while Python `str` indexes Unicode code points. The rules have no
ASCII guard, and `universal-correct` quantifies over an unrestricted K String.

Concrete false-result witness:

1. `krun` of the reviewer identity program with CLI input `"Ω"` returns
   `"\xce\xa9"` (`evidence/krun-unicode-identity.log`), establishing the input
   representation.
2. Fresh `krun` of the submitted program on the same input returns
   `"\xa9\xce"` (`evidence/krun-unicode-single-correct-quoting.log`).
3. Both trusted canonical and submitted Python return `"Ω"`.
   `evidence/unicode-byte-witness.log` records
   `identity_preserves_input=True`, `modeled_matches_identity=False`, and
   matching Python results.
4. `evidence/unicode-fidelity-spec.k` states the ground expected byte-preserving
   result. Its dry run builds successfully (exit 0), while the actual proof
   exits 1 with `WarnStuckClaimState` and residual `<result> "\xa9\xce"`;
   see `evidence/unicode-fidelity-build.log` and
   `evidence/unicode-fidelity-proof.log`.

This witness satisfies the formal entry precondition and the source signature.
The prompt does not restrict `s` to ASCII, and the trusted canonical provides a
normal result. The rules therefore enable a false observable conclusion about
the real Python execution on the intended string domain. The reference
functions share the same byte operations, so using them in the postcondition
causes the K proof to close rather than repairing the bridge.

### Other static findings

`bindParams [function,total]` is not globally covered: the grammar admits a
one-parameter/three-value mismatch and the converse, but no equation handles
either. `evidence/mismatched-arity.log` shows the resulting symbolic residual
for a ground mismatched program. The submitted program and every proof claim
always pair one with one and three with three, so this inaccurate totality
annotation is outside the actually used construct combinations and is not a
second verdict driver.

The K call stack is unbounded and the configuration has no exception state.
The 995/996 ASCII witness in `evidence/recursion-boundary.log` shows the real
CPython control difference. Treating resource limits abstractly can be a
declared partial-correctness boundary, but the candidate declares no such
boundary and its universal K state is not a complete model of real exceptional
execution.

Finally, no K claim proves that `refProcess(S,"","")` equals the canonical
split/sort/join property, even on ASCII. The reference is a faithful copy of
the submitted insertion algorithm under its own K operations. Examples and
finite Python differential evidence support the intent bridge; they do not
constitute a universal K theorem. Without the material semantics failure this
would be a documented `CONCERNS`-level limitation, not an oracle-soundness
failure.

## 6. Fresh non-vacuity test

No candidate `spec-vacuity.k` was supplied. The reviewer-created
`evidence/spec-vacuity.k` retains the exact two helper claims and adds a
satisfiable ground entry claim for input `"ba"` whose result obligation is
deliberately mutated from the true `"ab"` to false `"ba"`.

The mutation's `kprove --dry-run` compiles the spec and exits 0
(`evidence/vacuity-build.log`). The actual proof uses only the already
independently closed exact helper claims as trusted dependencies. It exits 1,
not by parser failure, timeout, or unrelated crash. The
`WarnStuckClaimState` residual has empty `<k>`, restored environment, and
actual `<result> "ab"`, which cannot unify with demanded `"ba"`; see
`evidence/vacuity-proof.log`.

The proof is therefore result-discriminating and non-vacuous. This passing
negative test does not cure the incorrect real-program semantics found in
Stage 5.

## 7. Proven versus assumed accounting

### Precisely what the successful reachability proof establishes

Conditional on the submitted K definition and K backend:

- exact modeled execution of `insert_char(C,W,B)` reaches the recursively
  defined K byte-string value `refInsert(C,W,B)` while restoring caller state;
- exact modeled execution of `process_words(T,W,R)` reaches
  `refProcess(T,W,R)` with the same restoration;
- modeled execution of the exact translated `solutionProgram` from its initial
  cells reaches `antiShuffleSpec(S) = refProcess(S,"","")` for arbitrary K
  `String S`;
- the four displayed concrete K examples have their displayed results.

The proof is partial-correctness reasoning through recursive circularities. It
does not prove CPython resource termination, and it does not independently
prove that the reference function means per-word Python sorting.

### Trust and assumption ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K v7.1.293 frontend, Haskell backend, reachability/circularity implementation | all `#Top` results | Ordinary unavoidable checker trust; version and commands are reproduced. |
| Imported Bool, Map, Int, and String hooks | semantics and reference equations | Ordinary low-level primitive trust. Their observed byte behavior is reproducible; using byte substring as Python code-point substring is the candidate's invalid bridge. |
| Trusted `py2mpy.py` transliteration | real-program AST identity | Acceptable and checked by byte regeneration plus the K identity claim. |
| Independently closed helper claims later passed with `--trusted` | process/universal/example modular runs | Acceptable modular proof boundary: exact source claims, commands, order, and prior `#Top` are preserved. |
| Candidate-generated MPY semantics models real Python | all claims as statements about `solution.py` | **Illegitimate.** Unicode byte-reordering and unmodeled reachable `RecursionError` supply concrete counterexamples. |
| `refProcess` equals the natural split/sort/join contract | interpretation of `universal-correct` | Not formally proved. Finite differentials and examples support only tested normal executions. |
| Independent Python differential | implementation-to-canonical evidence | Finite evidence only. It found eight recursion exceptions and cannot replace a K connection theorem. |

There are no fresh opaque program-derived result symbols and no task-answer
rewrite that bypasses the bodies. The failure is more fundamental: actual body
execution occurs under a materially wrong used language rule, and the
postcondition repeats that same wrong byte-level abstraction.

### Gate and decision accounting

- Real-program soundness (Gate A): **FAIL**. S22/S24/S28 have a concrete
  satisfying false-result witness; call/exception fidelity is also incomplete.
- Intent adequacy (Gate B): **FAIL**. The formal reference is not proved equal
  to canonical word sorting, and actual unrestricted Python behavior includes
  the documented Unicode and recursion discrepancies.
- Evidence auditability (Gate C): **PASS** for this audit. Reviewer scripts,
  complete deterministic inputs, exact commands, bounded outputs, exit
  statuses, and an evidence hash manifest are under `evidence/`.

The earliest failing gate controls the verdict. Fresh `#Top`, program identity,
and non-vacuity do not make a proof under materially invalid generated semantics
a legitimate proof of the real generated program.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
