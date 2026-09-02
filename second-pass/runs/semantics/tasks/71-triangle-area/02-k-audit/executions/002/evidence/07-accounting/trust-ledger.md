# Proven-versus-assumed ledger

## Formally established under the supplied K definition

- Loading the exact regenerated `solution.mpy` module binds
  `triangle_area` to the same three-parameter closure and constructor body used
  by the call claims.
- For all mathematical K integers `A,B,C`, the four mutually exclusive guards
  cover the left-to-right invalidity test.
- In each invalid partition, executing that exact closure returns integer `-1`.
- In the strict-valid integer partition, execution returns the fully constrained
  structural term
  `roundFN(powF(mulF(mulF(mulF(divII(...),...),...),...),0.5),2)`.
- The theorem is body-sensitive and result-sensitive: changing the executed
  invalid return to `-2` and changing the valid postcondition to `-1` each
  produces an expected stuck residual.

## Trusted primitives and assumptions

| Boundary | Effect | Dependents | Assessment |
|---|---|---|---|
| Supplied MPY configuration, sequencing, environments, maps, calls, frames, returns, integer arithmetic/comparison, and Boolean short-circuit rules | Control, binding, state, integer values | All five claims | Required immutable semantics boundary. The used path was traced statically; no candidate-local rule replaces it. |
| K built-in mathematical `Int`, `Bool`, `Map`, `List`, and `String` hooks | Values and state | All symbolic execution | Ordinary K trust boundary. |
| `divII(Int,Int)` | Result-bearing float primitive | Valid claim through `semiPerimeter` | Opaque and total to Haskell; the supplied concrete rule converts both integers to 53/11 floats and divides. Safe divisor here is literal 2, but the symbolic theorem does not evaluate the float. |
| `intToF(Int)` and `subF(Float,Float)` | Result-bearing promotion/subtraction | Valid claim | Opaque to Haskell, with supplied LLVM equations. |
| `mulF(Float,Float)` | Result-bearing multiplication | Valid claim | Opaque to Haskell, with supplied LLVM equation. |
| `powF(Float,Float)` at exponent `0.5` | Result-bearing exponentiation | Valid claim | Opaque to Haskell, with supplied LLVM `^Float` equation. The K theorem does not prove that this is geometric square root or reason about IEEE exceptional cases. |
| `roundFN(Float,Int)` at precision 2 | Final result | Valid claim | Opaque to Haskell, with supplied LLVM rounding equation. The K theorem proves the exact term is returned, not its numerical value. |
| Heron's formula characterizes triangle area | Natural-language meaning | Source-contract bridge | Informal mathematical bridge; not a K theorem. |
| CPython-AST translator preserves the candidate source | Program identity | Pinning argument | Trusted launcher-supplied translator plus byte-identical regeneration and a generated constructor-level load claim. |
| Python canonical implementation | Finite differential oracle | Fidelity/intent evidence | Trusted benchmark input. It agrees on 1,023 observations but finite testing is not a universal proof. |

The opaque float terms are not fresh program-derived oracles: the program
itself executes to those same primitive applications and `expectedArea` expands
to the identical structure. Thus they do not make an arbitrary opposite result
provable. They remain an important numeric and exception-model trust boundary.

## Excluded behavior

Every call claim has arguments `A:Int,B:Int,C:Int`. No theorem covers K `Float`
arguments, mixed integer/float inputs, booleans, or other Python numeric types.
This exclusion is material: the unannotated source contract speaks of side
lengths, both the canonical and candidate implementations accept non-integral
lengths, and the supplied semantics concretely executes them. For example,
`triangle_area(5.5,6.25,7.75)` returns `17.03` in canonical Python, candidate
Python, and the fresh LLVM assertion run, yet satisfies no formal entry claim.

The supplied float model also does not model all CPython overflow, NaN,
infinity, complex-number, or exception behavior. Those limitations matter less
than the explicit integer-only theorem restriction, which independently defeats
full source-contract adequacy.
