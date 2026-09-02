import Klean69Search.Lemmas

namespace Operational

local instance operationalFloatTermBEq : BEq SortFloat where
  beq left right := left.toBits == right.toBits

deriving instance BEq for
  SortExc, SortExcCell, SortEnvCell, SortExitCodeCell,
  SortGeneratedCounterCell, SortHeapLocCell, SortIntSeq, SortOptInt,
  SortScopeLocCell, SortParamNames, SortCellVars, SortFreeVars, SortParams

deriving instance BEq for
  SortApplyK, SortBound, SortCmpOp, SortEntries, SortEntry, SortExpr,
  SortExprs, SortGeneratedTopCell, SortHeapCell, SortIndex, SortIterable,
  SortK, SortKCell, SortKItem, SortList, SortMap, SortModule, SortRetCell,
  SortRetState, SortScopesCell, SortStackCell, SortStmt, SortStmts, SortVal,
  SortValSeq, SortVals

/- Exact models of the hooked integer operations used by MPY-INT. -/
def frozenKRem (left right : SortInt) : SortInt :=
  if right = 0 then 0 else Int.emod left right

def frozenPyMod (left right : SortInt) : SortInt :=
  if right = 0 then 0
  else frozenKRem (frozenKRem left right + right) right

def frozenFloorDiv (left right : SortInt) : SortInt :=
  if right = 0 then 0
  else Int.tdiv (left - frozenPyMod left right) right

def frozenIntPow (base exponent : SortInt) : Option SortInt :=
  if exponent < 0 then none else some (Int.pow base exponent.toNat)

/- The FLOAT hooks in MPY-FLOAT are the host IEEE-754 operations. -/
def frozenIntToFloat (value : SortInt) : SortFloat :=
  Float.ofInt value

def frozenFloatEq (left right : SortFloat) : SortBool :=
  left == right

def frozenFloatLt (left right : SortFloat) : SortBool :=
  decide (left < right)

def frozenFloatGt (left right : SortFloat) : SortBool :=
  decide (right < left)

def frozenFloatMod (left right : SortFloat) : SortFloat :=
  left - Float.floor (left / right) * right

/- K's ==K is equality of K terms, not Python's overloaded equality. -/
def frozenTermEq {α : Type} [BEq α] (left right : α) : SortBool :=
  left == right

def frozenValSeqLength : SortValSeq → SortInt
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => 0
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _ rest =>
      frozenValSeqLength rest + 1

def frozenCodeIn (needle : SortInt) : SortIntSeq → SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => false
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head tail =>
      decide (needle = head) || frozenCodeIn needle tail

def frozenCodeSubset : SortIntSeq → SortIntSeq → SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _ => true
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head tail, right =>
      frozenCodeIn head right && frozenCodeSubset tail right

def frozenSetEq (left right : SortIntSeq) : SortBool :=
  frozenCodeSubset left right && frozenCodeSubset right left

def frozenDictHasKey (needle : SortVal) : SortValSeq → SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => false
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» head tail =>
      frozenTermEq head needle || frozenDictHasKey needle tail

def frozenDictLookup
    (needle : SortVal) : SortValSeq → SortValSeq → Option SortVal
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» key keyRest,
      SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» value valueRest =>
      if frozenTermEq key needle then some value
      else frozenDictLookup needle keyRest valueRest
  | _, _ => none

def frozenDictSubset :
    SortValSeq → SortValSeq → SortValSeq → SortValSeq → SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq»,
      SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _, _ => true
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» key keyRest,
      SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» value valueRest,
      rightKeys, rightValues =>
      frozenDictHasKey key rightKeys
        && match frozenDictLookup key rightKeys rightValues with
           | some found =>
               frozenTermEq found value
                 && frozenDictSubset keyRest valueRest rightKeys rightValues
           | none => false
  | _, _, _, _ => false

def frozenDictEq
    (leftKeys leftValues rightKeys rightValues : SortValSeq) : SortBool :=
  decide (frozenValSeqLength leftKeys = frozenValSeqLength rightKeys)
    && frozenDictSubset leftKeys leftValues rightKeys rightValues

/- MPY-STR's total helper equations.  The generated Klean SortVal algebra does
not expose the frozen Str subsort, but retaining these helpers makes the
source-level table explicit without forging a Val constructor. -/
def frozenCodeConcat : SortIntSeq → SortIntSeq → SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», tail => tail
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head rest, tail =>
      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq»
        head (frozenCodeConcat rest tail)

def frozenStringPrefix : SortIntSeq → SortIntSeq → SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _ => true
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ _,
      SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => false
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» left leftRest,
      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» right rightRest =>
      decide (left = right) && frozenStringPrefix leftRest rightRest

def frozenStringContains (pattern : SortIntSeq) : SortIntSeq → SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» =>
      frozenStringPrefix pattern SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head rest =>
      frozenStringPrefix pattern
          (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head rest)
        || frozenStringContains pattern rest

def frozenStringLt : SortIntSeq → SortIntSeq → SortBool
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
      else frozenStringLt leftRest rightRest

def frozenStringBin
    (operator : SortString) (left right : SortIntSeq) : Option SortIntSeq :=
  if operator = "+" then some (frozenCodeConcat left right) else none

def frozenStringCmp
    (operator : SortString) (left right : SortIntSeq) : Option SortBool :=
  if operator = "==" then some (frozenTermEq left right)
  else if operator = "!=" then some (!frozenTermEq left right)
  else if operator = "in" then some (frozenStringContains left right)
  else if operator = "not in" then some (!frozenStringContains left right)
  else if operator = "<" then some (frozenStringLt left right)
  else if operator = ">" then some (frozenStringLt right left)
  else if operator = "<=" then some (!frozenStringLt right left)
  else if operator = ">=" then some (!frozenStringLt left right)
  else none

def frozenIntIntBin
    (operator : SortString) (left right : SortInt) : Option SortVal :=
  if operator = "+" then
    some (SortVal.inj_SortInt (left + right))
  else if operator = "-" then
    some (SortVal.inj_SortInt (left - right))
  else if operator = "*" then
    some (SortVal.inj_SortInt (left * right))
  else if operator = "%" then
    if right = 0 then none
    else some (SortVal.inj_SortInt (frozenPyMod left right))
  else if operator = "//" then
    if right = 0 then none
    else some (SortVal.inj_SortInt (frozenFloorDiv left right))
  else if operator = "**" then
    (frozenIntPow left right).map SortVal.inj_SortInt
  else if operator = "/" then
    some (SortVal.inj_SortFloat (frozenIntToFloat left / frozenIntToFloat right))
  else
    none

def frozenFloatFloatBin
    (operator : SortString) (left right : SortFloat) : Option SortVal :=
  if operator = "-" then
    some (SortVal.inj_SortFloat (left - right))
  else if operator = "/" then
    some (SortVal.inj_SortFloat (left / right))
  else if operator = "+" then
    some (SortVal.inj_SortFloat (left + right))
  else if operator = "*" then
    some (SortVal.inj_SortFloat (left * right))
  else if operator = "**" then
    some (SortVal.inj_SortFloat (Float.pow left right))
  else if operator = "%" then
    some (SortVal.inj_SortFloat (frozenFloatMod left right))
  else
    none

def frozenIntFloatBin
    (operator : SortString) (left : SortInt) (right : SortFloat) : Option SortVal :=
  let leftFloat := frozenIntToFloat left
  if operator = "/" then
    some (SortVal.inj_SortFloat (leftFloat / right))
  else if operator = "**" then
    some (SortVal.inj_SortFloat (Float.pow leftFloat right))
  else if operator = "-" then
    some (SortVal.inj_SortFloat (leftFloat - right))
  else if operator = "+" then
    some (SortVal.inj_SortFloat (leftFloat + right))
  else if operator = "*" then
    some (SortVal.inj_SortFloat (leftFloat * right))
  else
    none

def frozenFloatIntBin
    (operator : SortString) (left : SortFloat) (right : SortInt) : Option SortVal :=
  let rightFloat := frozenIntToFloat right
  if operator = "/" then
    some (SortVal.inj_SortFloat (left / rightFloat))
  else if operator = "**" then
    some (SortVal.inj_SortFloat (Float.pow left rightFloat))
  else if operator = "-" then
    some (SortVal.inj_SortFloat (left - rightFloat))
  else if operator = "+" then
    some (SortVal.inj_SortFloat (left + rightFloat))
  else if operator = "*" then
    some (SortVal.inj_SortFloat (left * rightFloat))
  else
    none

def frozenIntIntCmp (operator : SortString) (left right : SortInt) : Option SortBool :=
  if operator = "<" then some (decide (left < right))
  else if operator = "<=" then some (decide (left ≤ right))
  else if operator = ">" then some (decide (left > right))
  else if operator = ">=" then some (decide (left ≥ right))
  else if operator = "==" then some (decide (left = right))
  else if operator = "!=" then some (decide (left ≠ right))
  else none

def frozenFloatFloatCmp
    (operator : SortString) (left right : SortFloat) : Option SortBool :=
  if operator = "==" then some (frozenFloatEq left right)
  else if operator = "!=" then some (!frozenFloatEq left right)
  else if operator = "<" then some (frozenFloatLt left right)
  else if operator = ">" then some (frozenFloatGt left right)
  else if operator = ">=" then some (!frozenFloatLt left right)
  else if operator = "<=" then some (!frozenFloatGt left right)
  else none

def frozenIntFloatCmp
    (operator : SortString) (left : SortInt) (right : SortFloat) : Option SortBool :=
  let leftFloat := frozenIntToFloat left
  if operator = "==" then some (frozenFloatEq leftFloat right)
  else if operator = "!=" then some (!frozenFloatEq leftFloat right)
  else if operator = "<" then some (frozenFloatLt leftFloat right)
  else if operator = ">" then some (frozenFloatGt leftFloat right)
  else none

def frozenFloatIntCmp
    (operator : SortString) (left : SortFloat) (right : SortInt) : Option SortBool :=
  let rightFloat := frozenIntToFloat right
  if operator = "==" then some (frozenFloatEq left rightFloat)
  else if operator = "!=" then some (!frozenFloatEq left rightFloat)
  else if operator = "<" then some (frozenFloatLt left rightFloat)
  else if operator = ">" then some (frozenFloatGt left rightFloat)
  else none

end Operational
