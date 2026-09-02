import Klean135CanArrange.Lemmas

namespace Proof

/- Structural equality used by frozen `==K` rules.  Direct float comparison
   below uses the frozen Float hooks instead. -/
local instance operationalStructuralFloatBEq : BEq SortFloat where
  beq left right := left.toBits == right.toBits

deriving instance BEq for SortExc, SortIntSeq, SortStr, SortExcCell, SortEnvCell,
  SortExitCodeCell, SortGeneratedCounterCell, SortHeapLocCell,
  SortOptInt, SortScopeLocCell, SortParamNames, SortCellVars, SortFreeVars,
  SortParams

deriving instance BEq for SortApplyK, SortBound, SortCmpOp, SortEntries,
  SortEntry, SortExpr, SortExprs, SortGeneratedTopCell, SortHeapCell, SortIndex,
  SortIterable, SortK, SortKCell, SortKItem, SortList, SortMap, SortModule,
  SortRetCell, SortRetState, SortScopesCell, SortStackCell, SortStmt, SortStmts,
  SortVal, SortValSeq, SortVals

def operationalIsNumericVal : SortVal → SortBool
  | .inj_SortBool _ => true
  | .inj_SortFloat _ => true
  | .inj_SortInt _ => true
  | _ => false

def operationalIsStrVal : SortVal → SortBool
  | .inj_SortStr _ => true
  | _ => false

def operationalOrderablePair (left right : SortVal) : SortBool :=
  (operationalIsNumericVal left && operationalIsNumericVal right) ||
    (operationalIsStrVal left && operationalIsStrVal right)

def operationalBoolAsInt : SortBool → SortInt
  | false => 0
  | true => 1

/- These are exactly the frozen `<Float`, `>Float`, and `==Float` hooks on
   Base's binary64 SortFloat representation. -/
def operationalFloatLt (left right : SortFloat) : SortBool :=
  decide (left < right)

def operationalFloatGt (left right : SortFloat) : SortBool :=
  decide (right < left)

/- Exact binary64 decomposition for MPY-FLOAT's unbounded Int/Float bridge. -/
def operationalFiniteFloatParts
    (value : SortFloat) : SortBool × Nat × SortInt :=
  let bits := value.toBits.toNat
  let negative := decide (bits / (2 ^ 63) = 1)
  let storedExponent := (bits / (2 ^ 52)) % (2 ^ 11)
  let fraction := bits % (2 ^ 52)
  if storedExponent = 0 then
    (negative, fraction, -1074)
  else
    (negative, (2 ^ 52) + fraction, Int.ofNat storedExponent - 1075)

def operationalSplitFloatMagnitude
    (significand : Nat) (binaryExponent : SortInt) : Nat × Nat :=
  if binaryExponent ≥ 0 then
    (significand * (2 ^ binaryExponent.toNat), 0)
  else
    let denominator := 2 ^ (-binaryExponent).toNat
    (significand / denominator, significand % denominator)

def operationalFloorFiniteFloat (value : SortFloat) : SortInt :=
  let (negative, significand, binaryExponent) := operationalFiniteFloatParts value
  let (quotient, remainder) :=
    operationalSplitFloatMagnitude significand binaryExponent
  if negative then
    -Int.ofNat (quotient + if remainder = 0 then 0 else 1)
  else
    Int.ofNat quotient

def operationalCeilFiniteFloat (value : SortFloat) : SortInt :=
  let (negative, significand, binaryExponent) := operationalFiniteFloatParts value
  let (quotient, remainder) :=
    operationalSplitFloatMagnitude significand binaryExponent
  if negative then
    -Int.ofNat quotient
  else
    Int.ofNat (quotient + if remainder = 0 then 0 else 1)

def operationalNegativeFloat (value : SortFloat) : SortBool :=
  decide (value.toBits.toNat / (2 ^ 63) = 1)

/- MPFR's binary64 Int2Float hook overflows at the round-to-nearest midpoint
   between the largest finite value and infinity. -/
def operationalIntFloatOverflowBoundary : SortInt :=
  (2 : SortInt) ^ 1024 - (2 : SortInt) ^ 970

def operationalIntRoundsToPositiveInfinity (integer : SortInt) : SortBool :=
  decide (integer ≥ operationalIntFloatOverflowBoundary)

def operationalIntRoundsToNegativeInfinity (integer : SortInt) : SortBool :=
  decide (integer ≤ -operationalIntFloatOverflowBoundary)

def operationalLtFI (value : SortFloat) (integer : SortInt) : SortBool :=
  if value.isFinite then
    decide (operationalFloorFiniteFloat value < integer)
  else if value.isNaN then
    false
  else if operationalNegativeFloat value then
    !(operationalIntRoundsToNegativeInfinity integer)
  else
    false

def operationalLtIF (integer : SortInt) (value : SortFloat) : SortBool :=
  if value.isFinite then
    decide (integer < operationalCeilFiniteFloat value)
  else if value.isNaN then
    false
  else if operationalNegativeFloat value then
    false
  else
    !(operationalIntRoundsToPositiveInfinity integer)

def operationalEqIF (integer : SortInt) (value : SortFloat) : SortBool :=
  if value.isFinite then
    decide (
      operationalFloorFiniteFloat value = operationalCeilFiniteFloat value ∧
      operationalFloorFiniteFloat value = integer)
  else if value.isNaN then
    false
  else if operationalNegativeFloat value then
    operationalIntRoundsToNegativeInfinity integer
  else
    operationalIntRoundsToPositiveInfinity integer

def operationalCompareInts
    (operator : SortString) (left right : SortInt) : SortBool :=
  match operator with
  | "<" => decide (left < right)
  | "<=" => decide (left ≤ right)
  | ">" => decide (left > right)
  | ">=" => decide (left ≥ right)
  | "==" => decide (left = right)
  | "!=" => decide (left ≠ right)
  | _ => false

def operationalCompareFloats
    (operator : SortString) (left right : SortFloat) : SortBool :=
  match operator with
  | "<" => operationalFloatLt left right
  | "<=" => !(operationalFloatGt left right)
  | ">" => operationalFloatGt left right
  | ">=" => !(operationalFloatLt left right)
  | "==" => Float.beq left right
  | "!=" => !(Float.beq left right)
  | _ => false

def operationalCompareIntFloat
    (operator : SortString) (integer : SortInt) (value : SortFloat) : SortBool :=
  match operator with
  | "<" => operationalLtIF integer value
  | "<=" => !(operationalLtFI value integer)
  | ">" => operationalLtFI value integer
  | ">=" => !(operationalLtIF integer value)
  | "==" => operationalEqIF integer value
  | "!=" => !(operationalEqIF integer value)
  | _ => false

def operationalCompareFloatInt
    (operator : SortString) (value : SortFloat) (integer : SortInt) : SortBool :=
  match operator with
  | "<" => operationalLtFI value integer
  | "<=" => !(operationalLtIF integer value)
  | ">" => operationalLtIF integer value
  | ">=" => !(operationalLtFI value integer)
  | "==" => operationalEqIF integer value
  | "!=" => !(operationalEqIF integer value)
  | _ => false

def operationalStrPrefix : SortIntSeq → SortIntSeq → SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _ => true
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ _,
      SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => false
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» leftHead leftTail,
      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» rightHead rightTail =>
      decide (leftHead = rightHead) && operationalStrPrefix leftTail rightTail

def operationalStrContains (pattern : SortIntSeq) : SortIntSeq → SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» =>
      operationalStrPrefix pattern SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head tail =>
      if operationalStrPrefix pattern
          (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head tail) then
        true
      else
        operationalStrContains pattern tail

def operationalStrLt : SortIntSeq → SortIntSeq → SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»,
      SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => false
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»,
      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ _ => true
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ _,
      SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => false
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» leftHead leftTail,
      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» rightHead rightTail =>
      if leftHead < rightHead then true
      else if leftHead > rightHead then false
      else operationalStrLt leftTail rightTail

def operationalCompareStrings
    (operator : SortString) (left right : SortIntSeq) : SortBool :=
  match operator with
  | "==" => left == right
  | "!=" => !(left == right)
  | "in" => operationalStrContains left right
  | "not in" => !(operationalStrContains left right)
  | "<" => operationalStrLt left right
  | ">" => operationalStrLt right left
  | "<=" => !(operationalStrLt right left)
  | ">=" => !(operationalStrLt left right)
  | _ => false

def operationalOrderGe : SortVal → SortVal → SortBool
  | .inj_SortInt left, .inj_SortInt right => decide (left ≥ right)
  | .inj_SortBool left, .inj_SortBool right =>
      decide (operationalBoolAsInt left ≥ operationalBoolAsInt right)
  | .inj_SortBool left, .inj_SortInt right =>
      decide (operationalBoolAsInt left ≥ right)
  | .inj_SortInt left, .inj_SortBool right =>
      decide (left ≥ operationalBoolAsInt right)
  | .inj_SortFloat left, .inj_SortFloat right => !(operationalFloatLt left right)
  | .inj_SortInt left, .inj_SortFloat right => !(operationalLtIF left right)
  | .inj_SortFloat left, .inj_SortInt right => !(operationalLtFI left right)
  | .inj_SortBool left, .inj_SortFloat right =>
      !(operationalLtIF (operationalBoolAsInt left) right)
  | .inj_SortFloat left, .inj_SortBool right =>
      !(operationalLtFI left (operationalBoolAsInt right))
  | .inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» left),
      .inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» right) =>
      !(operationalStrLt left right)
  | .inj_SortStr _, _ => false
  | _, .inj_SortStr _ => false
  | _, _ => false

def operationalCodeIn (code : SortInt) : SortIntSeq → SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => false
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head tail =>
      decide (code = head) || operationalCodeIn code tail

def operationalSubsetCodes : SortIntSeq → SortIntSeq → SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _ => true
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head tail, right =>
      operationalCodeIn head right && operationalSubsetCodes tail right

def operationalSameSet (left right : SortIntSeq) : SortBool :=
  operationalSubsetCodes left right && operationalSubsetCodes right left

def operationalValSeqLength : SortValSeq → Nat
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => 0
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _ tail =>
      operationalValSeqLength tail + 1

def operationalHasDictKey (key : SortVal) : SortValSeq → SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => false
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» head tail =>
      (head == key) || operationalHasDictKey key tail

def operationalGetDictValue
    (key : SortVal) : SortValSeq → SortValSeq → Option SortVal
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» candidate keyTail,
      SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» value valueTail =>
      if candidate == key then some value
      else operationalGetDictValue key keyTail valueTail
  | _, _ => none

def operationalDictSubset :
    SortValSeq → SortValSeq → SortValSeq → SortValSeq → SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq»,
      SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _, _ => true
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» key keyTail,
      SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» value valueTail,
      rightKeys, rightValues =>
      operationalHasDictKey key rightKeys &&
        match operationalGetDictValue key rightKeys rightValues with
        | some found =>
            (found == value) &&
              operationalDictSubset keyTail valueTail rightKeys rightValues
        | none => false
  | _, _, _, _ => false

def operationalDictEq
    (leftKeys leftValues rightKeys rightValues : SortValSeq) : SortBool :=
  decide (operationalValSeqLength leftKeys = operationalValSeqLength rightKeys) &&
    operationalDictSubset leftKeys leftValues rightKeys rightValues

def operationalIsNone : SortVal → SortBool
  | SortVal.«noneV_MPY-CORE_Val» => true
  | _ => false

/- Complete frozen applyCmp table relative to the immutable Base value universe. -/
def operationalApplyCmp
    (operator : SortString) (left right : SortVal) : SortBool :=
  if operator = ">=" then
    if operationalOrderablePair left right then operationalOrderGe left right
    else false
  else
    match operator, left, right with
    | "==", value, SortVal.«noneV_MPY-CORE_Val» => operationalIsNone value
    | "!=", value, SortVal.«noneV_MPY-CORE_Val» => !(operationalIsNone value)
    | "is", value, SortVal.«noneV_MPY-CORE_Val» => operationalIsNone value
    | "is not", value, SortVal.«noneV_MPY-CORE_Val» => !(operationalIsNone value)
    | op, .inj_SortInt leftInt, .inj_SortInt rightInt =>
        operationalCompareInts op leftInt rightInt
    | op, .inj_SortBool leftBool, .inj_SortBool rightBool =>
        operationalCompareInts op (operationalBoolAsInt leftBool)
          (operationalBoolAsInt rightBool)
    | op, .inj_SortBool leftBool, .inj_SortInt rightInt =>
        operationalCompareInts op (operationalBoolAsInt leftBool) rightInt
    | op, .inj_SortInt leftInt, .inj_SortBool rightBool =>
        operationalCompareInts op leftInt (operationalBoolAsInt rightBool)
    | op, .inj_SortFloat leftFloat, .inj_SortFloat rightFloat =>
        operationalCompareFloats op leftFloat rightFloat
    | op, .inj_SortInt leftInt, .inj_SortFloat rightFloat =>
        operationalCompareIntFloat op leftInt rightFloat
    | op, .inj_SortFloat leftFloat, .inj_SortInt rightInt =>
        operationalCompareFloatInt op leftFloat rightInt
    | op, .inj_SortBool leftBool, .inj_SortFloat rightFloat =>
        operationalCompareIntFloat op (operationalBoolAsInt leftBool) rightFloat
    | op, .inj_SortFloat leftFloat, .inj_SortBool rightBool =>
        operationalCompareFloatInt op leftFloat (operationalBoolAsInt rightBool)
    | op,
        .inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» leftCodes),
        .inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» rightCodes) =>
        operationalCompareStrings op leftCodes rightCodes
    | "==", .inj_SortIterable
          (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» leftValues),
        .inj_SortIterable
          (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» rightValues) =>
        leftValues == rightValues
    | "!=", .inj_SortIterable
          (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» leftValues),
        .inj_SortIterable
          (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» rightValues) =>
        !(leftValues == rightValues)
    | "==", .inj_SortIterable
          (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» leftValues),
        .inj_SortIterable
          (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» rightValues) =>
        leftValues == rightValues
    | "!=", .inj_SortIterable
          (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» leftValues),
        .inj_SortIterable
          (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» rightValues) =>
        !(leftValues == rightValues)
    | "==", SortVal.«setV(_)_MPY-SET_Val_IntSeq» leftCodes,
        SortVal.«setV(_)_MPY-SET_Val_IntSeq» rightCodes =>
        operationalSameSet leftCodes rightCodes
    | "==", SortVal.«dictV(_,_)_MPY-DICT_Val_ValSeq_ValSeq» leftKeys leftValues,
        SortVal.«dictV(_,_)_MPY-DICT_Val_ValSeq_ValSeq» rightKeys rightValues =>
        operationalDictEq leftKeys leftValues rightKeys rightValues
    | _, _, _ => false

/- KORE symbol: LblapplyCmp'LParUndsCommUndsCommUndsRParUnds'MPY-CORE'Unds'Bool'Unds'String'Unds'Val'Unds'Val; frozen source obligations: rule-2fd1883e1dbbdfd9717b1321447ac996a4962a56a877371e6e1bee92b5b19050. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»
    (operator : SortString) (left right : SortVal) : SortBool :=
  operationalApplyCmp operator left right
/- KORE symbol: LblorderGe'LParUndsCommUndsRParUnds'VERIFICATION-BASE'Unds'Bool'Unds'Val'Unds'Val; frozen source obligations: rule-2fd1883e1dbbdfd9717b1321447ac996a4962a56a877371e6e1bee92b5b19050. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «orderGe(_,_)_VERIFICATION-BASE_Bool_Val_Val»
    (left right : SortVal) : SortBool := operationalOrderGe left right
/- KORE symbol: LblorderablePair'LParUndsCommUndsRParUnds'VERIFICATION-BASE'Unds'Bool'Unds'Val'Unds'Val; frozen source obligations: rule-2fd1883e1dbbdfd9717b1321447ac996a4962a56a877371e6e1bee92b5b19050. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «orderablePair(_,_)_VERIFICATION-BASE_Bool_Val_Val»
    (left right : SortVal) : SortBool := operationalOrderablePair left right

theorem final :
    Klean135CanArrange.Lemmas.targetStatement «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» «orderGe(_,_)_VERIFICATION-BASE_Bool_Val_Val» «orderablePair(_,_)_VERIFICATION-BASE_Bool_Val_Val» := by
  unfold Klean135CanArrange.Lemmas.targetStatement
  intro W V h
  unfold «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»
  unfold «orderGe(_,_)_VERIFICATION-BASE_Bool_Val_Val»
  unfold «orderablePair(_,_)_VERIFICATION-BASE_Bool_Val_Val» at h
  unfold operationalApplyCmp
  rw [if_pos rfl]
  rw [if_pos h]

end Proof
