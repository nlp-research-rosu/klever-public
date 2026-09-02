import Proof

namespace OperationalWitness

def emptyIS : SortIntSeq := SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»

def oneCode (code : Int) : SortVal :=
  SortVal.inj_SortStr
    (SortStr.«str(_)_MPY-CORE_Str_IntSeq»
      (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» code emptyIS))

def intValue (value : Int) : SortVal := SortVal.inj_SortInt value

def emptyVS : SortValSeq := SortValSeq.«.ValSeq_MPY-CORE_ValSeq»

def consVS (head : SortVal) (tail : SortValSeq) : SortValSeq :=
  SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» head tail

/- Source/K witness: ["b", 0, 0, "a"].  The third-position slice is
   ["b", "a"], which frozen sortVS orders as ["a", "b"]. -/
def stringInput : SortValSeq :=
  consVS (oneCode 98)
    (consVS (intValue 0)
      (consVS (intValue 0)
        (consVS (oneCode 97) emptyVS)))

def frozenExpected : SortValSeq :=
  consVS (oneCode 97)
    (consVS (intValue 0)
      (consVS (intValue 0)
        (consVS (oneCode 98) emptyVS)))

def isStringInput : SortValSeq → Bool
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
      (SortVal.inj_SortStr
        (SortStr.«str(_)_MPY-CORE_Str_IntSeq»
          (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 98
            SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)))
      (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
        (SortVal.inj_SortInt 0)
        (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
          (SortVal.inj_SortInt 0)
          (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
            (SortVal.inj_SortStr
              (SortStr.«str(_)_MPY-CORE_Str_IntSeq»
                (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 97
                  SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)))
            SortValSeq.«.ValSeq_MPY-CORE_ValSeq»))) => true
  | _ => false

def isFrozenExpected : SortValSeq → Bool
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
      (SortVal.inj_SortStr
        (SortStr.«str(_)_MPY-CORE_Str_IntSeq»
          (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 97
            SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)))
      (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
        (SortVal.inj_SortInt 0)
        (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
          (SortVal.inj_SortInt 0)
          (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
            (SortVal.inj_SortStr
              (SortStr.«str(_)_MPY-CORE_Str_IntSeq»
                (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 98
                  SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)))
            SortValSeq.«.ValSeq_MPY-CORE_ValSeq»))) => true
  | _ => false

def candidateStringOutput :=
  Proof.«sortThirdResult(_)_VERIFICATION_ValSeq_ValSeq» stringInput

#eval isStringInput candidateStringOutput
#eval isFrozenExpected candidateStringOutput

example : candidateStringOutput = stringInput := by rfl
example : isFrozenExpected frozenExpected = true := by rfl

end OperationalWitness
