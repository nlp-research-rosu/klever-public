import Klean90NextSmallest.Lemmas

/-!
Executable models of the hooked and recursively defined operations used by the
two global MPY dispatch symbols.  The constructors and cases mirror the frozen
tables in `reference-semantics/semantics/{bool,int,float,str,list,tuple,set,
dict,operators}.k`.
-/

namespace ProofOperational

/- The generated mutually recursive syntax did not request equality instances.
   Deriving the whole group together supplies the structural equality used by
   K's `==K` in the list/tuple/dict rules. -/
deriving instance BEq for
  SortExc, SortExcCell, SortEnvCell, SortExitCodeCell,
  SortGeneratedCounterCell, SortHeapLocCell, SortIntSeq, SortOptInt,
  SortScanState, SortScopeLocCell, SortParamNames, SortStr, SortCellVars,
  SortFreeVars, SortParams, SortApplyK, SortBound, SortCmpOp, SortEntries,
  SortEntry, SortExpr, SortExprs, SortGeneratedTopCell, SortHeapCell,
  SortIndex, SortIterable, SortK, SortKCell, SortKItem, SortList, SortMap,
  SortModule, SortRetCell, SortRetState, SortScopesCell, SortStackCell,
  SortStmt, SortStmts, SortVal, SortValSeq, SortVals

def intSeqAppend : SortIntSeq → SortIntSeq → SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», ys => ys
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» x xs, ys =>
      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» x (intSeqAppend xs ys)

def intSeqEq : SortIntSeq → SortIntSeq → Bool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»,
      SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => true
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» x xs,
      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» y ys =>
      (x == y) && intSeqEq xs ys
  | _, _ => false

def intSeqPrefix : SortIntSeq → SortIntSeq → Bool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _ => true
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ _,
      SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => false
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» x xs,
      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» y ys =>
      (x == y) && intSeqPrefix xs ys

def intSeqContains (pattern : SortIntSeq) : SortIntSeq → Bool
  | haystack@SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» =>
      intSeqPrefix pattern haystack
  | haystack@(SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ tail) =>
      intSeqPrefix pattern haystack || intSeqContains pattern tail

def intSeqLt : SortIntSeq → SortIntSeq → Bool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»,
      SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => false
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»,
      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ _ => true
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ _,
      SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => false
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» x xs,
      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» y ys =>
      if x < y then true else if x > y then false else intSeqLt xs ys

def codeIn (code : Int) : SortIntSeq → Bool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => false
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head tail =>
      (code == head) || codeIn code tail

def subsetCodes : SortIntSeq → SortIntSeq → Bool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _ => true
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head tail, other =>
      codeIn head other && subsetCodes tail other

def sameSetCodes (left right : SortIntSeq) : Bool :=
  subsetCodes left right && subsetCodes right left

def stringCodes? : SortVal → Option SortIntSeq
  | SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» codes) => some codes
  | SortVal.inj_SortIterable
      (SortIterable.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» codes)) => some codes
  | _ => none

def listValues? : SortVal → Option SortValSeq
  | SortVal.inj_SortIterable
      (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» values) => some values
  | _ => none

def tupleValues? : SortVal → Option SortValSeq
  | SortVal.inj_SortIterable
      (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» values) => some values
  | _ => none

def isNoneValue : SortVal → Bool
  | SortVal.«noneV_MPY-CORE_Val» => true
  | _ => false

def derivedStructuralEq {α : Type} [BEq α] (left right : α) : Bool := left == right

mutual
  def valStructuralEq : SortVal → SortVal → Bool
    | SortVal.inj_SortBool left, SortVal.inj_SortBool right => left == right
    | SortVal.inj_SortFloat left, SortVal.inj_SortFloat right =>
        left.toBits == right.toBits
    | SortVal.inj_SortInt left, SortVal.inj_SortInt right => left == right
    | SortVal.inj_SortIterable left, SortVal.inj_SortIterable right =>
        iterableStructuralEq left right
    | SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» left),
        SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» right) =>
        intSeqEq left right
    | SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» left),
        SortVal.inj_SortIterable
          (SortIterable.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» right)) =>
        intSeqEq left right
    | SortVal.inj_SortIterable
          (SortIterable.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» left)),
        SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» right) =>
        intSeqEq left right
    | SortVal.«boundMethodV(_,_)_MPY-CORE_Val_Val_String» leftObj leftName,
        SortVal.«boundMethodV(_,_)_MPY-CORE_Val_Val_String» rightObj rightName =>
        valStructuralEq leftObj rightObj && (leftName == rightName)
    | SortVal.«builtinV(_)_MPY-CORE_Val_String» left,
        SortVal.«builtinV(_)_MPY-CORE_Val_String» right => left == right
    | SortVal.«cellRef(_)_MPY-CORE_Val_Int» left,
        SortVal.«cellRef(_)_MPY-CORE_Val_Int» right => left == right
    | SortVal.«cellsMark(_)_MPY-CORE_Val_ParamNames» left,
        SortVal.«cellsMark(_)_MPY-CORE_Val_ParamNames» right =>
        derivedStructuralEq left right
    | SortVal.«closureVal(_,_,_)_MPY-CORE_Val_ParamNames_Stmts_Int» lp ls li,
        SortVal.«closureVal(_,_,_)_MPY-CORE_Val_ParamNames_Stmts_Int» rp rs ri =>
        derivedStructuralEq lp rp && derivedStructuralEq ls rs && (li == ri)
    | SortVal.«closureValC(_,_,_,_)_MPY-FUNCTIONS_Val_ParamNames_ParamNames_Stmts_Map»
          lp lcp ls lm,
        SortVal.«closureValC(_,_,_,_)_MPY-FUNCTIONS_Val_ParamNames_ParamNames_Stmts_Map»
          rp rcp rs rm =>
        derivedStructuralEq lp rp && derivedStructuralEq lcp rcp &&
          derivedStructuralEq ls rs && derivedStructuralEq lm rm
    | SortVal.«dictV(_,_)_MPY-DICT_Val_ValSeq_ValSeq» lk lv,
        SortVal.«dictV(_,_)_MPY-DICT_Val_ValSeq_ValSeq» rk rv =>
        valSeqStructuralEq lk rk && valSeqStructuralEq lv rv
    | SortVal.«kwV(_,_)_MPY-CORE_Val_String_Val» ln lv,
        SortVal.«kwV(_,_)_MPY-CORE_Val_String_Val» rn rv =>
        (ln == rn) && valStructuralEq lv rv
    | SortVal.«md5Obj(_)_MPY-BUILTINS_Val_IntSeq» left,
        SortVal.«md5Obj(_)_MPY-BUILTINS_Val_IntSeq» right => intSeqEq left right
    | SortVal.«noneV_MPY-CORE_Val», SortVal.«noneV_MPY-CORE_Val» => true
    | SortVal.«ref(_)_MPY-CORE_Val_Int» left,
        SortVal.«ref(_)_MPY-CORE_Val_Int» right => left == right
    | SortVal.«setV(_)_MPY-SET_Val_IntSeq» left,
        SortVal.«setV(_)_MPY-SET_Val_IntSeq» right => intSeqEq left right
    | SortVal.«typeV(_)_MPY-CORE_Val_String» left,
        SortVal.«typeV(_)_MPY-CORE_Val_String» right => left == right
    | _, _ => false

  def valSeqStructuralEq : SortValSeq → SortValSeq → Bool
    | SortValSeq.«.ValSeq_MPY-CORE_ValSeq»,
        SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => true
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» left lefts,
        SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» right rights =>
        valStructuralEq left right && valSeqStructuralEq lefts rights
    | _, _ => false

  def iterableStructuralEq : SortIterable → SortIterable → Bool
    | SortIterable.inj_SortStr
          (SortStr.«str(_)_MPY-CORE_Str_IntSeq» left),
        SortIterable.inj_SortStr
          (SortStr.«str(_)_MPY-CORE_Str_IntSeq» right) => intSeqEq left right
    | SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» left,
        SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» right =>
        valSeqStructuralEq left right
    | SortIterable.«rangeObj(_,_,_)_MPY-CORE_Iterable_Int_Int_Int» la lb lc,
        SortIterable.«rangeObj(_,_,_)_MPY-CORE_Iterable_Int_Int_Int» ra rb rc =>
        (la == ra) && (lb == rb) && (lc == rc)
    | SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» left,
        SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» right =>
        valSeqStructuralEq left right
    | SortIterable.«zipObj(_,_)_MPY-CORE_Iterable_ValSeq_ValSeq» la lb,
        SortIterable.«zipObj(_,_)_MPY-CORE_Iterable_ValSeq_ValSeq» ra rb =>
        valSeqStructuralEq la ra && valSeqStructuralEq lb rb
    | SortIterable.«zipObjS(_,_)_MPY-CORE_Iterable_IntSeq_IntSeq» la lb,
        SortIterable.«zipObjS(_,_)_MPY-CORE_Iterable_IntSeq_IntSeq» ra rb =>
        intSeqEq la ra && intSeqEq lb rb
    | _, _ => false
end

def valSeqLength : SortValSeq → Nat
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => 0
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _ rest =>
      valSeqLength rest + 1

def dictHasKey : SortValSeq → SortVal → Bool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _ => false
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» candidate rest, key =>
      valStructuralEq candidate key || dictHasKey rest key

def dictGet? : SortValSeq → SortValSeq → SortVal → Option SortVal
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» candidate keys,
      SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» value values, key =>
      if valStructuralEq candidate key then some value else dictGet? keys values key
  | _, _, _ => none

def dictSubset : SortValSeq → SortValSeq → SortValSeq → SortValSeq → Bool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq»,
      SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _, _ => true
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» key keys,
      SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» value values,
      otherKeys, otherValues =>
      dictHasKey otherKeys key &&
        (match dictGet? otherKeys otherValues key with
         | some otherValue => valStructuralEq otherValue value
         | none => false) &&
        dictSubset keys values otherKeys otherValues
  | _, _, _, _ => false

def dictEqual
    (leftKeys leftValues rightKeys rightValues : SortValSeq) : Bool :=
  (valSeqLength leftKeys == valSeqLength rightKeys) &&
    dictSubset leftKeys leftValues rightKeys rightValues

def boolInt (value : Bool) : Int := if value then 1 else 0

def pythonIntMod (left right : Int) : Int :=
  Int.tmod (Int.tmod left right + right) right

def pythonIntFloorDiv (left right : Int) : Int :=
  Int.tdiv (left - pythonIntMod left right) right

def intPower (base exponent : Int) : Int :=
  Int.pow base exponent.toNat

def intAsFloat (value : Int) : Float := Float.ofInt value

def pythonFloatMod (left right : Float) : Float :=
  left - Float.floor (left / right) * right

def makeStringValue (codes : SortIntSeq) : SortVal :=
  SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» codes)

def undefinedBinValue : SortVal := SortVal.«noneV_MPY-CORE_Val»

def applyBinComplete (operator : String) (left right : SortVal) : SortVal :=
  if operator == "+" then
    match stringCodes? left, stringCodes? right with
    | some leftCodes, some rightCodes =>
        makeStringValue (intSeqAppend leftCodes rightCodes)
    | _, _ =>
      match left, right with
      | SortVal.inj_SortInt l, SortVal.inj_SortInt r => SortVal.inj_SortInt (l + r)
      | SortVal.inj_SortInt l, SortVal.inj_SortBool r => SortVal.inj_SortInt (l + boolInt r)
      | SortVal.inj_SortBool l, SortVal.inj_SortInt r => SortVal.inj_SortInt (boolInt l + r)
      | SortVal.inj_SortFloat l, SortVal.inj_SortFloat r => SortVal.inj_SortFloat (l + r)
      | SortVal.inj_SortInt l, SortVal.inj_SortFloat r => SortVal.inj_SortFloat (intAsFloat l + r)
      | SortVal.inj_SortFloat l, SortVal.inj_SortInt r => SortVal.inj_SortFloat (l + intAsFloat r)
      | _, _ => undefinedBinValue
  else if operator == "-" then
    match left, right with
    | SortVal.inj_SortInt l, SortVal.inj_SortInt r => SortVal.inj_SortInt (l - r)
    | SortVal.inj_SortFloat l, SortVal.inj_SortFloat r => SortVal.inj_SortFloat (l - r)
    | SortVal.inj_SortInt l, SortVal.inj_SortFloat r => SortVal.inj_SortFloat (intAsFloat l - r)
    | SortVal.inj_SortFloat l, SortVal.inj_SortInt r => SortVal.inj_SortFloat (l - intAsFloat r)
    | _, _ => undefinedBinValue
  else if operator == "*" then
    match left, right with
    | SortVal.inj_SortInt l, SortVal.inj_SortInt r => SortVal.inj_SortInt (l * r)
    | SortVal.inj_SortFloat l, SortVal.inj_SortFloat r => SortVal.inj_SortFloat (l * r)
    | SortVal.inj_SortInt l, SortVal.inj_SortFloat r => SortVal.inj_SortFloat (intAsFloat l * r)
    | SortVal.inj_SortFloat l, SortVal.inj_SortInt r => SortVal.inj_SortFloat (l * intAsFloat r)
    | _, _ => undefinedBinValue
  else if operator == "%" then
    match left, right with
    | SortVal.inj_SortInt l, SortVal.inj_SortInt r =>
        if r == 0 then undefinedBinValue else SortVal.inj_SortInt (pythonIntMod l r)
    | SortVal.inj_SortFloat l, SortVal.inj_SortFloat r =>
        SortVal.inj_SortFloat (pythonFloatMod l r)
    | _, _ => undefinedBinValue
  else if operator == "//" then
    match left, right with
    | SortVal.inj_SortInt l, SortVal.inj_SortInt r =>
        if r == 0 then undefinedBinValue else SortVal.inj_SortInt (pythonIntFloorDiv l r)
    | _, _ => undefinedBinValue
  else if operator == "/" then
    match left, right with
    | SortVal.inj_SortInt l, SortVal.inj_SortInt r =>
        SortVal.inj_SortFloat (intAsFloat l / intAsFloat r)
    | SortVal.inj_SortInt l, SortVal.inj_SortFloat r =>
        SortVal.inj_SortFloat (intAsFloat l / r)
    | SortVal.inj_SortFloat l, SortVal.inj_SortInt r =>
        SortVal.inj_SortFloat (l / intAsFloat r)
    | SortVal.inj_SortFloat l, SortVal.inj_SortFloat r =>
        SortVal.inj_SortFloat (l / r)
    | _, _ => undefinedBinValue
  else if operator == "**" then
    match left, right with
    | SortVal.inj_SortInt l, SortVal.inj_SortInt r =>
        if r < 0 then undefinedBinValue else SortVal.inj_SortInt (intPower l r)
    | SortVal.inj_SortFloat l, SortVal.inj_SortFloat r =>
        SortVal.inj_SortFloat (Float.pow l r)
    | SortVal.inj_SortInt l, SortVal.inj_SortFloat r =>
        SortVal.inj_SortFloat (Float.pow (intAsFloat l) r)
    | SortVal.inj_SortFloat l, SortVal.inj_SortInt r =>
        SortVal.inj_SortFloat (Float.pow l (intAsFloat r))
    | _, _ => undefinedBinValue
  else undefinedBinValue

def applyCmpComplete (operator : String) (left right : SortVal) : Bool :=
  if operator == "is" then
    if isNoneValue right then isNoneValue left else false
  else if operator == "is not" then
    if isNoneValue right then !isNoneValue left else false
  else if operator == "==" then
    if isNoneValue right then isNoneValue left else
    match stringCodes? left, stringCodes? right with
    | some l, some r => intSeqEq l r
    | _, _ =>
      match left, right with
      | SortVal.inj_SortInt l, SortVal.inj_SortInt r => l == r
      | SortVal.inj_SortFloat l, SortVal.inj_SortFloat r => l == r
      | SortVal.inj_SortInt l, SortVal.inj_SortFloat r => intAsFloat l == r
      | SortVal.inj_SortFloat l, SortVal.inj_SortInt r => l == intAsFloat r
      | SortVal.inj_SortBool l, SortVal.inj_SortBool r => l == r
      | SortVal.inj_SortIterable (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» l),
          SortVal.inj_SortIterable (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» r) =>
          valSeqStructuralEq l r
      | SortVal.inj_SortIterable (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» l),
          SortVal.inj_SortIterable (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» r) =>
          valSeqStructuralEq l r
      | SortVal.«setV(_)_MPY-SET_Val_IntSeq» l,
          SortVal.«setV(_)_MPY-SET_Val_IntSeq» r => sameSetCodes l r
      | SortVal.«dictV(_,_)_MPY-DICT_Val_ValSeq_ValSeq» lk lv,
          SortVal.«dictV(_,_)_MPY-DICT_Val_ValSeq_ValSeq» rk rv =>
          dictEqual lk lv rk rv
      | _, _ => false
  else if operator == "!=" then
    if isNoneValue right then !isNoneValue left else
    match stringCodes? left, stringCodes? right with
    | some l, some r => !intSeqEq l r
    | _, _ =>
      match left, right with
      | SortVal.inj_SortInt l, SortVal.inj_SortInt r => l != r
      | SortVal.inj_SortFloat l, SortVal.inj_SortFloat r => !(l == r)
      | SortVal.inj_SortInt l, SortVal.inj_SortFloat r => !(intAsFloat l == r)
      | SortVal.inj_SortFloat l, SortVal.inj_SortInt r => !(l == intAsFloat r)
      | SortVal.inj_SortBool l, SortVal.inj_SortBool r => l != r
      | SortVal.inj_SortIterable (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» l),
          SortVal.inj_SortIterable (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» r) =>
          !valSeqStructuralEq l r
      | SortVal.inj_SortIterable (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» l),
          SortVal.inj_SortIterable (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» r) =>
          !valSeqStructuralEq l r
      | _, _ => false
  else if operator == "<" then
    match stringCodes? left, stringCodes? right with
    | some l, some r => intSeqLt l r
    | _, _ =>
      match left, right with
      | SortVal.inj_SortInt l, SortVal.inj_SortInt r => l < r
      | SortVal.inj_SortFloat l, SortVal.inj_SortFloat r => l < r
      | SortVal.inj_SortInt l, SortVal.inj_SortFloat r => intAsFloat l < r
      | SortVal.inj_SortFloat l, SortVal.inj_SortInt r => l < intAsFloat r
      | _, _ => false
  else if operator == ">" then
    match stringCodes? left, stringCodes? right with
    | some l, some r => intSeqLt r l
    | _, _ =>
      match left, right with
      | SortVal.inj_SortInt l, SortVal.inj_SortInt r => l > r
      | SortVal.inj_SortFloat l, SortVal.inj_SortFloat r => l > r
      | SortVal.inj_SortInt l, SortVal.inj_SortFloat r => intAsFloat l > r
      | SortVal.inj_SortFloat l, SortVal.inj_SortInt r => l > intAsFloat r
      | _, _ => false
  else if operator == "<=" then
    match stringCodes? left, stringCodes? right with
    | some l, some r => !intSeqLt r l
    | _, _ =>
      match left, right with
      | SortVal.inj_SortInt l, SortVal.inj_SortInt r => l <= r
      | SortVal.inj_SortFloat l, SortVal.inj_SortFloat r => !(l > r)
      | _, _ => false
  else if operator == ">=" then
    match stringCodes? left, stringCodes? right with
    | some l, some r => !intSeqLt l r
    | _, _ =>
      match left, right with
      | SortVal.inj_SortInt l, SortVal.inj_SortInt r => l >= r
      | SortVal.inj_SortFloat l, SortVal.inj_SortFloat r => !(l < r)
      | _, _ => false
  else if operator == "in" then
    match stringCodes? left, stringCodes? right with
    | some pattern, some text => intSeqContains pattern text
    | _, _ => false
  else if operator == "not in" then
    match stringCodes? left, stringCodes? right with
    | some pattern, some text => !intSeqContains pattern text
    | _, _ => false
  else false

end ProofOperational
