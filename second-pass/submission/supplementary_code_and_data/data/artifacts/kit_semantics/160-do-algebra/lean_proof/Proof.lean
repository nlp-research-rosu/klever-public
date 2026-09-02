import Proof.Operational

namespace Proof

/- KORE symbol: LblInt2String'LParUndsRParUnds'STRING-COMMON'Unds'String'Unds'Int; frozen source obligations: rule-532e0f2fb29f7ffe39ef42a75e9b8dc647afc9a5bea5118d59efc91aa6fb0c2d. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «Int2String(_)_STRING-COMMON_String_Int» (value : SortInt) :
    SortString :=
  toString value
/- KORE symbol: LblapplyBin'LParUndsCommUndsCommUndsRParUnds'MPY-CORE'Unds'Val'Unds'String'Unds'Val'Unds'Val; frozen source obligations: rule-732e3db12428149cde5df3649531def1390bb546c9e8bf72aa92ed954f7e9ea5. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val»
    (operator : SortString) (left right : SortVal) : SortVal :=
  Operational.modelApplyBin operator left right
/- KORE symbol: LblapplyBuiltin'LParUndsCommUndsRParUnds'MPY-BUILTINS'Unds'Val'Unds'String'Unds'Vals; frozen source obligations: rule-532e0f2fb29f7ffe39ef42a75e9b8dc647afc9a5bea5118d59efc91aa6fb0c2d. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «applyBuiltin(_,_)_MPY-BUILTINS_Val_String_Vals»
    (builtin : SortString) (arguments : SortVals) : SortVal :=
  Operational.modelApplyBuiltin builtin arguments
/- KORE symbol: LblcodesProject'LParUndsRParUnds'VERIFICATION-SYNTAX'Unds'IntSeq'Unds'Val; frozen source obligations: rule-732e3db12428149cde5df3649531def1390bb546c9e8bf72aa92ed954f7e9ea5. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «codesProject(_)_VERIFICATION-SYNTAX_IntSeq_Val»
    (value : SortVal) : SortIntSeq :=
  Operational.modelStringCodesOfValue value
/- KORE symbol: LbldefinedProjectInt'LParUndsRParUnds'VERIFICATION-SYNTAX'Unds'Bool'Unds'Val; frozen source obligations: rule-0312858a8718cb93d212cdb7b679a2875534dc14191dff8edf7bccf9a96d8b43, rule-532e0f2fb29f7ffe39ef42a75e9b8dc647afc9a5bea5118d59efc91aa6fb0c2d. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «definedProjectInt(_)_VERIFICATION-SYNTAX_Bool_Val» :
    SortVal → SortBool
  | SortVal.inj_SortInt _ => true
  | _ => false
/- KORE symbol: LbldefinedProjectStr'LParUndsRParUnds'VERIFICATION-SYNTAX'Unds'Bool'Unds'Val; frozen source obligations: rule-0dda33275c7cbd1779ea25ffe3285879bf6652eca3210dd703138ffe06f5bf83, rule-732e3db12428149cde5df3649531def1390bb546c9e8bf72aa92ed954f7e9ea5. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «definedProjectStr(_)_VERIFICATION-SYNTAX_Bool_Val» :
    SortVal → SortBool
  | SortVal.inj_SortStr _ => true
  | _ => false
/- KORE symbol: LblprojectIntTotal; frozen source obligations: rule-532e0f2fb29f7ffe39ef42a75e9b8dc647afc9a5bea5118d59efc91aa6fb0c2d. Replace this stub with its honest total meaning from the frozen K semantics. -/
def projectIntTotal : SortVal → SortInt
  | SortVal.inj_SortInt value => value
  | _ => 0
/- KORE symbol: LblseqConcat'LParUndsCommUndsRParUnds'MPY-STR'Unds'IntSeq'Unds'IntSeq'Unds'IntSeq; frozen source obligations: rule-732e3db12428149cde5df3649531def1390bb546c9e8bf72aa92ed954f7e9ea5. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq»
    (left right : SortIntSeq) : SortIntSeq :=
  Operational.modelIntSeqAppend left right
/- KORE symbol: LblstrToCodes'LParUndsRParUnds'MPY-STR'Unds'IntSeq'Unds'String; frozen source obligations: rule-532e0f2fb29f7ffe39ef42a75e9b8dc647afc9a5bea5118d59efc91aa6fb0c2d. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «strToCodes(_)_MPY-STR_IntSeq_String»
    (text : SortString) : SortIntSeq :=
  Operational.modelStringCodes text
/- KORE symbol: Lblproject'Coln'Int; frozen source obligations: rule-0312858a8718cb93d212cdb7b679a2875534dc14191dff8edf7bccf9a96d8b43. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «project:Int?» : SortK → Option SortInt
  | SortK.kseq (SortKItem.inj_SortInt value) SortK.dotk =>
      some value
  | _ => none
/- KORE symbol: Lblproject'Coln'Str; frozen source obligations: rule-0dda33275c7cbd1779ea25ffe3285879bf6652eca3210dd703138ffe06f5bf83. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «project:Str?» : SortK → Option SortStr
  | SortK.kseq (SortKItem.inj_SortStr value) SortK.dotk =>
      some value
  | _ => none

theorem final :
    Klean160DoAlgebra.Lemmas.targetStatement «Int2String(_)_STRING-COMMON_String_Int» «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» «applyBuiltin(_,_)_MPY-BUILTINS_Val_String_Vals» «codesProject(_)_VERIFICATION-SYNTAX_IntSeq_Val» «definedProjectInt(_)_VERIFICATION-SYNTAX_Bool_Val» «definedProjectStr(_)_VERIFICATION-SYNTAX_Bool_Val» projectIntTotal «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» «strToCodes(_)_MPY-STR_IntSeq_String» «project:Int?» «project:Str?» := by
  constructor
  · intro value
    cases value <;>
      simp [«project:Int?»,
        «definedProjectInt(_)_VERIFICATION-SYNTAX_Bool_Val», inj]
  constructor
  · intro value
    cases value <;>
      simp [«project:Str?»,
        «definedProjectStr(_)_VERIFICATION-SYNTAX_Bool_Val», inj]
  constructor
  · intro value hypothesis
    cases value <;>
      simp [«definedProjectInt(_)_VERIFICATION-SYNTAX_Bool_Val»]
        at hypothesis <;>
      rfl
  · intro value codes hypothesis
    cases value <;>
      simp [«definedProjectStr(_)_VERIFICATION-SYNTAX_Bool_Val»]
        at hypothesis <;>
      rfl

end Proof
