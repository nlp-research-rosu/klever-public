import Proof

namespace BridgeProbes

def empty : SortValSeq :=
  SortValSeq.«.ValSeq_MPY-CORE_ValSeq»

def cons (head : SortVal) (tail : SortValSeq) : SortValSeq :=
  SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» head tail

def intVal (value : SortInt) : SortVal :=
  SortVal.inj_SortInt value

def values : SortValSeq :=
  cons (intVal 3) (cons (intVal (-2)) (cons (intVal 7) empty))

def reversedValues : SortValSeq :=
  cons (intVal 7) (cons (intVal (-2)) (cons (intVal 3) empty))

def includesNonInt : SortValSeq :=
  cons (intVal 1) (cons SortVal.«noneV_MPY-CORE_Val» empty)

example :
    Proof.«allInts(_)_VERIFICATION_Bool_ValSeq» empty = true := by
  rfl

example :
    Proof.«allInts(_)_VERIFICATION_Bool_ValSeq» values = true := by
  rfl

example :
    Proof.«allInts(_)_VERIFICATION_Bool_ValSeq» includesNonInt = false := by
  rfl

example :
    Proof.«reverseVS(_)_VERIFICATION_ValSeq_ValSeq» values =
      reversedValues := by
  rfl

example :
    Proof.«sumIntVS(_)_VERIFICATION_Int_ValSeq» values = 8 := by
  rfl

example :
    Proof.«doSlice(_,_,_,_)_MPY-SUBSCRIPT_Val_Val_OptInt_OptInt_OptInt»
        (SortVal.inj_SortIterable
          (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» values))
        SortOptInt.«noB_MPY-SUBSCRIPT_OptInt»
        SortOptInt.«noB_MPY-SUBSCRIPT_OptInt»
        (SortOptInt.«someB(_)_MPY-SUBSCRIPT_OptInt_Int» (-1)) =
      SortVal.inj_SortIterable
        (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» reversedValues) := by
  rfl

example :
    Proof.«doSlice(_,_,_,_)_MPY-SUBSCRIPT_Val_Val_OptInt_OptInt_OptInt»
        (SortVal.inj_SortIterable
          (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» values))
        SortOptInt.«noB_MPY-SUBSCRIPT_OptInt»
        SortOptInt.«noB_MPY-SUBSCRIPT_OptInt»
        (SortOptInt.«someB(_)_MPY-SUBSCRIPT_OptInt_Int» 1) =
      (_root_.«doSlice(_,_,_,_)_MPY-SUBSCRIPT_Val_Val_OptInt_OptInt_OptInt»
        (SortVal.inj_SortIterable
          (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» values))
        SortOptInt.«noB_MPY-SUBSCRIPT_OptInt»
        SortOptInt.«noB_MPY-SUBSCRIPT_OptInt»
        (SortOptInt.«someB(_)_MPY-SUBSCRIPT_OptInt_Int» 1)).getD
          SortVal.«noneV_MPY-CORE_Val» := by
  rfl

/- Counterfactual definitions demonstrate why the operational-bridge audit is
   necessary in addition to checking the theorem mechanically. -/
def badAllInts (_ : SortValSeq) : SortBool := false

def badReverse (input : SortValSeq) : SortValSeq := input

noncomputable def badDoSlice :
    SortVal → SortOptInt → SortOptInt → SortOptInt → SortVal
  | SortVal.inj_SortIterable
      (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» input),
      SortOptInt.«noB_MPY-SUBSCRIPT_OptInt»,
      SortOptInt.«noB_MPY-SUBSCRIPT_OptInt»,
      SortOptInt.«someB(_)_MPY-SUBSCRIPT_OptInt_Int» (-1) =>
      SortVal.inj_SortIterable
        (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» (badReverse input))
  | _, _, _, _ => SortVal.«noneV_MPY-CORE_Val»

def badSum (_ : SortValSeq) : SortInt := 0

theorem counterfactualTargetStillCloses :
    Klean72WillItFly.Lemmas.targetStatement
      badAllInts badDoSlice badReverse badSum := by
  unfold Klean72WillItFly.Lemmas.targetStatement
  constructor
  · intro input
    rfl
  · intro _ _ _ _ _ _ _ _ _ _ _ input h
    simp [badAllInts] at h

example : badReverse values = values := by
  rfl

end BridgeProbes
