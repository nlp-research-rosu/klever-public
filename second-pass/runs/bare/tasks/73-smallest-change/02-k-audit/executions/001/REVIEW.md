# Independent adversarial review: 73-smallest-change

## Executive decision

The candidate reconstructs cleanly and every submitted claim prints `#Top`, but
those claims do not constitute a partial-correctness proof of the submitted
program. The only universal program claims stop after one function activation
at an intermediate `recur(...)` term. The separately defined mathematical
recurrence is never equated to the program's eventual result. No universal
claim starts from the submitted `Module(...)` or reaches `<result>`.

This is also mechanically body-insensitive: changing the translated program's
base return from `0` to `99`, rebuilding from source, and rerunning the proof
still produces `#Top`, because `verification.k` contains an independent
duplicate of the old body and the proof never reads `solution.mpy`. In addition,
one generic slice rule in the generated semantics can prove a concrete false
Python result.

The candidate therefore proves several one-step lemmas, three defining
equations, and three fixed examples—not the requested real-program theorem.

## 1. Input and provenance integrity

The rendered mode is `GENERATED_SEMANTICS`, and
`/reference/reference-semantics` is absent. The trusted mounts therefore do not
contradict the rendered mode; there is no infrastructure breach.

All trusted inputs and required candidate artifacts are regular files, not
symlinks or mistyped entries. The candidate prompt and translator are
byte-identical to the trusted mounts:

- `prompt.py`:
  `a91bec8bc0f85124b068553a370cb6c2b8564b2e298289f578e913cb77f619bf`
- `py2mpy.py`:
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`

There are no missing, changed, extra, mistyped, or symlinked required source
artifacts. The top-level `semantic-kompiled/`, `verification-kompiled/`, and
`__pycache__/` entries are extra generated caches, not required source; they
were treated as untrusted and never copied or reused. There are no extra helper
K source files. The structured trace is one regular JSONL file with 528 parsed
records.

`run-input.json`, `metrics.json`, `codex-last.txt`, bounded portions of
`codex-output.log`, and all structured trace records were read only as
untrusted claims. They claim successful examples, 4,000 random cases, and
`#Top`. The trace also records that a program-to-mathematical-result claim was
attempted and later removed; this is context only, not a premise of the
verdict. The final source independently establishes the missing connection.

Evidence:

- [integrity.log](/audit-output/evidence/stage1/integrity.log)
- [untrusted-metadata.log](/audit-output/evidence/stage1/untrusted-metadata.log)
- [trace-claims.log](/audit-output/evidence/stage1/trace-claims.log)
- [check_integrity.sh](/audit-output/evidence/stage1/check_integrity.sh)
- [extract_trace_claims.py](/audit-output/evidence/stage1/extract_trace_claims.py)

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract asks for the minimum number of individual element changes
needed to make an integer array palindromic, where one changed element may
become any integer. For each mirrored pair, an equal pair costs zero and an
unequal pair necessarily and sufficiently costs one. Thus the result is the
number of unequal mirrored pairs; empty and singleton arrays return zero.

The trusted canonical program iterates over the first half and counts mirrored
mismatches. The candidate recursively examines the outer pair, removes it, and
adds one exactly when it differs. This is mathematically equivalent for calls
that complete normally.

Regenerating with the trusted translator produced byte identity with submitted
`solution.mpy`; both hashes are
`519c414732e0e5b2ed5b09cd737f65151fc1a356e81e0841904dc3beb154b72e`.

The independent differential test used:

- all three documented examples;
- 11 explicit empty, singleton, equal/unequal endpoint, odd/even, and
  extreme-integer boundary cases;
- every length-0-through-8 array over `{-1,0,1}` (9,841 cases);
- 2,000 deterministic random arrays of length 0 through 128; and
- two valid length-2501 integer arrays.

Of 11,857 total cases, the first 11,855 match the independent mismatch oracle
and trusted canonical result. Both length-2501 cases diverge: under CPython
3.10's default recursion limit 1000, the candidate raises `RecursionError`,
while the canonical returns `1250` and `0`. The prompt states no length bound,
so this is an implementation-to-intent limitation and a concrete difference
between real CPython and the K model's unbounded recursion.

Evidence:

- [translation-identity.log](/audit-output/evidence/stage2/translation-identity.log)
- [differential_test.py](/audit-output/evidence/stage2/differential_test.py)
- [input_scope.txt](/audit-output/evidence/stage2/input_scope.txt)
- [differential.log](/audit-output/evidence/stage2/differential.log)

## 3. Clean proof reconstruction

Only source artifacts needed for execution were copied to
`/tmp/audit-work/73-smallest-change`. No candidate-built definition, binary, or
cache was copied. K v7.1.293 was used.

Fresh builds:

- Standalone generated semantics, LLVM backend: build exit 0.
- Standalone generated semantics, Haskell backend: build exit 0.
- Verification definition, Haskell backend: build exit 0.

The standalone Haskell semantics was concretely compared with both Python
implementations on ten normal and boundary cases: empty, singleton, equal and
unequal pairs, odd equal/unequal endpoints, a nested mismatch, and all three
prompt examples. Every K run exited 0 and all results matched. This satisfies
the generated-semantics concrete execution gate using an approved concrete
backend.

The LLVM definition builds, but eight recursive cases stop at
`eval(Slice(...))` with exit 113; only the two base cases complete. Since the
same fresh source executes under Haskell and the proof uses Haskell, this is
reported as backend sensitivity rather than an audit infrastructure failure or
the basis of the verdict.

The original all-claims command exits 0 and prints `#Top`. An audit-only copy
added labels without changing any claim body, then ran every one of the nine
claims independently. All nine exit 0 and print `#Top`. The three
`minimumPalindromeChanges` claims emit `WarnTrivialClaim`, because the
definition already contains the identical simplification equations.

Key evidence:

- [tool-versions.log](/audit-output/evidence/stage3/tool-versions.log)
- [kompile-semantic-llvm.log](/audit-output/evidence/stage3/kompile-semantic-llvm.log)
- [kompile-semantic-haskell.log](/audit-output/evidence/stage3/kompile-semantic-haskell.log)
- [kompile-verification-haskell.log](/audit-output/evidence/stage3/kompile-verification-haskell.log)
- [concrete-execution-haskell.log](/audit-output/evidence/stage3/concrete-execution-haskell.log)
- [concrete-execution-llvm.log](/audit-output/evidence/stage3/concrete-execution-llvm.log)
- [kprove-all.log](/audit-output/evidence/stage3/kprove-all.log)
- [spec-labeled.k](/audit-output/evidence/stage3/spec-labeled.k)
- Per-claim logs:
  [program base](/audit-output/evidence/stage3/kprove-program-base.log),
  [program equal](/audit-output/evidence/stage3/kprove-program-equal.log),
  [program unequal](/audit-output/evidence/stage3/kprove-program-unequal.log),
  [math base](/audit-output/evidence/stage3/kprove-math-base.log),
  [math equal](/audit-output/evidence/stage3/kprove-math-equal.log),
  [math unequal](/audit-output/evidence/stage3/kprove-math-unequal.log),
  [example 1](/audit-output/evidence/stage3/kprove-example-1.log),
  [example 2](/audit-output/evidence/stage3/kprove-example-2.log), and
  [example 3](/audit-output/evidence/stage3/kprove-example-3.log).

Fresh `#Top` is genuine verification under the submitted theory. It does not
settle adequacy or soundness of that theory.

## 4. Adequacy and real-program pinning

The nine formal claims say:

1. If `size(L) <= 1`, one activation of the duplicated body reaches
   `finish(0)`.
2. If `size(L) > 1` and the integer endpoints are equal, one activation
   reaches `recur(body, interior, body)`.
3. If `size(L) > 1` and endpoints differ, one activation reaches
   `recur(body, interior, body) ~> addResult(1)`.
4. For length at most one, the separate mathematical function rewrites to
   zero.
5. For equal endpoints, that function rewrites to itself on the interior.
6. For unequal endpoints, that function rewrites to one plus itself on the
   interior.
7-9. Three fixed internal-body runs reach `finish(4)`, `finish(1)`, and
   `finish(0)`.

Claims 1-3 are exhaustive one-activation summaries, but claims 2-3 do not
constrain the eventual returned value. Claims 4-6 define a different term.
There is no claim of either essential shape:

```text
run(actualBody, L, actualBody) => finish(minimumPalindromeChanges(L))
```

or:

```text
<k> Module(actual submitted solution.mpy) => .K </k>
<result> .K => minimumPalindromeChanges(L) </result>
```

Consequently, no circularity or induction hypothesis connects an interior
`recur` to the mathematical recurrence. The prose phrase “same exhaustive
recurrence” is an informal observation, not a K reachability theorem.

No proof claim's `<k>` cell executes the submitted `solution.mpy`. Claims use
the proof-local constant `#smallestChangeBody`. Its expansion is structurally
the same as the current submitted body, but this comparison lies outside the
proof. The body-sensitivity experiment changed the generated program's base
return to `99`; the mutated `.mpy` hash changed, Python returned `99` on `[]`,
the verification definition rebuilt from source, and all submitted claims
still printed `#Top`. This directly demonstrates that proof closure does not
depend on the real generated program.

Satisfying ground witnesses exist:

- Base: `L=[]`; both Python implementations return `0`, matching `finish(0)`.
- Equal branch: `L=[1,9,1]`; both return `0`, while the formal program RHS is
  only the intermediate `recur(body,[9],body)`.
- Unequal branch: `L=[1,9,2]`; both return `1`, while the formal RHS is only
  `recur(body,[9],body) ~> addResult(1)`.
- The three fixed-example claims match both Python implementations.

The preconditions are therefore not empty. The defect is missing result
constraint and real-program pinning, not an unsatisfiable precondition.

Evidence:

- [formal-source-numbered.log](/audit-output/evidence/stage4/formal-source-numbered.log)
- [precondition-witnesses.log](/audit-output/evidence/stage4/precondition-witnesses.log)
- [solution-mutated.py](/audit-output/evidence/stage4/solution-mutated.py)
- [solution-mutated.mpy](/audit-output/evidence/stage4/solution-mutated.mpy)
- [body-sensitivity-hashes.log](/audit-output/evidence/stage4/body-sensitivity-hashes.log)
- [body-sensitivity-kompile.log](/audit-output/evidence/stage4/body-sensitivity-kompile.log)
- [body-sensitivity-proof.log](/audit-output/evidence/stage4/body-sensitivity-proof.log)
- [body-sensitivity-python.log](/audit-output/evidence/stage4/body-sensitivity-python.log)

This stage independently requires `FAIL / NOT_LEGIT`.

## 5. Rule-by-rule static soundness review

The exhaustive inventory covers every local syntax production, configuration
cell, function/total attribute, operational rule, concrete attribute,
simplification rule, and claim:

- [rule-inventory.md](/audit-output/evidence/stage5/rule-inventory.md)

Summary by exact inventory IDs:

- S1-S2 (`concatStmts`) are true, disjoint, and structurally decreasing.
- S3 initializes the exact parsed one-function module correctly for concrete
  execution. The proof claims bypass it.
- S4-S5 implement the length branch with disjoint, exhaustive integer length
  guards.
- S6-S7 implement endpoint equality with disjoint integer guards. Real control
  flow ensures indexes are valid.
- S8-S10 model the three submitted return shapes and preserve their relevant
  control and value order.
- S11 ground-unfolds `recur` under `[concrete]`. It is faithful to idealized
  unbounded recursion but deliberately unavailable to symbolic proof and does
  not model CPython recursion exceptions.
- S12-S13 correctly add the saved mismatch count and transfer the finished
  value to `<result>`.
- S14-S18 correctly implement the used integer, negation, addition, length,
  and list-index operations for this program. Partial cases stop visibly.
- S19, the generic slice equation, is false over its declared domain.
- S20-S21 are correct projected integer comparison equations, though the
  hard-coded operational `If` rules do not invoke them.
- V1-V3 are truthful, disjoint, decreasing mismatch-count equations on finite
  integer lists. Declaring the function `[total]` over all K `List` values is
  broader than their integer-projection coverage.
- V4 truthfully expands the proof-local body constant to a duplicate of the
  current source body; it does not pin a proof entry to `solution.mpy`.

There are no local priority or `owise` rules, macros, opaque result-bearing
symbols, ordinary proof-local operational bridges in `verification.k`, or
additional helper K files. The local functions are `eval`, `truth`,
`concatStmts`, `minimumPalindromeChanges`, and `#smallestChangeBody`; only
`minimumPalindromeChanges` is marked `total`. Imported K integer, Boolean, and
list hooks form the low-level primitive boundary.

Construct coverage is complete for the submitted AST: `Module`, `FuncDef`,
`Params`, `If`, `Compare`, `Call`, `Name`, `Return`, `Int`, `Subscript`,
`Slice`, `UnaryOp`, `BinOp`, `CmpOp`, and `NoBound` all have declarations and
an applicable exact-program path. Missing semantics for other Python forms is
not charged as a defect in generated-semantics mode.

### Concrete false-conclusion witness for S19

K's `range(List,fromFront,fromBack)` removes counts from the front and back.
The candidate interprets every Python `arr[LOW:HIGH]` as
`range(arr, LOW, 0-HIGH)`. For the valid integer input `[0,1,2,3]` and slice
`[1:0]`, the candidate theory proves the result `[1,2,3]` and prints `#Top`.
CPython evaluates the same slice to `[]`. Thus S19 is not merely under-modeled:
it enables a specific false conclusion.

The submitted program only uses `[1:-1]`, for which S19 happens to be correct,
so this witness does not explain the one-step claim closure. It nevertheless
means the compiled local semantics contains a globally false equation and
fails the required rule-by-rule soundness contract.

Evidence:

- [slice-unsound-witness.k](/audit-output/evidence/stage5/slice-unsound-witness.k)
- [slice-witness-proof.log](/audit-output/evidence/stage5/slice-witness-proof.log)
- [slice-witness-python.log](/audit-output/evidence/stage5/slice-witness-python.log)

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`. A fresh mutation changed submitted
example claim 3 from the true `finish(0)` to false `finish(1)` for
`[1,2,3,2,1]`. This input satisfies the claim's unconditional precondition;
both Python implementations and concrete K return zero.

The mutation dry-run builds successfully with exit 0. The actual proof exits 1
with `WarnStuckClaimState`; its residual contains `finish(0)` and cannot unify
with the requested `finish(1)`. This is the expected unmet result obligation,
not a parser error, timeout, missing import, or unrelated crash.

This establishes that the fixed-example result is non-vacuous. It does not
repair the absent universal result claim.

Evidence:

- [spec-vacuity.k](/audit-output/evidence/stage6/spec-vacuity.k)
- [mutation-dry-run.log](/audit-output/evidence/stage6/mutation-dry-run.log)
- [mutation-proof.log](/audit-output/evidence/stage6/mutation-proof.log)

## 7. Proven versus assumed accounting

What is formally established is limited to:

- three guarded one-activation transitions of a duplicated body;
- three rewrite equations for a separately introduced mismatch-count
  function; and
- three ground internal-body examples.

It is not formally established that the actual submitted module returns
`minimumPalindromeChanges(L)` for arbitrary integer lists, nor that
`minimumPalindromeChanges` is the minimum over a formal edit relation.

The trust and assumption boundary is:

1. K v7.1.293, its Haskell backend, parser, rewriter, and prover.
2. Imported K `Int`, `Bool`, and `List` hooks. These are acceptable low-level
   primitives, but the local generic slice bridge misuses `range`.
3. The trusted translator for the byte-identity check. It is not invoked by
   the proof.
4. The informal/structural assertion that `#smallestChangeBody` duplicates the
   current source. This is concerning and mechanically body-insensitive.
5. Hard-coded bindings for `arr`, `len`, and `smallest_change`, acceptable for
   this exact source but not represented by an environment.
6. Idealized unbounded recursive control with no exception cell, contradicted
   by real CPython on two intended-domain length boundaries.
7. The informal mathematical bridge from mirrored mismatch count to minimum
   arbitrary element changes. No palindrome/edit/minimization model is proved.
8. An implicit all-integer domain despite K claims ranging over the broader
   `List` sort.
9. Finite differential and concrete tests. They support only the tested
   bridge, not universal equivalence.

The full ledger is preserved at
[trust-ledger.md](/audit-output/evidence/stage7/trust-ledger.md).

Gate A (real-program soundness) fails because the proof lacks a universal
program-result theorem, bypasses the actual module, is body-insensitive, and
contains a false local semantics equation. Gate B (intent adequacy) also fails
because of the unrestricted prompt domain versus CPython recursion behavior
and the informal minimum-change bridge. Reviewer evidence is reproducible and
auditable, but Gate C evidence cannot substitute for either missing proof.

Accordingly, fresh `#Top` is accepted as evidence that the submitted claims
close, but rejected as evidence of the requested partial-correctness theorem.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
