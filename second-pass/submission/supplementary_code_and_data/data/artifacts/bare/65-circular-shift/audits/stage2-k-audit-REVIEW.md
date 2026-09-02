# Independent adversarial audit: 65-circular-shift

The candidate's proof reconstructs and is non-vacuous, but it is not a
legitimate proof of the full real-program contract. The decisive defect is
domain adequacy: the two symbolic entry claims cover `shift >= 0` only, although
the trusted prompt and canonical program impose no such precondition. Negative
shifts are a real, infinite part of the integer input domain and the submitted
program has definite behavior there. Under the benchmark's explicit mapping, a
sound-but-materially-limited HumanEval theorem is `FAIL / NOT_LEGIT`.

There is also a real-program semantics discrepancy on the candidate's formally
unbounded `x` domain. The generated `str(int)` rule always returns
`Int2String(I)`, but CPython 3.10.12 in this audit has the default 4,300-digit
conversion limit. For a 4,301-digit integer and `shift = 0`, both the submitted
and canonical Python functions raise `ValueError`, while the fresh K semantics
returns a 4,301-character string. This is a concrete false-behavior witness for
the unguarded rule on an input admitted by the symbolic claim.

All candidate prose, generation traces, and prior success reports were treated
only as untrusted evidence.

## 1. Input and provenance integrity

The infrastructure gate passes.

- `/audit-input.json` declares `record_layout:
  legacy-selected-stage1`, condition `bare`, problem
  `65-circular-shift`, and `semantics_mode: GENERATED_SEMANTICS`.
- The `audit_campaign` object is exactly equal to
  `/audit-campaign-lock.json`, whose independently calculated SHA-256 is
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  matching the launcher record.
- I read `/run.json`, `/task.json`, `/generation-result.json`,
  `/generation-evidence/invocation.json`, `metrics.json`, `usage.json`,
  `codex-last.txt`, `codex-output.log`, `prompt.txt`, and the complete
  structured trace. The one JSONL trace has 216 parseable events under one
  session. Historical runtime metrics are not required for this legacy layout.
- Every required record is a real regular file, every required candidate
  deliverable is present, and no candidate or required provenance entry is a
  symlink.
- Every direct launcher-recorded file hash checked in
  `evidence/stage1-provenance-v2.log` matches. Every file listed in
  `/generation-result.json` also matches its recorded digest.
- The independently recomputed pipeline tree digest of `/candidate` is
  `a6a162c335d14bf05784926712a82c0d1f6fa1fce34e6291c57621a2d54409ad`,
  exactly the retained stage-1 workspace digest. The corresponding trace tree
  digest is
  `b9f6aa047845cc35b59e209d0273aa57fb6242489009bd4372bf681a9fba030a`,
  exactly `usage.json`'s source-trace digest.
- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`;
  `/candidate/py2mpy.py` is byte-identical to
  `/reference/py2mpy.py`.
- `/reference/reference-semantics` is absent, as required for
  `GENERATED_SEMANTICS`. I did not infer or use a hidden reference semantics.

The independent checker and full bounded output are
`evidence/provenance_check.py` and
`evidence/stage1-provenance-v2.log`.

## 2. Program fidelity and candidate-versus-canonical checks

### Trusted contract

For integer `x` and `shift`, let `s = str(x)`. The function returns a string:

- if `shift > len(s)`, return `s[::-1]`;
- otherwise return `s[len(s) - shift:] + s[:len(s) - shift]`.

The prompt gives `(12, 1) -> "21"` and `(12, 2) -> "12"`. It contains no
`shift >= 0`, size, or digit-count precondition.

`/candidate/solution.py` implements the trusted canonical algorithm. It removes
the docstring and writes the ordinary return after the `if` instead of inside an
`else`; because the true branch returns early, this is behaviorally equivalent.

Trusted regeneration was run in scratch:

```text
cmp -s solution.mpy <(python3 trusted-py2mpy.py solution.py)
```

It exited 0. Both byte streams have SHA-256
`35634b176f0c836959a648ca033f8fa84aa595d497afabf272920386b40de8d3`;
see `evidence/stage2-translation.log`.

The independent differential test imported the trusted canonical and submitted
entry points separately. It covered the two examples, `x = 0`, negative and
large integers, zero, negative, equal-length, and oversized shifts, plus 2,000
deterministically generated inputs. All 2,146 comparisons matched, including
895 negative-shift cases. See `evidence/differential_test.py` and
`evidence/stage2-differential.log`. This finite test supports implementation
fidelity; it is not the K proof.

## 3. Clean proof reconstruction

All candidate-built definitions and caches were ignored. Source files were
copied to the fresh directory
`/tmp/audit-work/65-circular-shift.DtaWTl`.

The observed toolchain was K 7.1.293 and Python 3.10.12. Exact version logs are
under `evidence/toolchain-*.log`.

### Fresh builds

The concrete definition was built from `semantic.k`:

```text
kompile semantic.k --backend llvm --main-module MPY \
  --syntax-module MPY-SYNTAX --output-definition concrete-kompiled
```

It exited 0 (`evidence/stage3-kompile-concrete.log`).

The proof definition was independently built from `verification.k`, which
imports the source `semantic.k`:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition proof-kompiled
```

It exited 0 (`evidence/stage3-kompile-proof.log`).

### Concrete semantics

Fresh LLVM `krun` executions were compared with both Python implementations on
16 targeted cases. The set exercises both examples, shift zero, shift equal to
the string length, shift one above it, negative shifts, `x = 0`, negative `x`,
and a 41-digit integer. Every result matched. See
`evidence/concrete_semantics_test.py` and the authoritative corrected log
`evidence/stage3-concrete-semantics-corrected.log`.

`evidence/stage3-concrete-semantics.log` is retained for transparency but is
superseded: its reviewer-authored regex accidentally contained doubled
backslashes and failed to recognize visibly correct `VString` output. The
corrected parser reran the same cases and exited 0; this was a reviewer harness
issue, not a candidate failure.

The separately recorded 4,301-digit boundary is a genuine mismatch, not a
parser issue; it is analyzed in Stage 5.

### Positive proof claims

The original all-claims command exited 0 and printed exactly `#Top`
(`evidence/stage3-kprove-all.log`):

```text
kprove spec.k --definition proof-kompiled --spec-module SPEC
```

Because the six candidate claims have no labels, I copied each claim unchanged
into a distinct reviewer spec module and ran it separately. Every isolated
command exited 0 and printed `#Top`:

| Claim | Reviewer spec | Log |
|---|---|---|
| symbolic ordinary branch | `evidence/stage3-claim-1-normal.k` | `evidence/stage3-kprove-claim-1.log` |
| symbolic oversized branch | `evidence/stage3-claim-2-oversized.k` | `evidence/stage3-kprove-claim-2.log` |
| `(12,1) -> "21"` | `evidence/stage3-claim-3-example-12-1.k` | `evidence/stage3-kprove-claim-3.log` |
| `(12,2) -> "12"` | `evidence/stage3-claim-4-example-12-2.k` | `evidence/stage3-kprove-claim-4.log` |
| `(1234,2) -> "3412"` | `evidence/stage3-claim-5-normal-1234-2.k` | `evidence/stage3-kprove-claim-5.log` |
| `(1234,5) -> "4321"` | `evidence/stage3-claim-6-oversized-1234-5.k` | `evidence/stage3-kprove-claim-6.log` |

Thus clean verification succeeds under the submitted generated semantics. That
fact does not cure the adequacy and semantics defects below.

## 4. Adequacy and real-program pinning

### Plain-language claims

1. For every K integer `X` and `SHIFT` satisfying
   `0 <= SHIFT <= len(str(X))`, executing the submitted function returns
   the last `SHIFT` characters followed by the preceding characters.
2. For every K integer `X` and `SHIFT` satisfying
   `len(str(X)) < SHIFT`, executing the function returns `str(X)` reversed.
3. Four unconditional ground claims require the exact results `"21"`,
   `"12"`, `"3412"`, and `"4321"` for the listed inputs.

Each destination consumes `<k>` to `.K` and rewrites `<result>` from `VNone`
to an exact `VString(...)`. There is no right-only result variable, existential
escape, implication-only weakening, omitted observable cell, or tautological
postcondition.

The symbolic preconditions are satisfiable. `X = 12, SHIFT = 1` witnesses the
ordinary claim and yields `"21"` in both Python implementations and K.
`X = 1234, SHIFT = 5` witnesses the oversized claim and yields `"4321"`.
The four concrete claims are themselves satisfying entry states. See
`evidence/stage4_scope_witness.py` and
`evidence/stage4-scope-witness.log`.

### Program identity

The `<k>` cell executes `solutionProgram`, a macro containing a hand-copied
constructor body. In the fresh definition I compared:

- `kast` of the trusted-regenerated `solution.mpy`; and
- `kast --expand-macros` of `solutionProgram`.

The terms are byte-equal after `kast` rendering and have the identical digest
`b3ec760417f31ab631a5a130a9488777106df0af4a1285d00ca49a3bc16701a6`.
See `evidence/stage4-program-pinning.log`. Together with trusted translation
identity, this mechanically pins the submitted function binding and body.

Body sensitivity was checked independently. I swapped the two concatenated
slices in the actual constructor term, compiled a separate Haskell definition,
and proved the original `(12,1) -> "21"` target. Compilation exited 0, but
`kprove` exited 1 with `WarnStuckClaimState` and residual result
`VString("12")`. See `evidence/stage4-body-mutant-verification.k`,
`evidence/stage4-body-mutant-spec.k`,
`evidence/stage4-body-mutant-kompile.log`, and
`evidence/stage4-body-mutant-kprove.log`.

### Material scope failure

The union of the two symbolic preconditions covers exactly nonnegative shifts:
the first states `SHIFT >= 0`, and the second implies positivity because a
decimal string has positive length. No candidate claim covers `SHIFT < 0`.

This is not a hypothetical or ill-typed case. For `x = 1234, shift = -1`:

- neither symbolic precondition holds;
- the trusted canonical returns `"1234"`;
- the submitted Python function returns `"1234"`;
- fresh `krun` returns `"1234"`; and
- a reviewer-added concrete reachability claim for this exact real program
  exits 0 with `#Top`.

See `evidence/stage4-scope-witness.log`,
`evidence/stage3-concrete-semantics-corrected.log`, and
`evidence/stage4-negative-shift-concrete-kprove.log`. Other witnesses
`(0,-1)` and `(-1234,-3)` are also recorded. The source contract does not grant
the candidate a nonnegative-shift assumption. Omitting every negative shift is
a material narrowing, so the benchmark requires `FAIL / NOT_LEGIT` even if the
restricted theorem is sound.

## 5. Rule-by-rule static soundness review

The lexical inventory is preserved in
`evidence/stage5-rule-inventory.log`: 42 rules in `semantic.k`, three local
rules in `verification.k`, and six reachability claims in `spec.k`.

### Syntax, configuration, attributes, and construct coverage

The declarations are:

- `semantic.k:4-26`: `Program`, statement lists, four `Stmt` constructors
  (`FuncDef`, `Assign`, `If`, `Return`), parameters, seven `Expr`
  constructors (`Name`, `Int`, `BinOp`, `UnaryOp`, `Compare`, `Call`,
  `Subscript`), argument lists, `CmpOp`, `Slice`, and bounds.
- `semantic.k:32-36`: four values (`VInt`, `VString`, `VBool`, `VNone`) and
  value lists.
- `semantic.k:38-44`: the complete four-cell configuration: `<k>`, `<entry>`,
  `<args>`, and `<result>`.
- `semantic.k:52,59,65-69,90-99,125,137-138`: execution and helper
  declarations.
- `verification.k:9,29,34`: the `solutionProgram` macro, `runSolution`, and
  `normalCircularShift`.

Local attributes are exhaustively accounted for:

- `[symbol(...)]` is used only on AST constructors.
- `[function]` is used on `runProgram`, `bind`, `exec`, `branch`, `continue`,
  `resultOf`, `eval`, `lookupVal`, `pyStr`, `pyLen`, `unary`, `binary`,
  `compare`, `sliceFrom`, `sliceTo`, `reverseValue`, `clipIndex`,
  `reverseString`, `reverseFrom`, `runSolution`, and
  `normalCircularShift`.
- `[total]` appears only on `clipIndex`.
- `[macro]` appears only on `solutionProgram`.
- There are no local `[functional]`, `[simplification]`, `[concrete]`,
  priority, anywhere, or opaque declarations.

Every constructor in `solution.mpy` is declared and modeled:

| Submitted construct | Declaration and execution |
|---|---|
| `Module`, `FuncDef`, `Params` | `semantic.k:4-13`, lookup/binding at 53-62 |
| `Assign(Name, Call(str,...))` | 7-8, 15, 20, execution/evaluation at 72-73, 101-102, 108, 117 |
| `If(Compare(... > Call(len,...)))` | 9, 19-20, 24, execution/evaluation at 74-85, 106-109, 118, 122 |
| `Return` and early control transfer | 10, rules 76 and 84-87 |
| subtraction and string concatenation | 17, rules 105 and 120-121 |
| open-ended ordinary slices | 21, 25-26, rules 112-115 and 125-135 |
| `[::-1]` with literal unary `-1` | 17, 21, 25-26, rules 104, 110-111, 119, 137-144 |

The semantics intentionally omits unused Python constructs. That is acceptable
in `GENERATED_SEMANTICS`: every submitted constructor is covered, and unsupported
syntax is not silently fabricated.

### Exhaustive semantic-rule decisions

| Rule(s) | Role and decision |
|---|---|
| `semantic.k:46-49` | Starts exactly the parsed `Program`, preserves entry/args, and puts `runProgram` in result. Sound for the pure four-cell interpreter. |
| `53-54` | Selects the first function with the requested name and executes its exact body with positional binding. Sound for the one-definition module. |
| `55-57` | Skips a differently named definition. Guard is disjoint from the preceding equal-name rule; sound. |
| `60` | Empty parameters plus empty arguments bind to an empty map; sound. |
| `61-62` | Recursively binds one positional value per parameter. Argument and parameter order are preserved; exact arity is enforced by visible stuckness; sound. |
| `71` | Empty statement sequence terminates normally with the current environment; sound. |
| `72-73` | Evaluates the assignment RHS and updates its named local before the rest; sound for the submitted `Name` target. |
| `74-75` | Evaluates the condition before selecting a branch and retains the trailing statements; sound. |
| `76` | Evaluates a return expression and discards later statements; sound early-return behavior. |
| `78-80` | True Boolean branch executes `THEN`; sound. |
| `81-83` | False Boolean branch executes `ELSE`; its guard is disjoint from the true rule; sound. |
| `84` | A returned value bypasses the retained continuation; sound. |
| `85` | Normal branch completion resumes trailing statements with the updated environment; sound. |
| `86` | Extracts an actual return value; sound. |
| `87` | A function falling off the end yields Python-like `None`; unused by the target's terminating paths but sound. |
| `101` | Variable evaluation delegates to environment lookup; sound. |
| `102` | Retrieves the exact key from a K map. Candidate parameters/local names are distinct, so no binding ambiguity; sound. |
| `103` | Integer literal to `VInt`; sound. |
| `104` | Evaluates unary operand before dispatch. Only pure unary `-` is used; sound. |
| `105` | Evaluates both binary operands before dispatch. The used operands are pure, so any unspecified internal rewrite order has no observable effect; sound for this program. |
| `106-107` | Evaluates the single comparison's two pure operands and dispatches its exact operator; sound for the submitted non-chained comparison. |
| `108` | Resolves the literal unshadowed name `str` to the generated primitive. Binding is correct for this module, but the primitive's unbounded behavior is unsound relative to real CPython; detailed below. |
| `109` | Resolves unshadowed `len` and evaluates its one argument; sound for the submitted module. |
| `110-111` | Recognizes exactly `[::-1]`, evaluates the base, and invokes the fully defined reverse helper; sound for the used ASCII decimal strings. |
| `112-113` | Evaluates a lower-bound ordinary slice and delegates to `sliceFrom`; sound. |
| `114-115` | Evaluates an upper-bound ordinary slice and delegates to `sliceTo`; sound. |
| `117` | Maps every `VInt(I)` to `VString(Int2String(I))`. Correct for ordinary-size integers, but materially over-broad and false for the real CPython domain admitted by the theorem; witness below. |
| `118` | Maps string length to `lengthString`; sound for decimal ASCII strings. |
| `119` | Integer unary minus; sound. |
| `120` | Integer subtraction; sound. |
| `121` | String concatenation; sound. |
| `122` | Integer greater-than to Boolean; sound. |
| `126` | Clips a sufficiently far negative endpoint to zero. Correct whenever `L >= 0`, which holds for every actual call. |
| `127-128` | Converts an in-range negative index to `I + L`. Correct whenever `L >= 0`. |
| `129` | Leaves endpoints in `[0,L]` unchanged; correct. |
| `130` | Clips endpoints above `L` to `L`; correct whenever `L >= 0`. |
| `132-133` | Implements `s[i:]` using the clipped lower endpoint and real string length; sound on all actual calls. |
| `134-135` | Implements `s[:i]` using the clipped upper endpoint; sound on all actual calls. |
| `139` | Applies the defined reverse to a string value; sound. |
| `140` | Initializes reversal at the last valid index; sound. |
| `141` | Ends reversal below zero; guard is disjoint from the recursive case; sound. |
| `142-144` | Prepends the one-character substring and strictly decrements the index. It terminates and computes reversal; sound for all actual strings. |

The generated helpers are pure and the submitted expressions have no side
effects, so the function-based interpreter does not lose a material Python
evaluation-order effect. The four configuration cells are all present in every
entry claim. Assignment, branch continuation, and early return are explicitly
modeled. Calls are pinned to unshadowed builtins in this exact module.

### Verification-rule decisions

| Rule | Classification and decision |
|---|---|
| `verification.k:10-27` | Macro expansion, not an execution shortcut. Fresh constructor-level comparison proves it is exactly the regenerated program term. |
| `30-31` | Definitional wrapper `runSolution`; it expands to the same `runProgram` invocation and is unused by the claims. Sound. |
| `35-37` | Definitional mathematical summary for the ordinary branch. Under `0 <= SHIFT <= length`, both substring bounds are valid and it equals the two source slices. It does not replace program execution. Sound on every claim use. |

There are no auxiliary claims, operational proof bridges, simplification
lemmas, fresh values, or opaque result-bearing symbols. `reverseString` is used
in both execution and the oversized postcondition, but it is not an oracle: its
base and recursive equations fully determine the value and descend by one.
No rule directly asserts this task's answer while bypassing the submitted body.

### Concrete semantics unsoundness witness: unbounded `str(int)`

The theorem quantifies over every K integer `X`. On this installed CPython:

```text
sys.get_int_max_str_digits() = 4300
X = 10 ** 4300
SHIFT = 0
```

`X` has 4,301 decimal digits and satisfies the candidate ordinary precondition.
Both `/candidate/solution.py` and `/reference/canonical.py` terminate by raising
`ValueError: Exceeds the limit (4300) for integer string conversion`. Fresh K
execution instead exits 0 and returns a `VString` of length 4,301. See
`evidence/stage5_large_int_boundary.py` and
`evidence/stage5-large-int-boundary.log`.

Thus `semantic.k:117` can enable the false conclusion that the real generated
program returns a string on a satisfying claimed input. This is not finite-test
absence: it is a concrete opposite-behavior witness at the exact primitive
boundary. The candidate neither bounds `X` nor models the exception. At best,
the proof is conditional on an unstated abstract-Python assumption that
decimal conversion never enforces CPython's configured limit.

### `clipIndex` declaration gap

`clipIndex` is declared `[function, total]` over all pairs of K integers, but
its equations are designed for a nonnegative length. At `I = 0, L = -1`, the
guards at lines 126 and 130 overlap while their right sides are respectively
`0` and `-1`. This is an over-broad declaration and should be guarded by
`L >= 0` or use a length sort.

No intended program execution can supply negative `L`, because every call uses
`lengthString(S)`. Therefore, under the benchmark's witness rule, I record this
as an off-path totalization/maintenance gap rather than a second
intended-domain unsoundness. A configuration-shaped probe showed the backend
normalizing the term to `0` and rejecting the `-1` destination; see
`evidence/stage5-clip-overlap.k` and
`evidence/stage5-clip-overlap-config-kprove.log`.
`evidence/stage5-clip-overlap-kprove.log` is the superseded first probe, whose
bare functional claims are unsupported by this Haskell backend; it is not used
as evidence for or against the candidate.

## 6. Fresh non-vacuity test

I did not reuse any candidate vacuity artifact. The fresh mutation changed the
symbolic ordinary-branch destination from:

```text
VString(normalCircularShift(Int2String(X), SHIFT))
```

to the deliberately false:

```text
VString(normalCircularShift(Int2String(X), SHIFT) +String "!")
```

`X = 12, SHIFT = 1` satisfies the unchanged precondition. The real result is
`"21"` and the mutation requires `"21!"`.

The mutation parsed and built successfully against the fresh proof definition.
`kprove` exited 1 with `WarnStuckClaimState`; the residual explicitly compares
the actual concatenation with the same concatenation plus `"!"`. This is the
expected unmet result obligation, not a parser error, crash, timeout, or
unreachable mutation. See `evidence/stage6-spec-vacuity.k` and
`evidence/stage6-kprove-vacuity.log`.

The independent body mutation in Stage 4 also failed for the expected changed
result, providing separate body-sensitivity evidence.

## 7. Proven-versus-assumed accounting

### What the successful K proof establishes

Conditional on the submitted generated MPY semantics and its imported K
builtins:

- for all K integers `X` and `SHIFT` with
  `0 <= SHIFT <= lengthString(Int2String(X))`, the exact submitted constructor
  program reaches `.K` with the ordinary two-substring rotation;
- for all K integers `X` and `SHIFT` with
  `lengthString(Int2String(X)) < SHIFT`, it reaches `.K` with the recursively
  defined string reversal; and
- the four listed concrete outputs hold.

This theorem is exact and non-vacuous for its stated restricted model. It is
not a theorem for negative shifts, and its universal `X` statement is not
faithful to the real CPython conversion boundary.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K 7.1.293 parser, compiler, LLVM/Haskell backends, and SMT/reachability implementation | All builds and proofs | Ordinary unavoidable toolchain trust; campaign version matches. |
| K `DOMAINS` primitives for unbounded integers, Booleans, strings, maps, lists, `lengthString`, `substrString`, `Int2String`, arithmetic, comparisons, and concatenation | All semantic execution and summaries | Acceptable low-level mathematical trust boundary, but `Int2String` is not by itself a faithful model of CPython's configured conversion exception. |
| Trusted CPython-AST translator | Source-to-`solution.mpy` bridge | Launcher hash matches; trusted regeneration is byte-identical. |
| Hand-copied `solutionProgram` macro | Every entry claim | Mechanically expanded constructor identity passes; body mutation is sensitive. |
| Generated semantics rules | Every entry claim | Most used-domain rules pass static and concrete review. The unguarded `pyStr` rule is materially over-broad relative to the real runtime. |
| `reverseString` and `normalCircularShift` | Oversized and ordinary postconditions | Fully defined mathematical helpers, not opaque assumptions. Their equations are reviewed above. |
| Python differential evidence (2,146 cases) | Implementation/canonical bridge | Zero mismatches, but finite and not a universal proof. |
| K/Python concrete evidence | Generated-semantics bridge | Supports ordinary and branch-boundary behavior; independently exposes the 4,301-digit mismatch. |
| Assumption `SHIFT >= 0` | Entire symbolic theorem coverage | Not granted by the trusted source contract; illegitimate material narrowing. |
| Abstract assumption that `str(int)` never raises | Universal `X` theorem | Unstated and contradicted by the real runtime witness; unacceptable for a proof of the real generated program. |

Gate accounting under the Kit terminology:

- clean verification: pass (`#Top` for the collective and every isolated
  positive claim);
- Gate A real-program soundness: fail at the unguarded `str(int)` boundary for
  a satisfying 4,301-digit input;
- Gate B intent adequacy: fail because every negative shift is omitted;
- Gate C evidence auditability: pass for the evidence actually claimed here,
  with finite testing explicitly kept separate from universal proof.

Even if one elects to idealize away CPython's configured digit limit, the
negative-shift omission remains a material HumanEval source-domain narrowing.
The benchmark explicitly maps that `SOUND-BUT-LIMITED` situation to
`FAIL / NOT_LEGIT`, not `CONCERNS / LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
