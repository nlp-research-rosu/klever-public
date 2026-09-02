import Klean40TriplesSumToZero.Lemmas
import Lean.Elab.Tactic.Omega

namespace Proof

/- KORE symbol: Lbl'Unds'andBool'Unds'; frozen source obligations: rule-02406fd68a82c2913a2b54042cfc3145ed95db3409554a09fc0a8d1b6cf799f4. Replace this stub with its honest total meaning from the frozen K semantics. -/
def _andBool_ (left right : SortBool) : SortBool :=
  left && right

/- KORE symbol: Lbl'Unds-LT-'Int'Unds'; frozen source obligations: rule-02406fd68a82c2913a2b54042cfc3145ed95db3409554a09fc0a8d1b6cf799f4. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_<Int_» (left right : SortInt) : SortBool :=
  decide (left < right)

/- KORE symbol: Lbl'Unds-LT-Eqls'Int'Unds'; frozen source obligations: rule-02406fd68a82c2913a2b54042cfc3145ed95db3409554a09fc0a8d1b6cf799f4. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_<=Int_» (left right : SortInt) : SortBool :=
  decide (left ≤ right)

/- KORE symbol: LblintAt'LParUndsCommUndsRParUnds'VERIFICATION'Unds'Int'Unds'IntSeq'Unds'Int; frozen source obligations: rule-02406fd68a82c2913a2b54042cfc3145ed95db3409554a09fc0a8d1b6cf799f4. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «intAt(_,_)_VERIFICATION_Int_IntSeq_Int» : SortIntSeq → SortInt → SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _ => 0
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» value rest, index =>
      if index = 0 then value
      else if index > 0 then
        «intAt(_,_)_VERIFICATION_Int_IntSeq_Int» rest (index - 1)
      else
        0

/- KORE symbol: LblintVals'LParUndsRParUnds'VERIFICATION'Unds'ValSeq'Unds'IntSeq; frozen source obligations: rule-041ae6f97e0a64393d4fd3489adb8b7922f6bdd833dd98ec4a40214de3ea0864, rule-02406fd68a82c2913a2b54042cfc3145ed95db3409554a09fc0a8d1b6cf799f4. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «intVals(_)_VERIFICATION_ValSeq_IntSeq» : SortIntSeq → SortValSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» =>
      SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» value rest =>
      SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
        (SortVal.inj_SortInt value)
        («intVals(_)_VERIFICATION_ValSeq_IntSeq» rest)

/- KORE symbol: LblisLen'LParUndsRParUnds'MPY-CORE'Unds'Int'Unds'IntSeq; frozen source obligations: rule-041ae6f97e0a64393d4fd3489adb8b7922f6bdd833dd98ec4a40214de3ea0864, rule-02406fd68a82c2913a2b54042cfc3145ed95db3409554a09fc0a8d1b6cf799f4. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «isLen(_)_MPY-CORE_Int_IntSeq» : SortIntSeq → SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => 0
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ rest =>
      1 + «isLen(_)_MPY-CORE_Int_IntSeq» rest

/- KORE symbol: LblvalSeqAt'LParUndsCommUndsRParUnds'MPY-SUBSCRIPT'Unds'Val'Unds'ValSeq'Unds'Int; frozen source obligations: rule-02406fd68a82c2913a2b54042cfc3145ed95db3409554a09fc0a8d1b6cf799f4. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int» : SortValSeq → SortInt → SortVal
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _ =>
      SortVal.«noneV_MPY-CORE_Val»
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» value rest, index =>
      if index = 0 then value
      else if index > 0 then
        «valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int» rest (index - 1)
      else
        SortVal.«noneV_MPY-CORE_Val»

/- KORE symbol: LblvsLen'LParUndsRParUnds'MPY-CORE'Unds'Int'Unds'ValSeq; frozen source obligations: rule-041ae6f97e0a64393d4fd3489adb8b7922f6bdd833dd98ec4a40214de3ea0864. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «vsLen(_)_MPY-CORE_Int_ValSeq» : SortValSeq → SortInt
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => 0
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _ rest =>
      1 + «vsLen(_)_MPY-CORE_Int_ValSeq» rest

theorem final :
    Klean40TriplesSumToZero.Lemmas.targetStatement _andBool_ «_<Int_» «_<=Int_» «intAt(_,_)_VERIFICATION_Int_IntSeq_Int» «intVals(_)_VERIFICATION_ValSeq_IntSeq» «isLen(_)_MPY-CORE_Int_IntSeq» «valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int» «vsLen(_)_MPY-CORE_Int_ValSeq» := by
  unfold Klean40TriplesSumToZero.Lemmas.targetStatement
  constructor
  · intro intSeq
    induction intSeq <;>
      simp [
        «intVals(_)_VERIFICATION_ValSeq_IntSeq»,
        «isLen(_)_MPY-CORE_Int_IntSeq»,
        «vsLen(_)_MPY-CORE_Int_ValSeq»,
        *
      ]
  · intro index intSeq guarded
    have bounds :
        0 ≤ index ∧ index < «isLen(_)_MPY-CORE_Int_IntSeq» intSeq := by
      simpa [_andBool_, «_<Int_», «_<=Int_»] using guarded
    rcases bounds with ⟨nonnegative, inBounds⟩
    clear guarded
    simp only [SortInt] at index nonnegative inBounds
    induction intSeq generalizing index
    · simp [«isLen(_)_MPY-CORE_Int_IntSeq»] at inBounds
      omega
    · rename_i value rest inductionHypothesis
      by_cases zero : index = 0
      · subst index
        simp [
          «intAt(_,_)_VERIFICATION_Int_IntSeq_Int»,
          «intVals(_)_VERIFICATION_ValSeq_IntSeq»,
          «valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int»
        ]
      · have positive : index > 0 := by omega
        have predecessorNonnegative : 0 ≤ index - 1 := by omega
        have predecessorInBounds :
            index - 1 < «isLen(_)_MPY-CORE_Int_IntSeq» rest := by
          simp [«isLen(_)_MPY-CORE_Int_IntSeq»] at inBounds
          simp only [SortInt] at inBounds ⊢
          omega
        simpa [
          «intAt(_,_)_VERIFICATION_Int_IntSeq_Int»,
          «intVals(_)_VERIFICATION_ValSeq_IntSeq»,
          «valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int»,
          zero,
          positive
        ] using
          inductionHypothesis
            (index - 1)
            predecessorNonnegative
            predecessorInBounds

end Proof
