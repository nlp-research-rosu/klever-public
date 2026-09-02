# Independent adversarial audit: 32-find-zero

The candidate is **FAIL / NOT_LEGIT**. Fresh reconstruction does reproduce
`#Top`, but only under proof-local priority rules that replace both program
loops with unconstrained, result-bearing constructors. The entry configuration
does not load `solution.mpy` and does not bind `poly`; without the bridge rules,
the same claim gets stuck at `#look("poly", -1)`. A proof-local rule then declares
the opaque result to be an approximate zero without evaluating the polynomial
or proving a connection theorem.

This verdict does not rely on the LLVM concrete-run crash recorded in Stage 3.
It follows from the independently reconstructed Haskell proofs, their source
dependencies, the bridge-free residual, and the static false-conclusion
witnesses.

## 1. Input and provenance integrity

The rendered mode is `SUPPLIED_SEMANTICS`. The trusted mount is consistent with
that mode: `/reference/reference-semantics` exists. There is therefore no
infrastructure-mode breach and a candidate verdict is appropriate.

The exact checks and hashes are in
[stage1_integrity.log](evidence/stage1_integrity.log), produced by
[stage1_integrity.sh](evidence/stage1_integrity.sh).

- `/candidate/prompt.py` and `/reference/prompt.py` are byte-identical
  (`cmp` exit 0; SHA-256
  `17c137edab480f3be30b47bb48eea2748f23b120a73b2bb80c7901112e1b223f`).
- `/candidate/py2mpy.py` and `/reference/py2mpy.py` are byte-identical
  (`cmp` exit 0; SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`).
- Recursive `diff -qr --no-dereference` between the trusted and candidate
  `reference-semantics/` trees exits 0. Each tree contains 24 regular files
  and two directories; the candidate tree contains no symlinks. There are no
  missing, additional, mistyped, changed, or symlinked entries in that tree.
- `solution.py`, `solution.mpy`, `spec.k`, and `verification.k` are regular
  files. Candidate `__pycache__` bytecode and auxiliary test/proof scripts were
  ignored as untrusted and were not reused as build products.
- The following named provenance artifacts are absent and therefore could not
  be read: `/candidate/run-input.json`, `/candidate/metrics.json`,
  `/candidate/codex-last.txt`, and `/candidate/codex-output.log`.
  No structured generation trace is present under the candidate root
  (`generation-trace.json` and `trace.json` are absent). `PROOF.md` is also
  absent. These are provenance/evidence omissions, not the basis of the
  legitimacy failure.

All sources used for rebuilding were copied to
`/tmp/audit-work/32-find-zero`; candidate-built definitions and caches were not
copied or used.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

`/reference/prompt.py` defines

`poly(xs, x) = Σ(i, coeff in enumerate(xs)) coeff * x^i`.

`find_zero(xs)` accepts a numeric coefficient list with an even number of
coefficients and a nonzero highest-degree coefficient. Thus the degree is odd,
which supplies the intended real-root existence argument. The reference
implementation starts with `[-1.0, 1.0]`, doubles both ends until their
polynomial values do not have the same strict sign, bisects while the interval
width exceeds `1e-10`, and returns the lower endpoint. The documented examples
are `[1, 2] -> approximately -0.5` and `[-6, 11, -6, 1] -> approximately 1`.

The candidate uses the same algorithm. Its initial values and doublings use
integer literals rather than `-1.`, `1.`, and `2.0`; subsequent `math.pow` and
true division promote the relevant arithmetic. No intended-domain numerical
divergence was observed.

### Translation identity

The trusted translator regenerated `solution.mpy` byte-for-byte:

```text
COMMAND: python3 /reference/py2mpy.py /candidate/solution.py > /tmp/audit-work/32-find-zero/regenerated-solution.mpy
EXIT_STATUS: 0
COMMAND: cmp /tmp/audit-work/32-find-zero/regenerated-solution.mpy /candidate/solution.mpy
EXIT_STATUS: 0
```

Both files have SHA-256
`fd0e785aa1efde54eeeaa27bd282112b62a98223aadb7e03b486dbf0ea4984c9`.
See [stage2_fidelity.log](evidence/stage2_fidelity.log).

### Independent differential execution

[differential_test.py](evidence/differential_test.py) imports the trusted
canonical and candidate modules independently. It ran 12 fixed cases and 72
deterministically generated valid-domain cases. Fixed cases include both
documented examples, the empty list (outside the stated domain), minimum-length
lists, roots at each initial endpoint, bracket expansion in each direction,
zero constant term, a last-zero outside-domain case that terminates, float
coefficients, a repeated root, and a six-coefficient polynomial. The generated
cases cover lengths 2, 4, and 6 with nonzero last coefficients.

The run covered zero and positive bracket-loop iteration counts and both
bisection branches. It reported `mismatch_count=0` and
`max_abs_output_delta=0.0`; see
[stage2_fidelity.log](evidence/stage2_fidelity.log). On the empty and
endpoint cases the canonical may return `-1.0` while the candidate returns
`-1`, which are numerically equal and the empty case is outside the contract.
This finite evidence supports Python implementation fidelity only; it is not a
K proof or a universal bridge theorem.

## 3. Clean proof reconstruction

[stage3_reconstruct.sh](evidence/stage3_reconstruct.sh) rebuilt everything in
the scratch copy. No candidate-compiled definition existed or was reused.
The complete bounded output and each command status are in
[stage3_reconstruct.log](evidence/stage3_reconstruct.log).

The fresh concrete definition command

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
```

exited 0. A reviewer-composed concrete program containing four assertions then
caused the fresh LLVM interpreter to receive SIGFPE (`krun` exit 136). This is
recorded as a concrete-backend limitation and is not converted into a candidate
failure. Python differential execution supplies the independent dynamic
program comparison required by Stage 2.

The fresh proof definition command

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
```

exited 0. Each positive entry claim was copied unchanged into its own reviewer
spec module:

- [positive-return-spec.k](evidence/positive-return-spec.k): `kprove` exited 0
  and printed `#Top`.
- [positive-approx-spec.k](evidence/positive-approx-spec.k): `kprove` exited 0
  and printed `#Top`.
- The original combined `/candidate/spec.k` also exited 0 and printed `#Top`.

This establishes closure only under the supplied semantics plus the actual
rules in `verification.k`. Stages 4 and 5 show why that theory is not a sound
proof of the submitted program.

## 4. Adequacy and real-program pinning

### Entry claims in plain language

Both claims use the same complete initial cells: module environment 0, an empty
module scope whose parent is the builtins scope, fresh scope location 1, empty
heap, heap location 0, empty call stack, no return, no exception, and exit code
0. Both require the proof-local Boolean `validPolynomial(VS)`.

1. The first claim manually calls
   `closureVal(("xs", .ParamNames), findZeroBody, 0)` with `list(VS)`. It says
   that the call returns the term
   `bisectLow(VS, bracketLow(VS), bracketHigh(VS))` and restores all listed
   cells to their initial values.
2. The second makes the same manual call followed by `#checkApprox(VS)`. It
   says that this continuation returns `true`, again with the listed cells
   unchanged.

The first postcondition is syntactically result-constraining but its result is
an irreducible proof-local constructor, not a number. The second is reduced to
`true` by the candidate's own `approximatesZero` rule.

### Satisfying states and concrete substitution

Because `validPolynomial` is a total, evaluator-free uninterpreted Boolean with
no equations, a consistent model may interpret it as true for
`VS = vCons(1, vCons(2, .ValSeq))`; combined with the exact listed cells, this
exhibits a state satisfying each formal entry precondition. The intended
contract also accepts `[1, 2]`. The lack of an equation proving that this ground
list satisfies the formal predicate is itself an intent bridge gap.

Substitution yields the formal first result

```text
bisectLow(
  vCons(1, vCons(2, .ValSeq)),
  bracketLow(vCons(1, vCons(2, .ValSeq))),
  bracketHigh(vCons(1, vCons(2, .ValSeq))))
```

while both Python implementations return `-0.5000000000582077`. For
`[-6, 11, -6, 1]`, the formal result is another irreducible constructor while
both Python implementations return `0.9999999999417923`. Exact outputs are in
[stage4_witness.log](evidence/stage4_witness.log).

### Failure to pin and execute the submitted program

The claims do not load the submitted `Module(...)` or the `solutionModule`
macro. They directly manufacture a closure containing the copied
`findZeroBody`. The initial scopes bind no `poly` function. The `polyBody` and
`solutionModule` macros are unused by either claim.

This is dynamically exposed by
[stage4_bridge_dependency.sh](evidence/stage4_bridge_dependency.sh):

- A fresh definition containing the exact macros and postcondition machinery
  but omitting the two loop bridges builds successfully.
- The first claim then exits 1 with `WarnStuckClaimState`. Its residual begins
  at `#look("poly", -1)` with `begin = -1`, `end = 1`, and `xs = list(VS)`.
  The fixed semantics therefore cannot execute the claimed call from the
  candidate's entry configuration.
- A reviewer mutation changes the submitted `solution.mpy` return from
  `Return(Name("begin"))` to `Return(Int(777))`; `cmp` confirms the files
  differ. Re-running the already reconstructed candidate claim still exits 0
  with `#Top`, because neither `spec.k` nor `verification.k` imports or reads
  `solution.mpy`.

The body macro happens to transcribe the candidate body, but this static copy
does not satisfy the requirement that the `<k>` cell execute the actual
submitted program, especially when both loops are bypassed. This is a material
real-program-pinning failure.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory and selected-semantics boundary

[rule_inventory.txt](evidence/rule_inventory.txt), generated by
[rule_inventory.py](evidence/rule_inventory.py), enumerates every configuration,
syntax declaration, context, and rule in all 24 supplied-semantics K files and
`verification.k`, with source line, normalized full declaration, and attributes.
The recorded command and status are in
[stage5_inventory.log](evidence/stage5_inventory.log).

The inventory contains 946 entries:

- 236 syntax declarations;
- 704 rules;
- 5 evaluation contexts;
- 1 configuration;
- 147 declarations tagged `function`, 108 tagged `total`, no declarations
  tagged `functional`, 23 tagged `no-evaluators`, 47 priority rules, no
  simplification rules, 9 `macro` and 1 `macro-rec` declarations.

Entries 0001-0928 are the exact trusted supplied-semantics baseline: 227 syntax
declarations, 695 rules, 5 contexts, and 1 configuration. At the selected
semantics level they are accepted as the fixed language definition, not as
candidate proof extensions. The fresh compilers warned about several
non-exhaustive total functions. Of relevance here, `toF` is defined concretely
only for numeric values; the candidate's `validPolynomial` does not formally
constrain `VS` to numeric values. That makes the candidate claim broader than
the intended numeric domain, even though the supplied semantics itself is
unchanged.

The fixed configuration has `<k>`, `<env>`, `<scopes>`, `<scopeLoc>`, `<heap>`,
`<heapLoc>`, `<stack>`, `<ret>`, `<exc>`, and `<exit-code>` cells. Call rules
evaluate the callee then arguments, allocate a scope/frame, bind parameters,
and return by restoring the continuation and environment. Assignment writes
the current scope. Fixed `While` rules evaluate the guard on every iteration;
fixed `If` rules evaluate one guard and select one branch. List comprehension
and `enumerate` allocate list objects in the monotonic heap. The used-construct
mapping and relevant rule locations are exhaustive in
[used_construct_map.md](evidence/used_construct_map.md).

For this program, fixed execution would perform `poly` lookup/calls,
comprehension expansion, tuple binding, `enumerate`, `math.pow`, `sum`, numeric
operators, comparisons, and branch/loop control. The candidate bridges fire
before either `While` guard, so none of those property-bearing operations runs.
They also suppress the heap allocations that fixed polynomial evaluation would
perform, allowing the claim to preserve the initially empty heap and zero
heap-location counter.

### Complete `verification.k` extension inventory

Entries 0929-0946 of the exhaustive inventory are all nine local syntax
declarations and all nine local rules:

| Lines | Extension and classification | Decision |
|---|---|---|
| 9-22 | `polyBody` syntax and macro equation | Exact definitional transcription of the translated `poly` body; acceptable as a macro, but unused by the entry claims. |
| 24-34 | `bracketLoop` syntax and macro equation | Exact loop-AST macro; acceptable as syntax. Its expansion makes the later bridge overlap the fixed `While`. |
| 36-53 | `bisectLoop` syntax and macro equation | Exact loop-AST macro; acceptable as syntax. Its expansion makes the later bridge overlap the fixed `While`. |
| 55-61 | `findZeroBody` syntax and macro equation | Exact body transcription; acceptable as a macro, but it is a copied body rather than a dependency on `solution.mpy`. |
| 63-73 | `solutionModule` syntax and macro equation | Transcribes the submitted module (empty `FreeVars` notation is equivalent); acceptable but completely unused. |
| 78-79 | `validPolynomial(ValSeq)` `[function,total,symbol,no-evaluators]` | Proof-local opaque Boolean with no defining equation. It does not state even length, numeric coefficients, or nonzero last coefficient. It controls every bridge and postcondition. This is an unsupported, illegitimate domain oracle rather than a formalization of the input contract. |
| 81-84 | `bracketLow`, `bracketHigh`, `bisectLow`, `bisectHigh` | Four unconstrained program-derived, result-bearing constructors. No equations or bridge-free execution claims connect them to the actual loops. Illegitimate abstractions. |
| 89-93 | `approximatesZero` syntax and its sole rule | The rule concludes `true` exactly for the opaque `bisectLow` shape under the opaque precondition. It encodes the requested answer and has no polynomial/root equation. Materially unsound as the claimed intent bridge. |
| 95-97 | `#checkApprox` syntax and continuation rule | Mechanically feeds a returned value to `approximatesZero`; sound only as plumbing and wholly dependent on the illegitimate predicate rule. |
| 103-115 | Priority-40 `bracketLoop` operational bridge | Replaces the complete loop before its guard, overwrites `begin/end` with opaque terms, skips lookup/calls/control/allocations/exceptions, and accepts arbitrary `REST`, parent, framed cells, and continuation. No bridge-free universal connection theorem exists. Materially unsound. |
| 117-129 | Priority-40 `bisectLoop` operational bridge | Replaces the complete bisection loop, overwrites `begin/end` with opaque terms, omits the real `center` binding and all numeric/control/allocation effects, and accepts an arbitrary continuation. No bridge-free universal connection theorem exists. Materially unsound. |

There are no proof-local auxiliary claims, derived lemmas, simplification
rules, functional declarations, or connection theorems. The only overlap
control is priority 40 on the two bridges, which makes them preempt generic
`While` execution whenever the same opaque guard is assumed. Priority does not
justify equivalence.

### False-conclusion witnesses

The following witnesses cover every rule labeled materially unsound above.
They are preserved in
[stage4_bridge_dependency.log](evidence/stage4_bridge_dependency.log) and
[stage5_false_witness.log](evidence/stage5_false_witness.log).

1. **`bracketLoop` bridge, exact candidate context.** The entry scopes have no
   binding for `poly`. Fixed semantics reaches `#look("poly", -1)` and gets
   stuck; the candidate bridge completes the loop and lets the whole claim
   reach `#Top`. Thus the bridge enables the false conclusion that this
   invocation returns normally while preserving the listed cells.
2. **`bracketLoop` value/state witness.** On intended input `[1, 2]`, fixed
   execution performs zero bracket iterations and leaves
   `(begin, end) = (-1.0, 1.0)`. Because no equation constrains
   `bracketLow/High`, an opposite value-level interpretation
   `bracketLow([1,2]) = 42`, `bracketHigh([1,2]) = 43` is admitted by the proof
   abstraction, yet the bridge still concludes that transition. This is not
   the fixed loop transition.
3. **`bisectLoop` and `approximatesZero` value witness.** Fixed execution on
   `[1, 2]` returns `-0.5000000000582077`. An admitted opposite interpretation
   sets the unconstrained `bisectLow` to 42. The actual polynomial value there
   is `1 + 2*42 = 85`, so 42 is not a zero under any plausible `1e-10`
   approximation. Nevertheless the second bridge injects that same opaque
   symbol and the `approximatesZero` rule concludes `true`. Reusing the symbol
   in execution and postcondition is circular, not a value connection.
4. **`bisectLoop` context/state witness.** The bridge matches an arbitrary
   suffix. With a continuation that observes `center` immediately after the
   loop, fixed execution has assigned the final midpoint, while the bridge
   never creates `center`; lookup would fail. The bridge's accepted context is
   therefore broader than any demonstrated justification even apart from its
   wrong value abstraction.

The candidate supplies no machine-checked, bridge-free theorem over either
bridge's complete match domain. Finite Python tests cannot discharge that
universal obligation.

## 6. Fresh non-vacuity test

No candidate `spec-vacuity.k` is present. The fresh reviewer mutation is
[spec-vacuity-fresh.k](evidence/spec-vacuity-fresh.k). It changes the first
result obligation from the produced `bisectLow(...)` constructor to the
distinct `bisectHigh(...)` constructor while preserving the satisfiable
symbolic precondition. `[1, 2]` is an intended-domain witness for why demanding
the wrong endpoint constructor is not the candidate claim.

[stage6_nonvacuity.log](evidence/stage6_nonvacuity.log) records:

- `kprove ... --dry-run`: exit 0, so the mutation parses and builds;
- normal `kprove`: exit 1 with `WarnStuckClaimState`;
- the residual `<k>` is exactly
  `bisectLow(VS, bracketLow(VS), bracketHigh(VS))`, which cannot unify with the
  mutated `bisectHigh` target.

This is meaningful non-vacuity evidence: the candidate theory distinguishes
its injected result constructor from a false alternative. It does not validate
the constructor's numerical meaning or its connection to program execution.

## 7. Proven versus assumed accounting

### What the reconstructed reachability proof actually establishes

Under the theory formed by the supplied semantics plus `verification.k`, and
under the symbolic assumption `validPolynomial(VS) = true`, a manually
constructed closure:

1. executes the two initial assignments;
2. uses the first priority bridge to replace the bracket loop with
   `bracketLow/High` terms;
3. uses the second priority bridge to replace the bisection loop with
   `bisectLow/High` terms;
4. returns the injected `bisectLow` term and restores the specified cells; and
5. when followed by `#checkApprox`, reduces to `true` because a proof-local
   equation declares that exact term shape to satisfy `approximatesZero`.

The proof does **not** establish that `validPolynomial` is the HumanEval domain,
that either loop executes, that `poly` is bound or called, that the returned
term is numeric, that evaluating the polynomial there yields or approaches
zero, that the submitted module is loaded, or that `solution.mpy` affects the
theorem.

### Trust and assumption ledger

| Boundary | Influence | Accounting |
|---|---|---|
| Exact supplied MPY semantics, including its configuration, control, call, allocation, and primitive rules | Defines the selected language semantics | Acceptable fixed trust boundary in `SUPPLIED_SEMANTICS`; integrity matched exactly. |
| Supplied opaque proof-domain float symbols such as `powF`, `mulF`, `addF`, `subF`, division/conversion symbols, and `gtF`, with concrete LLVM rules | Would affect real polynomial and loop execution | Acceptable only as the supplied low-level semantics boundary. The candidate proof bypasses these operations, so they provide no support for its result. |
| `validPolynomial` | Controls both bridge applicability and both entry claims | Illegitimate proof-local oracle. It has no equations or formal link to even length, numeric values, or nonzero leading coefficient. |
| `bracketLow/High` | Replaces first-loop state and feeds the second bridge/result | Illegitimate program-derived opaque summary; no connection theorem. |
| `bisectLow/High` | Replaces second-loop state and determines the return | Illegitimate result-bearing opaque summary; no connection theorem or opposite-interpretation rejection. |
| `approximatesZero` constructor rule | Sole reason the requested postcondition becomes `true` | Illegitimate task-answer axiom; false under the concrete opposite interpretation above. |
| Macro transcription of `solution.py` | Informal/static bridge from submitted source to proof term | Byte regeneration and inspection support transcription fidelity, but the proof has no dependency on `solution.mpy`, and `solutionModule/polyBody` are unused. |
| Python canonical differential test | Supports implementation-versus-canonical behavior on 84 cases | Finite empirical evidence only; it cannot replace K execution or a universal operational bridge theorem. |
| Natural-language claim that interval bisection returns an approximate root | Intended mathematical argument | Not formalized or proved anywhere in the candidate theory. |

### Decision

Fresh `#Top` and meaningful structural non-vacuity are present, but the proof
executes neither the submitted module nor the property-bearing loops. It relies
on materially unsound operational bridges and an answer-encoding
postcondition rule, with concrete and symbolic false-conclusion witnesses.
This meets multiple `FAIL / NOT_LEGIT` conditions: bypassed real execution,
failure to pin the submitted program, and materially unsound proof rules.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
