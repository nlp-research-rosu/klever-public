# Exhaustive local K inventory and soundness classification

This inventory covers the original candidate's only three K sources:
`semantic.k`, `verification.k`, and `spec.k`. There are no candidate helper K
files. Built-in modules `INT`, `BOOL`, and `domains.md` are external trust
dependencies, not local extensions.

## Local syntax and declarations

`MPY-SYNTAX` declares:

1. `Program`: `Module(Stmts)`.
2. `Stmts`: generated zero-or-more `Stmt` list with empty separator.
3. `Exprs`: generated comma-separated zero-or-more `Expr` list.
4. `Stmt`: five constructors/alternatives: `FuncDef`, `Assign`, `While`, `If`,
   and `Return`.
5. `Expr`: six constructors/alternatives: `Name`, `Int`, `Bool`, `ListExpr`,
   `BinOp`, and `Compare`.
6. `Cmp`: `CmpOp`.

`MPY` additionally declares:

7. `PList`: `nil`, `cons(Int,PList)`, and
   `chooseCons(Bool,Int,PList)`.
8. `chooseCons` is the only semantic function declaration and has `[function,
   total]`.
9. The configuration has exactly `<k>`, `<n>`, and `<result>` inside `<mpy>`.
   `<k>` initially holds `$PGM:Program`, `<n>` holds `$N:Int`, and `<result>`
   initially holds `.K`.
10. Four `KItem` control constructors: `scan`, `trial`, `prependIf`, and
    `returnValue`.

`VERIFICATION` additionally declares:

11. `noFactor(Int,Int):Bool [function,total]`.
12. `isPrime(Int):Bool [function,total]`.
13. `primesFrom(Int,Int):PList [function,total]`.
14. `primesBelow(Int):PList [function,total]`.

There are no local `[functional]`, `[simplification]`, `[priority]`, `owise`,
macro, anywhere, heating/cooling, fresh-variable, or opaque-symbol
declarations. None of the local rules has an explicit priority. All
result-bearing functions have visible equations.

## `semantic.k` rules

S1. `chooseCons(true,C,P) => cons(C,P)`.

- Class: definitional Boolean case.
- Soundness: valid.

S2. `chooseCons(false,_,P) => P`.

- Class: definitional Boolean case.
- Soundness: valid. S1/S2 are disjoint and cover the built-in `Bool` sort, so
  `[total]` is justified.

S3. The exact full `Module(FuncDef("count_up_to", Params("n"), ...))` tree
rewrites to `scan(2,N) ~> returnValue`, reading `<n> N` and framing the
continuation and `<result>`.

- Class: program-specific semantic lowering/operational bridge.
- Complete matched context: the exact parsed function name, sole parameter,
  every statement and expression in the body, the current continuation, `<n>`,
  and the framed result cell.
- State footprint: reads `<n>`; preserves `<result>`; replaces only the exact
  program term at the head of `<k>`.
- Fidelity map: `primes=[]` is the empty suffix later produced by the scan base;
  `candidate=2` becomes `scan(2,N)`; the outer guard becomes the two `scan`
  rules; `is_prime=True` and `divisor=2` become `trial(C,2,true,N)`; the inner
  guard and modulo `if` become the three `trial` rules; both increments become
  `D+1` and `C+1`; list append becomes suffix recursion plus `prependIf`; and
  return becomes `returnValue`.
- Classification: faithful on the exact submitted term and non-negative input
  domain. It contains no `primesBelow`, `isPrime`, or other specification
  symbol and therefore does not directly encode the desired answer. Its
  monolithic, non-compositional source-to-state-machine connection remains an
  informal generated-semantics trust boundary rather than a separately proved
  connection theorem.

S4. `scan(C,N) => nil` when `C >= N`.

- Class: outer-loop base.
- Soundness: valid; no candidates remain in `[C,N)`.

S5. `scan(C,N) => trial(C,2,true,N)` when `C < N`.

- Class: outer-loop step and inner-loop initialization.
- Soundness: valid on the reachable invariant `C >= 2`. S4/S5 are disjoint and
  exhaustive over integers.

S6. `trial(C,D,B,N) => scan(C+1,N) ~> prependIf(C,B)` when `D*D > C`.

- Class: inner-loop exit and outer increment.
- Soundness: valid: the source loop guard is false, the current flag controls
  append, and `candidate` advances by one.

S7. `trial(C,D,_B,N) => trial(C,D+1,false,N)` when `D*D <= C`,
`C % D == 0`, and `D != 0`.

- Class: divisible branch plus divisor increment.
- Soundness: valid; assignment to false is idempotent and the source does not
  break.

S8. `trial(C,D,B,N) => trial(C,D+1,B,N)` when `D*D <= C`,
`C % D != 0`, and `D != 0`.

- Class: non-divisible branch plus divisor increment.
- Soundness: valid. On reachable `D >= 2`, S6/S7/S8 are pairwise disjoint and
  exhaustive, modulo the trusted integer remainder operation.

S9. `P ~> prependIf(C,B) => chooseCons(B,C,P)`.

- Class: list accumulation.
- Soundness: valid. Recursive evaluation computes the later-candidate suffix
  first, so prepending `C` yields the same ascending list that forward Python
  execution obtains by appending `C` to its accumulated prefix.

S10. `P ~> returnValue => .K` and `<result> .K => P`.

- Class: entry return.
- Soundness: valid for the initial configuration and entry claim, both of which
  require an empty result cell. The surrounding continuation is framed rather
  than discarded.

## `verification.k` rules

V1. `noFactor(C,D) => true` when `D*D > C`.

- Class: recursive mathematical definition, base.
- Soundness: valid for `C >= 2, D >= 2`: there are no remaining tested divisors.

V2. `noFactor(C,D) => false` when `D*D <= C`, `C % D == 0`, and `D != 0`.

- Class: recursive mathematical definition, divisor case.
- Soundness: valid.

V3. `noFactor(C,D) => noFactor(C,D+1)` when `D*D <= C`,
`C % D != 0`, and `D != 0`.

- Class: recursive mathematical definition, non-divisor case.
- Soundness: valid and descending toward V1 on the theorem domain.

V1/V2/V3 are disjoint and exhaustive for the only proof uses (`C >= 2`,
`D >= 2`). The `[total]` annotation is over-broad globally: `noFactor(0,0)`
has no applicable defining equation because remainder by zero is undefined.
No theorem-domain state reaches `D=0`, so this is recorded as a declaration
coverage gap, not an intended-domain unsoundness finding.

V4. `isPrime(C) => false` when `C < 2`.

- Class: mathematical definition.
- Soundness: valid.

V5. `isPrime(C) => noFactor(C,2)` when `C >= 2`.

- Class: mathematical definition.
- Soundness: valid by the standard divisor bound: a composite integer at least
  two has a divisor between two and its square root. V4/V5 are disjoint and
  exhaustive, and `[total]` is justified.

V6. `primesFrom(C,N) => nil` when `C >= N`.

- Class: result-list definition, base.
- Soundness: valid.

V7. `primesFrom(C,N) => chooseCons(isPrime(C),C,primesFrom(C+1,N))`
when `C < N` and `C >= 2`.

- Class: result-list definition, step.
- Soundness: valid and descending toward V6 on `C >= 2`.

V6/V7 are disjoint and exhaustive on every theorem use. The `[total]`
annotation is over-broad globally because `C < N` and `C < 2` has no defining
equation. This off-domain coverage gap cannot affect `scan-correct`
(`C >= 2`) or `primesBelow`, which starts at two.

V8. `primesBelow(N) => primesFrom(2,N)`.

- Class: definitional alias.
- Soundness: valid and total for all integer `N`.

## Claims

C1 `trial-correct`: for `C >= 2` and `D >= 2`, the remaining divisor loop
equals advancing to `scan(C+1,N)` and conditionally prepending `C` according to
the existing flag conjoined with `noFactor(C,D)`.

C2 `scan-correct`: for `C >= 2`, the operational scan equals
`primesFrom(C,N)`.

C3 `count-up-to-correct`: for every integer `N >= 0`, the exact submitted
program term terminates in this semantics with result `primesBelow(N)`.

C1 is C2's circularity dependency; C1 and C2 are C3's dependencies. Every
positive target was reconstructed with that dependency closure. The
`scan`-without-helper diagnostic failure is not a counterexample to C2; it
removes C1 and exposes raw symbolic divisor unrolling.

## Constructor coverage

Every constructor in `solution.mpy` is declared: `Module`, `FuncDef`, `Params`,
`Assign`, `While`, `If`, `Return`, `Name`, `Int`, `Bool`, `ListExpr`, `BinOp`,
`Compare`, and `CmpOp`, plus the generated `Stmts` and `Exprs` list units. Each
occurrence is matched by S3, and every material operation it denotes is mapped
to S4-S10 as detailed above. Unsupported unused translator constructs are
irrelevant in generated-semantics mode.

The configuration's `<n>` cell is the entry-call argument. S3 checks the
binding name `count_up_to`, the sole formal `n`, and every `Name("n")`
occurrence before using that cell, so there is no name-only rebinding shortcut.
All evaluated source expressions are pure integer/Boolean operations; the only
potential exceptional operation is remainder, and reachable divisors are at
least two. Reordering the recursive list construction is observationally inert
here: no alias, identity comparison, mutation, heap, I/O, or exception can
observe Python list allocation, and the final element sequence and order agree.
There is no omitted source call, break, output, global state, or exception path
in the submitted implementation.
