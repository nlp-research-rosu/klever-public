# Independent adversarial audit: 38-decode-cyclic

The candidate is **not a legitimate proof of the real Python program over its
stated `str` domain**.  Fresh reconstruction confirms that the K claims close,
the specification constrains the result, the translated program is pinned
exactly, and a false-result mutation is rejected.  The fatal defect is instead
in the candidate-generated language semantics: its `STRING` hooks count and
slice the backend representation rather than Python Unicode code points for
characters outside the Latin-1 range.  This changes the submitted program's
result on ordinary valid Python strings.  The smallest full-program witness
used here is `S = "中"`: both Python implementations return `"中"`, whereas
fresh `krun` returns `pyStr("\xad\xe4\xb8")`.

All candidate material, including its prior `#Top`, was treated as untrusted.
Only source files were copied to
`/tmp/audit-work/38-decode-cyclic-audit`; candidate kompiled definitions and
caches were not used.

## 1. Input and provenance integrity

The rendered mode is `GENERATED_SEMANTICS`.  The trusted mount
`/reference/reference-semantics` is absent, as required.  There is therefore no
mode/mount contradiction and no audit-infrastructure breach.

The candidate prompt and translator are byte-identical to the trusted inputs:

- `prompt.py` SHA-256:
  `76b76b6f211ef2f4243678ddb1df6013ceac62da09fefe7bc38ba55e404a1ef8`
  in both trees.
- `py2mpy.py` SHA-256:
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`
  in both trees.
- Recursive symlink inspection found no candidate symlinks.

All required source deliverables are present as regular files:
`solution.py`, `solution.mpy`, `semantic.k`, `verification.k`, `spec.k`, and
`prove.sh`.  No helper K file is referenced or required.  `PROOF.md` is absent,
but it was not a deliverable in the generation prompt and its absence does not
affect reconstruction.  The candidate additionally contains `__pycache__`,
`semantic-kompiled`, generation logs, metrics, and a structured JSONL trace.
Those are extra untrusted evidence rather than source-integrity failures; the
compiled directory was deliberately ignored.

I read `run-input.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, and the structured trace as claims only.  They report a
successful generation, five concrete examples, `#Top`, and 2,020 Python
property checks.  None was used as proof evidence.  Exact types, hashes,
selected claims, and the trace's structural summary are preserved in
[01-provenance.log](/audit-output/evidence/01-provenance.log); the reproducing
script is [01_provenance.sh](/audit-output/evidence/01_provenance.sh).

Stage 1 result: integrity checks pass; no infrastructure error.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementation

`encode_cyclic` partitions a Python string into consecutive groups of three,
rotates each complete group one place to the left, and leaves a final group of
length zero, one, or two unchanged.  `decode_cyclic` must invert that mapping.
The trusted canonical implementation applies `encode_cyclic` twice, which
rotates every complete triple one place to the right and leaves the short
suffix unchanged.  Because the transformation is bijective on strings,
"encoded with `encode_cyclic`" does not narrow the domain: every Python `str`
is a possible encoded input.  The prompt supplies no explicit decode examples
and no ASCII-only or Latin-1-only precondition.

The submitted implementation:

```python
result = ""
i = 0
while i + 2 < len(s):
    result = result + s[i + 2] + s[i:i + 2]
    i = i + 3
return result + s[i:]
```

is a correct direct right-rotation algorithm under Python semantics.  It
handles the zero-iteration lengths 0, 1, and 2, every suffix class, repeated
iterations, and Unicode code points correctly.

### Trusted translation

Running the trusted translator from `/reference/py2mpy.py` on the scratch copy
of `solution.py` produced a file byte-identical to submitted `solution.mpy`.
Both have SHA-256
`3d2fa824ef26d25a4275888898b0c5cb30c7d70fe71b6e7df714e0c42199a11f`.
The command and exit-0 `cmp` are in
[03-build-fresh.log](/audit-output/evidence/03-build-fresh.log).

### Independent differential test

[02_differential.py](/audit-output/evidence/02_differential.py) imports
`/reference/canonical.py` and the scratch copy of `solution.py` under distinct
module names.  It tested:

- explicit empty, loop, suffix, control-character, Unicode, and long cases;
- every length boundary from 0 through 8;
- all strings of lengths 0 through 7 over `{"a", "é", "🙂"}`;
- 25 deterministically generated strings at every length 0 through 128,
  using seed 380038; and
- both direct equality with the canonical function and
  `candidate.decode_cyclic(canonical.encode_cyclic(s)) == s`.

There were 6,496 unique inputs, zero direct mismatches, and zero inverse
mismatches.  The exact generated corpus is
[02-differential-inputs.json](/audit-output/evidence/02-differential-inputs.json)
(SHA-256
`f9d0106dc022e614a0311540aa3c0aa7d404df5e0934d39eacb134a88e54746d`);
commands and results are in
[02-differential.log](/audit-output/evidence/02-differential.log).
This finite evidence supports Python implementation fidelity only.  It does
not validate the K semantics or replace the K proof.

Stage 2 result: the submitted Python program and `.mpy` translation are
faithful.

## 3. Clean proof reconstruction

### Fresh definitions

K version `v7.1.293` and Python `3.10.12` were used.  The source-only builds
were:

```text
kompile .../semantic.k --backend llvm --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition .../build-concrete/semantic-llvm-kompiled
# exit 0

kompile .../verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition .../build-proof/verification-kompiled
# exit 0
```

The full commands and outputs are in
[03-build-fresh.log](/audit-output/evidence/03-build-fresh.log).  Neither
command names or reads `/candidate/semantic-kompiled`.

### Positive claims

The loop claim was proved alone, then the complete two-claim target was proved
so that `program-correct` could use `loop-correct` as its circularity:

```text
kprove .../spec.k --definition .../verification-kompiled \
  --spec-module SPEC --claims SPEC.loop-correct
#Top
# exit 0

kprove .../spec.k --definition .../verification-kompiled \
  --spec-module SPEC
#Top
# exit 0
```

See [04-prove-positive.log](/audit-output/evidence/04-prove-positive.log) and
the raw exact outputs
[04-loop-correct.raw.log](/audit-output/evidence/04-loop-correct.raw.log) and
[04-complete-target.raw.log](/audit-output/evidence/04-complete-target.raw.log).
Selecting only `program-correct` removes its loop circularity and does not
represent the candidate target; the stopped diagnostic is preserved separately
in
[04-program-only-filter-diagnostic.log](/audit-output/evidence/04-program-only-filter-diagnostic.log).

Thus the candidate's positive K-verification claim is reproducible.

### Fresh concrete execution

Fresh LLVM execution agrees with both Python implementations on empty strings,
all ASCII branch and suffix boundaries, multiple iterations, NUL, and ASCII
control characters.  It materially diverges on valid non-Latin-1 Unicode.
For example:

```text
input Python "中"
K result:                  pyStr ( "\xad\xe4\xb8" )
submitted Python result:  "中"
trusted canonical result: "中"

input Python "中ab"
K result:                  pyStr ( "\xad\xe4\xb8ab" )
submitted Python result:  "b中a"
trusted canonical result: "b中a"
```

All `krun` commands themselves exit 0; the comparison driver exits 1 because
five of 18 K/Python comparisons differ.  Exact configurations and values are
in
[03-concrete-compare.log](/audit-output/evidence/03-concrete-compare.log), with
the driver in
[03_concrete_compare.py](/audit-output/evidence/03_concrete_compare.py).
The same two decisive observations were then rerun against the freshly built
Haskell proof definition: it also returns `pyStr("\xad\xe4\xb8")` for the full
program on `"中"` and `pyInt(3)` for `len("中")`.  See
[05-backend-consistency.log](/audit-output/evidence/05-backend-consistency.log)
and
[05_backend_consistency.sh](/audit-output/evidence/05_backend_consistency.sh).
The defect is therefore present in the theory used by `kprove`, not merely in
the LLVM concrete backend.

Stage 3 result: fresh compilation and positive proof reconstruction pass, but
fresh semantic execution exposes a candidate defect rather than an audit
infrastructure failure.

## 4. Adequacy and real-program pinning

### Claims in plain language

`loop-correct` starts with exactly:

- `whileLoop(decodeTest, decodeBody) ~> exec(decodeReturn)` in `<k>`;
- an environment containing only `s = pyStr(S)`, `i = pyInt(I)`, and
  `result = pyStr(ACC)`;
- `noResult`; and
- the precondition `0 <= I <= lengthString(S)`.

It claims that, if execution terminates, computation and environment are
consumed and the result is exactly
`pyStr(decodeFrom(S, I, ACC))`.  The comment that `ACC` is an already-decoded
prefix is not encoded as a precondition, but that is not vacuity: the claim is
stronger and is true in the candidate K model for arbitrary `ACC`.

`program-correct` has no side condition.  It starts from
`run(solutionProgram, S)`, an empty environment, and `noResult`, and claims an
empty computation/environment with the exact result
`pyStr(decodeFrom(S, 0, ""))`.  The result is neither free nor related through
a one-way implication.

### Exact program and control-flow pinning

[05_pinning_and_witnesses.py](/audit-output/evidence/05_pinning_and_witnesses.py)
independently derives terms using the trusted translator.  After whitespace
normalization:

- `solutionProgram` exactly equals the full submitted `.mpy`;
- `decodeTest` exactly equals the real `while` guard;
- `decodeBody` exactly equals the two real loop-body assignments; and
- `decodeReturn` exactly equals the real final return.

All four comparisons have equal SHA-256 pairs.  A fresh execution at depth 63
on `S = "bcaefdgh"` reaches the exact loop-claim control shape with
`I = 3`, `ACC = "abc"`, `noResult`, and the real return continuation.  This
rules out a substituted program or dead helper claim.  Evidence is in
[05-pinning-and-witnesses.log](/audit-output/evidence/05-pinning-and-witnesses.log).

### Satisfiable preconditions and ground substitution

The program entry precondition is `true`; `S = "bcaefdgh"` is a witness.
Substitution gives:

```text
decodeFrom("bcaefdgh", 0, "") = "abcdefgh"
submitted Python                 "abcdefgh"
trusted canonical Python         "abcdefgh"
```

The reachable loop witness
`S = "bcaefdgh", I = 3, ACC = "abc"` satisfies `0 <= 3 <= 8`.
Substitution gives:

```text
decodeFrom("bcaefdgh", 3, "abc") = "abcdefgh"
submitted full Python program       "abcdefgh"
trusted canonical Python            "abcdefgh"
```

These ASCII witnesses establish nonempty formal entry sets and correct claim
shape.  They do not cure the missing Python/K Unicode bridge.

Stage 4 result: real AST and control-flow pinning, satisfiability, and result
constraint pass.  Adequacy to the real Python string domain fails.

## 5. Rule-by-rule static soundness review

The complete numbered source and machine-generated declaration index are in
[05-static-inventory.log](/audit-output/evidence/05-static-inventory.log).
There are 17 syntax headers, 40 rules in `semantic.k`, three simplification
rules in `verification.k`, and two claims.  There are no local priority,
`owise`, `anywhere`, `concrete`, `functional`, opaque, or `trusted`
declarations.

### Local syntax, functions, and configuration

| Lines | Declaration | Audit |
|---|---|---|
| `semantic.k:7` | `Py ::= Module(Stmts)` | Exact top-level constructor used by `.mpy`. |
| `:9` | `Stmts ::= List{Stmt,""}` | Exact juxtaposed statement-list representation emitted by the translator. |
| `:10-13` | `Stmt ::= FuncDef \| Assign \| While \| Return` | Every submitted statement form is covered; unused forms remain unmodeled, which is permitted in generated mode. |
| `:15` | one-string `Params` | Exactly the submitted entry signature. |
| `:17-23` | `Expr ::= Name \| Str \| Int \| BinOp \| Compare \| Call \| Subscript` | Exactly the submitted expression constructors. |
| `:25` | `CmpOp(String,Expr)` | Covers the submitted one-link `<` comparison. |
| `:26-28` | `Index ::= Expr \| Slice`; `Slice`; `Bound ::= Expr \| NoBound` | Covers the one integer index, bounded slice, and tail slice. |
| `:38` | `Val ::= pyInt \| pyStr \| pyBool` | Sufficient value domain for the target. |
| `:39` | `Result ::= noResult \| Val` | Explicit observable result state. |
| `:41-59` | 19 `KItem` continuations | `run`, `exec`, `eval`, stores, binary/comparison continuations, `len`, index/slice continuations, loop continuations, and return are all used consistently. |
| `:61-64` | `<k>`, `<env>`, `<result>` configuration | These are exactly the control, local bindings, and return value needed; the target has no heap, allocation, I/O, exception, or user-call state. |
| `:133` | `solutionProgram [function,total]` | One unguarded constant equation; totality is justified and its RHS is mechanically exact. |
| `:162` | `decodeFrom [function]` | Deliberately not declared total.  Its two guarded equations cover every use under the claims' bounds. |
| `:179`, `:194`, `:200` | `decodeBody`, `decodeTest`, `decodeReturn [function,total]` | One unguarded exact equation each; totality is justified. |

The submitted constructor inventory is `Module`, `FuncDef`, `Params`,
`Assign`, `Name`, `Str`, `Int`, `While`, `Compare`, `CmpOp`, `BinOp`, `Call`,
`Subscript`, `Slice`, and `Return`.  The following rule inventory maps all of
them to behavior.

### All 40 semantic rules

| ID and lines | Rule role | Decision |
|---|---|---|
| S1 `66-68` | Match the exact `decode_cyclic(s)` module and bind `s`. | Sound for the only submitted top level; exact name, arity, and body are required. |
| S2 `70` | Empty `exec` consumes itself. | Sound. |
| S3 `71` | Split first statement from the remaining list. | Sound sequential order. |
| S4 `73` | Evaluate assignment RHS before store. | Sound for `Name` targets used here. |
| S5 `74-75` | Update the local map at the assigned name. | Sound for target locals. |
| S6 `77` | Lower `While` to `whileLoop`. | Sound. |
| S7 `78` | Evaluate the guard, retaining test/body. | Sound and returns to the invariant loop head. |
| S8 `79-80` | On true, execute the whole body then recur. | Sound Python while order. |
| S9 `81` | On false, exit the loop. | Sound. |
| S10 `83` | Evaluate return expression before `doReturn`. | Sound. |
| S11 `84-86` | Store returned value, clear locals, discard the target's remaining function continuation. | Sound on every reachable target state.  It would not model a caller stack, but no user-function call rule or caller frame exists in this deliberately minimal language. |
| S12 `88` | String literal to `pyStr`. | Sound as a K literal injection; the later K/Python representation bridge is not sound for all Unicode. |
| S13 `89` | Integer literal to `pyInt`. | Sound; K and Python integers are unbounded here. |
| S14 `90-91` | Name lookup in `<env>`. | Sound on the initialized target states. |
| S15 `93` | Evaluate binary left operand first. | Sound left-to-right order. |
| S16 `94` | Evaluate binary right operand second and remember left value. | Sound left-to-right order. |
| S17 `95` | Integer `+` via `+Int`. | Sound for Python integers. |
| S18 `96` | String concatenation via `+String`. | Concatenation itself preserves the candidate representation and agrees on valid representable substrings; it propagates bad fragments created by S24/S27/S31/S34. |
| S19 `98-99` | Evaluate comparison left operand first. | Sound. |
| S20 `100` | Evaluate comparison right operand second. | Sound. |
| S21 `101-102` | Integer `<` true branch. | Sound. |
| S22 `103-104` | Integer `<` false branch. | Sound; S21/S22 guards are disjoint and exhaustive over integers. |
| S23 `106` | Evaluate the argument of the exact built-in `len` binding. | Binding and evaluation order are sound. |
| S24 `107` | Python string `len` is modeled by K `lengthString`. | **Unsound for the intended Python domain.**  Witness: input `"中"` gives K `pyInt(3)` but Python `len("中") == 1`. |
| S25 `109-110` | Evaluate indexed base before integer index. | Sound order; the `IDX:Expr` sort excludes slices. |
| S26 `111` | Evaluate integer index after base. | Sound order. |
| S27 `112-114` | Index via `substrString(S,I,I+1)`. | **Unsound for the intended Python domain.**  Witness: `"中"[0]` is Python `"中"`, while K returns `pyStr("\xe4")`. |
| S28 `116-117` | Evaluate bounded-slice base. | Sound order and sort-disjoint from S25/S32. |
| S29 `118` | Evaluate lower bound after base. | Sound order. |
| S30 `119` | Evaluate upper bound after lower. | Sound order. |
| S31 `120-122` | Bounded slice via `substrString`. | **Unsound for the intended Python domain.**  Witness: Python `"中x"[0:1] == "中"` while K returns `pyStr("\xe4")`. |
| S32 `124-125` | Evaluate tail-slice base. | Sound order and pattern-disjoint from bounded slice. |
| S33 `126` | Evaluate tail lower bound. | Sound order. |
| S34 `127-129` | Tail slice via `substrString`. | **Unsound for the intended Python domain.**  Witness: Python `"中x"[1:] == "x"` while K returns `pyStr("\xb8\xadx")`. |
| S35 `134-158` | Expand `solutionProgram`. | Sound definitional macro; exact trusted-translation equality was checked. |
| S36 `163-171` | Recursive `decodeFrom` triple step. | Internally truthful over the candidate K string operations.  Its guard implies `I+3 <= lengthString(S)` and the remaining-length measure decreases by three.  It is not a valid Python-code-point specification because it inherits S24/S27/S31/S34. |
| S37 `173-177` | Base `decodeFrom` appends the short suffix. | Internally truthful; guard is disjoint from S36 and, with `I <= length`, covers the complementary claimed states.  It inherits the same adequacy failure. |
| S38 `180-192` | Expand `decodeBody`. | Sound exact macro for the real two assignments. |
| S39 `195-198` | Expand `decodeTest`. | Sound exact macro for the real guard. |
| S40 `201-206` | Expand `decodeReturn`. | Sound exact macro for the real return. |

The four false-conclusion witnesses above are generated from focused Python
programs by the trusted translator and then executed with the fresh LLVM
definition.  All four expected divergences were observed; commands and exact
outputs are in
[05-unicode-rule-witnesses.log](/audit-output/evidence/05-unicode-rule-witnesses.log),
the driver is
[05_unicode_rule_witnesses.py](/audit-output/evidence/05_unicode_rule_witnesses.py),
and the source witnesses are under
[unicode-witnesses](/audit-output/evidence/unicode-witnesses/).
These are concrete witnesses that the affected rules enable false conclusions
on the intended domain, not merely missing evidence.

Apart from the Unicode group, the operational patterns are constructor- or
sort-disjoint.  The two `<` guards are disjoint/exhaustive; bounded, tail, and
integer-subscript patterns do not overlap; and the two `decodeFrom` guards are
disjoint and cover its claimed bounded domain.  Unsupported operators or
constructors stop visibly instead of being fabricated.  No priority rule
preempts normal execution.

### All three verification rules

| ID and lines | Rule | Decision |
|---|---|---|
| V1 `verification.k:9-11` | Equal updates of the same map/key imply equality of the updated values. | Sound by extensional map equality: lookup at that same key yields each value.  It does not replace program execution. |
| V2 `:13` | `0 <= lengthString(S)` simplifies to true. | Sound for K strings. |
| V3 `:14` | `substrString(S,0,lengthString(S)) = S`. | Sound identity in the candidate K string theory. |

All three are simplifications.  There are no ordinary proof-only operational
bridges, opaque result symbols, priorities, or `trusted` claims.  `decodeFrom`
is result-bearing, but it is not an unconstrained oracle: fixed K execution is
connected to it by the loop reachability claim.  The problem is that both sides
use the same inadequate string model, so the connection does not establish
Python behavior.

Stage 5 result: local symbolic reasoning is internally sound, but the
generated semantics contains four materially unsound Python-string rules with
explicit intended-domain witnesses.  The full-program `"中"` witness shows
that these rules make the proved K result differ from the real program result.

## 6. Fresh non-vacuity test

I did not rely on a candidate mutation (none was supplied).  The fresh scratch
mutation in
[06-spec-vacuity.k](/audit-output/evidence/06-spec-vacuity.k) retains the real
loop circularity but changes the end-to-end destination to:

```k
pyStr(decodeFrom(S, 0, "") +String "!")
```

The entry state `S = ""` satisfies the original unconditional precondition.
Real execution and the original claim require `""`; the mutation requires
`"!"`.

`kprove --dry-run` exited 0, establishing successful parsing and claim
compilation.  The actual proof exited 1 with `WarnStuckClaimState`; its
residual explicitly contains:

```text
decodeFrom(S,0,"") +String "!" #Equals decodeFrom(S,0,"")
```

and reports that the implication check failed.  It was not a parser error,
missing import, timeout, or unrelated crash.  Commands and bounded output are
in [06-nonvacuity.log](/audit-output/evidence/06-nonvacuity.log), with raw
outputs in
[06-nonvacuity-dry-run.raw.log](/audit-output/evidence/06-nonvacuity-dry-run.raw.log)
and
[06-nonvacuity-proof.raw.log](/audit-output/evidence/06-nonvacuity-proof.raw.log).

Stage 6 result: non-vacuity and result sensitivity pass.

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Under the candidate's K definition and local simplifications, the successful
proof establishes this partial-correctness statement:

> For every K `String` value `S`, if execution of the exact
> trusted-translated `solutionProgram` from the initial K configuration
> terminates, the final K result is
> `pyStr(decodeFrom(S,0,""))`; similarly, every loop state satisfying
> `0 <= I <= lengthString(S)` terminates, if it terminates, with
> `pyStr(decodeFrom(S,I,ACC))`.

It does not prove termination.  It also does not prove that `decodeFrom` is
the inverse of the prompt's Python `encode_cyclic`; that bridge is an informal
mathematical reading plus finite differential evidence.

### Trust and assumption ledger

| Boundary | Influence | Accounting |
|---|---|---|
| K toolchain and Haskell/LLVM backends | Parsing, concrete execution, and symbolic closure | Ordinary unavoidable proof-tool trust; both backends were rebuilt from source. |
| Imported `INT`, `BOOL`, `MAP`, `STRING`, and `MAP-SYMBOLIC` modules | All primitive arithmetic, strings, maps, and solver reasoning | Acceptable low-level K trust in itself, but using K `STRING` hooks as Python `str` operations needs a bridge. |
| Trusted `/reference/py2mpy.py` | Program AST identity | Acceptable and byte-checked; the submitted `.mpy` and all proof macros match it. |
| S1-S40 generated language semantics | The meaning of the submitted program | This is part of what had to be audited, not a trusted primitive.  S24/S27/S31/S34 fail with concrete Python witnesses and affect control and the returned value. |
| `decodeFrom` | Final postcondition | Defined by guarded, descending K equations and connected to K execution; not opaque.  Its identification with the human-facing Python inverse is not machine-proved and, for non-Latin-1 Unicode, is false under this K model. |
| V1-V3 simplifications | Symbolic claim closure | Audited as truthful K equations; no operational execution is bypassed. |
| Python differential corpus | Candidate-vs-canonical intent bridge | Reproducible finite evidence for 6,496 inputs, including Unicode; it supports the Python program but cannot repair or replace the K proof. |
| Concrete K/Python comparisons | Generated-semantics bridge | ASCII cases support a restricted bridge.  Valid Unicode counterexamples refute the unrestricted bridge required by the prompt. |

There are no opaque symbols, unconstrained fresh results, proof-local
operational bridges, priorities, or trusted reachability claims.  The proof's
formal result is real and discriminating.  Nevertheless, the actual theorem is
about an incorrect generated model of Python strings.  The prompt's formal
domain has no restriction excluding `"中"`, and the program's loop guard,
index, bounded slice, tail slice, and final result all depend on the defective
rules.  This is a material real-program soundness failure, not merely thin
evidence or an informal-intent concern.

Gate summary:

- Real-program soundness: **FAIL** because the generated semantics changes
  observable results on satisfying intended-domain inputs.
- Intent adequacy: **FAIL** for the same unrestricted Python `str` mismatch;
  the inverse property is also only informally related to `decodeFrom`.
- Evidence auditability: **PASS**; source builds, positive proofs, pinning,
  differentials, counterexamples, and mutation are reproducible.

Accordingly, the decision boundary requires `FAIL / NOT_LEGIT`: a clean
`#Top`, exact AST pinning, and non-vacuity cannot legitimize materially unsound
semantics.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
