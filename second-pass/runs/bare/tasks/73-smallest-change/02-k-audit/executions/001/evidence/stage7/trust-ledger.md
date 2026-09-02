# Proven-versus-assumed ledger

## What the reconstructed `#Top` establishes

- For the duplicated `#smallestChangeBody` constant, one activation takes the
  base branch to `finish(0)`, the equal-end branch to an interior `recur`, or
  the unequal-end branch to an interior `recur ~> addResult(1)`, under the
  corresponding guards.
- The separately introduced `minimumPalindromeChanges` symbol rewrites by its
  three defining equations. These three claims are trivial under the same
  simplification rules.
- Three fixed internal-body executions reach `finish(4)`, `finish(1)`, and
  `finish(0)`.

It does not establish a universal reachability claim from the submitted
`Module(...)` program to a final result, and it does not equate the program's
result to `minimumPalindromeChanges(L)`.

## Trust and assumption inventory

1. K toolchain v7.1.293, Haskell backend, parser, rewrite engine, and prover:
   foundational machine trust for all dynamic evidence.
2. Imported K `Int`, `Bool`, and `List` hooks (`size`, negative indexing,
   `range`, arithmetic, equality): value-bearing trusted primitives. Their
   standard contracts are assumed. The local slice equation misuses `range`
   outside the submitted `[1:-1]` case.
3. Trusted `/reference/py2mpy.py`: the audit uses it to establish byte identity
   of submitted and regenerated `.mpy`; the K proof itself does not invoke it.
4. `#smallestChangeBody`: a proof-local duplicate of the AST body. Structural
   inspection finds it equal to the submitted body, but no K entry claim loads
   `solution.mpy`. Rebuilding after a materially different translated program
   still gives `#Top`, demonstrating lack of body sensitivity.
5. Binding model: `"arr"` is assumed to denote the `<input>` list and
   `"smallest_change"` the same `BODY`; `"len"` is assumed to be the builtin.
   This is sound for this exact source but not modeled with an environment.
6. Control model: idealized unbounded recursion with no stack or exception
   cell. It omits CPython's recursion limit; two valid length-2501 inputs
   produce `RecursionError` in the candidate Python and normal results in the
   canonical Python.
7. Mathematical intent bridge: the claim that the mismatch-count recurrence is
   exactly the minimum number of arbitrary element changes needed for a
   palindrome is an informal mathematical argument. No palindrome predicate,
   edit relation, or minimization theorem is formalized.
8. Domain bridge: formal `List` is not restricted to all-`Int` elements even
   though the source contract says integer arrays. The recurrence equations
   project endpoints to `Int`, and the `[total]` declaration lacks coverage for
   non-integer lists.
9. Differential evidence: 11,857 deterministic cases compare trusted
   canonical, independent mismatch-count oracle, and candidate. Ordinary
   11,855 cases match; both length-2501 cases diverge by `RecursionError`.
   This is finite bridge evidence, not a universal proof.
10. Non-vacuity evidence: a mutated fixed example demanding `finish(1)` instead
    of `finish(0)` parses and fails with a residual `finish(0)`. This shows the
    example claim is result-sensitive; it cannot supply the missing universal
    theorem.

## Gate outcomes

- Gate A, real-program soundness: FAIL. No universal result claim, no
  `Module(solution.mpy)` entry claim, body-insensitive proof, and one globally
  false local slice equation.
- Gate B, intent adequacy: FAIL. The candidate implementation diverges from the
  unbounded prompt domain at ordinary CPython recursion depth, and the
  recurrence-to-minimum bridge is informal.
- Gate C, evidence auditability: PASS for the reviewer evidence. Commands,
  statuses, sources, mutations, and bounded outputs are preserved. This does
  not cure Gates A or B.
