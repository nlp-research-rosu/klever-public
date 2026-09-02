import Klean79DecimalToBinary.Lemmas

namespace Proof

private def intSeqDrop : Nat → SortIntSeq → SortIntSeq
  | 0, sequence => sequence
  | _ + 1, SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» =>
      SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
  | count + 1, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ rest =>
      intSeqDrop count rest

private def valSeqDrop : Nat → SortValSeq → SortValSeq
  | 0, sequence => sequence
  | _ + 1, SortValSeq.«.ValSeq_MPY-CORE_ValSeq» =>
      SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
  | count + 1, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _ rest =>
      valSeqDrop count rest

private def intSeqToList : SortIntSeq → List SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => []
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» value rest =>
      value :: intSeqToList rest

private def listToIntSeq : List SortInt → SortIntSeq
  | [] => SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
  | value :: rest =>
      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» value (listToIntSeq rest)

private def valSeqToList : SortValSeq → List SortVal
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => []
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» value rest =>
      value :: valSeqToList rest

private def listToValSeq : List SortVal → SortValSeq
  | [] => SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
  | value :: rest =>
      SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» value (listToValSeq rest)

private def sliceStep : SortOptInt → SortInt
  | SortOptInt.«noB_MPY-SUBSCRIPT_OptInt» => 1
  | SortOptInt.«someB(_)_MPY-SUBSCRIPT_OptInt_Int» step => step

private def adjustSliceIndex (index length step : SortInt) : SortInt :=
  if index < 0 then
    let shifted := index + length
    if 0 ≤ shifted then shifted
    else if step < 0 then -1 else 0
  else if index < length then index
  else if step < 0 then length - 1 else length

private def sliceStart (lower : SortOptInt) (step length : SortInt) : SortInt :=
  match lower with
  | SortOptInt.«noB_MPY-SUBSCRIPT_OptInt» =>
      if 0 < step then 0 else length - 1
  | SortOptInt.«someB(_)_MPY-SUBSCRIPT_OptInt_Int» index =>
      adjustSliceIndex index length step

private def sliceStop (upper : SortOptInt) (step length : SortInt) : SortInt :=
  match upper with
  | SortOptInt.«noB_MPY-SUBSCRIPT_OptInt» =>
      if 0 < step then length else -1
  | SortOptInt.«someB(_)_MPY-SUBSCRIPT_OptInt_Int» index =>
      adjustSliceIndex index length step

private def enumerateFrom {α : Type} : Nat → List α → List (SortInt × α)
  | _, [] => []
  | index, value :: rest =>
      (Int.ofNat index, value) :: enumerateFrom (index + 1) rest

private def sliceListGeneral {α : Type}
    (values : List α) (lower upper stepBound : SortOptInt) : Option (List α) :=
  let step := sliceStep stepBound
  if step = 0 then none
  else
    let length : SortInt := Int.ofNat values.length
    let start := sliceStart lower step length
    let stop := sliceStop upper step length
    if 0 < step then
      some <| (enumerateFrom 0 values).filterMap fun (index, value) =>
        if start ≤ index ∧ index < stop ∧ (index - start) % step = 0
        then some value
        else none
    else
      some <| (enumerateFrom 0 values).reverse.filterMap fun (index, value) =>
        if index ≤ start ∧ stop < index ∧ (start - index) % (-step) = 0
        then some value
        else none

private def sliceIntSeq
    (sequence : SortIntSeq)
    (lower upper stepBound : SortOptInt) : Option SortIntSeq :=
  match lower, upper, stepBound with
  | SortOptInt.«noB_MPY-SUBSCRIPT_OptInt»,
      SortOptInt.«noB_MPY-SUBSCRIPT_OptInt»,
      SortOptInt.«noB_MPY-SUBSCRIPT_OptInt» =>
      some sequence
  | SortOptInt.«someB(_)_MPY-SUBSCRIPT_OptInt_Int» index,
      SortOptInt.«noB_MPY-SUBSCRIPT_OptInt»,
      SortOptInt.«noB_MPY-SUBSCRIPT_OptInt» =>
      if 0 ≤ index then some (intSeqDrop index.toNat sequence)
      else
        (sliceListGeneral (intSeqToList sequence) lower upper stepBound).map
          listToIntSeq
  | _, _, _ =>
      (sliceListGeneral (intSeqToList sequence) lower upper stepBound).map
        listToIntSeq

private def sliceValSeq
    (sequence : SortValSeq)
    (lower upper stepBound : SortOptInt) : Option SortValSeq :=
  match lower, upper, stepBound with
  | SortOptInt.«noB_MPY-SUBSCRIPT_OptInt»,
      SortOptInt.«noB_MPY-SUBSCRIPT_OptInt»,
      SortOptInt.«noB_MPY-SUBSCRIPT_OptInt» =>
      some sequence
  | SortOptInt.«someB(_)_MPY-SUBSCRIPT_OptInt_Int» index,
      SortOptInt.«noB_MPY-SUBSCRIPT_OptInt»,
      SortOptInt.«noB_MPY-SUBSCRIPT_OptInt» =>
      if 0 ≤ index then some (valSeqDrop index.toNat sequence)
      else
        (sliceListGeneral (valSeqToList sequence) lower upper stepBound).map
          listToValSeq
  | _, _, _ =>
      (sliceListGeneral (valSeqToList sequence) lower upper stepBound).map
        listToValSeq

/- KORE symbol: LbldoSlice'LParUndsCommUndsCommUndsCommUndsRParUnds'MPY-SUBSCRIPT'Unds'Val'Unds'Val'Unds'OptInt'Unds'OptInt'Unds'OptInt; frozen source obligations: rule-d413ecca2d0d055a04bc2f4fe8404284cf3025dc1bb61dd03e2d09244027583b. Replace this stub with its honest total meaning from the frozen K semantics. -/
/- The generated Lean signature is total although the K symbol is partial.
   List, tuple, and string inputs with nonzero steps follow the frozen
   slStart/slStop/slStep/buildVS/buildIS equations above. For K-stuck inputs
   (an unsupported value or a zero step), the original value is preserved
   because SortVal has no constructor for an unreduced doSlice application. -/
def «doSlice(_,_,_,_)_MPY-SUBSCRIPT_Val_Val_OptInt_OptInt_OptInt»
    (value : SortVal)
    (lower upper stepBound : SortOptInt) : SortVal :=
  match value with
  | SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» sequence) =>
      match sliceIntSeq sequence lower upper stepBound with
      | some result =>
          SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» result)
      | none => value
  | SortVal.inj_SortIterable
      (SortIterable.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» sequence)) =>
      match sliceIntSeq sequence lower upper stepBound with
      | some result =>
          SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» result)
      | none => value
  | SortVal.inj_SortIterable
      (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» sequence) =>
      match sliceValSeq sequence lower upper stepBound with
      | some result =>
          SortVal.inj_SortIterable
            (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» result)
      | none => value
  | SortVal.inj_SortIterable
      (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» sequence) =>
      match sliceValSeq sequence lower upper stepBound with
      | some result =>
          SortVal.inj_SortIterable
            (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» result)
      | none => value
  | _ => value

theorem final :
    Klean79DecimalToBinary.Lemmas.targetStatement «doSlice(_,_,_,_)_MPY-SUBSCRIPT_Val_Val_OptInt_OptInt_OptInt» := by
  intro REST _SECOND _FIRST
  rfl

end Proof
