import Klean4MeanAbsoluteDeviation.Lemmas

namespace Proof

/- The generated target exposes the K sequence projection both as an
   Option-valued cast and through `isFloat`.  This is the exact structural
   domain of the frozen cast: a singleton K sequence containing a Float. -/
private def kleanProjectedFloat : SortK → Option SortFloat
  | SortK.kseq (SortKItem.inj_SortFloat value) SortK.dotk => some value
  | _ => none

private def kleanBoolInteger : SortBool → SortInt
  | false => 0
  | true => 1

/- MPY-STR's `seqConcat` recurrence over the frozen integer-code string
   representation. -/
private def kleanCodeSequenceAppend : SortIntSeq → SortIntSeq → SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», right => right
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head tail, right =>
      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq»
        head (kleanCodeSequenceAppend tail right)

/- K's `%Int` hook is t-modulus, not Lean's default Euclidean modulus.
   MPY-INT then applies this exact normalization twice to obtain Python's
   divisor-signed modulo. -/
private def kleanPythonModulo (left right : SortInt) : SortInt :=
  Int.tmod (Int.tmod left right + right) right

private def kleanPythonFloorDivide (left right : SortInt) : SortInt :=
  Int.tdiv (left - kleanPythonModulo left right) right

/- All Float values representable by immutable Base are binary64 values.
   These operations therefore implement the matching K binary64 hooks. -/
private def kleanIntegerFloat (value : SortInt) : SortFloat :=
  Float.ofInt value

private def kleanFloatModulo (left right : SortFloat) : SortFloat :=
  Float.sub left (Float.mul (Float.floor (Float.div left right)) right)

/- `applyBin` is partial for absent cases, zero integer divisors, and negative
   integer exponents.  Its Lean type is total, so every such divergent state
   uses this one fixed totalization. -/
private def kleanUndefinedBinaryResult : SortVal :=
  SortVal.«noneV_MPY-CORE_Val»

/- Frozen `projectFloat` is constrained only on actual Float values.  A fixed
   zero is used uniformly for every value outside that guarded domain. -/
private def kleanUndefinedProjectedFloat : SortFloat :=
  0.0

/- KORE symbol: LbladdF; frozen source obligations: rule-92241e2e54ad3adfe5140246eafc88d12ee532fcfc8c8c2e0d517f63bee4e6d7. Replace this stub with its honest total meaning from the frozen K semantics. -/
def addF : SortFloat → SortFloat → SortFloat :=
  Float.add

/- KORE symbol: LblapplyBin'LParUndsCommUndsCommUndsRParUnds'MPY-CORE'Unds'Val'Unds'String'Unds'Val'Unds'Val; frozen source obligations: rule-92241e2e54ad3adfe5140246eafc88d12ee532fcfc8c8c2e0d517f63bee4e6d7, rule-6f259967cef4b955723deaec2b3a84a45eb80e7f4eaa15e3db1588a7a25c310f. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» :
    SortString → SortVal → SortVal → SortVal
  | "+", SortVal.inj_SortInt left, SortVal.inj_SortInt right =>
      SortVal.inj_SortInt (left + right)
  | "+", SortVal.inj_SortInt left, SortVal.inj_SortBool right =>
      SortVal.inj_SortInt (left + kleanBoolInteger right)
  | "+", SortVal.inj_SortBool left, SortVal.inj_SortInt right =>
      SortVal.inj_SortInt (kleanBoolInteger left + right)
  | "+",
      SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» left),
      SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» right) =>
      SortVal.inj_SortStr
        (SortStr.«str(_)_MPY-CORE_Str_IntSeq»
          (kleanCodeSequenceAppend left right))
  | "+",
      SortVal.inj_SortIterable
        (SortIterable.inj_SortStr
          (SortStr.«str(_)_MPY-CORE_Str_IntSeq» left)),
      SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» right) =>
      SortVal.inj_SortStr
        (SortStr.«str(_)_MPY-CORE_Str_IntSeq»
          (kleanCodeSequenceAppend left right))
  | "+",
      SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» left),
      SortVal.inj_SortIterable
        (SortIterable.inj_SortStr
          (SortStr.«str(_)_MPY-CORE_Str_IntSeq» right)) =>
      SortVal.inj_SortStr
        (SortStr.«str(_)_MPY-CORE_Str_IntSeq»
          (kleanCodeSequenceAppend left right))
  | "+",
      SortVal.inj_SortIterable
        (SortIterable.inj_SortStr
          (SortStr.«str(_)_MPY-CORE_Str_IntSeq» left)),
      SortVal.inj_SortIterable
        (SortIterable.inj_SortStr
          (SortStr.«str(_)_MPY-CORE_Str_IntSeq» right)) =>
      SortVal.inj_SortStr
        (SortStr.«str(_)_MPY-CORE_Str_IntSeq»
          (kleanCodeSequenceAppend left right))
  | "-", SortVal.inj_SortInt left, SortVal.inj_SortInt right =>
      SortVal.inj_SortInt (left - right)
  | "*", SortVal.inj_SortInt left, SortVal.inj_SortInt right =>
      SortVal.inj_SortInt (left * right)
  | "%", SortVal.inj_SortInt left, SortVal.inj_SortInt right =>
      if right = 0 then kleanUndefinedBinaryResult
      else SortVal.inj_SortInt (kleanPythonModulo left right)
  | "//", SortVal.inj_SortInt left, SortVal.inj_SortInt right =>
      if right = 0 then kleanUndefinedBinaryResult
      else SortVal.inj_SortInt (kleanPythonFloorDivide left right)
  | "**", SortVal.inj_SortInt base, SortVal.inj_SortInt exponent =>
      if 0 ≤ exponent then
        SortVal.inj_SortInt (Int.pow base exponent.toNat)
      else
        kleanUndefinedBinaryResult
  | "/", SortVal.inj_SortInt left, SortVal.inj_SortFloat right =>
      SortVal.inj_SortFloat (Float.div (kleanIntegerFloat left) right)
  | "/", SortVal.inj_SortInt left, SortVal.inj_SortInt right =>
      SortVal.inj_SortFloat
        (Float.div (kleanIntegerFloat left) (kleanIntegerFloat right))
  | "%", SortVal.inj_SortFloat left, SortVal.inj_SortFloat right =>
      SortVal.inj_SortFloat (kleanFloatModulo left right)
  | "-", SortVal.inj_SortFloat left, SortVal.inj_SortFloat right =>
      SortVal.inj_SortFloat (Float.sub left right)
  | "/", SortVal.inj_SortFloat left, SortVal.inj_SortFloat right =>
      SortVal.inj_SortFloat (Float.div left right)
  | "+", SortVal.inj_SortFloat left, SortVal.inj_SortFloat right =>
      SortVal.inj_SortFloat (Float.add left right)
  | "*", SortVal.inj_SortFloat left, SortVal.inj_SortFloat right =>
      SortVal.inj_SortFloat (Float.mul left right)
  | "**", SortVal.inj_SortFloat left, SortVal.inj_SortFloat right =>
      SortVal.inj_SortFloat (Float.pow left right)
  | "**", SortVal.inj_SortInt left, SortVal.inj_SortFloat right =>
      SortVal.inj_SortFloat (Float.pow (kleanIntegerFloat left) right)
  | "**", SortVal.inj_SortFloat left, SortVal.inj_SortInt right =>
      SortVal.inj_SortFloat (Float.pow left (kleanIntegerFloat right))
  | "-", SortVal.inj_SortInt left, SortVal.inj_SortFloat right =>
      SortVal.inj_SortFloat (Float.sub (kleanIntegerFloat left) right)
  | "-", SortVal.inj_SortFloat left, SortVal.inj_SortInt right =>
      SortVal.inj_SortFloat (Float.sub left (kleanIntegerFloat right))
  | "+", SortVal.inj_SortInt left, SortVal.inj_SortFloat right =>
      SortVal.inj_SortFloat (Float.add (kleanIntegerFloat left) right)
  | "+", SortVal.inj_SortFloat left, SortVal.inj_SortInt right =>
      SortVal.inj_SortFloat (Float.add left (kleanIntegerFloat right))
  | "*", SortVal.inj_SortInt left, SortVal.inj_SortFloat right =>
      SortVal.inj_SortFloat (Float.mul (kleanIntegerFloat left) right)
  | "*", SortVal.inj_SortFloat left, SortVal.inj_SortInt right =>
      SortVal.inj_SortFloat (Float.mul left (kleanIntegerFloat right))
  | "/", SortVal.inj_SortFloat left, SortVal.inj_SortInt right =>
      SortVal.inj_SortFloat (Float.div left (kleanIntegerFloat right))
  | _, _, _ => kleanUndefinedBinaryResult

/- KORE symbol: LblisFloat; frozen source obligations: rule-97b32164f2b5a0f8a4f7d3358ad9ac8bcf9d1636304fa03d8f8eba850e64967e, rule-92241e2e54ad3adfe5140246eafc88d12ee532fcfc8c8c2e0d517f63bee4e6d7, rule-6f259967cef4b955723deaec2b3a84a45eb80e7f4eaa15e3db1588a7a25c310f. Replace this stub with its honest total meaning from the frozen K semantics. -/
def isFloat (value : SortK) : SortBool :=
  (kleanProjectedFloat value).isSome

/- KORE symbol: LblprojectFloat; frozen source obligations: rule-92241e2e54ad3adfe5140246eafc88d12ee532fcfc8c8c2e0d517f63bee4e6d7, rule-6f259967cef4b955723deaec2b3a84a45eb80e7f4eaa15e3db1588a7a25c310f. Replace this stub with its honest total meaning from the frozen K semantics. -/
def projectFloat : SortVal → SortFloat
  | SortVal.inj_SortFloat value => value
  | _ => kleanUndefinedProjectedFloat

/- KORE symbol: LblsubF; frozen source obligations: rule-6f259967cef4b955723deaec2b3a84a45eb80e7f4eaa15e3db1588a7a25c310f. Replace this stub with its honest total meaning from the frozen K semantics. -/
def subF : SortFloat → SortFloat → SortFloat :=
  Float.sub

/- KORE symbol: Lblproject'Coln'Float; frozen source obligations: rule-97b32164f2b5a0f8a4f7d3358ad9ac8bcf9d1636304fa03d8f8eba850e64967e. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «project:Float?» : SortK → Option SortFloat :=
  kleanProjectedFloat

private theorem kleanGuardedValueIsFloat
    (value : SortVal)
    (guard :
      isFloat
        (SortK.kseq ((@inj SortVal SortKItem) value) SortK.dotk) = true) :
    ∃ floatValue, value = SortVal.inj_SortFloat floatValue := by
  cases value <;>
    simp [isFloat, kleanProjectedFloat, inj] at guard ⊢

theorem final :
    Klean4MeanAbsoluteDeviation.Lemmas.targetStatement addF «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» isFloat projectFloat subF «project:Float?» := by
  constructor
  · intro value
    simp [«project:Float?», isFloat]
  constructor
  · intro value accumulator guard
    obtain ⟨floatValue, rfl⟩ := kleanGuardedValueIsFloat value guard
    rfl
  · intro mean value guard
    obtain ⟨floatValue, rfl⟩ := kleanGuardedValueIsFloat value guard
    rfl

end Proof
