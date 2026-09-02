import Proof

def kOf (value : SortVal) : SortK :=
  SortK.kseq ((@inj SortVal SortKItem) value) SortK.dotk

def intNeg : SortVal := SortVal.inj_SortInt (-7)
def intPos : SortVal := SortVal.inj_SortInt 42
def boolFalse : SortVal := SortVal.inj_SortBool false
def boolTrue : SortVal := SortVal.inj_SortBool true
def floatVal : SortVal := SortVal.inj_SortFloat 1.5
def otherVal : SortVal := SortVal.«typeV(_)_MPY-CORE_Val_String» "int"

#eval (Proof._andBool_ false false, Proof._andBool_ false true,
  Proof._andBool_ true false, Proof._andBool_ true true)
#eval (Proof.notBool_ false, Proof.notBool_ true)

#eval (Proof.isInt (kOf intNeg), Proof.isBool (kOf intNeg),
  Proof.isFloat (kOf intNeg))
#eval (Proof.isInt (kOf boolTrue), Proof.isBool (kOf boolTrue),
  Proof.isFloat (kOf boolTrue))
#eval (Proof.isInt (kOf floatVal), Proof.isBool (kOf floatVal),
  Proof.isFloat (kOf floatVal))
#eval (Proof.isInt (kOf otherVal), Proof.isBool (kOf otherVal),
  Proof.isFloat (kOf otherVal))

#eval (Proof.«integralV(_)_VERIFICATION-SYNTAX_Bool_Val» intNeg,
  Proof.«integralV(_)_VERIFICATION-SYNTAX_Bool_Val» boolFalse,
  Proof.«integralV(_)_VERIFICATION-SYNTAX_Bool_Val» floatVal,
  Proof.«integralV(_)_VERIFICATION-SYNTAX_Bool_Val» otherVal)
#eval (Proof.«floatV(_)_VERIFICATION-SYNTAX_Bool_Val» intNeg,
  Proof.«floatV(_)_VERIFICATION-SYNTAX_Bool_Val» boolFalse,
  Proof.«floatV(_)_VERIFICATION-SYNTAX_Bool_Val» floatVal,
  Proof.«floatV(_)_VERIFICATION-SYNTAX_Bool_Val» otherVal)

#eval (Proof.intLikeTotal intNeg, Proof.intLikeTotal intPos,
  Proof.intLikeTotal boolFalse, Proof.intLikeTotal boolTrue)
#eval (Proof.«intOf(_)_MPY-BUILTINS_Int_Val» intNeg,
  Proof.«intOf(_)_MPY-BUILTINS_Int_Val» intPos,
  Proof.«intOf(_)_MPY-BUILTINS_Int_Val» boolFalse,
  Proof.«intOf(_)_MPY-BUILTINS_Int_Val» boolTrue)

#eval (Proof.«project:Int» (kOf intNeg), Proof.projectIntTotal intNeg,
  Proof.«project:Int?» (kOf intNeg))
#eval (Proof.«project:Bool» (kOf boolFalse), Proof.projectBoolTotal boolFalse,
  Proof.«project:Bool?» (kOf boolFalse))
#eval (Proof.«project:Float» (kOf floatVal), Proof.projectFloatTotal floatVal,
  Proof.«project:Float?» (kOf floatVal))

def nonValueContinuation : SortK :=
  SortK.kseq ((@inj SortVal SortKItem) intPos)
    (SortK.kseq ((@inj SortVal SortKItem) boolTrue) SortK.dotk)

#eval (Proof.isInt nonValueContinuation, Proof.isBool nonValueContinuation,
  Proof.isFloat nonValueContinuation)
#eval (Proof.«project:Int?» nonValueContinuation,
  Proof.«project:Bool?» nonValueContinuation,
  Proof.«project:Float?» nonValueContinuation)

example : Proof.intLikeTotal intPos = 42 := rfl
example : Proof.«intOf(_)_MPY-BUILTINS_Int_Val» intPos = 42 := rfl
example : Proof.intLikeTotal boolFalse = 0 := rfl
example : Proof.intLikeTotal boolTrue = 1 := rfl
example : Proof.«project:Int» (kOf intNeg) = Proof.projectIntTotal intNeg := rfl
example : Proof.«project:Bool» (kOf boolFalse) = Proof.projectBoolTotal boolFalse := rfl
example : Proof.«project:Float» (kOf floatVal) = Proof.projectFloatTotal floatVal := rfl

def badIntOf (_ : SortVal) : SortInt := 0

example :
    ¬ (∀ (V : SortVal)
        (_h : Proof.«integralV(_)_VERIFICATION-SYNTAX_Bool_Val» V = true),
        badIntOf V = Proof.intLikeTotal V) := by
  intro claimed
  have wrong := claimed intPos rfl
  have badValue : badIntOf intPos = 0 := rfl
  have honestValue : Proof.intLikeTotal intPos = 42 := rfl
  have zeroEqFortyTwo : (0 : Int) = 42 :=
    badValue.symm.trans (wrong.trans honestValue)
  exact (by decide : (0 : Int) ≠ 42) zeroEqFortyTwo

def coordinatedBadProjectInt (_ : SortK) : SortInt := 0
def coordinatedBadProjectIntTotal (_ : SortVal) : SortInt := 0

-- The associated relational obligation alone accepts these coordinated
-- constants, even though they do not implement the Int projection.
example :
    ∀ (V : SortVal)
      (_h : Proof._andBool_
        (Proof._andBool_ (Proof.isInt (kOf V))
          (Proof.notBool_ (Proof.isBool (kOf V))))
        (Proof.notBool_ (Proof.isFloat (kOf V))) = true),
      coordinatedBadProjectInt (kOf V) =
        coordinatedBadProjectIntTotal V := by
  intro V h
  rfl

example : coordinatedBadProjectInt (kOf intPos) ≠ 42 := by decide

def badIsInt (_ : SortK) : SortBool := false

example :
    ¬ (∀ (V : SortVal),
        ((Proof.«project:Int?» (kOf V)).isSome = true) ↔
          ((badIsInt (kOf V) = true) ∧ True)) := by
  intro claimed
  have consequence := (claimed intPos).mp (by rfl)
  exact (by decide : false ≠ true) consequence.1
