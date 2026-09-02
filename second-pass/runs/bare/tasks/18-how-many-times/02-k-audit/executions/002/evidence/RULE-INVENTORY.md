# Reviewer rule inventory

Source scope: the candidate contains exactly three K sources:
`semantic.k`, `verification.k`, and `spec.k`. There are no candidate helper K
files.

## Local syntax, attributes, and configuration

- `semantic.k:6`: `Program` has `Module(Stmts)`.
- `semantic.k:8`: `Stmts` is the separator-free generated `List{Stmt,""}`.
- `semantic.k:9-12`: `Stmt` has `FuncDef`, `If`, `Return`, and `Expr`.
- `semantic.k:14-17`: generated comma-separated `Strings`, `Exprs`, and
  `CmpOps`, plus `Params(Strings)`.
- `semantic.k:19-25`: `Expr` has `Int`, `Str`, `Name`, `BinOp`, `Compare`,
  `Call`, and `Subscript`.
- `semantic.k:27-29`: `CmpOp`, `Slice`, and the `Bound` alternatives `Expr`
  and `NoBound`.
- `semantic.k:36-38`: runtime values `intVal`, `strVal`, `boolVal`; stored
  `function`; and abrupt marker `returned`.
- `semantic.k:40-49`: the 15 control items `eval`, `addLeft`, `addRight`,
  `cmpLeft`, `cmpRight`, `ifFrame`, `lenFrame`, `callArgOne`, `callArgTwo`,
  `invoke`, `prefixBase`, `prefixEnd`, `tailFrame`, `makeReturn`, and
  `returnFrame`.
- `semantic.k:51-56`: configuration `<py>` with `<k>`, `<functions>`, and
  `<env>`; there is no stack-depth, exception, heap, or I/O cell.
- `verification.k:7`: `overlapCount(String,String)` is the only local
  `[function]`.
- No local declaration has `[total]`, `[functional]`, `[simplification]`,
  `[concrete]`, an opacity attribute, or a rule-priority attribute. There are
  no local syntax priorities. `spec.k` adds one reachability claim and no
  rule.

## `semantic.k` ordinary rules

| # | Lines | Rule role | Static decision |
|---:|---:|---|---|
| 1 | 59 | unwrap `Module` | Sound for the submitted constructor program. |
| 2 | 60 | consume empty statement list | Sound list-unit transition. |
| 3 | 61 | schedule head statement before tail | Sound left-to-right statement order. |
| 4 | 62 | remove terminal empty statement list after a value | Sound unit cleanup; no observable cell changes. |
| 5 | 64-65 | install a function binding | Sound for the submitted module; only the function map changes. |
| 6 | 67 | enter expression-statement evaluation | Sound. |
| 7 | 70 | integer literal | Sound. |
| 8 | 71 | string literal | Sound for parseable K strings. |
| 9 | 72-73 | environment lookup | Sound when the binding exists; all submitted uses are bound. |
| 10 | 75 | begin integer addition with left operand | Sound left-first evaluation. |
| 11 | 76 | evaluate the right addition operand | Sound and preserves the left value in `addRight`. |
| 12 | 77 | compute integer addition | Sound use of `+Int`. |
| 13 | 79-80 | begin a one-comparator comparison | Sound for the submitted one-comparator expressions. |
| 14 | 81-82 | evaluate comparison right operand | Sound left-to-right order. |
| 15 | 83-84 | string equality | Sound operand orientation; equality is symmetric. |
| 16 | 85-86 | integer less-than | Sound operand orientation (`left < right`). |
| 17 | 89 | evaluate an `If` guard | Sound. |
| 18 | 90 | true branch | Sound under guard `B`. |
| 19 | 91 | false branch | Sound under complementary guard `notBool B`; rules 18/19 are disjoint and exhaustive for `Bool`. |
| 20 | 94 | dispatch the submitted `len` call | Sound for this body, whose environment cannot shadow `len`; not a reusable general-Python name-resolution rule. |
| 21 | 95 | string length | Sound conditional on the trusted `STRING.length` hook. |
| 22 | 97-98 | begin `base[:len(bound)]` | Sound base-before-bound evaluation. |
| 23 | 99-100 | evaluate the prefix bound | Sound. |
| 24 | 101-102 | compute the prefix slice | Sound on reachable submitted states, where the earlier length guard ensures a valid bound. |
| 25 | 104-105 | begin `base[1:]` | Sound. |
| 26 | 106-107 | compute the tail slice | Sound on reachable recursive states; nonempty `T` and `len(S)>=len(T)` imply nonempty `S`. |
| 27 | 109-110 | begin the two-argument recursive call | Sound for the pinned function name, but it models an unbounded abstract call stack. |
| 28 | 111-112 | evaluate the second argument | Sound left-to-right call evaluation. |
| 29 | 113 | form `invoke` after both arguments | Sound within the submitted subset. |
| 30 | 116-122 | enter the pinned body with a fresh parameter environment and saved caller map | Binding and state restoration design is sound in the idealized unbounded-stack model. It omits CPython recursion-depth exceptions. |
| 31 | 124 | evaluate a returned expression | Sound. |
| 32 | 125 | mark abrupt return | Sound. |
| 33 | 128 | discard one following statement after return | Sound; no stateful statement exists in the submitted suffix. |
| 34 | 129 | discard a following statement list after return | Sound; its overlap with rule 33 has the same right-hand side. |
| 35 | 130-131 | pop the saved caller environment and expose the value | Sound for normal returns in the idealized model. |

Rules 27-35 have a material language-model omission when claimed as semantics
of the real CPython program: there is no recursion-limit or exception state.
The concrete witness `string="a"*1000, substring="b"` yields `intVal(0)` under
these rules but raises `RecursionError` in the submitted Python under the
recorded recursion limit 1000. This is an omission of a used control effect,
not an unsupported allegation about any arithmetic equation.

## `verification.k` function equations

| # | Lines | Guard/domain | Decision |
|---:|---:|---|---|
| V1 | 9-10 | `T == ""` | Truthful: the canonical range has `length(S)+1` empty slices. |
| V2 | 12-14 | `T != ""` and `length(S)<length(T)` | Truthful: no occurrence fits. |
| V3 | 16-21 | nonempty `T`, enough source remains, and prefix equals `T` | Truthful overlapping recurrence: count this start and recurse at the next index. |
| V4 | 23-27 | nonempty `T`, enough source remains, and prefix differs | Truthful overlapping recurrence: skip this start and recurse at the next index. |

V1-V4 are pairwise disjoint and exhaustive on K `String` pairs. V3/V4
descend because their guards imply `length(S)>=length(T)>=1`. The function is
not opaque and is not an operational bridge: no semantic rule rewrites program
execution to `overlapCount`.

## `spec.k` claim

`spec.k:8-37` is the sole entry claim. It has no `requires`: `S` and `T` range
over all K Strings, `CONT` over every continuation, and `_ENV` over every map.
It pins the functions cell to a singleton `how_many_times` binding with the
submitted body, rewrites a real `invoke`, requires the same continuation, map,
and binding afterward, and constrains the value to
`intVal(overlapCount(S,T))`. The claim is used coinductively only after
semantic progress at recursive calls.
