# Independent adversarial review: 86-anti-shuffle

The candidate has a clean, non-vacuous K proof of an idealized unbounded-stack
string program, and its theorem is mechanically pinned to the submitted
`solution.mpy`. It is not a legitimate proof of the real generated Python
program over the unrestricted source-contract domain. The generated call
semantics omits CPython's recursion-depth exception and turns an actual
exceptional termination into a normal return. A valid 1,100-character input is
a concrete false-control/result witness: the trusted canonical returns, the
submitted Python raises `RecursionError`, and the candidate K semantics returns
normally. That material real-program mismatch determines the verdict.

All candidate files and generation records were treated as untrusted. All
compilation, execution, mutations, and generated artifacts were made below
`/tmp/audit-work/anti-shuffle`; no candidate-built definition was used.
Reviewer-authored scripts, mutations, and bounded logs are preserved in
[`/audit-output/evidence`](/audit-output/evidence).

## 1. Input and provenance integrity

Status: pass; there is no audit-infrastructure breach.

`/audit-input.json` declares `record_layout` =
`legacy-selected-stage1`, condition `bare`, problem
`86-anti-shuffle`, and `semantics_mode` = `GENERATED_SEMANTICS`.
The `container_paths` map, rather than the host-only provenance paths, was used.
The required generated-semantics condition is satisfied:
`/reference/reference-semantics` does not exist.

The independent checker and complete result are
[`provenance_check.py`](/audit-output/evidence/provenance_check.py) and
[`01-provenance.log`](/audit-output/evidence/01-provenance.log). In particular:

- `/audit-campaign-lock.json` is byte-hashed as
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  matching `/audit-input.json`, and its parsed object exactly equals the
  `audit_campaign` block.
- Every required legacy-selected-stage1 record is readable and regular:
  `/run.json`, `/task.json`, `/generation-result.json`,
  `invocation.json`, `metrics.json`, `codex-last.txt`,
  `codex-output.log`, `prompt.txt`, and the structured trace. The optional
  `usage.json` is present and was inspected. Historical
  `runtime-metrics.json` is absent, which is allowed for this record layout.
- Every recorded regular-file hash checked in `01-provenance.log` matches,
  including the run/task/result/invocation manifests, prompt, usage, metrics,
  output log, final response, canonical, translator, and trace JSONL.
- A fresh pipeline tree hash of `/candidate` is
  `af433c2e0f692229c66678a02091f50d6ddc98cb88ea39109cfdd636ed885b36`;
  it matches the stage-one output, retained-workspace, and result records.
  A fresh tree hash of the trace is
  `a1f148d332b4e91c5a81c9470caa1ed3eaaa7fc14d9dfbde3783ae2ba9090bbe`;
  it matches `usage.json`, while the single JSONL's byte hash separately
  matches the invocation/result evidence manifest.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to
  `/reference/prompt.py` and `/reference/py2mpy.py`.
- The candidate, generation evidence, and trusted-reference trees contain no
  symlinks or unsupported node types. All six required proof artifacts
  (`solution.py`, `solution.mpy`, `semantic.k`, `verification.k`, `spec.k`,
  and `prove.sh`) are regular files.

For the structured trace, the reviewer parsed all 320 JSONL records, found zero
malformed records, inventoried all 64 tool calls and all messages, and treated
their contents only as historical claims. See
[`inspect_generation_trace.py`](/audit-output/evidence/inspect_generation_trace.py)
and [`02-generation-trace.log`](/audit-output/evidence/02-generation-trace.log).
The generation report's `#Top` and “2,000 tests” claims were not used as proof
evidence.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The trusted prompt requires `anti_shuffle(s)` to retain the order of
space-delimited words and every space, while sorting the characters within each
word in ascending character/ASCII order. The trusted canonical is:

```python
return ' '.join([''.join(sorted(list(i))) for i in s.split(' ')])
```

There is no length bound or recursion-related precondition in the trusted
contract.

The submitted program implements insertion into a current word through
`insert_char`, then scans the string through `process_words`. Its ordinary
algorithm agrees with the canonical: spaces close the current word and are
copied exactly; a non-space character is insertion-sorted into that word.

### Translation identity

The trusted translator was run from scratch:

```text
python3 trusted/py2mpy.py solution.py > regenerated.mpy
cmp -s regenerated.mpy solution.mpy
```

Both files hash to
`5fa1095ee5d5321e42f438e9e860c1c09fc314c86c7233f5421db4cef89931df`,
and `cmp` exits zero. See
[`03-regenerate-mpy.log`](/audit-output/evidence/03-regenerate-mpy.log).

### Independent differential testing

[`differential_test.py`](/audit-output/evidence/differential_test.py) imports
the trusted canonical and submitted generated entry point by independent file
paths. It exercises:

- all three documented examples;
- empty, one-character, one-space, leading/trailing/repeated-space cases;
- each `insert_char` and `process_words` branch boundary;
- punctuation, NUL, tabs/newlines, BMP, combining, and astral Unicode;
- every string of length 0 through 5 over `" ab!"`; and
- 3,000 deterministic generated strings of length 0 through 100.

Those 4,381 normal cases have zero mismatches. The same script includes five
recursion-stress cases. Three valid cases diverge because the submitted Python
raises `RecursionError` while the canonical returns. The shortest recorded
stress divergence is an ascending 500-character word; a repeated
1,100-character word also diverges. The script correctly exits 1 because it
does not hide those mismatches. Complete results are in
[`04-differential.log`](/audit-output/evidence/04-differential.log).

This is not merely an inability to establish termination. In the actual
CPython execution, the exceptional control path terminates by raising, while
the generated K semantics produces a normal value for the same input, as
demonstrated independently in stages 3 and 5.

## 3. Clean proof reconstruction

The observed toolchain is K `v7.1.293` and Python `3.10.12`
([`05-toolchain.log`](/audit-output/evidence/05-toolchain.log)).

### Fresh builds

The concrete definition was freshly compiled from `semantic.k`:

```text
kompile semantic.k --backend llvm --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-semantics-kompiled
```

It exits zero. The compiler emits one relevant warning: the
`[function,total]` declaration of `bindParams` is non-exhaustive for a
one-parameter `Params` paired with three `vals`. This is addressed in stage 5.
See [`06-build-concrete.log`](/audit-output/evidence/06-build-concrete.log).

The proof definition was freshly compiled from `verification.k`:

```text
kompile verification.k --backend haskell --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
```

It exits zero with no output; see
[`08-build-proof.log`](/audit-output/evidence/08-build-proof.log).

### Concrete generated-semantics execution

Fresh LLVM execution covers empty input, a single space, all examples,
repeated/edge spaces, both character-order branches, punctuation/digits, and
Unicode. Every ASCII/space case finishes with the same result as both Python
implementations. Commands, exit statuses, and final configurations are in
[`07-concrete-cases.log`](/audit-output/evidence/07-concrete-cases.log).

There is a separate K String/backend limitation. Configuration-variable
injection of characters above Latin-1 is byte-oriented in these concrete runs:
for `éA Ωβ`, `krun` prints
`"A\xe9 \xa9\xb2\xce\xce"` instead of Python's `"Aé Ωβ"`. The installed K
String documentation expressly says support beyond the first 256 code points
is incomplete
([`22-k-string-doc.log`](/audit-output/evidence/22-k-string-doc.log)).
Haskell proof-backend probes using in-file escaped K literals nevertheless
prove identity, Greek code-point order, and astral code-point order
([`15a-unicode-identity.log`](/audit-output/evidence/15a-unicode-identity.log),
[`18a-unicode-greek-proof.log`](/audit-output/evidence/18a-unicode-greek-proof.log),
and
[`18b-unicode-astral-proof.log`](/audit-output/evidence/18b-unicode-astral-proof.log)).
Because the formal Haskell probes produce the intended results, this review
records the concrete-input/backend discrepancy as a trust/evidence limitation,
not as an additional false-rule finding.

The decisive long-input witness is separate and ASCII-only. The fresh LLVM
semantics returns normally for `"a" * 1100`; the canonical returns the same
1,100 characters; the submitted Python raises `RecursionError`. All three
outcomes and their hashes are in
[`21-long-input-semantics.log`](/audit-output/evidence/21-long-input-semantics.log).

### Every positive target claim

The candidate has seven claims. They were reconstructed through the candidate's
three modular proof stages:

| Target set | Assumed only after independent closure | Result |
|---|---|---|
| `SPEC.insert-correct` | none | exit 0, `#Top` |
| `SPEC.insert-correct,SPEC.process-correct` | `SPEC.insert-correct` | exit 0, `#Top` |
| all remaining claims (universal plus four examples) | both helper claims | exit 0, `#Top` |

Exact evidence:
[`09-proof-insert.log`](/audit-output/evidence/09-proof-insert.log),
[`10-proof-process.log`](/audit-output/evidence/10-proof-process.log), and
[`11-proof-remaining.log`](/audit-output/evidence/11-proof-remaining.log).
Thus clean reconstruction itself passes. The adverse verdict is based on what
that reconstructed theory models, not on a failed or missing proof run.

## 4. Adequacy and real-program pinning

### Claims in plain language

- `insert-correct` has no `requires` clause. For any K strings `C`, `W`, and
  `B`, any caller environment, and any continuation, invoking the exact
  `insert_char` binding reaches `val(refInsert(C,W,B))`, restores the
  environment, and preserves the continuation.
- `process-correct` likewise says every exact `process_words(T,W,R)` invocation
  reaches `val(refProcess(T,W,R))`; it uses the independently closed insertion
  claim.
- `universal-correct` has no precondition beyond `S:String`. From the concrete
  initial configuration—empty function and environment cells and empty result—
  `run(solutionProgram,S)` must consume the computation and put
  `antiShuffleSpec(S)` in `<result>`.
- The remaining claims instantiate the exact program on `"Hi"`, `"hello"`,
  `"Hello World!!!"`, and `"  ba  dc "`, with exact result strings.

Every entry precondition is satisfiable. For example, `S = "hello"` with the
literal initial cells is such a state; both Python implementations and fresh K
execution return `"ehllo"`. Empty string and `"  ba  dc "` provide boundary
witnesses as well.

### Mechanical program identity

The proof does not read `solution.mpy`; it embeds a named constructor constant.
That maintenance choice is not itself a defect. The independent checker
extracts the `solutionFunctions` right-hand side, normalizes only `.Stmts` to
the blank external spelling of the same generated list unit, parses both
programs with `kast`, and compares their complete JSON constructor trees.
The result is `constructor_ast_equal=True`:
[`pinning_check.py`](/audit-output/evidence/pinning_check.py) and
[`17-pinning.log`](/audit-output/evidence/17-pinning.log).

Thus `<k> run(solutionProgram,S)` executes the same three bindings, names,
parameters, bodies, argument nesting, operators, indices, and slices as the
trusted regeneration of submitted `solution.py`. It is not a substituted
program.

### Body sensitivity

The reviewer changed the *executed proof term*, not merely external
`solution.py`: the embedded `anti_shuffle` body was mutated to
`Return(Str(""))`. The mutated definition builds successfully, but the
universal claim fails with `WarnStuckClaimState` and the unmet condition
`"" == refProcess(S,"","")`. See
[`verification-body-mutated.k`](/audit-output/evidence/verification-body-mutated.k),
[`19a-build-body-mutant.log`](/audit-output/evidence/19a-build-body-mutant.log),
and
[`19b-prove-body-mutant.log`](/audit-output/evidence/19b-prove-body-mutant.log).
This confirms genuine body dependence.

### Fatal adequacy gap

The entry theorem admits every K string and has no maximum-length or
normal-termination precondition. The generated semantics' invocation rules
permit unbounded recursive calls and have no recursion-depth or exception
state. Consequently the semantics executes `"a" * 1100` to a normal result,
where the actual submitted CPython function terminates exceptionally.

The false conclusion witness is:

```text
S = "a" repeated 1100 times
trusted canonical: normal return, length 1100
submitted solution.py: raises RecursionError
fresh candidate K semantics: normal return, length 1100
```

This changes call/return control and the observable outcome on a satisfying,
unrestricted-contract input. It is not an excluded nontermination case, and
the source contract supplies no bound that would remove the witness. The proof
therefore establishes a theorem about an idealized unbounded-stack substitute,
not partial correctness of the real generated program over the full contract
domain.

## 5. Rule-by-rule static soundness review

The complete inventory of every local syntax production, attribute,
configuration component, semantic rule, proof equation, and claim is
[`rule-inventory.md`](/audit-output/evidence/rule-inventory.md). It enumerates:

- 14 syntax/configuration groups in `semantic.k`, including every one of the
  20 continuation `KItem` constructors;
- all 35 rules in `semantic.k`, individually identified as R01–R35;
- all five proof-local function declarations and all nine equations in
  `verification.k`, identified as V01–V09; and
- all seven claims in `spec.k`, identified as C01–C07.

There are no local simplification, `functional`, `concrete`, `owise`, priority,
anywhere, or opaque-result declarations.

### Construct coverage and ordinary rules

Every constructor in `solution.mpy` is declared and has operational behavior:
`Module`, statement lists, `FuncDef`, `Return`, `If`, one/three parameters,
`Name`, `Str`, `Int`, string `BinOp("+")`, two-way `Compare`, indexing,
open-ended slicing, and one/three-argument named calls. The concrete cases
exercise every submitted branch.

R01–R02 implement ordered function lookup. Although this would choose the
first duplicate definition rather than Python's final rebinding, the exact
submitted module has three unique names, so no input reaches that discrepancy.
R03–R06 correctly bind matching arities and append statement lists. R07 loads
the exact definition list. R08–R10 implement function lookup, environment
replacement/restoration, and return to the caller. R11–R15 correctly discard a
function body's remainder after return and preserve it after a false/empty
conditional branch. R16–R28 implement left-to-right literal/name, string
addition, valid indexing/slicing, and comparison. R29–R34 preserve Python's
left-to-right argument evaluation for the exact statically unshadowed calls.
R35 updates `<result>` only after a top-level `val` has no continuation.

All used indices are valid: `text[0]` and `word[0]` occur only on the
nonempty branch, and both open-ended slices start at one. There is no mutable
heap, assignment, I/O, closure, or allocation behavior in the submitted
program, so the absence of those constructs is acceptable minimal coverage.

The material unsound abstraction is specifically R08–R10 together with a
configuration that has no stack-depth/exception component. Their complete
match domain accepts every recursive invocation regardless of current depth.
On the 1,100-character witness they enable a normal return, whereas the real
execution raises. This is the required concrete false-control/result witness
on the intended input domain.

### Functions, overlaps, and totality

`solutionProgram` and `solutionFunctions` are zero-argument total definitional
constants and are constructor-exact. `refInsert` has three disjoint/exhaustive
guards (empty word, nonempty/insertion point, nonempty/recurse) and its
recursive case shortens `WORD`. `refProcess` has three disjoint/exhaustive
guards (empty text, leading ASCII space, leading non-space) and shortens
`TEXT`. `antiShuffleSpec` is a covered one-equation total wrapper. No proof
equation overlaps inconsistently.

`bindParams` is declared `[total]`, but only the one/one and three/three
equations exist. The compiler's concrete witness is
`bindParams(Params("p"), vals("a","b","c"))`, for which no equation applies.
The declaration is therefore globally over-broad. No source string can create
that mismatched arity: the exact one-argument function is always called with
one value and both exact three-argument functions with three. Because there is
no witness through an entry precondition and no demonstrated false entry
conclusion from this attribute, this review records it as a non-fatal
off-path totality defect rather than using it as the verdict's unsoundness
claim.

### Proof-extension classification

`solutionProgram`/`solutionFunctions` are definitional constants, not execution
bridges. `refInsert`, `refProcess`, and `antiShuffleSpec` are result-bearing
definitional summaries. No semantic rule rewrites an invocation or expression
directly to one of them. Instead, C01 connects the exact fixed-semantics
`insert_char` execution to `refInsert`; C02 connects exact `process_words`
execution to `refProcess` using the already established C01; C03 executes the
exact `anti_shuffle` body using both. The same symbol is not injected by an
operational oracle. The body mutation confirms this separation.

The informal remaining intent bridge is that `refProcess(S,"","")`, with
`refInsert`, denotes split-on-ASCII-space insertion sorting. Its equations make
that interpretation transparent, and the broad finite differential supports
it, but there is no separate machine-checked sortedness/permutation theorem.
Standing alone this would be a documented `CONCERNS`-level limitation, not the
fatal issue.

## 6. Fresh non-vacuity test

The reviewer-authored mutation changes the concrete `"hello"` result obligation
from the true `"ehllo"` to false `"ehllp"`:
[`spec-vacuity-audit.k`](/audit-output/evidence/spec-vacuity-audit.k).

It builds successfully under:

```text
kprove spec-vacuity-audit.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC-VACUITY-AUDIT --dry-run
```

The dry run exits zero
([`20a-vacuity-build.log`](/audit-output/evidence/20a-vacuity-build.log)).
The actual proof exits 1 with `WarnStuckClaimState`; its final reachable
configuration contains `<k> .K </k>` and `<result> "ehllo" </result>`, which
does not unify with the false destination
([`20b-vacuity-proof.log`](/audit-output/evidence/20b-vacuity-proof.log)).
This is the expected unmet result obligation, not a parser error, timeout,
unreachable mutation, or unrelated crash. Non-vacuity passes.

## 7. Proven versus assumed accounting

### What the successful K proof establishes

Under the candidate's K definition and the Haskell backend's K builtins:

1. exact `insert_char` execution refines `refInsert` for all formal K strings;
2. exact `process_words` execution refines `refProcess` for all formal K
   strings, assuming the separately proved insertion claim;
3. exact `anti_shuffle` execution from the modeled initial configuration
   refines `antiShuffleSpec` for every formal K string, assuming the two
   separately proved helper claims; and
4. the four concrete example results follow.

This is result-constraining, non-vacuous, body-sensitive, and pinned to the
regenerated constructor program. As specified by the Kit workflow, it is a
partial-correctness result under the supplied theory; it does not prove
termination.

### Trust and assumption ledger

| Boundary | Influence | Assessment |
|---|---|---|
| K compiler, Haskell prover, reachability/circularity implementation | All proof closure | Ordinary foundational trust boundary. |
| K `String`, `Bool`, `Int`, list, and `Map` hooks/equations | Branches, slicing, comparison, concatenation, environments, results | Acceptable for ordinary formal strings, but K's documented Unicode/backend inconsistency limits concrete auditability beyond Latin-1. |
| Trusted `py2mpy.py` and CPython AST parsing | Source-to-constructor identity | Strongly supported: candidate translator is trusted-byte-identical and regeneration is byte-identical. |
| Manual `solutionFunctions` embedding | Program identity | Mechanically discharged by constructor-AST comparison; body sensitivity also passes. |
| C01 and C02 handed to later invocations through `--trusted` | C02 and C03–C07 | Acceptable modular handoff because each assumed claim first independently exits 0 with `#Top`. |
| `refInsert`/`refProcess` meaning “sort each ASCII-space word” | Human-facing postcondition | Transparent but informal; 4,381 normal differential cases support it, not prove it. |
| `[total] bindParams` | Function-definedness reasoning | Over-broad off-path declaration; no entry-domain false conclusion demonstrated. |
| Unbounded call depth and absence of exceptions | Control and final result for long valid inputs | Illegitimate for the claimed real Python program: the 1,100-character witness demonstrates a false normal return. |
| Python differential tests | Canonical/generated implementation bridge | Finite evidence only. They also expose, rather than hide, the fatal recursion mismatch. |

### Gate and decision accounting

- Clean verification: pass. All positive claims freshly close.
- Real-program soundness: fail. The call/return model changes a reachable
  exceptional execution into a normal result on an unrestricted valid input.
- Intent/domain adequacy: fail. The trusted contract has no length bound; the
  proof can only be interpreted as covering an idealized unbounded-stack
  substitute.
- Non-vacuity and program identity: pass.
- Evidence auditability: pass with documented K Unicode/backend and informal
  specification-meaning limitations.

Per the benchmark's decision boundary, materially changing the real program's
behavior or silently excluding a material part of the unrestricted
source-contract domain is `FAIL / NOT_LEGIT`, even when the narrower/idealized K
theorem is internally non-vacuous and reconstructs to `#Top`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
