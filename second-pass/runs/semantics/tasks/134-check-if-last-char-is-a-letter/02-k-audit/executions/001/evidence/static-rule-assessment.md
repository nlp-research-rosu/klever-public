# Static rule assessment

The exact, line-located inventory is `rule-inventory.txt`. It covers 26 K source
files, 699 rules, 228 syntax declarations, 5 contexts, 1 configuration, and the
6 entry claims. Source hashes and exact declaration/rule blocks are included
there. This assessment assigns a disposition to every inventoried file and
spells out every proof-local extension.

## Disposition key

- **Active/faithful**: exercised by at least one target claim and consistent
  with the supplied semantics plus ordinary mathematics on its match domain.
- **Active/fidelity failure**: exercised by a target claim but not faithful to
  the submitted CPython program on the stated string domain; a witness is given.
- **Supplied/inactive**: part of the byte-identical trusted supplied baseline
  but unreachable from every target claim. It contributes no equation,
  narrowing, branch, state change, or result to these proofs.
- **Local/valid lemma**: proof-local and mathematically true throughout its
  unguarded domain.
- **Local/pinning gap**: a local term may execute faithfully as written, but no
  machine-checked connection pins it to the submitted program artifact.

## File-by-file decision

| File | Inventory | Decision for every rule/declaration in the file |
|---|---:|---|
| `reference-semantics/semantics.k` | 23 imports, 2 modules | Assembly only; byte-identical supplied baseline. `VERIFICATION` imports `MPY`, not concrete-only `MPY-CONCRETE`. |
| `semantics/syntax.k` | 16 syntax declarations | Supplied syntax. The submitted MPY uses `Module`, `FuncDef`, `Params`, `If`, `Compare`, `Call`, `Name`, `Int`, `Bool`, `UnaryOp`, `Attribute`, `Subscript`, `Return`, and `Str`; each has a declaration. Unused productions are supplied/inactive. Strictness/contexts establish the intended operand order for the used productions. |
| `semantics/core.k` | 46 rules, 37 syntax, 1 configuration | Active/faithful for literal evaluation, scope lookup, builtin scope, left-to-right argument evaluation, truthiness, `isLen`, and call state. The claims explicitly provide a realizable instance of the configuration. Heap/cell/list helpers not reached by this program are supplied/inactive. |
| `semantics/iter.k` | 1 syntax declaration | Supplied/inactive. |
| `semantics/range.k` | 6 rules, 2 syntax | Supplied/inactive. |
| `semantics/operators.k` | 10 rules, 2 contexts | Active/faithful for unary minus, unary `not`, and integer/string equality dispatch. Heap-reference paths and other comparison operators are supplied/inactive. |
| `semantics/int.k` | 16 rules, 1 syntax | Active/faithful for unary minus and integer equality. All other rules are supplied/inactive. |
| `semantics/bool.k` | 13 rules, 1 context | Active/faithful for unary `not`; the `BoolOp` rules are supplied/inactive. |
| `semantics/float.k` | 121 rules, 34 syntax | Entirely supplied/inactive. Its opaque proof-domain float primitives cannot influence any target branch or result. |
| `semantics/str.k` | 28 rules, 5 syntax | Active/faithful within the supplied ASCII code-sequence model for `Str(" ")`, concatenation, and string equality. The literal used by the program is ASCII. Other rules are supplied/inactive. |
| `semantics/set.k` | 12 rules, 6 syntax | Supplied/inactive. |
| `semantics/list.k` | 27 rules, 5 syntax | Supplied/inactive. |
| `semantics/tuple.k` | 21 rules, 4 syntax | Supplied/inactive. |
| `semantics/subscript.k` | 40 rules, 15 syntax, 2 contexts | Active/faithful for string indexing. `normIdx` converts `-1`/`-2`; every path reaching `intSeqAt` is in bounds because the prior length branches enforce length at least one/two. Slice/list/tuple rules are supplied/inactive. |
| `semantics/comprehension.k` | 7 rules, 3 syntax | Supplied/inactive. |
| `semantics/methods.k` | 75 rules, 27 syntax | **Active/fidelity failure** for `applyMethod(...,"isalpha",...)`, `allAlpha`, and `isAlphaC`: they recognize only ASCII A–Z/a–z. Witness: `C=233` makes K return `false` for `"é".isalpha()`, while CPython 3.10 returns `True`. `18a-unicode-formal-proof.log` proves the formal `false`; `15-claim-witnesses.log` records the CPython disagreement; `18b-unicode-opposite-proof.log` shows the theory rejects `true`. Other method rules are supplied/inactive. |
| `semantics/controls.k` | 34 rules, 3 syntax | Active/faithful for `If` and branch selection. Assignment, loops, imports, and loop control are supplied/inactive. |
| `semantics/functions.k` | 15 rules, 4 syntax | Active/faithful for parameter binding, `Return`, frame pop, and exact restoration of `env`, `scopes`, `scopeLoc`, `stack`, and `ret`. Annotated-closure rules are supplied/inactive. |
| `semantics/builtins.k` | 137 rules, 38 syntax | Active/faithful only for `len(str) -> isLen`; all folds, conversions, evaluator, digest, and other builtins are supplied/inactive. |
| `semantics/call.k` | 21 rules, 3 syntax | Active/faithful for callee evaluation, method dispatch, builtin dispatch, the ordinary closure call, frame creation, and argument evaluation. Other callable forms and heap dereferences are supplied/inactive. |
| `semantics/sort.k` | 19 rules, 6 syntax | Supplied/inactive. |
| `semantics/assert.k` | 3 rules | Supplied/inactive in every proof claim; used only by the separately run concrete smoke program. |
| `semantics/dict.k` | 28 rules, 12 syntax | Supplied/inactive. |
| `semantics/concrete.k` | 16 rules, 5 syntax | Not imported by the proof definition and therefore incapable of contributing to claim closure. It is used only by the fresh LLVM concrete run. |
| `verification.k` | 4 rules, 1 syntax | Individually assessed below. |
| `spec.k` | 6 claims | Individually restated and witnessed in the review. |

## Proof-local extensions

1. `#checkIfLastChar(Val)` and its sole rewrite at `verification.k:8-33`.
   This is an operational harness that calls a manually embedded closure under
   the ordinary supplied call semantics. The embedded body text matches the
   current `solution.mpy`, and the call preserves continuation and all
   observable cells through the ordinary frame rules. However, neither the rule
   nor the build reads `solution.mpy`; no bridge-free connection claim executes
   module loading/name selection. Classification: **Local/pinning gap**. A
   complete source-body replacement still rebuilds and proves `#Top`; see
   `16a`–`16d`.

2. `isLen(seqConcat(P, iCons(A, iCons(B,.)))) = isLen(P)+2` at
   `verification.k:39-41`. This follows by structural induction on `P`, has no
   guard, terminates through the supplied `seqConcat`/`isLen` equations, and has
   no disagreeing overlap. Classification: **Local/valid lemma**. It supports
   the three length-at-least-two claims.

3. `intSeqAt(seqConcat(P,[A,B]),isLen(P)) = A` at
   `verification.k:43-47`. Structural induction on `P` reduces both the
   concatenation and index by one; the base case is supplied `intSeqAt([A,B],0)`.
   Its index is always in bounds. Classification: **Local/valid lemma**.

4. `intSeqAt(seqConcat(P,[A,B]),isLen(P)+1) = B` at
   `verification.k:49-53`. The same induction ends at
   `intSeqAt([A,B],1)=B`; its index is in bounds. Classification:
   **Local/valid lemma**.

There are no local `[function]`, `[total]`, `[functional]`, priority, concrete,
or opaque declarations. The only local attributes are the three
`[simplification]` attributes above.

## Opaque and totalized supplied symbols

The only supplied functions with no local equation at all are
`md5hexCodes` and `sortKeyVS`. Proof-opaque/no-evaluator primitives also include
`sortVS` and the float symbols `intFloatDiv`, `divII`, `floatMod`, `floatLt`,
`absF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`,
`divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`, and `sqrtF`;
`floorFI`, `toF`, and `ceilF` are total symbolic functions with concrete-only
equations for their supported constructors. None occurs in `solution.mpy`,
`verification.k`, any entry precondition/postcondition, or any residual along
the six proofs. The build warnings for partial totality (`mapStrVS`, `floorFI`,
`toF`, `ceilF`, `joinCodes`, `valSeqAt`) therefore do not affect these claims.
