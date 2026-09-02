import Klean105ByLength.Lemmas

namespace Proof

/- KORE symbol: Lbl'UndsEqlsEqls'Int'Unds'; frozen source obligations: rule-4a33e8fabf1037b714c839a6db0b745a25e879f3ee38553ad06d7cffc831f430. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_==Int_» (left right : SortInt) : SortBool :=
  left == right

-- Executable structural equality for K's algebraic terms.  The first group
-- contains the nonrecursive sorts used by the generated mutual block.
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

def kIntSeqPrefix : SortIntSeq → SortIntSeq → SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _ => true
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ _,
      SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => false
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» leftHead leftTail,
      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» rightHead rightTail =>
      (leftHead == rightHead) && kIntSeqPrefix leftTail rightTail

def kIntSeqContains (pattern : SortIntSeq) : SortIntSeq → SortBool
  | candidate@SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» =>
      kIntSeqPrefix pattern candidate
  | candidate@(SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ tail) =>
      kIntSeqPrefix pattern candidate || kIntSeqContains pattern tail

def kIntSeqLt : SortIntSeq → SortIntSeq → SortBool
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
      else kIntSeqLt leftTail rightTail

def kCodeIn (code : SortInt) : SortIntSeq → SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => false
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head tail =>
      (code == head) || kCodeIn code tail

def kSubsetCodes : SortIntSeq → SortIntSeq → SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _ => true
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head tail, other =>
      kCodeIn head other && kSubsetCodes tail other

def kSameSet (left right : SortIntSeq) : SortBool :=
  kSubsetCodes left right && kSubsetCodes right left

def kValSeqLength : SortValSeq → SortInt
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => 0
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _ tail =>
      1 + kValSeqLength tail

def kDictHasKey (keys : SortValSeq) (key : SortVal) : SortBool :=
  match keys with
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => false
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» head tail =>
      (head == key) || kDictHasKey tail key

def kDictGet? (keys values : SortValSeq) (key : SortVal) : Option SortVal :=
  match keys, values with
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» keyHead keyTail,
      SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» valueHead valueTail =>
      if keyHead == key then some valueHead else kDictGet? keyTail valueTail key
  | _, _ => none

def kDictSubset : SortValSeq → SortValSeq → SortValSeq → SortValSeq → SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq»,
      SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _, _ => true
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» key keyTail,
      SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» value valueTail,
      otherKeys, otherValues =>
      kDictHasKey otherKeys key &&
        (match kDictGet? otherKeys otherValues key with
         | some otherValue => otherValue == value
         | none => false) &&
        kDictSubset keyTail valueTail otherKeys otherValues
  | _, _, _, _ => false

/- KORE symbol: LblapplyCmp'LParUndsCommUndsCommUndsRParUnds'MPY-CORE'Unds'Bool'Unds'String'Unds'Val'Unds'Val; frozen source obligations: rule-4a33e8fabf1037b714c839a6db0b745a25e879f3ee38553ad06d7cffc831f430. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»
    (operator : SortString) (left right : SortVal) : SortBool :=
  match operator, left, right with
  -- MPY-BOOL
  | "==", SortVal.inj_SortBool leftBool, SortVal.inj_SortBool rightBool =>
      leftBool == rightBool
  | "!=", SortVal.inj_SortBool leftBool, SortVal.inj_SortBool rightBool =>
      leftBool != rightBool
  -- MPY-INT
  | "<", SortVal.inj_SortInt leftInt, SortVal.inj_SortInt rightInt =>
      leftInt < rightInt
  | "<=", SortVal.inj_SortInt leftInt, SortVal.inj_SortInt rightInt =>
      leftInt <= rightInt
  | ">", SortVal.inj_SortInt leftInt, SortVal.inj_SortInt rightInt =>
      leftInt > rightInt
  | ">=", SortVal.inj_SortInt leftInt, SortVal.inj_SortInt rightInt =>
      leftInt >= rightInt
  | "==", SortVal.inj_SortInt leftInt, SortVal.inj_SortInt rightInt =>
      leftInt == rightInt
  | "!=", SortVal.inj_SortInt leftInt, SortVal.inj_SortInt rightInt =>
      leftInt != rightInt
  -- MPY-FLOAT
  | "==", SortVal.inj_SortFloat leftFloat, SortVal.inj_SortFloat rightFloat =>
      leftFloat == rightFloat
  | "!=", SortVal.inj_SortFloat leftFloat, SortVal.inj_SortFloat rightFloat =>
      leftFloat != rightFloat
  | "<", SortVal.inj_SortFloat leftFloat, SortVal.inj_SortFloat rightFloat =>
      leftFloat < rightFloat
  | ">", SortVal.inj_SortFloat leftFloat, SortVal.inj_SortFloat rightFloat =>
      rightFloat < leftFloat
  | ">=", SortVal.inj_SortFloat leftFloat, SortVal.inj_SortFloat rightFloat =>
      !(leftFloat < rightFloat)
  | "<=", SortVal.inj_SortFloat leftFloat, SortVal.inj_SortFloat rightFloat =>
      !(rightFloat < leftFloat)
  -- MPY-FLOAT Int/Float coercions
  | "==", SortVal.inj_SortInt leftInt, SortVal.inj_SortFloat rightFloat =>
      Float.ofInt leftInt == rightFloat
  | "==", SortVal.inj_SortFloat leftFloat, SortVal.inj_SortInt rightInt =>
      leftFloat == Float.ofInt rightInt
  | "!=", SortVal.inj_SortInt leftInt, SortVal.inj_SortFloat rightFloat =>
      Float.ofInt leftInt != rightFloat
  | "!=", SortVal.inj_SortFloat leftFloat, SortVal.inj_SortInt rightInt =>
      leftFloat != Float.ofInt rightInt
  | "<", SortVal.inj_SortInt leftInt, SortVal.inj_SortFloat rightFloat =>
      Float.ofInt leftInt < rightFloat
  | "<", SortVal.inj_SortFloat leftFloat, SortVal.inj_SortInt rightInt =>
      leftFloat < Float.ofInt rightInt
  | ">", SortVal.inj_SortInt leftInt, SortVal.inj_SortFloat rightFloat =>
      rightFloat < Float.ofInt leftInt
  | ">", SortVal.inj_SortFloat leftFloat, SortVal.inj_SortInt rightInt =>
      Float.ofInt rightInt < leftFloat
  -- MPY-STR
  | "==", SortVal.inj_SortStr
      (SortStr.«str(_)_MPY-CORE_Str_IntSeq» leftCodes),
      SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» rightCodes) =>
      leftCodes == rightCodes
  | "!=", SortVal.inj_SortStr
      (SortStr.«str(_)_MPY-CORE_Str_IntSeq» leftCodes),
      SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» rightCodes) =>
      leftCodes != rightCodes
  | "in", SortVal.inj_SortStr
      (SortStr.«str(_)_MPY-CORE_Str_IntSeq» pattern),
      SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» candidate) =>
      kIntSeqContains pattern candidate
  | "not in", SortVal.inj_SortStr
      (SortStr.«str(_)_MPY-CORE_Str_IntSeq» pattern),
      SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» candidate) =>
      !kIntSeqContains pattern candidate
  | "<", SortVal.inj_SortStr
      (SortStr.«str(_)_MPY-CORE_Str_IntSeq» leftCodes),
      SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» rightCodes) =>
      kIntSeqLt leftCodes rightCodes
  | ">", SortVal.inj_SortStr
      (SortStr.«str(_)_MPY-CORE_Str_IntSeq» leftCodes),
      SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» rightCodes) =>
      kIntSeqLt rightCodes leftCodes
  | "<=", SortVal.inj_SortStr
      (SortStr.«str(_)_MPY-CORE_Str_IntSeq» leftCodes),
      SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» rightCodes) =>
      !kIntSeqLt rightCodes leftCodes
  | ">=", SortVal.inj_SortStr
      (SortStr.«str(_)_MPY-CORE_Str_IntSeq» leftCodes),
      SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» rightCodes) =>
      !kIntSeqLt leftCodes rightCodes
  -- MPY-LIST and MPY-TUPLE: both frozen rules use structural ==K.
  | "==", SortVal.inj_SortIterable
      (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» leftValues),
      SortVal.inj_SortIterable
        (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» rightValues) =>
      leftValues == rightValues
  | "!=", SortVal.inj_SortIterable
      (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» leftValues),
      SortVal.inj_SortIterable
        (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» rightValues) =>
      leftValues != rightValues
  | "==", SortVal.inj_SortIterable
      (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» leftValues),
      SortVal.inj_SortIterable
        (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» rightValues) =>
      leftValues == rightValues
  | "!=", SortVal.inj_SortIterable
      (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» leftValues),
      SortVal.inj_SortIterable
        (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» rightValues) =>
      leftValues != rightValues
  -- MPY-SET
  | "==", SortVal.«setV(_)_MPY-SET_Val_IntSeq» leftCodes,
      SortVal.«setV(_)_MPY-SET_Val_IntSeq» rightCodes =>
      kSameSet leftCodes rightCodes
  -- MPY-DICT
  | "==", SortVal.«dictV(_,_)_MPY-DICT_Val_ValSeq_ValSeq» leftKeys leftValues,
      SortVal.«dictV(_,_)_MPY-DICT_Val_ValSeq_ValSeq» rightKeys rightValues =>
      (kValSeqLength leftKeys == kValSeqLength rightKeys) &&
        kDictSubset leftKeys leftValues rightKeys rightValues
  -- MPY-FLOAT/MPY-OPERATORS None equality and identity cases.
  | "==", value, SortVal.«noneV_MPY-CORE_Val» =>
      value == SortVal.«noneV_MPY-CORE_Val»
  | "!=", value, SortVal.«noneV_MPY-CORE_Val» =>
      value != SortVal.«noneV_MPY-CORE_Val»
  | "is", value, SortVal.«noneV_MPY-CORE_Val» =>
      value == SortVal.«noneV_MPY-CORE_Val»
  | "is not", value, SortVal.«noneV_MPY-CORE_Val» =>
      value != SortVal.«noneV_MPY-CORE_Val»
  -- K leaves all other applications stuck; false is the total Lean encoding
  -- only for those rule-free combinations.
  | _, _, _ => false

/- KORE symbol: LblisInt; frozen source obligations: rule-4a33e8fabf1037b714c839a6db0b745a25e879f3ee38553ad06d7cffc831f430. Replace this stub with its honest total meaning from the frozen K semantics. -/
def isInt : SortK → SortBool
  | SortK.kseq (SortKItem.inj_SortInt _) SortK.dotk => true
  | _ => false

/- KORE symbol: Lblproject'Coln'Int; frozen source obligations: rule-4a33e8fabf1037b714c839a6db0b745a25e879f3ee38553ad06d7cffc831f430. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «project:Int» : SortK → SortInt
  | SortK.kseq (SortKItem.inj_SortInt value) SortK.dotk => value
  -- The frozen projection is partial outside this injection.  This branch
  -- totalizes only that undefined part of the fixed Lean function type.
  | _ => 0

theorem final :
    Klean105ByLength.Lemmas.targetStatement «_==Int_» «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» isInt «project:Int» := by
  intro I V h
  cases V <;> cases h <;> rfl

end Proof
