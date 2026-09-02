# Reviewer rule inventory

Sources inventoried: scratch copies of `semantic.k`, `verification.k`, and
`spec.k`. Line numbers below refer to the immutable candidate files.

## Local syntax and attributes

`semantic.k` declares the following source constructors:

- `Pgm ::= Program`; `Module(Stmts)`; the empty-separated `Stmts` list.
- `FuncDef(String, Params, Stmts)`, `Assign(Expr, Expr)`, and `Return(Expr)`.
- `Params(StringList)` and the comma-separated `StringList`.
- `Name(String)`, `Int(Int)`, `Subscript(Expr, Index)`, and
  `Call(Expr, Exprs)`, plus the comma-separated `Exprs`.
- the `Index ::= Expr` subsort, `Slice(Bound, Bound, Bound)`, the
  `Bound ::= Expr` subsort, and `NoBound`.
- comma-separated integer sequences `Ints`, `VList(Ints)`, and `VInt(Int)`.

It declares runtime constructors `returned(Value)` and `finished(Map)`.
It declares ten `[function]` symbols: `exec`, `eval`, `sliceThird`,
`sortedValue`, `assignThird`, `thirds`, `thirdsFrom`, `sortInts`,
`insertInt`, and `replaceThirdInts`. `verification.k` adds the eleventh
`[function]` symbol, `contractResult`.

All displayed constructor/function symbols except list/subsort/no-bound
productions have explicit `[symbol(...)]` attributes as shown in source.
There are no local `[total]`, `[functional]`, `[simplification]`,
`[concrete]`, `[owise]`, priority, or opaque declarations. There are no local
syntax macros. The only claims are the three reachability claims in `spec.k`.

The configuration is:

- `<k>`: initial parsed `Pgm`, then an `exec`/`returned` computation;
- `<input>`: the supplied `Value`, preserved by every rule;
- `<result>`: initially `.K`, written once with the returned `Value`.

## Rule-by-rule review

| # | Source | Rule/function equation | Classification and audit |
|---:|---|---|---|
| 1 | `semantic.k:65` | Load `Module(FuncDef("sort_third", Params(P), BODY))` | Target-local operational rule. It selects the exact entry-point name, binds its sole parameter to `<input>`, and executes `BODY`; the submitted module has exactly that shape. |
| 2 | `semantic.k:69` | `returned(V)` writes `<result>` | Operational return completion. It consumes only the `returned` marker, writes the initially empty result cell, preserves input and any continuation. |
| 3 | `semantic.k:72` | `eval(Name(X), RHO)` | Map lookup guarded by key membership and cast to `Value`; correct for target locals `l` and `result`. |
| 4 | `semantic.k:74` | `eval(Int(I), _)` | Truthful literal injection into `VInt`; unused by the exact target because stride `Int(3)` is pattern-matched syntactically. |
| 5 | `semantic.k:75` | full slice evaluates to the same `Value` | Target-local value abstraction for `l[:]`. For integer lists, later assignment replaces the `result` map binding with a fresh value term and leaves `l`/`<input>` unchanged, so the omitted allocation identity is unobservable to this target. |
| 6 | `semantic.k:77` | stride-three slice calls `sliceThird` | Correct target-local interpretation of `[::3]`; bounds are exactly `(None,None,3)`. |
| 7 | `semantic.k:79` | `Call(Name("sorted"), E)` calls `sortedValue` | Correct for the exact unshadowed builtin binding selected by this module. It is deliberately not a reusable Python name-resolution semantics; other programs that shadow `sorted` are outside this target-local model. |
| 8 | `semantic.k:82` | `sliceThird(VList(IS))` | Definitional wrapper around `thirds(IS)`. |
| 9 | `semantic.k:83` | `sortedValue(VList(IS))` | Definitional wrapper around `sortInts(IS)`. |
| 10 | `semantic.k:84` | `assignThird(VList(IS), VList(RS))` | Definitional wrapper around replacement beginning at index zero. In the target, `RS` comes from sorting `thirds(IS)`, so it has exactly the required length. |
| 11 | `semantic.k:87` | `exec(.Stmts, RHO)` | Truthful normal fall-through result; not reached by the submitted body because it returns. |
| 12 | `semantic.k:88` | name assignment | Evaluates the RHS in the old environment, updates one binding, then executes the suffix. This models the target's `result = l[:]`. |
| 13 | `semantic.k:90` | stride-three subscript assignment | Looks up the target list and evaluates the RHS in the pre-update environment, then replaces only the target binding. For the pure target expressions, the equation preserves relevant evaluation behavior and input. |
| 14 | `semantic.k:96` | return | Evaluates the return expression, discards the remaining function-body statements, and produces `returned`; correct Python return control for the target. |
| 15 | `semantic.k:98` | `thirds(IS)` | Starts a three-position counter at zero. |
| 16 | `semantic.k:99` | `thirdsFrom(_, .Ints)` | Empty-list base case; no selected values remain. |
| 17 | `semantic.k:100` | counter zero | Selects the head and resets the counter to two, hence selects indices 0, 3, 6, ... . |
| 18 | `semantic.k:101` | positive counter | Drops an unselected head and decrements. It strictly descends on the finite source list. |
| 19 | `semantic.k:104` | `sortInts(.Ints)` | Empty insertion-sort base case. |
| 20 | `semantic.k:105` | nonempty `sortInts` | Recursively sorts the tail, then inserts the head; it strictly descends on the finite list. |
| 21 | `semantic.k:106` | insert into empty | Produces the singleton list. |
| 22 | `semantic.k:107` | insert before `J` when `I <= J` | Correct ascending insertion branch, including equality. |
| 23 | `semantic.k:109` | pass `J` when `I > J` | Correct complementary insertion branch and strict descent. For mathematical integers, `<=` and `>` are disjoint and exhaustive. |
| 24 | `semantic.k:112` | replace when source and replacements are empty | Correct simultaneous base case for target-generated equal-length replacement data. |
| 25 | `semantic.k:113` | replacement counter zero | Replaces the selected head, consumes one replacement, and resets the counter to two. |
| 26 | `semantic.k:115` | positive replacement counter | Preserves an unselected head and decrements without consuming a replacement. It strictly descends on the source list. |
| 27 | `verification.k:10` | `contractResult(IS)` | Definitional contract summary: extract indices divisible by three, insertion-sort them, and weave them back. It does not rewrite the program term; the entry proof executes rules 1–26 and equates that result with this definition. |

## Coverage, overlaps, and omissions

The submitted `solution.mpy` uses exactly `Module`, `FuncDef`, `Params`,
`Assign`, `Name`, full and stride-three `Subscript`/`Slice`, `NoBound`,
`Int(3)`, the one-argument `Call(Name("sorted"), ...)`, `Return`, statement
sequencing, and integer lists. Every used construct maps to a declaration and
one of rules 1–27.

The relevant rule heads are disjoint: full and stride-three slices differ
syntactically; name and subscript assignments differ syntactically; empty and
nonempty lists differ; counter-zero and positive-counter guards are disjoint;
and integer `<=`/`>` insertion guards are complementary. No rule has a
priority, totality, or simplification attribute that could assert additional
coverage. Unsupported forms therefore remain visibly stuck.

The model is intentionally target-local, not reusable full Python semantics.
It omits arbitrary calls, general slices, heaps, exceptions, user-defined
objects, identity, and shadowing behavior. Those omissions do not fabricate a
result for the exact integer-list execution. The source-contract domain issue
caused by representing list elements only as `Int` is assessed separately in
the review.
