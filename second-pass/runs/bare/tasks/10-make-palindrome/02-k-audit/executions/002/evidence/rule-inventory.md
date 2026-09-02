# Exhaustive local K inventory

Audited sources:

- `semantic.k`: SHA-256 `97618cb45d23a229beae549f3986b0d85822d8615cd8d7cc9f4c283794d56d8a`
- `verification.k`: SHA-256 `2d635f1231eb5fab6eb935dde601d32a3048d0199956c745628136d5d0d1d6e1`
- `spec.k`: SHA-256 `71cb7ec5e419c0801b70949269978973db75859f122d7300cf49f1aa22bbc79b`

There are 38 local rules (33 in `semantic.k`, 5 in
`verification.k`), 8 reachability claims, no local simplification rules, no
`opaque` declarations, and one explicit priority attribute.

## Syntax, configuration, attributes, and imports

- `MPY-SYNTAX` imports `DOMAINS`.
- AST productions: `Module(Module(Stmts))`; the empty-separated `Stmts` list;
  `Stmt(FuncDef, Return, If)`; one-name `Params`; `Expr(Name, Str, Int,
  UnaryOp, BinOp, Compare, Subscript, Slice, Call)`; `CmpOp`; and
  `Bound(Expr, NoBound)`. Every constructor has `[symbol]`.
- `SOLUTION-AST` imports `MPY-SYNTAX` and declares `#solution : Module`
  `[function]`.
- `MPY-SEMANTICS` imports `MPY-SYNTAX`, `SOLUTION-AST`, `BOOL`, `INT`, and
  `STRING`.
- Runtime data productions: `Val(strVal, boolVal, intVal)`, one-binding
  `Env(env)`, `Function(function)`, and `Outcome(normal, returned)`, all
  `[symbol]`.
- Entry KItems `#run` and `#runFunction` are `[symbol]`.
- Functions: `#lookup`, `#call`, `#apply`, `#eval`, `#exec`, `#resume`,
  `#valueEq`, `#outcomeValue`, `#negate`, `#add`, `#indexZero`, `#tail`, and
  `#reversed`.
- Total functions: `#branch : Val × Stmts × Stmts -> Stmts` and
  `#reverse : String -> String`.
- Configuration: `<mpy>` contains `<k>`, `<program>`, `<input>`,
  `<ast-match>`, and `<result>`. Initial `<k>` is `#run($PGM,$INPUT)`;
  `<ast-match>` is `$PGM ==K #solution`; `<result>` is empty.
- `EXECUTION` imports only `MPY-SEMANTICS`. `SEMANTIC` imports
  `MPY-SEMANTICS` and `VERIFICATION`.
- `VERIFICATION` imports `MPY-SEMANTICS`; it declares total functions
  `#reference` and `#referenceChoice`, plus function `#isPalindrome`.
- There are no `[functional]`, `[simplification]`, or `[opaque]`
  declarations. The sole explicit priority is `[priority(40)]` on V04.

## Construct coverage

`solution.mpy` uses `Module`, `FuncDef`, `Params`, `Return`, `If`, `Name`,
`Int`, `UnaryOp("-")`, `BinOp("+")`, `Compare`/`CmpOp("==")`,
`Subscript`, all three used `Slice` shapes, `NoBound`, and `Call`. These map
respectively to S01/S04-S13 and S16-S33 below. `Str` is declared but unused
by the submitted program. No submitted-program constructor is undeclared or
left without a reachable rule.

## `semantic.k` rules

| ID | Lines | Exact role | Static finding |
|---|---:|---|---|
| S01 | 35-58 | `#solution` expands to the two-function AST | Byte-identical trusted regeneration plus `<ast-match>true</ast-match>` confirms the constructor term. |
| S02 | 98-99 | `#run(P,S)` clears `<k>` and places `#call("make_palindrome",strVal(S),P)` in `<result>` | Faithful entry setup in the five-cell model. |
| S03 | 100-101 | `#runFunction` analog for a named function | Faithful helper entry setup. |
| S04 | 103-104 | Function lookup hit | Correct first matching binding. |
| S05 | 105-107 | Function lookup skips a different name | Disjoint from S04 by `F =/=String G`; correct for the module list. |
| S06 | 109-110 | `#call` performs lookup then apply | Correct binding path; it is preempted for `make_palindrome/#solution` only by V04. |
| S07 | 111-112 | `#apply` binds the single parameter and executes the body | Adequate for the submitted one-argument functions. |
| S08 | 115 | Extracts a returned value | Correct on all reachable submitted-function outcomes. |
| S09 | 117 | Empty statement list yields `normal` | Correct. |
| S10 | 118 | `Return` evaluates its expression and discards trailing statements | Correct return control. |
| S11 | 119-122 | `If` evaluates the condition, executes the selected branch, then resumes the suffix | Correct for pure expressions and the represented control state. |
| S12 | 123 | A returned branch bypasses the suffix | Correct. |
| S13 | 124 | A normal branch resumes the suffix | Correct. |
| S14 | 126-127 | `#branch(boolVal(true),...)` selects then | Correct on its guard. |
| S15 | 128-129 | `#branch(boolVal(false),...)` selects else | Correct and disjoint from S14. The `[total]` declaration is over-broad because no equation covers `strVal` or `intVal`, but those cases are unreachable for the submitted conditions. |
| S16 | 131 | Reads the one matching environment binding | Correct for submitted functions. |
| S17 | 132 | Evaluates a string literal | Correct as a K String value; unused by the submitted body. |
| S18 | 133 | Evaluates an integer literal | Correct for used `0` and `1`. |
| S19 | 134-135 | Integer unary negation | Correct for used `-1`. |
| S20 | 136-137 | String `+` via evaluated operands and `#add` | Pure-expression result/order is adequate for the used path. |
| S21 | 138-139 | Equality comparison via evaluated operands and `#valueEq` | Correct for K Strings. |
| S22 | 140-141 | Index zero via `#indexZero` | Correct dispatch to the K code-point substring primitive. |
| S23 | 142-143 | Slice `[1:]` via `#tail` | Correct dispatch to the K code-point substring primitive. |
| S24 | 144-146 | Slice `[::-1]` via `#reversed` | Correct dispatch to the local code-point reversal. |
| S25 | 147-148 | Direct-name one-argument call | Correct for the fixed module and evaluated argument. |
| S26 | 155 | Integer negation primitive | Correct. |
| S27 | 156 | String concatenation primitive | Correct for K Strings. |
| S28 | 157-158 | `string[0]` as `substrString(S,0,1)` | Correct because K documents String indices as code-point indices. |
| S29 | 159-160 | `string[1:]` as code-point substring | Correct on the nonempty guard. |
| S30 | 161 | Reversal dispatch | Correct. |
| S31 | 163 | String value equality | Correct for represented values. |
| S32 | 165 | Empty reverse | Correct. |
| S33 | 166-169 | Reverse last code point plus recursive prefix | Well-founded and correct for K Strings. |

The local String rules themselves pass fresh fixed-semantics claims for
`"\u00e9"`, `"\u03bb"`, `"\u03bb\u6f22"`, and `"\U0001f642"`; see
`stage5-unicode-formal-claims.log`. There is, however, a separate concrete
input-boundary defect: the candidate's documented `krun ... -cINPUT=...`
interface reinterprets configured code points above U+00FF as their UTF-8 byte
sequence. Fresh execution therefore returns mojibake for `"λ漢🙂"` and for 32
distinct Cyrillic code points, while all ASCII cases and U+00E9 agree. This is
an unvalidated/incorrect Python-input-to-K-configuration bridge, not a false
local substring rule; see `stage3-concrete-semantics-bridge-final.log`.

## `verification.k` rules

| ID | Lines | Exact role | Static finding |
|---|---:|---|---|
| V01 | 10-11 | Dispatches `#reference(S)` on `S ==String #reverse(S)` | A code-point string recursion, not independently proved in K to express the HumanEval property. |
| V02 | 12-13 | Palindromic/true choice returns `S` | Correct on the guard. |
| V03 | 14-18 | False choice mirrors the first code point around recursive tail | Guards are disjoint from V02 and recursion decreases length. The `[total]` declaration is globally over-broad at `#referenceChoice("",false)`, though that ground case is unreachable from V01. |
| V04 | 24-27 | Priority operational bridge: exact `make_palindrome` call on `P ==K #solution` rewrites directly to `strVal(#reference(S))` | Illegitimate target-conclusion axiom. It skips S04-S33; no bridge-free universal connection claim exists. Removing it leaves the universal claim stuck. A constructor-level body mutation to `return "broken"` leaves the claim at `#Top`, while fixed execution returns `"broken"` and bridge-enabled execution returns `"catac"` for `"cat"`. |
| V05 | 32 | Defines `#isPalindrome(S)` as equality with code-point reversal | Truthful for K Strings; the concrete configuration-input bridge remains separate. |

V04 reads the already evaluated `strVal(S)` and exact module `P`; in this
minimal semantics it skips no heap/output cells because none exist. It
nevertheless replaces the entire program-defined lookup, binding, body,
recursive calls, condition, and return computation with the theorem's own
postcondition function. The body-sensitivity witness is in
`stage5-body-mutation-{fixed-krun,bridge-krun,functional-proof}.log`.

## Reachability claims

| ID | Module/label | Domain and postcondition | Finding |
|---|---|---|---|
| C01 | `SPEC.functional-correctness` | Every K `String S`; result is `strVal(#reference(S))` | Result-constraining and syntactically pinned, but closes through V04 without executing the body. |
| C02 | `SPEC.helper-correctness` | Every K `String S`; helper result is `boolVal(#isPalindrome(S))` | Executes the helper body under fixed rules and characterizes K code-point reversal equality. |
| C03 | `CONCRETE-SPEC.empty` | Fixed `""`; result `""` | Honest fixed-semantics example. |
| C04 | `CONCRETE-SPEC.cat` | Fixed `"cat"`; result `"catac"` | Honest fixed-semantics example. |
| C05 | `CONCRETE-SPEC.cata` | Fixed `"cata"`; result `"catac"` | Honest fixed-semantics example. |
| C06 | `CONCRETE-SPEC.xyx` | Fixed `"xyx"`; result `"xyx"` | Honest fixed-semantics example. |
| C07 | `CONCRETE-SPEC.abcd` | Fixed `"abcd"`; result `"abcdcba"` | Honest fixed-semantics example. |
| C08 | `CONCRETE-SPEC.aabb` | Fixed `"aabb"`; result `"aabbaa"` | Honest fixed-semantics example. |
