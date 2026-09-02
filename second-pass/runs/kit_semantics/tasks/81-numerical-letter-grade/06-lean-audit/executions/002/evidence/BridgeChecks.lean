import Proof

namespace AuditBridgeChecks

example (i : SortInt) :
    Proof.«isGradeNumber(_)_VERIFICATION_Bool_Val» (SortVal.inj_SortInt i) = true := rfl

example (f : SortFloat) :
    Proof.«isGradeNumber(_)_VERIFICATION_Bool_Val» (SortVal.inj_SortFloat f) = true := rfl

example :
    Proof.«isGradeNumber(_)_VERIFICATION_Bool_Val» SortVal.«noneV_MPY-CORE_Val» = false := rfl

example (i : SortInt) (f : SortFloat) :
    Proof.«gradeEq(_,_)_VERIFICATION_Bool_Val_Float» (SortVal.inj_SortInt i) f =
      match _root_.«Int2Float(_,_,_)_FLOAT_Float_Int_Int_Int» i 53 11 with
      | some promoted => (_root_.«_==Float_» promoted f).getD false
      | none => false := rfl

example (g f : SortFloat) :
    Proof.«gradeEq(_,_)_VERIFICATION_Bool_Val_Float» (SortVal.inj_SortFloat g) f =
      (_root_.«_==Float_» g f).getD false := rfl

example :
    Proof.«gradeEq(_,_)_VERIFICATION_Bool_Val_Float» SortVal.«noneV_MPY-CORE_Val» 4.0 = false := rfl

example (i : SortInt) (f : SortFloat) :
    Proof.«gradeGt(_,_)_VERIFICATION_Bool_Val_Float» (SortVal.inj_SortInt i) f =
      match _root_.«Int2Float(_,_,_)_FLOAT_Float_Int_Int_Int» i 53 11 with
      | some promoted => (_root_.«_>Float__FLOAT_Bool_Float_Float» promoted f).getD false
      | none => false := rfl

example (g f : SortFloat) :
    Proof.«gradeGt(_,_)_VERIFICATION_Bool_Val_Float» (SortVal.inj_SortFloat g) f =
      (_root_.«_>Float__FLOAT_Bool_Float_Float» g f).getD false := rfl

example :
    Proof.«gradeGt(_,_)_VERIFICATION_Bool_Val_Float» SortVal.«noneV_MPY-CORE_Val» 0.0 = false := rfl

example (i : SortInt) (f : SortFloat) :
    Proof.«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»
        "==" (SortVal.inj_SortInt i) (SortVal.inj_SortFloat f) =
      Proof.«gradeEq(_,_)_VERIFICATION_Bool_Val_Float» (SortVal.inj_SortInt i) f := rfl

example (g f : SortFloat) :
    Proof.«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»
        "==" (SortVal.inj_SortFloat g) (SortVal.inj_SortFloat f) =
      Proof.«gradeEq(_,_)_VERIFICATION_Bool_Val_Float» (SortVal.inj_SortFloat g) f := rfl

example (i : SortInt) (f : SortFloat) :
    Proof.«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»
        ">" (SortVal.inj_SortInt i) (SortVal.inj_SortFloat f) =
      Proof.«gradeGt(_,_)_VERIFICATION_Bool_Val_Float» (SortVal.inj_SortInt i) f := rfl

example (g f : SortFloat) :
    Proof.«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»
        ">" (SortVal.inj_SortFloat g) (SortVal.inj_SortFloat f) =
      Proof.«gradeGt(_,_)_VERIFICATION_Bool_Val_Float» (SortVal.inj_SortFloat g) f := rfl

example (v : SortVal) :
    Proof.«isGradeNumber(_)_VERIFICATION_Bool_Val» v =
      (_root_.«isGradeNumber(_)_VERIFICATION_Bool_Val» v).getD false := by
  cases v <;> rfl

end AuditBridgeChecks
