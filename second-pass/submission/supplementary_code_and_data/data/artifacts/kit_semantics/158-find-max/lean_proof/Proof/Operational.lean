import Klean158FindMax.Lemmas

/- Complete executable models of the frozen global dispatch tables. -/

/- Executable equality for the complete generated K value universe.  The
   frozen rules use ==K for list, tuple, and dictionary observations. -/
deriving instance BEq for
  SortExc, SortExcCell, SortEnvCell, SortExitCodeCell,
  SortGeneratedCounterCell, SortHeapLocCell, SortIntSeq, SortOptInt,
  SortScopeLocCell, SortParamNames, SortStr, SortCellVars, SortFreeVars,
  SortParams

deriving instance BEq for
  SortApplyK, SortBound, SortCmpOp, SortEntries, SortEntry, SortExpr,
  SortExprs, SortGeneratedTopCell, SortHeapCell, SortIndex, SortIterable,
  SortK, SortKCell, SortKItem, SortList, SortMap, SortModule, SortRetCell,
  SortRetState, SortScopesCell, SortStackCell, SortStmt, SortStmts,
  SortVal, SortValSeq, SortVals

namespace Operational

def emptyCodes : SortIntSeq :=
  SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»

def emptyValues : SortValSeq :=
  SortValSeq.«.ValSeq_MPY-CORE_ValSeq»

def noArguments : SortVals :=
  SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals»

def noneValue : SortVal :=
  SortVal.«noneV_MPY-CORE_Val»

def integerValue (value : SortInt) : SortVal :=
  SortVal.inj_SortInt value

def booleanValue (value : SortBool) : SortVal :=
  SortVal.inj_SortBool value

def floatValue (value : SortFloat) : SortVal :=
  SortVal.inj_SortFloat value

def stringValue (codes : SortIntSeq) : SortVal :=
  SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» codes)

def iterableValue (value : SortIterable) : SortVal :=
  SortVal.inj_SortIterable value

def stringPayload : SortStr → SortIntSeq
  | SortStr.«str(_)_MPY-CORE_Str_IntSeq» codes => codes

def intSequenceLength : SortIntSeq → SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => 0
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ rest =>
      1 + intSequenceLength rest

def valueSequenceLength : SortValSeq → SortInt
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => 0
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _ rest =>
      1 + valueSequenceLength rest

def codeOccurs (code : SortInt) : SortIntSeq → SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => false
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head rest =>
      (code == head) || codeOccurs code rest

def appendCode : SortIntSeq → SortInt → SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», code =>
      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» code emptyCodes
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head rest, code =>
      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq»
        head (appendCode rest code)

def deduplicateFrom : SortIntSeq → SortIntSeq → SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», acc => acc
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» code rest, acc =>
      if codeOccurs code acc then
        deduplicateFrom rest acc
      else
        deduplicateFrom rest (appendCode acc code)

def deduplicateCharacterCodes (codes : SortIntSeq) : SortIntSeq :=
  deduplicateFrom codes emptyCodes

def lexicographicallyLess : SortIntSeq → SortIntSeq → SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»,
    SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => false
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»,
    SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ _ => true
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ _,
    SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => false
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» left leftRest,
    SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» right rightRest =>
      if left < right then true
      else if left > right then false
      else lexicographicallyLess leftRest rightRest

def codesPrefix : SortIntSeq → SortIntSeq → SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _ => true
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ _,
    SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => false
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» left leftRest,
    SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» right rightRest =>
      (left == right) && codesPrefix leftRest rightRest

def codesContain (pattern : SortIntSeq) : SortIntSeq → SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => codesPrefix pattern emptyCodes
  | whole@(SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ rest) =>
      codesPrefix pattern whole || codesContain pattern rest

def codesSubset : SortIntSeq → SortIntSeq → SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _ => true
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» code rest, right =>
      codeOccurs code right && codesSubset rest right

def codeSetsEqual (left right : SortIntSeq) : SortBool :=
  codesSubset left right && codesSubset right left

def valuesEqual (left right : SortVal) : SortBool :=
  left == right

def valueSequencesEqual (left right : SortValSeq) : SortBool :=
  left == right

def dictionaryHasKey : SortValSeq → SortVal → SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _ => false
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» candidate rest, key =>
      valuesEqual candidate key || dictionaryHasKey rest key

def dictionaryGet : SortValSeq → SortValSeq → SortVal → Option SortVal
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» candidate keys,
    SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» value values, key =>
      if valuesEqual candidate key then some value
      else dictionaryGet keys values key
  | _, _, _ => none

def dictionarySubset :
    SortValSeq → SortValSeq → SortValSeq → SortValSeq → SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq»,
    SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _, _ => true
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» key keys,
    SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» value values,
    rightKeys, rightValues =>
      match dictionaryGet rightKeys rightValues key with
      | some rightValue =>
          valuesEqual rightValue value &&
            dictionarySubset keys values rightKeys rightValues
      | none => false
  | _, _, _, _ => false

def dictionariesEqual
    (leftKeys leftValues rightKeys rightValues : SortValSeq) : SortBool :=
  (valueSequenceLength leftKeys == valueSequenceLength rightKeys) &&
    dictionarySubset leftKeys leftValues rightKeys rightValues

def rangeLength (low high step : SortInt) : Option SortInt :=
  if step > 0 && high > low then
    some (Int.tdiv (high - low + step - 1) step)
  else if step < 0 && high < low then
    some (Int.tdiv (low - high - step - 1) (0 - step))
  else if (step > 0 && high <= low) || (step < 0 && high >= low) then
    some 0
  else
    none

def sequenceLength : SortVal → Option SortInt
  | SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» codes) =>
      some (intSequenceLength codes)
  | SortVal.inj_SortIterable
      (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» values) =>
      some (valueSequenceLength values)
  | SortVal.inj_SortIterable
      (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» values) =>
      some (valueSequenceLength values)
  | SortVal.«setV(_)_MPY-SET_Val_IntSeq» codes =>
      some (intSequenceLength codes)
  | SortVal.inj_SortIterable
      (SortIterable.«rangeObj(_,_,_)_MPY-CORE_Iterable_Int_Int_Int»
        low high step) =>
      rangeLength low high step
  | _ => none

def absoluteInteger (value : SortInt) : SortInt :=
  if value < 0 then 0 - value else value

def maximumArguments : SortInt → SortVals → Option SortInt
  | current, SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
      some current
  | current, SortVals.«_,__MPY-CORE_Vals_Val_Vals»
      (SortVal.inj_SortInt next) rest =>
      maximumArguments (if current < next then next else current) rest
  | _, _ => none

def minimumArguments : SortInt → SortVals → Option SortInt
  | current, SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
      some current
  | current, SortVals.«_,__MPY-CORE_Vals_Val_Vals»
      (SortVal.inj_SortInt next) rest =>
      minimumArguments (if current < next then current else next) rest
  | _, _ => none

def characterListToCodes : List Char → SortIntSeq
  | [] => emptyCodes
  | char :: rest =>
      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq»
        (Int.ofNat char.toNat) (characterListToCodes rest)

def naturalBaseTwoCodes (value : Nat) : SortIntSeq :=
  characterListToCodes (Nat.toDigits 2 value)

def binaryRepresentation (value : SortInt) : SortIntSeq :=
  let zero := Int.ofNat 48
  let bee := Int.ofNat 98
  let minus := Int.ofNat 45
  if value < 0 then
    SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» minus
      (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» zero
        (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» bee
          (naturalBaseTwoCodes (Int.natAbs value))))
  else
    SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» zero
      (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» bee
        (naturalBaseTwoCodes value.toNat))

def decimalRepresentation (value : SortInt) : SortIntSeq :=
  characterListToCodes (toString value).toList

def decimalFold : SortIntSeq → SortInt → SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», acc => acc
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» code rest, acc =>
      decimalFold rest (acc * 10 + (code - 48))

def integerFromStringCodes (codes : SortIntSeq) : Option SortInt :=
  match codes with
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq»
      code SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» =>
      if 48 <= code && code <= 57 then some (code - 48) else none
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _
      (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ _) =>
      some (decimalFold codes 0)
  | _ => none

def operatorTokens : SortIntSeq → List String
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => []
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 42
      (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 42 rest) =>
      "**" :: operatorTokens rest
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 47
      (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 47 rest) =>
      "//" :: operatorTokens rest
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 32 rest =>
      operatorTokens rest
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» code rest =>
      if 48 <= code && code <= 57 then
        operatorTokens rest
      else
        if code = 42 then "*" :: operatorTokens rest
        else if code = 47 then "/" :: operatorTokens rest
        else if code = 43 then "+" :: operatorTokens rest
        else if code = 45 then "-" :: operatorTokens rest
        else operatorTokens rest

def operandTokensAcc : SortIntSeq → Option SortInt → List SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», none => []
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», some acc => [acc]
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» code rest, current =>
      if 48 <= code && code <= 57 then
        let next :=
          match current with
          | none => code - 48
          | some acc => acc * 10 + (code - 48)
        operandTokensAcc rest (some next)
      else
        match current with
        | none => operandTokensAcc rest none
        | some acc => acc :: operandTokensAcc rest none

def operandTokens (codes : SortIntSeq) : List SortInt :=
  operandTokensAcc codes none

def integerPower (base exponent : SortInt) : SortInt :=
  if exponent < 0 then 0 else Int.pow base exponent.toNat

def applyArithmeticOperator
    (operator : String) (left right : SortInt) : SortInt :=
  if operator = "+" then left + right
  else if operator = "-" then left - right
  else if operator = "*" then left * right
  else if operator = "//" then Int.fdiv left right
  else if operator = "**" then integerPower left right
  else left

def powerPass : List String → List SortInt → List String × List SortInt
  | [], operands => ([], operands)
  | _, [] => ([], [])
  | operator :: operators, value :: values =>
      let (remainingOperators, remainingValues) := powerPass operators values
      if operator = "**" then
        match remainingValues with
        | next :: rest =>
            (remainingOperators, integerPower value next :: rest)
        | [] => (remainingOperators, [value])
      else
        (operator :: remainingOperators, value :: remainingValues)

def operatorAtLevel (level operator : String) : SortBool :=
  if level = "mul" then
    operator = "*" || operator = "//" || operator = "/"
  else if level = "add" then
    operator = "+" || operator = "-"
  else
    false

def appendString (values : List String) (value : String) : List String :=
  values ++ [value]

def appendInteger (values : List SortInt) (value : SortInt) : List SortInt :=
  values ++ [value]

def leftPassGo
    (level : String) (current : SortInt)
    (operators : List String) (operands : List SortInt)
    (outOperators : List String) (outOperands : List SortInt) :
    List String × List SortInt :=
  match operators, operands with
  | [], _ => (outOperators, appendInteger outOperands current)
  | operator :: remainingOperators, next :: remainingOperands =>
      if operatorAtLevel level operator then
        leftPassGo level (applyArithmeticOperator operator current next)
          remainingOperators remainingOperands outOperators outOperands
      else
        leftPassGo level next remainingOperators remainingOperands
          (appendString outOperators operator) (appendInteger outOperands current)
  | _ :: _, [] => (outOperators, appendInteger outOperands current)

def leftPass
    (level : String) (pair : List String × List SortInt) :
    List String × List SortInt :=
  match pair.2 with
  | [] => pair
  | first :: rest => leftPassGo level first pair.1 rest [] []

def evaluateArithmetic (codes : SortIntSeq) : SortInt :=
  let powered := powerPass (operatorTokens codes) (operandTokens codes)
  let multiplied := leftPass "mul" powered
  let added := leftPass "add" multiplied
  match added.2 with
  | first :: _ => first
  | [] => 0

def integerPartAcc : SortIntSeq → SortInt → SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», acc => acc
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 46 _, acc => acc
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» code rest, acc =>
      integerPartAcc rest (acc * 10 + (code - 48))

def fractionalAcc : SortIntSeq → SortInt → SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», acc => acc
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» code rest, acc =>
      fractionalAcc rest (acc * 10 + (code - 48))

def fractionalPart : SortIntSeq → SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => 0
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 46 rest =>
      fractionalAcc rest 0
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ rest =>
      fractionalPart rest

def fractionalScaleAcc : SortIntSeq → SortInt → SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», acc => acc
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ rest, acc =>
      fractionalScaleAcc rest (acc * 10)

def fractionalScale : SortIntSeq → SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => 1
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 46 rest =>
      fractionalScaleAcc rest 1
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ rest =>
      fractionalScale rest

def decimalFloat : SortIntSeq → SortFloat
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 45 rest =>
      0.0 - decimalFloat rest
  | codes =>
      Float.ofInt (integerPartAcc codes 0) +
        (Float.ofInt (fractionalPart codes) /
          Float.ofInt (fractionalScale codes))

def floatComparisonLess (left right : SortFloat) : SortBool :=
  decide (left < right)

def floatComparisonGreater (left right : SortFloat) : SortBool :=
  decide (right < left)

def floatComparisonEqual (left right : SortFloat) : SortBool :=
  left == right

def integralFloatToInteger (value : SortFloat) : SortInt :=
  let bits := value.toBits.toNat
  let sign := bits / (2 ^ 63)
  let exponentBits := (bits / (2 ^ 52)) % (2 ^ 11)
  let fraction := bits % (2 ^ 52)
  let magnitude :=
    if exponentBits = 0 then
      0
    else if exponentBits = 2047 then
      0
    else
      let significand := (2 ^ 52) + fraction
      if exponentBits >= 1023 + 52 then
        significand * (2 ^ (exponentBits - 1023 - 52))
      else if exponentBits >= 1023 then
        significand / (2 ^ (52 - (exponentBits - 1023)))
      else
        0
  if sign = 0 then Int.ofNat magnitude else 0 - Int.ofNat magnitude

def floorFloatToInteger (value : SortFloat) : SortInt :=
  integralFloatToInteger value.floor

def ceilFloatToInteger (value : SortFloat) : SortInt :=
  integralFloatToInteger value.ceil

def truncateFloatToInteger (value : SortFloat) : SortInt :=
  if decide (value >= 0.0) then
    floorFloatToInteger value
  else
    ceilFloatToInteger value

def roundFloatToInteger (value : SortFloat) : SortInt :=
  let floorValue := value.floor
  let floorInteger := integralFloatToInteger floorValue
  if (value - floorValue) == 0.5 then
    if floorInteger % 2 == 0 then
      floorInteger
    else
      ceilFloatToInteger value
  else
    floorFloatToInteger (value + 0.5)

def tenPower (exponent : SortInt) : SortInt :=
  if exponent < 0 then 1 else Int.pow 10 exponent.toNat

def roundFloatAtPrecision
    (value : SortFloat) (precision : SortInt) : SortFloat :=
  if precision < 0 then
    let scale := Float.ofInt (tenPower (0 - precision))
    Float.ofInt (roundFloatToInteger (value / scale)) * scale
  else
    let scale := Float.ofInt (tenPower precision)
    Float.ofInt (roundFloatToInteger (value * scale)) / scale

def projectStringDefined : SortVal → SortBool
  | SortVal.inj_SortStr _ => true
  | _ => false

def totalStringProjection : SortVal → SortStr
  | SortVal.inj_SortStr value => value
  | _ => SortStr.«str(_)_MPY-CORE_Str_IntSeq» emptyCodes

def optionalStringProjection : SortK → Option SortStr
  | SortK.kseq (SortKItem.inj_SortStr value) SortK.dotk => some value
  | _ => none

def compareStrings
    (operator : SortString) (left right : SortIntSeq) : SortBool :=
  if operator = "==" then left == right
  else if operator = "!=" then !(left == right)
  else if operator = "in" then codesContain left right
  else if operator = "not in" then !(codesContain left right)
  else if operator = "<" then lexicographicallyLess left right
  else if operator = ">" then lexicographicallyLess right left
  else if operator = "<=" then !(lexicographicallyLess right left)
  else if operator = ">=" then !(lexicographicallyLess left right)
  else false

def compareIntegers
    (operator : SortString) (left right : SortInt) : SortBool :=
  if operator = "<" then decide (left < right)
  else if operator = "<=" then decide (left <= right)
  else if operator = ">" then decide (left > right)
  else if operator = ">=" then decide (left >= right)
  else if operator = "==" then left == right
  else if operator = "!=" then !(left == right)
  else false

def compareFloats
    (operator : SortString) (left right : SortFloat) : SortBool :=
  if operator = "==" then floatComparisonEqual left right
  else if operator = "!=" then !(floatComparisonEqual left right)
  else if operator = "<" then floatComparisonLess left right
  else if operator = ">" then floatComparisonGreater left right
  else if operator = ">=" then !(floatComparisonLess left right)
  else if operator = "<=" then !(floatComparisonGreater left right)
  else false

def compareIntegerFloat
    (operator : SortString) (left : SortInt) (right : SortFloat) : SortBool :=
  let promoted := Float.ofInt left
  if operator = "==" then floatComparisonEqual promoted right
  else if operator = "!=" then !(floatComparisonEqual promoted right)
  else if operator = "<" then floatComparisonLess promoted right
  else if operator = ">" then floatComparisonGreater promoted right
  else false

def compareFloatInteger
    (operator : SortString) (left : SortFloat) (right : SortInt) : SortBool :=
  let promoted := Float.ofInt right
  if operator = "==" then floatComparisonEqual left promoted
  else if operator = "!=" then !(floatComparisonEqual left promoted)
  else if operator = "<" then floatComparisonLess left promoted
  else if operator = ">" then floatComparisonGreater left promoted
  else false

def dispatchComparison
    (operator : SortString) (left right : SortVal) : SortBool :=
  match left, right with
  | value, SortVal.«noneV_MPY-CORE_Val» =>
      if operator = "is" || operator = "==" then
        match value with
        | SortVal.«noneV_MPY-CORE_Val» => true
        | _ => false
      else if operator = "is not" || operator = "!=" then
        match value with
        | SortVal.«noneV_MPY-CORE_Val» => false
        | _ => true
      else false
  | SortVal.inj_SortInt leftValue, SortVal.inj_SortInt rightValue =>
      compareIntegers operator leftValue rightValue
  | SortVal.inj_SortBool leftValue, SortVal.inj_SortBool rightValue =>
      if operator = "==" then leftValue == rightValue
      else if operator = "!=" then !(leftValue == rightValue)
      else false
  | SortVal.inj_SortFloat leftValue, SortVal.inj_SortFloat rightValue =>
      compareFloats operator leftValue rightValue
  | SortVal.inj_SortInt leftValue, SortVal.inj_SortFloat rightValue =>
      compareIntegerFloat operator leftValue rightValue
  | SortVal.inj_SortFloat leftValue, SortVal.inj_SortInt rightValue =>
      compareFloatInteger operator leftValue rightValue
  | SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» leftCodes),
    SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» rightCodes) =>
      compareStrings operator leftCodes rightCodes
  | SortVal.inj_SortIterable
      (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» leftValues),
    SortVal.inj_SortIterable
      (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» rightValues) =>
      if operator = "==" then valueSequencesEqual leftValues rightValues
      else if operator = "!=" then !(valueSequencesEqual leftValues rightValues)
      else false
  | SortVal.inj_SortIterable
      (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» leftValues),
    SortVal.inj_SortIterable
      (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» rightValues) =>
      if operator = "==" then valueSequencesEqual leftValues rightValues
      else if operator = "!=" then !(valueSequencesEqual leftValues rightValues)
      else false
  | SortVal.«setV(_)_MPY-SET_Val_IntSeq» leftCodes,
    SortVal.«setV(_)_MPY-SET_Val_IntSeq» rightCodes =>
      if operator = "==" then codeSetsEqual leftCodes rightCodes else false
  | SortVal.«dictV(_,_)_MPY-DICT_Val_ValSeq_ValSeq»
      leftKeys leftValues,
    SortVal.«dictV(_,_)_MPY-DICT_Val_ValSeq_ValSeq»
      rightKeys rightValues =>
      if operator = "==" then
        dictionariesEqual leftKeys leftValues rightKeys rightValues
      else false
  | _, _ => false

def dispatchBuiltin (name : SortString) (args : SortVals) : SortVal :=
  if name = "len" then
    match args with
    | SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        object SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
        match sequenceLength object with
        | some length => integerValue length
        | none => noneValue
    | _ => noneValue
  else if name = "set" then
    match args with
    | SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortStr
          (SortStr.«str(_)_MPY-CORE_Str_IntSeq» codes))
        SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
        SortVal.«setV(_)_MPY-SET_Val_IntSeq»
          (deduplicateCharacterCodes codes)
    | _ => noneValue
  else if name = "abs" then
    match args with
    | SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortInt value)
        SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
        integerValue (absoluteInteger value)
    | SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortFloat value)
        SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
        floatValue value.abs
    | _ => noneValue
  else if name = "max" then
    match args with
    | SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortInt first) rest =>
        match maximumArguments first rest with
        | some result => integerValue result
        | none => noneValue
    | _ => noneValue
  else if name = "min" then
    match args with
    | SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortInt first) rest =>
        match minimumArguments first rest with
        | some result => integerValue result
        | none => noneValue
    | _ => noneValue
  else if name = "bin" then
    match args with
    | SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortInt value)
        SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
        stringValue (binaryRepresentation value)
    | _ => noneValue
  else if name = "ord" then
    match args with
    | SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortStr
          (SortStr.«str(_)_MPY-CORE_Str_IntSeq»
            (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq»
              code SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)))
        SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
        integerValue code
    | _ => noneValue
  else if name = "chr" then
    match args with
    | SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortInt code)
        SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
        if 0 <= code && code < 128 then
          stringValue
            (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq»
              code emptyCodes)
        else noneValue
    | _ => noneValue
  else if name = "str" then
    match args with
    | SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortInt value)
        SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
        stringValue (decimalRepresentation value)
    | SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        value@(SortVal.inj_SortStr _)
        SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
        value
    | _ => noneValue
  else if name = "int" then
    match args with
    | SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        value@(SortVal.inj_SortInt _)
        SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
        value
    | SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortFloat value)
        SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
        integerValue (truncateFloatToInteger value)
    | SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortStr
          (SortStr.«str(_)_MPY-CORE_Str_IntSeq» codes))
        SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
        match integerFromStringCodes codes with
        | some value => integerValue value
        | none => noneValue
    | _ => noneValue
  else if name = "float" then
    match args with
    | SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortInt value)
        SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
        floatValue (Float.ofInt value)
    | SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        value@(SortVal.inj_SortFloat _)
        SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
        value
    | SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortStr
          (SortStr.«str(_)_MPY-CORE_Str_IntSeq» codes))
        SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
        floatValue (decimalFloat codes)
    | _ => noneValue
  else if name = "floor" then
    match args with
    | SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        value@(SortVal.inj_SortInt _)
        SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
        value
    | SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortFloat value)
        SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
        integerValue (floorFloatToInteger value)
    | _ => noneValue
  else if name = "ceil" then
    match args with
    | SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        value@(SortVal.inj_SortInt _)
        SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
        value
    | SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortFloat value)
        SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
        integerValue (ceilFloatToInteger value)
    | _ => noneValue
  else if name = "round" then
    match args with
    | SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortFloat value)
        SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
        integerValue (roundFloatToInteger value)
    | SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortFloat value)
        (SortVals.«_,__MPY-CORE_Vals_Val_Vals»
          (SortVal.inj_SortInt precision)
          SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals») =>
        floatValue (roundFloatAtPrecision value precision)
    | _ => noneValue
  else if name = "zip" then
    match args with
    | SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortIterable
          (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» left))
        (SortVals.«_,__MPY-CORE_Vals_Val_Vals»
          (SortVal.inj_SortIterable
            (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» right))
          SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals») =>
        iterableValue
          (SortIterable.«zipObj(_,_)_MPY-CORE_Iterable_ValSeq_ValSeq»
            left right)
    | SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortStr
          (SortStr.«str(_)_MPY-CORE_Str_IntSeq» left))
        (SortVals.«_,__MPY-CORE_Vals_Val_Vals»
          (SortVal.inj_SortStr
            (SortStr.«str(_)_MPY-CORE_Str_IntSeq» right))
          SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals») =>
        iterableValue
          (SortIterable.«zipObjS(_,_)_MPY-CORE_Iterable_IntSeq_IntSeq»
            left right)
    | _ => noneValue
  else if name = "range" then
    match args with
    | SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortInt stop)
        SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
        iterableValue
          (SortIterable.«rangeObj(_,_,_)_MPY-CORE_Iterable_Int_Int_Int»
            0 stop 1)
    | SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortInt start)
        (SortVals.«_,__MPY-CORE_Vals_Val_Vals»
          (SortVal.inj_SortInt stop)
          SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals») =>
        iterableValue
          (SortIterable.«rangeObj(_,_,_)_MPY-CORE_Iterable_Int_Int_Int»
            start stop 1)
    | SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortInt start)
        (SortVals.«_,__MPY-CORE_Vals_Val_Vals»
          (SortVal.inj_SortInt stop)
          (SortVals.«_,__MPY-CORE_Vals_Val_Vals»
            (SortVal.inj_SortInt step)
            SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals»)) =>
        if step == 0 then noneValue
        else
          iterableValue
            (SortIterable.«rangeObj(_,_,_)_MPY-CORE_Iterable_Int_Int_Int»
              start stop step)
    | _ => noneValue
  else if name = "eval" then
    match args with
    | SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortStr
          (SortStr.«str(_)_MPY-CORE_Str_IntSeq» codes))
        SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
        integerValue (evaluateArithmetic codes)
    | _ => noneValue
  else if name = "isinstance" then
    match args with
    | SortVals.«_,__MPY-CORE_Vals_Val_Vals» value
        (SortVals.«_,__MPY-CORE_Vals_Val_Vals»
          (SortVal.«typeV(_)_MPY-CORE_Val_String» "int")
          SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals») =>
        match value with
        | SortVal.inj_SortInt _ => booleanValue true
        | _ => booleanValue false
    | SortVals.«_,__MPY-CORE_Vals_Val_Vals» value
        (SortVals.«_,__MPY-CORE_Vals_Val_Vals»
          (SortVal.«typeV(_)_MPY-CORE_Val_String» "str")
          SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals») =>
        match value with
        | SortVal.inj_SortStr _ => booleanValue true
        | _ => booleanValue false
    | _ => noneValue
  else
    noneValue

end Operational
