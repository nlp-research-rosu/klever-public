import Proof.Operational

namespace Proof

/- KORE symbol: LblapplyMethod'LParUndsCommUndsCommUndsRParUnds'MPY-METHODS'Unds'Val'Unds'Val'Unds'String'Unds'Vals; frozen source obligations: rule-9c06989c16c7a097c03e07267ceaa4fc5afd44c87f6099c4345fad7d4fc52617. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «applyMethod(_,_,_)_MPY-METHODS_Val_Val_String_Vals» :
    SortVal → SortString → SortVals → SortVal :=
  Operational.dispatchMethodMeaning

/- KORE symbol: LblcntSub'LParUndsCommUndsRParUnds'MPY-METHODS'Unds'Int'Unds'IntSeq'Unds'IntSeq; frozen source obligations: rule-9c06989c16c7a097c03e07267ceaa4fc5afd44c87f6099c4345fad7d4fc52617. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «cntSub(_,_)_MPY-METHODS_Int_IntSeq_IntSeq» :
    SortIntSeq → SortIntSeq → SortInt :=
  Operational.nonoverlapSubstringCount

/- KORE symbol: LblisStringVal'LParUndsRParUnds'VERIFICATION-SYNTAX'Unds'Bool'Unds'Val; frozen source obligations: rule-9c06989c16c7a097c03e07267ceaa4fc5afd44c87f6099c4345fad7d4fc52617. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «isStringVal(_)_VERIFICATION-SYNTAX_Bool_Val» :
    SortVal → SortBool :=
  Operational.recognizesStringValue

/- KORE symbol: LblstringCodes; frozen source obligations: rule-9c06989c16c7a097c03e07267ceaa4fc5afd44c87f6099c4345fad7d4fc52617. Replace this stub with its honest total meaning from the frozen K semantics. -/
def stringCodes : SortVal → SortIntSeq :=
  Operational.projectStringCodeSequence

theorem final :
    Klean113OddCount.Lemmas.targetStatement «applyMethod(_,_,_)_MPY-METHODS_Val_Val_String_Vals» «cntSub(_,_)_MPY-METHODS_Int_IntSeq_IntSeq» «isStringVal(_)_VERIFICATION-SYNTAX_Bool_Val» stringCodes := by
  intro pattern value h
  cases value <;> try { cases h }
  case inj_SortStr stringValue =>
    cases stringValue
    rfl

end Proof
