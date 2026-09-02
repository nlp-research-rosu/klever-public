# Proven-versus-assumed ledger

## Machine-checked statement

Under the freshly compiled candidate semantics and verification module, for
arbitrary mathematical integers `A` and `B`, execution of the exact submitted
constructor program from empty `<env>` and `<functions>` maps and `noResult`
finishes the claimed computation with:

- `<env>` equal to `"a" |-> absInt(A), "b" |-> absInt(B)`;
- `<functions>` containing the exact submitted `multiply` body; and
- `<result>` equal to
  `(absInt(A) %Int 10) *Int (absInt(B) %Int 10)`.

The original abbreviation-based claim and the reviewer literal-AST claim both
returned `#Top` with exit 0. The theorem constrains the result and all modeled
state cells. The off-by-one result mutation parsed successfully and failed on
the expected equality obligation.

## Boundaries and dependents

| Boundary | Kind and influence | Dependents | Evidence / assessment |
|---|---|---|---|
| K parser, compiler, Haskell backend, and reachability prover v7.1.293 | Trusted implementation of proof checking; affects all conclusions | Every claim | Standard unavoidable checker trust boundary. Fresh source builds avoid candidate caches. |
| Builtin `Int`, `Bool`, `String`, `Map`, `absInt`, `-Int`, `%Int`, `*Int`, `<Int`, map lookup/update, and strict heat/cool machinery | Trusted primitive semantics; affects values, guards, evaluation, and state | S4-S22 and V3 | Acceptable low-level language/runtime boundary. Used arithmetic is ordinary mathematics; divisor is always 10. |
| Trusted `/reference/py2mpy.py` | Source-to-constructor syntactic bridge | Identity of `solution.py` and `solution.mpy` | Candidate translator is byte-identical to the trusted mount, and regeneration is byte-identical. This establishes use of the trusted translation, conditional on the translator's own correctness. |
| Reviewer static correspondence between each used AST node and `semantic.k` | Informal generated-semantics-to-Python bridge; affects control, state, and final value | Meaning of the K theorem as a theorem about Python `solution.py` | Exhaustive rule inventory plus 17 concrete K-vs-candidate-Python checks. Strong finite and structural evidence, but not a machine-checked universal CPython connection theorem. Acceptable for validating this minimal generated semantics, with the limitation stated. |
| Closed `multiplyProgram` and `multiplyBody` rules | Definitional program abbreviations; influence executed body but carry no result | Original entry claim | Exact AST expansions. A separate literal-AST K claim removes both and closes, so they are not result oracles. |
| `unitDigit(I)` | Proof-local total mathematical function; affects postcondition only | Original and literal entry claims | One unguarded, nonrecursive equation `absInt(I) %Int 10`, with complete coverage and no overlap. It never replaces execution. |
| `function(...)` and `noResult` | Opaque data constructors/sentinel; affect stored body and initialization, not computed answer | Configuration and final function-map constraint | Fully inspected and harmless: neither can synthesize an integer result. |
| K partial-correctness interpretation | Termination is outside the requested theorem form | The headline theorem | Explicit scope. The submitted code is loop-free, and all concrete runs terminate, but the report does not promote testing into a separate total-correctness theorem. |
| Candidate implementation to trusted task intent | Intent bridge; affects whether the proved algorithm solves HumanEval/97 | Natural-language correctness judgment | Material failure. The trusted canonical uses Python `abs(a % 10)`, whereas the candidate proves `(abs(a) % 10)`. For `(-1,1)`, canonical is 9 and candidate/formal result is 1; 338/882 differential cases mismatch. |

There are no fresh existential answer variables, proof-local axioms,
simplification lemmas, opaque result oracles, externally interpreted
result-bearing functions, or auxiliary loop claims.
