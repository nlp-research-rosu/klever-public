# Static soundness review

The exhaustive lexical inventory is `k-rule-inventory.md` / `.json`
(inventory SHA-256
`ec054996094f700acd4a31dd662b7d92f38554e1e8787984f313e5a1a6175b83`).
It enumerates all 933 outer K sentences: 228 syntax declarations, one
configuration, five contexts, 697 rules, and two claims. Of the rules, 695
belong to the byte-identical supplied reference semantics and two are
proof-local simplification equations.

## Per-entry decision policy

- Every syntax declaration, context, and the configuration is accepted as part
  of the fixed supplied MPY language boundary. The candidate did not modify
  these entries. Declarations used by this program are mapped below; the rest
  introduce constructors that cannot arise from `solution.mpy`.
- Every one of the 695 fixed-semantic rules was read in source order. Rules
  outside the execution slice below are classified `FIXED / NONCONTRIBUTING`
  for this theorem: their left-hand sides require floats, lists, tuples, dicts,
  sets, ranges, comprehensions, string methods, imports, assertions, sorting,
  subscripting, or other constructors absent from the submitted program and
  absent from the two claims. No such rule can rewrite the reached Int-only
  configurations.
- The 22 fixed `[no-evaluators]` opaque declarations are
  `md5hexCodes`, the float-family symbols (`intFloatDiv`, `divII`,
  `floatMod`, `floatLt`, `absF`, `subF`, `divF`, `addF`, `mulF`, `powF`,
  `gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`,
  `roundFN`, `sqrtF`), `sortVS`, and `sortKeyVS`. None is reachable from the
  program or occurs in a claim/postcondition, so none influences control,
  state, or result here.
- All 45 fixed priority rules and 26 fixed `owise` rules were checked for an
  overlap with the program slice. The only potentially adjacent specialized
  rules concern heap references/cells or non-Int calls; the proof states have
  an empty heap and plain scopes, so their guards or constructor patterns are
  disjoint. Priority does not bypass any program operation.
- The two proof-local rules are reviewed individually below. There is no
  proof-local ordinary rewrite, priority rule, operational bridge, opaque
  symbol, or trusted primitive.

This classification decides every inventory entry. The fixed-reference
classification is an explicit trust boundary selected by the audit prompt,
not a claim that the supplied minimal language is a complete CPython model.

## Used constructor-to-rule map

| Program constructor/effect | Declaration and operational rules | Decision |
|---|---|---|
| `Module`, `FuncDef`, `Params`, statement sequence | `syntax.k:41-61`; `core.k:124-127`; `functions.k:14-16` | The fixed module loader sequences the module, and `FuncDef` binds the exact closure body in scope 0. Fresh `krun solution.mpy` reaches exactly that binding. |
| `Expr(Str(...))` docstring | `syntax.k:9-30,41-54`; `str.k:10-17`; `controls.k:48-50` | ASCII string literal is evaluated, then discarded. It changes no cell relevant to the theorem. |
| `Assign(Name(...), ...)` | strict RHS declaration at `syntax.k:41-54`; `controls.k:9-18` | The plain-scope rule writes the current local map. The priority cell rule is inapplicable because the local map has no `$cells`. Assignments occur in program order. |
| `Name`, `Int` | `core.k:131-156,194` | Lookup walks the exact local/global/builtins parent chain; integer literals become mathematical K `Int`. No heap/cell path is enabled. |
| `While`, `#while`, guard truth | `controls.k:65-84`; `core.k:199-205` | The guard is re-evaluated each iteration. Nonzero Int enters the body; zero exits. `#loopLbl` restores the next loop head after the complete three-statement body. |
| `Compare(..., "!=")` | compare contexts and dispatch at `operators.k:15-17`; Int case `int.k:27` | Left then right operand evaluation is explicit; Int inequality is exact. Specialized container/reference rules are disjoint. |
| `BinOp("%", ...)` | `seqstrict(2,3)` at `syntax.k:9-30`; dispatch `operators.k:12-14`; `int.k:15,19-20` | Both operands evaluate left-to-right. The loop guard guarantees divisor `b != 0`. `pyMod` is Python floor-modulo, including negative divisors. |
| user call and argument binding | `call.k:19-21,69-79`; `core.k:186-191,213-215`; `functions.k:63-77` | Callee lookup precedes left-to-right argument evaluation. The exact selected closure allocates a plain local scope, pushes the exact frame, and binds `a,b`. No binding is pinned by a proof shortcut. |
| builtin `abs` | `core.k:152-184`; `call.k:31`; `builtins.k:17-19,44-46` | The global-shadow exclusion in `gcd-loop` forces lookup to the fixed builtins scope. The entry state has only the function global, so it satisfies that guard. Int `abs` is exact. |
| `Return` and frame cleanup | strict declaration `syntax.k:41-54`; `functions.k:78-90` | The return expression executes, `retV` records it, and `#pop` restores env 0, removes local scope 1 and the frame, resets `scopeLoc`, and resumes `CONT`. Heap, exception, and exit code remain as claimed. |

The fixed configuration (`core.k:49-67`) supplies env 0, module scope 0,
builtins scope -1, empty heap/stack, `noRet`, `NoExc`, and exit code 0. The
entry claim uses the state reached after module loading rather than fabricating
a different environment; fresh concrete execution records that exact state.

## Proof-local extension review

1. `syntax Int ::= gcdEuclid(Int, Int) [function, total]`

   Classification: definitional summary. It never appears on the left of an
   operational `<k>` rewrite and therefore replaces no execution. It influences
   only the loop claim's result/postcondition.

2. `gcdEuclid(A, 0) => absInt(A) [simplification]`

   True base equation for the conventional non-negative gcd. Its guard domain
   is exactly second argument zero.

3. `gcdEuclid(A, B) => gcdEuclid(B, pyMod(A,B)) requires B =/=Int 0`

   True Euclidean recurrence. For nonzero `B`, fixed `pyMod` returns the
   Python-floor remainder `R` with `A = q*B + R` and `|R| < |B|`; therefore
   `(A,B)` and `(B,R)` have exactly the same common divisors. Absolute value of
   the second argument strictly descends, so the equations terminate. The
   nonzero guard is disjoint from and exhaustive with the base equation.

There are no overlaps with unequal right-hand sides, no uncovered use of the
declared total function, and no circular value oracle: the loop executes fixed
semantics and is related coinductively to the independently defined Euclidean
summary. No unsound rule or false-conclusion witness was found.

## Claim review

- `gcd-entry` executes the actual function call and reaches the exact loop-head
  state after the docstring and `remainder = 0`. Its formal domain is all K
  integers `A,B` in the exact post-module environment.
- `gcd-loop` executes the actual loop, return, builtin call, and frame cleanup,
  producing `gcdEuclid(A,B)`. Its only semantic precondition beyond the exact
  frame is that the global scope does not shadow `abs`.

The entry target and loop source unify with `GLOBALS` equal to the entry global
map, `_R = 0`, and `CONT = .K`; their `<k>` terms compare byte-for-byte after
normalization. Reachability transitivity therefore gives a final result, rather
than leaving the entry theorem non-constraining.
