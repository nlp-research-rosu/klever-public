# Independent adversarial audit: 124-valid-date

The candidate contains a legitimate, freshly reproducible partial-correctness
proof of the submitted program under the supplied MPY semantics. The result is
`CONCERNS / LEGIT`, not `PASS`, because the submitted program and proved
postcondition materially disagree with the trusted canonical Python function.
The disagreement is partly caused by an apparent operator-precedence defect in
the canonical implementation and partly by the candidate choosing a strict
ASCII, fixed-width reading of `mm-dd-yyyy`. The K theorem itself remains sound
and execution-sensitive.

## 1. Input and provenance integrity

The rendered mode is `SUPPLIED_SEMANTICS`. The trusted mount is consistent with
that mode: `/reference/reference-semantics` exists. There is no infrastructure
breach.

I treated all candidate reports, traces, logs, and compiled definitions as
untrusted claims. `run-input.json` identifies problem `124-valid-date`,
condition `kit-semantics`; `metrics.json` claims an exit-0 generation;
`codex-last.txt`, `codex-output.log`, and `PROOF.md` claim `VALIDATED` and
`KPROVE_PASSED`. The one JSONL trace contains 284 valid JSON records and no
parse error. None of those claims was used as proof evidence. The candidate's
`runtime-kompiled`, `verification-kompiled`, and `mutation-kompiled`
directories and all caches were ignored.

Integrity checks found:

- The candidate and trusted semantics trees have exactly the same directories,
  regular files, and bytes. `diff -qr --no-dereference` exited 0. Neither tree
  contains a symlink.
- Candidate [prompt.py](/candidate/prompt.py) is byte-identical to
  [the trusted prompt](/reference/prompt.py), SHA-256
  `71bb688d...2930b78`.
- Candidate [py2mpy.py](/candidate/py2mpy.py) is byte-identical to
  [the trusted translator](/reference/py2mpy.py), SHA-256
  `406485ea...664db16`.
- `run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`,
  `solution.py`, `solution.mpy`, `verification.k`, and `spec.k` are present as
  regular, non-symlink files. No required artifact is missing or mistyped.
- There are no changed, missing, additional, or symlinked entries inside
  `candidate/reference-semantics/`. Additional top-level candidate test files,
  reports, and compiled products are generated evidence, not additions to the
  required supplied-semantics tree.

All executable sources were copied to
`/tmp/audit-work/124-valid-date`; the trusted canonical, prompt, and translator
were copied into its `trusted/` subdirectory. All subsequent builds used those
scratch copies.

Evidence:
[integrity commands and hashes](/audit-output/evidence/01_integrity.log),
[full untrusted-log scan](/audit-output/evidence/01b_untrusted_claims.log).

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The trusted [prompt](/reference/prompt.py:2) asks for `valid_date(date)` on a
date string. A valid result requires a nonempty `mm-dd-yyyy` date, month
`1..12`, day `1..29` for February, `1..30` for April/June/September/November,
and `1..31` for the remaining months. No leap-year rule or numeric year range
is stated. A literal fixed-width reading makes the two month characters, two
day characters, and four year characters decimal digits with hyphens at
positions 2 and 5.

The trusted [canonical implementation](/reference/canonical.py:26) does not
implement that literal contract exactly:

- It calls `strip()`, then `split("-")` and `int`, so it accepts surrounding
  whitespace, variable-width and signed fields, spaces inside numeric fields,
  and Unicode decimal digits.
- Its unparenthesized conditions at
  [lines 32–36](/reference/canonical.py:32) are parsed using Python's `and`
  precedence over `or`. In particular,
  `if month == 2 and day < 1 or day > 29` rejects `day > 29` for *every*
  month. Thus canonical returns `False` for ordinary prompt-valid dates such
  as `01-31-2000`.

The submitted [solution.py](/candidate/solution.py:1) is a strict parser: it
requires length 10, ASCII digits at all eight digit positions, exact hyphens,
and the stated month/day bounds. It accepts February 29 for every four-digit
year, as the prompt requires.

### Translation identity

Running the trusted translator on the scratch copy produced
`solution.regenerated.mpy`; it is byte-identical to submitted
[solution.mpy](/candidate/solution.mpy), with matching SHA-256
`f7802bd0...b90e3b`. Python compilation also succeeded.

### Independent differential

The reviewer-authored differential imports the scratch copy of the trusted
canonical entry point and the scratch copy of the generated entry point. It
contains the five documented examples, empty and malformed strings, every
month/day boundary, position-wise separator/digit mutations, whitespace,
variable-width, signed and Unicode inputs, and all `00..99` month/day pairs for
years `0000`, `2000`, and `9999`. The deterministic input corpus is preserved
as [02_differential-inputs.json](/audit-output/evidence/02_differential-inputs.json).

Results over 30,054 inputs:

- Candidate versus a separately written literal prompt oracle: 0 mismatches.
- Candidate versus trusted canonical: 73 mismatches.
- All five documented examples agree.
- Fifty-four canonical mismatches occur even in the generated strict ASCII
  corpus, chiefly valid day-30/day-31 dates.

Material witnesses include:

| Input | Prompt reading | Candidate | Canonical |
|---|---:|---:|---:|
| `01-31-2000` | `True` | `True` | `False` |
| `04-30-2000` | `True` | `True` | `False` |
| ` 03-11-2000 ` | `False` under exact format | `False` | `True` |
| `01-01-000` | `False` under exact format | `False` | `True` |
| Arabic-Indic `٠٣-١١-٢٠٠٠` | ambiguous unless “digits” means ASCII | `False` | `True` |

This is not hidden by the test aggregate. The candidate follows the literal
natural-language format more closely than the canonical does, but it is not
behaviorally equivalent to the trusted canonical on the intended string
domain. That conflict is the principal reason for `CONCERNS`.

Evidence:
[differential source](/audit-output/evidence/02_differential.py),
[translation/differential command log](/audit-output/evidence/02_program_fidelity.log).

## 3. Clean proof reconstruction

K version 7.1.293 was available. I built distinct fresh definitions below
`/tmp/audit-work/124-valid-date`; no candidate-compiled definition was read or
reused.

The fresh LLVM command was:

```text
kompile /tmp/audit-work/124-valid-date/reference-semantics/semantics.k \
  --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/124-valid-date/runtime-fresh-kompiled
```

It exited 0. A reviewer-authored Python test file begins with the exact 40-line
submitted function (byte comparison exited 0), then exercises the examples,
empty and whitespace inputs, malformed digits/separators, and every material
month/day boundary. CPython exited 0; trusted translation exited 0; `krun`
exited 0 with `<k> .K </k>`, empty stack, `NoExc`, and exit code 0.

The fresh Haskell command was:

```text
kompile --backend haskell /tmp/audit-work/124-valid-date/verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/124-valid-date/verification-fresh-kompiled
```

It exited 0. Every positive target claim was then run independently:

| Command selection | Output | Exit |
|---|---|---:|
| `--claims SPEC.valid-date-non10` | `#Top` | 0 |
| `--claims SPEC.valid-date-ten` | `#Top` | 0 |
| full `--spec-module SPEC` | `#Top` | 0 |

The compiler warned about unused variables in supplied `strLt`. The LLVM build
also reported non-exhaustive supplied functions `mapStrVS`, `floorFI`, `toF`,
`ceilF`, `joinCodes`, and `valSeqAt`. None of those heads occurs on this
program's proof path; their trust status is accounted for in Stages 5 and 7.

One deliberately extra diagnostic in `03_reconstruct.sh` attempted to parse
the embedded K-rule term containing explicit `.Stmts` as standalone concrete
`.mpy`; the standalone parser rejected `.Stmts`, so that script's final
aggregate status is 1 even though all builds, concrete execution, and all
positive proofs succeeded. This parser-error probe is not used as evidence.
The corrected check removed only explicit empty-list terminals, parsed both
terms through the freshly built syntax, and obtained byte-identical KAST JSON
with SHA-256 `a92182c7...16cc7f`, exit 0.

Evidence:
[fresh reconstruction log](/audit-output/evidence/03_reconstruct.log),
[reviewer concrete source](/audit-output/evidence/03_concrete_tests.py),
[corrected parsed-AST identity log](/audit-output/evidence/03b_program_identity.log).

## 4. Adequacy and real-program pinning

The two entry claims in [spec.k](/candidate/spec.k:6) mean:

1. `valid-date-non10`: from the complete initial MPY state, load the submitted
   program, call `valid_date(str(CS))`, and return `false` whenever
   `isLen(CS) != 10`.
2. `valid-date-ten`: from the same initial state, call it on an arbitrary
   ten-code `IntSeq` and return exactly
   `validDate10(C0,...,C9)`.

The `<k>` source is `#loadAll(solutionProgram) ~> Call(...)`.
`solutionProgram` expands to a `Module(FuncDef(...))`; the corrected fresh KAST
comparison proves that this module is the same parsed AST as submitted
`solution.mpy`. There is no substituted helper body and no rule intercepting
the `Call`. Fixed supplied rules perform module binding, name lookup, callee
and argument evaluation, frame creation, parameter/local binding, all branch
execution, return, and frame pop.

There are no loop or helper reachability claims. The only two claims are the
entry claims above.

The returned value is not free or one-way constrained. The complete `<k>` cell
rewrites to literal `false` or to the Boolean function `validDate10`. The final
scope map is existential because module loading retains the function binding;
all other cells remain pinned: environment 0, scope allocator 1, empty heap,
heap allocator 0, empty stack, `noRet`, `NoExc`, and exit code 0.

Satisfying states and concrete substitutions:

- `CS = .IntSeq` satisfies `isLen(CS) != 10`; claimed, candidate, and canonical
  results are all `False`.
- The codes of `02-29-2000` satisfy the length-10 claim; formula, candidate,
  and canonical results are all `True`.
- The codes of `01-31-2000` satisfy the length-10 claim; formula and candidate
  are `True`, while canonical is `False`, exposing the intent conflict rather
  than a K pinning defect.
- `04-31-2000` and `01-01-20a0` satisfy the length-10 precondition and produce
  `False` from the formula and both Python implementations.

A fresh body-sensitivity check changed only the executable final
`day <= 31` branch to `day <= 30`, rebuilt the Haskell definition from source,
and tried to prove the original concrete `01-31-2000 => true` obligation. The
build exited 0; proof exited 1 with `WarnStuckClaimState` and residual
`<k> false ~> .K </k>`. Thus the result depends on the real body.

Evidence:
[claim witness substitutions](/audit-output/evidence/04_claim_witnesses.log),
[body mutation source claim](/audit-output/evidence/05_body_sensitivity_spec.k),
[body mutation command log](/audit-output/evidence/05_body_sensitivity.log).

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The reviewer inventory enumerates every configuration, context, syntax
declaration, function/total declaration, ordinary rule, priority/concrete/owise
attribute, and claim in the supplied semantics, `verification.k`, and `spec.k`.
It contains 942 declaration blocks:

| Boundary | Declarations |
|---|---:|
| Supplied semantics used by this program | 145 |
| Supplied semantics with unreachable rule patterns/declarations | 783 |
| Candidate-local syntax/function declarations and equations | 12 |
| Target claims | 2 |

There is no `[simplification]` rule and no `functional` declaration in the
candidate proof. Candidate-local code contains no priority rule, opaque symbol,
operational rewrite, circularity, or auxiliary claim. Every inventory row has
an explicit decision. Supplied-unreachable rows are retained as part of the
exact selected semantics but cannot match a term produced on this program's
well-sorted execution path; supplied-used rows are reviewed below.

The complete per-declaration record, including source line, attributes,
complete-block hash, normalized declaration, relevance, and decision, is
[05_rule_inventory.md](/audit-output/evidence/05_rule_inventory.md).

### Candidate-local declarations and equations

| Extension | Class, domain, and decision |
|---|---|
| `solutionProgram` | Definitional program-syntax constant. Its sole equation expands to the parsed submitted AST. It changes no cell and does not replace any execution step. Sound. |
| `asciiDigit(C)` | Total definitional Boolean `48 <= C <= 57`, one unconditional equation, no overlap. Correct for all integers. |
| `twoDigits(T,O)` | Total arithmetic definition `(T-48)*10+(O-48)`, one unconditional equation. It denotes the decimal value on the ASCII-digit guard used by `validDate10`; no claim treats non-digits as valid digits. |
| `maxDay(M)` | Total conditional: 29 for 2, 30 for 4/6/9/11, 31 otherwise. Branches are exhaustive; invalid months are separately rejected by `validMonthDay`. |
| `validMonthDay(M,D)` | Total conjunction of month `1..12`, day at least 1, and `D <= maxDay(M)`. Directly matches the literal prompt. |
| `validDate10(C0,...,C9)` | Total conjunction of exact separators, eight ASCII-digit checks, and `validMonthDay(twoDigits(...))`. It is the postcondition, not an operational rule. Fixed execution independently reaches the same Boolean. |

All six function symbols have one terminating, unconditional equation. There
are no pairwise overlaps or guard-coverage gaps. These equations do encode the
property to be proved, but they do not rewrite a `Call`, `Return`, frame,
continuation, binding, or state cell. The successful body mutation and failed
false-result mutation show they are not an execution-bypassing oracle.

### Used syntax and operational path

| Submitted construct | Declaration/rule path | Review |
|---|---|---|
| `Module`, `Stmts`, `FuncDef` | `syntax.k`; `core.k` `#loadAll`/statement sequencing; `functions.k` def rule | Loads the exact body into module scope 0 with builtin parent -1. |
| `Call`, `Name` | `call.k` callee then left-to-right argument evaluation; `core.k` scope walk | `valid_date` resolves in module scope; `len`, `ord`, and `int` resolve in `builtinsScope`. No local call interception exists. |
| `If`, `BoolOp`, `Compare` | strict/context rules in `syntax.k`, `controls.k`, `bool.k`, `operators.k`, `int.k`, `str.k` | Conditions evaluate before branches; `or` is left-to-right and short-circuiting. Invalid length returns before indexing; invalid character returns before `int`. |
| Integer/Boolean/string literals | `core.k`, `str.k` | All program literals are ASCII; `"-"` maps to code 45. |
| String index and slice | `subscript.k` index contexts, `intSeqAt`, `normIdx`, slice-bound evaluation, `buildIS` | Every index is in bounds after the length-10 guard. Slices `[0:2]` and `[3:5]` produce exactly two codes with step 1. |
| `len`, `ord`, `int` | `builtins.k` `seqLen/isLen`, one-character `ord`, digit fold | `ord` receives one-character indexed strings. The two `int` calls occur only on two ASCII digits and reduce to `twoDigits`. |
| `Assign` | strict RHS plus `controls.k` current-scope update | Writes only `month` and `day` in the fresh call scope. No heap allocation occurs. |
| `Return` | strict return expression, `functions.k` `#pop` | Abruptly discards the remaining function-body continuation, restores caller environment, empties the stack, resets return state and scope allocator. This is the fixed function semantics, not a proof bridge. |

Configuration/cell checks:

- Calls allocate a fresh scope at 1, push the caller continuation, and restore
  environment 0 and allocator 1 on pop. The callee scope is removed. The
  retained module scope explains the existential final `scopes` cell.
- Strings and integers are values; this program never allocates or mutates a
  heap object. `heap`, `heapLoc`, exception, and exit-code cells remain fixed.
- Relevant high-priority cell/dereference rules have false guards because no
  `cellRef`, heap `ref`, or `$cells` marker can occur. Unused priority rules for
  floats, MD5, collections, methods, and imports have nonmatching heads.
- The generic call rule is `[owise]`, but there is no candidate-local higher
  priority call rule. Supplied special-call rules also have nonmatching
  syntactic callees.
- The single-character and multi-character `int(str)` cases are disjoint by
  length on this path; integer comparison rules are disjoint by operator.

The supplied multi-character `int(str)` rule is deliberately over-broad
relative to CPython because it requires length at least 2 but does not itself
guard every code as a digit. A concrete model-gap witness is `int("ab")`:
the supplied fold would calculate `540`, whereas CPython raises `ValueError`.
This is not a candidate-local rule and cannot enable a false conclusion here:
the real program's preceding short-circuit digit branch makes such a call
unreachable. On its reachable domain of two ASCII digits, the rule is exact.
I therefore record a fixed-semantics trust limitation, not an unsound
candidate proof rule.

Likewise, the compiler's non-exhaustive totality warnings and every supplied
opaque float/sort/MD5 symbol are unreachable. No rule fabricates the task
answer, no used construct is silently unmodeled, and no false candidate-local
equation was found. Accordingly there is no claimed unsound candidate rule
requiring a false-conclusion witness.

Evidence:
[trust/attribute inventory](/audit-output/evidence/07_trust_inventory.log).

## 6. Fresh non-vacuity test

I did not reuse candidate `spec-vacuity.k`. The fresh mutation
[06_spec_false.k](/audit-output/evidence/06_spec_false.k) starts from the same
complete initial state, loads the exact program, calls
`valid_date("03-11-2000")`, and deliberately requires `false`.
`03-11-2000` is a concrete satisfying input and the true result is independently
confirmed by both Python implementations.

Results:

1. `kprove ... --dry-run` exited 0, so the mutation parsed and built against
   the fresh definition.
2. The real proof exited 1.
3. It emitted `WarnStuckClaimState`.
4. The semantic residual was `<k> true ~> .K </k>` while the destination
   required `false`.

This is the expected unmet result obligation, not a parser error, missing
import, timeout, unrelated crash, or unreachable mutation.

Evidence:
[mutation runner log](/audit-output/evidence/06_nonvacuity.log),
[raw failed proof output](/audit-output/evidence/06_false_proof_output.log).

## 7. Proven versus assumed accounting

### Precisely proven

Conditional on the K toolchain and the supplied MPY definition, the successful
reachability claims establish this partial-correctness statement about the
actual submitted `solution.mpy`:

- For every modeled finite `IntSeq` string of length other than 10, if the call
  terminates, it returns `false` and restores every observable machine cell
  fixed by the claim.
- For every modeled ten-code string, if the call terminates, it returns exactly
  the Boolean saying: positions 2 and 5 are code 45; the other eight positions
  are ASCII codes 48 through 57; the two-digit month is 1 through 12; and the
  two-digit day is within the prompt's 29/30/31 bound.

The K proof does not establish equivalence to `canonical.py`, total correctness,
correctness for non-string Python arguments, full CPython exception behavior,
or correctness of K/Kore/SMT implementations.

### Trust and assumption ledger

| Boundary | Role and dependents | Assessment |
|---|---|---|
| K 7.1.293 parser, compiler, Kore backend, SMT/implication engine | Parses, rewrites, simplifies, and checks both claims | Necessary low-level proof-checker trust; acceptable and freshly exercised. |
| K builtin theories | Used operations are `+Int`, `-Int`, `*Int`, integer comparisons/equality, `andBool`/`orBool`/`notBool`, `#if`, string equality and literal helpers, K equality, maps, map lookup/update/key membership, and list/continuation operations | Ordinary low-level mathematical/runtime primitives; acceptable. |
| Exact supplied MPY semantics | Defines strings, calls, scope/frame state, control, indexing/slicing, and builtins | Required fixed semantics. Used paths were statically audited and concretely exercised. Its broader CPython model is partial; the over-broad `int(str)` witness and unused totality warnings are documented concerns. |
| Trusted `py2mpy.py` | Bridges `solution.py` to submitted `solution.mpy` | Not proved correct generally. For this source, byte regeneration plus equal parsed KAST pins the exact translated artifact; acceptable finite/source-specific evidence. |
| Candidate-local property equations | Give names to the target Boolean | Formally part of the proof theory, but fully defined, non-overlapping, state-free, and independently matched to executed behavior. Acceptable; not opaque primitives. |
| Literal prompt interpretation | Treats `mm-dd-yyyy` as exactly ten ASCII characters | Informal intent bridge. Strongly supported by wording/examples, but Unicode/whitespace are not explicitly resolved and canonical behaves differently. This is concerning, not formally proved. |
| CPython canonical and reviewer prompt oracle | Finite intent/program comparison only | Empirical evidence, never a K premise. The canonical conflict is material and remains visible. |
| Termination | Kit reachability result is reported as partial correctness | Not claimed. The submitted code is loop-free, but no separate total-correctness theorem is asserted. |

The complete supplied opaque-symbol list is:

- Sort/digest: `sortVS`, `sortKeyVS`, `md5hexCodes`.
- Float-related: `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`,
  `floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`,
  `eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`,
  `roundFN`, and `sqrtF`.

All 25 are in the exact supplied baseline, none appears in the submitted
program, target claims, candidate-local equations, or any reachable proof
term. Partially defined supplied functions that can remain abstract outside
their constructor domains include `valSeqAt`; the compiler also warned about
`mapStrVS`, `joinCodes`, `floorFI`, `toF`, and `ceilF`. They have no dependent
claim here.

### Decision

The clean proof closes, the postcondition constrains the Boolean, the parsed
program is the submitted program, every candidate-local equation is sound, and
both result and body mutations fail for the expected semantic obligations.
That rules out `FAIL / NOT_LEGIT`.

The material canonical divergences rule out an unqualified `PASS`: a consumer
who treats the trusted canonical as the benchmark's behavioral authority would
not receive a proof of that function. Under the prompt's literal fixed-width
reading, however, the candidate program and theorem are correct. The honest
classification is therefore a legitimate proof with an intent/reference
concern.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
