import Klean95CheckDictCase.Lemmas
import Proof.Operational

namespace Proof

/- KORE symbol: Lbl'Unds'andBool'Unds'; frozen source obligations: rule-abdbb3ec2ce0c337fa0e067accc49ce82c1571492380cf994657b7bb2f038b5c, rule-fd44f126befee86dadbf8dd8073de5b8f775b3f5479a88c614b7f274860a0b8c. Replace this stub with its honest total meaning from the frozen K semantics. -/
def _andBool_ (left right : SortBool) : SortBool :=
  left && right
/- KORE symbol: LblapplyMethod'LParUndsCommUndsCommUndsRParUnds'MPY-METHODS'Unds'Val'Unds'Val'Unds'String'Unds'Vals; frozen source obligations: rule-abdbb3ec2ce0c337fa0e067accc49ce82c1571492380cf994657b7bb2f038b5c, rule-fd44f126befee86dadbf8dd8073de5b8f775b3f5479a88c614b7f274860a0b8c. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «applyMethod(_,_,_)_MPY-METHODS_Val_Val_String_Vals»
    (receiver : SortVal) (method : SortString) (arguments : SortVals) : SortVal :=
  Operational.dispatchRepresentableMethod receiver method arguments
/- KORE symbol: LblisRefV'LParUndsRParUnds'MPY-CORE'Unds'Bool'Unds'Val; frozen source obligations: rule-abdbb3ec2ce0c337fa0e067accc49ce82c1571492380cf994657b7bb2f038b5c, rule-fd44f126befee86dadbf8dd8073de5b8f775b3f5479a88c614b7f274860a0b8c. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «isRefV(_)_MPY-CORE_Bool_Val» : SortVal → SortBool
  | SortVal.«ref(_)_MPY-CORE_Val_Int» _ => true
  | _ => false
/- KORE symbol: LblisStringKey'LParUndsRParUnds'PROOF-THEORY'Unds'Bool'Unds'Val; frozen source obligations: rule-abdbb3ec2ce0c337fa0e067accc49ce82c1571492380cf994657b7bb2f038b5c, rule-fd44f126befee86dadbf8dd8073de5b8f775b3f5479a88c614b7f274860a0b8c. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «isStringKey(_)_PROOF-THEORY_Bool_Val» : SortVal → SortBool
  | SortVal.inj_SortStr _ => true
  | SortVal.inj_SortIterable (SortIterable.inj_SortStr _) => true
  | _ => false
/- KORE symbol: LbllowerKeyCodes'LParUndsRParUnds'PROOF-THEORY'Unds'Bool'Unds'IntSeq; frozen source obligations: rule-abdbb3ec2ce0c337fa0e067accc49ce82c1571492380cf994657b7bb2f038b5c. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «lowerKeyCodes(_)_PROOF-THEORY_Bool_IntSeq» (codes : SortIntSeq) : SortBool :=
  Operational.hasLowerCode codes && !Operational.hasUpperCode codes
/- KORE symbol: LblnotBool'Unds'; frozen source obligations: rule-abdbb3ec2ce0c337fa0e067accc49ce82c1571492380cf994657b7bb2f038b5c, rule-fd44f126befee86dadbf8dd8073de5b8f775b3f5479a88c614b7f274860a0b8c. Replace this stub with its honest total meaning from the frozen K semantics. -/
def notBool_ (value : SortBool) : SortBool :=
  !value
/- KORE symbol: LblstringCodes; frozen source obligations: rule-abdbb3ec2ce0c337fa0e067accc49ce82c1571492380cf994657b7bb2f038b5c, rule-fd44f126befee86dadbf8dd8073de5b8f775b3f5479a88c614b7f274860a0b8c. Replace this stub with its honest total meaning from the frozen K semantics. -/
def stringCodes (value : SortVal) : SortIntSeq :=
  Operational.totalStringCodes value
/- KORE symbol: LblupperKeyCodes'LParUndsRParUnds'PROOF-THEORY'Unds'Bool'Unds'IntSeq; frozen source obligations: rule-fd44f126befee86dadbf8dd8073de5b8f775b3f5479a88c614b7f274860a0b8c. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «upperKeyCodes(_)_PROOF-THEORY_Bool_IntSeq» (codes : SortIntSeq) : SortBool :=
  Operational.hasUpperCode codes && !Operational.hasLowerCode codes

theorem final :
    Klean95CheckDictCase.Lemmas.targetStatement _andBool_ «applyMethod(_,_,_)_MPY-METHODS_Val_Val_String_Vals» «isRefV(_)_MPY-CORE_Bool_Val» «isStringKey(_)_PROOF-THEORY_Bool_Val» «lowerKeyCodes(_)_PROOF-THEORY_Bool_IntSeq» notBool_ stringCodes «upperKeyCodes(_)_PROOF-THEORY_Bool_IntSeq» := by
  constructor <;> intro V h <;>
    cases V <;>
      simp [_andBool_, «isStringKey(_)_PROOF-THEORY_Bool_Val»,
        «isRefV(_)_MPY-CORE_Bool_Val»] at h
  all_goals
    rename_i value
    cases value <;>
      simp_all [notBool_] <;>
      try rfl
  all_goals
    rename_i stringValue
    cases stringValue
    rfl

end Proof
