import Proof.Inner
import Lean.Elab.Tactic.Omega

open Proof

set_option maxHeartbeats 10000000

private theorem outerMeasureStep (upper start : Int) (h : start < upper) :
    (upper - start).toNat =
      Nat.succ (upper - (start + 1)).toNat := by
  omega

private theorem outerMeasureDecreases (upper start : Int)
    (h : start < upper) :
    (upper - (start + 1)).toNat < (upper - start).toNat := by
  omega

theorem Proof.outerProof
    (start upper : SortInt) (builtins moduleVars : SortMap)
    (values : SortValSeq) (scopeLoc : SortScopeLocCell)
    (heapLoc : SortHeapLocCell) (stack : SortStackCell)
    (ret : SortRetCell) (exc : SortExcCell)
    (exitCode : SortExitCodeCell)
    (generatedCounter : SortGeneratedCounterCell) (rest : SortK)
    (lower : 2 ≤ start) (bound : start ≤ upper) :
    Rewrites
      (machine (.kseq outerLoop rest)
        (outerLocals upper start true 2) builtins moduleVars values
        scopeLoc heapLoc stack ret exc exitCode generatedCounter)
      (machine rest
        (outerLocals upper upper true 2) builtins moduleVars
        (primesAcc values start upper)
        scopeLoc heapLoc stack ret exc exitCode generatedCounter) := by
  unfold outerLoop outerCondition outerBody innerWhileStatement
  apply Rewrites.tran Rewrites._0edcaa2
  apply Rewrites.tran (Rewrites._1f0e78f rfl rfl rfl rfl)
  apply Rewrites.tran
    (lookupInner true start 2 true upper builtins moduleVars values
      scopeLoc heapLoc stack ret exc exitCode generatedCounter
      "candidate" (.inj_SortInt start) _
      (by
        simp only [loopLocals, outerLocals, if_true, Proof._Map_,
          Proof.«_|->_»,
          «_in_keys(_)_MAP_Bool_KItem_Map»]
        unfold_kmap_models
        simp [inj, Inj.inj, instInjSortStringSortKItem])
      (by
        simp only [loopLocals, outerLocals, if_true, Proof._Map_,
          Proof.«_|->_»,
          «Map:lookup»]
        unfold_kmap_models
        simp [inj, Inj.inj, instInjSortStringSortKItem])
      (by rfl))
  apply Rewrites.tran
    (Rewrites._dfb9e43
      (HOLE := (@inj SortVal SortExpr) (.inj_SortInt start))
      (_Gen0 := .«CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» "<"
        (.«Name(_)_MPY-SYNTAX_Expr_String» "n"))
      rfl rfl rfl)
  apply Rewrites.tran
    (Rewrites._e1122bd
      (HOLE := .«Name(_)_MPY-SYNTAX_Expr_String» "n")
      (_Gen0 := .inj_SortInt start) (_Gen1 := "<")
      rfl rfl rfl rfl)
  apply Rewrites.tran
    (lookupInner true start 2 true upper builtins moduleVars values
      scopeLoc heapLoc stack ret exc exitCode generatedCounter
      "n" (.inj_SortInt upper) _
      (by
        simp only [loopLocals, outerLocals, if_true, Proof._Map_,
          Proof.«_|->_»,
          «_in_keys(_)_MAP_Bool_KItem_Map»]
        unfold_kmap_models
        simp [inj, Inj.inj, instInjSortStringSortKItem])
      (by
        simp only [loopLocals, outerLocals, if_true, Proof._Map_,
          Proof.«_|->_»,
          «Map:lookup»]
        unfold_kmap_models
        simp [inj, Inj.inj, instInjSortStringSortKItem])
      (by rfl))
  apply Rewrites.tran
    (Rewrites._aae3b52
      (HOLE := (@inj SortVal SortExpr) (.inj_SortInt upper))
      (_Gen0 := .inj_SortInt start) (_Gen1 := "<")
      rfl rfl rfl)
  apply Rewrites.tran
    (Rewrites._a00964a
      (LV := .inj_SortInt start) (RV := .inj_SortInt upper)
      (OP := "<") (_Val0 := decide (start < upper)) rfl)
  by_cases hlt : start < upper
  · rw [show decide (start < upper) = true by simp [hlt]]
    have nextBound : start + 1 ≤ upper := Int.add_one_le_iff.mpr hlt
    have measureStep :
        (upper - start).toNat =
          Nat.succ (upper - (start + 1)).toNat :=
      outerMeasureStep upper start hlt
    apply Rewrites.tran
      (Rewrites._0d9d338 (V := .inj_SortBool true) rfl rfl)
    kstep Rewrites._94bd14e
    kstep Rewrites._ba16b53
    apply Rewrites.tran
      (innerProofLayout true start 2 true upper builtins moduleVars values
        scopeLoc heapLoc stack ret exc exitCode generatedCounter _
        (by decide) (by omega))
    simp only [Proof._andBool_, true_and]
    unfold outerTail
    kstep Rewrites._94bd14e
    kstep Rewrites.«MPY_SYNTAX_If(_,_,_)_MPY_SYNTAX_Stmt_Expr_Stmts_Stmts1_heat»
    apply Rewrites.tran
      (lookupInner true start start (noDivisor start 2 start) upper
        builtins moduleVars values scopeLoc heapLoc stack ret exc exitCode
        generatedCounter "is_prime"
        (.inj_SortBool (noDivisor start 2 start)) _
        (by
          simp only [loopLocals, outerLocals, if_true, Proof._Map_,
            Proof.«_|->_», «_in_keys(_)_MAP_Bool_KItem_Map»]
          unfold_kmap_models
          simp [inj, Inj.inj, instInjSortStringSortKItem])
        (by
          simp only [loopLocals, outerLocals, if_true, Proof._Map_,
            Proof.«_|->_», «Map:lookup»]
          unfold_kmap_models
          simp [inj, Inj.inj, instInjSortStringSortKItem])
        (by rfl))
    apply Rewrites.tran
      (Rewrites.«MPY_SYNTAX_If(_,_,_)_MPY_SYNTAX_Stmt_Expr_Stmts_Stmts1_cool»
        (HOLE := (@inj SortVal SortExpr)
          (.inj_SortBool (noDivisor start 2 start)))
        rfl rfl rfl)
    kstep Rewrites._c82b7aa
    cases hp : Proof.noDivisor start 2 start
    · kstep Rewrites._052f78e
      kstep Rewrites._2a0ddee
      kstep Rewrites._94bd14e
      apply Rewrites.tran
        (incrementOuterCandidate upper start false start builtins moduleVars
          values scopeLoc heapLoc stack ret exc exitCode generatedCounter _)
      kstep Rewrites._94bd14e
      apply Rewrites.tran
        (assignInnerBool true (start + 1) start false true upper
          builtins moduleVars values scopeLoc heapLoc stack ret exc exitCode
          generatedCounter _)
      kstep Rewrites._94bd14e
      apply Rewrites.tran
        (assignOuterDivisor upper (start + 1) true start 2
          builtins moduleVars values scopeLoc heapLoc stack ret exc exitCode
          generatedCounter _)
      kstep Rewrites._2a0ddee
      kstep Rewrites._d499ad9
      simpa [Proof.primesAcc, primesAccSteps, measureStep, hp] using
        (outerProof (start + 1) upper builtins moduleVars values
          scopeLoc heapLoc stack ret exc exitCode generatedCounter rest
          (Int.le_trans lower
            (Int.le_add_one (Int.le_refl start))) nextBound)
    · kstep Rewrites._0fd4639
      kstep Rewrites._94bd14e
      kstep Rewrites.«MPY_SYNTAX_Expr(_)_MPY_SYNTAX_Stmt_Expr1_heat»
      kstep Rewrites._2d73ccf
      kstep Rewrites.«MPY_SYNTAX_Attribute(_,_)_MPY_SYNTAX_Expr_Expr_String1_heat»
      apply Rewrites.tran
        (lookupInner true start start true upper builtins moduleVars values
          scopeLoc heapLoc stack ret exc exitCode generatedCounter
          "result" (.«ref(_)_MPY-CORE_Val_Int» 0) _
          (by
            simp only [loopLocals, outerLocals, if_true, Proof._Map_,
              Proof.«_|->_», «_in_keys(_)_MAP_Bool_KItem_Map»]
            unfold_kmap_models
            simp [inj, Inj.inj, instInjSortStringSortKItem])
          (by
            simp only [loopLocals, outerLocals, if_true, Proof._Map_,
              Proof.«_|->_», «Map:lookup»]
            unfold_kmap_models
            simp [inj, Inj.inj, instInjSortStringSortKItem])
          (by rfl))
      apply Rewrites.tran
        (Rewrites.«MPY_SYNTAX_Attribute(_,_)_MPY_SYNTAX_Expr_Expr_String1_cool»
          (HOLE := (@inj SortVal SortExpr)
            (.«ref(_)_MPY-CORE_Val_Int» 0))
          (K1 := "append") rfl rfl rfl)
      kstep Rewrites._c03debd
      kstep Rewrites._0619f01
      kstep Rewrites._f0c4941
      apply Rewrites.tran
        (lookupInner true start start true upper builtins moduleVars values
          scopeLoc heapLoc stack ret exc exitCode generatedCounter
          "candidate" (.inj_SortInt start) _
          (by
            simp only [loopLocals, outerLocals, if_true, Proof._Map_,
              Proof.«_|->_», «_in_keys(_)_MAP_Bool_KItem_Map»]
            unfold_kmap_models
            simp [inj, Inj.inj, instInjSortStringSortKItem])
          (by
            simp only [loopLocals, outerLocals, if_true, Proof._Map_,
              Proof.«_|->_», «Map:lookup»]
            unfold_kmap_models
            simp [inj, Inj.inj, instInjSortStringSortKItem])
          (by rfl))
      apply Rewrites.tran
        (Rewrites._c75b3bb
          (_Val0 := .«_,__MPY-CORE_Vals_Val_Vals»
            (.inj_SortInt start)
            .«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals»)
          (by
            simp [«appendVal(_,_)_MPY-CORE_Vals_Vals_Val»,
              _1dc0c6c, _b10f912]))
      kstep Rewrites._4f8838c
      apply Rewrites.tran
        (Rewrites._5e18747
          (H := 0) (V := .inj_SortInt start) (VS := values)
          (_Val2 := valSeqAppendInt values start)
          (_Val0 := heapList values) (_Val1 := heapList values)
          (_Val3 := heapList (valSeqAppendInt values start))
          (_Val4 := heapList (valSeqAppendInt values start))
          (_DotVar2 := { coll := [] })
          (by
            simp [heapList, Proof.«_|->_», _root_.«_|->_», inj, Inj.inj,
              instInjSortIntSortKItem, instInjSortIterableSortKItem])
          (by
            simp only [heapList, Proof.«_|->_», _root_._Map_,
              _root_.«_|->_»]
            unfold_kmap_models
            simp [inj, Inj.inj, instInjSortIntSortKItem,
              instInjSortIterableSortKItem])
          (valSeqConcatSingleton values start)
          (by
            simp [heapList, Proof.«_|->_», _root_.«_|->_», inj, Inj.inj,
              instInjSortIntSortKItem, instInjSortIterableSortKItem])
          (by
            simp only [heapList, Proof.«_|->_», _root_._Map_,
              _root_.«_|->_»]
            unfold_kmap_models
            simp [inj, Inj.inj, instInjSortIntSortKItem,
              instInjSortIterableSortKItem]))
      apply Rewrites.tran
        (Rewrites.«MPY_SYNTAX_Expr(_)_MPY_SYNTAX_Stmt_Expr1_cool»
          (HOLE := (@inj SortVal SortExpr) .«noneV_MPY-CORE_Val»)
          rfl rfl rfl)
      kstep Rewrites._eaf4781
      kstep Rewrites._2a0ddee
      kstep Rewrites._94bd14e
      apply Rewrites.tran
        (incrementOuterCandidate upper start true start builtins moduleVars
          (valSeqAppendInt values start) scopeLoc heapLoc stack ret exc
          exitCode generatedCounter _)
      kstep Rewrites._94bd14e
      apply Rewrites.tran
        (assignInnerBool true (start + 1) start true true upper
          builtins moduleVars (valSeqAppendInt values start)
          scopeLoc heapLoc stack ret exc exitCode generatedCounter _)
      kstep Rewrites._94bd14e
      apply Rewrites.tran
        (assignOuterDivisor upper (start + 1) true start 2
          builtins moduleVars (valSeqAppendInt values start)
          scopeLoc heapLoc stack ret exc exitCode generatedCounter _)
      kstep Rewrites._2a0ddee
      kstep Rewrites._d499ad9
      simpa [Proof.primesAcc, primesAccSteps, measureStep, hp] using
        (outerProof (start + 1) upper builtins moduleVars
          (valSeqAppendInt values start)
          scopeLoc heapLoc stack ret exc exitCode generatedCounter rest
          (Int.le_trans lower
            (Int.le_add_one (Int.le_refl start))) nextBound)
  · have done : start = upper :=
      Int.le_antisymm bound (Int.le_of_not_gt hlt)
    subst upper
    rw [show decide (start < start) = false by simp]
    simpa [Proof.primesAcc, primesAccSteps, outerBody, loopLocals,
      machine, heapList] using
      (Rewrites._b13ae76
        (V := .inj_SortBool false) (_B := outerBody)
        rfl rfl rfl)
termination_by (upper - start).toNat
decreasing_by
  all_goals exact outerMeasureDecreases upper start hlt
