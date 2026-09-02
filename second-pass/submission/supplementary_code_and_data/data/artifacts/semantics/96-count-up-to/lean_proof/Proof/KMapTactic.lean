import Klean96CountUpTo.Lemmas
import Lean.Elab.Tactic.Unfold
import Lean.Meta.Tactic.Refl

open Lean Elab Tactic

private def generatedPrivateName (tail : String) : Name :=
  Name.str (Name.num `_private.Klean96CountUpTo.Func 0) tail

/-- Unfold the executable association-list helpers hidden by the generated
Klean module's `private` namespace.  This only exposes their existing bodies;
it does not add any equation or logical assumption. -/
elab "unfold_kmap_models" : tactic => do
  for _ in [0:16] do
    for tail in #[
        "kleanMapLookupModel",
        "kleanMapContainsModel",
        "kleanMapDisjointModel",
        "kleanMapDeleteModel",
        "kleanMapUpdateModel"] do
      try
        unfoldTarget (generatedPrivateName tail)
      catch _ =>
        pure ()

/-- Compose one named generated rewrite constructor with the current
reachability goal. Explicit constructor premises become ordinary subgoals,
followed by the residual reachability goal. -/
elab "kstep " ctorId:ident : tactic => do
  let ctorName ← resolveGlobalConstNoOverload ctorId
  let goal ← getMainGoal
  let transGoals ← goal.apply (mkConst ``Rewrites.tran)
  match transGoals with
  | first :: continuation :: middle :: [] =>
      let premises ← first.apply
        (cfg := { newGoals := .nonDependentOnly })
        (mkConst ctorName)
      let mut goals := []
      for candidate in middle :: premises ++ [continuation] do
        unless ← candidate.isAssigned do
          try
            candidate.refl
          catch _ =>
            goals := goals ++ [candidate]
      replaceMainGoal goals
  | _ =>
      throwError "unexpected subgoal shape while composing a rewrite: {transGoals.length}"

/-- Close a reachability goal with one named generated rewrite constructor. -/
elab "kfinish " ctorId:ident : tactic => do
  let ctorName ← resolveGlobalConstNoOverload ctorId
  let goal ← getMainGoal
  replaceMainGoal (← goal.apply (mkConst ctorName))
