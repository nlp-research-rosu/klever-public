# Independent adversarial audit: 154-cycpattern-check

## Outcome

The candidate's two positive K claims reconstruct successfully and the entry
claim mechanically pins the submitted `solution.mpy` body. The theorem is
non-vacuous and, apart from a documented connection-proof gap for a pure slice
acceleration, the proof-local rules have no identified false-conclusion
witness.

It is nevertheless not a proof of the HumanEval source contract over its
intended domain. The prompt does not exclude an empty second string, the
trusted canonical returns `True` for every input with `b == ""`, and this also
follows from ordinary substring behavior because `"" in a` is true. The
submitted program and its K summary both return `False` on that boundary.
The independent differential run found 193 such mismatches. Under the
benchmark's explicit mapping, this material loss of the source-contract domain
is `FAIL / NOT_LEGIT`, not a non-fatal concern.

## 1. Input and provenance integrity

The launcher declares `record_layout = legacy-selected-stage1`,
`condition = semantics`, and `semantics_mode = SUPPLIED_SEMANTICS`. The trusted
`/reference/reference-semantics` tree is present, so the rendered mode and
mounts are consistent.

I read and checked `/audit-input.json`, `/audit-campaign-lock.json`,
`/run.json`, `/task.json`, `/generation-result.json`, the required invocation,
metrics, prompt, last-message, output-log, and structured trace records, plus
the present `usage.json`, `legacy-metrics.json`, and `legacy-run-input.json`.
The structured trace has one valid JSONL file with 609 records and no invalid
JSON. Historical runtime metrics are not required for this legacy layout and
were not reconstructed.

Independent results:

- The campaign block is exactly equal to the lock JSON. The lock's actual
  SHA-256 is
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  matching `/audit-input.json`.
- Every launcher-required path is readable, is the expected regular-file or
  directory type, and is not a symlink.
- The recorded hashes of the canonical, prompt, translator, run/task/result
  records, invocation, metrics, usage, generation prompt, log, and last
  message all match their mounted bytes. Every generation-evidence file
  declared by `generation-result.json` also matches its declared hash.
- The candidate prompt and translator are byte-identical to the trusted
  mounts.
- A no-follow inventory of the complete candidate has 39 entries and no
  symlink or special-file entry. Its independently defined inventory digest is
  `5e55f10fb9ef298309f2f055f3253b28cf1a35ff5e08a01f0651450cc3c1be32`.
- The candidate and trusted supplied-semantics trees each have exactly 25
  entries. Relative paths, entry types, and every regular-file SHA-256 match;
  there are no additions, omissions, changes, or symlinks. Both have the
  independent inventory digest
  `be33a565bce2ab7be5268671512997fc361449f7c45dcfbc2b2195987ee59bf8`.

The generation records claim prior success, but no such claim or compiled
artifact was reused. Detailed commands and results are in
[`evidence/stage1.log`](evidence/stage1.log),
[`evidence/stage1-integrity-rerun.log`](evidence/stage1-integrity-rerun.log),
and the reviewer-authored parsers
[`evidence/stage1_integrity.py`](evidence/stage1_integrity.py) and
[`evidence/trace_inspect.py`](evidence/trace_inspect.py).

Stage 1 result: **PASS**. There is no audit-infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

For string inputs `a` and `b`, return `True` exactly when `b` itself or one of
its cyclic rotations occurs as a contiguous substring of `a`; otherwise return
`False`. No non-emptiness precondition appears in `/reference/prompt.py`.

The trusted canonical sets `pat = b + b` and compares every length-`len(b)`
window of `a` to every such window of `pat`. For `b == ""`, both loop ranges
contain an iteration and the compared empty slices are equal, so it returns
`True`.

The submitted implementation starts `pattern = b`, checks one rotation per
character of `b`, and advances the rotation by `pattern[1:] + char`. This is
equivalent for nonempty `b`. For empty `b`, the loop has no iteration and the
function immediately returns `False`. The candidate's own concrete harness
even asserts this changed result, but that assertion does not alter the trusted
contract.

### Translation identity

Using only the copied trusted translator in `/tmp/audit-work/fresh`:

```text
python3 py2mpy.py solution.py > solution.regenerated.mpy
cmp solution.mpy solution.regenerated.mpy
```

Both commands exited 0. The submitted and regenerated files are byte-identical
with SHA-256
`fc0856f0a0475b9c73186876195c6c73e91dabf18cd514e0d4fe6d64b7c9548b`.

### Independent differential evidence

[`evidence/differential_test.py`](evidence/differential_test.py) imports the
trusted canonical and copied submitted function through separate module
loaders. It exercises:

- all six documented examples;
- 14 explicit empty, length-boundary, repetition, rotation, Unicode, and NUL
  cases;
- all binary-alphabet strings with both lengths from 0 through 5; and
- 5,000 deterministic random string pairs with lengths 0 through 40 over
  ASCII, whitespace, NUL, accented, and non-BMP characters.

The command exited 0 after reporting all results rather than hiding
mismatches: 8,989 checks and 193 mismatches. Every observed mismatch has
`b == ""`, with canonical `True` and generated `False`. The documented
examples and sampled nonempty cases agree. See
[`evidence/differential.log`](evidence/differential.log) and
[`evidence/stage2.log`](evidence/stage2.log).

Stage 2 result: **FAIL for source-contract fidelity**. The difference is a
material boundary case in the unrestricted string domain.

## 3. Clean proof reconstruction

All execution occurred under `/tmp/audit-work/fresh`. Only explicit source
files and the trusted supplied-semantics tree were copied. Candidate-provided
compiled definitions, caches, `kore-exec.tar.gz`, logs, and bytecode were not
copied or used.

The independently available toolchain reports K v7.1.293. The following fresh
operations all exited 0:

1. regenerate and byte-compare the concrete harness;
2. compile `reference-semantics/semantics.k` with LLVM as `MPY-KRUN`;
3. execute the regenerated concrete harness to a final `.K` state with exit
   code 0;
4. compile `verification.k` with Haskell as `VERIFICATION-BASE`;
5. prove `SPEC-LEMMA`, obtaining `#Top`;
6. compile `verification.k` afresh with Haskell as `VERIFICATION`; and
7. prove `SPEC`, obtaining `#Top`.

The full commands, compiler warnings, output, and statuses are preserved in
[`evidence/stage3.log`](evidence/stage3.log). The LLVM harness's successful
empty-string assertion is evidence that K executes the submitted program's
`False` behavior, not evidence that this behavior satisfies the contract.

Stage 3 result: **PASS**. Every candidate positive target claim cleanly
reconstructs with exit 0 and `#Top`.

## 4. Adequacy and real-program pinning

### Claims in plain language

`SPEC-LEMMA.loop-invariant` has no `requires` clause. From a live function
frame whose local `a`, `b`, `char`, and `pattern` values are strings, and whose
computation is the exact submitted loop followed by `return False` and
`#endcall`, it says execution:

- checks `pattern in a` once for every character remaining in `REM`;
- rotates `pattern` by dropping its first code and appending that current
  character after each failed check;
- returns the Boolean `rotationsLoop(A,P,REM)`;
- restores environment 0, removes local scope 1, resets `scopeLoc` to 1,
  pops the exact caller frame, preserves the remaining stack, and resumes
  `CONT`.

`SPEC.entry-point` also has no `requires` clause. For every finite K `IntSeq`
pair `A,B`, from the exact initial call configuration and a global binding of
`cycpattern_check` to the submitted closure, it says the call produces
`rotationsLoop(A,B,B)`.

Both preconditions are satisfiable. For example, the entry precondition with
`A = "hello"` and `B = "ell"` is a concrete state and the result is `true`.
The loop precondition can use the corresponding live frame with
`P = REM = "ell"` and any ordinary caller continuation.

### Mechanical program identity

The fresh `kast` output for regenerated `solution.mpy` and the dry-run JSON
KAST for the entry claim were traversed independently. The function and call
names are both `"cycpattern_check"`. The parameter constructors have the same
SHA-256
`599f36a7cade744f011f0d5b5706fcdc25aeadcad123410d2c18256b81237c5c`.
The translated function body and the claim's closure body are structurally
identical KASTs, both with SHA-256
`ef59e6e386fa28bcc9a0603ff9a4714400a16b66a63cfb332a9820b3522ed8ed`.
See [`evidence/stage4.log`](evidence/stage4.log) and
[`evidence/pinning_check.py`](evidence/pinning_check.py).

Thus the claim pins the submitted program by the allowed constructor-level
route even though it starts from a preloaded function binding rather than the
complete module.

### Concrete substitutions and sensitivity

Direct instances of the formal equations agree with both Python
implementations on `("hello","ell")`, `("abcd","abd")`, and `("abab","baa")`.
For `("anything","")` and `("","")`, the claimed summary and generated Python
both return `False`, while the trusted canonical returns `True`. These results
are in [`evidence/claim_instances.py`](evidence/claim_instances.py) and
[`evidence/stage4.log`](evidence/stage4.log).

A body-sensitivity mutation changed the final `Return(Bool(false))` inside the
claim's actual closure term to `Return(Bool(true))` while leaving the result
summary unchanged. It parsed, ran, and failed with exit 1 and
`WarnStuckClaimState`; the residual exposes the satisfying `B = .IntSeq`
branch returning `true`. See
[`evidence/spec-body-mutation.k`](evidence/spec-body-mutation.k) and
[`evidence/body-sensitivity.log`](evidence/body-sensitivity.log).

Stage 4 result: **PASS for pinning and result constraint; FAIL for intent
adequacy**. The claim precisely proves the wrong empty-pattern result of the
real submitted program.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[`evidence/rule-inventory.txt`](evidence/rule-inventory.txt) inventories every
local declaration from the assembled supplied semantics, all 23 helper K
files, `verification.k`, and `spec.k`. It records the complete normalized
declaration, source line, and attributes such as `function`, `total`,
`symbol`, `simplification`, `priority`, `owise`, `strict`, and `seqstrict`.
Totals are:

- 704 rules;
- 229 syntax declarations;
- 5 contexts;
- 1 configuration; and
- 2 claims.

There is no local `[functional]` declaration. The opaque/no-evaluator float,
sort, keyed-sort, and MD5 symbols are enumerated, but their constructors and
operations cannot arise on this string-only proof path.

[`evidence/rule-review.tsv`](evidence/rule-review.tsv) gives a disposition and
reason for every one of the 941 inventoried declarations. Proof-reachable
fixed rules are marked individually; fixed imported rules with incompatible
constructors, operators, calls, or value sorts are marked unreachable rather
than silently trusted as proof contributors. LLVM-only rules are separated
from the Haskell proof theory.

### Used-language coverage

The submitted term maps to the following fixed declarations and rules:

- `Module`, `FuncDef`, `Params`, statement sequencing, `Assign`, `For`, `If`,
  `Return`, `Name`, `Str`, `Compare`, `CmpOp`, `BinOp`, `Subscript`, and
  `Slice` from `syntax.k`;
- exact configuration, scope lookup, literals, truthiness, and left-to-right
  argument evaluation from `core.k`;
- generic call evaluation, closure invocation, parameter binding, return, and
  frame pop from `call.k` and `functions.k`;
- assignment, string iteration, loop stepping, target binding, and branch
  control from `controls.k`, `str.k`, and `tuple.k`;
- ordered comparison/binop dispatch from `operators.k`; and
- fully structural string concatenation, prefix, and substring membership
  from `str.k`.

The fixed configuration cells and the entry claim agree. Argument lookup and
evaluation precede frame allocation and binding. The loop target is rebound
before the body. `Return` discards the in-function continuation and `#pop`
restores the caller. String slicing and concatenation have no heap, allocation,
exception, or output effects. The program uses only the ASCII literal `""`;
symbolic input strings enter directly as `str(IntSeq)`, so the supplied
literal rule's ASCII restriction does not narrow the input theorem.

### Every proof-local rule

| Rule(s) | Classification and decision |
|---|---|
| Symbolic `#branch` true/false | Derived rules. Their guards `C` and `notBool C` are disjoint and they agree with the fixed ground branch rules on overlap. |
| Two `dropOne` equations | Total structural definition over the two `IntSeq` constructors; exhaustive, non-overlapping, and descending. |
| `Subscript(str(S), Slice(1,None,None))` bridge | Operational bridge at priority 30. It is pure and its result is mathematically the tail-or-empty sequence produced by fixed CPython-clamped slicing. Three independent fixed-semantics ground claims close with `#Top`. A bridge-free universal claim over symbolic `S` builds but gets stuck because the supplied theory does not derive `auditDropOne(S) == buildIS(...)`; therefore this is a universal connection-theorem evidence gap, not a demonstrated false rule. |
| Three `rotationsLoop` equations | Total structural summary. Empty `REM` returns false; a nonempty matching state returns true; the disjoint failed-match case descends on the `REM` tail after the exact slice/concat update. Guards are exhaustive and pairwise disjoint. |
| Promoted loop rule | Operational bridge at priority 30, but its complete LHS, continuation, binding, scope, stack, return state, and RHS are exactly the separately proved `SPEC-LEMMA` domain and result. The base proof excludes this promoted rule. It preserves heap, heap location, exception, exit code, and stack remainder, which the skipped string-only loop cannot change. |

The bridge-free universal slice attempt is preserved in
[`evidence/slice-connection.k`](evidence/slice-connection.k) and
[`evidence/slice-connection.log`](evidence/slice-connection.log); its ground
checks are in [`evidence/slice-ground.log`](evidence/slice-ground.log).
Because there is no fixed-versus-bridge counterexample, I do not label this
rule unsound. It would independently justify `CONCERNS` if the source-contract
proof were otherwise adequate.

The loop bridge's match domain is not broader than its theorem: `CONT` is read
from the exact top stack frame in both; the whole trailing computation inside
the function is fixed as `Return(false) ~> #endcall`; the exact four-entry
local map is removed; and arbitrary `G`, builtins scope `BS`, and stack
remainder are preserved. The body-sensitivity failure separately confirms
that this bridge does not make arbitrary substituted bodies provable.

No proof-local rule is rejected as unsound, so there is no unsupported
unsoundness allegation requiring a false-conclusion witness. The fatal defect
is instead the explicitly witnessed mismatch between the proved program
behavior and the source contract.

Stage 5 result: **no demonstrated rule unsoundness; one non-fatal proof-local
connection evidence gap; fatal adequacy mismatch remains**.

## 6. Fresh non-vacuity test

There is no candidate `spec-vacuity.k`. I created a fresh spec preserving the
exact submitted closure and initial configuration but replacing the entry
postcondition with `notBool rotationsLoop(A,B,B)`. This obligation is false;
for the satisfying witness `a = "hello", b = "ell"`, the program and original
summary are `true` while the mutation demands `false`.

The dry run exited 0, establishing successful parsing and claim construction.
The actual proof exited 1 with `WarnStuckClaimState`. Its residual shows the
reached `rotationsLoop(A,B,B)` value and the unmet equality to
`notBool rotationsLoop(A,B,B)`, rather than a parser error, missing import,
timeout, or unrelated crash. The wrapper therefore reports
`EXPECTED_FALSE_POSTCONDITION_FAILURE: PASS`.

See [`evidence/spec-vacuity.k`](evidence/spec-vacuity.k) and
[`evidence/stage6.log`](evidence/stage6.log).

Stage 6 result: **PASS**. The entry proof is result-constraining and
non-vacuous.

## 7. Proven versus assumed accounting

### What the successful K proof establishes

Conditional on the supplied semantics, K backend, and proof-local slice
bridge, the staged reachability proof establishes:

> For every finite `IntSeq` pair `A,B`, executing the exact submitted
> `cycpattern_check` closure from the stated initial configuration reaches the
> Boolean `rotationsLoop(A,B,B)`. This value is true exactly when one of the
> `len(B)` loop iterations observes its current rotated pattern as a substring
> of `A`; it is false when no such iteration does. In particular, it is false
> when `B` is empty because the loop has zero iterations.

This is a partial-correctness reachability result. Termination of the Python
loop on finite strings is also evident from its structurally shrinking
iterator, but the requested classification does not rely on elevating that
informal fact into a separate total-correctness theorem.

### Trust and evidence ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| Supplied K semantics and K v7.1.293 backend | Both claims | Required fixed trust boundary. Rebuilt from source; all material program operations are modeled and reviewed. |
| Trusted `py2mpy.py` translation | Link from `solution.py` to `solution.mpy` | Trusted input, byte-regenerated exactly. This is translation evidence, not a universal compiler-correctness proof. |
| Constructor-level source-to-claim comparison | Entry claim's program identity | Mechanical KAST equality establishes the immutable submitted binding/body used by the theorem. |
| Proof-local symbolic branch rules | Loop lemma and entry proof | Ordinary Boolean case splitting; disjoint and fixed-rule compatible. |
| `dropOne` and `rotationsLoop` definitions | Loop lemma and postcondition | Fully equated structural functions; no opaque result-bearing oracle. |
| Pure `s[1:]` operational bridge | Failed-match rotation step, hence both claims | Mathematically consistent and ground-checked, but the independent bridge-free universal K claim is stuck. This is an explicit evidence limitation. |
| `SPEC-LEMMA` promoted as an operational rule | Entry proof | Acceptable staged theorem use: the bridge-free base claim closes first and has the same complete context and state footprint. |
| Opaque float/sort/MD5 and other imported primitives | None | Constructor-inert and do not affect control, state, or result here. |
| Natural-language/canonical interpretation of empty strings | Overall requested correctness | Trusted prompt plus canonical and ordinary Python substring behavior all require `True`; finite differential testing witnesses the submitted divergence but is not used as the K proof. |

Gate summary:

- Fresh verification: **PASS**.
- Real-program pinning and non-vacuity: **PASS**.
- Proof-extension audit: **no false rule found**, with the stated universal
  slice-connection evidence limitation.
- Intent/domain adequacy: **FAIL** because the unrestricted contract includes
  `b == ""`, while the proved result is false there.
- Reproducibility/evidence: **PASS**; reviewer scripts, mutations, commands,
  statuses, and bounded logs are preserved under `/audit-output/evidence/`.

The reconstructed `#Top` results therefore prove the actual submitted
algorithmic summary, but they do not constitute a legitimate proof that the
generated program satisfies HumanEval/154 on its real source-contract domain.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
