import Klean30GetPositive.Func
import Klean30GetPositive.Lemmas

namespace Proof

private noncomputable def totalIntToFloat (value : SortInt) : SortFloat :=
  (intToF value).getD (0.0 : Float)

private noncomputable def totalFloatGreater
    (left right : SortFloat) : SortBool :=
  (gtF left right).getD false

/- KORE symbol: LblapplyCmp'LParUndsCommUndsCommUndsRParUnds'MPY-CORE'Unds'Bool'Unds'String'Unds'Val'Unds'Val; frozen source obligations: rule-34f56aec2aa3edbac282cf16b737d75ec1da43edea47cc5bccecc9d81dad9db0. Replace this stub with its honest total meaning from the frozen K semantics. -/
noncomputable def «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»
    : SortString → SortVal → SortVal → SortBool
  | ">", SortVal.inj_SortInt left, SortVal.inj_SortInt right =>
      decide (left > right)
  | ">", SortVal.inj_SortInt left, SortVal.inj_SortFloat right =>
      totalFloatGreater (totalIntToFloat left) right
  | ">", SortVal.inj_SortFloat left, SortVal.inj_SortInt right =>
      totalFloatGreater left (totalIntToFloat right)
  | ">", SortVal.inj_SortFloat left, SortVal.inj_SortFloat right =>
      totalFloatGreater left right
  | _, _, _ => false

/- KORE symbol: LblnumericVal'LParUndsRParUnds'VERIFICATION-BASE'Unds'Bool'Unds'Val; frozen source obligations: rule-34f56aec2aa3edbac282cf16b737d75ec1da43edea47cc5bccecc9d81dad9db0. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «numericVal(_)_VERIFICATION-BASE_Bool_Val» : SortVal → SortBool
  | SortVal.inj_SortInt _ => true
  | SortVal.inj_SortFloat _ => true
  | _ => false

/- KORE symbol: LblpositiveNumeric'LParUndsRParUnds'VERIFICATION-BASE'Unds'Bool'Unds'Val; frozen source obligations: rule-34f56aec2aa3edbac282cf16b737d75ec1da43edea47cc5bccecc9d81dad9db0. Replace this stub with its honest total meaning from the frozen K semantics. -/
noncomputable def «positiveNumeric(_)_VERIFICATION-BASE_Bool_Val»
    : SortVal → SortBool
  | SortVal.inj_SortInt value =>
      totalFloatGreater (totalIntToFloat value) (0.0 : Float)
  | SortVal.inj_SortFloat value =>
      totalFloatGreater value (0.0 : Float)
  | _ => false

theorem final :
    Klean30GetPositive.Lemmas.targetStatement «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» «numericVal(_)_VERIFICATION-BASE_Bool_Val» «positiveNumeric(_)_VERIFICATION-BASE_Bool_Val» := by
  intro V h
  cases V <;>
    simp_all [
      «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»,
      «numericVal(_)_VERIFICATION-BASE_Bool_Val»,
      «positiveNumeric(_)_VERIFICATION-BASE_Bool_Val»
    ]

end Proof
