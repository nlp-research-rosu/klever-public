import Proof

open Klean51RemoveVowels.Lemmas

def seqOfList : List SortInt → SortIntSeq
  | [] => SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
  | c :: rest =>
      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» c (seqOfList rest)

def vowelCodes : SortIntSeq :=
  seqOfList [97, 101, 105, 111, 117, 65, 69, 73, 79, 85]

-- An independent direct transcription of verification.k:12-16.
def operationalIsVowel (C : SortInt) : SortBool :=
  C == 65 || C == 69 || C == 73 || C == 79 || C == 85 ||
  C == 97 || C == 101 || C == 105 || C == 111 || C == 117

-- Independent direct transcriptions of supplied semantics/str.k:32-41.
def operationalPrefix : SortIntSeq → SortIntSeq → SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _ => true
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ _,
      SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => false
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» a as,
      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» b bs =>
      a == b && operationalPrefix as bs

def operationalContains (needle : SortIntSeq) : SortIntSeq → SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» =>
      operationalPrefix needle SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head rest =>
      if operationalPrefix needle
          (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head rest) then
        true
      else
        operationalContains needle rest

#check Proof.«isVowelCode(_)_VERIFICATION_Bool_Int»
#check Proof.«strContains(_,_)_MPY-STR_Bool_IntSeq_IntSeq»

#eval [
  Proof.«isVowelCode(_)_VERIFICATION_Bool_Int» (-1),
  Proof.«isVowelCode(_)_VERIFICATION_Bool_Int» 64,
  Proof.«isVowelCode(_)_VERIFICATION_Bool_Int» 65,
  Proof.«isVowelCode(_)_VERIFICATION_Bool_Int» 66,
  Proof.«isVowelCode(_)_VERIFICATION_Bool_Int» 97,
  Proof.«isVowelCode(_)_VERIFICATION_Bool_Int» 117,
  Proof.«isVowelCode(_)_VERIFICATION_Bool_Int» 118,
  Proof.«isVowelCode(_)_VERIFICATION_Bool_Int» 1000000
]

#eval [
  Proof.«strContains(_,_)_MPY-STR_Bool_IntSeq_IntSeq» (seqOfList []) (seqOfList []),
  Proof.«strContains(_,_)_MPY-STR_Bool_IntSeq_IntSeq» (seqOfList []) vowelCodes,
  Proof.«strContains(_,_)_MPY-STR_Bool_IntSeq_IntSeq» (seqOfList [97]) vowelCodes,
  Proof.«strContains(_,_)_MPY-STR_Bool_IntSeq_IntSeq» (seqOfList [101]) vowelCodes,
  Proof.«strContains(_,_)_MPY-STR_Bool_IntSeq_IntSeq» (seqOfList [66]) vowelCodes,
  Proof.«strContains(_,_)_MPY-STR_Bool_IntSeq_IntSeq» (seqOfList [101, 105]) vowelCodes,
  Proof.«strContains(_,_)_MPY-STR_Bool_IntSeq_IntSeq» (seqOfList [105, 101]) vowelCodes,
  Proof.«strContains(_,_)_MPY-STR_Bool_IntSeq_IntSeq» (seqOfList [85, 0]) vowelCodes
]

example (C : SortInt) :
    Proof.«isVowelCode(_)_VERIFICATION_Bool_Int» C = operationalIsVowel C := by
  rfl

example :
    Proof.«strContains(_,_)_MPY-STR_Bool_IntSeq_IntSeq»
      (seqOfList [101, 105]) vowelCodes =
    operationalContains (seqOfList [101, 105]) vowelCodes := by
  decide

-- Counterfactual 1: dropping U+0075/'u' changes the operational result.
def missingLowerU (C : SortInt) : SortBool :=
  C == 65 || C == 69 || C == 73 || C == 79 || C == 85 ||
  C == 97 || C == 101 || C == 105 || C == 111

example :
    missingLowerU 117 ≠
      Proof.«isVowelCode(_)_VERIFICATION_Bool_Int» 117 := by
  decide

-- Counterfactual 2: checking only the first haystack position misses 'e'.
def prefixOnlyContains (needle haystack : SortIntSeq) : SortBool :=
  operationalPrefix needle haystack

example :
    prefixOnlyContains (seqOfList [101]) vowelCodes ≠
      Proof.«strContains(_,_)_MPY-STR_Bool_IntSeq_IntSeq»
        (seqOfList [101]) vowelCodes := by
  decide

-- The generated equation alone admits coordinated constants. This witness is
-- why the separate operational-bridge audit of both candidate definitions is
-- necessary; the submitted definitions above are not these constants.
def constantFalseIs (_ : SortInt) : SortBool := false
def constantFalseContains (_ _ : SortIntSeq) : SortBool := false

example :
    targetStatement constantFalseIs constantFalseContains := by
  intro C
  rfl

-- The conjunct is not a tautology: changing either bridge alone is rejected
-- at the satisfiable witness C = 97.
example :
    ¬ targetStatement
      constantFalseIs
      operationalContains := by
  intro h
  have h97 := h 97
  simp [
    constantFalseIs,
    operationalContains,
    operationalPrefix
  ] at h97

example :
    ¬ targetStatement
      Proof.«isVowelCode(_)_VERIFICATION_Bool_Int»
      constantFalseContains := by
  intro h
  have h97 := h 97
  simp [
    constantFalseContains,
    Proof.«isVowelCode(_)_VERIFICATION_Bool_Int»
  ] at h97
