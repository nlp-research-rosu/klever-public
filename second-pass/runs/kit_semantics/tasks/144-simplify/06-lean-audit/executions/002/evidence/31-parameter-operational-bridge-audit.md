# Independent target-parameter operational audit

Inputs compared: immutable `generator-manifest.json` parameter records; the two
frozen rules `rule-ab9ad07a78277db66d0daa17d1890ca498e7cfba285dcb571a8014e3726d1543`
(digit bridge) and
`rule-c37d3f4e07aa03cba6c5454c87da6676a49c0ee9f8f31c9f2f047d68206cb650`
(slash bridge); `verification.k`; `solution.py`; the supplied MPython semantics;
and the exact candidate definitions in `Proof.lean`. The full manifest bindings
and candidate source are preserved in evidence 18, 19, 20, and 24.

The frozen solution scans `x ++ "/" ++ n`, increments `part` at slash code 47,
accumulates decimal digits into `a,b,c,d`, and returns
`(a*c) % (b*d) == 0`. Both bridge rules require the precise loop body, return,
callee scope, builtins scope, phase bounds, and `validScan`; the digit rule also
requires `isDigitC`.

| # | Target name / bound KORE symbol | Candidate location | Independent comparison |
|---|---|---|---|
| 1 | `«.List»` / `Lbl'Stop'List` | `Proof.lean:6` | `⟨[]⟩` is the empty generated list and matches the post-bridge empty stack in both rules. |
| 2 | `«.Map»` / `Lbl'Stop'Map` | `Proof.lean:8` | `⟨[]⟩` is the empty generated map and matches the empty heap and empty root-scope map in both rules. |
| 3 | `_Map_` / `Lbl'Unds'Map'Unds'` | `Proof.lean:10-11` | List append is associative with the stated unit and builds the fixed, disjoint-key maps in the same order as the frozen rules. It is not a faithful total model of hooked `MAP.concat` on unrestricted maps: raw order remains observable and duplicate-key validity is unchecked. Evidence 30 gives opposite first keys after swapping two singleton maps. |
| 4 | `_andBool_` / `Lbl'Unds'andBool'Unds'` | `Proof.lean:13` | Lean `&&` matches strict K Boolean conjunction used by every guard. Boundary mutations to constant true/false would respectively erase or make guards vacuous. |
| 5 | `«_<Int_»` / `Lbl'Unds-LT-'Int'Unds'` | `Proof.lean:15` | Decided mathematical integer `<` matches the slash rule's `P <Int 3`. |
| 6 | `«_<=Int_»` / `Lbl'Unds-LT-Eqls'Int'Unds'` | `Proof.lean:17` | Decided mathematical integer `≤` matches `0 <=Int P` and the digit bound `P <=Int 3`. |
| 7 | `«_==K_»` / `Lbl'UndsEqlsEqls'K'Unds'` | `Proof.lean:19-20` | Decided structural equality matches equality of the generated K syntax values used for loop-body, return, and scope guards, subject to the raw-map representation limitation in parameter 3. |
| 8 | `«_|->_»` / `Lbl'UndsPipe'-'-GT-Unds'` | `Proof.lean:22` | A singleton pair matches the map-element hook for the distinct keys appearing in the two configurations and in `simplifyScope`. |
| 9 | `ListItem` / `LblListItem` | `Proof.lean:24` | A singleton generated list matches the one-frame pre-state stack. |
| 10 | `«builtinsScope_MPY-CORE_Scope»` / `LblbuiltinsScope'Unds'MPY-CORE'Unds'Scope` | `Proof.lean:26-42` | The 20 builtin bindings and three type bindings, their names/values, and root parent exactly match `semantics/core.k:158-181`. |
| 11 | `«isDigitC(_)_MPY-METHODS_Bool_Int»` / `LblisDigitC'LParUndsRParUnds'MPY-METHODS'Unds'Bool'Unds'Int` | `Proof.lean:44-45` | Exactly `48 ≤ code ≤ 57`. Evidence 30 returns false/true/true/false for 47/48/57/58. |
| 12 | `scanResult` / its recorded `LblscanResult...VERIFICATION-SYNTAX...` symbol | `Proof.lean:47-76` | The six guarded frozen recurrence cases are reproduced: slash advances phases 0-2; digits update the selected accumulator; terminal phase 3 computes Python-style nonnegative modulo. The candidate totalizes states where the K function is undefined as false (and divisor zero as zero); `validScan` and the bridge guards exclude those states. Evidence 30 produces true for `1/5 * 5/1` and false for `1/6 * 2/1`. |
| 13 | `simplifyLoopBody` / `LblsimplifyLoopBody'Unds'VERIFICATION-SYNTAX'Unds'Stmts` | `Proof.lean:78-80` | The referenced generated option is definitionally `some` of the exact frozen nested slash/digit assignment AST (`Func.lean:_e59711f`); therefore the `getD` fallback is unreachable. It matches `solution.py` and `verification.k`. |
| 14 | `simplifyReturn` / `LblsimplifyReturn'Unds'VERIFICATION-SYNTAX'Unds'Stmt` | `Proof.lean:82-85` | The referenced generated option is definitionally `some` of the exact `(a*c) % (b*d) == 0` return AST (`Func.lean:_5af5fc9`); the fallback is unreachable. |
| 15 | `simplifyScope` / its recorded `LblsimplifyScope...VERIFICATION-SYNTAX...` symbol | `Proof.lean:87-112` | It binds exactly `x,n,part,a,b,c,d,ch` to the supplied values and uses `parent(0)`, matching the frozen definition and both bridge guards. Evidence 30 reports eight entries. It inherits parameter 3's unrestricted raw-map limitation. |
| 16 | `validScan` / its recorded `LblvalidScan...VERIFICATION-SYNTAX...` symbol | `Proof.lean:114-145` | It reproduces the four empty/phase cases, four recursive digit/slash cases, and the frozen owise-false behavior. The positive-fraction source precondition is exactly its accepting terminal condition. Evidence 30 accepts the code sequence for `1/5/5/1`. |

## Adversarial and counterfactual result

The decisive operational-bridge failure is independent of whether the mostly
faithful source-specific definitions above are used. `Proof.final` is:

```lean
exact Empty.elim (SetHookDef.choiceAx Empty [])
```

Evidence 28 checks three counterfactuals with Lean itself:

1. the same term proves `False`;
2. it proves the false arithmetic statement `(0 : Nat) = 1`; and
3. it proves the exact immutable `targetStatement` while all sixteen target
   parameters are arbitrary binders.

Consequently a constant, identity, hard-coded, or otherwise mutated definition
for any parameter leaves the proof valid. Neither generated rewrite obligation
is proved and no operational definition participates in the proof. This fails
the non-vacuity and operational-bridge gate.
