import Klean35MaxElement.Lemmas

namespace Operational

/- Honest total models of the frozen K symbols.  Every helper name is distinct
   from the generated binding names declared in Proof.lean. -/

def valItemImpl : SortVal → SortKItem
  | SortVal.inj_SortBool b => SortKItem.inj_SortBool b
  | SortVal.inj_SortFloat f => SortKItem.inj_SortFloat f
  | SortVal.inj_SortInt i => SortKItem.inj_SortInt i
  | SortVal.inj_SortIterable it => SortKItem.inj_SortIterable it
  | SortVal.inj_SortStr s => SortKItem.inj_SortStr s
  | v => SortKItem.inj_SortVal v

theorem injValItem_eq (v : SortVal) :
    ((@inj SortVal SortKItem) v) = valItemImpl v := by
  cases v <;> rfl

def boolAndImpl (a b : SortBool) : SortBool := a && b
def boolOrImpl (a b : SortBool) : SortBool := a || b
def intGreaterImpl (a b : SortInt) : SortBool := decide (a > b)

def boolProjectionOptImpl : SortK → Option SortBool
  | SortK.kseq (SortKItem.inj_SortBool b) SortK.dotk => some b
  | _ => none

def floatProjectionOptImpl : SortK → Option SortFloat
  | SortK.kseq (SortKItem.inj_SortFloat f) SortK.dotk => some f
  | _ => none

def intProjectionOptImpl : SortK → Option SortInt
  | SortK.kseq (SortKItem.inj_SortInt i) SortK.dotk => some i
  | _ => none

def strProjectionOptImpl : SortK → Option SortStr
  | SortK.kseq (SortKItem.inj_SortStr s) SortK.dotk => some s
  | _ => none

def isBoolImpl (k : SortK) : SortBool := (boolProjectionOptImpl k).isSome
def isFloatImpl (k : SortK) : SortBool := (floatProjectionOptImpl k).isSome
def isIntImpl (k : SortK) : SortBool := (intProjectionOptImpl k).isSome
def isStrImpl (k : SortK) : SortBool := (strProjectionOptImpl k).isSome

def boolProjectionImpl (k : SortK) : SortBool :=
  (boolProjectionOptImpl k).getD false

def floatProjectionImpl (k : SortK) : SortFloat :=
  (floatProjectionOptImpl k).getD 0.0

def intProjectionImpl (k : SortK) : SortInt :=
  (intProjectionOptImpl k).getD 0

def emptyStrImpl : SortStr :=
  SortStr.«str(_)_MPY-CORE_Str_IntSeq» SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»

def strProjectionImpl (k : SortK) : SortStr :=
  (strProjectionOptImpl k).getD emptyStrImpl

def boolTotalProjectionImpl : SortVal → SortBool
  | SortVal.inj_SortBool b => b
  | _ => false

def floatTotalProjectionImpl : SortVal → SortFloat
  | SortVal.inj_SortFloat f => f
  | _ => 0.0

def intTotalProjectionImpl : SortVal → SortInt
  | SortVal.inj_SortInt i => i
  | _ => 0

def strTotalProjectionImpl : SortVal → SortStr
  | SortVal.inj_SortStr s => s
  | _ => emptyStrImpl

def codesFromStrImpl : SortStr → SortIntSeq
  | SortStr.«str(_)_MPY-CORE_Str_IntSeq» cs => cs

def intSeqEqualImpl : SortIntSeq → SortIntSeq → SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => true
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» a as,
      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» b bs =>
      decide (a = b) && intSeqEqualImpl as bs
  | _, _ => false

def strLessImpl : SortIntSeq → SortIntSeq → SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => false
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»,
      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ _ => true
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ _,
      SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => false
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» a as,
      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» b bs =>
      if a < b then true else if a > b then false else strLessImpl as bs

def strPrefixImpl : SortIntSeq → SortIntSeq → SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _ => true
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ _,
      SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => false
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» a as,
      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» b bs =>
      decide (a = b) && strPrefixImpl as bs

def strContainsImpl (pattern : SortIntSeq) : SortIntSeq → SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» =>
      strPrefixImpl pattern SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
  | haystack@(SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ rest) =>
      if strPrefixImpl pattern haystack then true else strContainsImpl pattern rest

def codeInImpl (code : SortInt) : SortIntSeq → SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => false
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head tail =>
      decide (code = head) || codeInImpl code tail

def subsetCodesImpl : SortIntSeq → SortIntSeq → SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _ => true
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head tail, other =>
      codeInImpl head other && subsetCodesImpl tail other

def sameSetImpl (a b : SortIntSeq) : SortBool :=
  subsetCodesImpl a b && subsetCodesImpl b a

/- `==K` is syntactic equality of generated K terms. -/
noncomputable def valTermEqualImpl (a b : SortVal) : SortBool := by
  classical
  exact decide (a = b)

noncomputable def valSeqTermEqualImpl (a b : SortValSeq) : SortBool := by
  classical
  exact decide (a = b)

def valSeqLengthImpl : SortValSeq → Nat
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => 0
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _ tail => valSeqLengthImpl tail + 1

noncomputable def dictFindImpl
    (keys values : SortValSeq) (key : SortVal) : Option SortVal :=
  match keys, values with
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» candidate keyTail,
      SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» value valueTail =>
      if valTermEqualImpl candidate key then some value
      else dictFindImpl keyTail valueTail key
  | _, _ => none

noncomputable def dictHasKeyImpl (keys : SortValSeq) (key : SortVal) : SortBool :=
  match keys with
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => false
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» candidate tail =>
      if valTermEqualImpl candidate key then true else dictHasKeyImpl tail key

noncomputable def dictSubsetImpl
    (keys values otherKeys otherValues : SortValSeq) : SortBool :=
  match keys, values with
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => true
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» key keyTail,
      SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» value valueTail =>
      dictHasKeyImpl otherKeys key &&
        (match dictFindImpl otherKeys otherValues key with
         | some found => valTermEqualImpl found value
         | none => false) &&
        dictSubsetImpl keyTail valueTail otherKeys otherValues
  | _, _ => false

noncomputable def dictEqualImpl
    (keys₁ values₁ keys₂ values₂ : SortValSeq) : SortBool :=
  decide (valSeqLengthImpl keys₁ = valSeqLengthImpl keys₂) &&
    dictSubsetImpl keys₁ values₁ keys₂ values₂

def boolAsIntImpl (b : SortBool) : SortInt := if b then 1 else 0

/- Exact binary64 decoding for the frozen ltIF/ltFI/eqIF hooks. -/
structure FloatDyadicImpl where
  mantissa : Int
  exponent : Int

def floatSignBitImpl (f : SortFloat) : SortBool :=
  ((f.toBits.toNat / (2 ^ 63)) % 2) = 1

def floatDyadicImpl (f : SortFloat) : Option FloatDyadicImpl :=
  let bits := f.toBits.toNat
  let exponentBits := (bits / (2 ^ 52)) % (2 ^ 11)
  let fraction := bits % (2 ^ 52)
  if exponentBits = (2 ^ 11) - 1 then none
  else
    let magnitude := if exponentBits = 0 then fraction else (2 ^ 52) + fraction
    let signedMantissa : Int :=
      if floatSignBitImpl f then -(Int.ofNat magnitude) else Int.ofNat magnitude
    let exponent : Int :=
      if exponentBits = 0 then -1074 else Int.ofNat exponentBits - 1075
    some ⟨signedMantissa, exponent⟩

def dyadicLessThanIntImpl (d : FloatDyadicImpl) (i : SortInt) : SortBool :=
  if d.exponent ≥ 0 then
    decide (d.mantissa * Int.ofNat (2 ^ d.exponent.toNat) < i)
  else
    decide (d.mantissa < i * Int.ofNat (2 ^ (-d.exponent).toNat))

def intLessThanDyadicImpl (i : SortInt) (d : FloatDyadicImpl) : SortBool :=
  if d.exponent ≥ 0 then
    decide (i < d.mantissa * Int.ofNat (2 ^ d.exponent.toNat))
  else
    decide (i * Int.ofNat (2 ^ (-d.exponent).toNat) < d.mantissa)

def intEqualDyadicImpl (i : SortInt) (d : FloatDyadicImpl) : SortBool :=
  if d.exponent ≥ 0 then
    decide (i = d.mantissa * Int.ofNat (2 ^ d.exponent.toNat))
  else
    decide (i * Int.ofNat (2 ^ (-d.exponent).toNat) = d.mantissa)

def floatLessThanIntImpl (f : SortFloat) (i : SortInt) : SortBool :=
  match floatDyadicImpl f with
  | some d => dyadicLessThanIntImpl d i
  | none => if f.isNaN then false else floatSignBitImpl f

def intLessThanFloatImpl (i : SortInt) (f : SortFloat) : SortBool :=
  match floatDyadicImpl f with
  | some d => intLessThanDyadicImpl i d
  | none => if f.isNaN then false else !floatSignBitImpl f

def intEqualFloatImpl (i : SortInt) (f : SortFloat) : SortBool :=
  match floatDyadicImpl f with
  | some d => intEqualDyadicImpl i d
  | none => false

def floatLessImpl (a b : SortFloat) : SortBool := decide (a < b)
def floatGreaterImpl (a b : SortFloat) : SortBool := decide (b < a)
def floatEqualImpl (a b : SortFloat) : SortBool := a == b

/- K 7.1.293 FLOAT.max is max-number, not NaN-propagating: if exactly
   one operand is NaN it returns the non-NaN operand.  Equal signed zeros select
   +0, and otherwise the numerically greater operand wins. -/
def floatMaxImpl (a b : SortFloat) : SortFloat :=
  if a.isNaN then b
  else if b.isNaN then a
  else if a < b then b
  else if b < a then a
  else if a.toBits = 0x8000000000000000 && b.toBits = 0 then b
  else if b.toBits = 0x8000000000000000 && a.toBits = 0 then a
  else a

def numericImpl : SortVal → SortBool
  | SortVal.inj_SortInt _ => true
  | SortVal.inj_SortBool _ => true
  | SortVal.inj_SortFloat _ => true
  | _ => false

def numericViewImpl : SortVal → SortNumericView
  | SortVal.inj_SortInt i => SortNumericView.«nInt(_)_VERIFICATION_NumericView_Int» i
  | SortVal.inj_SortBool b => SortNumericView.«nBool(_)_VERIFICATION_NumericView_Bool» b
  | SortVal.inj_SortFloat f => SortNumericView.«nFloat(_)_VERIFICATION_NumericView_Float» f
  | v => SortNumericView.«nOther(_)_VERIFICATION_NumericView_Val» v

def numericGreaterImpl : SortNumericView → SortNumericView → SortBool
  | SortNumericView.«nInt(_)_VERIFICATION_NumericView_Int» i,
      SortNumericView.«nInt(_)_VERIFICATION_NumericView_Int» j => intGreaterImpl i j
  | SortNumericView.«nInt(_)_VERIFICATION_NumericView_Int» i,
      SortNumericView.«nBool(_)_VERIFICATION_NumericView_Bool» b => intGreaterImpl i (boolAsIntImpl b)
  | SortNumericView.«nBool(_)_VERIFICATION_NumericView_Bool» b,
      SortNumericView.«nInt(_)_VERIFICATION_NumericView_Int» i => intGreaterImpl (boolAsIntImpl b) i
  | SortNumericView.«nBool(_)_VERIFICATION_NumericView_Bool» a,
      SortNumericView.«nBool(_)_VERIFICATION_NumericView_Bool» b => intGreaterImpl (boolAsIntImpl a) (boolAsIntImpl b)
  | SortNumericView.«nFloat(_)_VERIFICATION_NumericView_Float» a,
      SortNumericView.«nFloat(_)_VERIFICATION_NumericView_Float» b => floatGreaterImpl a b
  | SortNumericView.«nInt(_)_VERIFICATION_NumericView_Int» i,
      SortNumericView.«nFloat(_)_VERIFICATION_NumericView_Float» f => floatLessThanIntImpl f i
  | SortNumericView.«nFloat(_)_VERIFICATION_NumericView_Float» f,
      SortNumericView.«nInt(_)_VERIFICATION_NumericView_Int» i => intLessThanFloatImpl i f
  | SortNumericView.«nBool(_)_VERIFICATION_NumericView_Bool» b,
      SortNumericView.«nFloat(_)_VERIFICATION_NumericView_Float» f => floatLessThanIntImpl f (boolAsIntImpl b)
  | SortNumericView.«nFloat(_)_VERIFICATION_NumericView_Float» f,
      SortNumericView.«nBool(_)_VERIFICATION_NumericView_Bool» b => intLessThanFloatImpl (boolAsIntImpl b) f
  | _, _ => false

def intCompareImpl (operator : SortString) (a b : SortInt) : SortBool :=
  match operator with
  | "<" => decide (a < b)
  | "<=" => decide (a ≤ b)
  | ">" => decide (a > b)
  | ">=" => decide (a ≥ b)
  | "==" => decide (a = b)
  | "!=" => decide (a ≠ b)
  | _ => false

def floatCompareImpl (operator : SortString) (a b : SortFloat) : SortBool :=
  match operator with
  | "<" => floatLessImpl a b
  | "<=" => !floatGreaterImpl a b
  | ">" => floatGreaterImpl a b
  | ">=" => !floatLessImpl a b
  | "==" => floatEqualImpl a b
  | "!=" => !floatEqualImpl a b
  | _ => false

def intFloatCompareImpl (operator : SortString) (i : SortInt) (f : SortFloat) : SortBool :=
  match operator with
  | "<" => intLessThanFloatImpl i f
  | "<=" => !floatLessThanIntImpl f i
  | ">" => floatLessThanIntImpl f i
  | ">=" => !intLessThanFloatImpl i f
  | "==" => intEqualFloatImpl i f
  | "!=" => !intEqualFloatImpl i f
  | _ => false

def floatIntCompareImpl (operator : SortString) (f : SortFloat) (i : SortInt) : SortBool :=
  match operator with
  | "<" => floatLessThanIntImpl f i
  | "<=" => !intLessThanFloatImpl i f
  | ">" => intLessThanFloatImpl i f
  | ">=" => !floatLessThanIntImpl f i
  | "==" => intEqualFloatImpl i f
  | "!=" => !intEqualFloatImpl i f
  | _ => false

def strCompareImpl (operator : SortString) (a b : SortIntSeq) : SortBool :=
  match operator with
  | "==" => intSeqEqualImpl a b
  | "!=" => !intSeqEqualImpl a b
  | "in" => strContainsImpl a b
  | "not in" => !strContainsImpl a b
  | "<" => strLessImpl a b
  | ">" => strLessImpl b a
  | "<=" => !strLessImpl b a
  | ">=" => !strLessImpl a b
  | _ => false

/- Complete rule table over the Base-representable Val universe.  The final arm
   totalizes only combinations for which frozen MPY has no applyCmp rule. -/
noncomputable def cmpDispatchImpl
    (operator : SortString) (left right : SortVal) : SortBool :=
  match left, right with
  | _, SortVal.«noneV_MPY-CORE_Val» =>
      match operator with
      | "==" | "is" =>
          match left with
          | SortVal.«noneV_MPY-CORE_Val» => true
          | _ => false
      | "!=" | "is not" =>
          match left with
          | SortVal.«noneV_MPY-CORE_Val» => false
          | _ => true
      | _ => false
  | SortVal.inj_SortInt a, SortVal.inj_SortInt b => intCompareImpl operator a b
  | SortVal.inj_SortFloat a, SortVal.inj_SortFloat b => floatCompareImpl operator a b
  | SortVal.inj_SortBool a, SortVal.inj_SortBool b =>
      if operator = "==" then decide (a = b)
      else if operator = "!=" then decide (a ≠ b)
      else intCompareImpl operator (boolAsIntImpl a) (boolAsIntImpl b)
  | SortVal.inj_SortBool a, SortVal.inj_SortInt b => intCompareImpl operator (boolAsIntImpl a) b
  | SortVal.inj_SortInt a, SortVal.inj_SortBool b => intCompareImpl operator a (boolAsIntImpl b)
  | SortVal.inj_SortInt i, SortVal.inj_SortFloat f => intFloatCompareImpl operator i f
  | SortVal.inj_SortFloat f, SortVal.inj_SortInt i => floatIntCompareImpl operator f i
  | SortVal.inj_SortBool b, SortVal.inj_SortFloat f => intFloatCompareImpl operator (boolAsIntImpl b) f
  | SortVal.inj_SortFloat f, SortVal.inj_SortBool b => floatIntCompareImpl operator f (boolAsIntImpl b)
  | SortVal.inj_SortStr a, SortVal.inj_SortStr b =>
      strCompareImpl operator (codesFromStrImpl a) (codesFromStrImpl b)
  | SortVal.inj_SortIterable (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» a),
      SortVal.inj_SortIterable (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» b) =>
      if operator = "==" then valSeqTermEqualImpl a b
      else if operator = "!=" then !valSeqTermEqualImpl a b else false
  | SortVal.inj_SortIterable (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» a),
      SortVal.inj_SortIterable (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» b) =>
      if operator = "==" then valSeqTermEqualImpl a b
      else if operator = "!=" then !valSeqTermEqualImpl a b else false
  | SortVal.«setV(_)_MPY-SET_Val_IntSeq» a, SortVal.«setV(_)_MPY-SET_Val_IntSeq» b =>
      if operator = "==" then sameSetImpl a b else false
  | SortVal.«dictV(_,_)_MPY-DICT_Val_ValSeq_ValSeq» keys₁ values₁,
      SortVal.«dictV(_,_)_MPY-DICT_Val_ValSeq_ValSeq» keys₂ values₂ =>
      if operator = "==" then dictEqualImpl keys₁ values₁ keys₂ values₂ else false
  | _, _ => false

end Operational
