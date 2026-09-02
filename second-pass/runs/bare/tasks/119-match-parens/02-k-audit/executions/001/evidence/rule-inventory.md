# Reviewer rule and declaration inventory

All line numbers refer to the candidate source copied unchanged into
`/tmp/audit-work/119-match-parens-audit`.

## Local syntax and configuration

- `semantic.k:6`: `Pgm ::= Module(Stmts)`.
- `semantic.k:8-10`: statement lists, comma-separated string lists, and
  `Params(String...)`.
- `semantic.k:12-14`: the three statement constructors used by the program:
  `FuncDef`, `If`, and `Return`.
- `semantic.k:16-20`: expression lists, comparison-operation lists,
  `CmpOp`, optional slice bounds, and `Slice`.
- `semantic.k:22-31`: `Name`, `Int`, `Bool`, `Str`, two-element-capable
  `ListExpr`, `BinOp`, `Compare`, integer and slice `Subscript`, and `Call`.
- `semantic.k:44-46`: inductive parenthesis strings `.PString`, `lp`, `rp`.
- `semantic.k:48-50`: modeled Python strings `parens`, `yesString`,
  `noString`.
- `semantic.k:52-57`: runtime values `intVal`, `boolVal`, `strVal`,
  `listVal`, `closure`, and comma-separated value lists.
- `semantic.k:61`: proof-input-only expression `PStr(PString)`.
- `semantic.k:63-84`: 22 control constructors: `exec`, `eval`, `binRight`,
  `binApply`, `compareRight`, `compareApply`, `indexAt`, `sliceTail`,
  `listSecond`, `makeList2`, `callOne`, `callOneApply`, `callTwoFirst`,
  `callTwoSecond`, `callTwoApply`, `invoke`, `choose`, `returnFrom`,
  `returned`, `finishCall`, `launch`, and `invokeEntry`.
- `semantic.k:101-108`: configuration cells are `<k>`, `<input>`, `<env>`,
  `<functions>`, and `<result>`, under `<mpy>`.
- `semantic.k:110`: results are `noResult` or a runtime `Value`.
- `verification.k:6`: `solutionProgram` is a proof-side `Pgm` alias.
- `verification.k:9-10`: proof functions `balanced` and `contractAnswer`.

The submitted `solution.mpy` uses every source constructor listed above except
`ListExpr`, which is used by the external input term rather than by the module
body. Each used constructor has an operational path below.

## Functions, attributes, and opaque terms

There are eleven `[function]` declarations and no `[total]`, `[functional]`,
`[simplification]`, or `[concrete]` declarations.

- `semantic.k:86`: `chars`. Equations 207-213 cover empty and nonempty
  strings whose next character is `(` or `)`. It is intentionally partial on
  other characters, which are outside the prompt domain.
- `semantic.k:87`: `pconcat`. Equations 215-217 are exhaustive and
  structurally decreasing on the first `PString`.
- `semantic.k:88`: `ptail`. It has no equations and is therefore opaque, but
  it has no occurrences outside its declaration and cannot affect a claim.
- `semantic.k:89`: `literalString`. Equations 202-205 separate `Yes`, `No`,
  and all other source strings; parenthesis literals then depend on `chars`.
- `semantic.k:90-92`: `stringPlus`, `stringHead`, `stringTail`. Equations
  218 and 220-223 cover exactly the parenthesis-string operands reached by the
  submitted program; head/tail are intentionally undefined on the empty
  string, which the program guards before indexing or slicing.
- `semantic.k:93-94`: `valueEq` and `pstringEq`. Equations 225-241 correctly
  cover the same-typed integer, boolean, parenthesis-string, and Yes/No cases
  reached here; cross-type, list, and closure equality are unmodeled and
  unused. `pstringEq` is exhaustive and structurally decreasing.
- `verification.k:9`: `balanced`. Equations 12-15 have disjoint integer
  guards, cover every `PString × Int`, and structurally decrease the string.
- `verification.k:10`: `contractAnswer`. Rules 17-20 return `yesString`
  exactly when one concatenation has `balanced(..., 0) = true`; `[owise]`
  supplies the complementary `noString` case.

The only priority attributes are `[priority(40)]` on the two proof operational
bridges at `verification.k:25-43` and `verification.k:48-65`. The only
`[owise]` rule is `contractAnswer`'s negative case at line 20.

## Ordinary rules in `semantic.k`

Every one of the 76 rules is enumerated here.

| Line | Rule role | Static judgment |
|---:|---|---|
| 114 | `Module` schedules function loading then launch | Sound for the modeled module. |
| 116 | empty `exec` disappears | Sound. |
| 117-119 | load one `FuncDef` into `<functions>` | Sound for top-level, capture-free functions used here. |
| 121-122 | evaluate `If` condition, choose a branch, then continue | Sound and preserves statement order. |
| 123 | true branch selection | Sound. |
| 124 | false branch selection | Sound. |
| 126 | evaluate `Return` and discard later statements in that list | Sound. |
| 127 | turn a returned value into the `returned` control marker | Sound. |
| 129 | discard a pending `exec` continuation after return | Sound for the nested-if control contexts generated here. |
| 132 | integer literal evaluation | Sound. |
| 133 | boolean literal evaluation | Sound. |
| 134 | string literal evaluation through `literalString` | Sound on the modeled strings. |
| 135 | proof-only `PStr` evaluation | A transparent representation bridge from an arbitrary inductive parenthesis string to a modeled Python string. |
| 136 | name lookup in `<env>` | Sound when the name is local. |
| 137 | name lookup in `<functions>` | Sound on this program's disjoint local/function names; globally overlaps line 136 when both maps bind the same name, so the reusable semantics lacks Python's local-first shadowing guard. No such overlap is reachable in the submitted program. |
| 139 | start left-to-right binary evaluation | Sound. |
| 140 | evaluate right operand after the left value | Sound. |
| 141 | integer addition | Sound. |
| 142 | integer subtraction | Sound. |
| 143-144 | modeled string concatenation | Sound for `parens` operands. |
| 147-148 | start the one-link comparison used here | Sound; longer chains are deliberately unmodeled. |
| 149-150 | evaluate the comparison's right operand second | Sound. |
| 151-152 | equality via `valueEq` | Sound for covered same-typed values. |
| 153-154 | integer less-than | Sound. |
| 156 | evaluate an integer subscript receiver first | Sound. |
| 157 | list index zero | Sound. |
| 158-160 | positive list-index recursion | Sound and decreasing; negative/out-of-range cases are unmodeled and unused. |
| 161 | parenthesis-string index zero via `stringHead` | Sound on nonempty strings. |
| 163-164 | recognize exactly the `[1:]` slice used here | Sound. |
| 165 | parenthesis-string tail | Sound on nonempty strings. |
| 167-168 | evaluate the first element of a two-element list literal | Sound. |
| 169 | evaluate the second element after the first | Sound. |
| 170 | construct the two-element list | Sound. |
| 172 | start a one-argument call with callee first | Sound. |
| 173 | evaluate the one argument after the callee | Sound. |
| 174 | invoke the one-argument callee | Sound. |
| 175-176 | start a two-argument call with callee first | Sound. |
| 177-178 | evaluate first argument | Sound. |
| 179-180 | evaluate second argument | Sound. |
| 181 | invoke the two-argument callee | Sound. |
| 185-187 | bind one parameter in a fresh local map and save caller map | Sound for the used arity. |
| 188-191 | bind two parameters left-to-right in a fresh local map | Sound for the used arity. |
| 192-193 | restore the caller map after explicit return | Sound. |
| 195 | evaluate configured input before entry invocation | Sound. |
| 196-197 | resolve and invoke `match_parens` | Sound for a loaded module; it explicitly reads the binding from `<functions>`. |
| 198 | consume the final value and store it in `<result>` | Sound. |
| 202 | source literal `"Yes"` | Sound. |
| 203 | source literal `"No"` | Sound. |
| 204-205 | all other literals become parenthesis strings via `chars` | Sound on the prompt alphabet; execution visibly sticks on other nonempty strings. |
| 207 | empty concrete string conversion | Sound. |
| 208-210 | consume a leading `(` | Sound and length-decreasing. |
| 211-213 | consume a leading `)` | Sound and length-decreasing. |
| 215 | concatenate onto empty left string | Sound. |
| 216 | preserve a leading `lp` while concatenating | Sound and decreasing. |
| 217 | preserve a leading `rp` while concatenating | Sound and decreasing. |
| 218 | modeled string `+` delegates to `pconcat` | Sound. |
| 220 | head of an `lp` string is one `lp` | Sound. |
| 221 | head of an `rp` string is one `rp` | Sound. |
| 222 | tail of an `lp` string | Sound. |
| 223 | tail of an `rp` string | Sound. |
| 225 | integer equality | Sound. |
| 226 | boolean equality | Sound. |
| 227 | parenthesis-string equality | Sound. |
| 228 | `Yes == Yes` | Sound. |
| 229 | `No == No` | Sound. |
| 230 | `Yes == No` | Sound. |
| 231 | `No == Yes` | Sound. |
| 233 | empty equals empty | Sound. |
| 234 | empty differs from `lp` | Sound. |
| 235 | empty differs from `rp` | Sound. |
| 236 | `lp` differs from empty | Sound. |
| 237 | `rp` differs from empty | Sound. |
| 238 | equal leading `lp` reduces to tail equality | Sound and decreasing. |
| 239 | equal leading `rp` reduces to tail equality | Sound and decreasing. |
| 240 | `lp` differs from `rp` | Sound. |
| 241 | `rp` differs from `lp` | Sound. |

## Rules in `verification.k`

| Line | Classification | Static judgment |
|---:|---|---|
| 12 | definitional equation for `balanced` at negative depth | Mathematically true. |
| 13 | definitional equation for empty string at nonnegative depth | Mathematically true. |
| 14 | definitional equation for leading `lp` | Mathematically true and decreasing. |
| 15 | definitional equation for leading `rp` | Mathematically true and decreasing. |
| 17-19 | positive `contractAnswer` equation | Mathematically true by the prompt's definition. |
| 20 | `[owise]` negative `contractAnswer` equation | Mathematically true complement of the preceding case. |
| 25-43 | priority-40 operational bridge for `is_balanced` | **Unsound over its declared match domain and illegitimate as a proof step.** It omits `<functions>`, even though fixed execution resolves the recursive `Name("is_balanced")` there, and no auxiliary fixed-semantics reachability theorem proves the summary. In `bridge-context-witness.k`, fixed semantics returns `boolVal(true)` for input `")"` with a true-returning recursive binding, while the bridge-enabled definition returns `boolVal(false)`. |
| 48-65 | priority-40 operational bridge for `match_parens` | **Unsound over its declared match domain and directly encodes the theorem.** It omits `<functions>`, even though the body calls whatever `"is_balanced"` binding is present, and no auxiliary execution theorem connects the body to `contractAnswer`. For inputs `[")", ")"]` with a true-returning binding, the fixed semantics returns `yesString`, while the bridge-enabled definition returns `noString`. |
| 69-109 | `solutionProgram` alias rule | Acceptable exact program pin: normalized KORE for its expanded RHS is byte-identical to normalized KORE parsed from submitted `solution.mpy` (see `04-program-pinning.log`). |

The bridge witnesses use parenthesis strings from the intended input domain and
a satisfiable complete K configuration admitted by each bridge. The altered
function binding is not reachable from the submitted module-loading entry
claim, but the rules do not constrain it; a globally false proof rule cannot be
justified by an unstated reachability restriction. On the actual entry path,
the `match_parens` bridge still bypasses all program-defined conditionals and
helper calls and assumes the exact result the universal claim requests.

## Claims in `spec.k`

- `spec.k:8-13`: universal entry claim for arbitrary inductive parenthesis
  strings `A,B`; empty environment/functions/result; postcondition
  `strVal(contractAnswer(A,B))`.
- `spec.k:16-21`: closed prompt example `["()(", ")"]`, requiring `yesString`.
- `spec.k:23-28`: closed prompt example `[")", ")"]`, requiring `noString`.

There are no auxiliary helper or recursion reachability claims. Consequently,
neither priority bridge is derived from fixed execution.
