# Proven-versus-assumed ledger

## Formally established by reconstructed K proof

- The exact constructor program regenerated from `solution.py` is the program
  term in the entry claim after macro expansion.
- For every K integer `N`, execution from the modeled entry configuration
  reaches `.K`, returns `fizzFrom(0,N)`, and reaches the stated modeled local
  environment.
- The inner loop adds `digitSevens(X)` for every `X >= 0`.
- The outer loop adds `fizzFrom(I,N)` for every `0 <= I <= N`.

## Candidate-local proof extensions

- `digitSevens`, `fizzContribution`, `fizzFrom`, and `fizzEnd` are definitional
  summaries with guarded, exhaustive, disjoint, terminating equations.
- Integer associativity is a derived mathematical simplification.
- `INNER-LOOP` and `OUTER-LOOP` are compile-time aliases whose expanded KORE is
  mechanically identical to the submitted program fragment.
- There are no operational bridges, opaque result symbols, fresh result
  values, priority overrides, or program-answer axioms.

## Trusted boundaries

1. K 7.1.293, the Haskell `kore-exec` prover, and the sound implementation of
   imported `INT`, `BOOL`, `STRING`, and `MAP` domains. Every proof claim
   depends on this standard toolchain boundary.
2. The launcher-designated `py2mpy.py` translator as the syntactic Python-AST
   to constructor bridge. Byte regeneration establishes that the candidate
   submitted exactly its output; it does not prove the translator itself.
3. The rule-by-rule meta-level judgment that generated `semantic.k` models the
   submitted program's used Python subset. This is the required
   `GENERATED_SEMANTICS` trust audit. Concrete execution, branch coverage, body
   sensitivity, and static analysis support it; no hidden reference semantics
   is assumed.
4. Ordinary mathematics: repeated positive division by ten with remainder
   counts base-10 digits equal to seven, and the `fizzFrom` recurrence is the
   finite sum over nonnegative integers below `N` divisible by 11 or 13.
5. CPython execution of trusted `canonical.py` and candidate `solution.py` is
   only a finite empirical check. It supports implementation-to-intent
   alignment on recorded inputs and is not used as a universal K lemma.

## Explicit exclusions

- Non-integer arguments and Python constructs not present in `solution.py`.
- Full CPython object, exception, call-stack, and module-definition semantics.
- Runtime complexity and resource termination outside the modeled mathematical
  integers.
- Universal equivalence to the canonical implementation as a separate K
  theorem; the proved recurrence directly formalizes the source contract.

The extra initial `x |-> 0` binding in the minimal environment is not a claim
about an observable Python return value. `x` is not read before assignment on
any path that enters the inner loop and is not externally observable after
return; for empty iteration the binding is semantically inert.
