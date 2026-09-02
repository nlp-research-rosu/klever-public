import Klean110Exchange.Inj

namespace ProofModel

def pyMod (x modulus : SortInt) : Option SortInt :=
  if modulus = 0 then
    none
  else
    some (Int.tmod (Int.tmod x modulus + modulus) modulus)

def boolToInt : SortBool → SortInt
  | false => 0
  | true => 1

/- MPY-FLOAT fixes IEEE-754's (53, 11) format, represented by Lean `Float`. -/
def intToFloat : SortInt → SortFloat
  | Int.ofNat value => Float.ofNat value
  | Int.negSucc value => -(Float.ofNat (value + 1))

def floatEq (x y : SortFloat) : SortBool := x == y

def floatLt (x y : SortFloat) : SortBool := decide (x < y)

def floatGt (x y : SortFloat) : SortBool := decide (y < x)

def floatMod (x modulus : SortFloat) : SortFloat :=
  x - Float.floor (x / modulus) * modulus

def floatModTwo (x : SortFloat) : SortFloat :=
  floatMod x (2.0 : SortFloat)

/- K's `==K` is structural equality of constructed K terms. -/
noncomputable def kEqual {α : Type} (left right : α) : SortBool := by
  classical
  exact decide (left = right)

def intSeqAppend : SortIntSeq → SortIntSeq → SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», suffix => suffix
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head tail, suffix =>
      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq»
        head (intSeqAppend tail suffix)

def intSeqPrefix : SortIntSeq → SortIntSeq → SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _ => true
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ _,
      SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => false
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» leftHead leftTail,
      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» rightHead rightTail =>
      (leftHead == rightHead) && intSeqPrefix leftTail rightTail

def intSeqContains (pattern : SortIntSeq) : SortIntSeq → SortBool
  | text@(SortIntSeq.«.IntSeq_MPY-CORE_IntSeq») =>
      intSeqPrefix pattern text
  | text@(SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ tail) =>
      intSeqPrefix pattern text || intSeqContains pattern tail

def intSeqLt : SortIntSeq → SortIntSeq → SortBool
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
      else intSeqLt leftTail rightTail

def codeIn (code : SortInt) : SortIntSeq → SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => false
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head tail =>
      (code == head) || codeIn code tail

def subsetCodes : SortIntSeq → SortIntSeq → SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _ => true
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head tail, right =>
      codeIn head right && subsetCodes tail right

def sameSet (left right : SortIntSeq) : SortBool :=
  subsetCodes left right && subsetCodes right left

def valSeqLength : SortValSeq → SortInt
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => 0
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _ tail =>
      valSeqLength tail + 1

noncomputable def dictLookup
    (key : SortVal) : SortValSeq → SortValSeq → Option SortVal
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» candidate keys,
      SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» value values =>
      if kEqual candidate key then some value else dictLookup key keys values
  | _, _ => none

noncomputable def dictSubset
    (rightKeys rightValues : SortValSeq) :
    SortValSeq → SortValSeq → SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq»,
      SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => true
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» key keys,
      SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» value values =>
      match dictLookup key rightKeys rightValues with
      | some rightValue =>
          kEqual rightValue value &&
            dictSubset rightKeys rightValues keys values
      | none => false
  | _, _ => false

noncomputable def dictEqual
    (leftKeys leftValues rightKeys rightValues : SortValSeq) : SortBool :=
  (valSeqLength leftKeys == valSeqLength rightKeys) &&
    dictSubset rightKeys rightValues leftKeys leftValues

/- Complete frozen `applyBin` rule table. `none` means that no frozen rule
   matches, or that a guarded/partial Int operation is undefined. -/
noncomputable def applyBin?
    (operator : SortString) (left right : SortVal) : Option SortVal :=
  match left, right with
  | SortVal.inj_SortInt x, SortVal.inj_SortInt y =>
      if operator = "+" then some (SortVal.inj_SortInt (x + y))
      else if operator = "-" then some (SortVal.inj_SortInt (x - y))
      else if operator = "*" then some (SortVal.inj_SortInt (x * y))
      else if operator = "%" then (pyMod x y).map SortVal.inj_SortInt
      else if operator = "//" then
        (pyMod x y).map
          (fun remainder => SortVal.inj_SortInt (Int.tdiv (x - remainder) y))
      else if operator = "**" then
        if y < 0 then none
        else some (SortVal.inj_SortInt (x ^ y.toNat))
      else if operator = "/" then
        some (SortVal.inj_SortFloat (intToFloat x / intToFloat y))
      else none
  | SortVal.inj_SortInt x, SortVal.inj_SortBool y =>
      if operator = "+" then
        some (SortVal.inj_SortInt (x + boolToInt y))
      else none
  | SortVal.inj_SortBool x, SortVal.inj_SortInt y =>
      if operator = "+" then
        some (SortVal.inj_SortInt (boolToInt x + y))
      else if operator = "%" then
        if y = 2 then
          some (SortVal.inj_SortInt ((pyMod (boolToInt x) 2).getD 0))
        else none
      else none
  | SortVal.inj_SortFloat x, SortVal.inj_SortFloat y =>
      if operator = "+" then some (SortVal.inj_SortFloat (x + y))
      else if operator = "-" then some (SortVal.inj_SortFloat (x - y))
      else if operator = "*" then some (SortVal.inj_SortFloat (x * y))
      else if operator = "/" then some (SortVal.inj_SortFloat (x / y))
      else if operator = "%" then
        some (SortVal.inj_SortFloat (floatMod x y))
      else if operator = "**" then some (SortVal.inj_SortFloat (x ^ y))
      else none
  | SortVal.inj_SortInt x, SortVal.inj_SortFloat y =>
      if operator = "+" then some (SortVal.inj_SortFloat (intToFloat x + y))
      else if operator = "-" then
        some (SortVal.inj_SortFloat (intToFloat x - y))
      else if operator = "*" then
        some (SortVal.inj_SortFloat (intToFloat x * y))
      else if operator = "/" then
        some (SortVal.inj_SortFloat (intToFloat x / y))
      else if operator = "**" then
        some (SortVal.inj_SortFloat (intToFloat x ^ y))
      else none
  | SortVal.inj_SortFloat x, SortVal.inj_SortInt y =>
      if operator = "%" then
        if y = 2 then some (SortVal.inj_SortFloat (floatModTwo x)) else none
      else if operator = "+" then
        some (SortVal.inj_SortFloat (x + intToFloat y))
      else if operator = "-" then
        some (SortVal.inj_SortFloat (x - intToFloat y))
      else if operator = "*" then
        some (SortVal.inj_SortFloat (x * intToFloat y))
      else if operator = "/" then
        some (SortVal.inj_SortFloat (x / intToFloat y))
      else if operator = "**" then
        some (SortVal.inj_SortFloat (x ^ intToFloat y))
      else none
  | SortVal.inj_SortStr
      (SortStr.«str(_)_MPY-CORE_Str_IntSeq» leftCodes),
      SortVal.inj_SortStr
      (SortStr.«str(_)_MPY-CORE_Str_IntSeq» rightCodes) =>
      if operator = "+" then
        some (SortVal.inj_SortStr
          (SortStr.«str(_)_MPY-CORE_Str_IntSeq»
            (intSeqAppend leftCodes rightCodes)))
      else none
  | _, _ => none

noncomputable def equality?
    (left right : SortVal) : Option SortBool :=
  match right with
  | SortVal.«noneV_MPY-CORE_Val» => some (kEqual left right)
  | _ =>
    match left, right with
    | SortVal.inj_SortInt x, SortVal.inj_SortInt y => some (x == y)
    | SortVal.inj_SortBool x, SortVal.inj_SortBool y => some (x == y)
    | SortVal.inj_SortFloat x, SortVal.inj_SortFloat y =>
        some (floatEq x y)
    | SortVal.inj_SortInt x, SortVal.inj_SortFloat y =>
        some (floatEq (intToFloat x) y)
    | SortVal.inj_SortFloat x, SortVal.inj_SortInt y =>
        if y = 0 then some (floatEq x (0.0 : SortFloat))
        else some (floatEq x (intToFloat y))
    | SortVal.inj_SortStr
        (SortStr.«str(_)_MPY-CORE_Str_IntSeq» leftCodes),
        SortVal.inj_SortStr
        (SortStr.«str(_)_MPY-CORE_Str_IntSeq» rightCodes) =>
        some (kEqual leftCodes rightCodes)
    | SortVal.inj_SortIterable
        (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» leftValues),
        SortVal.inj_SortIterable
        (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» rightValues) =>
        some (kEqual leftValues rightValues)
    | SortVal.inj_SortIterable
        (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» leftValues),
        SortVal.inj_SortIterable
        (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» rightValues) =>
        some (kEqual leftValues rightValues)
    | SortVal.«setV(_)_MPY-SET_Val_IntSeq» leftCodes,
        SortVal.«setV(_)_MPY-SET_Val_IntSeq» rightCodes =>
        some (sameSet leftCodes rightCodes)
    | SortVal.«dictV(_,_)_MPY-DICT_Val_ValSeq_ValSeq» leftKeys leftValues,
        SortVal.«dictV(_,_)_MPY-DICT_Val_ValSeq_ValSeq» rightKeys rightValues =>
        some (dictEqual leftKeys leftValues rightKeys rightValues)
    | _, _ => none

noncomputable def inequality?
    (left right : SortVal) : Option SortBool :=
  match right with
  | SortVal.«noneV_MPY-CORE_Val» => some (!(kEqual left right))
  | _ =>
    match left, right with
    | SortVal.inj_SortInt x, SortVal.inj_SortInt y => some (!(x == y))
    | SortVal.inj_SortBool x, SortVal.inj_SortBool y => some (!(x == y))
    | SortVal.inj_SortFloat x, SortVal.inj_SortFloat y =>
        some (!(floatEq x y))
    | SortVal.inj_SortInt x, SortVal.inj_SortFloat y =>
        some (!(floatEq (intToFloat x) y))
    | SortVal.inj_SortFloat x, SortVal.inj_SortInt y =>
        some (!(floatEq x (intToFloat y)))
    | SortVal.inj_SortStr
        (SortStr.«str(_)_MPY-CORE_Str_IntSeq» leftCodes),
        SortVal.inj_SortStr
        (SortStr.«str(_)_MPY-CORE_Str_IntSeq» rightCodes) =>
        some (!(kEqual leftCodes rightCodes))
    | SortVal.inj_SortIterable
        (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» leftValues),
        SortVal.inj_SortIterable
        (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» rightValues) =>
        some (!(kEqual leftValues rightValues))
    | SortVal.inj_SortIterable
        (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» leftValues),
        SortVal.inj_SortIterable
        (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» rightValues) =>
        some (!(kEqual leftValues rightValues))
    | _, _ => none

/- Complete frozen `applyCmp` table. List/tuple membership is intentionally
   absent because the frozen semantics implements it as a configuration fold
   before `applyCmp`, not as a rule for this symbol. -/
noncomputable def applyCmp?
    (operator : SortString) (left right : SortVal) : Option SortBool :=
  if operator = "==" then equality? left right
  else if operator = "!=" then inequality? left right
  else if operator = "is" then
    match right with
    | SortVal.«noneV_MPY-CORE_Val» => some (kEqual left right)
    | _ => none
  else if operator = "is not" then
    match right with
    | SortVal.«noneV_MPY-CORE_Val» => some (!(kEqual left right))
    | _ => none
  else
    match left, right with
    | SortVal.inj_SortInt x, SortVal.inj_SortInt y =>
        if operator = "<" then some (decide (x < y))
        else if operator = "<=" then some (decide (x ≤ y))
        else if operator = ">" then some (decide (x > y))
        else if operator = ">=" then some (decide (x ≥ y))
        else none
    | SortVal.inj_SortFloat x, SortVal.inj_SortFloat y =>
        if operator = "<" then some (floatLt x y)
        else if operator = ">" then some (floatGt x y)
        else if operator = ">=" then some (!(floatLt x y))
        else if operator = "<=" then some (!(floatGt x y))
        else none
    | SortVal.inj_SortInt x, SortVal.inj_SortFloat y =>
        if operator = "<" then some (floatLt (intToFloat x) y)
        else if operator = ">" then some (floatGt (intToFloat x) y)
        else none
    | SortVal.inj_SortFloat x, SortVal.inj_SortInt y =>
        if operator = "<" then some (floatLt x (intToFloat y))
        else if operator = ">" then some (floatGt x (intToFloat y))
        else none
    | SortVal.inj_SortStr
        (SortStr.«str(_)_MPY-CORE_Str_IntSeq» leftCodes),
        SortVal.inj_SortStr
        (SortStr.«str(_)_MPY-CORE_Str_IntSeq» rightCodes) =>
        if operator = "in" then some (intSeqContains leftCodes rightCodes)
        else if operator = "not in" then
          some (!(intSeqContains leftCodes rightCodes))
        else if operator = "<" then some (intSeqLt leftCodes rightCodes)
        else if operator = ">" then some (intSeqLt rightCodes leftCodes)
        else if operator = "<=" then some (!(intSeqLt rightCodes leftCodes))
        else if operator = ">=" then some (!(intSeqLt leftCodes rightCodes))
        else none
    | _, _ => none

noncomputable def applyBin
    (operator : SortString) (left right : SortVal) : SortVal :=
  (applyBin? operator left right).getD SortVal.«noneV_MPY-CORE_Val»

noncomputable def applyCmp
    (operator : SortString) (left right : SortVal) : SortBool :=
  (applyCmp? operator left right).getD false

def definedProjectBool : SortVal → SortBool
  | SortVal.inj_SortBool _ => true
  | _ => false

def definedProjectFloat : SortVal → SortBool
  | SortVal.inj_SortFloat _ => true
  | _ => false

def definedProjectInt : SortVal → SortBool
  | SortVal.inj_SortInt _ => true
  | _ => false

def isNumberVal : SortVal → SortBool
  | SortVal.inj_SortInt _ => true
  | SortVal.inj_SortBool _ => true
  | SortVal.inj_SortFloat _ => true
  | _ => false

def intEven (x : SortInt) : SortBool :=
  match pyMod x 2 with
  | some remainder => remainder == 0
  | none => false

def numberEven : SortVal → SortBool
  | SortVal.inj_SortInt x => intEven x
  | SortVal.inj_SortBool x => intEven (boolToInt x)
  | SortVal.inj_SortFloat x => floatEq (floatModTwo x) (0.0 : SortFloat)
  | _ => false

def projectBool? : SortK → Option SortBool
  | SortK.kseq (SortKItem.inj_SortBool value) SortK.dotk => some value
  | _ => none

def projectFloat? : SortK → Option SortFloat
  | SortK.kseq (SortKItem.inj_SortFloat value) SortK.dotk => some value
  | _ => none

def projectInt? : SortK → Option SortInt
  | SortK.kseq (SortKItem.inj_SortInt value) SortK.dotk => some value
  | _ => none

end ProofModel
