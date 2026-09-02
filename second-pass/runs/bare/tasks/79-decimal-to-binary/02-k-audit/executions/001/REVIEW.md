# Independent adversarial review: 79-decimal-to-binary

## Overall assessment

The candidate contains a legitimate, result-constraining partial-correctness
proof of the submitted translated program under its generated semantics. The
proof was reconstructed from source only; all five positive claims independently
closed with `#Top` and exit 0; the concrete semantics agreed with both Python
implementations; every claim pins the submitted AST; a body mutation changed the
reachable result; and a fresh false-result mutation was rejected for the expected
semantic reason.

The verdict is `CONCERNS / LEGIT`, rather than `PASS`, because the proof's
human-intent bridge is not itself a separate K theorem. The formal result uses
the transparent recursive helper `binDigits`, which is mathematically the usual
base-two expansion and which was independently tested, but the universal
connection between that generated model, CPython's `bin`, and the English phrase
"binary format" remains an audited informal/modeling argument. There is also an
intent ambiguity for negative integers: the formal theorem deliberately covers
them and exactly matches the trusted canonical function, but the result contains
an interior `b` (for example `dbb101db`) and therefore is not literally composed
only of binary digits between the wrappers. Neither limitation makes a false K
conclusion provable.

## 1. Input and provenance integrity

The rendered mode is `GENERATED_SEMANTICS`. The required boundary is intact:
`/reference/reference-semantics` is neither present nor a symlink. There was no
attempt to locate or infer a hidden reference semantics.

The required candidate source deliverables are all regular files:

- `/candidate/solution.py`
- `/candidate/solution.mpy`
- `/candidate/semantic.k`
- `/candidate/verification.k`
- `/candidate/spec.k`
- `/candidate/prove.sh`

There are no candidate symlinks and no helper K files. No required artifact is
missing, mistyped, or unexpectedly replaced. `/candidate/prompt.py` is
byte-identical to `/reference/prompt.py` (SHA-256
`642ae5cf366d95e0595e3e2941597956baa6029b29ead988dd25754fbafa26c3`),
and `/candidate/py2mpy.py` is byte-identical to the trusted translator
(SHA-256
`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`).

The candidate additionally contains `.kbuild/` and `__pycache__/`. These are
generated build/cache artifacts, not source-integrity anomalies. They were not
copied into either fresh build directory and were never used. Provenance files
`run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`, and the
one JSONL generation trace were read only as untrusted claims. Both JSON files
and all 175 JSONL records parse, and the trace/log assert a successful prior
proof; none of that assertion was credited as proof evidence.

Exact inventory, hashes, comparisons, trace parsing, commands, and statuses are
in [01-provenance.log](evidence/01-provenance.log), produced by
[01-provenance.sh](evidence/01-provenance.sh) and
[inspect_trace.py](evidence/inspect_trace.py). The script and outer command both
exited 0.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and source comparison

For a Python integer `decimal`, the trusted prompt requests a string containing
its binary representation, wrapped with `db` at both ends. The trusted canonical
implementation makes this operationally precise:

```python
return "db" + bin(decimal)[2:] + "db"
```

Thus nonnegative values use ordinary unsigned binary digits (`0` maps to `0`);
for a negative integer, CPython's `bin` starts with `-0b`, and slicing from index
2 leaves `b` plus the magnitude's digits. The candidate `solution.py` is the same
one-line algorithm and signature, with only the canonical docstring omitted.
The intended audited domain is Python integers. Zero is the meaningful empty- or
zero-iteration numeric boundary; no separate "empty integer" exists. Non-integer
objects, custom `__index__`, and resource failures are outside the formal `Int`
domain.

The trusted command

```text
python3 /tmp/audit-work/py2mpy.py /tmp/audit-work/solution.py > /tmp/audit-work/regenerated-solution.mpy
```

exited 0. `cmp` against the submitted `solution.mpy` exited 0, and both files
have SHA-256
`b6ff40e8ee7da4fb4cc501f09c4cc85a38fa63951d9f53479c1922bd949c6666`.

### Independent differential test

[differential.py](evidence/differential.py) separately imports the trusted
canonical entry point and candidate entry point. It tested 5,094 distinct
integers:

- examples 15 and 32;
- sign/recursion boundaries including `-2,-1,0,1,2,3`;
- values adjacent to powers of two;
- 64-bit boundaries and positive/negative 4097-bit values;
- every integer in `[-2048, 2048]`; and
- 1,000 deterministic generated signed integers of 1 to 1024 bits.

There were zero return/exception/type/value mismatches. The complete input list,
edge results, command, exit status, and zero-mismatch result are preserved in
[02-fidelity.log](evidence/02-fidelity.log). This finite test supports program
fidelity; it is not treated as a universal K proof.

## 3. Clean proof reconstruction

Candidate definitions and caches were excluded. Source copies were placed under
`/tmp/audit-work/source`, `/tmp/audit-work/build-concrete`, and
`/tmp/audit-work/build-proof`. Before compilation, checks that
`concrete-kompiled` and `verification-kompiled` did not exist both exited 0.
The independently installed tools report K version `v7.1.293`.

Fresh concrete build:

```text
kompile /tmp/audit-work/build-concrete/semantic.k \
  --backend llvm --main-module SEMANTIC \
  --syntax-module SEMANTIC-SYNTAX \
  --output-definition /tmp/audit-work/build-concrete/concrete-kompiled
```

Fresh proof build:

```text
kompile /tmp/audit-work/build-proof/verification.k \
  --backend haskell --main-module VERIFICATION \
  --syntax-module SEMANTIC-SYNTAX \
  --output-definition /tmp/audit-work/build-proof/verification-kompiled
```

Both commands exited 0. [split_claims.py](evidence/split_claims.py) copied each
of the five unchanged claim bodies into a distinct scratch spec module. Each of
the following independently printed `#Top` and exited 0:

```text
kprove spec-claim-1.k --definition verification-kompiled --spec-module AUDIT-SPEC-CLAIM-1
kprove spec-claim-2.k --definition verification-kompiled --spec-module AUDIT-SPEC-CLAIM-2
kprove spec-claim-3.k --definition verification-kompiled --spec-module AUDIT-SPEC-CLAIM-3
kprove spec-claim-4.k --definition verification-kompiled --spec-module AUDIT-SPEC-CLAIM-4
kprove spec-claim-5.k --definition verification-kompiled --spec-module AUDIT-SPEC-CLAIM-5
```

The original aggregate command on `spec.k` also printed `#Top` and exited 0.
Full absolute commands, unchanged-body hashes, bounded output, and statuses are
in [03-reconstruction.log](evidence/03-reconstruction.log).

Because this is generated semantics, the fresh LLVM definition was also run on
19 normal and boundary inputs: negative sign cases, zero, the `1/2` recursion
boundary, both examples, values around 256, and positive/negative 64-bit
boundaries. Every `krun` exited 0, reached `.K`, produced a concrete `strVal`,
and matched both independent Python executions; mismatch count was zero. The
exact `krun` commands and configurations are in the same reconstruction log,
and the comparator is [concrete_compare.py](evidence/concrete_compare.py).

## 4. Adequacy and real-program pinning

### Entry claims in plain language

| Claim | Precondition | Postcondition |
|---|---|---|
| 1 | `I` is a K integer and `I >= 0` | The exact submitted program consumes `<k>` and changes the empty result to `strVal(decimalToBinarySpec(I))`. |
| 2 | `I` is a K integer and `I < 0` | The same exact program consumes `<k>` and returns the corresponding negative-case summary. |
| 3 | Argument is 15 | It returns exactly `strVal("db1111db")`. |
| 4 | Argument is 32 | It returns exactly `strVal("db100000db")`. |
| 5 | Argument is -5 | It returns exactly `strVal("dbb101db")`. |

The two symbolic preconditions are disjoint and exhaustive over K `Int`.
The postconditions contain no fresh variable, existential result, implication,
or unconstrained oracle. They constrain the complete result cell to a `strVal`
and require the program computation to be consumed.

### Pinning and control flow

[check_pinning.py](evidence/check_pinning.py) extracts the balanced `Module(...)`
term from every claim and compares it, modulo formatting outside strings, with
the submitted translated program. All five are identical and share normalized
SHA-256
`fbb7ca290d81c351043a0db996ba32e407e861e9e68b38dadba0cba1bbca954b`.
The check exited 0; details are in
[04-static-review.log](evidence/04-static-review.log).

The entry semantic rule matches exactly
`Module(FuncDef("decimal_to_binary", Params("decimal"), Return(E)))`. It reads
the configured integer argument, binds it to `decimal`, evaluates the real body
expression, writes that value to `<result>`, and consumes `<k>`. The submitted
body's `Str`, `Name`, `Call(bin, ...)`, `Slice(2, NoBound, NoBound)`, nested
string `BinOp("+",...)`, and `Return` all follow the corresponding rules. There
are no helper or loop claims, so there is no detached invariant or substituted
control-flow summary to validate.

The separate body-sensitivity probe replaces the body with
`Return(Str("changed"))` while leaving the expected result `db1111db`. It
successfully parsed (`--dry-run` exit 0), then `kprove` exited 1 with a stuck
terminal configuration containing `strVal("changed")`. This demonstrates that
fixed execution, not the operation name alone, determines the result. The
artifact and result are
[spec-body-sensitivity.k](evidence/spec-body-sensitivity.k) and
[05-sensitivity-and-nonvacuity.log](evidence/05-sensitivity-and-nonvacuity.log).

### Satisfying states and ground substitutions

Realizable initial configurations are the parsed submitted `Module(...)` in
`<k>`, one of the following integers in `<arg>`, and `.K` in `<result>`:

| Claim witness | Formal result | Trusted canonical | Candidate Python | Fresh K execution |
|---:|---|---|---|---|
| `I = 0` | `db0db` | `db0db` | `db0db` | `db0db` |
| `I = -1` | `dbb1db` | `dbb1db` | `dbb1db` | `dbb1db` |
| `15` | `db1111db` | `db1111db` | `db1111db` | `db1111db` |
| `32` | `db100000db` | `db100000db` | `db100000db` | `db100000db` |
| `-5` | `dbb101db` | `dbb101db` | `dbb101db` | `dbb101db` |

Ground substitutions of `decimalToBinarySpec` for these values were compiled
and closed with `#Top`; both Python implementations returned the same strings.
Commands and output are in
[06-ground-summaries.log](evidence/06-ground-summaries.log), with the preserved
probe in [spec-ground-summaries.k](evidence/spec-ground-summaries.k).

## 5. Rule-by-rule static soundness review

### Exhaustive declaration inventory

There are no generated helper K files beyond `semantic.k` and
`verification.k`.

`SEMANTIC-SYNTAX` declares:

- `Program`: `Module(Stmt)`;
- `Stmt`: `FuncDef(String, Params, Stmt)` and `Return(Expr)`;
- `Params`: `Params(String)`;
- `Expr`: `Int(Int)`, `Str(String)`, `Name(String)`,
  `BinOp(String, Expr, Expr)`, `Call(Expr, Expr)`, and
  `Subscript(Expr, Slice)`;
- `Slice`: `Slice(Bound, Bound, Bound)`; and
- `Bound`: an `Expr` injection or `NoBound`.

`SEMANTIC` declares:

- environment constructor `bind(String, Int)`;
- value constructors `intVal`, `strVal`, `binVal`, and `negativeBinVal`;
- functions `eval`, `addValues`, `callBin`, `suffixFrom`, and `binDigits`; and
- configuration cells `<k>`, `<arg>`, and `<result>`.

`VERIFICATION` declares the function `decimalToBinarySpec`.

All AST/value/environment constructors carry only ordinary `symbol(...)`
attributes. Exactly six local declarations have `[function]`: `eval`,
`addValues`, `callBin`, `suffixFrom`, `binDigits`, and
`decimalToBinarySpec`. There are no local `[total]`, `[functional]`,
`[simplification]`, `[concrete]`, priority, macro, anywhere, hook, or opaque
declarations. There are no simplification rules, priority rules, auxiliary
claims, fresh symbols, or operational rules in `verification.k`. The source
listing and attribute/rule search are preserved in
[04-static-review.log](evidence/04-static-review.log).

### Used-construct coverage

| Submitted construct | Declaration and behavior |
|---|---|
| `Module`, `FuncDef`, `Params`, `Return` | Parsed by the syntax declarations; the exact entry rule selects the named function/parameter and evaluates its return expression. |
| `Str` | `eval(Str(S), _) => strVal(S)`. |
| `Name("decimal")` | Exact one-binding lookup through `eval(Name(X), bind(X,I))`. |
| `BinOp("+",...)` | Structural evaluation followed by `addValues`; this program reaches the string/string rule. |
| `Call(Name("bin"),...)` | Structural argument evaluation followed by the guarded sign cases of `callBin`. |
| `Subscript` and `Slice(Int(2),NoBound,NoBound)` | Structural base evaluation followed by the two exact index-2 `suffixFrom` cases. |
| `Int(2)` and `NoBound` | Parsed explicitly in the slice pattern; no unmodeled target term remains. |

There is no assignment, mutation, heap, allocation, exception path, output,
loop, user-function call stack, or continuation after the module term in the
submitted IR. The semantics therefore needs no cells for those features.
Recursive `eval` does not state a source evaluation order with `strict`
attributes, but every target subexpression is pure and total over the formal
integer input, so reordering cannot change value, state, control, or exceptions
for this program.

### Every local rule

| Rule(s) | Classification and decision |
|---|---|
| `semantic.k:56-63` | Ordinary entry semantic rule. Exact function name, parameter, body, binding, argument, empty result, and complete `<k>` are matched. It consumes control and writes exactly the evaluated body. Sound for the submitted module. |
| `65` | Integer literal evaluation. Constructor-preserving and sound. It is used by the slice start. |
| `66` | String literal evaluation. Constructor-preserving and sound. |
| `67` | Lookup in the only environment constructor. The repeated `X` enforces binding identity; sound. |
| `68-69` | Binary `+` structurally evaluates both operands and delegates to typed addition. Sound for the pure nested string expressions. |
| `70` | The only modeled call is the fixed external builtin name `bin`; the argument is evaluated before `callBin`. Sound on the used binding and integer argument. |
| `71-72` | The only modeled subscript is an open-ended slice whose start is an integer expression. It evaluates the base and passes the start. The actual start is 2. Sound and deliberately partial outside the used form. |
| `74` | K-integer addition for two `intVal`s. Mathematically sound but unreachable in this program. |
| `75` | K-string concatenation for two `strVal`s. Sound and used twice. |
| `78-79` | For nonnegative input, `binVal(binDigits(I))` is the internal representation of Python `"0b" + digits`. The guard is exact and the constructor is consumed only by the modeled slice. Sound. |
| `81-82` | For negative input, `negativeBinVal(binDigits(-I))` represents Python `"-0b" + digits(abs(I))`. The magnitude is positive and the sign guard is disjoint from the preceding case. Sound. |
| `84` | Slicing the positive internal bin representation from index 2 removes `0b` and returns its digit string. Sound for the only used slice. |
| `85` | Slicing `"-0b" + S` from index 2 yields `"b" + S`. This matches CPython and the trusted canonical implementation, including the arguably surprising interior `b`. Sound. |
| `87-88` | Base cases 0 and 1 return `Int2String(0)` or `Int2String(1)`. Sound. |
| `89-90` | For `I >= 2`, the quotient `I /Int 2` is nonnegative and strictly smaller, and the remainder is 0 or 1. Prefix recursion followed by the remainder digit is the usual base-two recurrence. The rule descends and is mathematically sound. |
| `verification.k:11-13` | Definitional summary for `I >= 0`; it wraps exactly the same transparent digit expansion with `db`. It does not replace execution. Sound. |
| `verification.k:14-16` | Disjoint negative summary; it accounts for the `bin(...)[2:]` behavior and wraps it. It does not replace execution. Sound. |

Guard and overlap audit:

- `I >= 0` and `I < 0` are disjoint and exhaustive for both `callBin` and
  `decimalToBinarySpec`.
- On the only reachable `binDigits` domain (`I >= 0`), `0 <= I < 2` and
  `I >= 2` are disjoint and exhaustive. Negative calls intentionally remain
  visibly undefined.
- The `addValues` and `suffixFrom` equations are separated by distinct value
  constructors.
- `eval` equations are separated by distinct AST constructors, apart from the
  intentionally exact operator/builtin/slice patterns.
- No priority is needed, and no two applicable equations disagree.

The functions are correctly not declared `[total]` because the intentionally
minimal generated language leaves unused operators, calls, slices, and bad
bindings stuck. Missing semantics for those unused constructs does not fabricate
a result and is permitted in this mode.

The core base-conversion operation appears in generated semantics because the
real Python program delegates that operation to the external builtin `bin`.
This is an acceptable modeled primitive, not a proof-local bypass: it has
transparent terminating equations on every reachable input, the actual program
body must reach it, and the body-sensitivity probe rejects a changed body.
`binVal` and `negativeBinVal` are internal tagged representations, not
unconstrained result oracles. No rule was found unsound, so no unsoundness label
or false-conclusion witness is asserted.

## 6. Fresh non-vacuity test

There was no candidate `spec-vacuity.k` to trust. The reviewer-authored
[spec-false-result.k](evidence/spec-false-result.k) keeps the exact submitted
program and satisfying input 15, but changes the required result from the actual
`db1111db` to the demonstrably false `db1110db`.

The dry-run command parsed and built the mutation successfully with exit 0. The
real proof command

```text
kprove /tmp/audit-work/build-proof/spec-false-result.k \
  --definition /tmp/audit-work/build-proof/verification-kompiled \
  --spec-module AUDIT-SPEC-FALSE-RESULT
```

exited 1. Its `WarnStuckClaimState` residual has `.K`, argument 15, and
`strVal("db1111db")` in the result cell, exactly identifying the unmet false
obligation. Both Python implementations independently returned `db1111db`.
This is a reachable semantic failure, not a parser error, missing import,
timeout, or unrelated crash. Exact commands and output are in
[05-sensitivity-and-nonvacuity.log](evidence/05-sensitivity-and-nonvacuity.log).

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Under the generated K definition and K's mathematical integer/string domains:

- for every K integer `I >= 0`, if the exact submitted translated module is run
  from the configured entry state and terminates, its result is
  `strVal("db" +String binDigits(I) +String "db")`;
- for every K integer `I < 0`, its result is
  `strVal("db" +String "b" +String binDigits(-I) +String "db")`; and
- the exact concrete corollaries for 15, 32, and -5 hold.

The proof is partial correctness. It does not prove finite-resource behavior or
CPython termination under memory exhaustion. The recursive semantic equations
do descend for every concrete nonnegative integer, and fresh concrete runs
terminated, but the reachability result should still be stated in the requested
partial-correctness form.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K v7.1.293 frontend, LLVM/Haskell backends, and `kprove` soundness | All compilation, execution, and proof conclusions | Standard unavoidable proof-tool trust boundary. Fresh dual-backend reconstruction reduces cache/provenance risk but does not verify the tool implementation. |
| K `INT`, `STRING`, and `BOOL` domains, including comparisons, `+Int`, `-Int`, `/Int`, `%Int`, `+String`, and `Int2String` | Expression semantics, `binDigits`, summaries, all claims | Acceptable low-level mathematical primitives. Guards restrict division/remainder to nonnegative values where the stated recurrence applies. |
| Trusted `py2mpy.py` translation | Link from `solution.py` to submitted IR and the claimed AST | Acceptable trusted input. Regeneration was byte-identical, and all five claim ASTs exactly pin that IR. |
| `callBin`, `binDigits`, `binVal`, and `negativeBinVal` as a model of CPython `bin` followed by `[2:]` | Every result-bearing symbolic claim | Transparent, guarded, descending model rather than an opaque oracle. Ordinary induction validates the recurrence; 19 fresh K/Python comparisons and 5,094 candidate/canonical comparisons give independent finite support. The absence of a separate universal connection theorem to CPython is the principal documented concern. |
| Interpretation of the prompt's domain | Intent adequacy | Formal domain is all mathematical integers. This matches the trusted canonical function, but negative strings contain an interior `b`, exposing an ambiguity in the prose's "each character ... `0` or `1`" statement. Non-integer Python protocols and runtime-resource behavior are excluded. |

There are no fresh existential results, opaque proof symbols, proof-local
operational bridges, simplification axioms, priority overrides, empirical rules,
or assumed loop invariants. Differential and concrete testing support only the
translation/model/intent bridges they exercise; they are not substitutes for
the reconstructed `kprove` result.

Gate summary:

- Real-program soundness and non-vacuity: pass.
- Program identity and result constraint: pass.
- Generated-semantics rule soundness on every used construct: pass.
- Natural-language adequacy: legitimate with the documented negative-domain and
  informal universal-model bridge concerns.
- Evidence reproducibility: pass; every preserved audit script/log terminates
  with script exit 0 and outer command exit 0.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
