# Reviewer-authored exhaustive local K inventory

The candidate has exactly three top-level K sources: `semantic.k`,
`verification.k`, and `spec.k`. There are no generated helper K files.
Imports from the installed K distribution are outside the candidate-local
inventory.

## `semantic.k`: `MPY-SYNTAX`

Imports: `INT-SYNTAX`, `STRING-SYNTAX`.

Declared sorts:

1. `Pgm`
2. `Params`
3. `Stmt`
4. `Expr`
5. `Value`

Local productions:

1. `Pgm ::= Module(Stmt)`.
2. `Params ::= Params(String)`.
3. `Stmt ::= FuncDef(String, Params, Stmt)`.
4. `Stmt ::= Return(Expr) [strict]`. The strictness attribute generates
   evaluation of the return expression before the return rule.
5. `Value ::= Int(Int)`.
6. `Expr ::= Value`.
7. `Expr ::= Name(String)`.
8. `Expr ::= BinOp(String, Expr, Expr) [seqstrict(2,3)]`. The sequential
   strictness attribute generates left-operand evaluation followed by
   right-operand evaluation.

No token, bracket, macro, priority, associativity, function, total,
functional, simplification, concrete, or opaque declarations occur in this
module.

## `semantic.k`: `MPY`

Imports: `MPY-SYNTAX`, `INT`, `STRING`, `MAP`.

Local productions:

1. `KResult ::= Value`.
2. `Result ::= noResult`.
3. `Result ::= result(Int)`.

Configuration:

1. `<k>` initially contains `$PGM:Pgm`.
2. `<input>` initially contains `$N:Int`.
3. `<env>` initially contains `.Map`.
4. `<result>` initially contains `noResult`.
5. These are wrapped by `<mpy>`.

Ordinary operational rules:

1. Entry/load: `Module(FuncDef(_FN, Params(X), BODY))` becomes `BODY`; for
   input `N` and an empty environment it installs `X |-> N`.
2. Lookup: `Name(X)` becomes `Int(I)` when the environment contains
   `X |-> I`.
3. Addition: `BinOp("+", Int(I), Int(J))` becomes `Int(I +Int J)`.
4. Subtraction: `BinOp("-", Int(I), Int(J))` becomes `Int(I -Int J)`.
5. Multiplication: `BinOp("*", Int(I), Int(J))` becomes `Int(I *Int J)`.
6. Floor-division bridge: `BinOp("//", Int(I), Int(J))` becomes
   `Int(I divInt J)` under `J =/=Int 0`.
7. Return: with result cell `noResult`, `Return(Int(I))` consumes the
   computation and changes the result cell to `result(I)`.

There are no local function, total, functional, opaque, priority,
simplification, concrete, or claim declarations in `MPY`.

## `verification.k`: `VERIFICATION`

Import: `MPY`.

Pure function declarations and their sole defining equations:

1. `choose3(Int) : Int [function, total]`.
   `choose3(X) => X*(X-1)*(X-2) divInt 6`, unguarded.
2. `validTripleCount(Int) : Int [function, total]`.
   It rewrites, unguarded, to
   `choose3((N+1) divInt 3) + choose3(N-((N+1) divInt 3))`.

Coverage is complete because both equations are unguarded. They do not overlap
with another equation for the same symbol. Neither is recursive. There are no
operational bridges, ordinary semantic rules, claims, lemmas, opaque symbols,
priorities, or simplification rules in this file.

## `spec.k`: `SPEC`

Import: `VERIFICATION`.

One unlabeled positive reachability claim and no rules or helper claims. Its
source configuration contains the full `Module(FuncDef(...))` term, input `N`,
empty environment, and `noResult`; it requires `N >=Int 1`. Its destination
requires `.K`, environment `"n" |-> N`, and the result
`result(validTripleCount(N))`. There is no existential result variable.

## Used-construct map

The submitted `solution.mpy` uses every local source-language production:
`Module`, `FuncDef`, `Params`, `Return`, `Int`, the `Value`-to-`Expr`
injection, `Name`, and `BinOp`. Its operator strings are exactly `+`, `-`, `*`,
and `//`, each of which has a corresponding semantic rule. `Return [strict]`
and `BinOp [seqstrict(2,3)]` provide the required evaluation contexts.

The program uses no calls, loops, mutation, allocation, heap, I/O, exceptions,
collections, multiple definitions, default arguments, or identifier tokens in
K claims.

## Static judgments

1. Entry/load is exact for this configured single-function entry convention:
   the submitted module contains the sole function, the function parameter is
   `"n"`, and the start environment is empty. Ignoring the function name is a
   limitation of the tiny language, not a substituted binding on this program.
2. Lookup, integer addition, subtraction, and multiplication agree with Python
   arbitrary-precision integer behavior for this program.
3. The division rule is exact on every reachable division in the submitted
   program under `N >= 1`: denominators are the positive constants `3` and `6`,
   and all divided numerators are nonnegative (products for class sizes
   `0`, `1`, or `2` are zero; later products are positive).
4. The division rule is over-broad as a general Python model. The preserved
   negative-denominator probe evaluates `7 divInt -3` to `-2`, while Python
   `7 // -3` is `-3`. No negative denominator can arise in the submitted
   program on the intended domain, so this is a language-scope limitation and
   not a false conclusion witness for the audited entry claim.
5. Division by zero is modeled as stuck rather than as a Python exception.
   The submitted program has only denominators `3` and `6`, so the omitted
   exception behavior is unreachable.
6. Return consumes the complete computation and changes only the result cell.
   This program has no continuation after its sole return and no other
   observable state effect.
7. `choose3` is a definitional mathematical summary, not an operational
   bridge. Its unguarded equation is total as an integer-valued polynomial
   quotient: a product of three consecutive integers is divisible by six.
   Its combinatorial interpretation is used only at reachable nonnegative
   class sizes.
8. `validTripleCount` exactly names the formula computed by `solution.mpy`.
   It is nonrecursive, fully covered, and has no overlapping equations.
9. There are no fresh or opaque result-bearing values, proof-local operational
   shortcuts, ordinary proof rules, auxiliary circularities, priorities, or
   simplification axioms.
