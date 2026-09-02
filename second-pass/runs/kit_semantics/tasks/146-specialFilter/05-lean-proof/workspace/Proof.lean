import Klean146Specialfilter.Lemmas

namespace Proof

/- KORE symbol: Lbl'Unds-GT-'Int'Unds'; frozen source obligations: rule-b16fd6610afeba9b173c4b9ae74c4766789b5284e03220a93a65bb86fd2ce505. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_>Int_» (left right : SortInt) : SortBool := left > right

/- KORE symbol: LblInt2String'LParUndsRParUnds'STRING-COMMON'Unds'String'Unds'Int; frozen source obligations: rule-532e0f2fb29f7ffe39ef42a75e9b8dc647afc9a5bea5118d59efc91aa6fb0c2d. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «Int2String(_)_STRING-COMMON_String_Int» (value : SortInt) : SortString :=
  toString value

private def charsToIntSeq : List Char → SortIntSeq
  | [] => SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
  | char :: rest =>
      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq»
        (Int.ofNat char.toNat) (charsToIntSeq rest)

/- KORE symbol: LblstrToCodes'LParUndsRParUnds'MPY-STR'Unds'IntSeq'Unds'String; frozen source obligations: rule-532e0f2fb29f7ffe39ef42a75e9b8dc647afc9a5bea5118d59efc91aa6fb0c2d. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «strToCodes(_)_MPY-STR_IntSeq_String» (value : SortString) : SortIntSeq :=
  charsToIntSeq value.toList

/- KORE symbol: LbldefinedProjectInt'LParUndsRParUnds'VERIFICATION'Unds'Bool'Unds'Val; frozen source obligations: rule-0312858a8718cb93d212cdb7b679a2875534dc14191dff8edf7bccf9a96d8b43, rule-22fa1e67d4a05b75b5a578312159b0a4e049b756806628df2540b007f43bcb5d, rule-b16fd6610afeba9b173c4b9ae74c4766789b5284e03220a93a65bb86fd2ce505, rule-532e0f2fb29f7ffe39ef42a75e9b8dc647afc9a5bea5118d59efc91aa6fb0c2d. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «definedProjectInt(_)_VERIFICATION_Bool_Val» : SortVal → SortBool
  | SortVal.inj_SortInt _ => true
  | _ => false

private def projectIntOption : SortK → Option SortInt
  | SortK.kseq (SortKItem.inj_SortInt value) SortK.dotk => some value
  | _ => none

/- KORE symbol: Lblproject'Coln'Int; frozen source obligations: rule-0312858a8718cb93d212cdb7b679a2875534dc14191dff8edf7bccf9a96d8b43. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «project:Int?» (term : SortK) : Option SortInt :=
  projectIntOption term

/- KORE symbol: Lblproject'Coln'Int; frozen source obligations: rule-22fa1e67d4a05b75b5a578312159b0a4e049b756806628df2540b007f43bcb5d. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «project:Int» (term : SortK) : SortInt :=
  (projectIntOption term).getD 0

/- KORE symbol: LblprojectIntTotal; frozen source obligations: rule-22fa1e67d4a05b75b5a578312159b0a4e049b756806628df2540b007f43bcb5d, rule-b16fd6610afeba9b173c4b9ae74c4766789b5284e03220a93a65bb86fd2ce505, rule-532e0f2fb29f7ffe39ef42a75e9b8dc647afc9a5bea5118d59efc91aa6fb0c2d. Replace this stub with its honest total meaning from the frozen K semantics. -/
def projectIntTotal : SortVal → SortInt
  | SortVal.inj_SortInt value => value
  | _ => 0

private def compareInts (operator : SortString) (left right : SortInt) : SortBool :=
  match operator with
  | "<" => left < right
  | "<=" => left ≤ right
  | ">" => left > right
  | ">=" => left ≥ right
  | "==" => left == right
  | "!=" => left != right
  | _ => false

private def boolAsInt (value : SortBool) : SortInt :=
  if value then 1 else 0

private def intSeqEq : SortIntSeq → SortIntSeq → SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»,
      SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => true
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» left lefts,
      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» right rights =>
      left == right && intSeqEq lefts rights
  | _, _ => false

private def intSeqLt : SortIntSeq → SortIntSeq → SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»,
      SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => false
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»,
      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ _ => true
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ _,
      SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => false
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» left lefts,
      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» right rights =>
      if left < right then true
      else if left > right then false
      else intSeqLt lefts rights

private def compareStrings
    (operator : SortString) (left right : SortIntSeq) : SortBool :=
  match operator with
  | "==" => intSeqEq left right
  | "!=" => !(intSeqEq left right)
  | "<" => intSeqLt left right
  | ">" => intSeqLt right left
  | "<=" => !(intSeqLt right left)
  | ">=" => !(intSeqLt left right)
  | _ => false

/- KORE symbol: LblapplyCmp'LParUndsCommUndsCommUndsRParUnds'MPY-CORE'Unds'Bool'Unds'String'Unds'Val'Unds'Val; frozen source obligations: rule-b16fd6610afeba9b173c4b9ae74c4766789b5284e03220a93a65bb86fd2ce505. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»
    (operator : SortString) (left right : SortVal) : SortBool :=
  match left, right with
  | SortVal.inj_SortInt left, SortVal.inj_SortInt right =>
      compareInts operator left right
  | SortVal.inj_SortBool left, SortVal.inj_SortInt right =>
      compareInts operator (boolAsInt left) right
  | SortVal.inj_SortInt left, SortVal.inj_SortBool right =>
      compareInts operator left (boolAsInt right)
  | SortVal.inj_SortBool left, SortVal.inj_SortBool right =>
      compareInts operator (boolAsInt left) (boolAsInt right)
  | SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» left),
      SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» right) =>
      compareStrings operator left right
  | _, _ => false

private def singletonCode (value : SortInt) : SortIntSeq :=
  SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq»
    value SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»

/- KORE symbol: LblapplyBuiltin'LParUndsCommUndsRParUnds'MPY-BUILTINS'Unds'Val'Unds'String'Unds'Vals; frozen source obligations: rule-532e0f2fb29f7ffe39ef42a75e9b8dc647afc9a5bea5118d59efc91aa6fb0c2d. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «applyBuiltin(_,_)_MPY-BUILTINS_Val_String_Vals»
    (name : SortString) (arguments : SortVals) : SortVal :=
  match name, arguments with
  | "str",
      SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortInt value)
        SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
      SortVal.inj_SortStr
        (SortStr.«str(_)_MPY-CORE_Str_IntSeq»
          («strToCodes(_)_MPY-STR_IntSeq_String»
            («Int2String(_)_STRING-COMMON_String_Int» value)))
  | "str",
      SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortStr value)
        SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
      SortVal.inj_SortStr value
  | "int",
      SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortInt value)
        SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
      SortVal.inj_SortInt value
  | "ord",
      SortVals.«_,__MPY-CORE_Vals_Val_Vals»
        (SortVal.inj_SortStr
          (SortStr.«str(_)_MPY-CORE_Str_IntSeq» codes))
        SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
      match codes with
      | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» value
          SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» =>
          SortVal.inj_SortInt value
      | _ => SortVal.«noneV_MPY-CORE_Val»
  | "chr",
      SortVals.«_,__MPY-CORE_Vals_Val_Vals» (SortVal.inj_SortInt value)
        SortVals.«.List{"_,__MPY-CORE_Vals_Val_Vals"}_Vals» =>
      if 0 ≤ value ∧ value < 128 then
        SortVal.inj_SortStr
          (SortStr.«str(_)_MPY-CORE_Str_IntSeq» (singletonCode value))
      else
        SortVal.«noneV_MPY-CORE_Val»
  | _, _ => SortVal.«noneV_MPY-CORE_Val»

theorem final :
    Klean146Specialfilter.Lemmas.targetStatement «_>Int_» «Int2String(_)_STRING-COMMON_String_Int» «applyBuiltin(_,_)_MPY-BUILTINS_Val_String_Vals» «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» «definedProjectInt(_)_VERIFICATION_Bool_Val» «project:Int» projectIntTotal «strToCodes(_)_MPY-STR_IntSeq_String» «project:Int?» := by
  constructor
  · intro value
    cases value <;>
      exact ⟨fun present => ⟨present, True.intro⟩,
        fun defined => defined.1⟩
  constructor
  · intro value defined
    cases value <;> cases defined <;> rfl
  constructor
  · intro integer value defined
    cases value <;> cases defined <;> rfl
  · intro value defined
    cases value <;> cases defined <;> rfl

end Proof
