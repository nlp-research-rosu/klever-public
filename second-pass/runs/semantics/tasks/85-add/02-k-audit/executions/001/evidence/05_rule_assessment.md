# Static rule assessment

This assessment is keyed to the exhaustive source-level inventory in
`05_rule_inventory.md`.

## Selected supplied-semantics level

The complete candidate `reference-semantics/` tree is recursively identical to
the trusted supplied tree. Under `SUPPLIED_SEMANTICS`, its 658 ordinary rules,
48 priority rules, 123 non-opaque function declarations, 25 symbol/opaque
declarations, 85 other syntax declarations, five contexts, and one
configuration are therefore the selected fixed semantic level, not
candidate-authored proof lemmas. Every item is enumerated with its complete
guard/cells/attributes in `05_rule_inventory.md`. No local source rule has a
`simplification` or `simplifier` attribute.

The used semantic slice is integer-only and does not reach any of the 25
opaque/symbol declarations (the float family, `sortVS`, `sortKeyVS`, or
`md5hexCodes`). The LLVM compiler reported narrower totality gaps for
`mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, and `valSeqAt`. None is
reachable from this program or either formal claim, so this audit does not call
those declarations unsound; the warnings are recorded as unused fixed-semantics
coverage limitations.

## Candidate-local declarations and rules

Every candidate-local declaration/rule in `verification.k` is assessed here.

1. `verification.k:9`, `intVals(IntSeq)`: a new constructor encoding a finite
   integer sequence as a `ValSeq`. It is not fresh or opaque; the argument is
   structurally constrained by `.IntSeq`/`iCons(Int,IntSeq)`.
2. `verification.k:11-15`, the two priority-40 iterator rules: definitional
   input-encoding rules. They cover both `IntSeq` constructors, are disjoint,
   yield exactly the head integer, recurse on the tail, and touch only `<k>`.
   They do not overlap the fixed list iterator rules, whose arguments require
   `.ValSeq` or `vCons`.
3. `verification.k:17-18`, total function `scopeMap`: truthful projection from
   the sole `Scope` constructor `scope(Map,Parent)`. It is exhaustive and unused
   by both claims.
4. `verification.k:20-29`, function `addAccSpec` and four equations:
   structural recursion over `IntSeq`; the false-flag branch skips one element
   and toggles true; the true-flag branches add exactly an even head and toggle
   false. The modulo guards `== 0` and `=/= 0` are complementary, all recursion
   descends to the tail, and the base returns the accumulator. It is
   result-bearing but fully defined rather than opaque.
5. `verification.k:31-39`, macro `addLoopBody`: an exact expansion of the two
   statements in the submitted loop. It changes no semantics.
6. `verification.k:41-48`, macro `addFunctionBody`: an exact expansion of the
   submitted function body, including the docstring expression and all
   initializations.
7. `verification.k:50-52`, macro `solutionModule`: an exact expansion of the
   submitted module/function. Expanded `kast` output is byte-identical to the
   expanded parse of submitted `solution.mpy`; see `04_program_pinning.log`.
8. `verification.k:57-75`, priority-30 loop-summary rule: an operational
   bridge. It reads `<k>`, `<env>`, and `<scopes>`, requires the exact
   function-entry local bindings and exact `Return(total) .Stmts ~> #endcall`
   suffix, then replaces loop execution with `Return(addAccSpec(...))`. It
   omits `<stack>`, `<ret>`, `<scopeLoc>`, `<heap>`, and all other cells from
   its match. Thus it accepts configurations beyond a valid active call frame
   while skipping changes to `total`, `odd_index`, and `value`.

Items 1-7 are sound definitions/macros on their complete domains. Item 8 is
not sound on its complete match domain. The bridge-free loop theorem closes
(`05_kprove_loop_no_bridge.log`), so the arithmetic summary itself is not an
oracle. The defect is control/state-context containment.

Concrete false-conclusion witness: `05_bridge-domain-witness.k` uses intended
input `[4,2]`, the exact local bindings and continuation accepted by item 8,
`<ret> noRet`, but `<stack> .List`. Under the candidate extension, the claim
that the bridge immediately reaches `Return(2) ~> #endcall` while retaining
initial locals closes with `#Top` (`05_bridge_domain_extended.log`). Under the
same definition with item 8 removed, fixed execution adds 2, leaves
`total=2`, `value=2`, sets `retV(2)`, and sticks at `#pop` because no frame
exists; it cannot reach the bridge target (`05_bridge_domain_fixed.log`).
This is a machine-checked false reachability conclusion enabled by the rule on
a non-empty list of integers, not merely an undocumented proof gap.

## Syntax-to-rule map for submitted `solution.mpy`

- `Module` and statement sequencing: `syntax.k:61`, `core.k:124-127`.
- `FuncDef`, `Params`, call frame, parameter binding, return/pop:
  `syntax.k:53,57`, `functions.k:14-16,63-90`,
  `call.k:19-21,69-75`.
- `Expr(Str(...))`: `syntax.k:13,52`, `str.k:13-17`,
  `controls.k:46-48`.
- `Assign(Name(...), ...)`: `syntax.k:12,41`,
  `core.k:130-154`, `controls.k:8-18`.
- `Int` and `Bool` literals: `syntax.k:9,11`, `core.k:193-196`.
- `For`: `syntax.k:45`, `controls.k:62-74`, with the two candidate
  `intVals` iterator rules above and simple-name target binding in
  `tuple.k:31-41`.
- `If`: `syntax.k:49`, `controls.k:50-54`, and `truthy` in
  `core.k:198-205`.
- `BinOp("%",...)`, `Compare(...,"==",...)`: `syntax.k:15,30-32`,
  contexts/dispatch in `operators.k:10-17`, and integer cases
  `int.k:15,19-20,26`.
- `AugAssign("+",...)`: `syntax.k:44`, `controls.k:20-31`, and integer
  addition `int.k:9`.
- `UnaryOp("not",...)`: `syntax.k:14`, `operators.k:10`, `bool.k:8`.
- `Return`: `syntax.k:50`, `functions.k:77-90`.
- The entry-only `Call` and `#loadAll`: `syntax.k:28`,
  `core.k:123-127,183-191`, `call.k:18-21,69-75`.

This slice preserves left-to-right evaluation through strictness/seqstrict and
the shared argument evaluator. The only allocation rules are for program list
constructors; the formal input is a read-only bare `list(intVals(INPUT))`, so
the verified path leaves heap and heap location unchanged. The divisor is the
constant 2, so no arithmetic exception path is admitted. Function local
updates occur in the allocated callee scope, and fixed return restores the
caller environment, deletes that scope, resets `scopeLoc`, and pops the frame.
