# Adversarial audit: 89-encrypt

The candidate reconstructs to a non-vacuous K proof of a transparent summary
under its submitted K machine. It is nevertheless **not a legitimate proof of
the real generated Python program over the formal claim's domain**, and the
submitted program also fails the trusted canonical contract. The decisive
real-program witness is `S = "🙂"`: submitted Python returns `"t"`, while both
freshly rebuilt K backends return `"roil"`. Independently, `S = "A"` witnesses
the implementation/contract mismatch: the canonical function preserves `"A"`,
whereas the submission returns `"y"`.

All candidate prose, traces, logs, and compiled artifacts were treated as
untrusted. Source copies and all execution occurred under
`/tmp/audit-work`; reviewer evidence is under `/audit-output/evidence`.

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `GENERATED_SEMANTICS`. The trusted mount contains exactly
the three expected regular files at its top level:

- `/reference/canonical.py`
- `/reference/prompt.py`
- `/reference/py2mpy.py`

`/reference/reference-semantics` does not exist, as required. No hidden or
inferred reference semantics was used. There is no infrastructure
contradiction, so a candidate verdict is appropriate.

### Candidate artifacts and untrusted claims

The candidate contains regular source artifacts `prompt.py`, `py2mpy.py`,
`solution.py`, `solution.mpy`, `semantic.k`, `verification.k`, `spec.k`, and
`prove.sh`. The requested `run-input.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, and structured JSONL trace are also present. No discovered
candidate entry is a symlink.

The extra `semantic-kompiled/` and `__pycache__/` entries are generated
artifacts, not required source. They were not copied into the audit build and
were not used. No candidate `PROOF.md` or `spec-vacuity.k` exists; neither was a
required generation artifact, and the non-vacuity test was created afresh by
the reviewer.

The candidate's untrusted records claim a bare run, exit 0, no timeout, and a
successful `#Top` proof. The structured trace has 258 parseable JSON records,
52 tool calls, no JSON parse errors, and a final `KPROVE_PASSED` message. These
facts describe what the generator claimed; they were not accepted as proof
evidence.

### Trusted comparisons

The candidate prompt is byte-identical to `/reference/prompt.py`; both have
SHA-256
`efefc17723390b1692f2f4fdbb26dac3ecc055be739dbaaa2a020f5b18d4999a`.
The candidate translator is byte-identical to `/reference/py2mpy.py`; both have
SHA-256
`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.
Those hashes also match `run-input.json`.

Evidence: `evidence/provenance.sh` and `evidence/provenance.log`.

Stage 1 result: **PASS**. There is no provenance or mount integrity breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The trusted prompt asks for alphabet rotation by `2 * 2`, i.e. four positions.
The trusted canonical implementation makes the intended behavior precise:
process every character in order; rotate lowercase ASCII `a` through `z`
forward by four with wraparound; preserve every character not in that
lowercase alphabet. The empty string returns the empty string.

The candidate uses a different recursive algorithm:

```python
if s == "":
    return ""
return chr((ord(s[0]) - 97 + 4) % 26 + 97) + encrypt(s[1:])
```

For lowercase ASCII this implements the requested rotation. For every other
character it forcibly maps the code point into `a` through `z` instead of
preserving it. It also uses one Python call frame per character, unlike the
canonical loop.

### Translator fidelity

Running the trusted translator on the scratch copy of `solution.py` exited 0.
The regenerated `solution.mpy` is byte-identical to the submitted
`solution.mpy`; both have SHA-256
`f0ce1818f2a6cbfcc0b656a5c4b604d24a526be95f6f285440ac91bae9ec7cab`.
Thus the `.mpy` artifact faithfully represents the submitted Python source.

### Independent differential test

The reviewer script imports the trusted canonical entry point directly from
`/reference/canonical.py` and the submitted entry point from the isolated
source copy. It does not reuse K equations. Its deterministic scope was:

- all four documented examples;
- 22 empty, wrap-boundary, membership-boundary, mixed, and Unicode cases;
- every lowercase string of length zero, one, or two after de-duplication
  (692 cases);
- 194 deterministic generated lowercase strings;
- 191 deterministic generated mixed-character strings;
- lowercase strings of lengths 900 and 1,100.

All 1,105 inputs and per-input outcomes are preserved. There were 205
mismatches:

- documented examples: 0/4;
- exhaustive lowercase length at most two: 0/692;
- generated lowercase: 0/194;
- boundary cases: 13/22;
- generated mixed strings: 191/191;
- long strings: 1/2.

Concrete material witnesses include:

- `"A"`: canonical `"A"`, candidate `"y"`;
- `"0"`: canonical `"0"`, candidate `"h"`;
- `"hello world"`: canonical `"lipps asvph"`, candidate
  `"lippsrasvph"`;
- `"a" * 1100`: canonical returns a string, candidate raises
  `RecursionError`.

Evidence: `evidence/differential_test.py`,
`evidence/differential-inputs.json`, `evidence/differential-results.json`,
`evidence/fidelity_and_diff.sh`, and `evidence/fidelity-and-diff.log`.

Stage 2 result: **FAIL**. Translation is faithful, but the actual submitted
program materially diverges from the trusted canonical behavior on the
unrestricted string domain.

## 3. Clean proof reconstruction

### Fresh definitions

Only source files were copied to `/tmp/audit-work/source`. Neither the
candidate's `semantic-kompiled/` nor any candidate cache was copied. With K
7.1.293, the following fresh builds both exited 0:

```text
kompile semantic.k --backend llvm --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/build/concrete-kompiled

kompile semantic.k --backend haskell --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/build/proof-kompiled
```

The independently selected recursive helper claim exited 0 and printed
`#Top`. The complete target spec, containing the helper and its dependent
end-to-end claim, also exited 0 and printed `#Top`:

```text
kprove spec.k --definition /tmp/audit-work/build/proof-kompiled \
  --spec-module SPEC --claims SPEC.encrypt-call-correct
#Top

kprove spec.k --definition /tmp/audit-work/build/proof-kompiled \
  --spec-module SPEC
#Top
```

Both commands have exit status 0 in `evidence/positive-proofs.log`.

A reviewer diagnostic selected only `SPEC.program-correct`. That selection
removes `SPEC.encrypt-call-correct`, the recursive circularity on which the
entry proof depends. It stayed CPU-active without a conclusion for about
10 minutes 35 seconds and was interrupted by the reviewer with status 130.
This dependency-removal diagnostic is not treated as either positive evidence
or a candidate/infrastructure failure. Its exact disposition is recorded in
`evidence/program-only-diagnostic-status.txt`.

### Generated-semantics concrete reconstruction

The fresh LLVM definition was run on 17 normal and boundary inputs and compared
with independent execution of submitted Python. Sixteen matched, including
empty, every lowercase wrap boundary, all documented examples, uppercase,
digits, punctuation, spaces, and `"é"`.

The non-BMP input `"🙂"` did not match:

```text
submitted Python: "t"
fresh LLVM K:     "roil"
fresh Haskell K:  "roil"
```

All three commands terminate normally. This is not a timeout or harness error.
The Haskell result is especially material because that is the definition used
by `kprove`.

Evidence: `evidence/rebuild.log`, `evidence/rebuild.sh`,
`evidence/positive_proofs.sh`, `evidence/positive-proofs.log`,
`evidence/concrete_semantics_test.py`,
`evidence/concrete-semantics-results.json`,
`evidence/concrete-semantics.log`, `evidence/unicode_witness.sh`, and
`evidence/unicode-backend-witness.log`.

Stage 3 result: **FAIL**. Fresh compilation and K proof closure succeed, but the
mandatory generated-semantics execution check exposes a false bridge to real
Python behavior over the claim's stated domain.

## 4. Adequacy and real-program pinning

### Claim meanings

`encrypt-call-correct` has no restriction on `S` beyond being a K `String`.
Given:

- the already-evaluated argument `S` immediately before
  `applyFun("encrypt")`;
- the exact function metadata `"encrypt"`, parameter `"s"`, and
  `solutionBody`;
- any environment, stack, continuation `K`, and result cell;

it claims that execution returns the value `rotate4(S)` into the same
continuation, restores the original environment and stack, and preserves the
result cell. This is a proper call-level result constraint; the returned value
is not free.

`program-correct` also has no restriction on `S` beyond K `String`. From the
initial module, empty metadata/environment/stack, and `noResult`, it claims
that execution clears `<k>`, installs the exact function metadata, leaves the
environment and stack empty, and writes exactly `rotate4(S)` to `<result>`.
This is equality to a specific recursive function, not a tautology or one-way
implication.

### Satisfying states

Both preconditions are satisfiable:

- helper witness: `S = "hi"`, `K = finish`, `ENV = .Map`,
  `STACK = .List`, `_R = noResult`, with the exact function metadata;
- entry witness: `S = ""` in the declared initial configuration.

The non-vacuity experiment in Stage 6 independently confirms reachability of a
result-bearing obligation.

### Actual-body pinning

The spec uses the abbreviation `solutionBody` rather than loading a file
directly. This abbreviation is transparent and expands to the exact statement
tree in `solution.mpy`. Three checks pin it:

1. trusted regeneration gives byte identity for `solution.mpy`;
2. static comparison shows the sole `solutionBody` equation is the same `If`
   and following `Return` tree;
3. after the module-entry transition, fresh Haskell execution of the actual
   parsed `.mpy` and execution of
   `Module(FuncDef("encrypt", Params("s"), solutionBody))` produce
   byte-identical configurations, SHA-256
   `0e7bdaf2f69650dc3348c516b923fa1d50cdfea4d86caa544db3cae9f615977e`.

Thus the K claim does not substitute a different AST. Evidence:
`evidence/pinning.sh`, `evidence/mpy-full-parser.sh`,
`evidence/solution-symbolic.mpy`, and `evidence/pinning.log`.

### Concrete substitutions

- `S = ""`: claimed K result `""`; submitted and canonical Python both
  return `""`.
- `S = "hi"`: claimed K result `"lm"`; submitted and canonical Python both
  return `"lm"`.
- `S = "A"`: claimed K result `"y"` and submitted Python returns `"y"`, but
  canonical Python returns `"A"`.
- `S = "🙂"`: claimed/rebuilt K result `"roil"`, submitted Python returns
  `"t"`, and canonical Python returns `"🙂"`.

Stage 4 result: **FAIL**. The theorem is non-vacuous, result-constraining, and
pins the submitted AST, but its all-K-strings execution claim does not pin real
Python semantics, and its postcondition does not express the canonical
property.

## 5. Rule-by-rule static soundness review

The full local inventory, including all declaration spellings and rule
classifications, is preserved in `evidence/rule-inventory.md`. There are no
generated helper K files other than `verification.k`.

### Every local syntax/state declaration

`semantic.k` declares:

- `Pgm`: `Module`;
- separator-free `Stmts`;
- `Stmt`: `FuncDef`, `If`, `Return`;
- `Params`;
- `Expr`: `Name`, `Str`, `Int`, `BinOp`, `Call`, `Subscript`, `Slice`,
  `Compare`;
- `CmpOp`;
- `Bound`: `Expr` or `NoBound`;
- `Result`: `noResult` or `String`;
- `Val`: `Int`, `String`, `Bool`, or `PyBool`;
- control items `start`, `eval`, `exec`, `binLeft`, `binRight`, `cmpLeft`,
  `cmpRight`, `subBase`, `applyFun`, `choose`, `endCall`, `finish`;
- `appendStmts`, marked `[function,total]`;
- cells for computation, one stored function, environment, call stack, and
  result.

`verification.k` declares `solutionBody`, marked `[function,total]`, and
`rotate4(String)`, marked `[function]`. There are no local `[functional]`
declarations, opaque symbols, priorities, `owise` rules, or operational
bridges. Only the two `rotate4` equations are marked `[simplification]`.

Every construct in `solution.mpy` is covered: module/function/parameter,
statement lists, `If`, `Return`, names, string and integer literals,
comparisons with `==`, binary `+`, `-`, `%`, calls, integer subscription, and
the `[1:]` slice with `NoBound`.

### All 28 `semantic.k` rules

| No. | Rule | Static decision |
|---:|---|---|
| 1 | empty `appendStmts` | True empty-list equation. |
| 2 | nonempty `appendStmts` | True, disjoint structural recursion. |
| 3 | module/start | Correctly captures the submitted single function and calls it before `finish`. |
| 4 | string literal | Correct on used terms. |
| 5 | integer literal | Correct on used terms. |
| 6 | name lookup | Correct for a present typed binding; submitted uses only bound `s`. |
| 7 | begin binary expression | Establishes left-first order. |
| 8 | continue binary expression | Evaluates right only after a left value. |
| 9 | integer `+` | Correct imported integer operation. |
| 10 | string `+` | Correct concatenation operation. |
| 11 | integer `-` | Correct imported integer operation. |
| 12 | integer `%` | `modInt` agrees with Python for the reached positive divisor 26. |
| 13 | begin comparison | Establishes left-first order. |
| 14 | continue comparison | Evaluates the right expression second. |
| 15 | string `==` | Produces the dedicated Python-bool wrapper used by `If`. |
| 16 | begin subscript | Evaluates the base first; used indices are literal forms. |
| 17 | integer string subscript | **Unsound Python bridge over the formal string domain**, together with the hooked string operations; see the witness below. |
| 18 | `[I:]` string slice | **Unsound Python bridge over the formal string domain**, together with the hooked string operations; see the witness below. |
| 19 | begin one-argument call | Preserves the submitted argument-before-dispatch order. |
| 20 | `chr` dispatch | Correct on the reached range 97 through 122. |
| 21 | `ord` dispatch | Correct only if its K string operand represents Python's one code point; rules 17-18 fail that bridge on the witness. |
| 22 | stored user call | Correctly overwrites `s`, saves the old environment, and executes the exact body for this recursive one-function program. |
| 23 | begin `If` | Preserves branches and suffix while evaluating the condition. |
| 24 | true branch | Executes then-statements followed by the suffix. |
| 25 | false branch | Executes else-statements followed by the suffix. |
| 26 | `Return` | Correctly discards the remaining statement suffix and evaluates the return expression. |
| 27 | end call | Restores the saved environment and pops one stack entry. |
| 28 | finish | Writes the final string and clears computation. |

Rules 17 and 18 translate Python code-point indexing/slicing directly to the
local K string hooks. The concrete, satisfying, normally terminating witness is
the formal input `S = "🙂"`. Python evaluates `s[0]` to the one character
`"🙂"`, computes the candidate result `"t"`, and terminates. Under both
freshly built K backends, the rule sequence using
`substrString`/`lengthString` advances through the UTF-8 representation and
enables the false final conclusion `"roil"`. This witnesses a false result on
the intended input domain, not merely missing evidence.

Rules 17, 18, 20, and 21 also omit Python's invalid-index and invalid-`ord`/
`chr` exception conditions. Those broader cases are unreachable in this exact
source because the empty guard precedes index 0 and the computed `chr` argument
is always 97 through 122. No additional unsoundness verdict is based on those
unreachable contexts; they are recorded as a narrower over-breadth gap.

The generic stored-function rule could overlap `ord` dispatch if the stored
user function were itself named `ord`. The actual module fixes the name to
`encrypt`, so there is no reachable false conclusion witness for this program
and the overlap is not labeled materially unsound.

The single-function metadata is not stacked, but all reachable user calls are
recursion into that same function. The environment is stacked and restored,
so no state/allocation/output effect is silently lost for this program.

### Every `verification.k` extension

1. `solutionBody` has one total, transparent equation equal to the actual
   parsed source body. It is a definitional abbreviation, not a substituted
   program or oracle.
2. `rotate4("") => "" [simplification]` is a truthful base equation.
3. The guarded nonempty `rotate4` simplification emits the transformed first
   K-string unit and recursively processes the remaining K substring.
4. The `rotate4` declaration is a non-opaque K function; it is not declared
   total.

The two `rotate4` guards are disjoint and cover concrete K strings. The
recursion descends according to the imported K string hooks. `rotate4` never
rewrites a program execution term; it occurs only in claim destinations.
Therefore it is not an unconstrained result oracle or execution bypass.

It is also not an independent connection theorem to Python: it uses the same
`lengthString`, `substrString`, `ordChar`, and `chrChar` hooks as program
execution. Agreement between execution and `rotate4` is internally meaningful
but circular as evidence that those hooks model CPython. The `"🙂"` witness
falsifies that external bridge.

### Imported primitives and overlaps

The proof imports K integer operations, K string hooks, map lookup/update,
lists, booleans, sequencing, and K equality. Integer rule shapes and reached
types are disjoint. Base/non-base `rotate4` guards are disjoint. Empty/nonempty
`appendStmts` patterns are disjoint. No priority silently preempts normal
execution.

Stage 5 result: **FAIL**. There is no smuggled task-answer axiom, but the
generated semantics materially mis-models a used Python construct over the
unrestricted claimed domain, with the required concrete false-result witness.

## 6. Fresh non-vacuity test

No candidate mutation was trusted. The reviewer created
`/tmp/audit-work/source/spec-vacuity.k`, preserved as
`evidence/spec-vacuity.k`. It keeps the recursive helper and changes the entry
postcondition from:

```text
rotate4(S)
```

to:

```text
rotate4(S) +String "x"
```

This is demonstrably false for the satisfying input `S = ""`: actual execution
returns `""`, while the mutation demands `"x"`.

The dry run exited 0, showing that parsing, imports, and claim construction
succeeded. The real mutated proof exited 1 with `WarnStuckClaimState`. Its
residual explicitly requires the unmet equality:

```text
rotate4(S) +String "x" #Equals rotate4(S)
```

This is the intended result-obligation failure, not a parser error, missing
import, timeout, or unrelated crash.

Evidence: `evidence/nonvacuity.sh`, `evidence/spec-vacuity.k`, and
`evidence/nonvacuity.log`.

Stage 6 result: **PASS**. The original theorem is result-sensitive and
non-vacuous.

## 7. Proven-versus-assumed accounting

### What `#Top` actually establishes

Under the candidate-defined `MPY` K machine and its imported K hooks, the
successful reachability proof establishes partial correctness of the exact
submitted `.mpy` tree:

- a recursive call with the exact stored `encrypt` body returns
  `rotate4(S)`, restoring environment and stack and preserving its arbitrary
  continuation;
- the exact module entry reaches an empty `<k>`, empty environment/stack, and
  result `rotate4(S)`.

The theorem is universal over K `String` and contains no ASCII-only
precondition. It does not establish that `rotate4` is canonical lowercase-only
encryption, that K string indexing equals CPython string indexing, that
non-lowercase characters are preserved, or that CPython recursion limits and
exceptions are modeled.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K 7.1.293 parser, Haskell/LLVM backends, and reachability prover | All builds and proof closure | Ordinary accepted toolchain trust for the K theorem. Fresh dual builds reduce cache risk. |
| Imported integer hooks | Arithmetic in execution and `rotate4` | Acceptable on the reached integer domain; modulo divisor is positive. |
| Imported K string hooks | Indexing, slicing, `ord`, `chr`, recursion, returned value, both claims | Legitimate primitives for a theorem about the K machine, but an **illegitimate bridge to CPython over all strings** because `"🙂"` yields different normal results. |
| Map/list/Bool/K-equality primitives | Binding, calls/returns, guards | Acceptable low-level structural trust for this program. |
| Trusted `py2mpy.py` | Source-to-AST identity | Acceptable and directly checked by byte regeneration. |
| `solutionBody` | Both claims | Transparent and machine-pinned to the submitted AST; acceptable. |
| `rotate4` | Both postconditions | Transparent K definition, not opaque; acceptable internally but not independent evidence for K-to-Python string fidelity. |
| Canonical-to-natural-language interpretation | Intended task property | Trusted mounted reference makes lowercase rotation plus preservation explicit. |
| Differential tests | Program/canonical and K/Python bridges on tested inputs | Finite empirical evidence only. It does not replace a universal proof; here it supplies concrete counterexamples, which are sufficient to refute universal equivalence. |
| CPython recursion behavior | Long-input implementation behavior | Not modeled by K. The 1,100-character witness is an additional implementation/adequacy limitation, not the basis for claiming reachability-rule inconsistency. |

There are no fresh opaque result symbols, external oracles, proof-local
priority rules, or assumed operational bridges. The fatal assumption is more
basic: the generated language semantics treats its K string hooks as a faithful
model of Python indexing/slicing over a universal string domain, which the
recorded normal-termination witness disproves.

### Gates and decision

- Real-program soundness: **FAIL**. `S = "🙂"` gives Python `"t"` and
  proof semantics `"roil"` under both fresh backends.
- Intent adequacy: **FAIL**. `S = "A"` gives canonical `"A"` and candidate
  `"y"`; mixed-character differential testing produces 204 such result
  divergences before the separate long-input exception mismatch.
- Non-vacuity/result constraint: **PASS**.
- Reproducibility/auditability: **PASS for the reviewer evidence**; the
  candidate's own reports were not relied upon.

The successful `#Top` is therefore an internally meaningful proof about a
different string machine and a noncanonical result function. Because the
semantics makes a false normally terminating conclusion possible on the
formal intended domain, this is not the narrower kind of informal bridge or
thin evidence limitation eligible for `CONCERNS / LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
