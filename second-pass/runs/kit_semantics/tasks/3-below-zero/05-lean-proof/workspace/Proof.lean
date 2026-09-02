import Klean3BelowZero.Lemmas

namespace Proof

noncomputable section

local instance : DecidableEq SortKItem := Classical.typeDecidableEq SortKItem

private noncomputable def mapKeyPresentOperational
    (entries : List (SortKItem × SortKItem))
    (key : SortKItem) : Bool :=
  match entries with
  | [] => false
  | (candidate, _) :: rest =>
      if candidate = key then true
      else mapKeyPresentOperational rest key

private noncomputable def mapCrossDisjointOperational
    (left right : List (SortKItem × SortKItem)) : Bool :=
  match left with
  | [] => true
  | (key, _) :: rest =>
      if mapKeyPresentOperational right key then false
      else mapCrossDisjointOperational rest right

private noncomputable def mapDeleteOperational
    (entries : List (SortKItem × SortKItem))
    (key : SortKItem) : List (SortKItem × SortKItem) :=
  match entries with
  | [] => []
  | (candidate, value) :: rest =>
      if candidate = key then mapDeleteOperational rest key
      else (candidate, value) :: mapDeleteOperational rest key

private theorem mapDeleteOperational_eq_self
    (entries : List (SortKItem × SortKItem))
    (key : SortKItem)
    (h : mapKeyPresentOperational entries key = false) :
    mapDeleteOperational entries key = entries := by
  induction entries with
  | nil => rfl
  | cons entry rest ih =>
      rcases entry with ⟨candidate, value⟩
      by_cases same : candidate = key
      · simp [mapKeyPresentOperational, same] at h
      · simp only [mapKeyPresentOperational, same, if_false] at h
        simp [mapDeleteOperational, same, ih h]

/- KORE symbol: Lbl'Unds'Map'Unds'; frozen source obligations: rule-cb90fdcb0e186a19989751bd4a10097f8ae8a2187f7744809e5610f526f6179b. Replace this stub with its honest total meaning from the frozen K semantics. -/
noncomputable def _Map_ (left right : SortMap) : SortMap :=
  if mapCrossDisjointOperational left.coll right.coll then
    ⟨left.coll ++ right.coll⟩
  else
    ⟨[]⟩
/- KORE symbol: Lbl'Unds'in'Unds'keys'LParUndsRParUnds'MAP'Unds'Bool'Unds'KItem'Unds'Map; frozen source obligations: rule-cb90fdcb0e186a19989751bd4a10097f8ae8a2187f7744809e5610f526f6179b. Replace this stub with its honest total meaning from the frozen K semantics. -/
noncomputable def «_in_keys(_)_MAP_Bool_KItem_Map»
    (key : SortKItem) (map : SortMap) : SortBool :=
  mapKeyPresentOperational map.coll key
/- KORE symbol: Lbl'UndsLSqBUnds-LT-'-undef'RSqB'; frozen source obligations: rule-cb90fdcb0e186a19989751bd4a10097f8ae8a2187f7744809e5610f526f6179b. Replace this stub with its honest total meaning from the frozen K semantics. -/
noncomputable def «_[_<-undef]» (map : SortMap) (key : SortKItem) : SortMap :=
  ⟨mapDeleteOperational map.coll key⟩
/- KORE symbol: Lbl'UndsPipe'-'-GT-Unds'; frozen source obligations: rule-cb90fdcb0e186a19989751bd4a10097f8ae8a2187f7744809e5610f526f6179b. Replace this stub with its honest total meaning from the frozen K semantics. -/
noncomputable def «_|->_» (key value : SortKItem) : SortMap :=
  ⟨[(key, value)]⟩
/- KORE symbol: Lbl'UndsPlus'Int'Unds'; frozen source obligations: rule-573796c5ae90b21570a38c51e4cd10a1610683b2a2b51c68ff466ef5277fc7fc. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_+Int_» (left right : SortInt) : SortInt :=
  left + right

private def pythonModOperational (left right : SortInt) : Option SortInt :=
  if right = 0 then none
  else some (Int.tmod (Int.tmod left right + right) right)

private def pythonFloorDivOperational (left right : SortInt) : Option SortInt :=
  match pythonModOperational left right with
  | none => none
  | some modulus => some (Int.tdiv (left - modulus) right)

private def concatCodesOperational
    (left right : SortIntSeq) : SortIntSeq :=
  match left with
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => right
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» code rest =>
      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq»
        code (concatCodesOperational rest right)

private def stringCodesViewOperational (value : SortVal) : Option SortIntSeq :=
  match value with
  | SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» codes) => some codes
  | SortVal.inj_SortIterable
      (SortIterable.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» codes)) => some codes
  | _ => none

private def undefinedValOperational : SortVal :=
  SortVal.«noneV_MPY-CORE_Val»

/- KORE symbol: LblapplyBin'LParUndsCommUndsCommUndsRParUnds'MPY-CORE'Unds'Val'Unds'String'Unds'Val'Unds'Val; frozen source obligations: rule-573796c5ae90b21570a38c51e4cd10a1610683b2a2b51c68ff466ef5277fc7fc. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val»
    (operator : SortString) (left right : SortVal) : SortVal :=
  match left, right with
  | SortVal.inj_SortInt leftInt, SortVal.inj_SortInt rightInt =>
      match operator with
      | "+" => SortVal.inj_SortInt (leftInt + rightInt)
      | "-" => SortVal.inj_SortInt (leftInt - rightInt)
      | "*" => SortVal.inj_SortInt (leftInt * rightInt)
      | "%" =>
          match pythonModOperational leftInt rightInt with
          | some result => SortVal.inj_SortInt result
          | none => undefinedValOperational
      | "//" =>
          match pythonFloorDivOperational leftInt rightInt with
          | some result => SortVal.inj_SortInt result
          | none => undefinedValOperational
      | "**" =>
          if rightInt < 0 then undefinedValOperational
          else SortVal.inj_SortInt (leftInt ^ rightInt.toNat)
      | "/" =>
          SortVal.inj_SortFloat (Float.ofInt leftInt / Float.ofInt rightInt)
      | _ => undefinedValOperational
  | SortVal.inj_SortInt leftInt, SortVal.inj_SortBool rightBool =>
      if operator = "+" then
        SortVal.inj_SortInt (leftInt + if rightBool then 1 else 0)
      else undefinedValOperational
  | SortVal.inj_SortBool leftBool, SortVal.inj_SortInt rightInt =>
      if operator = "+" then
        SortVal.inj_SortInt ((if leftBool then 1 else 0) + rightInt)
      else undefinedValOperational
  | SortVal.inj_SortFloat leftFloat, SortVal.inj_SortFloat rightFloat =>
      match operator with
      | "+" => SortVal.inj_SortFloat (leftFloat + rightFloat)
      | "-" => SortVal.inj_SortFloat (leftFloat - rightFloat)
      | "*" => SortVal.inj_SortFloat (leftFloat * rightFloat)
      | "/" => SortVal.inj_SortFloat (leftFloat / rightFloat)
      | "%" =>
          SortVal.inj_SortFloat
            (leftFloat - Float.floor (leftFloat / rightFloat) * rightFloat)
      | "**" => SortVal.inj_SortFloat (Float.pow leftFloat rightFloat)
      | _ => undefinedValOperational
  | SortVal.inj_SortInt leftInt, SortVal.inj_SortFloat rightFloat =>
      let leftFloat := Float.ofInt leftInt
      match operator with
      | "+" => SortVal.inj_SortFloat (leftFloat + rightFloat)
      | "-" => SortVal.inj_SortFloat (leftFloat - rightFloat)
      | "*" => SortVal.inj_SortFloat (leftFloat * rightFloat)
      | "/" => SortVal.inj_SortFloat (leftFloat / rightFloat)
      | "**" => SortVal.inj_SortFloat (Float.pow leftFloat rightFloat)
      | _ => undefinedValOperational
  | SortVal.inj_SortFloat leftFloat, SortVal.inj_SortInt rightInt =>
      let rightFloat := Float.ofInt rightInt
      match operator with
      | "+" => SortVal.inj_SortFloat (leftFloat + rightFloat)
      | "-" => SortVal.inj_SortFloat (leftFloat - rightFloat)
      | "*" => SortVal.inj_SortFloat (leftFloat * rightFloat)
      | "/" => SortVal.inj_SortFloat (leftFloat / rightFloat)
      | "**" => SortVal.inj_SortFloat (Float.pow leftFloat rightFloat)
      | _ => undefinedValOperational
  | leftString, rightString =>
      if operator = "+" then
        match stringCodesViewOperational leftString,
            stringCodesViewOperational rightString with
        | some leftCodes, some rightCodes =>
            SortVal.inj_SortStr
              (SortStr.«str(_)_MPY-CORE_Str_IntSeq»
                (concatCodesOperational leftCodes rightCodes))
        | _, _ => undefinedValOperational
      else undefinedValOperational

/- KORE symbol: LbldefinedProjectInt'LParUndsRParUnds'VERIFICATION-BASE'Unds'Bool'Unds'Val; frozen source obligations: rule-0312858a8718cb93d212cdb7b679a2875534dc14191dff8edf7bccf9a96d8b43, rule-22fa1e67d4a05b75b5a578312159b0a4e049b756806628df2540b007f43bcb5d. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «definedProjectInt(_)_VERIFICATION-BASE_Bool_Val»
    (value : SortVal) : SortBool :=
  match value with
  | SortVal.inj_SortInt _ => true
  | _ => false
/- KORE symbol: LblisInt; frozen source obligations: rule-573796c5ae90b21570a38c51e4cd10a1610683b2a2b51c68ff466ef5277fc7fc. Replace this stub with its honest total meaning from the frozen K semantics. -/
def isInt (term : SortK) : SortBool :=
  match term with
  | SortK.kseq (SortKItem.inj_SortInt _) SortK.dotk => true
  | _ => false
/- KORE symbol: LblnotBool'Unds'; frozen source obligations: rule-cb90fdcb0e186a19989751bd4a10097f8ae8a2187f7744809e5610f526f6179b. Replace this stub with its honest total meaning from the frozen K semantics. -/
def notBool_ (value : SortBool) : SortBool :=
  !value

private def projectIntOptionOperational (term : SortK) : Option SortInt :=
  match term with
  | SortK.kseq (SortKItem.inj_SortInt value) SortK.dotk => some value
  | _ => none

/- KORE symbol: Lblproject'Coln'Int; frozen source obligations: rule-22fa1e67d4a05b75b5a578312159b0a4e049b756806628df2540b007f43bcb5d. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «project:Int» (term : SortK) : SortInt :=
  match projectIntOptionOperational term with
  | some value => value
  | none => 0
/- KORE symbol: LblprojectIntTotal; frozen source obligations: rule-22fa1e67d4a05b75b5a578312159b0a4e049b756806628df2540b007f43bcb5d, rule-9e1486b6d25b62bd0949213fd58d7aac97ed89cc3e87b8c5063f915d1d6b7081, rule-573796c5ae90b21570a38c51e4cd10a1610683b2a2b51c68ff466ef5277fc7fc. Replace this stub with its honest total meaning from the frozen K semantics. -/
def projectIntTotal (value : SortVal) : SortInt :=
  match value with
  | SortVal.inj_SortInt result => result
  | _ => 0
/- KORE symbol: Lblproject'Coln'Int; frozen source obligations: rule-0312858a8718cb93d212cdb7b679a2875534dc14191dff8edf7bccf9a96d8b43. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «project:Int?» (term : SortK) : Option SortInt :=
  projectIntOptionOperational term

theorem final :
    Klean3BelowZero.Lemmas.targetStatement _Map_ «_in_keys(_)_MAP_Bool_KItem_Map» «_[_<-undef]» «_|->_» «_+Int_» «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» «definedProjectInt(_)_VERIFICATION-BASE_Bool_Val» isInt notBool_ «project:Int» projectIntTotal «project:Int?» := by
  unfold Klean3BelowZero.Lemmas.targetStatement
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · intro value
    cases value <;>
      simp [inj, «project:Int?», projectIntOptionOperational,
        «definedProjectInt(_)_VERIFICATION-BASE_Bool_Val»]
  · intro value h
    cases value <;>
      simp_all [inj, «project:Int», projectIntOptionOperational, projectIntTotal,
        «definedProjectInt(_)_VERIFICATION-BASE_Bool_Val»]
  · intro value
    cases value <;> rfl
  · intro value integer h
    cases value <;>
      simp_all [inj, isInt, «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val»,
        «_+Int_», projectIntTotal]
  · intro location store scope h
    rcases store with ⟨entries⟩
    let key := SortKItem.inj_SortInt location
    have absent : mapKeyPresentOperational entries key = false := by
      simpa [key, notBool_, «_in_keys(_)_MAP_Bool_KItem_Map»] using h
    have deleted : mapDeleteOperational entries key = entries :=
      mapDeleteOperational_eq_self entries key absent
    have deleteInserted :
        mapDeleteOperational
          ((key, SortKItem.inj_SortScope scope) :: entries) key = entries := by
      simp [mapDeleteOperational, deleted]
    simp [«_[_<-undef]», _Map_, «_|->_», mapCrossDisjointOperational,
      absent, key, deleteInserted]

end

end Proof
