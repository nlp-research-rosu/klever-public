import Klean94Skjkasdkd.Lemmas

/-!
Executable interpretations of the generated MPY value universe and of the
operator-dispatch tables frozen under `/reference/k-proof`.

The generated sorts did not carry equality instances.  These mutually-derived
instances are structural, so the MPY rules written with K's `==K` can be
implemented without an ad-hoc or theorem-specific equality relation.
-/

deriving instance BEq for SortExc
deriving instance BEq for SortExcCell
deriving instance BEq for SortEnvCell
deriving instance BEq for SortExitCodeCell
deriving instance BEq for SortGeneratedCounterCell
deriving instance BEq for SortHeapLocCell
deriving instance BEq for SortIntSeq
deriving instance BEq for SortOptInt
deriving instance BEq for SortScopeLocCell
deriving instance BEq for SortParamNames
deriving instance BEq for SortCellVars
deriving instance BEq for SortFreeVars
deriving instance BEq for SortParams

deriving instance BEq for
  SortApplyK, SortBound, SortCmpOp, SortEntries, SortEntry, SortExpr,
  SortExprs, SortGeneratedTopCell, SortHeapCell, SortIndex, SortIterable,
  SortK, SortKCell, SortKItem, SortList, SortMap, SortModule, SortRetCell,
  SortRetState, SortScopesCell, SortStackCell, SortStmt, SortStmts, SortVal,
  SortValSeq, SortVals

namespace Operational

def noneValue : SortVal :=
  SortVal.«noneV_MPY-CORE_Val»

def boolAsInteger (b : SortBool) : SortInt :=
  if b then 1 else 0

def intValue (i : SortInt) : SortVal :=
  SortVal.inj_SortInt i

def floatValue (f : SortFloat) : SortVal :=
  SortVal.inj_SortFloat f

def intToFloatModel : SortInt → SortFloat
  | .ofNat n => Float.ofScientific n false 0
  | .negSucc n => -Float.ofScientific (n + 1) false 0

def pythonModulo (x y : SortInt) : SortInt :=
  Int.tmod (Int.tmod x y + y) y

def integerPower (base exponent : SortInt) : SortVal :=
  if exponent < 0 then noneValue
  else intValue (Int.pow base exponent.toNat)

def integerBinary (op : SortString) (x y : SortInt) : SortVal :=
  if op == "+" then intValue (x + y)
  else if op == "-" then intValue (x - y)
  else if op == "*" then intValue (x * y)
  else if op == "%" then intValue (pythonModulo x y)
  else if op == "//" then intValue (Int.tdiv (x - pythonModulo x y) y)
  else if op == "/" then floatValue (intToFloatModel x / intToFloatModel y)
  else if op == "**" then integerPower x y
  else noneValue

def floatBinary (op : SortString) (x y : SortFloat) : SortVal :=
  if op == "+" then floatValue (x + y)
  else if op == "-" then floatValue (x - y)
  else if op == "*" then floatValue (x * y)
  else if op == "/" then floatValue (x / y)
  else if op == "%" then floatValue (x - Float.floor (x / y) * y)
  else if op == "**" then floatValue (Float.pow x y)
  else noneValue

def integerFloatBinary (op : SortString) (x : SortInt) (y : SortFloat) : SortVal :=
  if op == "+" then floatValue (intToFloatModel x + y)
  else if op == "-" then floatValue (intToFloatModel x - y)
  else if op == "*" then floatValue (intToFloatModel x * y)
  else if op == "/" then floatValue (intToFloatModel x / y)
  else if op == "**" then floatValue (Float.pow (intToFloatModel x) y)
  else noneValue

def floatIntegerBinary (op : SortString) (x : SortFloat) (y : SortInt) : SortVal :=
  if op == "+" then floatValue (x + intToFloatModel y)
  else if op == "-" then floatValue (x - intToFloatModel y)
  else if op == "*" then floatValue (x * intToFloatModel y)
  else if op == "/" then floatValue (x / intToFloatModel y)
  else if op == "**" then floatValue (Float.pow x (intToFloatModel y))
  else noneValue

/- The selected generated sort universe contains every MPY value production
used by the target except `Str`; Klean omitted that unreferenced subsort and
there is therefore no Lean constructor on which a string dispatch arm could
match.  All representable arms of the frozen applyBin table are below. -/
def applyBinaryModel (op : SortString) (left right : SortVal) : SortVal :=
  match left, right with
  | .inj_SortInt x, .inj_SortInt y =>
      integerBinary op x y
  | .inj_SortInt x, .inj_SortBool y =>
      integerBinary op x (boolAsInteger y)
  | .inj_SortBool x, .inj_SortInt y =>
      integerBinary op (boolAsInteger x) y
  | .inj_SortBool x, .inj_SortBool y =>
      integerBinary op (boolAsInteger x) (boolAsInteger y)
  | .inj_SortFloat x, .inj_SortFloat y =>
      floatBinary op x y
  | .inj_SortInt x, .inj_SortFloat y =>
      integerFloatBinary op x y
  | .inj_SortFloat x, .inj_SortInt y =>
      floatIntegerBinary op x y
  | .inj_SortBool x, .inj_SortFloat y =>
      integerFloatBinary op (boolAsInteger x) y
  | .inj_SortFloat x, .inj_SortBool y =>
      floatIntegerBinary op x (boolAsInteger y)
  | _, _ => noneValue

def intSequenceLength : SortIntSeq → Nat
  | .«.IntSeq_MPY-CORE_IntSeq» => 0
  | .«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ rest =>
      intSequenceLength rest + 1

def codeMember (code : SortInt) : SortIntSeq → Bool
  | .«.IntSeq_MPY-CORE_IntSeq» => false
  | .«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head rest =>
      code == head || codeMember code rest

def codeSubset : SortIntSeq → SortIntSeq → Bool
  | .«.IntSeq_MPY-CORE_IntSeq», _ => true
  | .«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head rest, other =>
      codeMember head other && codeSubset rest other

def sameCodeSet (left right : SortIntSeq) : Bool :=
  codeSubset left right && codeSubset right left

def valueSequenceLength : SortValSeq → Nat
  | .«.ValSeq_MPY-CORE_ValSeq» => 0
  | .«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _ rest =>
      valueSequenceLength rest + 1

def dictionaryLookup (key : SortVal) : SortValSeq → SortValSeq → Option SortVal
  | .«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» firstKey remainingKeys,
    .«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» firstValue remainingValues =>
      if firstKey == key then some firstValue
      else dictionaryLookup key remainingKeys remainingValues
  | _, _ => none

def dictionarySubset : SortValSeq → SortValSeq → SortValSeq → SortValSeq → Bool
  | .«.ValSeq_MPY-CORE_ValSeq», .«.ValSeq_MPY-CORE_ValSeq», _, _ => true
  | .«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» key remainingKeys,
    .«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» value remainingValues,
    otherKeys, otherValues =>
      match dictionaryLookup key otherKeys otherValues with
      | some otherValue =>
          otherValue == value &&
            dictionarySubset remainingKeys remainingValues otherKeys otherValues
      | none => false
  | _, _, _, _ => false

def dictionaryEqual
    (keys₁ values₁ keys₂ values₂ : SortValSeq) : Bool :=
  valueSequenceLength keys₁ == valueSequenceLength keys₂ &&
    dictionarySubset keys₁ values₁ keys₂ values₂

def integerCompare (op : SortString) (x y : SortInt) : SortBool :=
  if op == "<" then decide (x < y)
  else if op == "<=" then decide (x ≤ y)
  else if op == ">" then decide (x > y)
  else if op == ">=" then decide (x ≥ y)
  else if op == "==" then x == y
  else if op == "!=" then !(x == y)
  else false

def floatCompare (op : SortString) (x y : SortFloat) : SortBool :=
  if op == "<" then decide (x < y)
  else if op == ">" then decide (y < x)
  else if op == "<=" then !(decide (y < x))
  else if op == ">=" then !(decide (x < y))
  else if op == "==" then x == y
  else if op == "!=" then !(x == y)
  else false

def floatSignificand (f : SortFloat) : Nat :=
  let bits := Float.toBits f
  let rawExponent := ((bits >>> 52) &&& 0x7ff).toNat
  let fraction := (bits &&& 0xfffffffffffff).toNat
  if rawExponent == 0 then fraction else 2 ^ 52 + fraction

def floatBinaryExponent (f : SortFloat) : Int :=
  let rawExponent := ((Float.toBits f >>> 52) &&& 0x7ff).toNat
  if rawExponent == 0 then -1074
  else (Int.ofNat rawExponent) - 1023 - 52

def floatNegative (f : SortFloat) : Bool :=
  ((Float.toBits f >>> 63) &&& 1) == 1

def floatMagnitudeQuotientRemainder (f : SortFloat) : Nat × Nat :=
  let significand := floatSignificand f
  let exponent := floatBinaryExponent f
  if exponent ≥ 0 then
    (significand * 2 ^ exponent.toNat, 0)
  else
    let denominator := 2 ^ (-exponent).toNat
    (significand / denominator, significand % denominator)

def floatFloorInteger (f : SortFloat) : SortInt :=
  let qr := floatMagnitudeQuotientRemainder f
  if floatNegative f then
    if qr.2 == 0 then -Int.ofNat qr.1 else -Int.ofNat (qr.1 + 1)
  else
    Int.ofNat qr.1

def floatCeilingInteger (f : SortFloat) : SortInt :=
  let qr := floatMagnitudeQuotientRemainder f
  if floatNegative f then
    -Int.ofNat qr.1
  else
    if qr.2 == 0 then Int.ofNat qr.1 else Int.ofNat (qr.1 + 1)

def intFloatEqual (integer : SortInt) (floating : SortFloat) : SortBool :=
  if Float.isFinite floating then
    let qr := floatMagnitudeQuotientRemainder floating
    qr.2 == 0 &&
      (if floatNegative floating then -Int.ofNat qr.1 else Int.ofNat qr.1) == integer
  else
    intToFloatModel integer == floating

def floatLessInteger (floating : SortFloat) (integer : SortInt) : SortBool :=
  if Float.isFinite floating then floatFloorInteger floating < integer
  else decide (floating < intToFloatModel integer)

def integerLessFloat (integer : SortInt) (floating : SortFloat) : SortBool :=
  if Float.isFinite floating then integer < floatCeilingInteger floating
  else decide (intToFloatModel integer < floating)

def integerFloatCompare
    (op : SortString) (integer : SortInt) (floating : SortFloat) : SortBool :=
  if op == "==" then intFloatEqual integer floating
  else if op == "!=" then !(intFloatEqual integer floating)
  else if op == "<" then integerLessFloat integer floating
  else if op == ">" then floatLessInteger floating integer
  else if op == "<=" then !(floatLessInteger floating integer)
  else if op == ">=" then !(integerLessFloat integer floating)
  else false

def floatIntegerCompare
    (op : SortString) (floating : SortFloat) (integer : SortInt) : SortBool :=
  if op == "==" then intFloatEqual integer floating
  else if op == "!=" then !(intFloatEqual integer floating)
  else if op == "<" then floatLessInteger floating integer
  else if op == ">" then integerLessFloat integer floating
  else if op == "<=" then !(integerLessFloat integer floating)
  else if op == ">=" then !(floatLessInteger floating integer)
  else false

def applyComparisonModel (op : SortString) (left right : SortVal) : SortBool :=
  match left, right with
  | value, .«noneV_MPY-CORE_Val» =>
      if op == "==" || op == "is" then value == noneValue
      else if op == "!=" || op == "is not" then !(value == noneValue)
      else false
  | .inj_SortInt x, .inj_SortInt y =>
      integerCompare op x y
  | .inj_SortInt x, .inj_SortBool y =>
      integerCompare op x (boolAsInteger y)
  | .inj_SortBool x, .inj_SortInt y =>
      integerCompare op (boolAsInteger x) y
  | .inj_SortBool x, .inj_SortBool y =>
      integerCompare op (boolAsInteger x) (boolAsInteger y)
  | .inj_SortFloat x, .inj_SortFloat y =>
      floatCompare op x y
  | .inj_SortInt x, .inj_SortFloat y =>
      integerFloatCompare op x y
  | .inj_SortFloat x, .inj_SortInt y =>
      floatIntegerCompare op x y
  | .inj_SortBool x, .inj_SortFloat y =>
      integerFloatCompare op (boolAsInteger x) y
  | .inj_SortFloat x, .inj_SortBool y =>
      floatIntegerCompare op x (boolAsInteger y)
  | .inj_SortIterable (.«list(_)_MPY-CORE_Iterable_ValSeq» x),
    .inj_SortIterable (.«list(_)_MPY-CORE_Iterable_ValSeq» y) =>
      if op == "==" then x == y
      else if op == "!=" then !(x == y)
      else false
  | .inj_SortIterable (.«tuple(_)_MPY-CORE_Iterable_ValSeq» x),
    .inj_SortIterable (.«tuple(_)_MPY-CORE_Iterable_ValSeq» y) =>
      if op == "==" then x == y
      else if op == "!=" then !(x == y)
      else false
  | .«setV(_)_MPY-SET_Val_IntSeq» x, .«setV(_)_MPY-SET_Val_IntSeq» y =>
      if op == "==" then sameCodeSet x y else false
  | .«dictV(_,_)_MPY-DICT_Val_ValSeq_ValSeq» keys₁ values₁,
    .«dictV(_,_)_MPY-DICT_Val_ValSeq_ValSeq» keys₂ values₂ =>
      if op == "==" then dictionaryEqual keys₁ values₁ keys₂ values₂ else false
  | _, _ => false

end Operational
