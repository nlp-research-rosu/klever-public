import Proof.Model
import Lean.Elab.Tactic.Omega

open Proof

set_option maxHeartbeats 10000000

private theorem intMeasureStep (candidate divisor : Int)
    (h : divisor < candidate) :
    (candidate - divisor).toNat =
      Nat.succ (candidate - (divisor + 1)).toNat := by
  omega

private theorem intMeasureDecreases (candidate divisor : Int)
    (h : divisor < candidate) :
    (candidate - (divisor + 1)).toNat <
      (candidate - divisor).toNat := by
  omega

theorem Proof.innerProofLayout
    (outerLayout : Bool) (candidate divisor : SortInt)
    (isPrime : SortBool) (n : SortInt)
    (builtins moduleVars : SortMap) (values : SortValSeq)
    (scopeLoc : SortScopeLocCell) (heapLoc : SortHeapLocCell)
    (stack : SortStackCell) (ret : SortRetCell) (exc : SortExcCell)
    (exitCode : SortExitCodeCell)
    (generatedCounter : SortGeneratedCounterCell) (rest : SortK)
    (lower : 2 ≤ divisor) (upper : divisor ≤ candidate) :
    Rewrites
      (machine (.kseq innerLoop rest)
        (loopLocals outerLayout candidate divisor isPrime n)
        builtins moduleVars values
        scopeLoc heapLoc stack ret exc exitCode generatedCounter)
      (machine rest
        (loopLocals outerLayout candidate candidate
          (_andBool_ isPrime (noDivisor candidate divisor candidate)) n)
        builtins moduleVars values scopeLoc heapLoc stack ret exc exitCode
        generatedCounter) := by
  unfold innerLoop innerCondition innerBody machine heapList
  apply Rewrites.tran Rewrites._0edcaa2
  apply Rewrites.tran (Rewrites._1f0e78f rfl rfl rfl rfl)
  apply Rewrites.tran
    (lookupInner outerLayout candidate divisor isPrime n
      builtins moduleVars values
      scopeLoc heapLoc stack ret exc exitCode generatedCounter
      "divisor" (.inj_SortInt divisor) _
      (by
        cases outerLayout <;>
          simp only [loopLocals, outerLocals, innerLocals, if_false, if_true,
            _Map_, «_|->_», «_in_keys(_)_MAP_Bool_KItem_Map»]
        all_goals unfold_kmap_models
        all_goals simp [inj, Inj.inj, instInjSortStringSortKItem])
      (by
        cases outerLayout <;>
          simp only [loopLocals, outerLocals, innerLocals, if_false, if_true,
            _Map_, «_|->_», «Map:lookup»]
        all_goals unfold_kmap_models
        all_goals simp [inj, Inj.inj, instInjSortStringSortKItem])
      (by rfl))
  apply Rewrites.tran
    (Rewrites._dfb9e43
      (HOLE := (@inj SortVal SortExpr) (.inj_SortInt divisor))
      (_Gen0 := .«CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» "<"
        (.«Name(_)_MPY-SYNTAX_Expr_String» "candidate"))
      rfl rfl rfl)
  apply Rewrites.tran
    (Rewrites._e1122bd
      (HOLE := .«Name(_)_MPY-SYNTAX_Expr_String» "candidate")
      (_Gen0 := .inj_SortInt divisor) (_Gen1 := "<")
      rfl rfl rfl rfl)
  apply Rewrites.tran
    (lookupInner outerLayout candidate divisor isPrime n
      builtins moduleVars values
      scopeLoc heapLoc stack ret exc exitCode generatedCounter
      "candidate" (.inj_SortInt candidate) _
      (by
        cases outerLayout <;>
          simp only [loopLocals, outerLocals, innerLocals, if_false, if_true,
            _Map_, «_|->_», «_in_keys(_)_MAP_Bool_KItem_Map»]
        all_goals unfold_kmap_models
        all_goals simp [inj, Inj.inj, instInjSortStringSortKItem])
      (by
        cases outerLayout <;>
          simp only [loopLocals, outerLocals, innerLocals, if_false, if_true,
            _Map_, «_|->_», «Map:lookup»]
        all_goals unfold_kmap_models
        all_goals simp [inj, Inj.inj, instInjSortStringSortKItem])
      (by rfl))
  apply Rewrites.tran
    (Rewrites._aae3b52
      (HOLE := (@inj SortVal SortExpr) (.inj_SortInt candidate))
      (_Gen0 := .inj_SortInt divisor) (_Gen1 := "<")
      rfl rfl rfl)
  apply Rewrites.tran
    (Rewrites._a00964a
      (LV := .inj_SortInt divisor) (RV := .inj_SortInt candidate)
      (OP := "<") (_Val0 := decide (divisor < candidate)) rfl)
  by_cases hd : divisor < candidate
  · rw [show decide (divisor < candidate) = true by simp [hd]]
    apply Rewrites.tran
      (Rewrites._0d9d338 (V := .inj_SortBool true) rfl rfl)
    kstep Rewrites._94bd14e
    kstep Rewrites.«MPY_SYNTAX_If(_,_,_)_MPY_SYNTAX_Stmt_Expr_Stmts_Stmts1_heat»
    kstep Rewrites._1f0e78f
    kstep Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr2_heat»
    apply Rewrites.tran
      (lookupInner outerLayout candidate divisor isPrime n
        builtins moduleVars values
        scopeLoc heapLoc stack ret exc exitCode generatedCounter
        "candidate" (.inj_SortInt candidate) _
        (by
          cases outerLayout <;>
            simp only [loopLocals, outerLocals, innerLocals, if_false, if_true,
              _Map_, «_|->_», «_in_keys(_)_MAP_Bool_KItem_Map»]
          all_goals unfold_kmap_models
          all_goals simp [inj, Inj.inj, instInjSortStringSortKItem])
        (by
          cases outerLayout <;>
            simp only [loopLocals, outerLocals, innerLocals, if_false, if_true,
              _Map_, «_|->_», «Map:lookup»]
          all_goals unfold_kmap_models
          all_goals simp [inj, Inj.inj, instInjSortStringSortKItem])
        (by rfl))
    apply Rewrites.tran
      (Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr2_cool»
        (HOLE := (@inj SortVal SortExpr) (.inj_SortInt candidate))
        (K0 := "%") (K2 := .«Name(_)_MPY-SYNTAX_Expr_String» "divisor")
        rfl rfl rfl)
    kstep Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr3_heat»
    apply Rewrites.tran
      (lookupInner outerLayout candidate divisor isPrime n
        builtins moduleVars values
        scopeLoc heapLoc stack ret exc exitCode generatedCounter
        "divisor" (.inj_SortInt divisor) _
        (by
          cases outerLayout <;>
            simp only [loopLocals, outerLocals, innerLocals, if_false, if_true,
              _Map_, «_|->_», «_in_keys(_)_MAP_Bool_KItem_Map»]
          all_goals unfold_kmap_models
          all_goals simp [inj, Inj.inj, instInjSortStringSortKItem])
        (by
          cases outerLayout <;>
            simp only [loopLocals, outerLocals, innerLocals, if_false, if_true,
              _Map_, «_|->_», «Map:lookup»]
          all_goals unfold_kmap_models
          all_goals simp [inj, Inj.inj, instInjSortStringSortKItem])
        (by rfl))
    apply Rewrites.tran
      (Rewrites.«MPY_SYNTAX_BinOp(_,_,_)_MPY_SYNTAX_Expr_String_Expr_Expr3_cool»
        (HOLE := (@inj SortVal SortExpr) (.inj_SortInt divisor))
        (K0 := "%")
        (K1 := (@inj SortVal SortExpr) (.inj_SortInt candidate))
        rfl rfl rfl)
    have hpos : 0 < divisor :=
      Int.lt_of_lt_of_le (by decide : (0 : Int) < 2) lower
    have hne : divisor ≠ 0 := Int.ne_of_gt hpos
    apply Rewrites.tran
      (Rewrites._d9b5bba
        (L := .inj_SortInt candidate) (R := .inj_SortInt divisor)
        (OP := "%") (_Val0 := .inj_SortInt (pyModTotal candidate divisor))
        (by
          simp [«applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val»,
            _13d6ee6, _1909c2e, _2acce51, _30456db, _3598da3,
            _42bfa12, _4f03d42, _4f373ea, _50f1b5a, _614d946,
            _798d463, _7f23ecf,
            «pyMod(_,_)_MPY-INT_Int_Int_Int», _2d78aae,
            «_%Int_», «_+Int_», pyModTotal, hne,
            inj, Inj.inj, instInjSortIntSortVal]))
    apply Rewrites.tran
      (Rewrites._dfb9e43
        (HOLE := (@inj SortVal SortExpr)
          (.inj_SortInt (pyModTotal candidate divisor)))
        (_Gen0 := .«CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr» "=="
          (.«Int(_)_MPY-SYNTAX_Expr_Int» 0))
        rfl rfl rfl)
    apply Rewrites.tran
      (Rewrites._e1122bd
        (HOLE := .«Int(_)_MPY-SYNTAX_Expr_Int» 0)
        (_Gen0 := .inj_SortInt (pyModTotal candidate divisor))
        (_Gen1 := "==") rfl rfl rfl rfl)
    kstep Rewrites._665cd53
    apply Rewrites.tran
      (Rewrites._aae3b52
        (HOLE := (@inj SortVal SortExpr) (.inj_SortInt 0))
        (_Gen0 := .inj_SortInt (pyModTotal candidate divisor))
        (_Gen1 := "==") rfl rfl rfl)
    apply Rewrites.tran
      (Rewrites._a00964a
        (LV := .inj_SortInt (pyModTotal candidate divisor))
        (RV := .inj_SortInt 0) (OP := "==")
        (_Val0 := decide (pyModTotal candidate divisor = 0)) rfl)
    apply Rewrites.tran
      (Rewrites.«MPY_SYNTAX_If(_,_,_)_MPY_SYNTAX_Stmt_Expr_Stmts_Stmts1_cool»
        (HOLE := (@inj SortVal SortExpr)
          (.inj_SortBool (decide (pyModTotal candidate divisor = 0))))
        rfl rfl rfl)
    kstep Rewrites._c82b7aa
    have nextUpper : divisor + 1 ≤ candidate :=
      Int.add_one_le_iff.mpr hd
    have measureStep :
        (candidate - divisor).toNat =
          Nat.succ (candidate - (divisor + 1)).toNat :=
      intMeasureStep candidate divisor hd
    by_cases hm : pyModTotal candidate divisor = 0
    · rw [show decide (pyModTotal candidate divisor = 0) = true by simp [hm]]
      kstep Rewrites._0fd4639
      kstep Rewrites._94bd14e
      apply Rewrites.tran
        (assignInnerBool outerLayout candidate divisor isPrime false n
          builtins moduleVars
          values scopeLoc heapLoc stack ret exc exitCode generatedCounter _)
      kstep Rewrites._2a0ddee
      kstep Rewrites._94bd14e
      apply Rewrites.tran
        (incrementInnerDivisor outerLayout candidate divisor false n
          builtins moduleVars
          values scopeLoc heapLoc stack ret exc exitCode generatedCounter _)
      kstep Rewrites._2a0ddee
      kstep Rewrites._d499ad9
      simpa [_andBool_, noDivisor, noDivisorSteps, measureStep, hm] using
        (innerProofLayout outerLayout candidate (divisor + 1) false n
          builtins moduleVars
          values scopeLoc heapLoc stack ret exc exitCode generatedCounter rest
          (Int.le_trans lower
            (Int.le_add_one (Int.le_refl divisor))) nextUpper)
    · rw [show decide (pyModTotal candidate divisor = 0) = false by simp [hm]]
      kstep Rewrites._052f78e
      kstep Rewrites._2a0ddee
      kstep Rewrites._94bd14e
      apply Rewrites.tran
        (incrementInnerDivisor outerLayout candidate divisor isPrime n
          builtins moduleVars
          values scopeLoc heapLoc stack ret exc exitCode generatedCounter _)
      kstep Rewrites._2a0ddee
      kstep Rewrites._d499ad9
      simpa [_andBool_, noDivisor, noDivisorSteps, measureStep, hm] using
        (innerProofLayout outerLayout candidate (divisor + 1) isPrime n
          builtins moduleVars
          values scopeLoc heapLoc stack ret exc exitCode generatedCounter rest
          (Int.le_trans lower
            (Int.le_add_one (Int.le_refl divisor))) nextUpper)
  · have done : divisor = candidate :=
      Int.le_antisymm upper (Int.le_of_not_gt hd)
    subst candidate
    rw [show decide (divisor < divisor) = false by simp]
    simpa [_andBool_, noDivisor, noDivisorSteps] using
      (Rewrites._b13ae76
        (V := .inj_SortBool false) (_B := innerBody)
        rfl rfl rfl)
termination_by (candidate - divisor).toNat
decreasing_by
  all_goals exact intMeasureDecreases candidate divisor hd

theorem Proof.innerProof
    (candidate divisor : SortInt) (isPrime : SortBool) (n : SortInt)
    (builtins moduleVars : SortMap) (values : SortValSeq)
    (scopeLoc : SortScopeLocCell) (heapLoc : SortHeapLocCell)
    (stack : SortStackCell) (ret : SortRetCell) (exc : SortExcCell)
    (exitCode : SortExitCodeCell)
    (generatedCounter : SortGeneratedCounterCell) (rest : SortK)
    (lower : 2 ≤ divisor) (upper : divisor ≤ candidate) :
    Rewrites
      (machine (.kseq innerLoop rest)
        (innerLocals candidate divisor isPrime n) builtins moduleVars values
        scopeLoc heapLoc stack ret exc exitCode generatedCounter)
      (machine rest
        (innerLocals candidate candidate
          (_andBool_ isPrime (noDivisor candidate divisor candidate)) n)
        builtins moduleVars values scopeLoc heapLoc stack ret exc exitCode
        generatedCounter) := by
  simpa [loopLocals] using
    (innerProofLayout false candidate divisor isPrime n builtins moduleVars
      values scopeLoc heapLoc stack ret exc exitCode generatedCounter rest
      lower upper)
