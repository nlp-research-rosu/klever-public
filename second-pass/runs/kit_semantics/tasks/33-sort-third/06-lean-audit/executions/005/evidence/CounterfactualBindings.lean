import Klean33SortThird.Lemmas

namespace CounterfactualBindings

def badLe (_left _right : SortInt) : SortBool := false

def badSort (_values : SortValSeq) : SortValSeq :=
  SortValSeq.«.ValSeq_MPY-CORE_ValSeq»

def badConcat (left _right : SortValSeq) : SortValSeq := left

def badLen (_values : SortValSeq) : SortInt := 0

theorem convenientButOperationallyFalse :
    Klean33SortThird.Lemmas.targetStatement
      badLe badSort badConcat badLen := by
  exact
    ⟨(fun _VS h => Bool.noConfusion h),
     (fun _C _B _A => rfl),
     (fun _A => rfl)⟩

#print axioms convenientButOperationallyFalse

end CounterfactualBindings
