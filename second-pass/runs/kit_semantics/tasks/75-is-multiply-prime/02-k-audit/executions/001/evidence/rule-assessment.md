# Static rule assessment

This assessment covers the byte-identical supplied semantics copied into the
scratch tree, `verification.k`, and `spec.k`. The complete item-by-item source
inventory is `k-rule-inventory.md`; `classified-k-inventory.tsv` assigns one
disposition to every one of its 929 items.

## Disposition meanings

- `ON_PATH_SOUND` (60 items): a declaration, generated evaluation mechanism,
  context, or rule used by the submitted program. Each item agrees with the
  constructor program, Python evaluation order, and the modeled state changes.
- `TARGET_CLAIM_RESULT_CONSTRAINING` (1 item): the single target claim. Its
  destination is the explicit 22-way Boolean, not a fresh or unconstrained
  value.
- `OPAQUE_UNUSED_NO_DEPENDENCY` (25 items): a declared `symbol`/opaque proof
  boundary. None is syntactically reachable from the submitted program or
  appears in its claim/postcondition.
- `CONCRETE_ONLY_NOT_IN_PROOF` (56 items): an item in `MPY-CONCRETE` or bearing
  `[concrete]`. The Haskell definition imports `MPY`, not `MPY-CONCRETE`; these
  items do not contribute to proof closure.
- `OFF_PATH_REVIEWED_NO_TASK_WITNESS` (787 items): a declaration/rule for an
  unused source construct. Guards, priority, recursion, and modeled state were
  reviewed. Some deliberately model only a stated valid-input subset or leave
  unsupported behavior stuck. Because the submitted program cannot construct
  their left-hand sides, none can enable a false conclusion for any `A < 100`.

There are 227 syntax declarations, one configuration, five contexts, 695
rules, and one claim. Attributes comprise 145 function, 107 total, 45
priority, 26 owise, 35 concrete, 25 symbol, 22 no-evaluators, four macro, one
macro-rec, two strict, and one seqstrict occurrences. There are no local
`functional`, `simplification`, or `anywhere` declarations/rules.

## Per-module decision

| Module | Inventory | Task-path role | Decision |
|---|---:|---|---|
| `semantics.k` | assembler only | `VERIFICATION` imports `MPY`; LLVM uses `MPY-KRUN` | Import graph is explicit; proof excludes `MPY-CONCRETE`. |
| `syntax.k` | 16 syntax | Declares `Module`, `FuncDef`, `Params`, `Return`, `BoolOp`, `Compare`, `Name`, `Int`, `Call`, and lists; `[strict]` evaluates `Return`'s expression | Constructor sorts and strictness match the translated AST. Unused alternatives only broaden syntax. |
| `core.k` | 37 syntax, 1 configuration, 46 rules | Initial cells; module sequencing; local lookup; argument evaluation; integer literals; Boolean truthiness; `applyCmp`; argument accumulation | On-path rules preserve all ten cells. Lookup guards are disjoint. Argument evaluation is left-to-right. Structural helper recursion descends. |
| `functions.k` | 4 syntax, 15 rules | Binds the function, binds `a`, records return, pops frame | Callee scope allocation/deallocation, environment restoration, stack cleanup, and returned value agree with the real call. Cell-closure branches are guard-disjoint and absent here. |
| `call.k` | 3 syntax, 21 rules | Generic call routing and ordinary `closureVal` call | Callee is evaluated before arguments; arguments are left-to-right; the closure binding and body execute. `[owise]` does not preempt any applicable target-specific rule. |
| `operators.k` | 2 contexts, 10 rules | Evaluates both comparison operands and dispatches equality | Context order is left then right. Heap dereference priority rules cannot match integer operands. |
| `bool.k` | 1 context, 13 rules | Evaluates the `or` chain one head at a time | `truthy(true)` returns early and `truthy(false)` advances. Guards are complements. The final singleton returns its Boolean. Ref-only priority rules cannot match. |
| `int.k` | 1 syntax, 16 rules | `applyCmp("==", Int, Int)` | Equality is exactly K integer equality; no overlapping integer equality rule has a different result. |
| `assert.k` | 3 rules | none | Assertion termination/error rules are outside both entry claim and positive proof path. |
| `builtins.k` | 38 syntax, 137 rules | none | No builtin name is called. `md5hexCodes` is opaque but unused. Partial valid-input models and folds cannot affect the theorem. |
| `comprehension.k` | 3 syntax, 7 rules | none | Macros are unused; expansions are ordinary closure/list/loop constructors. |
| `concrete.k` | 5 syntax, 16 rules | LLVM-only | Not imported by the Haskell proof. The concrete driver does not use deep equality or keyed sorting. |
| `controls.k` | 3 syntax, 34 rules | none | No assignment, conditional, import, or loop appears in the program. State-changing rules therefore cannot match. |
| `dict.k` | 12 syntax, 28 rules | none | Dict operations and their deliberately limited error behavior are unreachable. |
| `float.k` | 34 syntax, 121 rules | none | All float constructors/operations are unreachable. Its 19 no-evaluator symbols plus three other proof-opaque declared symbols have no dependency edge to the claim. |
| `iter.k` | 1 syntax | none | Iterator protocol declaration only; no iterator term is built. |
| `list.k` | 5 syntax, 27 rules | none | No list constructor, heap ref, membership, or mutator occurs. |
| `methods.k` | 27 syntax, 75 rules | none | No `Attribute` or method call occurs. |
| `range.k` | 2 syntax, 6 rules | none | No range object or range builtin occurs. |
| `set.k` | 6 syntax, 12 rules | none | No set term occurs. |
| `sort.k` | 6 syntax, 19 rules | none | `sortVS` and `sortKeyVS` are result-bearing opaque boundaries in other tasks, but neither symbol, wrapper rule, nor builtin appears here. |
| `str.k` | 5 syntax, 28 rules | none | No string term or comparison occurs. |
| `subscript.k` | 15 syntax, 2 contexts, 40 rules | none | Total/underspecified out-of-bounds access is a semantics limitation for other programs, not a dependency of this theorem. |
| `tuple.k` | 4 syntax, 21 rules | none | No tuple, unpacking, or target-binding term occurs. |
| `verification.k` | 0 local items | imports fixed `MPY` only | No proof-local function, totality assertion, opaque term, priority, equation, semantic rewrite, simplification, bridge, lemma, or auxiliary claim exists. |
| `spec.k` | 1 claim | sole target theorem | The entry configuration loads the exact submitted constructor term and calls its binding with symbolic integer `A`; the destination is a fixed Boolean formula and all state cells are constrained. |

## Exact reachable execution

1. `#loadAll` exposes the one-element module statement list; statement
   sequencing executes `FuncDef` and binds the exact body at module scope `0`.
2. Generic `Call` evaluates `Name("is_multiply_prime")` by in-frame lookup,
   then evaluates the already-valued integer argument `A` and invokes that
   `closureVal`.
3. The closure rule allocates scope `1`, pushes a frame, binds parameter `a`,
   and executes the actual `Return(BoolOp(...))` body.
4. `Return` strictness, the `BoolOp` head context, the two `Compare` contexts,
   direct lookup of `a`, integer literal evaluation, and integer equality
   execute each comparison left-to-right with Python short-circuit `or`.
5. `Return` records the Boolean; `#pop` deletes the callee scope, restores
   environment `0` and `scopeLoc` `1`, empties the stack/return state, and
   places the Boolean in `<k>`. No heap, exception, exit-code, allocation, or
   output effect occurs.

The on-path rules have no opaque result, task-answer rewrite, external oracle,
unmodeled used construct, or operational bridge. The 22 constants occur in the
submitted program and in the result specification; no semantic rule contains
them. The full classified TSV provides a decision for every inventory row.
