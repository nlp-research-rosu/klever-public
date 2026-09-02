import Proof

namespace AuditBridge

def nil : SortValSeq :=
  SortValSeq.«.ValSeq_MPY-CORE_ValSeq»

def intVal (n : SortInt) : SortVal :=
  SortVal.inj_SortInt n

def boolVal (b : SortBool) : SortVal :=
  SortVal.inj_SortBool b

def cons (v : SortVal) (rest : SortValSeq) : SortValSeq :=
  SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» v rest

def ints : List SortInt → SortValSeq
  | [] => nil
  | n :: rest => cons (intVal n) (ints rest)

example : Proof._andBool_ true false = false := rfl
example : Proof._andBool_ true true = true := rfl
example : Proof.«_==Int_» (-3) (-3) = true := by native_decide
example : Proof.«_==Int_» (-3) 3 = false := by native_decide
example : Proof.notBool_ true = false := rfl
example : Proof.notBool_ false = true := rfl

example : Proof.«collatzNext(_)_VERIFICATION-SYNTAX_Int_Int» (-4) = -2 := by
  native_decide
example : Proof.«collatzNext(_)_VERIFICATION-SYNTAX_Int_Int» (-3) = -8 := by
  native_decide
example : Proof.«collatzNext(_)_VERIFICATION-SYNTAX_Int_Int» 0 = 0 := by
  native_decide
example : Proof.«collatzNext(_)_VERIFICATION-SYNTAX_Int_Int» 5 = 16 := by
  native_decide
example : Proof.«collatzNext(_)_VERIFICATION-SYNTAX_Int_Int» 6 = 3 := by
  native_decide

example :
    Proof.«maybeOdd(_)_VERIFICATION-SYNTAX_ValSeq_Int» (-4) = nil := by
  rfl
example :
    Proof.«maybeOdd(_)_VERIFICATION-SYNTAX_ValSeq_Int» (-3) =
      cons (intVal (-3)) nil := by
  rfl

example :
    Proof.«valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»
        (ints [5, 16]) (ints [8, 1]) =
      ints [5, 16, 8, 1] := rfl

example :
    Proof.«traceFirstInt(_)_VERIFICATION-SYNTAX_Int_ValSeq»
        (cons (boolVal true) (ints [7])) = 0 := rfl
example :
    Proof.«traceLastInt(_)_VERIFICATION-SYNTAX_Int_ValSeq»
        (cons (boolVal true) (ints [7])) = 7 := rfl
example :
    Proof.«traceLastInt(_)_VERIFICATION-SYNTAX_Int_ValSeq»
        (cons (intVal 7) (cons (boolVal true) nil)) = 0 := rfl

example :
    Proof.«oddWithoutLast(_)_VERIFICATION-SYNTAX_ValSeq_ValSeq»
        (ints [5, 16, 8, 4, 2, 1]) =
      ints [5] := by rfl
example :
    Proof.«oddWithoutLast(_)_VERIFICATION-SYNTAX_ValSeq_ValSeq»
        (cons (boolVal true) (ints [5, 16, 1])) =
      ints [5] := by rfl
example :
    Proof.«oddWithoutLast(_)_VERIFICATION-SYNTAX_ValSeq_ValSeq»
        (ints [1]) = nil := rfl

example :
    Proof.«validCollatzTrace(_)_VERIFICATION-SYNTAX_Bool_ValSeq»
        (ints [5, 16, 8, 4, 2, 1]) = true := by native_decide
example :
    Proof.«validCollatzTrace(_)_VERIFICATION-SYNTAX_Bool_ValSeq»
        (ints [5, 15]) = false := by native_decide
example :
    Proof.«validCollatzTrace(_)_VERIFICATION-SYNTAX_Bool_ValSeq»
        (cons (boolVal true) nil) = false := rfl
example :
    Proof.«validCollatzTrace(_)_VERIFICATION-SYNTAX_Bool_ValSeq»
        nil = false := rfl

example :
    Proof.«_==K_»
        (SortK.kseq (SortKItem.inj_SortValSeq (ints [5])) SortK.dotk)
        (SortK.kseq (SortKItem.inj_SortValSeq (ints [5])) SortK.dotk) =
      true := by
  simp [Proof.«_==K_»]
example :
    Proof.«_==K_»
        (SortK.kseq (SortKItem.inj_SortValSeq (ints [5])) SortK.dotk)
        (SortK.kseq (SortKItem.inj_SortValSeq (ints [6])) SortK.dotk) =
      false := by
  simp [Proof.«_==K_», ints, cons, intVal, nil]

def hardcodedNext (_ : SortInt) : SortInt := 1
def alwaysEmptyMaybe (_ : SortInt) : SortValSeq := nil
def constantConcat (_ _ : SortValSeq) : SortValSeq := nil
def identityOdd (values : SortValSeq) : SortValSeq := values
def constantValid (_ : SortValSeq) : SortBool := true

example :
    hardcodedNext 5 ≠
      Proof.«collatzNext(_)_VERIFICATION-SYNTAX_Int_Int» 5 := by
  native_decide
example :
    alwaysEmptyMaybe (-3) ≠
      Proof.«maybeOdd(_)_VERIFICATION-SYNTAX_ValSeq_Int» (-3) := by
  simp [alwaysEmptyMaybe, Proof.«maybeOdd(_)_VERIFICATION-SYNTAX_ValSeq_Int»,
    nil, cons, intVal]
example :
    constantConcat (ints [5]) (ints [1]) ≠
      Proof.«valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»
        (ints [5]) (ints [1]) := by
  simp [constantConcat, Proof.«valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»,
    ints, nil, cons, intVal]
example :
    identityOdd (ints [5, 16, 1]) ≠
      Proof.«oddWithoutLast(_)_VERIFICATION-SYNTAX_ValSeq_ValSeq»
        (ints [5, 16, 1]) := by
  simp [identityOdd,
    Proof.«oddWithoutLast(_)_VERIFICATION-SYNTAX_ValSeq_ValSeq»,
    ints, nil, cons, intVal]
example :
    constantValid (ints [5, 15]) ≠
      Proof.«validCollatzTrace(_)_VERIFICATION-SYNTAX_Bool_ValSeq»
        (ints [5, 15]) := by
  native_decide

end AuditBridge
