import Klean106F.Lemmas
import Init.Omega

namespace Proof

/- KORE symbol: Lbl'Unds'andBool'Unds'; frozen source obligations: rule-cd588e1b203a59d4324edead96d5948bf0c1c5b2173430eda0466e8f903d55f7, rule-fb668e722ce1e9413ff23f2c2ed84482db6011cd49f97844b2747538201651ac. Replace this stub with its honest total meaning from the frozen K semantics. -/
def _andBool_ (left right : SortBool) : SortBool := left && right
/- KORE symbol: Lbl'Unds-LT-Eqls'Int'Unds'; frozen source obligations: rule-ab7cbb359dda1a6c9c1a14fe5b45df7a4f54c5eced049f1d2c5066c92c667ec7, rule-5aa051dcb3d8aa1545bc998933e91b5adea53c25b6565ff7e8213e15b8ba1b66, rule-cd588e1b203a59d4324edead96d5948bf0c1c5b2173430eda0466e8f903d55f7, rule-fb668e722ce1e9413ff23f2c2ed84482db6011cd49f97844b2747538201651ac. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_<=Int_» (left right : SortInt) : SortBool := decide (left ≤ right)
/- KORE symbol: Lbl'UndsEqlsEqls'Int'Unds'; frozen source obligations: rule-cd588e1b203a59d4324edead96d5948bf0c1c5b2173430eda0466e8f903d55f7. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_==Int_» (left right : SortInt) : SortBool := decide (left = right)
/- KORE symbol: Lbl'UndsEqlsSlshEqls'Int'Unds'; frozen source obligations: rule-fb668e722ce1e9413ff23f2c2ed84482db6011cd49f97844b2747538201651ac. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_=/=Int_» (left right : SortInt) : SortBool := decide (left ≠ right)
/- KORE symbol: Lbl'UndsPlus'Int'Unds'; frozen source obligations: rule-ab7cbb359dda1a6c9c1a14fe5b45df7a4f54c5eced049f1d2c5066c92c667ec7, rule-5aa051dcb3d8aa1545bc998933e91b5adea53c25b6565ff7e8213e15b8ba1b66, rule-cd588e1b203a59d4324edead96d5948bf0c1c5b2173430eda0466e8f903d55f7, rule-fb668e722ce1e9413ff23f2c2ed84482db6011cd49f97844b2747538201651ac. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_+Int_» (left right : SortInt) : SortInt := left + right
/- KORE symbol: Lbl'UndsStar'Int'Unds'; frozen source obligations: rule-ab7cbb359dda1a6c9c1a14fe5b45df7a4f54c5eced049f1d2c5066c92c667ec7, rule-cd588e1b203a59d4324edead96d5948bf0c1c5b2173430eda0466e8f903d55f7, rule-fb668e722ce1e9413ff23f2c2ed84482db6011cd49f97844b2747538201651ac. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_*Int_» (left right : SortInt) : SortInt := left * right
/- KORE symbol: LblfactRun'LParUndsCommUndsCommUndsRParUnds'VERIFICATION'Unds'Int'Unds'Int'Unds'Int'Unds'Int; frozen source obligations: rule-ab7cbb359dda1a6c9c1a14fe5b45df7a4f54c5eced049f1d2c5066c92c667ec7. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «factRun(_,_,_)_VERIFICATION_Int_Int_Int_Int»
    (I N F : SortInt) : SortInt :=
  if _hI : I ≤ N then
    «factRun(_,_,_)_VERIFICATION_Int_Int_Int_Int» (I + 1) N (F * I)
  else
    F
termination_by (N - I + 1).toNat
decreasing_by
  have hpositive : 0 < N - I + 1 :=
    Int.add_pos_of_nonneg_of_pos (Int.sub_nonneg_of_le _hI) (by decide)
  apply (Int.toNat_lt_toNat hpositive).2
  omega
/- KORE symbol: LblpyMod'LParUndsCommUndsRParUnds'MPY-INT'Unds'Int'Unds'Int'Unds'Int; frozen source obligations: rule-cd588e1b203a59d4324edead96d5948bf0c1c5b2173430eda0466e8f903d55f7, rule-fb668e722ce1e9413ff23f2c2ed84482db6011cd49f97844b2747538201651ac. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «pyMod(_,_)_MPY-INT_Int_Int_Int» (value modulus : SortInt) : SortInt :=
  Int.tmod (Int.tmod value modulus + modulus) modulus

private def valSeqConcatModel : SortValSeq → SortValSeq → SortValSeq
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», right => right
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» value rest, right =>
      SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» value
        (valSeqConcatModel rest right)

/- KORE symbol: LblresultRun'LParUndsCommUndsCommUndsCommUndsCommUndsRParUnds'VERIFICATION'Unds'ValSeq'Unds'ValSeq'Unds'Int'Unds'Int'Unds'Int'Unds'Int; frozen source obligations: rule-cd588e1b203a59d4324edead96d5948bf0c1c5b2173430eda0466e8f903d55f7, rule-fb668e722ce1e9413ff23f2c2ed84482db6011cd49f97844b2747538201651ac. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «resultRun(_,_,_,_,_)_VERIFICATION_ValSeq_ValSeq_Int_Int_Int_Int»
    (VS : SortValSeq) (I N F T : SortInt) : SortValSeq :=
  if _hI : I ≤ N then
    if «pyMod(_,_)_MPY-INT_Int_Int_Int» I 2 = 0 then
      «resultRun(_,_,_,_,_)_VERIFICATION_ValSeq_ValSeq_Int_Int_Int_Int»
        (valSeqConcatModel VS
          (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
            (SortVal.inj_SortInt (F * I))
            SortValSeq.«.ValSeq_MPY-CORE_ValSeq»))
        (I + 1) N (F * I) (T + I)
    else
      «resultRun(_,_,_,_,_)_VERIFICATION_ValSeq_ValSeq_Int_Int_Int_Int»
        (valSeqConcatModel VS
          (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
            (SortVal.inj_SortInt (T + I))
            SortValSeq.«.ValSeq_MPY-CORE_ValSeq»))
        (I + 1) N (F * I) (T + I)
  else
    VS
termination_by (N - I + 1).toNat
decreasing_by
  all_goals
    have hpositive : 0 < N - I + 1 :=
      Int.add_pos_of_nonneg_of_pos (Int.sub_nonneg_of_le _hI) (by decide)
    apply (Int.toNat_lt_toNat hpositive).2
    omega
/- KORE symbol: LbltotalRun'LParUndsCommUndsCommUndsRParUnds'VERIFICATION'Unds'Int'Unds'Int'Unds'Int'Unds'Int; frozen source obligations: rule-5aa051dcb3d8aa1545bc998933e91b5adea53c25b6565ff7e8213e15b8ba1b66. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «totalRun(_,_,_)_VERIFICATION_Int_Int_Int_Int»
    (I N T : SortInt) : SortInt :=
  if _hI : I ≤ N then
    «totalRun(_,_,_)_VERIFICATION_Int_Int_Int_Int» (I + 1) N (T + I)
  else
    T
termination_by (N - I + 1).toNat
decreasing_by
  have hpositive : 0 < N - I + 1 :=
    Int.add_pos_of_nonneg_of_pos (Int.sub_nonneg_of_le _hI) (by decide)
  apply (Int.toNat_lt_toNat hpositive).2
  omega
/- KORE symbol: LblvalSeqConcat'LParUndsCommUndsRParUnds'MPY-LIST'Unds'ValSeq'Unds'ValSeq'Unds'ValSeq; frozen source obligations: rule-cd588e1b203a59d4324edead96d5948bf0c1c5b2173430eda0466e8f903d55f7, rule-fb668e722ce1e9413ff23f2c2ed84482db6011cd49f97844b2747538201651ac. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»
    (left right : SortValSeq) : SortValSeq :=
  valSeqConcatModel left right

theorem final :
    Klean106F.Lemmas.targetStatement _andBool_ «_<=Int_» «_==Int_» «_=/=Int_» «_+Int_» «_*Int_» «factRun(_,_,_)_VERIFICATION_Int_Int_Int_Int» «pyMod(_,_)_MPY-INT_Int_Int_Int» «resultRun(_,_,_,_,_)_VERIFICATION_ValSeq_ValSeq_Int_Int_Int_Int» «totalRun(_,_,_)_VERIFICATION_Int_Int_Int_Int» «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» := by
  constructor
  · intro I F N h
    have hle : I ≤ N := by
      simpa [«_<=Int_»] using h
    symm
    rw [«factRun(_,_,_)_VERIFICATION_Int_Int_Int_Int».eq_1]
    simp [hle, «_+Int_», «_*Int_»]
  constructor
  · intro I T N h
    have hle : I ≤ N := by
      simpa [«_<=Int_»] using h
    symm
    rw [«totalRun(_,_,_)_VERIFICATION_Int_Int_Int_Int».eq_1]
    simp [hle, «_+Int_»]
  constructor
  · intro I T F N VS h
    have conditions :
        I ≤ N ∧ «pyMod(_,_)_MPY-INT_Int_Int_Int» I 2 = 0 := by
      simpa [_andBool_, «_<=Int_», «_==Int_»] using h
    symm
    rw [«resultRun(_,_,_,_,_)_VERIFICATION_ValSeq_ValSeq_Int_Int_Int_Int».eq_1]
    simp [conditions.1, conditions.2,
      «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq», «_+Int_», «_*Int_»]
  · intro I T F N VS h
    have conditions :
        I ≤ N ∧ «pyMod(_,_)_MPY-INT_Int_Int_Int» I 2 ≠ 0 := by
      simpa [_andBool_, «_<=Int_», «_=/=Int_»] using h
    symm
    rw [«resultRun(_,_,_,_,_)_VERIFICATION_ValSeq_ValSeq_Int_Int_Int_Int».eq_1]
    simp [conditions.1, conditions.2,
      «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq», «_+Int_», «_*Int_»]

end Proof
