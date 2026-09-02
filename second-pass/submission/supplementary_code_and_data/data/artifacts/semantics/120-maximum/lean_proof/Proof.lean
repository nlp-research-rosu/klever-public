import Klean120Maximum.Lemmas

namespace Proof

-- `sort.k` implements `sortVS` by stable insertion sort and takes the
-- insertion-left branch exactly when two integer values satisfy `a ≤ b`.
-- Integer lists are the task's input domain.  The generated `SortVal` has no
-- runtime string-value constructor; for its unsupported value forms, keeping
-- the incoming value before the tail is a stable total extension of the
-- frozen concrete rules.
private def sortLe (x y : SortVal) : Bool :=
  match x, y with
  | .inj_SortInt a, .inj_SortInt b => decide (a ≤ b)
  | _, _ => true

private def insertSorted (x : SortVal) : SortValSeq → SortValSeq
  | .«.ValSeq_MPY-CORE_ValSeq» =>
      .«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
        x
        .«.ValSeq_MPY-CORE_ValSeq»
  | .«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» y ys =>
      if sortLe x y then
        .«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
          x
          (.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» y ys)
      else
        .«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
          y
          (insertSorted x ys)

/- KORE symbol: LblsortVS; frozen source obligations: rule-cc6f58aca1084e3612f2f52f4a593aa3490485de2b5353d8bf0ae5c830c9f907. Replace this stub with its honest total meaning from the frozen K semantics. -/
def sortVS : SortValSeq → SortValSeq
  | .«.ValSeq_MPY-CORE_ValSeq» =>
      .«.ValSeq_MPY-CORE_ValSeq»
  | .«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» x xs =>
      insertSorted x (sortVS xs)

/- KORE symbol: LblvsLen'LParUndsRParUnds'MPY-CORE'Unds'Int'Unds'ValSeq; frozen source obligations: rule-cc6f58aca1084e3612f2f52f4a593aa3490485de2b5353d8bf0ae5c830c9f907. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «vsLen(_)_MPY-CORE_Int_ValSeq» : SortValSeq → SortInt
  | .«.ValSeq_MPY-CORE_ValSeq» => 0
  | .«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _ xs =>
      1 + «vsLen(_)_MPY-CORE_Int_ValSeq» xs

private theorem vsLen_insertSorted (x : SortVal) :
    ∀ xs : SortValSeq,
      «vsLen(_)_MPY-CORE_Int_ValSeq» (insertSorted x xs) =
        1 + «vsLen(_)_MPY-CORE_Int_ValSeq» xs
  | .«.ValSeq_MPY-CORE_ValSeq» => rfl
  | .«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» y ys => by
      simp only [insertSorted]
      split
      · rfl
      · simp only [«vsLen(_)_MPY-CORE_Int_ValSeq»,
          vsLen_insertSorted x ys]

private theorem vsLen_sortVS :
    ∀ xs : SortValSeq,
      «vsLen(_)_MPY-CORE_Int_ValSeq» (sortVS xs) =
        «vsLen(_)_MPY-CORE_Int_ValSeq» xs
  | .«.ValSeq_MPY-CORE_ValSeq» => rfl
  | .«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» x xs => by
      calc
        «vsLen(_)_MPY-CORE_Int_ValSeq»
            (sortVS
              (.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» x xs)) =
            «vsLen(_)_MPY-CORE_Int_ValSeq»
              (insertSorted x (sortVS xs)) := rfl
        _ = 1 + «vsLen(_)_MPY-CORE_Int_ValSeq» (sortVS xs) :=
          vsLen_insertSorted x (sortVS xs)
        _ = 1 + «vsLen(_)_MPY-CORE_Int_ValSeq» xs :=
          congrArg (fun n : SortInt => 1 + n) (vsLen_sortVS xs)
        _ = «vsLen(_)_MPY-CORE_Int_ValSeq»
              (.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» x xs) := rfl

theorem final :
    Klean120Maximum.Lemmas.targetStatement sortVS «vsLen(_)_MPY-CORE_Int_ValSeq» := by
  exact vsLen_sortVS

end Proof
