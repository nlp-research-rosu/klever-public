import Klean114Minsubarraysum.Lemmas
import Init.Data.OfScientific

namespace FrozenDispatch

/- The minimized generated `SortVal` omits MPY's `str(IntSeq)` constructor.
   This private tag is an injective structural representation of that frozen
   constructor inside the otherwise unused keyword-wrapper shape. -/
private def stringTag : SortString := "__frozen_mpy_str__"

def stringVal (codes : SortIntSeq) : SortVal :=
  SortVal.«kwV(_,_)_MPY-CORE_Val_String_Val» stringTag
    (SortVal.«md5Obj(_)_MPY-BUILTINS_Val_IntSeq» codes)

def stringCodes : SortVal → Option SortIntSeq
  | SortVal.«kwV(_,_)_MPY-CORE_Val_String_Val» tag
      (SortVal.«md5Obj(_)_MPY-BUILTINS_Val_IntSeq» codes) =>
      if tag == stringTag then some codes else none
  | _ => none

def intSeqAppend : SortIntSeq → SortIntSeq → SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», right => right
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head tail, right =>
      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq»
        head (intSeqAppend tail right)

def intSeqLength : SortIntSeq → SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => 0
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ tail =>
      intSeqLength tail + 1

def valSeqLength : SortValSeq → SortInt
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => 0
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _ tail =>
      valSeqLength tail + 1

def intSeqToList : SortIntSeq → List SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => []
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head tail =>
      head :: intSeqToList tail

def charsToCodes : List Char → SortIntSeq
  | [] => SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
  | head :: tail =>
      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq»
        (Int.ofNat head.toNat) (charsToCodes tail)

def hostStringToCodes (value : String) : SortIntSeq :=
  charsToCodes value.toList

def intToCodes (value : SortInt) : SortIntSeq :=
  hostStringToCodes (toString value)

def codeIn (code : SortInt) : SortIntSeq → Bool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => false
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head tail =>
      code == head || codeIn code tail

def snocCode : SortIntSeq → SortInt → SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», code =>
      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq»
        code SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head tail, code =>
      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq»
        head (snocCode tail code)

def dedupFrom : SortIntSeq → SortIntSeq → SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», accumulated => accumulated
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head tail,
      accumulated =>
      if codeIn head accumulated then
        dedupFrom tail accumulated
      else
        dedupFrom tail (snocCode accumulated head)

def dedupCodes (codes : SortIntSeq) : SortIntSeq :=
  dedupFrom codes SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»

def rangeLength (low high step : SortInt) : Option SortInt :=
  if step > 0 then
    if high > low then some ((high - low + step - 1) / step) else some 0
  else if step < 0 then
    if high < low then some ((low - high - step - 1) / (0 - step)) else some 0
  else
    none

def sequenceLength : SortVal → Option SortInt
  | SortVal.inj_SortIterable
      (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» values) =>
      some (valSeqLength values)
  | SortVal.inj_SortIterable
      (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» values) =>
      some (valSeqLength values)
  | SortVal.inj_SortIterable
      (SortIterable.«rangeObj(_,_,_)_MPY-CORE_Iterable_Int_Int_Int»
        low high step) =>
      rangeLength low high step
  | SortVal.«setV(_)_MPY-SET_Val_IntSeq» codes =>
      some (intSeqLength codes)
  | value => (stringCodes value).map intSeqLength

def absInt (value : SortInt) : SortInt :=
  if value < 0 then 0 - value else value

def minInt (left right : SortInt) : SortInt :=
  if left < right then left else right

def maxInt (left right : SortInt) : SortInt :=
  if left < right then right else left

def minVals : SortInt → SortVals → Option SortInt
  | current, SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
      some current
  | current,
      SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortInt next) rest =>
      minVals (minInt current next) rest
  | _, _ => none

def maxVals : SortInt → SortVals → Option SortInt
  | current, SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
      some current
  | current,
      SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortInt next) rest =>
      maxVals (maxInt current next) rest
  | _, _ => none

def pyMod (left right : SortInt) : Option SortInt :=
  if right == 0 then none
  else some (Int.tmod (Int.tmod left right + right) right)

def floorDiv (left right : SortInt) : Option SortInt :=
  (pyMod left right).map fun remainder => Int.tdiv (left - remainder) right

def intPow (base exponent : SortInt) : Option SortInt :=
  if exponent < 0 then none else some (Int.pow base exponent.toNat)

def integralFloatToInt (value : SortFloat) : SortInt :=
  let bits := value.toBits.toNat
  let negative := (bits / (2 ^ 63)) % 2 == 1
  let exponentBits := (bits / (2 ^ 52)) % 2048
  let fraction := bits % (2 ^ 52)
  if exponentBits == 0 then
    0
  else if exponentBits == 2047 then
    0
  else
    let mantissa := 2 ^ 52 + fraction
    let exponent : Int := Int.ofNat exponentBits - 1023 - 52
    let magnitude :=
      if exponent < 0 then
        mantissa / (2 ^ (0 - exponent).toNat)
      else
        mantissa * (2 ^ exponent.toNat)
    if negative then 0 - Int.ofNat magnitude else Int.ofNat magnitude

def intToFloat (value : SortInt) : SortFloat :=
  Float.ofInt value

def floatMod (left right : SortFloat) : SortFloat :=
  left - Float.floor (left / right) * right

def floorValue : SortVal → Option SortInt
  | SortVal.inj_SortInt value => some value
  | SortVal.inj_SortFloat value =>
      some (integralFloatToInt (Float.floor value))
  | _ => none

def ceilValue : SortVal → Option SortInt
  | SortVal.inj_SortInt value => some value
  | SortVal.inj_SortFloat value =>
      some (integralFloatToInt (Float.ceil value))
  | _ => none

def truncateFloat (value : SortFloat) : SortInt :=
  if value < (0.0 : Float) then
    integralFloatToInt (Float.ceil value)
  else
    integralFloatToInt (Float.floor value)

def roundFloat (value : SortFloat) : SortInt :=
  let lower := Float.floor value
  if (value - lower) == (0.5 : Float) then
    let lowerInt := integralFloatToInt lower
    if lowerInt % 2 == 0 then lowerInt
    else integralFloatToInt (Float.ceil value)
  else
    integralFloatToInt (Float.floor (value + (0.5 : Float)))

def roundFloatDigits (value : SortFloat) (digits : SortInt) : SortFloat :=
  let scale :=
    if digits < 0 then
      Float.pow (10.0 : Float) (intToFloat digits)
    else
      intToFloat (Int.pow 10 digits.toNat)
  intToFloat (roundFloat (value * scale)) / scale

def intPartAcc : SortIntSeq → SortInt → SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», accumulated => accumulated
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 46 _, accumulated =>
      accumulated
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» code tail,
      accumulated =>
      intPartAcc tail (accumulated * 10 + (code - 48))

def intPart (codes : SortIntSeq) : SortInt :=
  intPartAcc codes 0

def fracAcc : SortIntSeq → SortInt → SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», accumulated => accumulated
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» code tail,
      accumulated =>
      fracAcc tail (accumulated * 10 + (code - 48))

def fracPart : SortIntSeq → SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => 0
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 46 tail =>
      fracAcc tail 0
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ tail =>
      fracPart tail

def fracScaleAcc : SortIntSeq → SortInt → SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», accumulated => accumulated
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ tail,
      accumulated =>
      fracScaleAcc tail (accumulated * 10)

def fracScale : SortIntSeq → SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => 1
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 46 tail =>
      fracScaleAcc tail 1
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ tail =>
      fracScale tail

def decimalCodesToFloat : SortIntSeq → Option SortFloat
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => none
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 45 tail =>
      (decimalCodesToFloat tail).map fun value => (0.0 : Float) - value
  | codes =>
      some
        (intToFloat (intPart codes) +
          intToFloat (fracPart codes) / intToFloat (fracScale codes))

def digitsToIntAcc : SortIntSeq → SortInt → SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», accumulated => accumulated
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» code tail,
      accumulated =>
      digitsToIntAcc tail (accumulated * 10 + (code - 48))

def digitsToInt (codes : SortIntSeq) : SortInt :=
  digitsToIntAcc codes 0

inductive EvalOp where
  | add
  | sub
  | mul
  | div
  | floorDiv
  | pow
  deriving BEq

def isDigitCode (code : SortInt) : Bool :=
  decide (48 ≤ code ∧ code ≤ 57)

def flushNumber (current : Option SortInt) (numbersRev : List SortInt) :
    List SortInt :=
  match current with
  | some number => number :: numbersRev
  | none => numbersRev

def tokenizeEval :
    List SortInt → Option SortInt → List SortInt → List EvalOp →
      List SortInt × List EvalOp
  | [], current, numbersRev, operatorsRev =>
      ((flushNumber current numbersRev).reverse, operatorsRev.reverse)
  | code :: rest, current, numbersRev, operatorsRev =>
      if isDigitCode code then
        let next :=
          match current with
          | some number => number * 10 + (code - 48)
          | none => code - 48
        tokenizeEval rest (some next) numbersRev operatorsRev
      else if code == 32 then
        tokenizeEval rest none (flushNumber current numbersRev) operatorsRev
      else
        let numbersRev := flushNumber current numbersRev
        match code, rest with
        | 42, 42 :: tail =>
            tokenizeEval tail none numbersRev (EvalOp.pow :: operatorsRev)
        | 47, 47 :: tail =>
            tokenizeEval tail none numbersRev (EvalOp.floorDiv :: operatorsRev)
        | 42, tail =>
            tokenizeEval tail none numbersRev (EvalOp.mul :: operatorsRev)
        | 47, tail =>
            tokenizeEval tail none numbersRev (EvalOp.div :: operatorsRev)
        | 43, tail =>
            tokenizeEval tail none numbersRev (EvalOp.add :: operatorsRev)
        | 45, tail =>
            tokenizeEval tail none numbersRev (EvalOp.sub :: operatorsRev)
        | _, tail => tokenizeEval tail none numbersRev operatorsRev

def passPower : List EvalOp → List SortInt → List EvalOp × List SortInt
  | [], numbers => ([], numbers)
  | _, [] => ([], [])
  | operator :: operators, number :: numbers =>
      let (remainingOperators, remainingNumbers) := passPower operators numbers
      match operator, remainingNumbers with
      | EvalOp.pow, next :: rest =>
          (remainingOperators, Int.pow number next.toNat :: rest)
      | EvalOp.pow, [] => (remainingOperators, [number])
      | other, rest => (other :: remainingOperators, number :: rest)

def atLevel (level : Bool) : EvalOp → Bool
  | EvalOp.mul | EvalOp.floorDiv | EvalOp.div => level
  | EvalOp.add | EvalOp.sub => !level
  | EvalOp.pow => false

def applyEvalOp (operator : EvalOp) (left right : SortInt) : SortInt :=
  match operator with
  | EvalOp.add => left + right
  | EvalOp.sub => left - right
  | EvalOp.mul => left * right
  | EvalOp.floorDiv => if right == 0 then left else left / right
  | EvalOp.div => left
  | EvalOp.pow => Int.pow left right.toNat

def passLevelGo (level : Bool) :
    SortInt → List EvalOp → List SortInt → List EvalOp → List SortInt →
      List EvalOp × List SortInt
  | current, [], _, operatorsRev, numbersRev =>
      (operatorsRev.reverse, (current :: numbersRev).reverse)
  | current, _, [], operatorsRev, numbersRev =>
      (operatorsRev.reverse, (current :: numbersRev).reverse)
  | current, operator :: operators, number :: numbers,
      operatorsRev, numbersRev =>
      if atLevel level operator then
        passLevelGo level (applyEvalOp operator current number)
          operators numbers operatorsRev numbersRev
      else
        passLevelGo level number operators numbers
          (operator :: operatorsRev) (current :: numbersRev)

def passLevel (level : Bool) :
    List EvalOp × List SortInt → List EvalOp × List SortInt
  | (operators, []) => (operators, [])
  | (operators, first :: rest) =>
      passLevelGo level first operators rest [] []

def evalArith (codes : SortIntSeq) : SortInt :=
  let (numbers, operators) := tokenizeEval (intSeqToList codes) none [] []
  let powered := passPower operators numbers
  let multiplied := passLevel true powered
  let added := passLevel false multiplied
  match added.2 with
  | first :: _ => first
  | [] => 0

def binaryCodes (value : SortInt) : SortIntSeq :=
  let magnitude := value.natAbs
  let digits := charsToCodes (Nat.toDigits 2 magnitude)
  let prefixCodes :=
    SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 48
      (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq»
        98 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
  if value < 0 then
    SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq»
      45 (intSeqAppend prefixCodes digits)
  else
    intSeqAppend prefixCodes digits

def applyBin : SortString → SortVal → SortVal → SortVal
  | "+", SortVal.inj_SortInt left, SortVal.inj_SortInt right =>
      SortVal.inj_SortInt (left + right)
  | "+", SortVal.inj_SortInt left, SortVal.inj_SortBool right =>
      SortVal.inj_SortInt (left + if right then 1 else 0)
  | "+", SortVal.inj_SortBool left, SortVal.inj_SortInt right =>
      SortVal.inj_SortInt ((if left then 1 else 0) + right)
  | "-", SortVal.inj_SortInt left, SortVal.inj_SortInt right =>
      SortVal.inj_SortInt (left - right)
  | "*", SortVal.inj_SortInt left, SortVal.inj_SortInt right =>
      SortVal.inj_SortInt (left * right)
  | "%", SortVal.inj_SortInt left, SortVal.inj_SortInt right =>
      match pyMod left right with
      | some result => SortVal.inj_SortInt result
      | none => SortVal.«noneV_MPY-CORE_Val»
  | "//", SortVal.inj_SortInt left, SortVal.inj_SortInt right =>
      match floorDiv left right with
      | some result => SortVal.inj_SortInt result
      | none => SortVal.«noneV_MPY-CORE_Val»
  | "**", SortVal.inj_SortInt left, SortVal.inj_SortInt right =>
      match intPow left right with
      | some result => SortVal.inj_SortInt result
      | none => SortVal.«noneV_MPY-CORE_Val»
  | "/", SortVal.inj_SortInt left, SortVal.inj_SortInt right =>
      SortVal.inj_SortFloat (intToFloat left / intToFloat right)
  | "/", SortVal.inj_SortInt left, SortVal.inj_SortFloat right =>
      SortVal.inj_SortFloat (intToFloat left / right)
  | "/", SortVal.inj_SortFloat left, SortVal.inj_SortInt right =>
      SortVal.inj_SortFloat (left / intToFloat right)
  | "%", SortVal.inj_SortFloat left, SortVal.inj_SortFloat right =>
      SortVal.inj_SortFloat (floatMod left right)
  | "-", SortVal.inj_SortFloat left, SortVal.inj_SortFloat right =>
      SortVal.inj_SortFloat (left - right)
  | "/", SortVal.inj_SortFloat left, SortVal.inj_SortFloat right =>
      SortVal.inj_SortFloat (left / right)
  | "+", SortVal.inj_SortFloat left, SortVal.inj_SortFloat right =>
      SortVal.inj_SortFloat (left + right)
  | "*", SortVal.inj_SortFloat left, SortVal.inj_SortFloat right =>
      SortVal.inj_SortFloat (left * right)
  | "**", SortVal.inj_SortFloat left, SortVal.inj_SortFloat right =>
      SortVal.inj_SortFloat (Float.pow left right)
  | "**", SortVal.inj_SortInt left, SortVal.inj_SortFloat right =>
      SortVal.inj_SortFloat (Float.pow (intToFloat left) right)
  | "**", SortVal.inj_SortFloat left, SortVal.inj_SortInt right =>
      SortVal.inj_SortFloat (Float.pow left (intToFloat right))
  | "-", SortVal.inj_SortInt left, SortVal.inj_SortFloat right =>
      SortVal.inj_SortFloat (intToFloat left - right)
  | "-", SortVal.inj_SortFloat left, SortVal.inj_SortInt right =>
      SortVal.inj_SortFloat (left - intToFloat right)
  | "+", SortVal.inj_SortInt left, SortVal.inj_SortFloat right =>
      SortVal.inj_SortFloat (intToFloat left + right)
  | "+", SortVal.inj_SortFloat left, SortVal.inj_SortInt right =>
      SortVal.inj_SortFloat (left + intToFloat right)
  | "*", SortVal.inj_SortInt left, SortVal.inj_SortFloat right =>
      SortVal.inj_SortFloat (intToFloat left * right)
  | "*", SortVal.inj_SortFloat left, SortVal.inj_SortInt right =>
      SortVal.inj_SortFloat (left * intToFloat right)
  | "+", left, right =>
      match stringCodes left, stringCodes right with
      | some leftCodes, some rightCodes =>
          stringVal (intSeqAppend leftCodes rightCodes)
      | _, _ => SortVal.«noneV_MPY-CORE_Val»
  | _, _, _ => SortVal.«noneV_MPY-CORE_Val»

def applyBuiltin : SortString → SortVals → SortVal
  | "len", SortVals.«_,__MPY-CORE_Vals_Val_Vals» object
      SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
      match sequenceLength object with
      | some result => SortVal.inj_SortInt result
      | none => SortVal.«noneV_MPY-CORE_Val»
  | "set", SortVals.«_,__MPY-CORE_Vals_Val_Vals» object
      SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
      match stringCodes object with
      | some codes => SortVal.«setV(_)_MPY-SET_Val_IntSeq» (dedupCodes codes)
      | none => SortVal.«noneV_MPY-CORE_Val»
  | "abs", SortVals.«_,__MPY-CORE_Vals_Val_Vals»
      (SortVal.inj_SortInt value)
      SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
      SortVal.inj_SortInt (absInt value)
  | "abs", SortVals.«_,__MPY-CORE_Vals_Val_Vals»
      (SortVal.inj_SortFloat value)
      SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
      SortVal.inj_SortFloat (Float.abs value)
  | "max", SortVals.«_,__MPY-CORE_Vals_Val_Vals»
      (SortVal.inj_SortInt first) rest =>
      match maxVals first rest with
      | some result => SortVal.inj_SortInt result
      | none => SortVal.«noneV_MPY-CORE_Val»
  | "min", SortVals.«_,__MPY-CORE_Vals_Val_Vals»
      (SortVal.inj_SortInt first) rest =>
      match minVals first rest with
      | some result => SortVal.inj_SortInt result
      | none => SortVal.«noneV_MPY-CORE_Val»
  | "bin", SortVals.«_,__MPY-CORE_Vals_Val_Vals»
      (SortVal.inj_SortInt value)
      SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
      stringVal (binaryCodes value)
  | "int", SortVals.«_,__MPY-CORE_Vals_Val_Vals» value
      SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
      match value with
      | SortVal.inj_SortInt integer => SortVal.inj_SortInt integer
      | SortVal.inj_SortFloat float =>
          SortVal.inj_SortInt (truncateFloat float)
      | other =>
          match stringCodes other with
          | some
              (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq»
                code SortIntSeq.«.IntSeq_MPY-CORE_IntSeq») =>
              if 48 ≤ code ∧ code ≤ 57 then
                SortVal.inj_SortInt (code - 48)
              else SortVal.«noneV_MPY-CORE_Val»
          | some codes =>
              if intSeqLength codes ≥ 2 then
                SortVal.inj_SortInt (digitsToInt codes)
              else SortVal.«noneV_MPY-CORE_Val»
          | none => SortVal.«noneV_MPY-CORE_Val»
  | "ord", SortVals.«_,__MPY-CORE_Vals_Val_Vals» value
      SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
      match stringCodes value with
      | some
          (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq»
            code SortIntSeq.«.IntSeq_MPY-CORE_IntSeq») =>
          SortVal.inj_SortInt code
      | _ => SortVal.«noneV_MPY-CORE_Val»
  | "chr", SortVals.«_,__MPY-CORE_Vals_Val_Vals»
      (SortVal.inj_SortInt code)
      SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
      if 0 ≤ code ∧ code < 128 then
        stringVal
          (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq»
            code SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
      else SortVal.«noneV_MPY-CORE_Val»
  | "str", SortVals.«_,__MPY-CORE_Vals_Val_Vals» value
      SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
      match value with
      | SortVal.inj_SortInt integer => stringVal (intToCodes integer)
      | other =>
          match stringCodes other with
          | some codes => stringVal codes
          | none => SortVal.«noneV_MPY-CORE_Val»
  | "zip", SortVals.«_,__MPY-CORE_Vals_Val_Vals»
      (SortVal.inj_SortIterable
        (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» left))
      (SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortIterable
          (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» right))
        SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals») =>
      SortVal.inj_SortIterable
        (SortIterable.«zipObj(_,_)_MPY-CORE_Iterable_ValSeq_ValSeq»
          left right)
  | "zip", SortVals.«_,__MPY-CORE_Vals_Val_Vals» left
      (SortVals.«_,__MPY-CORE_Vals_Val_Vals» right
        SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals») =>
      match stringCodes left, stringCodes right with
      | some leftCodes, some rightCodes =>
          SortVal.inj_SortIterable
            (SortIterable.«zipObjS(_,_)_MPY-CORE_Iterable_IntSeq_IntSeq»
              leftCodes rightCodes)
      | _, _ => SortVal.«noneV_MPY-CORE_Val»
  | "range", SortVals.«_,__MPY-CORE_Vals_Val_Vals»
      (SortVal.inj_SortInt stop)
      SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
      SortVal.inj_SortIterable
        (SortIterable.«rangeObj(_,_,_)_MPY-CORE_Iterable_Int_Int_Int»
          0 stop 1)
  | "range", SortVals.«_,__MPY-CORE_Vals_Val_Vals»
      (SortVal.inj_SortInt start)
      (SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortInt stop)
        SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals») =>
      SortVal.inj_SortIterable
        (SortIterable.«rangeObj(_,_,_)_MPY-CORE_Iterable_Int_Int_Int»
          start stop 1)
  | "range", SortVals.«_,__MPY-CORE_Vals_Val_Vals»
      (SortVal.inj_SortInt start)
      (SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortInt stop)
        (SortVals.«_,__MPY-CORE_Vals_Val_Vals»
          (SortVal.inj_SortInt step)
          SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals»)) =>
      if step == 0 then SortVal.«noneV_MPY-CORE_Val»
      else
        SortVal.inj_SortIterable
          (SortIterable.«rangeObj(_,_,_)_MPY-CORE_Iterable_Int_Int_Int»
            start stop step)
  | "eval", SortVals.«_,__MPY-CORE_Vals_Val_Vals» value
      SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
      match stringCodes value with
      | some codes => SortVal.inj_SortInt (evalArith codes)
      | none => SortVal.«noneV_MPY-CORE_Val»
  | "isinstance", SortVals.«_,__MPY-CORE_Vals_Val_Vals» value
      (SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.«typeV(_)_MPY-CORE_Val_String» typeName)
        SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals») =>
      if typeName == "int" then
        SortVal.inj_SortBool
          (match value with
          | SortVal.inj_SortInt _ => true
          | _ => false)
      else if typeName == "str" then
        SortVal.inj_SortBool (stringCodes value).isSome
      else
        SortVal.«noneV_MPY-CORE_Val»
  | "float", SortVals.«_,__MPY-CORE_Vals_Val_Vals» value
      SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
      match value with
      | SortVal.inj_SortInt integer =>
          SortVal.inj_SortFloat (intToFloat integer)
      | SortVal.inj_SortFloat float => SortVal.inj_SortFloat float
      | other =>
          match stringCodes other with
          | some codes =>
              match decimalCodesToFloat codes with
              | some result => SortVal.inj_SortFloat result
              | none => SortVal.«noneV_MPY-CORE_Val»
          | none => SortVal.«noneV_MPY-CORE_Val»
  | "floor", SortVals.«_,__MPY-CORE_Vals_Val_Vals» value
      SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
      match floorValue value with
      | some result => SortVal.inj_SortInt result
      | none => SortVal.«noneV_MPY-CORE_Val»
  | "ceil", SortVals.«_,__MPY-CORE_Vals_Val_Vals» value
      SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
      match ceilValue value with
      | some result => SortVal.inj_SortInt result
      | none => SortVal.«noneV_MPY-CORE_Val»
  | "round", SortVals.«_,__MPY-CORE_Vals_Val_Vals»
      (SortVal.inj_SortFloat value)
      SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
      SortVal.inj_SortInt (roundFloat value)
  | "round", SortVals.«_,__MPY-CORE_Vals_Val_Vals»
      (SortVal.inj_SortFloat value)
      (SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortInt digits)
        SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals») =>
      SortVal.inj_SortFloat (roundFloatDigits value digits)
  | _, _ => SortVal.«noneV_MPY-CORE_Val»

end FrozenDispatch
