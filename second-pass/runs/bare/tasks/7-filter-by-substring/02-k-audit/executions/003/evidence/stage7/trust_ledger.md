# Proven-versus-assumed ledger

## What the reconstructed `#Top` results establish

Conditional on the generated K definition and the K toolchain:

1. For arbitrary K `PyList INPUT` and K `String SUBSTRING`, the exact
   constructor term named by `solutionProgram` reduces to
   `evalComp(INPUT, substringFilter(SUBSTRING))`.
2. `evalComp` and `filterRef` agree on `Nil`.
3. For one `Cons(HEAD,TAIL)`, they agree if the corresponding keep/drop guard
   holds **and** tail equality is already supplied as a precondition.
4. The two fixed example executions reach the claimed concrete results.

The reconstructed proof does not contain a successful K claim composing item 1
with a universal `evalComp = filterRef` theorem. A reviewer-created direct
universal reachability claim stops on that symbolic equality.

## Boundaries and assumptions

| Boundary | Dependents | Evidence | Classification |
|---|---|---|---|
| Trusted CPython source contract and canonical implementation | Program-fidelity judgment | `/reference/prompt.py`, `/reference/canonical.py`; 1,000-case independent differential run | Acceptable trusted benchmark input; finite tests support candidate/canonical equivalence but are not a proof. |
| Trusted `py2mpy.py` translation | Real-program pinning | Byte-identical regenerated `solution.mpy`; mechanical constructor-token equality with `solutionProgram` | Acceptable and directly checked for this immutable source. |
| K parser, kompiler, Haskell/LLVM backends, reachability engine | Every K execution and `#Top` | Fresh K 7.1.293 rebuilds and runs | Conventional low-level proof trust boundary. |
| Imported K `Map`, `Bool`, `Int`, `String`, collection, and `K-EQUAL` definitions | Environment lookup, guards, recursion, claims | Fresh concrete/proof builds; ordinary library meaning | Acceptable low-level primitives as K operations. |
| `findString(H,N,0) >=Int 0` as a bridge to Python `N in H` | `containsString`, both recursion definitions, intended result | Concrete normal/boundary tests | **Illegitimate as stated:** counterexample `H=N=""` makes the generated semantics drop the empty string while Python retains it. |
| Specialized list-comprehension equation | Exact candidate execution | Constructor pattern, recursive equations, concrete cases, body mutation | Narrow but not opaque; acceptable for the pure used construct only, subject to the failed membership bridge. |
| Informal structural induction combining base and conditional step claims | Alleged universal correctness | Candidate comment and universally quantified step variables; no candidate target claim | Material proof gap. The actual K target was not machine-checked; reviewer target gets stuck. |
| Partial correctness / termination | Interpretation of reachability | Structural recursion over finite `PyList`; Python list comprehension terminates for finite typed lists | Termination is outside the claimed partial-correctness theorem; no issue by itself. |

There are no locally declared fresh values, opaque functions, uninterpreted
result oracles, priority rules, or simplification axioms. The two local total
functions (`evalComp`, `filterRef`) have structurally covering constructor
rules, but both depend on the defective membership bridge.

## Kit gate accounting

- Gate A (real-program soundness): **FAIL**. Program identity/body sensitivity
  and false-postcondition discrimination pass, but the generated semantics
  enables a false intended-domain result at `([""], "")`.
- Gate B (intent adequacy): **FAIL**. The source domain includes empty strings
  and empty substring, and no successful entry claim states the unrestricted
  program-to-contract postcondition.
- Gate C (trust/evidence): reproducible finite evidence is present, but it
  cannot repair Gate A/B. The trust ledger exposes rather than validates the
  failed bridge.
