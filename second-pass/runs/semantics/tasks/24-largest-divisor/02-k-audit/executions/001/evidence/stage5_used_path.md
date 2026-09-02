# Target-path mapping and proof-local rule review

## Program syntax and operational rules

| Submitted construct | Syntax declaration | Evaluation and state rules |
|---|---|---|
| `Module(...)` | `semantics/syntax.k:61` | `#loadAll` and statement sequencing at `semantics/core.k:124-127` |
| `FuncDef("largest_divisor", Params("n"), BODY)` | `semantics/syntax.k:53,57-60` | closure installation at `semantics/functions.k:14-16` |
| public call harness `Call(Name(...), Int(N))` | `semantics/syntax.k:28` | name lookup `core.k:130-154`; callee then left-to-right arguments `call.k:18-21` and `core.k:185-191`; closure frame allocation `call.k:69-74`; parameter bind `functions.k:63-66` |
| docstring `Expr(Str(...))` | `semantics/syntax.k:13,52` | ASCII conversion `str.k:13-17`; expression discard `controls.k:46-48` |
| `Assign(Name("divisor"), BinOp("-", Name("n"), Int(1)))` | `semantics/syntax.k:9-16,41` | sequential operand evaluation; integer literal `core.k:193-196`; subtraction `operators.k:12`, `int.k:13`; local update `controls.k:9-11` |
| `While(Compare(BinOp("%", ...), CmpOp("!=", Int(0))), BODY)` | `semantics/syntax.k:15,30,32,46` | comparison contexts and dispatch `operators.k:14-17`; modulo `int.k:15,19-20`; integer inequality `int.k:27`; while test/body/back-edge `controls.k:65-82` |
| `AugAssign(Name("divisor"), "-", Int(1))` | `semantics/syntax.k:44` | integer subtraction and local update `controls.k:20-23`, `int.k:13` |
| `Return(Name("divisor"))` | `semantics/syntax.k:50` | strict value evaluation, abrupt return, frame pop, environment restoration, and result placement at `functions.k:77-90` |
| runtime/proof cells | `semantics/core.k:49-60` | the claims pin all 10 observable/control cells plus generated counter completion |

The term order is deterministic on this path: statements sequence left to right;
`BinOp` is `seqstrict(2,3)`; assignment, augmented assignment, and return are
strict in their value expression; `Compare` evaluates its left then wrapped
right operand; `Call` evaluates the callee before its arguments; and `While`
re-evaluates its guard before each body iteration. The program allocates one
callee scope and no heap objects. Return discards the remaining callee
continuation, pops exactly the saved frame, deletes the callee scope, restores
the caller environment and allocation counter, and places the returned integer
in the caller computation.

## Proof-local declarations and rules

| Extension | Class and complete domain | Static decision |
|---|---|---|
| `largestDivisorBody()` and its equation (`verification.k:8-17`) | Definitional syntactic sharing, zero arguments, unconditional | Sound. Its RHS is exactly the statement body in the trusted regeneration of `solution.mpy`; it neither skips nor summarizes execution. |
| `largestProperDivisor(N)` equation (`verification.k:22-26`) | Definitional summary for every integer where the recursive scan is later defined | Sound as an initializer: it is exactly `firstDivisorAtOrBelow(N,N-1)`. The target uses only `N>1`. |
| base equation for `firstDivisorAtOrBelow(N,D)` (`verification.k:28-29`) | Definitional summary when `D>0` and `pyMod(N,D)=0` | Sound: the descending scan's first tested candidate divides `N`, so it returns `D`. |
| recursive equation for `firstDivisorAtOrBelow(N,D)` (`verification.k:31-33`) | Definitional summary when `D>1` and `pyMod(N,D) != 0` | Sound: the candidate fails and the next candidate is exactly `D-1`. On the target domain it descends to 1, whose positive-divisor base case applies. Guards are disjoint from the base case. |
| `deleteFreshFrame` (`verification.k:38-41`) | Derived Map simplification for `(1 |-> S SC)[1 <- undef]`, guarded by `1` absent from `SC` | Sound extensional Map fact. The LHS is precisely the scope deletion produced by fixed `#pop`; deleting the unique key 1 leaves `SC`. It changes no value, control, heap, exception, or other cell and is not an operational bridge. |

No proof-local declaration is `total`, `functional`, opaque, `concrete`, or
priority-bearing. There is no rule matching a source-language invocation or
loop that bypasses the supplied semantics. The only simplification is the Map
identity above. The two recursive-summary guards do not overlap: equality and
inequality of the same positive-modulus result are complementary, and at
`D=1`, `pyMod(N,1)=0`.

## Modular claim composition

`PREFIX-SPEC` executes the exact translated module and call through function
loading, lookup, binding, docstring evaluation, assignment, and reaches the
real `#while` head with `D=N-1`. Its destination has:

- `env=1`, `scopeLoc=2`, empty heap, frame `frame(.K,0,1)`, and local
  `{"n":N,"divisor":N-1}`;
- the exact loop, return, and `#endcall` continuation consumed by `LOOP-SPEC`.

For every `N>1`, `D=N-1` satisfies `D>=1` and `D<N`, so `LOOP-SPEC` applies.
Its destination is `firstDivisorAtOrBelow(N,N-1)`, definitionally
`largestProperDivisor(N)`, with the caller cells restored. The reviewer-authored
composition check in `stage4_end_to_end.k` restates those two claims in one
module and proves the resulting public-entry claim to `largestProperDivisor(N)`.
