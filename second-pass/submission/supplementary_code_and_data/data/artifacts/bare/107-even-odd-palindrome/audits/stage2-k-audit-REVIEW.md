# Independent adversarial review: 107-even-odd-palindrome

The candidate contains a legitimate proof for the complete HumanEval contract
domain. I rebuilt both definitions from source, reran the only positive claim,
checked the executed constructor term against trusted regeneration, reviewed
every local K declaration and rule, and ran two independent negative
sensitivity tests. The positive proof printed `#Top` with exit 0. Both
deliberately false mutations built successfully and then failed on the expected
reachable result mismatch.

## 1. Input and provenance integrity

The launcher declares `record_layout = legacy-selected-stage1` and
`semantics_mode = GENERATED_SEMANTICS`. The generated-semantics boundary is
internally consistent: `/reference/reference-semantics` is absent, so no hidden
or supplied semantics was sought or used.

I read `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
`/task.json`, `/generation-result.json`, and all records required for the
legacy-selected layout:

- `/generation-evidence/invocation.json`
- `/generation-evidence/metrics.json`
- `/generation-evidence/codex-last.txt`
- `/generation-evidence/codex-output.log`
- `/generation-evidence/prompt.txt`
- `/generation-evidence/codex-trace/**`

`usage.json` is present and was also inspected. `runtime-metrics.json` is
absent, which is permitted for this historical layout and was not
reconstructed. Every required record is a real regular file, not a symlink,
and every JSON/JSONL record parses. The structured trace contains 227 valid
records. The campaign-lock JSON is structurally identical to the embedded
`audit_campaign` block, and its SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
exactly the recorded value.

All directly framed hashes in `/audit-input.json` match the mounted bytes:
run/task/result/invocation/metrics/usage, prompt, output log, last message,
canonical source, trusted prompt, and trusted translator. Every per-file
generation-evidence hash in `/generation-result.json` also matches. Independent
length-delimited tree hashing matches the retained workspace digest
`ff8e1668...b9d0d` and trace digest `f2f3d99f...8e392` recorded by the
generation pipeline. The separate audit aggregate values were read as well;
`audit-input.json` does not declare their distinct aggregate framing, so
content integrity was checked through the direct hashes, per-file manifest,
and pipeline tree digests rather than assuming a framing.

`/candidate/prompt.py` is byte-identical to `/reference/prompt.py`, and
`/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`. Neither the
candidate nor trusted reference contains a `reference-semantics` tree. The
candidate and trace trees contain no symlink or unsupported entry. All required
candidate proof sources (`solution.py`, `solution.mpy`, `semantic.k`,
`verification.k`, `spec.k`, and `prove.sh`) are present.

I treated the generation transcript's `KPROVE_PASSED` statement only as an
untrusted historical claim. `evidence/02-generation-trace-summary.log`
documents the complete trace read and its bounded action summary; it was not
used as proof evidence. Detailed integrity results and the reviewer script are
in `evidence/01-integrity.log` and `evidence/integrity_check.py`.

Stage 1 result: pass; no infrastructure breach or provenance defect.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract says: for an integer `n` satisfying `1 <= n <= 1000`,
return `(E, O)`, where `E` and `O` are respectively the counts of even and odd
base-10 palindromic integers in the inclusive range `1..n`. The examples are
`3 -> (1,2)` and `12 -> (4,6)`. The trusted canonical implementation tests
decimal-string reversal while enumerating `1..n`.

The candidate uses a different but valid constant-time arithmetic algorithm.
It counts one-digit palindromes directly, two-digit palindromes as multiples of
11 with parity determined by their repeated digit, and three-digit
palindromes as `101*lead + 10*middle`. Its special `n=1000` path includes all
three-digit palindromes and correctly adds none for 1000 itself.

I regenerated the IR in scratch with the trusted translator:

```text
python3 py2mpy.py solution.py > solution.regenerated.mpy
cmp -s solution.regenerated.mpy solution.mpy
```

Both commands exited 0. The files are byte-identical and share SHA-256
`60d5919f4357b108abed4936a847fbd0492c2cdfb52877036400e5c45a1f60d4`;
see `evidence/03-translation-identity.log`.

The independent differential script imports the trusted canonical entry point
and candidate entry point from their mounted paths. It also uses a separately
written direct decimal-palindrome enumerator. It checks both documented
examples, the adjacent empty-range case `0`, explicit branch boundaries, 64
seeded generated values, and every intended input `1..1000`. All 1,001 unique
inputs agreed, including `1`, `9/10`, `100/101`, `109/110`, `110/111`,
`120/121`, `201/202`, `999/1000`; mismatch count was zero. The complete scope,
script, command, selected outputs, digest, and exit 0 are in
`evidence/differential_test.py` and `evidence/04-differential.log`.

Stage 2 result: pass; the generated implementation is faithful on the entire
source-contract domain.

## 3. Clean proof reconstruction

All source artifacts needed for execution were copied to
`/tmp/audit-work/reconstruction`. No candidate-built definition or cache was
copied or reused. The installed independent toolchain is K v7.1.293; version
and executable evidence is in `evidence/00-toolchain.log`.

I rebuilt the generated semantics from `semantic.k` with the LLVM backend:

```text
kompile --backend llvm semantic.k --main-module MPY \
  --syntax-module MPY-SYNTAX --output-definition concrete-kompiled
```

It exited 0 (`evidence/05-kompile-concrete.log`). The warnings concern
deprecated empty-K spelling, unused pattern variables, and the old
zero-argument `symbol` attribute; none changes rule meaning or indicates an
unmodeled used construct.

I then concretely ran the trusted-regenerated `solution.mpy` through this fresh
definition for 20 normal and boundary inputs:

```text
krun solution.mpy -cN=<n> --definition concrete-kompiled --output pretty
```

All runs exited 0, returned a fully reduced `VTuple`, restored `noReturn`, and
matched independent Python. This set exercises every used statement form,
operator, comparison, and both sides of every material branch, including the
`lead > 9` path at 1000. See `evidence/concrete_semantics_test.py` and
`evidence/06-concrete-semantics.log`.

I separately rebuilt `verification.k` with Haskell:

```text
kompile --backend haskell verification.k --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX --output-definition proof-kompiled
```

That exited 0 (`evidence/07-kompile-proof.log`). `spec.k` contains exactly one
positive claim. Independently running it:

```text
kprove spec.k --definition proof-kompiled \
  --spec-module SPEC --warnings none
```

printed `#Top` and exited 0. The complete bounded result is
`evidence/08-kprove-positive.log`.

Stage 3 result: pass; the sole positive target claim closes from a genuinely
fresh source build.

## 4. Adequacy and real-program pinning

### Entry claim in plain language

The claim has no symbolic variable or `requires` clause. Its precondition is
the single literal, realizable state

```text
<k> verifyRange(solutionProgram, 1, 1000, 0, 0) </k>
<env> .Map </env>
<return> noReturn </return>
```

Its postcondition is the exact terminal `<k>` term `verified`, with the
environment again empty and the return state again `noReturn`. Thus the
precondition is plainly satisfiable: it is the initialized configuration
displayed above.

`verifyRange` does not assert a free result. For each concrete `N` from 1
through 1000 it places `run(solutionProgram,N)` at the front of `<k>`. Normal
program execution must return a tuple exactly matching the accumulated
digit-reversal oracle through `N`; only the exact rule
`VTuple(VInt(E),VInt(O)) ~> expect(E,O)` lets the range advance. At `N=1001`,
and only then, the harness rewrites to `verified`. A wrong even component or
wrong odd component is a stuck state, as the negative tests demonstrate.

There are no helper or loop claims to assume. The finite `verifyRange` control
flow is defined by ordinary semantic rules and is fully executed by the sole
claim. A ground enumeration is adequate here because the source contract
itself has exactly 1,000 admissible integer inputs; this is not a bounded
substitute for an unrestricted domain.

### Mechanical program pinning

Pinning has three independent links:

1. trusted regeneration is byte-identical to submitted `solution.mpy`;
2. a reviewer-authored constructor parser normalizes only the two textual
   spellings of an empty statement list and finds the `solutionProgram` RHS
   exactly equal to the submitted module AST, with identical normalized hash
   `74793e09...7edceb`; and
3. the `run` semantic rule matches the exact function name and parameter,
   installs `n`, and executes that exact `BODY` through the normal statement
   rules.

The constructor comparison is in `evidence/program_term_compare.py` and
`evidence/09-program-term-identity.log`. The manual duplication of the module
term in `verification.k` creates a maintenance risk for future edits, but it is
not a defect in this immutable candidate because trusted regeneration and the
mechanical comparison establish exact identity.

Concrete substitutions also agree across all relevant layers:

| Scheduled input | Fresh K result | Candidate Python | Canonical Python |
|---:|---:|---:|---:|
| 1 | `(0,1)` | `(0,1)` | `(0,1)` |
| 12 | `(4,6)` | `(4,6)` | `(4,6)` |
| 1000 | `(48,60)` | `(48,60)` | `(48,60)` |

For body sensitivity, I changed the executed `solutionProgram` constructor term
itself from `even = 4` to `even = 5`, rebuilt the mutated Haskell definition
successfully, and reran the original claim. It exited 1 with
`WarnStuckClaimState` at `n=10`, showing actual `(5,5)` followed by
`expect(4,5)`. The exact mutation and logs are
`evidence/11-body-mutation.patch`,
`evidence/11-body-mutation-build.log`, and
`evidence/12-body-mutation-kprove.log`.

Stage 4 result: pass; the theorem is result-constraining and pins the actual
trusted-regenerated program.

## 5. Rule-by-rule static soundness review

`evidence/10-rule-inventory.md` is the exhaustive inventory. It enumerates
every local syntax production, constructor/opaque marker, configuration cell,
K function declaration, guarded equation, and operational rule in
`semantic.k` and `verification.k`, plus the sole claim. There are no candidate
helper K files. There are no `[total]`, `[functional]`, simplification,
priority, `owise`, macro, fresh-symbol, anywhere, or proof-module lemma
declarations.

### Used-construct coverage

Every constructor in `solution.mpy` is declared and modeled:

- `Module`/`FuncDef`/`Params` are selected by the exact `run` entry rule.
- Juxtaposed statement lists are consumed by the assignment, conditional,
  return, empty-list, and returned-state rules.
- `Int`, `Name`, `BinOp`, `Compare`, and `TupleExpr` are handled by `eval`.
- All used operations have explicit equations: `+`, `-`, `*`, `//`, `%`,
  `<`, `<=`, `>`, `>=`, and integer `==`.
- The three cells model precisely the state used here: computation, local
  bindings, and function return/control. This pure function uses no heap,
  allocation, I/O, exception, closure, or external-state construct.

The semantics intentionally covers only this translator subset, which is
permitted in generated-semantics mode. Unsupported unused Python constructs
remain visibly unmodeled rather than receiving a catch-all result.

### Operational fidelity

Integer literals and locals reduce to typed values. Assignment evaluates its
pure RHS in the old environment, updates one local, and continues with the
exact tail. The true and false `If` rules have complementary guards and
preserve the same continuation. An early return drops the current list and the
returned-state rule drops any separately scheduled outer suffix; `finish`
exposes the exact recorded value and resets return state. This matches the
actual control flow, including the early `n < 10` return.

All reachable integers and intermediates are nonnegative, and every division
or modulus divisor is a positive literal, so K `/Int` and `%Int` agree with
Python `//` and `%` on the theorem domain. Expression evaluation is pure, so
using recursive functions for operands cannot hide a stateful evaluation-order
difference. Every local read is preceded by an assignment on its reachable
branch.

Operator equations are disjoint by literal operator. The two conditional rules
are Boolean complements. Statement heads or return-state guards are disjoint;
the benign overlap between empty `exec` and returned-state `exec` has the same
RHS. Map lookup selects the unique binding. There is no rule that fabricates a
result for an unsupported used term.

### Proof-local mathematics and harness

`solutionProgram` is a concrete data alias, not an execution bridge.
`reverseDigits` has four disjoint cases covering exactly 1..1000:
one digit, two digits, three digits, and 1000. Each equation is the elementary
base-10 reversal formula and handles zeros correctly. The positive and
negative `evenPalindrome` guards are complements, as are the odd guards. For
positive integers, parity is exactly 0 or 1 modulo 2.

The active `verifyRange` rule does not replace program execution: it schedules
`run(P,N)` before an exact `expect`. The completion guard `N > MAX` is
disjoint from the active `N <= MAX` guard. The `expect` rule is proof-harness
cleanup after normal return; it matches only both required components and
cannot introduce an opaque result. Its arbitrary environment reset is
intentional between independent top-level calls and cannot bypass the tuple
check. Genuine `finish` has already restored the return cell.

No operational bridge preempts or summarizes a program-defined operation, no
result-bearing opaque value exists, and no task answer is embedded as a table
or unconstrained oracle. I therefore identify no unsound local rule. Because
no rule is labeled unsound, there is no false-conclusion witness to supply;
the two concrete false-result witnesses instead confirm discrimination.

Stage 5 result: pass; the minimal generated semantics is sound and complete for
every construct the submitted program uses.

## 6. Fresh non-vacuity test

No candidate vacuity artifact was trusted. I authored
`evidence/13-spec-vacuity.k`, which leaves the actual program unchanged but
starts the result oracle's even accumulator at 1 instead of 0. This mutation is
demonstrably false at the reachable first input: the correct/actual result for
`n=1` is `(0,1)`, whereas the mutated obligation demands `(1,1)`.

First, `kprove ... --dry-run` parsed and built the mutated spec successfully
with exit 0 (`evidence/14-vacuity-build.log`). The real mutation run:

```text
kprove spec-vacuity.k --definition proof-kompiled \
  --spec-module SPEC-VACUITY --warnings none
```

exited 1 with `WarnStuckClaimState`. Its residual shows exactly
`VTuple(VInt(0),VInt(1)) ~> expect(1,1)` at `n=1`; this is the expected unmet
result obligation, not a parser error, missing import, timeout, or unrelated
crash. See `evidence/15-vacuity-kprove.log`.

Stage 6 result: pass; the proof is non-vacuous and constrains both tuple
components.

## 7. Proven versus assumed accounting

### What the reachability proof establishes

Under the audited generated K semantics and proof-local mathematical
definitions, starting with an empty local environment, the actual submitted
function body is executed once for every integer `N` from 1 to 1000. Every
execution returns the cumulative even and odd counts obtained by testing each
integer through `N` for equality with its base-10 digit reversal and then
classifying its parity. After all 1,000 exact checks, the harness reaches
`verified` with the environment empty and return state reset.

This is a partial-correctness result for the generated program on the complete
stated HumanEval domain. It does not claim behavior for `n < 1`, `n > 1000`,
non-integers, unsupported Python constructs, exceptions, or external effects.
Those cases are outside the source contract or absent from this program.

### Trust ledger

1. **K engine and built-ins.** The proof trusts K v7.1.293, the Haskell
   reachability backend, the LLVM concrete backend, and the imported `INT`,
   `BOOL`, and `MAP` implementations. These affect arithmetic, maps, rewriting,
   and proof closure. This is the ordinary unavoidable toolchain boundary.
2. **Trusted translator and mounts.** The launcher-designated translator,
   prompt, and canonical source are trusted inputs. Byte identity and
   independent hashing establish that the candidate used the same prompt and
   translator. Constructor comparison, rather than the generation trace,
   connects translation to the theorem term.
3. **Generated language semantics.** `semantic.k` is not externally blessed.
   Its 24 rules and all declarations were audited locally. It directly executes
   every material source operation and introduces no oracle. Normal/boundary K
   runs give independent executable support.
4. **Digit-reversal specification.** The proof-local `reverseDigits` equations
   and parity predicates are the formal target specification. The bridge from
   decimal digit reversal to “integer palindrome” is elementary ordinary
   mathematics: a positive integer is a decimal palindrome exactly when its
   decimal digit sequence equals its reversal. The disjoint one/two/three-digit
   formulas cover the complete 1..1000 domain, with 1000 handled explicitly.
   This is an acceptable transparent intent formalization, not a program-derived
   opaque abstraction.
5. **Python differential evidence.** Exhaustive agreement with the trusted
   canonical implementation and independent direct oracle supports the
   implementation-to-intent and semantics bridges for all 1,000 admissible
   inputs. It is corroborating evidence, not a substitute for the K proof.
6. **Manual program alias.** `verification.k` manually repeats the constructor
   term rather than regenerating it during the proof build. This is only an
   artifact-maintenance observation: byte-identical trusted translation,
   constructor-level equality, and the body mutation establish the immutable
   candidate's real-program pinning.

There is no fresh or opaque symbol whose interpretation influences a branch,
return, state cell, or postcondition. There is also no empirical bridge being
used as a universal connection theorem for skipped program execution, because
no such execution is skipped.

Gate A (real-program soundness), Gate B (intent adequacy), and Gate C (trust
and evidence auditability) all pass. The finite ground enumeration covers,
rather than narrows, the explicit `1 <= n <= 1000` source domain. No material
adequacy gap or non-fatal soundness concern remains.

VERDICT: PASS
LEGITIMACY: LEGIT
