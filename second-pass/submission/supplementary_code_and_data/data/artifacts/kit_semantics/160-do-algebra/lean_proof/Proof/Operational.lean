import Klean160DoAlgebra.Lemmas

/- Total executable models for the frozen MPY dispatch tables. -/

namespace Operational

def modelEmptyIntSeq : SortIntSeq :=
  SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»

def modelIntSeqCons (head : SortInt) (tail : SortIntSeq) : SortIntSeq :=
  SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head tail

def modelEmptyVals : SortVals :=
  SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals»

def modelNoneValue : SortVal :=
  SortVal.«noneV_MPY-CORE_Val»

def modelIntValue (value : SortInt) : SortVal :=
  SortVal.inj_SortInt value

def modelFloatValue (value : SortFloat) : SortVal :=
  SortVal.inj_SortFloat value

def modelBoolValue (value : SortBool) : SortVal :=
  SortVal.inj_SortBool value

def modelStringValue (codes : SortIntSeq) : SortVal :=
  SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» codes)

def modelIntSeqAppend : SortIntSeq → SortIntSeq → SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», tail => tail
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head rest, tail =>
      modelIntSeqCons head (modelIntSeqAppend rest tail)

def modelIntSeqSnoc : SortIntSeq → SortInt → SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», value =>
      modelIntSeqCons value modelEmptyIntSeq
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head rest, value =>
      modelIntSeqCons head (modelIntSeqSnoc rest value)

def modelIntSeqLength : SortIntSeq → SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => 0
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ rest =>
      modelIntSeqLength rest + 1

def modelValSeqLength : SortValSeq → SortInt
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => 0
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _ rest =>
      modelValSeqLength rest + 1

def modelStringCodes (text : SortString) : SortIntSeq :=
  text.toList.foldr
    (fun character rest =>
      modelIntSeqCons (Int.ofNat character.toNat) rest)
    modelEmptyIntSeq

def modelStringCodesOfValue : SortVal → SortIntSeq
  | SortVal.inj_SortStr
      (SortStr.«str(_)_MPY-CORE_Str_IntSeq» codes) => codes
  | _ => modelEmptyIntSeq

def modelTruncDiv (left right : SortInt) : SortInt :=
  if right = 0 then 0 else Int.tdiv left right

def modelFloorDiv (left right : SortInt) : SortInt :=
  if right = 0 then
    0
  else
    let quotient := modelTruncDiv left right
    let remainder := left - quotient * right
    if remainder = 0 then
      quotient
    else if (remainder < 0 ∧ right > 0) ∨
            (remainder > 0 ∧ right < 0) then
      quotient - 1
    else
      quotient

def modelPythonMod (left right : SortInt) : SortInt :=
  left - modelFloorDiv left right * right

def modelIntegerPower (base exponent : SortInt) : SortInt :=
  if exponent < 0 then 0 else Int.pow base exponent.toNat

def modelNatBinaryAcc : Nat → Nat → SortIntSeq → SortIntSeq
  | 0, _, accumulator => accumulator
  | _ + 1, 0, accumulator => accumulator
  | fuel + 1, value, accumulator =>
      modelNatBinaryAcc fuel (value / 2)
        (modelIntSeqCons (Int.ofNat (48 + value % 2)) accumulator)

def modelBinaryDigits (value : SortInt) : SortIntSeq :=
  if value = 0 then
    modelIntSeqCons 48 modelEmptyIntSeq
  else
    let magnitude := value.natAbs
    modelNatBinaryAcc (magnitude + 1) magnitude modelEmptyIntSeq

def modelBinaryString (value : SortInt) : SortIntSeq :=
  let digits := modelBinaryDigits value
  if value < 0 then
    modelIntSeqCons 45
      (modelIntSeqCons 48 (modelIntSeqCons 98 digits))
  else
    modelIntSeqCons 48 (modelIntSeqCons 98 digits)

def modelIntSeqContains (needle : SortInt) : SortIntSeq → Bool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => false
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head rest =>
      (needle == head) || modelIntSeqContains needle rest

def modelDedupCodesLoop : SortIntSeq → SortIntSeq → SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», accumulator => accumulator
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head rest,
      accumulator =>
      if modelIntSeqContains head accumulator then
        modelDedupCodesLoop rest accumulator
      else
        modelDedupCodesLoop rest (modelIntSeqSnoc accumulator head)

def modelDedupCodes (codes : SortIntSeq) : SortIntSeq :=
  modelDedupCodesLoop codes modelEmptyIntSeq

def modelDigitFold : SortIntSeq → SortInt → SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», accumulator => accumulator
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» code rest,
      accumulator =>
      modelDigitFold rest (accumulator * 10 + (code - 48))

def modelMaximumVals : SortInt → SortVals → Option SortInt
  | current, SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
      some current
  | current,
      SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortInt value) rest =>
      modelMaximumVals (if current < value then value else current) rest
  | _, _ => none

def modelMinimumVals : SortInt → SortVals → Option SortInt
  | current, SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
      some current
  | current,
      SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortInt value) rest =>
      modelMinimumVals (if value < current then value else current) rest
  | _, _ => none

def modelRangeLength (low high step : SortInt) : Option SortInt :=
  if step > 0 ∧ high > low then
    some (modelTruncDiv (high - low + step - 1) step)
  else if step < 0 ∧ high < low then
    some (modelTruncDiv (low - high - step - 1) (-step))
  else if (step > 0 ∧ high ≤ low) ∨ (step < 0 ∧ high ≥ low) then
    some 0
  else
    none

def modelSequenceLength : SortVal → Option SortInt
  | SortVal.inj_SortIterable
      (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» values) =>
      some (modelValSeqLength values)
  | SortVal.inj_SortIterable
      (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» values) =>
      some (modelValSeqLength values)
  | SortVal.inj_SortIterable
      (SortIterable.«rangeObj(_,_,_)_MPY-CORE_Iterable_Int_Int_Int»
        low high step) =>
      modelRangeLength low high step
  | SortVal.inj_SortStr
      (SortStr.«str(_)_MPY-CORE_Str_IntSeq» codes) =>
      some (modelIntSeqLength codes)
  | SortVal.«setV(_)_MPY-SET_Val_IntSeq» codes =>
      some (modelIntSeqLength codes)
  | _ => none

def modelFloatToTruncatedInt (value : SortFloat) : SortInt :=
  let bits := value.toBits.toNat
  let signIsNegative := bits / (2 ^ 63) = 1
  let exponentBits := (bits / (2 ^ 52)) % (2 ^ 11)
  let fractionBits := bits % (2 ^ 52)
  if exponentBits = 0 ∨ exponentBits = 2047 ∨ exponentBits < 1023 then
    0
  else
    let significant := (2 ^ 52) + fractionBits
    let unbiased := exponentBits - 1023
    let magnitude :=
      if unbiased ≥ 52 then
        significant * (2 ^ (unbiased - 52))
      else
        significant / (2 ^ (52 - unbiased))
    let integer := Int.ofNat magnitude
    if signIsNegative then -integer else integer

def modelFloatFloorInt (value : SortFloat) : SortInt :=
  modelFloatToTruncatedInt (Float.floor value)

def modelFloatCeilInt (value : SortFloat) : SortInt :=
  modelFloatToTruncatedInt (Float.ceil value)

def modelIntegerAsFloat (value : SortInt) : SortFloat :=
  Float.ofInt value

def modelDecimalIntPartLoop : SortIntSeq → SortInt → SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», accumulator => accumulator
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 46 _, accumulator =>
      accumulator
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» code rest,
      accumulator =>
      modelDecimalIntPartLoop rest (accumulator * 10 + (code - 48))

def modelDecimalFractionLoop : SortIntSeq → SortInt → SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», accumulator => accumulator
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» code rest,
      accumulator =>
      modelDecimalFractionLoop rest (accumulator * 10 + (code - 48))

def modelDecimalFraction : SortIntSeq → SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => 0
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 46 rest =>
      modelDecimalFractionLoop rest 0
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ rest =>
      modelDecimalFraction rest

def modelDecimalScaleLoop : SortIntSeq → SortInt → SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», accumulator => accumulator
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ rest,
      accumulator =>
      modelDecimalScaleLoop rest (accumulator * 10)

def modelDecimalScale : SortIntSeq → SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => 1
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 46 rest =>
      modelDecimalScaleLoop rest 1
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ rest =>
      modelDecimalScale rest

def modelDecimalFloat : SortIntSeq → SortFloat
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 45 rest =>
      -(modelDecimalFloat rest)
  | codes =>
      modelIntegerAsFloat (modelDecimalIntPartLoop codes 0) +
        modelIntegerAsFloat (modelDecimalFraction codes) /
          modelIntegerAsFloat (modelDecimalScale codes)

def modelRoundFloat (value : SortFloat) : SortInt :=
  let lower := Float.floor value
  let fraction := value - lower
  if fraction == (0.5 : Float) then
    let lowerInt := modelFloatToTruncatedInt lower
    if modelPythonMod lowerInt 2 = 0 then
      lowerInt
    else
      modelFloatCeilInt value
  else
    modelFloatFloorInt (value + 0.5)

def modelRoundFloatDigits (value : SortFloat) (digits : SortInt) :
    Option SortFloat :=
  if digits < 0 then
    none
  else
    let scaleInt := modelIntegerPower 10 digits
    let scale := modelIntegerAsFloat scaleInt
    some (modelIntegerAsFloat (modelRoundFloat (value * scale)) / scale)

def modelIntSeqToList : SortIntSeq → List SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => []
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head rest =>
      head :: modelIntSeqToList rest

def modelIsDigit (code : SortInt) : Bool :=
  decide (code ≥ 48 ∧ code ≤ 57)

def modelTokenOperatorsFuel : Nat → List SortInt → List SortString
  | 0, _ => []
  | _ + 1, [] => []
  | fuel + 1, 32 :: rest => modelTokenOperatorsFuel fuel rest
  | fuel + 1, code :: rest =>
      if modelIsDigit code then
        modelTokenOperatorsFuel fuel rest
      else if code = 42 then
        match rest with
        | 42 :: tail => "**" :: modelTokenOperatorsFuel fuel tail
        | _ => "*" :: modelTokenOperatorsFuel fuel rest
      else if code = 47 then
        match rest with
        | 47 :: tail => "//" :: modelTokenOperatorsFuel fuel tail
        | _ => "/" :: modelTokenOperatorsFuel fuel rest
      else if code = 43 then
        "+" :: modelTokenOperatorsFuel fuel rest
      else if code = 45 then
        "-" :: modelTokenOperatorsFuel fuel rest
      else
        modelTokenOperatorsFuel fuel rest

def modelTokenOperators (codes : List SortInt) : List SortString :=
  modelTokenOperatorsFuel (codes.length + 1) codes

def modelConsumeDigits : SortInt → List SortInt → SortInt × List SortInt
  | accumulator, [] => (accumulator, [])
  | accumulator, code :: rest =>
      if modelIsDigit code then
        modelConsumeDigits (accumulator * 10 + (code - 48)) rest
      else
        (accumulator, code :: rest)

def modelTokenNumbersFuel : Nat → List SortInt → List SortInt
  | 0, _ => []
  | _ + 1, [] => []
  | fuel + 1, code :: rest =>
      if code = 32 then
        modelTokenNumbersFuel fuel rest
      else if modelIsDigit code then
        let consumed := modelConsumeDigits (code - 48) rest
        consumed.1 :: modelTokenNumbersFuel fuel consumed.2
      else
        modelTokenNumbersFuel fuel rest

def modelTokenNumbers (codes : List SortInt) : List SortInt :=
  modelTokenNumbersFuel (codes.length + 1) codes

def modelEvalOperator (operator : SortString)
    (left right : SortInt) : SortInt :=
  if operator = "+" then left + right
  else if operator = "-" then left - right
  else if operator = "*" then left * right
  else if operator = "//" then modelFloorDiv left right
  else if operator = "**" then modelIntegerPower left right
  else left

def modelPowerPass : List SortString → List SortInt →
    List SortString × List SortInt
  | [], numbers => ([], numbers)
  | _ :: _, [] => ([], [])
  | operator :: operators, number :: numbers =>
      let processed := modelPowerPass operators numbers
      if operator = "**" then
        match processed.2 with
        | next :: rest =>
            (processed.1,
              modelIntegerPower number next :: rest)
        | [] => (processed.1, [number])
      else
        (operator :: processed.1, number :: processed.2)

def modelOperatorAtLevel (level operator : SortString) : Bool :=
  if level = "mul" then
    operator = "*" || operator = "//" || operator = "/"
  else if level = "add" then
    operator = "+" || operator = "-"
  else
    false

def modelLevelLoop (level : SortString) :
    SortInt → List SortString → List SortInt →
      List SortString → List SortInt →
        List SortString × List SortInt
  | current, [], _, outputOperators, outputNumbers =>
      (outputOperators, outputNumbers ++ [current])
  | current, _ :: _, [], outputOperators, outputNumbers =>
      (outputOperators, outputNumbers ++ [current])
  | current, operator :: operators, number :: numbers,
      outputOperators, outputNumbers =>
      if modelOperatorAtLevel level operator then
        modelLevelLoop level
          (modelEvalOperator operator current number)
          operators numbers outputOperators outputNumbers
      else
        modelLevelLoop level number operators numbers
          (outputOperators ++ [operator])
          (outputNumbers ++ [current])

def modelLevelPass (level : SortString)
    (input : List SortString × List SortInt) :
    List SortString × List SortInt :=
  match input.2 with
  | [] => (input.1, [])
  | number :: numbers =>
      modelLevelLoop level number input.1 numbers [] []

def modelEvalArithmetic (codes : SortIntSeq) : SortInt :=
  let codeList := modelIntSeqToList codes
  let powered :=
    modelPowerPass (modelTokenOperators codeList)
      (modelTokenNumbers codeList)
  let multiplied := modelLevelPass "mul" powered
  let added := modelLevelPass "add" multiplied
  match added.2 with
  | first :: _ => first
  | [] => 0

def modelApplyBin (operator : SortString)
    (left right : SortVal) : SortVal :=
  match operator, left, right with
  | "+", SortVal.inj_SortInt first, SortVal.inj_SortInt second =>
      modelIntValue (first + second)
  | "+", SortVal.inj_SortInt first, SortVal.inj_SortBool second =>
      modelIntValue (first + if second then 1 else 0)
  | "+", SortVal.inj_SortBool first, SortVal.inj_SortInt second =>
      modelIntValue ((if first then 1 else 0) + second)
  | "-", SortVal.inj_SortInt first, SortVal.inj_SortInt second =>
      modelIntValue (first - second)
  | "*", SortVal.inj_SortInt first, SortVal.inj_SortInt second =>
      modelIntValue (first * second)
  | "%", SortVal.inj_SortInt first, SortVal.inj_SortInt second =>
      if second = 0 then modelNoneValue
      else modelIntValue (modelPythonMod first second)
  | "//", SortVal.inj_SortInt first, SortVal.inj_SortInt second =>
      if second = 0 then modelNoneValue
      else modelIntValue (modelFloorDiv first second)
  | "**", SortVal.inj_SortInt first, SortVal.inj_SortInt second =>
      if second < 0 then modelNoneValue
      else modelIntValue (modelIntegerPower first second)
  | "/", SortVal.inj_SortInt first, SortVal.inj_SortInt second =>
      modelFloatValue
        (modelIntegerAsFloat first / modelIntegerAsFloat second)
  | "+", SortVal.inj_SortFloat first, SortVal.inj_SortFloat second =>
      modelFloatValue (first + second)
  | "-", SortVal.inj_SortFloat first, SortVal.inj_SortFloat second =>
      modelFloatValue (first - second)
  | "*", SortVal.inj_SortFloat first, SortVal.inj_SortFloat second =>
      modelFloatValue (first * second)
  | "/", SortVal.inj_SortFloat first, SortVal.inj_SortFloat second =>
      modelFloatValue (first / second)
  | "%", SortVal.inj_SortFloat first, SortVal.inj_SortFloat second =>
      modelFloatValue (first - Float.floor (first / second) * second)
  | "**", SortVal.inj_SortFloat first, SortVal.inj_SortFloat second =>
      modelFloatValue (Float.pow first second)
  | "+", SortVal.inj_SortInt first, SortVal.inj_SortFloat second =>
      modelFloatValue (modelIntegerAsFloat first + second)
  | "+", SortVal.inj_SortFloat first, SortVal.inj_SortInt second =>
      modelFloatValue (first + modelIntegerAsFloat second)
  | "-", SortVal.inj_SortInt first, SortVal.inj_SortFloat second =>
      modelFloatValue (modelIntegerAsFloat first - second)
  | "-", SortVal.inj_SortFloat first, SortVal.inj_SortInt second =>
      modelFloatValue (first - modelIntegerAsFloat second)
  | "*", SortVal.inj_SortInt first, SortVal.inj_SortFloat second =>
      modelFloatValue (modelIntegerAsFloat first * second)
  | "*", SortVal.inj_SortFloat first, SortVal.inj_SortInt second =>
      modelFloatValue (first * modelIntegerAsFloat second)
  | "/", SortVal.inj_SortInt first, SortVal.inj_SortFloat second =>
      modelFloatValue (modelIntegerAsFloat first / second)
  | "/", SortVal.inj_SortFloat first, SortVal.inj_SortInt second =>
      modelFloatValue (first / modelIntegerAsFloat second)
  | "**", SortVal.inj_SortInt first, SortVal.inj_SortFloat second =>
      modelFloatValue (Float.pow (modelIntegerAsFloat first) second)
  | "**", SortVal.inj_SortFloat first, SortVal.inj_SortInt second =>
      modelFloatValue (Float.pow first (modelIntegerAsFloat second))
  | "+",
      SortVal.inj_SortStr
        (SortStr.«str(_)_MPY-CORE_Str_IntSeq» first),
      SortVal.inj_SortStr
        (SortStr.«str(_)_MPY-CORE_Str_IntSeq» second) =>
      modelStringValue (modelIntSeqAppend first second)
  | _, _, _ => modelNoneValue

def modelApplyBuiltin (builtin : SortString)
    (arguments : SortVals) : SortVal :=
  match builtin, arguments with
  | "len",
      SortVals.«_,__MPY-CORE_Vals_Val_Vals» object
        SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
      match modelSequenceLength object with
      | some length => modelIntValue length
      | none => modelNoneValue
  | "set",
      SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortStr
          (SortStr.«str(_)_MPY-CORE_Str_IntSeq» codes))
        SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
      SortVal.«setV(_)_MPY-SET_Val_IntSeq» (modelDedupCodes codes)
  | "abs",
      SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortInt value)
        SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
      modelIntValue (if value < 0 then -value else value)
  | "abs",
      SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortFloat value)
        SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
      modelFloatValue (Float.abs value)
  | "floor",
      SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortInt value)
        SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
      modelIntValue value
  | "floor",
      SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortFloat value)
        SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
      modelIntValue (modelFloatFloorInt value)
  | "ceil",
      SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortInt value)
        SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
      modelIntValue value
  | "ceil",
      SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortFloat value)
        SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
      modelIntValue (modelFloatCeilInt value)
  | "max",
      SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortInt first) rest =>
      match modelMaximumVals first rest with
      | some result => modelIntValue result
      | none => modelNoneValue
  | "min",
      SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortInt first) rest =>
      match modelMinimumVals first rest with
      | some result => modelIntValue result
      | none => modelNoneValue
  | "bin",
      SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortInt value)
        SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
      modelStringValue (modelBinaryString value)
  | "int",
      SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortInt value)
        SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
      modelIntValue value
  | "int",
      SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortFloat value)
        SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
      modelIntValue (modelFloatToTruncatedInt value)
  | "int",
      SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortStr
          (SortStr.«str(_)_MPY-CORE_Str_IntSeq» codes))
        SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
      match codes with
      | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq»
          code SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» =>
          if 48 ≤ code ∧ code ≤ 57 then modelIntValue (code - 48)
          else modelNoneValue
      | _ =>
          if modelIntSeqLength codes ≥ 2 then
            modelIntValue (modelDigitFold codes 0)
          else
            modelNoneValue
  | "ord",
      SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortStr
          (SortStr.«str(_)_MPY-CORE_Str_IntSeq»
            (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq»
              code SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)))
        SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
      modelIntValue code
  | "chr",
      SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortInt code)
        SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
      if 0 ≤ code ∧ code < 128 then
        modelStringValue (modelIntSeqCons code modelEmptyIntSeq)
      else
        modelNoneValue
  | "str",
      SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortInt value)
        SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
      modelStringValue (modelStringCodes (toString value))
  | "str",
      SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortStr
          (SortStr.«str(_)_MPY-CORE_Str_IntSeq» codes))
        SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
      modelStringValue codes
  | "zip",
      SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortIterable
          (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» first))
        (SortVals.«_,__MPY-CORE_Vals_Val_Vals»
          (SortVal.inj_SortIterable
            (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» second))
          SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals») =>
      SortVal.inj_SortIterable
        (SortIterable.«zipObj(_,_)_MPY-CORE_Iterable_ValSeq_ValSeq»
          first second)
  | "zip",
      SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortStr
          (SortStr.«str(_)_MPY-CORE_Str_IntSeq» first))
        (SortVals.«_,__MPY-CORE_Vals_Val_Vals»
          (SortVal.inj_SortStr
            (SortStr.«str(_)_MPY-CORE_Str_IntSeq» second))
          SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals») =>
      SortVal.inj_SortIterable
        (SortIterable.«zipObjS(_,_)_MPY-CORE_Iterable_IntSeq_IntSeq»
          first second)
  | "range",
      SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortInt stop)
        SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
      SortVal.inj_SortIterable
        (SortIterable.«rangeObj(_,_,_)_MPY-CORE_Iterable_Int_Int_Int»
          0 stop 1)
  | "range",
      SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortInt start)
        (SortVals.«_,__MPY-CORE_Vals_Val_Vals»
          (SortVal.inj_SortInt stop)
          SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals») =>
      SortVal.inj_SortIterable
        (SortIterable.«rangeObj(_,_,_)_MPY-CORE_Iterable_Int_Int_Int»
          start stop 1)
  | "range",
      SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortInt start)
        (SortVals.«_,__MPY-CORE_Vals_Val_Vals»
          (SortVal.inj_SortInt stop)
          (SortVals.«_,__MPY-CORE_Vals_Val_Vals»
            (SortVal.inj_SortInt step)
            SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals»)) =>
      if step = 0 then modelNoneValue
      else
        SortVal.inj_SortIterable
          (SortIterable.«rangeObj(_,_,_)_MPY-CORE_Iterable_Int_Int_Int»
            start stop step)
  | "eval",
      SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortStr
          (SortStr.«str(_)_MPY-CORE_Str_IntSeq» codes))
        SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
      modelIntValue (modelEvalArithmetic codes)
  | "isinstance",
      SortVals.«_,__MPY-CORE_Vals_Val_Vals» value
        (SortVals.«_,__MPY-CORE_Vals_Val_Vals»
          (SortVal.«typeV(_)_MPY-CORE_Val_String» "int")
          SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals») =>
      match value with
      | SortVal.inj_SortInt _ => modelBoolValue true
      | _ => modelBoolValue false
  | "isinstance",
      SortVals.«_,__MPY-CORE_Vals_Val_Vals» value
        (SortVals.«_,__MPY-CORE_Vals_Val_Vals»
          (SortVal.«typeV(_)_MPY-CORE_Val_String» "str")
          SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals») =>
      match value with
      | SortVal.inj_SortStr _ => modelBoolValue true
      | _ => modelBoolValue false
  | "float",
      SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortInt value)
        SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
      modelFloatValue (modelIntegerAsFloat value)
  | "float",
      SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortFloat value)
        SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
      modelFloatValue value
  | "float",
      SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortStr
          (SortStr.«str(_)_MPY-CORE_Str_IntSeq» codes))
        SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
      modelFloatValue (modelDecimalFloat codes)
  | "round",
      SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortFloat value)
        SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
      modelIntValue (modelRoundFloat value)
  | "round",
      SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortFloat value)
        (SortVals.«_,__MPY-CORE_Vals_Val_Vals»
          (SortVal.inj_SortInt digits)
          SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals») =>
      match modelRoundFloatDigits value digits with
      | some result => modelFloatValue result
      | none => modelNoneValue
  | _, _ => modelNoneValue

end Operational
