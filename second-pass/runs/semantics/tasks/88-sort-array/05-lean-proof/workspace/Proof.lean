import Klean88SortArray.Lemmas
import Lean.Elab.Tactic.Omega

namespace Proof

/- KORE symbol: LblsnocVS'LParUndsCommUndsRParUnds'VERIFICATION'Unds'ValSeq'Unds'ValSeq'Unds'Val; frozen source obligations: rule-ab4b49bc5cb4d2f873e2b399b9cb8d81a81689b74a6ddc22dfb813e2f897e479. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «snocVS(_,_)_VERIFICATION_ValSeq_ValSeq_Val» : SortValSeq → SortVal → SortValSeq
  | .«.ValSeq_MPY-CORE_ValSeq», value =>
      .«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» value .«.ValSeq_MPY-CORE_ValSeq»
  | .«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» head tail, value =>
      .«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
        head
        («snocVS(_,_)_VERIFICATION_ValSeq_ValSeq_Val» tail value)

def valSeqLength : SortValSeq → Nat
  | .«.ValSeq_MPY-CORE_ValSeq» => 0
  | .«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _ tail =>
      valSeqLength tail + 1

theorem valSeqLength_snoc (values : SortValSeq) (last : SortVal) :
    valSeqLength
        («snocVS(_,_)_VERIFICATION_ValSeq_ValSeq_Val» values last)
      = valSeqLength values + 1 := by
  cases values with
  | «.ValSeq_MPY-CORE_ValSeq» =>
      rfl
  | «vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» head tail =>
      simp [
        «snocVS(_,_)_VERIFICATION_ValSeq_ValSeq_Val»,
        valSeqLength, valSeqLength_snoc tail last]

theorem vsLen_eq_length (values : SortValSeq) :
    «vsLen(_)_MPY-CORE_Int_ValSeq» values =
      some (valSeqLength values : Int) := by
  cases values with
  | «.ValSeq_MPY-CORE_ValSeq» =>
      simp [
        «vsLen(_)_MPY-CORE_Int_ValSeq», _5d69a53, _b662ad7,
        valSeqLength, Option.orElse]
  | «vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» head tail =>
      simp [
        «vsLen(_)_MPY-CORE_Int_ValSeq», _5d69a53, _b662ad7,
        vsLen_eq_length tail, valSeqLength, «_+Int_»,
        Option.bind, Option.orElse, Int.add_comm]

theorem valSeqAt_empty (index : SortInt) :
    «valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int»
        SortValSeq.«.ValSeq_MPY-CORE_ValSeq» index
      = none := by
  rw [«valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int»]
  simp [_86fc1c7, _a66427b, Option.orElse]

theorem a664_cons_positive
    (value : SortVal) (tail : SortValSeq) (index : Nat) :
    _a66427b
        (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» value tail)
        ((index : Int) + 1)
      = none := by
  generalize index_eq : ((index : Int) + 1) = actual
  cases actual with
  | ofNat n =>
      cases n with
      | zero =>
          have positive : (0 : Int) < (index : Int) + 1 :=
            Int.add_pos_of_nonneg_of_pos (Int.natCast_nonneg index) (by decide)
          rw [index_eq] at positive
          simp at positive
      | succ n => rfl
  | negSucc n => rfl

theorem valSeqAt_snoc_length (values : SortValSeq) (last : SortVal) :
    «valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int»
        («snocVS(_,_)_VERIFICATION_ValSeq_ValSeq_Val» values last)
        (valSeqLength values : Int)
      = some last := by
  cases values with
  | «.ValSeq_MPY-CORE_ValSeq» =>
      rw [«valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int»]
      simp [
        «snocVS(_,_)_VERIFICATION_ValSeq_ValSeq_Val», valSeqLength,
        _86fc1c7, _a66427b, «_>Int_», «_-Int_»,
        guard, Option.orElse, valSeqAt_empty]
  | «vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» head tail =>
      rw [«valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int»]
      simp [
        «snocVS(_,_)_VERIFICATION_ValSeq_ValSeq_Val», valSeqLength,
        _86fc1c7, a664_cons_positive,
        «_>Int_», «_-Int_»,
        guard]
      have ih :
          «valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int»
              («snocVS(_,_)_VERIFICATION_ValSeq_ValSeq_Val» tail last)
              (valSeqLength tail : Int)
            = some last :=
        valSeqAt_snoc_length tail last
      exact ih

theorem valSeqAt_cons_snoc_last
    (first last : SortVal) (middle : SortValSeq) :
    «valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int»
        (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
          first
          («snocVS(_,_)_VERIFICATION_ValSeq_ValSeq_Val» middle last))
        ((valSeqLength middle : Int) + 1)
      = some last := by
  rw [«valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int»]
  simp [
    _86fc1c7, a664_cons_positive,
    «_>Int_», «_-Int_», guard]
  have hlast :
      «valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int»
          («snocVS(_,_)_VERIFICATION_ValSeq_ValSeq_Val» middle last)
          (valSeqLength middle : Int)
        = some last :=
    valSeqAt_snoc_length middle last
  rw [hlast]

theorem applyIndex_list_cons_snoc_last
    (first last : SortInt) (middle : SortValSeq) :
    «applyIndex(_,_)_MPY-SUBSCRIPT_Val_Val_Int»
        (SortVal.inj_SortIterable
          (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq»
            (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
              (SortVal.inj_SortInt first)
              («snocVS(_,_)_VERIFICATION_ValSeq_ValSeq_Val»
                middle (SortVal.inj_SortInt last)))))
        (-1)
      = some (SortVal.inj_SortInt last) := by
  simp [
    «applyIndex(_,_)_MPY-SUBSCRIPT_Val_Val_Int», _77afc7e, _ae682a5,
    _dff41b0, retr, vsLen_eq_length,
    «normIdx(_,_)_MPY-SUBSCRIPT_Int_Int_Int», _6e2ceae, _92d2fec,
    valSeqLength, valSeqLength_snoc,
    «_<Int_», «_>=Int_», «_+Int_»,
    guard, Option.orElse]
  have index_eq :
      (-1 : Int) + ((valSeqLength middle : Int) + 1 + 1) =
        (valSeqLength middle : Int) + 1 := by
    omega
  have hlast :=
    valSeqAt_cons_snoc_last
      (SortVal.inj_SortInt first)
      (SortVal.inj_SortInt last)
      middle
  rw [index_eq]
  exact hlast

theorem final :
    Klean88SortArray.Lemmas.targetStatement «snocVS(_,_)_VERIFICATION_ValSeq_ValSeq_Val» := by
  unfold Klean88SortArray.Lemmas.targetStatement
  intro _Gen9 _Gen8 _Gen7 _Gen6 _Gen5 _Gen4 _Gen3 _Gen2 _Gen1 _Gen0
    _DotVar1 KleanDef0 _F L _M h
  cases h
  let object : SortVal :=
    SortVal.inj_SortIterable
      (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq»
        (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
          (SortVal.inj_SortInt _F)
          («snocVS(_,_)_VERIFICATION_ValSeq_ValSeq_Val»
            _M (SortVal.inj_SortInt L))))
  let oneExpr : SortExpr := SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» 1
  let negExpr : SortExpr :=
    SortExpr.«UnaryOp(_,_)_MPY-SYNTAX_Expr_String_Expr» "-" oneExpr
  apply Rewrites.tran
  · exact Rewrites._06d3a17
      (HOLE := negExpr)
      (_Gen0 := object)
      (_Val0 := false) (_Val1 := true) (_Val2 := true)
      (by
        simp [
          negExpr, isKResult, _f4c2469, _afefecb, inj, retr,
          Option.orElse])
      (by simp [notBool_, _17ebc68, _53fc758, Option.orElse])
      (by simp [_andBool_, _5b9db8d, _61fbef3, Option.orElse])
      rfl
  · apply Rewrites.tran
    · exact Rewrites.«MPY_SYNTAX_UnaryOp(_,_)_MPY_SYNTAX_Expr_String_Expr2_heat»
        (HOLE := oneExpr) (K0 := "-")
        (_Val0 := false) (_Val1 := true) (_Val2 := true)
        (by
          simp [
            oneExpr, isKResult, _f4c2469, _afefecb, inj, retr,
            Option.orElse])
        (by simp [notBool_, _17ebc68, _53fc758, Option.orElse])
        (by simp [_andBool_, _5b9db8d, _61fbef3, Option.orElse])
        rfl
    · apply Rewrites.tran
      · exact Rewrites._665cd53 (I := 1)
      · apply Rewrites.tran
        · exact
            Rewrites.«MPY_SYNTAX_UnaryOp(_,_)_MPY_SYNTAX_Expr_String_Expr2_cool»
              (HOLE := SortExpr.inj_SortInt 1) (K0 := "-")
              (_Val0 := true) (_Val1 := true)
              (by
                simp [
                  isKResult, _f4c2469, _afefecb, inj, retr,
                  Option.orElse])
              (by simp [_andBool_, _5b9db8d, _61fbef3, Option.orElse])
              rfl
        · apply Rewrites.tran
          · exact Rewrites._4aae5e8
              (OP := "-")
              (V := SortVal.inj_SortInt 1)
              (_Val0 := SortVal.inj_SortInt (-1))
              (by
                simp [
                  «applyUn(_,_)_MPY-CORE_Val_String_Val», _30ee06e,
                  _69b3bda, _b48e091, «_-Int_», inj,
                  Option.bind, Option.orElse]
                change SortVal.inj_SortInt (-1) = SortVal.inj_SortInt (-1)
                rfl)
          · apply Rewrites.tran
            · exact Rewrites._6105b33
                (HOLE := SortExpr.inj_SortInt (-1))
                (_Gen0 := object)
                (_Val0 := true) (_Val1 := true)
                (by
                  simp [
                    isKResult, _f4c2469, _afefecb, inj, retr,
                    Option.orElse])
                (by simp [_andBool_, _5b9db8d, _61fbef3, Option.orElse])
                rfl
            · exact Rewrites._f3fd256
                (I := -1)
                (OBJ := object)
                (_Val0 := SortVal.inj_SortInt L)
                (by
                  simpa [object] using
                    applyIndex_list_cons_snoc_last _F L _M)

end Proof
