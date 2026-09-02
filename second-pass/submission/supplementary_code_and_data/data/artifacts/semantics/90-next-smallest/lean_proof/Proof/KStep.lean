import Lean
import Klean90NextSmallest.Rewrite

open Lean Meta Elab Tactic

private def generatedPrivateMapName (suffix : String) : TacticM Name := do
  for (name, _) in (← getEnv).constants do
    if name.toString.endsWith suffix then
      return name
  throwError "generated private map definition ending in '{suffix}' was not found"

/-- Unfold the generated file-private map models in the current goal. -/
elab "kunfold_maps" : tactic => do
  let disjoint ← generatedPrivateMapName ".kleanMapDisjointModel"
  let contains ← generatedPrivateMapName ".kleanMapContainsModel"
  try
    replaceMainGoal [← Meta.unfoldTarget (← getMainGoal) disjoint]
  catch _ =>
    pure ()
  try
    replaceMainGoal [← Meta.unfoldTarget (← getMainGoal) contains]
  catch _ =>
    pure ()

/-- Unfold one layer of the generated file-private map membership model. -/
elab "kunfold_contains" : tactic => do
  let contains ← generatedPrivateMapName ".kleanMapContainsModel"
  try
    replaceMainGoal [← Meta.unfoldTarget (← getMainGoal) contains]
  catch _ =>
    pure ()

/-- Unfold one layer of the generated file-private map deletion model. -/
elab "kunfold_delete" : tactic => do
  let delete ← generatedPrivateMapName ".kleanMapDeleteModel"
  try
    replaceMainGoal [← Meta.unfoldTarget (← getMainGoal) delete]
  catch _ =>
    pure ()

elab "kunfold_delete" "at" hypothesis:ident : tactic => do
  let delete ← generatedPrivateMapName ".kleanMapDeleteModel"
  let goal ← getMainGoal
  let fvar ← getFVarId hypothesis
  replaceMainGoal [← Meta.unfoldLocalDecl goal fvar delete]

/--
Normalize generated lookup, update, deletion, membership, and disjointness
models on the small explicit maps used by the frozen function frame.
-/
elab "kunfold_concrete_maps" : tactic => do
  let lookup ← generatedPrivateMapName ".kleanMapLookupModel"
  let update ← generatedPrivateMapName ".kleanMapUpdateModel"
  let delete ← generatedPrivateMapName ".kleanMapDeleteModel"
  let contains ← generatedPrivateMapName ".kleanMapContainsModel"
  let disjoint ← generatedPrivateMapName ".kleanMapDisjointModel"
  for _ in [:64] do
    for name in [lookup, update, delete, contains, disjoint] do
      try
        replaceMainGoal [← Meta.unfoldTarget (← getMainGoal) name]
      catch _ =>
        pure ()

private partial def seedGeneratedInjections
    (pattern actual : Expr) : MetaM Unit := do
  let pattern ← instantiateMVars pattern
  let actual ← instantiateMVars actual
  let patternFn := pattern.getAppFn
  if patternFn.isConstOf ``inj then
    let patternArgs := pattern.getAppArgs
    let actualArgs := actual.getAppArgs
    if patternArgs.size ≥ 1 && actualArgs.size ≥ 1 then
      let payloadPattern := patternArgs.back!
      let payloadActual := actualArgs.back!
      if payloadPattern.isMVar then
        let payloadPatternType ← inferType payloadPattern
        let payloadActualType ← inferType payloadActual
        if ← isDefEq payloadPatternType payloadActualType then
          payloadPattern.mvarId!.assign payloadActual
        else
          let payloadPatternType ← whnf payloadPatternType
          if let .const targetSort _ := payloadPatternType then
            if let .const actualConstructor _ := actual.getAppFn then
              let suffixes ←
                if actualConstructor == ``inj then
                  match payloadActualType with
                  | .const sourceSort _ =>
                      let source := sourceSort.getString!
                      if source.startsWith "Sort" then
                        pure [s!"inj_{source}"]
                      else
                        pure [s!"inj_{source}", s!"inj_Sort{source}"]
                  | _ => pure []
                else
                  pure [actualConstructor.getString!]
              for suffix in suffixes do
                let liftedConstructor := Name.str targetSort suffix
                if (← getEnv).contains liftedConstructor then
                  let lifted ← mkAppM liftedConstructor #[payloadActual]
                  payloadPattern.mvarId!.assign lifted
                else if targetSort == ``SortExpr then
                  let valConstructor := Name.str ``SortVal suffix
                  let exprConstructor := Name.str ``SortExpr "inj_SortVal"
                  if (← getEnv).contains valConstructor &&
                      (← getEnv).contains exprConstructor then
                    let value ← mkAppM valConstructor #[payloadActual]
                    let expression ← mkAppM exprConstructor #[value]
                    payloadPattern.mvarId!.assign expression
      else
        seedGeneratedInjections payloadPattern payloadActual
  else if patternFn == actual.getAppFn then
    let patternArgs := pattern.getAppArgs
    let actualArgs := actual.getAppArgs
    if patternArgs.size = actualArgs.size then
      for index in [:patternArgs.size] do
        seedGeneratedInjections patternArgs[index]! actualArgs[index]!

/--
Apply one generated K rewrite rule and leave the remaining transitive rewrite
as the sole goal. Rule side conditions are discharged by definitional
reduction, simplification, arithmetic, and hypotheses in the current branch.
-/
elab "kstep" : tactic => do
  let goals ← getGoals
  let goal ← getMainGoal
  let restGoals := goals.tail
  let target ← whnf (← goal.getType)
  let targetArgs := target.getAppArgs
  unless targetArgs.size = 2 do
    throwError "kstep: expected a binary Rewrites goal"
  let source := targetArgs[0]!
  let destination := targetArgs[1]!
  let stateType ← inferType source
  let intermediate ← mkFreshExprMVar stateType MetavarKind.natural
  let firstStep ← mkFreshExprMVar
    (mkAppN (mkConst ``Rewrites) #[source, intermediate])
    MetavarKind.syntheticOpaque
  let continuation ← mkFreshExprMVar
    (mkAppN (mkConst ``Rewrites) #[intermediate, destination])
    MetavarKind.syntheticOpaque
  goal.assign <| mkAppN (mkConst ``Rewrites.tran)
    #[source, intermediate, destination, firstStep, continuation]
  let saved ← saveState
  let ruleGoal := firstStep.mvarId!
  let continuationGoal := continuation.mvarId!
  let some (.inductInfo rewriteInfo) := (← getEnv).find? ``Rewrites
    | throwError "kstep: Rewrites is not an inductive declaration"
  let ruleConstructors := rewriteInfo.ctors.drop 1
  for constructorName in ruleConstructors do
    saved.restore
    try
      let constructor := mkConst constructorName
      let constructorType ← inferType constructor
      let (constructorMVars, _, constructorConclusion) ←
        forallMetaTelescopeReducing constructorType
      let ruleTarget ← ruleGoal.getType
      let conclusionArgs := constructorConclusion.getAppArgs
      let targetArgs := ruleTarget.getAppArgs
      if conclusionArgs.size = 2 && targetArgs.size = 2 then
        seedGeneratedInjections conclusionArgs[0]! targetArgs[0]!
      let constructorApp := mkAppN constructor constructorMVars
      let premiseGoals ← ruleGoal.apply constructorApp
      let mut propositionGoals := []
      let mut dataGoals := []
      for premise in premiseGoals do
        if ← isProp (← premise.getType) then
          propositionGoals := propositionGoals ++ [premise]
        else
          dataGoals := dataGoals ++ [premise]
      setGoals (propositionGoals ++ dataGoals)
      evalTactic (← `(tactic|
        all_goals
          first
          | assumption
          | rfl
          | (try simp
             try kunfold_concrete_maps
             try simp
             try grind)))
      let remainingPremises ← (← getGoals).filterM fun premise =>
        not <$> premise.isAssigned
      if remainingPremises.isEmpty then
        setGoals (continuationGoal :: restGoals)
        return
    catch _ =>
      pure ()
  saved.restore
  let target ← instantiateMVars (← ruleGoal.getType)
  throwError "kstep: no generated operational rule closed the next step from\n{target}"

/--
Finish the evaluation of an integer comparison after its left operand has
been looked up.  These are the five ordinary MPY heating, literal, cooling,
and comparison rules generated from the frozen semantics.
-/
syntax "finish_int_compare" "(" term ", " term ", " term ", " term ")" :
  tactic

macro_rules
  | `(tactic| finish_int_compare ($left, $right, $operator, $result)) =>
      `(tactic|
        refine Rewrites.tran
          (Rewrites._dfb9e43
            (HOLE := SortExpr.inj_SortInt $left)
            (_Val0 := true) (_Val1 := true)
            (by rfl) (by rfl) rfl) ?_;
        refine Rewrites.tran
          (Rewrites._e1122bd
            (HOLE := SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» $right)
            (_Gen0 := SortVal.inj_SortInt $left) (_Gen1 := $operator)
            (_Val0 := false) (_Val1 := true) (_Val2 := true)
            (by rfl) (by rfl) (by rfl) rfl) ?_;
        refine Rewrites.tran Rewrites._665cd53 ?_;
        refine Rewrites.tran
          (Rewrites._aae3b52
            (HOLE := SortExpr.inj_SortInt $right)
            (_Gen0 := SortVal.inj_SortInt $left) (_Gen1 := $operator)
            (_Val0 := true) (_Val1 := true)
            (by rfl) (by rfl) rfl) ?_;
        refine Rewrites.tran
          (Rewrites._a00964a
            (LV := SortVal.inj_SortInt $left)
            (RV := SortVal.inj_SortInt $right) (OP := $operator)
            (_Val0 := $result) (by rfl)) ?_)

syntax "finish_if_true" : tactic
macro_rules
  | `(tactic| finish_if_true) =>
      `(tactic|
        refine Rewrites.tran
          (Rewrites.«MPY_SYNTAX_If(_,_,_)_MPY_SYNTAX_Stmt_Expr_Stmts_Stmts1_cool»
            (HOLE := SortExpr.inj_SortBool true)
            (_Val0 := true) (_Val1 := true)
            (by rfl) (by rfl) rfl) ?_;
        refine Rewrites.tran
          (Rewrites._c82b7aa
            (C := SortVal.inj_SortBool true) (_Val0 := true)
            (by rfl)) ?_;
        refine Rewrites.tran Rewrites._0fd4639 ?_)

syntax "finish_if_false" : tactic
macro_rules
  | `(tactic| finish_if_false) =>
      `(tactic|
        refine Rewrites.tran
          (Rewrites.«MPY_SYNTAX_If(_,_,_)_MPY_SYNTAX_Stmt_Expr_Stmts_Stmts1_cool»
            (HOLE := SortExpr.inj_SortBool false)
            (_Val0 := true) (_Val1 := true)
            (by rfl) (by rfl) rfl) ?_;
        refine Rewrites.tran
          (Rewrites._c82b7aa
            (C := SortVal.inj_SortBool false) (_Val0 := false)
            (by rfl)) ?_;
        refine Rewrites.tran Rewrites._052f78e ?_)

syntax "heat_assign_name" "(" term ", " term ")" : tactic
macro_rules
  | `(tactic| heat_assign_name ($target, $source)) =>
      `(tactic|
        refine Rewrites.tran
          (Rewrites.«MPY_SYNTAX_Assign(_,_)_MPY_SYNTAX_Stmt_Expr_Expr2_heat»
            (HOLE := SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» $source)
            (K0 := SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» $target)
            (_Val0 := false) (_Val1 := true) (_Val2 := true)
            (by rfl) (by rfl) (by rfl) rfl) ?_;
        refine Rewrites.tran Rewrites._6d39855 ?_)

syntax "cool_assign_int" "(" term ", " term ")" : tactic
macro_rules
  | `(tactic| cool_assign_int ($target, $value)) =>
      `(tactic|
        refine Rewrites.tran
          (Rewrites.«MPY_SYNTAX_Assign(_,_)_MPY_SYNTAX_Stmt_Expr_Expr2_cool»
            (HOLE := SortExpr.inj_SortInt $value)
            (K0 := SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» $target)
            (_Val0 := true) (_Val1 := true)
            (by rfl) (by rfl) rfl) ?_)

syntax "eval_assign_literal" "(" term ", " term ")" : tactic
macro_rules
  | `(tactic| eval_assign_literal ($target, $value)) =>
      `(tactic|
        refine Rewrites.tran
          (Rewrites.«MPY_SYNTAX_Assign(_,_)_MPY_SYNTAX_Stmt_Expr_Expr2_heat»
            (HOLE := SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» $value)
            (K0 := SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» $target)
            (_Val0 := false) (_Val1 := true) (_Val2 := true)
            (by rfl) (by rfl) (by rfl) rfl) ?_;
        refine Rewrites.tran Rewrites._665cd53 ?_;
        cool_assign_int ($target, $value))

syntax "heat_compare_name" "(" term ", " term ", " term ")" : tactic
macro_rules
  | `(tactic| heat_compare_name ($left, $operator, $name)) =>
      `(tactic|
        refine Rewrites.tran
          (Rewrites._dfb9e43
            (HOLE := SortExpr.inj_SortInt $left)
            (_Val0 := true) (_Val1 := true)
            (by rfl) (by rfl) rfl) ?_;
        refine Rewrites.tran
          (Rewrites._e1122bd
            (HOLE := SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» $name)
            (_Gen0 := SortVal.inj_SortInt $left) (_Gen1 := $operator)
            (_Val0 := false) (_Val1 := true) (_Val2 := true)
            (by rfl) (by rfl) (by rfl) rfl) ?_;
        refine Rewrites.tran Rewrites._6d39855 ?_)

syntax "cool_compare_int" "(" term ", " term ", " term ", " term ")" :
  tactic
macro_rules
  | `(tactic| cool_compare_int ($left, $right, $operator, $result)) =>
      `(tactic|
        refine Rewrites.tran
          (Rewrites._aae3b52
            (HOLE := SortExpr.inj_SortInt $right)
            (_Gen0 := SortVal.inj_SortInt $left) (_Gen1 := $operator)
            (_Val0 := true) (_Val1 := true)
            (by rfl) (by rfl) rfl) ?_;
        refine Rewrites.tran
          (Rewrites._a00964a
            (LV := SortVal.inj_SortInt $left)
            (RV := SortVal.inj_SortInt $right) (OP := $operator)
            (_Val0 := $result) (by rfl)) ?_)
