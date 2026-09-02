# Exhaustive local rule and syntax inventory

This inventory covers the submitted `semantic.k`, `verification.k`, and
`spec.k`. Imported K builtins are recorded separately as the trust boundary.

## Local syntax declarations

`semantic.k`, module `MPY-SYNTAX`:

1. `#Layout ::= r"[ \n\r\t]+"`.
2. `Pgm ::= Module(Stmts)`.
3. `Stmts ::= Stmt | Stmt Stmts`.
4. `Exprs ::= List{Expr, ","}`.
5. `Params ::= Params(String)`.
6. `CmpPart ::= CmpOp(String, Expr)`.
7. `Stmt` has six constructors: `ImportFrom`, `FuncDef`, `Assign`, `For`,
   `If`, and `Return`.
8. `Expr` has eight constructors: `Name`, `Str`, `Int`, `ListExpr`,
   `Attribute`, `Call`, `Compare`, and `BinOp`.

`semantic.k`, module `MPY`:

9. `PyValue` has `pyInt`, `pyStr`, `pyBool`, `pyList`, and `noResult`.
10. `Function ::= function(String, Stmts)`.
11. `KItem` adds thirteen control terms: `invoke`, `store`, `finishReturn`,
    `prepareMethod`, `applyMethod`, `compareRight`, `compareApply`, `binRight`,
    `binApply`, `choose`, `startFor`, `loop`, and `bind`.
12. `List ::= splitWords(String) [function]`.

`verification.k`, module `MPY-VERIFICATION`:

13. Nullary `Stmts ::= parserBranch [function, total]`.
14. Nullary `Stmts ::= parserFunctionBody [function, total]`.
15. Nullary `Pgm ::= theProgram [function, total]`.

There are no local `functional` declarations, opaque symbols, priority rules,
strictness attributes, or syntax macros. The three proof-side names are
nullary total K functions, not opaque constants.

## Configuration

The generated semantics has exactly four user-visible cells:

- `<k>`: translated program followed by `invoke("parse_music", INPUT)`;
- `<functions>`: map from function name to parameter/body;
- `<env>`: current local bindings;
- `<result>`: `noResult` until `Return`.

There is no heap, call stack, exception state, output, allocation counter, or
I/O cell. These omissions are adequate for this exact program because it has
one top-level call, immutable strings/integers, no aliases escaping the local
list construction, no exceptions on the valid-note domain, and a final
`Return`. They are not a reusable model of full Python.

## Operational and equational rules

All 36 rules in `semantic.k` are listed below in source order.

| No. | Lines | Rule / role | Classification and audit result |
|---:|---:|---|---|
| 1 | 73 | `Module(SS) => SS` | Operational module-entry rule; faithful for the target constructor module. |
| 2 | 74 | `S SS => S ~> SS` | Operational left-to-right statement sequencing; faithful. |
| 3 | 76 | `ImportFrom(_,_) => .K` | Trusted typing-import erasure; `typing.List` has no runtime influence here. |
| 4 | 77-78 | `FuncDef` stores `function(P,BODY)` | Operational binding rule; faithful for the one top-level function. |
| 5 | 80-82 | `invoke` looks up the binding, installs argument env, runs body | Operational call rule. It lacks general frames/caller locals but is exact for the sole top-level call. |
| 6 | 85 | `Assign(Name(X),E) => E ~> store(X)` | Operational evaluation-order rule; faithful. |
| 7 | 86-87 | value/store updates `<env>` | Operational assignment; faithful. |
| 8 | 89 | `Return(E) => E ~> finishReturn` | Operational return evaluation; faithful for the final statement. |
| 9 | 90-91 | value/finishReturn stores `<result>` | Operational return completion. It would not discard a later continuation, but no such continuation exists in the submitted body. |
| 10 | 93 | `If` evaluates guard before `choose` | Operational evaluation-order rule; faithful. |
| 11 | 94 | true `choose` selects then branch | Operational control rule; faithful. |
| 12 | 95 | false `choose` selects else branch | Operational control rule; faithful. |
| 13 | 97 | `For` evaluates iterable before `startFor` | Operational evaluation-order rule; faithful. |
| 14 | 98 | list/startFor creates a `loop` | Operational loop setup; faithful for list iteration. |
| 15 | 99 | empty `loop` terminates | Operational loop base; faithful. |
| 16 | 100-101 | nonempty `loop` binds head, runs body, recurs on tail | Operational loop step and order; faithful. |
| 17 | 102-103 | `bind` updates loop variable | Operational binding; faithful. |
| 18 | 106 | `Int(I) => pyInt(I)` | Literal semantics; faithful. |
| 19 | 107 | `Str(S) => pyStr(S)` | Literal semantics; faithful. |
| 20 | 108-109 | `Name(X)` looks up `<env>` | Variable lookup; faithful on all target states. |
| 21 | 110 | empty list literal | Literal semantics; faithful. |
| 22 | 111 | singleton integer list literal | Literal semantics; faithful for every target list literal. |
| 23 | 119-120 | `splitWords("o " + S)` prefix equation `[simplification]` | Truthful specialization of explicit-separator split; first separator is at index 1. |
| 24 | 121-122 | `splitWords("o| " + S)` prefix equation `[simplification]` | Truthful specialization; first separator is at index 2. |
| 25 | 123-124 | `splitWords(".| " + S)` prefix equation `[simplification]` | Truthful specialization; first separator is at index 2. |
| 26 | 125-126 | no-separator `splitWords` equation | Truthful base case, guarded by `findString == -1`. |
| 27 | 127-131 | separator-present recursive `splitWords` equation | Truthful recursive case; suffix begins after the first separator and strictly shortens. |
| 28 | 133-134 | split call evaluates receiver first | Operational call-order rule; faithful. |
| 29 | 135-136 | split call evaluates its one argument second | Operational call-order rule; faithful. |
| 30 | 137-138 | string `.split(" ")` returns `splitWords(S)` | Trusted primitive bridge to the fully defined helper; faithful to CPython explicit-separator behavior. |
| 31 | 141-142 | comparison evaluates left first | Operational evaluation-order rule; faithful. |
| 32 | 143-144 | comparison evaluates right second | Operational evaluation-order rule; faithful. |
| 33 | 145-146 | string equality | Trusted K string-equality primitive; faithful. |
| 34 | 148 | binary operation evaluates left first | Operational evaluation-order rule; faithful. |
| 35 | 149-150 | binary operation evaluates right second | Operational evaluation-order rule; faithful. |
| 36 | 151-152 | list `+` concatenates K lists | Operational value rule; faithful because target lists have no observable aliases. |

Rules 23-27 define the only non-builtin local function. The three
simplification guards overlap the general separator-present guard, but their
right-hand sides agree exactly with the general rule. The three specialized
prefixes are pairwise disjoint. The two general guards (`findString == -1`
versus `>= 0`) are disjoint and cover K strings. The recursive rule strictly
decreases the suffix length. `splitWords` is not declared `total`; no
unsupported value sort is silently totalized.

The three equations in `verification.k` are:

| No. | Lines | Equation | Classification and audit result |
|---:|---:|---|---|
| 37 | 9-17 | `parserBranch =>` exact nested-if constructor term | Definitional summary; one unguarded equation for a nullary total function. |
| 38 | 20-25 | `parserFunctionBody =>` exact assignment/for/return body | Definitional summary; one unguarded equation for a nullary total function. |
| 39 | 28-31 | `theProgram =>` exact module/function binding | Definitional summary; one unguarded equation for a nullary total function. |

Each nullary total function has complete, nonoverlapping coverage. The
machine-checked identity claim in `04_program-identity-spec.k` confirms that
`theProgram` simplifies to the trusted translator's regenerated constructor
term (with `ListExpr()` represented canonically as `ListExpr(.Exprs)`).

## Construct-to-rule coverage for `solution.mpy`

| Submitted constructor | Declaration | Executing rules |
|---|---|---|
| `Module` | syntax item 2 | rule 1 |
| `ImportFrom("typing","List")` | statement constructor | rule 3 |
| `FuncDef`, `Params` | statement/parameter constructors | rule 4 |
| top-level invocation | control syntax item 11 | rule 5 |
| multi-statement body | syntax item 3 | rule 2 |
| `Assign(Name, ...)` | statement/expression constructors | rules 6-7, 20 |
| empty and singleton `ListExpr` | expression constructor | rules 21-22, 18 |
| `For(Name, Call(...), body)` | statement constructor | rules 13-17 |
| `Attribute`, `Call`, `Str(" ")` for split | expression constructors | rules 19, 23-30 |
| nested `If` | statement constructor | rules 10-12 |
| `Compare`, `CmpOp("==", ...)` | expression/comparison constructors | rules 19, 20, 31-33 |
| `BinOp("+", list, list)` | expression constructor | rules 18, 20, 22, 34-36 |
| final `Return(Name("beats"))` | statement constructor | rules 8-9, 20 |

Every material operation in the submitted constructor program is executed.
There is no proof rule that returns the task answer, no unconstrained oracle,
and no operational bridge in `verification.k`.

## Claims in `spec.k`

There are 11 unlabeled positive claims:

1. Exact end-to-end result and final state for input `"o"`.
2. Exact end-to-end result and final state for the documented 11-note example.
3. Exact end-to-end result and final state for input `"o|"`.
4. Exact end-to-end result and final state for input `".|"`.
5. One symbolic loop step for head token `"o"` and arbitrary `PREFIX, REST`.
6. One symbolic loop step for head token `"o|"` and arbitrary `PREFIX, REST`.
7. One symbolic loop step for head token `".|"` and arbitrary `PREFIX, REST`.
8. Empty-loop plus final return for arbitrary `PREFIX`.
9. Partial source-to-loop reachability for strings `"o" + " " + T`.
10. Partial source-to-loop reachability for strings `"o|" + " " + T`.
11. Partial source-to-loop reachability for strings `".|" + " " + T`.

The claims are target obligations, not imported semantic rules or reusable
lemmas. Claims 5-11 do not compose into a universal entry-point postcondition.
In particular, claims 9-11 stop before any loop iteration and leave
`<result> noResult`; they constrain no returned list.

## Imported trust boundary

The definition trusts K's `INT`, `STRING`, `BOOL`, `MAP`, `LIST`, and parser
modules, especially `findString`, `substrString`, `lengthString`,
`==String`, string concatenation, map lookup/update, and list concatenation.
It also relies on the informal correspondence between those K builtins and
the relevant CPython operations. Concrete differential evidence tests that
bridge but does not prove it universally.
