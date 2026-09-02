# Independent adversarial audit: 44-change-base

The candidate contains a reproducible, non-vacuous K reachability proof of the
exact submitted constructor term under its own idealized semantics. It does not
contain a legitimate proof of the full real HumanEval program contract. The
proved function disagrees with the trusted canonical implementation at `x = 0`
(which satisfies the claim), excludes other prompt-unrestricted integers, and
the generated semantics proves normal return for positive inputs at which the
submitted CPython function raises `RecursionError`.

All candidate and generation artifacts were treated only as untrusted evidence.
All execution used source copies below
`/tmp/audit-work/change-base-audit-20260726`; no candidate-compiled definition
or cache was copied or reused. Reviewer-authored scripts, mutations, and bounded
logs are in `/audit-output/evidence/`.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- problem `44-change-base`, condition `bare`;
- `record_layout = legacy-selected-stage1`;
- `semantics_mode = GENERATED_SEMANTICS`;
- the launcher-owned container paths used in this audit.

The audit campaign block is exactly equal, field for field, to
`/audit-campaign-lock.json`. The independently computed lock hash is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
equal to the hash recorded in `/audit-input.json`.

All records required by `legacy-selected-stage1` are present, readable regular
files: `/run.json`, `/task.json`, `/generation-result.json`,
`invocation.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`,
`prompt.txt`, and the structured trace. `usage.json` is present and was also
inspected. `runtime-metrics.json` is absent, but it is not required for this
legacy layout; historical runtime observations must not be reconstructed.
`legacy-run-input.json` and `legacy-metrics.json` are present and their
generation-result hashes match.

Independent SHA-256 checks match every launcher-recorded file hash, including
the run/task/stage result, prompt, translator, canonical source, generation
records, and trace file. The 163 JSONL trace records all parse. No entry under
the candidate, trusted reference, or generation-evidence trees is a symlink.
The candidate's `prompt.py` and `py2mpy.py` are byte-identical to their trusted
mounted versions. `/reference/reference-semantics` does not exist, as required
in generated-semantics mode. There is no infrastructure breach.

Evidence:

- `evidence/stage1_integrity.py` and `evidence/stage1_integrity.log`
- `evidence/stage1_manifest.log`
- `evidence/stage1_records_raw.log`
- `evidence/stage1_evidence_tree.log`
- `evidence/stage1_generation_claims.log`

The generation log and trace claim that the candidate's original `prove.sh`
closed the proof. That historical claim was not relied upon.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and trusted behavior

The trusted prompt defines `change_base(x: int, base: int)` and asks for the
string representation of `x` in a base less than 10, with examples
`(8,3) -> "22"`, `(8,2) -> "1000"`, and `(7,2) -> "111"`. For meaningful
positional bases, the effective base domain is integers 2 through 9. The prompt
does not state `x > 0` or otherwise exclude zero or negative integers.

The trusted canonical program repeatedly prepends `x % base` while `x > 0`.
Consequently it returns the usual base representation for positive `x` and
returns the empty string for `x <= 0`.

The submitted program is a recursive rewrite:

```python
if x < base:
    return str(x)
return change_base(x // base, base) + str(x % base)
```

It therefore returns `"0"` for zero and a signed decimal string such as `"-1"`
for negative input, unlike the canonical implementation.

### Translator identity

The trusted translator was copied from `/reference/py2mpy.py` and run against
the scratch copy of `solution.py`. The regenerated file has SHA-256
`b24e22f9a8fa6426e18daa45874f69927cd37d6bafc9d57baa94ac29cdab51ad`
and is byte-identical to submitted `solution.mpy`.

Exact command and result are in `evidence/stage2_translation.log`
(`cmp_exit=0`, command exit 0).

### Independent differential execution

`evidence/differential_change_base.py` independently imports the trusted
canonical and submitted entry points. Its deterministic scope is:

- all three documented examples;
- 88 branch/boundary cases across bases 2 through 9;
- every positive `x` from 1 through 512 for every base 2 through 9;
- 1,000 seeded positive generated cases;
- 250 seeded nonpositive generated cases.

Command:

```text
/audit-output/evidence/differential_change_base.py
```

The script intentionally exits 1 on any mismatch. Over 5,437 calls it found
282 mismatches: zero positive mismatches, eight zero-input mismatches, and 274
negative-input mismatches. The first satisfying boundary witness is:

```text
x=0, base=2: canonical='', submitted='0'
```

See `evidence/stage2_differential.log`.

An additional real-execution boundary probe used CPython 3.10.12 with recursion
limit 1000. The canonical loop returns correctly through the tested values,
while the submitted recursive function begins raising `RecursionError` at
`x = 2**997`, `base = 2`. Six of ten tested exponent-boundary cases fail.
See `evidence/python_recursion_boundary.py` and
`evidence/stage2_recursion_boundary.log`.

These are material discrepancies, not merely alternative algorithms. Zero is
inside the candidate theorem's own `X >= 0` domain. The recursion witness is a
positive integer in the unrestricted prompt domain.

## 3. Clean proof reconstruction

The scratch tree was created from source files only. Candidate caches and any
candidate-built definitions were excluded.

### Fresh concrete definition

```text
kompile semantic.k --backend llvm --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition semantic-llvm-kompiled
```

This exited 0. A second LLVM build added `--enable-search` and wrote
`semantic-llvm-search-kompiled`, also exiting 0, so pattern-based comparisons
could be used. Logs:

- `evidence/stage3_kompile_concrete.log`
- `evidence/stage3_kompile_concrete_search.log`

The first batch comparison attempted `krun --pattern` with the non-search LLVM
definition. LLVM rejected that diagnostic option before program execution.
That preserved failure is `evidence/stage3_generated_semantics.log`. The
corrected search-enabled rerun is the evidence used below.

### Fresh proof definition and every positive claim

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-fresh-kompiled
```

This exited 0 (`evidence/stage3_kompile_proof.log`).

There is exactly one positive target claim in `spec.k`. It was run independently:

```text
kprove spec.k --definition verification-fresh-kompiled \
  --spec-module SPEC
```

It printed `#Top` and exited 0
(`evidence/stage3_kprove_positive.log`).

### Generated-semantics concrete execution

`evidence/generated_semantics_differential.py` ran 14 documented, ordinary,
branch-boundary, large, zero, and negative cases through the freshly compiled
LLVM semantics. It generated each expected result independently from submitted
Python and required `krun --pattern` to return `#Top`. All 14 K results match
submitted Python. Four deliberately included nonpositive results differ from
canonical Python. The corrected run exited 0; exact per-case `krun` commands
and results are in `evidence/stage3_generated_semantics_rerun.log`.

At the recursion boundary, fresh K execution for `x = 2**997`, `base = 2`
returns the canonical 998-character binary string and prints `#Top`, while the
submitted CPython function raises `RecursionError`. Exact inputs and the exact
K command are in `evidence/k_recursion_boundary.py` and
`evidence/stage5_k_recursion_boundary.log`.

The reconstruction gate therefore passes as a statement about the supplied K
theory, but the concrete comparison exposes a real-Python modeling gap.

## 4. Adequacy and real-program pinning

### Plain-language claim

The sole entry claim assumes a mathematical integer `X >= 0`, an integer base
`2 <= B <= 9`, and an arbitrary K continuation `CONT`. It executes a call to a
one-function `Module` binding `change_base(x, base)` to the submitted recursive
body. Its postcondition requires the call to be replaced by exactly
`strVal(baseString(X,B))`, followed by the same `CONT`.

The result is not free, existential, tautological, or guarded by a one-way
implication. There are no helper or loop claims.

### Mechanical program identity

`evidence/claim_program_identity.py` extracts the balanced `Module(...)`
constructor from `spec.k`, parses both it and regenerated `solution.mpy` using
the freshly built K parser, and compares canonical JSON KASTs. K's explicit
`.Stmts` spelling was normalized to the equivalent empty
`List{Stmt,""}` concrete field. Both KASTs have SHA-256
`113cd71e26be25511487dade3d8a70103494edcfbae00c5575dfd358b78019ac`;
constructor-level identity is true
(`evidence/stage4_program_identity_normalized.log`). The earlier unnormalized
program-parser rejection of internal `.Stmts` syntax is preserved in
`evidence/stage4_program_identity.log`.

Thus the claim executes the actual translated submitted body. It does not
prove a substituted summary program.

### Satisfying states and ground substitution

`X=8`, `B=3`, `CONT=.K` satisfies the precondition. The claimed recurrence,
submitted Python, and canonical Python all yield `"22"`.

`X=0`, `B=2`, `CONT=.K` also satisfies the precondition. The claimed recurrence
and submitted Python yield `"0"`; canonical Python yields `""`. These
substitutions are recorded in
`evidence/ground_claim_substitution.py` and
`evidence/stage4_ground_substitution.log`.

### Body sensitivity

The reviewer-authored `evidence/spec-body-mutation.k` changes the function term
actually executed by the claim: its base branch returns `str(base)` instead of
`str(x)`, while the postcondition remains unchanged. `kprove` exits 1 with a
reachable stuck implication requiring `Int2String(B) = Int2String(X)`.
This is the expected body-sensitive failure; see
`evidence/stage4_body_sensitivity.log`.

### Adequacy decision

Program pinning and result constraint pass, but intent adequacy fails:

1. a satisfying zero input proves a result different from the trusted
   canonical behavior;
2. negative integers are omitted by `X >= 0` despite no such prompt
   restriction;
3. the theorem covers arbitrarily large mathematical integers, but the real
   submitted recursive CPython program raises a reachable `RecursionError`.

Even if one informally chose to exclude negative inputs, the first and third
defects remain.

## 5. Rule-by-rule static soundness review

The exhaustive source inventory is also preserved in
`evidence/RULE-INVENTORY.md`. Machine-extracted declaration/rule locations and
counts are in `evidence/stage5_inventory.log`: 23 rules in `semantic.k`, two
rules in `verification.k`, and one claim in `spec.k`.

### Local declaration inventory

| ID | Declaration | Scope and decision |
|---|---|---|
| D1 | `Program ::= Module(Stmts)` | Exact submitted top-level form. |
| D2 | `Stmts ::= List{Stmt,""}` | Ordered statement sequence, including `.Stmts`. |
| D3 | `Stmt ::= FuncDef \| If \| Return` | Covers every submitted statement. |
| D4 | two-string `Params` | Covers the exact two-argument entry/recursive signature. |
| D5 | comma-separated `Exprs` | Covers one- and two-argument calls. |
| D6 | `Expr ::= Name \| Int \| BinOp \| Compare \| Call` | Covers every submitted expression; `Int` is unused. |
| D7 | `CmpOp(String,Expr)` | Covers submitted `<`. |
| D8 | `Value ::= intVal \| strVal \| boolVal` | Adequate for this pure program. |
| D9 | `appendStmts(Stmts,Stmts) [function]` | Definitional list append. |
| D10 | 11 internal KItems | Explicit evaluation/control frames; none is opaque. |
| D11 | one `<k>`-cell configuration | Adequate for the body's pure state footprint. |
| D12 | `baseString(Int,Int) [function] : String` | Definitional summary, not an execution-replacing bridge. |
| C1 | sole reachability claim | Exact body, constrained result, arbitrary preserved continuation. |

There are no local `total`, `functional`, simplification, priority, `owise`,
`anywhere`, macro, or opaque declarations/rules. The two `[function]`
declarations are D9 and D12.

### Every local rule

| ID | Location | Decision |
|---|---|---|
| S1 | `semantic.k:37` | Empty-list append is a true equation. |
| S2 | `semantic.k:38` | Nonempty append is true, decreases the first list, and is disjoint from S1. |
| S3 | `semantic.k:59-65` | Function selection/binding is faithful for the exact sole submitted binding and distinct parameters. |
| S4 | `semantic.k:67` | General Python fall-through should yield `None`, not `strVal("")`. A hypothetical empty/fall-through body is a counterexample, but no satisfying submitted-program input reaches this rule because both actual paths encounter `Return`. This is an off-target modeling limitation, not an intended-domain false-proof witness. |
| S5 | `semantic.k:72` | Return evaluates its expression, discards remaining statements, and preserves the outer K continuation. |
| S6 | `semantic.k:74-78` | If guard is evaluated before branching. |
| S7 | `semantic.k:79-83` | True branch is prepended to the remaining statements correctly. |
| S8 | `semantic.k:84-88` | False branch is prepended correctly. |
| S9 | `semantic.k:91` | Integer literal evaluation is truthful but unused. |
| S10 | `semantic.k:92` | Bound-name map lookup is correct; unsupported unbound access stops. |
| S11 | `semantic.k:95-99` | Comparison left operand is evaluated first. |
| S12 | `semantic.k:100-104` | Comparison right operand is evaluated second with the left value retained. |
| S13 | `semantic.k:105-106` | Computes the correctly oriented `I <Int J`. |
| S14 | `semantic.k:109-113` | Binary left operand is evaluated first. |
| S15 | `semantic.k:114-118` | Binary right operand is evaluated second with the left value retained. |
| S16 | `semantic.k:119-121` | `/Int` agrees with Python `//` on used nonnegative numerator/positive denominator states. |
| S17 | `semantic.k:122-124` | `%Int` agrees with Python `%` on the same states. |
| S18 | `semantic.k:125-126` | String concatenation is faithful and order-correct. |
| S19 | `semantic.k:129-133` | One-argument `str` evaluates its argument and selects the unshadowed builtin in this closed module. |
| S20 | `semantic.k:134` | `Int2String` matches Python integer string conversion for reachable base-case values. |
| S21 | `semantic.k:136-140` | Ordinary call argument 1 evaluates first. |
| S22 | `semantic.k:141-145` | Argument 2 evaluates second while retaining argument 1. |
| S23 | `semantic.k:146-150` | Recursive invocation selects the exact module binding and preserves the caller continuation. |
| V1 | `verification.k:11-12` | `baseString(X,B) = Int2String(X)` under `X < B` is true. |
| V2 | `verification.k:14-16` | Quotient recurrence is true; under `B >= 2`, `X /Int B` strictly decreases. |

V1 and V2 have disjoint guards and cover every use in C1. D12 is not declared
total outside that domain. S1/S2 likewise have disjoint constructors and
terminate. There is no operational bridge, task-answer rewrite of a program
term, unconstrained oracle, or circular reuse of an opaque result. The program
body executes, and C1 itself supplies the universal execution-to-`baseString`
connection.

Construct mapping is complete: submitted `Module`, `FuncDef`, `Params`, `If`,
`Compare`, `Name`, `CmpOp("<")`, `Return`, one-argument `str`, two-argument
recursive `Call`, `//`, `%`, `+`, and empty/nonempty statement lists map to
D1-D7 and S1-S3, S5-S8, S10-S23. S4 and S9 are the only operational rules not
needed by the submitted body.

The material static limitation is the execution model, not a smuggled proof
rule: recursive calls use an unbounded K continuation and omit CPython
recursion-limit exceptions. The concrete false-conclusion witness is
`X=2**997`, `B=2`: C1 and K execution produce a string, but the real submitted
CPython function raises `RecursionError`.

## 6. Fresh non-vacuity test

The candidate did not supply a vacuity spec. The fresh
`evidence/spec-audit-vacuity.k` preserves the exact program and precondition but
changes the postcondition to:

```text
strVal(baseString(X,B) +String "0") ~> CONT
```

`X=8`, `B=3`, `CONT=.K` is a satisfying witness: the real result is `"22"`,
not `"220"`.

Build/parse check:

```text
kprove spec-audit-vacuity.k \
  --definition verification-fresh-kompiled \
  --spec-module SPEC-AUDIT-VACUITY --dry-run
```

It exited 0 and emitted a valid `kore-exec --prove` command
(`evidence/stage6_vacuity_build.log`).

Actual mutation proof:

```text
kprove spec-audit-vacuity.k \
  --definition verification-fresh-kompiled \
  --spec-module SPEC-AUDIT-VACUITY
```

It exited 1 with `WarnStuckClaimState`. The residual is the expected reachable
unmet equality:

```text
Int2String(X) +String "0" = Int2String(X)
```

See `evidence/stage6_vacuity_proof.log`. This is a meaningful semantic
rejection, not a parser error, timeout, missing import, or unreachable mutation.
The original proof is non-vacuous.

## 7. Proven versus assumed accounting

### What is formally proven

Under the candidate's K definition and K's imported domain theory, for every
mathematical integer `X >= 0`, integer `2 <= B <= 9`, and K continuation
`CONT`, executing the exact submitted `change_base` constructor reaches
`strVal(baseString(X,B)) ~> CONT`. The recurrence means:

- if `X < B`, the result is `Int2String(X)`;
- otherwise it is the quotient's representation followed by the single
  decimal remainder digit.

This is result-constraining and body-sensitive. It proves the submitted
recursive algorithm's idealized, unbounded-stack behavior; it is not merely a
test result or an assumed summary.

### Trust and assumption ledger

| Boundary | Influence | Status |
|---|---|---|
| K 7.1.293 toolchain, Haskell prover/backend, LLVM executor | Parsing, rewriting, reachability closure | Ordinary proof-checker trust boundary; version and fresh commands recorded. |
| Imported `INT`, `BOOL`, `STRING`, `MAP` domains | Arithmetic, comparisons, strings, maps | Trusted K primitives. Relevant operations are `/Int`, `%Int`, `<Int`, comparisons, `Int2String`, `+String`, Boolean connectives, and map construction/lookup. |
| Trusted `py2mpy.py` | Python-to-constructor identity | Byte-checked trusted input; fresh regeneration and KAST comparison mechanically pin the submitted body. |
| Candidate `semantic.k` | Meaning of every program construct | Not externally supplied or blessed. Audited rule by rule and finitely tested. It is faithful for ordinary target executions but idealizes call-stack depth. |
| `baseString` equations | Final value | Fully defined by disjoint equations on every formal use; not opaque and not an operational bridge. C1 proves the execution connection. |
| Python/K intent bridge | Whether the K subset is the real Python execution model | Informal plus finite differential evidence only; refuted at the CPython recursion boundary. |
| Candidate/canonical equivalence | Whether the implementation meets the HumanEval source contract | Finite differential evidence refutes it at zero and negatives; no assumption can erase those concrete witnesses. |

There are no candidate-local opaque symbols or empirical oracles. Differential
tests support only their finite scopes; they are not substitutes for C1.

### Gate accounting and decision

- Fresh verification: **passes** (`#Top`, exit 0).
- Program constructor identity, result constraint, and body sensitivity:
  **pass**.
- Local extension/equation soundness for the idealized subset: **passes**.
- Non-vacuity: **passes**.
- Real-language model adequacy: **fails** because reachable CPython recursion
  failure is omitted.
- Source-contract/canonical adequacy: **fails** at a satisfying zero input and
  by excluding prompt-unrestricted negative integers.
- Evidence reproducibility: **passes**; exact scripts, commands, exit statuses,
  and bounded logs are preserved.

At best, the successful K run is a sound theorem about a materially narrowed,
idealized domain. Under the benchmark's explicit mapping, such
`SOUND-BUT-LIMITED` progress is not a legitimate proof of the unrestricted
HumanEval contract. The concrete zero and recursion witnesses independently
make the candidate inadequate, even though its internal K theorem is genuine
and non-vacuous.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
