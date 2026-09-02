import Proof

namespace BridgeAudit

def emptyCodes : SortIntSeq :=
  .«.IntSeq_MPY-CORE_IntSeq»

def oneCode : SortIntSeq :=
  .«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 97 emptyCodes

def threeCodes : SortIntSeq :=
  .«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 97
    (.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 98
      (.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 99 emptyCodes))

def emptyValues : SortValSeq :=
  .«.ValSeq_MPY-CORE_ValSeq»

def twoValues : SortValSeq :=
  .«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (.inj_SortInt 11)
    (.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (.inj_SortBool true) emptyValues)

def oneString : SortVal :=
  .inj_SortStr (.«str(_)_MPY-CORE_Str_IntSeq» oneCode)

def threeString : SortVal :=
  .inj_SortStr (.«str(_)_MPY-CORE_Str_IntSeq» threeCodes)

def nestedNoncanonicalString : SortVal :=
  .inj_SortIterable
    (.inj_SortStr (.«str(_)_MPY-CORE_Str_IntSeq» oneCode))

def listTwo : SortVal :=
  .inj_SortIterable (.«list(_)_MPY-CORE_Iterable_ValSeq» twoValues)

def tupleTwo : SortVal :=
  .inj_SortIterable (.«tuple(_)_MPY-CORE_Iterable_ValSeq» twoValues)

def rangePositive : SortVal :=
  .inj_SortIterable
    (.«rangeObj(_,_,_)_MPY-CORE_Iterable_Int_Int_Int» 0 5 2)

def rangeNegative : SortVal :=
  .inj_SortIterable
    (.«rangeObj(_,_,_)_MPY-CORE_Iterable_Int_Int_Int» 5 0 (-2))

def rangeEmpty : SortVal :=
  .inj_SortIterable
    (.«rangeObj(_,_,_)_MPY-CORE_Iterable_Int_Int_Int» 5 0 2)

def rangeZeroStep : SortVal :=
  .inj_SortIterable
    (.«rangeObj(_,_,_)_MPY-CORE_Iterable_Int_Int_Int» 0 5 0)

def setThree : SortVal :=
  .«setV(_)_MPY-SET_Val_IntSeq» threeCodes

example : Proof.«isLen(_)_MPY-CORE_Int_IntSeq» emptyCodes = 0 := by rfl
example : Proof.«isLen(_)_MPY-CORE_Int_IntSeq» oneCode = 1 := by rfl
example : Proof.«isLen(_)_MPY-CORE_Int_IntSeq» threeCodes = 3 := by rfl

example : Proof.«isStrV(_)_MPY-BUILTINS_Bool_Val» threeString = true := by rfl
example : Proof.«isStrV(_)_MPY-BUILTINS_Bool_Val» (.inj_SortInt 3) = false := by rfl
example : Proof.«isStrV(_)_MPY-BUILTINS_Bool_Val» listTwo = false := by rfl
example : Proof.«isStrV(_)_MPY-BUILTINS_Bool_Val» nestedNoncanonicalString = false := by rfl

example : Proof.«stringCodes(_)_VERIFICATION_IntSeq_Val» threeString = threeCodes := by rfl
example :
    Proof.«stringCodes(_)_VERIFICATION_IntSeq_Val» (.inj_SortInt 3) =
      emptyCodes := by rfl

example : Proof.«seqLen(_)_MPY-BUILTINS_Int_Val» threeString = 3 := by rfl
example : Proof.«seqLen(_)_MPY-BUILTINS_Int_Val» listTwo = 2 := by rfl
example : Proof.«seqLen(_)_MPY-BUILTINS_Int_Val» tupleTwo = 2 := by rfl
example : Proof.«seqLen(_)_MPY-BUILTINS_Int_Val» rangePositive = 3 := by rfl
example : Proof.«seqLen(_)_MPY-BUILTINS_Int_Val» rangeNegative = 3 := by rfl
example : Proof.«seqLen(_)_MPY-BUILTINS_Int_Val» rangeEmpty = 0 := by rfl
example : Proof.«seqLen(_)_MPY-BUILTINS_Int_Val» rangeZeroStep = 0 := by rfl
example : Proof.«seqLen(_)_MPY-BUILTINS_Int_Val» setThree = 3 := by rfl
example :
    Proof.«seqLen(_)_MPY-BUILTINS_Int_Val» SortVal.«noneV_MPY-CORE_Val» =
      0 := by rfl

#eval Proof.«isLen(_)_MPY-CORE_Int_IntSeq» threeCodes
#eval Proof.«isStrV(_)_MPY-BUILTINS_Bool_Val» threeString
#eval Proof.«isStrV(_)_MPY-BUILTINS_Bool_Val» (.inj_SortInt 3)
#eval Proof.«seqLen(_)_MPY-BUILTINS_Int_Val» threeString
#eval Proof.«seqLen(_)_MPY-BUILTINS_Int_Val» listTwo
#eval Proof.«seqLen(_)_MPY-BUILTINS_Int_Val» rangePositive
#eval Proof.«seqLen(_)_MPY-BUILTINS_Int_Val» rangeNegative
#eval Proof.«seqLen(_)_MPY-BUILTINS_Int_Val» setThree

def falseRecognizer (_ : SortVal) : SortBool := false
def zeroIntSeqLength (_ : SortIntSeq) : SortInt := 0
def zeroValueLength (_ : SortVal) : SortInt := 0
def emptyProjection (_ : SortVal) : SortIntSeq := emptyCodes

theorem vacuousRecognizerMutation :
    Klean74TotalMatch.Lemmas.targetStatement
      Proof.«isLen(_)_MPY-CORE_Int_IntSeq»
      falseRecognizer
      Proof.«seqLen(_)_MPY-BUILTINS_Int_Val»
      Proof.«stringCodes(_)_VERIFICATION_IntSeq_Val» := by
  unfold Klean74TotalMatch.Lemmas.targetStatement
  intro value impossible
  cases impossible

theorem coordinatedConstantMutation :
    Klean74TotalMatch.Lemmas.targetStatement
      zeroIntSeqLength
      Proof.«isStrV(_)_MPY-BUILTINS_Bool_Val»
      zeroValueLength
      emptyProjection := by
  unfold Klean74TotalMatch.Lemmas.targetStatement
  intro value isString
  rfl

theorem isolatedZeroValueLengthRejected :
    ¬ Klean74TotalMatch.Lemmas.targetStatement
      Proof.«isLen(_)_MPY-CORE_Int_IntSeq»
      Proof.«isStrV(_)_MPY-BUILTINS_Bool_Val»
      zeroValueLength
      Proof.«stringCodes(_)_VERIFICATION_IntSeq_Val» := by
  intro claimed
  have bad := claimed oneString (by rfl)
  have impossible : (0 : SortInt) = 1 := by
    simpa [zeroValueLength, oneString, oneCode, emptyCodes,
      Proof.«isLen(_)_MPY-CORE_Int_IntSeq»,
      Proof.«stringCodes(_)_VERIFICATION_IntSeq_Val»] using bad
  exact (by decide : (0 : SortInt) ≠ 1) impossible

theorem isolatedZeroIntSeqLengthRejected :
    ¬ Klean74TotalMatch.Lemmas.targetStatement
      zeroIntSeqLength
      Proof.«isStrV(_)_MPY-BUILTINS_Bool_Val»
      Proof.«seqLen(_)_MPY-BUILTINS_Int_Val»
      Proof.«stringCodes(_)_VERIFICATION_IntSeq_Val» := by
  intro claimed
  have bad := claimed oneString (by rfl)
  have impossible : (1 : SortInt) = 0 := by
    simpa [zeroIntSeqLength, oneString, oneCode, emptyCodes,
      Proof.«isLen(_)_MPY-CORE_Int_IntSeq»,
      Proof.«seqLen(_)_MPY-BUILTINS_Int_Val»,
      Proof.«stringCodes(_)_VERIFICATION_IntSeq_Val»] using bad
  exact (by decide : (1 : SortInt) ≠ 0) impossible

theorem isolatedEmptyProjectionRejected :
    ¬ Klean74TotalMatch.Lemmas.targetStatement
      Proof.«isLen(_)_MPY-CORE_Int_IntSeq»
      Proof.«isStrV(_)_MPY-BUILTINS_Bool_Val»
      Proof.«seqLen(_)_MPY-BUILTINS_Int_Val»
      emptyProjection := by
  intro claimed
  have bad := claimed oneString (by rfl)
  have impossible : (1 : SortInt) = 0 := by
    simpa [emptyProjection, oneString, oneCode, emptyCodes,
      Proof.«isLen(_)_MPY-CORE_Int_IntSeq»,
      Proof.«seqLen(_)_MPY-BUILTINS_Int_Val»] using bad
  exact (by decide : (1 : SortInt) ≠ 0) impossible

end BridgeAudit
