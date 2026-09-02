import Klean81NumericalLetterGrade.Lemmas
import Klean81NumericalLetterGrade.Func

namespace Proof

/- Total observations of the three frozen K hooks used by numeric comparison.
   Klean represents a potentially undefined hook application with `Option`; the
   frozen K declarations are total on these argument sorts, while `false` is
   the conservative totalization if a generated hook model returns `none`. -/
private noncomputable def cmpFloatEq (a b : SortFloat) : SortBool :=
  (_root_.«_==Float_» a b).getD false

private noncomputable def cmpFloatGt (a b : SortFloat) : SortBool :=
  (_root_.«_>Float__FLOAT_Bool_Float_Float» a b).getD false

private noncomputable def cmpPromoteInt (i : SortInt) : Option SortFloat :=
  _root_.«Int2Float(_,_,_)_FLOAT_Float_Int_Int_Int» i 53 11

private noncomputable def cmpIntFloatEq (i : SortInt) (f : SortFloat) : SortBool :=
  match cmpPromoteInt i with
  | some promoted => cmpFloatEq promoted f
  | none => false

private noncomputable def cmpFloatIntEq (f : SortFloat) (i : SortInt) : SortBool :=
  match cmpPromoteInt i with
  | some promoted => cmpFloatEq f promoted
  | none => false

private noncomputable def cmpIntFloatLt (i : SortInt) (f : SortFloat) : SortBool :=
  match cmpPromoteInt i with
  | some promoted => cmpFloatGt f promoted
  | none => false

private noncomputable def cmpFloatIntLt (f : SortFloat) (i : SortInt) : SortBool :=
  match cmpPromoteInt i with
  | some promoted => cmpFloatGt promoted f
  | none => false

private noncomputable def cmpFloatIntGt (f : SortFloat) (i : SortInt) : SortBool :=
  match cmpPromoteInt i with
  | some promoted => cmpFloatGt f promoted
  | none => false

private noncomputable def cmpGradeEqImpl (v : SortVal) (f : SortFloat) : SortBool :=
  match v with
  | SortVal.inj_SortInt i => cmpIntFloatEq i f
  | SortVal.inj_SortFloat g => cmpFloatEq g f
  | _ => false

private noncomputable def cmpGradeGtImpl (v : SortVal) (f : SortFloat) : SortBool :=
  match v with
  | SortVal.inj_SortInt i =>
      match cmpPromoteInt i with
      | some promoted => cmpFloatGt promoted f
      | none => false
  | SortVal.inj_SortFloat g => cmpFloatGt g f
  | _ => false

private def cmpIsGradeNumberImpl (v : SortVal) : SortBool :=
  match v with
  | SortVal.inj_SortInt _ => true
  | SortVal.inj_SortFloat _ => true
  | _ => false

/- `==K` is equality of K terms.  Structural equality of the generated Lean
   constructors is its direct model, including for arbitrary dictionary keys
   and nested list/tuple elements. -/
private noncomputable def cmpKTermEq {α : Type} (a b : α) : SortBool :=
  letI : DecidableEq α := Classical.typeDecidableEq α
  decide (a = b)

private def cmpIntSeqEq : SortIntSeq → SortIntSeq → SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»,
      SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => true
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» a as,
      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» b bs =>
      (a == b) && cmpIntSeqEq as bs
  | _, _ => false

private def cmpStringPrefix : SortIntSeq → SortIntSeq → SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _ => true
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ _,
      SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => false
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» a as,
      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» b bs =>
      (a == b) && cmpStringPrefix as bs

private def cmpStringContains (pattern : SortIntSeq) : SortIntSeq → SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» =>
      cmpStringPrefix pattern SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
  | whole@(SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ rest) =>
      if cmpStringPrefix pattern whole = true then true
      else cmpStringContains pattern rest

private def cmpStringLt : SortIntSeq → SortIntSeq → SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»,
      SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => false
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»,
      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ _ => true
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ _,
      SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => false
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» a as,
      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» b bs =>
      if a < b then true else if a > b then false else cmpStringLt as bs

private def cmpCodeMember (code : SortInt) : SortIntSeq → SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => false
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head tail =>
      (code == head) || cmpCodeMember code tail

private def cmpSetSubset : SortIntSeq → SortIntSeq → SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _ => true
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» code rest, other =>
      cmpCodeMember code other && cmpSetSubset rest other

private def cmpSameSet (a b : SortIntSeq) : SortBool :=
  cmpSetSubset a b && cmpSetSubset b a

private def cmpValSeqLength : SortValSeq → Nat
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => 0
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _ rest =>
      cmpValSeqLength rest + 1

private noncomputable def cmpDictLookup :
    SortValSeq → SortValSeq → SortVal → Option SortVal
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» key keys,
      SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» value values, wanted =>
      if cmpKTermEq key wanted = true then some value
      else cmpDictLookup keys values wanted
  | _, _, _ => none

private noncomputable def cmpDictSubset :
    SortValSeq → SortValSeq → SortValSeq → SortValSeq → SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq»,
      SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _, _ => true
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» key keys,
      SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» value values,
      otherKeys, otherValues =>
      match cmpDictLookup otherKeys otherValues key with
      | some found =>
          cmpKTermEq found value &&
            cmpDictSubset keys values otherKeys otherValues
      | none => false
  | _, _, _, _ => false

private noncomputable def cmpDictEq
    (keys₁ values₁ keys₂ values₂ : SortValSeq) : SortBool :=
  (cmpValSeqLength keys₁ == cmpValSeqLength keys₂) &&
    cmpDictSubset keys₁ values₁ keys₂ values₂

private def cmpIsNone : SortVal → SortBool
  | SortVal.«noneV_MPY-CORE_Val» => true
  | _ => false

/- KORE symbol: LblapplyCmp'LParUndsCommUndsCommUndsRParUnds'MPY-CORE'Unds'Bool'Unds'String'Unds'Val'Unds'Val; frozen source obligations: rule-bb0819476c6343e9119c99a78b2ae8eb72ebad42dbc170a9eaa3c4af6f39f115, rule-79c1c8d9ff74acff507b7b4a319ee7d9d034df3550afdf9196f29291297713c8. Replace this stub with its honest total meaning from the frozen K semantics. -/
noncomputable def «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»
    (op : SortString) (lhs rhs : SortVal) : SortBool :=
  match lhs, rhs with
  | value, SortVal.«noneV_MPY-CORE_Val» =>
      if op = "==" then cmpIsNone value
      else if op = "!=" then !cmpIsNone value
      else if op = "is" then cmpIsNone value
      else if op = "is not" then !cmpIsNone value
      else false
  | SortVal.inj_SortBool a, SortVal.inj_SortBool b =>
      if op = "==" then a == b
      else if op = "!=" then !(a == b)
      else false
  | SortVal.inj_SortInt a, SortVal.inj_SortInt b =>
      if op = "<" then decide (a < b)
      else if op = "<=" then decide (a ≤ b)
      else if op = ">" then decide (a > b)
      else if op = ">=" then decide (a ≥ b)
      else if op = "==" then a == b
      else if op = "!=" then !(a == b)
      else false
  | value@(SortVal.inj_SortInt i), SortVal.inj_SortFloat f =>
      if op = "==" then cmpGradeEqImpl value f
      else if op = "!=" then !cmpGradeEqImpl value f
      else if op = "<" then cmpIntFloatLt i f
      else if op = ">" then cmpGradeGtImpl value f
      else false
  | SortVal.inj_SortFloat f, SortVal.inj_SortInt i =>
      if op = "==" then cmpFloatIntEq f i
      else if op = "!=" then !cmpFloatIntEq f i
      else if op = "<" then cmpFloatIntLt f i
      else if op = ">" then cmpFloatIntGt f i
      else false
  | value@(SortVal.inj_SortFloat a), SortVal.inj_SortFloat b =>
      if op = "==" then cmpGradeEqImpl value b
      else if op = "!=" then !cmpGradeEqImpl value b
      else if op = "<" then cmpFloatGt b a
      else if op = ">" then cmpGradeGtImpl value b
      else if op = ">=" then !cmpFloatGt b a
      else if op = "<=" then !cmpFloatGt a b
      else false
  | SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» a),
      SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» b) =>
      if op = "==" then cmpIntSeqEq a b
      else if op = "!=" then !cmpIntSeqEq a b
      else if op = "in" then cmpStringContains a b
      else if op = "not in" then !cmpStringContains a b
      else if op = "<" then cmpStringLt a b
      else if op = ">" then cmpStringLt b a
      else if op = "<=" then !cmpStringLt b a
      else if op = ">=" then !cmpStringLt a b
      else false
  | SortVal.inj_SortIterable
        (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» a),
      SortVal.inj_SortIterable
        (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» b) =>
      if op = "==" then cmpKTermEq a b
      else if op = "!=" then !cmpKTermEq a b
      else false
  | SortVal.inj_SortIterable
        (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» a),
      SortVal.inj_SortIterable
        (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» b) =>
      if op = "==" then cmpKTermEq a b
      else if op = "!=" then !cmpKTermEq a b
      else false
  | SortVal.«setV(_)_MPY-SET_Val_IntSeq» a,
      SortVal.«setV(_)_MPY-SET_Val_IntSeq» b =>
      if op = "==" then cmpSameSet a b else false
  | SortVal.«dictV(_,_)_MPY-DICT_Val_ValSeq_ValSeq» keys₁ values₁,
      SortVal.«dictV(_,_)_MPY-DICT_Val_ValSeq_ValSeq» keys₂ values₂ =>
      if op = "==" then cmpDictEq keys₁ values₁ keys₂ values₂ else false
  | _, _ => false
/- KORE symbol: LblgradeEq'LParUndsCommUndsRParUnds'VERIFICATION'Unds'Bool'Unds'Val'Unds'Float; frozen source obligations: rule-bb0819476c6343e9119c99a78b2ae8eb72ebad42dbc170a9eaa3c4af6f39f115. Replace this stub with its honest total meaning from the frozen K semantics. -/
noncomputable def «gradeEq(_,_)_VERIFICATION_Bool_Val_Float»
    (v : SortVal) (f : SortFloat) : SortBool :=
  cmpGradeEqImpl v f
/- KORE symbol: LblgradeGt'LParUndsCommUndsRParUnds'VERIFICATION'Unds'Bool'Unds'Val'Unds'Float; frozen source obligations: rule-79c1c8d9ff74acff507b7b4a319ee7d9d034df3550afdf9196f29291297713c8. Replace this stub with its honest total meaning from the frozen K semantics. -/
noncomputable def «gradeGt(_,_)_VERIFICATION_Bool_Val_Float»
    (v : SortVal) (f : SortFloat) : SortBool :=
  cmpGradeGtImpl v f
/- KORE symbol: LblisGradeNumber'LParUndsRParUnds'VERIFICATION'Unds'Bool'Unds'Val; frozen source obligations: rule-bb0819476c6343e9119c99a78b2ae8eb72ebad42dbc170a9eaa3c4af6f39f115, rule-79c1c8d9ff74acff507b7b4a319ee7d9d034df3550afdf9196f29291297713c8. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «isGradeNumber(_)_VERIFICATION_Bool_Val» (v : SortVal) : SortBool :=
  cmpIsGradeNumberImpl v

theorem final :
    Klean81NumericalLetterGrade.Lemmas.targetStatement «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» «gradeEq(_,_)_VERIFICATION_Bool_Val_Float» «gradeGt(_,_)_VERIFICATION_Bool_Val_Float» «isGradeNumber(_)_VERIFICATION_Bool_Val» := by
  constructor
  · intro F V h
    cases V <;>
      simp [«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»,
        «gradeEq(_,_)_VERIFICATION_Bool_Val_Float»,
        «isGradeNumber(_)_VERIFICATION_Bool_Val»,
        cmpIsGradeNumberImpl] at h ⊢
  · intro F V h
    cases V <;>
      simp [«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»,
        «gradeGt(_,_)_VERIFICATION_Bool_Val_Float»,
        «isGradeNumber(_)_VERIFICATION_Bool_Val»,
        cmpIsGradeNumberImpl] at h ⊢

end Proof
