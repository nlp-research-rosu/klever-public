import Proof

namespace BridgeAudit

open Proof

def nil : SortValSeq := SortValSeq.«.ValSeq_MPY-CORE_ValSeq»

def cons (head : SortVal) (tail : SortValSeq) : SortValSeq :=
  SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» head tail

def none : SortVal := SortVal.«noneV_MPY-CORE_Val»
def bool (value : Bool) : SortVal := SortVal.inj_SortBool value
def int (value : Int) : SortVal := SortVal.inj_SortInt value

def headBool : SortValSeq → Bool
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
      (SortVal.inj_SortBool value) _ => value
  | _ => false

/- Selected positions 0 and 3 are [true, false]. Python's sorted operation
   returns [false, true], but the candidate's non-integer fallback is identity. -/
def boolInput : SortValSeq :=
  cons (bool true) (cons none (cons none (cons (bool false) nil)))

def boolSourceExpected : SortValSeq :=
  cons (bool false) (cons none (cons none (cons (bool true) nil)))

theorem candidateBoolIsIdentity :
    «sortThirdResult(_)_VERIFICATION_ValSeq_ValSeq» boolInput = boolInput := by
  rfl

theorem candidateBoolDisagreesWithSource :
    «sortThirdResult(_)_VERIFICATION_ValSeq_ValSeq» boolInput ≠
      boolSourceExpected := by
  rw [candidateBoolIsIdentity]
  intro h
  have htf : true = false := by
    simpa [headBool, boolInput, boolSourceExpected, bool, cons] using
      congrArg headBool h
  exact Bool.noConfusion htf

/- Frozen HumanEval example: selected integer positions [5, 4, 2] become
   [2, 4, 5], while all non-third positions are unchanged. -/
def intInput : SortValSeq :=
  cons (int 5) (cons (int 6) (cons (int 3)
    (cons (int 4) (cons (int 8) (cons (int 9) (cons (int 2) nil))))))

def intExpected : SortValSeq :=
  cons (int 2) (cons (int 6) (cons (int 3)
    (cons (int 4) (cons (int 8) (cons (int 9) (cons (int 5) nil))))))

theorem candidateIntegerExample :
    «sortThirdResult(_)_VERIFICATION_ValSeq_ValSeq» intInput = intExpected := by
  rfl

/- Counterfactual mutation at a selected position changes the sorted result. -/
def intMutated : SortValSeq :=
  cons (int 5) (cons (int 6) (cons (int 3)
    (cons (int 7) (cons (int 8) (cons (int 9) (cons (int 2) nil))))))

def intMutatedExpected : SortValSeq :=
  cons (int 2) (cons (int 6) (cons (int 3)
    (cons (int 5) (cons (int 8) (cons (int 9) (cons (int 7) nil))))))

theorem candidateIntegerMutation :
    «sortThirdResult(_)_VERIFICATION_ValSeq_ValSeq» intMutated =
      intMutatedExpected := by
  rfl

theorem comparisonBoundary :
    Proof.«_<=Int_» 1 2 = true ∧ Proof.«_<=Int_» 2 1 = false := by
  decide

theorem lengthBoundary :
    «vsLen(_)_MPY-CORE_Int_ValSeq» nil = 0 ∧
      «vsLen(_)_MPY-CORE_Int_ValSeq» (cons none nil) = 1 := by
  decide

theorem concatBoundary :
    «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» nil boolInput =
        boolInput ∧
      «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» boolInput nil =
        boolInput := by
  exact ⟨rfl, rfl⟩

end BridgeAudit
