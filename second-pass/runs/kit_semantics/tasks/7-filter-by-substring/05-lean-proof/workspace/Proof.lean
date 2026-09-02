import Klean7FilterBySubstring.Lemmas

namespace Proof

/- KORE symbol: LblapplyCmp'LParUndsCommUndsCommUndsRParUnds'MPY-CORE'Unds'Bool'Unds'String'Unds'Val'Unds'Val; frozen source obligations: rule-ce7624945e06d02ae5606649e897ef6ded8e343e6c0ed28075613044c8e40503. Replace this stub with its honest total meaning from the frozen K semantics. -/
private def intSeqEq : SortIntSeq → SortIntSeq → Bool
  | .«.IntSeq_MPY-CORE_IntSeq», .«.IntSeq_MPY-CORE_IntSeq» => true
  | .«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» a as,
      .«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» b bs =>
      a == b && intSeqEq as bs
  | _, _ => false

private def intSeqPrefix : SortIntSeq → SortIntSeq → Bool
  | .«.IntSeq_MPY-CORE_IntSeq», _ => true
  | .«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ _,
      .«.IntSeq_MPY-CORE_IntSeq» => false
  | .«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» a as,
      .«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» b bs =>
      a == b && intSeqPrefix as bs

private def intSeqContains (pattern : SortIntSeq) : SortIntSeq → Bool
  | .«.IntSeq_MPY-CORE_IntSeq» =>
      intSeqPrefix pattern .«.IntSeq_MPY-CORE_IntSeq»
  | whole@(.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ rest) =>
      intSeqPrefix pattern whole || intSeqContains pattern rest

private def intSeqLt : SortIntSeq → SortIntSeq → Bool
  | .«.IntSeq_MPY-CORE_IntSeq», .«.IntSeq_MPY-CORE_IntSeq» => false
  | .«.IntSeq_MPY-CORE_IntSeq»,
      .«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ _ => true
  | .«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ _,
      .«.IntSeq_MPY-CORE_IntSeq» => false
  | .«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» a as,
      .«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» b bs =>
      if a < b then true else if a > b then false else intSeqLt as bs

private def codeIn (code : SortInt) : SortIntSeq → Bool
  | .«.IntSeq_MPY-CORE_IntSeq» => false
  | .«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head tail =>
      code == head || codeIn code tail

private def intSeqSubset : SortIntSeq → SortIntSeq → Bool
  | .«.IntSeq_MPY-CORE_IntSeq», _ => true
  | .«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» head tail, other =>
      codeIn head other && intSeqSubset tail other

private def sameSet (left right : SortIntSeq) : Bool :=
  intSeqSubset left right && intSeqSubset right left

private def valSeqLength : SortValSeq → Nat
  | .«.ValSeq_MPY-CORE_ValSeq» => 0
  | .«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _ tail =>
      valSeqLength tail + 1

private noncomputable def eqBool {α : Type} (left right : α) : Bool :=
  match Classical.typeDecidableEq α left right with
  | isTrue _ => true
  | isFalse _ => false

private noncomputable def dictLookup
    (keys values : SortValSeq) (needle : SortVal) : Option SortVal :=
  match keys, values with
  | .«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» key keyTail,
      .«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» value valueTail =>
      match Classical.typeDecidableEq SortVal key needle with
      | isTrue _ => some value
      | isFalse _ => dictLookup keyTail valueTail needle
  | _, _ => none

private noncomputable def dictSubset
    (keys values otherKeys otherValues : SortValSeq) : Bool :=
  match keys, values with
  | .«.ValSeq_MPY-CORE_ValSeq», .«.ValSeq_MPY-CORE_ValSeq» => true
  | .«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» key keyTail,
      .«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» value valueTail =>
      match dictLookup otherKeys otherValues key with
      | some otherValue =>
          eqBool otherValue value &&
            dictSubset keyTail valueTail otherKeys otherValues
      | none => false
  | _, _ => false

private noncomputable def dictEq
    (keys₁ values₁ keys₂ values₂ : SortValSeq) : Bool :=
  valSeqLength keys₁ == valSeqLength keys₂ &&
    dictSubset keys₁ values₁ keys₂ values₂

noncomputable def «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»
    (op : SortString) (left right : SortVal) : SortBool :=
  if op = "is" then
    match right with
    | .«noneV_MPY-CORE_Val» => eqBool left .«noneV_MPY-CORE_Val»
    | _ => false
  else if op = "is not" then
    match right with
    | .«noneV_MPY-CORE_Val» => !eqBool left .«noneV_MPY-CORE_Val»
    | _ => false
  else
    match op, left, right with
    | "==", _, .«noneV_MPY-CORE_Val» =>
        eqBool left .«noneV_MPY-CORE_Val»
    | "!=", _, .«noneV_MPY-CORE_Val» =>
        !eqBool left .«noneV_MPY-CORE_Val»
    | "==", .inj_SortStr (.«str(_)_MPY-CORE_Str_IntSeq» a),
        .inj_SortStr (.«str(_)_MPY-CORE_Str_IntSeq» b) => intSeqEq a b
    | "!=", .inj_SortStr (.«str(_)_MPY-CORE_Str_IntSeq» a),
        .inj_SortStr (.«str(_)_MPY-CORE_Str_IntSeq» b) => !intSeqEq a b
    | "in", .inj_SortStr (.«str(_)_MPY-CORE_Str_IntSeq» pattern),
        .inj_SortStr (.«str(_)_MPY-CORE_Str_IntSeq» text) =>
        intSeqContains pattern text
    | "not in", .inj_SortStr (.«str(_)_MPY-CORE_Str_IntSeq» pattern),
        .inj_SortStr (.«str(_)_MPY-CORE_Str_IntSeq» text) =>
        !intSeqContains pattern text
    | "<", .inj_SortStr (.«str(_)_MPY-CORE_Str_IntSeq» a),
        .inj_SortStr (.«str(_)_MPY-CORE_Str_IntSeq» b) => intSeqLt a b
    | ">", .inj_SortStr (.«str(_)_MPY-CORE_Str_IntSeq» a),
        .inj_SortStr (.«str(_)_MPY-CORE_Str_IntSeq» b) => intSeqLt b a
    | "<=", .inj_SortStr (.«str(_)_MPY-CORE_Str_IntSeq» a),
        .inj_SortStr (.«str(_)_MPY-CORE_Str_IntSeq» b) => !intSeqLt b a
    | ">=", .inj_SortStr (.«str(_)_MPY-CORE_Str_IntSeq» a),
        .inj_SortStr (.«str(_)_MPY-CORE_Str_IntSeq» b) => !intSeqLt a b
    | "==", .inj_SortBool a, .inj_SortBool b => a == b
    | "!=", .inj_SortBool a, .inj_SortBool b => !(a == b)
    | "<", .inj_SortInt a, .inj_SortInt b => decide (a < b)
    | "<=", .inj_SortInt a, .inj_SortInt b => decide (a ≤ b)
    | ">", .inj_SortInt a, .inj_SortInt b => decide (a > b)
    | ">=", .inj_SortInt a, .inj_SortInt b => decide (a ≥ b)
    | "==", .inj_SortInt a, .inj_SortInt b => a == b
    | "!=", .inj_SortInt a, .inj_SortInt b => !(a == b)
    | "<", .inj_SortFloat a, .inj_SortFloat b => decide (a < b)
    | "<=", .inj_SortFloat a, .inj_SortFloat b => !(decide (b < a))
    | ">", .inj_SortFloat a, .inj_SortFloat b => decide (b < a)
    | ">=", .inj_SortFloat a, .inj_SortFloat b => !(decide (a < b))
    | "==", .inj_SortFloat a, .inj_SortFloat b => a == b
    | "!=", .inj_SortFloat a, .inj_SortFloat b => !(a == b)
    | op, .inj_SortInt a, .inj_SortFloat b =>
        let converted := Float.ofInt a
        if op = "<" then decide (converted < b)
        else if op = ">" then decide (b < converted)
        else if op = "==" then converted == b
        else if op = "!=" then !(converted == b)
        else false
    | op, .inj_SortFloat a, .inj_SortInt b =>
        let converted := Float.ofInt b
        if op = "<" then decide (a < converted)
        else if op = ">" then decide (converted < a)
        else if op = "==" then a == converted
        else if op = "!=" then !(a == converted)
        else false
    | "==", .inj_SortIterable (.«list(_)_MPY-CORE_Iterable_ValSeq» a),
        .inj_SortIterable (.«list(_)_MPY-CORE_Iterable_ValSeq» b) => eqBool a b
    | "!=", .inj_SortIterable (.«list(_)_MPY-CORE_Iterable_ValSeq» a),
        .inj_SortIterable (.«list(_)_MPY-CORE_Iterable_ValSeq» b) => !eqBool a b
    | "==", .inj_SortIterable (.«tuple(_)_MPY-CORE_Iterable_ValSeq» a),
        .inj_SortIterable (.«tuple(_)_MPY-CORE_Iterable_ValSeq» b) => eqBool a b
    | "!=", .inj_SortIterable (.«tuple(_)_MPY-CORE_Iterable_ValSeq» a),
        .inj_SortIterable (.«tuple(_)_MPY-CORE_Iterable_ValSeq» b) => !eqBool a b
    | "==", .«setV(_)_MPY-SET_Val_IntSeq» a,
        .«setV(_)_MPY-SET_Val_IntSeq» b => sameSet a b
    | "==", .«dictV(_,_)_MPY-DICT_Val_ValSeq_ValSeq» keys₁ values₁,
        .«dictV(_,_)_MPY-DICT_Val_ValSeq_ValSeq» keys₂ values₂ =>
        dictEq keys₁ values₁ keys₂ values₂
    | _, _, _ => false
/- KORE symbol: LblstrCodes'LParUndsRParUnds'VERIFICATION'Unds'IntSeq'Unds'Val; frozen source obligations: rule-ce7624945e06d02ae5606649e897ef6ded8e343e6c0ed28075613044c8e40503. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «strCodes(_)_VERIFICATION_IntSeq_Val» : SortVal → SortIntSeq
  | .inj_SortStr (.«str(_)_MPY-CORE_Str_IntSeq» codes) => codes
  | _ => .«.IntSeq_MPY-CORE_IntSeq»

theorem final :
    Klean7FilterBySubstring.Lemmas.targetStatement «applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» «strCodes(_)_VERIFICATION_IntSeq_Val» := by
  intro V P h
  cases V <;> simp [inj, «strCodes(_)_VERIFICATION_IntSeq_Val»] at h
  rfl

end Proof
