import Proof

private def digits105 : SortIntSeq :=
  .«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 49
    (.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 48
      (.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 53
        .«.IntSeq_MPY-CORE_IntSeq»))

private def digitsNeg42 : SortIntSeq :=
  .«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 45
    (.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 52
      (.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 50
        .«.IntSeq_MPY-CORE_IntSeq»))

private def asciiA : SortIntSeq :=
  .«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 97
    .«.IntSeq_MPY-CORE_IntSeq»

private def asciiB : SortIntSeq :=
  .«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 98
    .«.IntSeq_MPY-CORE_IntSeq»

private def oneIntArg (i : SortInt) : SortVals :=
  .«_,__MPY-CORE_Vals_Val_Vals» (.inj_SortInt i)
    .«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals»

private def intK (i : SortInt) : SortK :=
  .kseq (.inj_SortInt i) .dotk

private def strK : SortK :=
  .kseq
    (.inj_SortStr
      (.«str(_)_MPY-CORE_Str_IntSeq» .«.IntSeq_MPY-CORE_IntSeq»))
    .dotk

-- Discriminating examples for all 13 public bridge definitions.
example : Proof.«_-Int_» 7 3 = 4 := rfl
example : Proof._andBool_ true false = false := rfl
example : Proof.«_>=Int_» (-2) 0 = false := rfl
example : Proof.«_<Int_» (-2) 4 = true := rfl

example :
    Proof.«allDigitCodes(_)_VERIFICATION_Bool_IntSeq» digits105 = true := rfl
example :
    Proof.«allDigitCodes(_)_VERIFICATION_Bool_IntSeq»
      (.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 47
        .«.IntSeq_MPY-CORE_IntSeq») = false := rfl

example :
    Proof.«applyBuiltin(_,_)_MPY-BUILTINS_Val_String_Vals»
      "str" (oneIntArg 105) =
      .inj_SortStr (.«str(_)_MPY-CORE_Str_IntSeq» digits105) := rfl
example :
    Proof.«applyBuiltin(_,_)_MPY-BUILTINS_Val_String_Vals»
      "str" (oneIntArg (-42)) =
      .inj_SortStr (.«str(_)_MPY-CORE_Str_IntSeq» digitsNeg42) := rfl

example :
    Proof.«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»
      "<" (.inj_SortInt (-2)) (.inj_SortInt 4) = true := rfl
example :
    Proof.«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»
      "<" (.inj_SortInt 4) (.inj_SortInt (-2)) = false := rfl

example :
    Proof.«applyUn(_,_)_MPY-CORE_Val_String_Val»
      "-" (.inj_SortInt (-3)) = .inj_SortInt 3 := rfl

example :
    Proof.«decimalCodes(_)_VERIFICATION_IntSeq_Int» 105 = digits105 := rfl
example :
    Proof.«decimalCodes(_)_VERIFICATION_IntSeq_Int» (-42) = digitsNeg42 := rfl

example :
    Proof.«definedProjectInt(_)_VERIFICATION_Bool_Val»
      (.inj_SortInt 8) = true := rfl
example :
    Proof.«definedProjectInt(_)_VERIFICATION_Bool_Val»
      (.inj_SortStr
        (.«str(_)_MPY-CORE_Str_IntSeq» .«.IntSeq_MPY-CORE_IntSeq»)) =
      false := rfl

example : Proof.isInt (intK 8) = true := rfl
example : Proof.isInt strK = false := rfl
example : Proof.projectIntTotal (.inj_SortInt (-17)) = -17 := rfl
example : Proof.«project:Int?» (intK 8) = some 8 := rfl
example : Proof.«project:Int?» strK = none := rfl

-- Full-symbol counterexamples outside the one source-used dispatcher case.
-- The frozen rules give "a" < "b" = true, not true = false, and int(3) = 3.
example :
    Proof.«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»
      "<"
      (.inj_SortStr (.«str(_)_MPY-CORE_Str_IntSeq» asciiA))
      (.inj_SortStr (.«str(_)_MPY-CORE_Str_IntSeq» asciiB)) = false := rfl
example :
    Proof.«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»
      "<"
      (.inj_SortStr (.«str(_)_MPY-CORE_Str_IntSeq» asciiA))
      (.inj_SortStr (.«str(_)_MPY-CORE_Str_IntSeq» asciiB)) ≠ true := by
  decide
example :
    Proof.«applyUn(_,_)_MPY-CORE_Val_String_Val»
      "not" (.inj_SortBool true) = .«noneV_MPY-CORE_Val» := rfl
example :
    Proof.«applyUn(_,_)_MPY-CORE_Val_String_Val»
      "not" (.inj_SortBool true) ≠ .inj_SortBool false := by
  intro h
  cases h
example :
    Proof.«applyBuiltin(_,_)_MPY-BUILTINS_Val_String_Vals»
      "int" (oneIntArg 3) = .«noneV_MPY-CORE_Val» := rfl
example :
    Proof.«applyBuiltin(_,_)_MPY-BUILTINS_Val_String_Vals»
      "int" (oneIntArg 3) ≠ .inj_SortInt 3 := by
  intro h
  cases h

-- Counterfactual convenient bridges; each is separated by an example from
-- the corresponding candidate definition on a source-reachable input.
private def badSub (x _ : SortInt) := x
private def badAnd (_ _ : SortBool) := true
private def badGE (_ _ : SortInt) := true
private def badLT (_ _ : SortInt) := false
private def badAllDigit (_ : SortIntSeq) := true
private def badBuiltin (_ : SortString) (_ : SortVals) :=
  SortVal.«noneV_MPY-CORE_Val»
private def badCmp (_ : SortString) (_ _ : SortVal) := false
private def badUn (_ : SortString) (v : SortVal) := v
private def badDecimal (_ : SortInt) :=
  SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 48
    .«.IntSeq_MPY-CORE_IntSeq»
private def badDefined (_ : SortVal) := true
private def badIsInt (_ : SortK) := true
private def badProject (_ : SortVal) : SortInt := 0
private def badProjectOption (_ : SortK) : Option SortInt := none

example : badSub 7 3 ≠ Proof.«_-Int_» 7 3 := by decide
example : badAnd true false ≠ Proof._andBool_ true false := by decide
example : badGE (-2) 0 ≠ Proof.«_>=Int_» (-2) 0 := by decide
example : badLT (-2) 4 ≠ Proof.«_<Int_» (-2) 4 := by decide
example :
    badAllDigit
      (.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 47
        .«.IntSeq_MPY-CORE_IntSeq») ≠
      Proof.«allDigitCodes(_)_VERIFICATION_Bool_IntSeq»
        (.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 47
          .«.IntSeq_MPY-CORE_IntSeq») := by decide
example :
    badBuiltin "str" (oneIntArg 105) ≠
      .inj_SortStr (.«str(_)_MPY-CORE_Str_IntSeq» digits105) := by
  intro h
  cases h
example :
    badCmp "<" (.inj_SortInt (-2)) (.inj_SortInt 4) ≠
      Proof.«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»
        "<" (.inj_SortInt (-2)) (.inj_SortInt 4) := by decide
example :
    badUn "-" (.inj_SortInt (-3)) ≠ .inj_SortInt 3 := by
  simp [badUn]
example :
    badDecimal 105 ≠ digits105 := by
  simp [badDecimal, digits105]
example :
    badDefined
      (.inj_SortStr
        (.«str(_)_MPY-CORE_Str_IntSeq» .«.IntSeq_MPY-CORE_IntSeq»)) ≠
      Proof.«definedProjectInt(_)_VERIFICATION_Bool_Val»
        (.inj_SortStr
          (.«str(_)_MPY-CORE_Str_IntSeq» .«.IntSeq_MPY-CORE_IntSeq»)) := by
  decide
example : badIsInt strK ≠ Proof.isInt strK := by decide
example :
    badProject (.inj_SortInt (-17)) ≠
      Proof.projectIntTotal (.inj_SortInt (-17)) := by decide
example :
    badProjectOption (intK 8) ≠ Proof.«project:Int?» (intK 8) := by decide

#reduce Proof.«decimalCodes(_)_VERIFICATION_IntSeq_Int» 105
#reduce Proof.«decimalCodes(_)_VERIFICATION_IntSeq_Int» (-42)
#reduce Proof.«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»
  "<" (.inj_SortInt (-2)) (.inj_SortInt 4)
