import Klean33SortThird.Lemmas

namespace Proof

/- KORE symbol: Lbl'Unds-LT-Eqls'Int'Unds'; frozen source obligations: rule-684bef72ba46103ebf75024cdc1fa13051bb1bec81e5c3ebfd659638388ad8f2. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_<=Int_» (left right : SortInt) : SortBool :=
  decide (left ≤ right)

private def proofValSeqToList : SortValSeq → List SortVal
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => []
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» value rest =>
      value :: proofValSeqToList rest

private def proofValSeqOfList : List SortVal → SortValSeq
  | [] => SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
  | value :: rest =>
      SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
        value (proofValSeqOfList rest)

private def proofValSeqLength : SortValSeq → Nat
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => 0
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _ rest =>
      Nat.succ (proofValSeqLength rest)

/- The exact `buildVS(VS, 0, vsLen(VS), 3)` selection. -/
private def proofEveryThirdValue : List SortVal → List SortVal
  | [] => []
  | first :: _ :: _ :: rest => first :: proofEveryThirdValue rest
  | first :: _ => [first]

private def proofBoolAsInt (value : Bool) : Int :=
  if value then 1 else 0

private def proofCompareInts (left right : Int) : Ordering :=
  if left < right then .lt else if right < left then .gt else .eq

/- This is exactly the recurrence of frozen `strLt`: lexicographic comparison
   over the integer code sequence, including all artificial integer codes. -/
private def proofCompareCodeSequences : SortIntSeq → SortIntSeq → Ordering
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»,
      SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => .eq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»,
      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ _ => .lt
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ _,
      SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => .gt
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» left leftRest,
      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» right rightRest =>
      if left < right then .lt
      else if right < left then .gt
      else proofCompareCodeSequences leftRest rightRest

private def proofCompareStrings (left right : SortStr) : Ordering :=
  match left, right with
  | SortStr.«str(_)_MPY-CORE_Str_IntSeq» leftCodes,
      SortStr.«str(_)_MPY-CORE_Str_IntSeq» rightCodes =>
      proofCompareCodeSequences leftCodes rightCodes

/- Frozen `floatLt` is `<Float`; mixed numeric comparisons first apply
   `Int2Float(I, 53, 11)`. Base's `Float` is binary64, so these are the
   corresponding Lean operations. NaN always has the fixed incomparable result. -/
private def proofCompareFloats (left right : Float) : Option Ordering :=
  if left.isNaN || right.isNaN then none
  else if left < right then some .lt
  else if right < left then some .gt
  else some .eq

/- Executable structural fuel for nested lexicographic comparison. -/
mutual
  private def proofComparableValueSize : SortVal → Nat
    | SortVal.inj_SortIterable value =>
        Nat.succ (proofComparableIterableSize value)
    | _ => 1

  private def proofComparableIterableSize : SortIterable → Nat
    | SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» values =>
        Nat.succ (proofComparableSequenceSize values)
    | SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» values =>
        Nat.succ (proofComparableSequenceSize values)
    | _ => 1

  private def proofComparableSequenceSize : SortValSeq → Nat
    | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => 1
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» value rest =>
        Nat.succ
          (proofComparableValueSize value + proofComparableSequenceSize rest)
end

/- Source `<` over every comparable family retained by Base. Strings are
   covered in both the canonical direct injection and the constructible nested
   Iterable injection. Unsupported pairs share one incomparable totalization. -/
mutual
  private def proofCompareBaseValuesFuel :
      Nat → SortVal → SortVal → Option Ordering
    | 0, _, _ => none
    | Nat.succ _, SortVal.inj_SortBool left, SortVal.inj_SortBool right =>
        some (proofCompareInts (proofBoolAsInt left) (proofBoolAsInt right))
    | Nat.succ _, SortVal.inj_SortBool left, SortVal.inj_SortInt right =>
        some (proofCompareInts (proofBoolAsInt left) right)
    | Nat.succ _, SortVal.inj_SortInt left, SortVal.inj_SortBool right =>
        some (proofCompareInts left (proofBoolAsInt right))
    | Nat.succ _, SortVal.inj_SortInt left, SortVal.inj_SortInt right =>
        some (proofCompareInts left right)
    | Nat.succ _, SortVal.inj_SortFloat left, SortVal.inj_SortFloat right =>
        proofCompareFloats left right
    | Nat.succ _, SortVal.inj_SortInt left, SortVal.inj_SortFloat right =>
        proofCompareFloats (Float.ofInt left) right
    | Nat.succ _, SortVal.inj_SortFloat left, SortVal.inj_SortInt right =>
        proofCompareFloats left (Float.ofInt right)
    | Nat.succ _, SortVal.inj_SortBool left, SortVal.inj_SortFloat right =>
        proofCompareFloats (Float.ofInt (proofBoolAsInt left)) right
    | Nat.succ _, SortVal.inj_SortFloat left, SortVal.inj_SortBool right =>
        proofCompareFloats left (Float.ofInt (proofBoolAsInt right))
    | Nat.succ _, SortVal.inj_SortStr left, SortVal.inj_SortStr right =>
        some (proofCompareStrings left right)
    | Nat.succ _, SortVal.inj_SortStr left,
        SortVal.inj_SortIterable (SortIterable.inj_SortStr right) =>
        some (proofCompareStrings left right)
    | Nat.succ _, SortVal.inj_SortIterable (SortIterable.inj_SortStr left),
        SortVal.inj_SortStr right =>
        some (proofCompareStrings left right)
    | Nat.succ _, SortVal.inj_SortIterable (SortIterable.inj_SortStr left),
        SortVal.inj_SortIterable (SortIterable.inj_SortStr right) =>
        some (proofCompareStrings left right)
    | Nat.succ fuel,
        SortVal.inj_SortIterable
          (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» left),
        SortVal.inj_SortIterable
          (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» right) =>
        proofCompareBaseSequencesFuel fuel left right
    | Nat.succ fuel,
        SortVal.inj_SortIterable
          (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» left),
        SortVal.inj_SortIterable
          (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» right) =>
        proofCompareBaseSequencesFuel fuel left right
    | Nat.succ _, _, _ => none

  private def proofCompareBaseSequencesFuel :
      Nat → SortValSeq → SortValSeq → Option Ordering
    | 0, _, _ => none
    | Nat.succ _, SortValSeq.«.ValSeq_MPY-CORE_ValSeq»,
        SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some .eq
    | Nat.succ _, SortValSeq.«.ValSeq_MPY-CORE_ValSeq»,
        SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _ _ => some .lt
    | Nat.succ _, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _ _,
        SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some .gt
    | Nat.succ fuel,
        SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» left leftRest,
        SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» right rightRest =>
        match proofCompareBaseValuesFuel fuel left right with
        | some .eq => proofCompareBaseSequencesFuel fuel leftRest rightRest
        | result => result
end

private def proofCompareBaseValues
    (left right : SortVal) : Option Ordering :=
  proofCompareBaseValuesFuel
    (proofComparableValueSize left + proofComparableValueSize right + 1)
    left right

/- Stable insertion using source `<`. Equal and incomparable pairs both retain
   their input order, giving one fixed totalization outside frozen guards. -/
private def proofInsertBySourceOrder
    (value : SortVal) : List SortVal → List SortVal
  | [] => [value]
  | head :: tail =>
      match proofCompareBaseValues head value with
      | some .lt => head :: proofInsertBySourceOrder value tail
      | _ => value :: head :: tail

private def proofSortBySourceOrder : List SortVal → List SortVal
  | [] => []
  | value :: rest =>
      proofInsertBySourceOrder value (proofSortBySourceOrder rest)

/- Exact `mergeThirdFrom` result at I = 0. Sorting is confined to the selected
   slice, so unrelated values in unselected positions cannot block it. -/
private def proofMergeThirdResult : List SortVal → List SortVal → List SortVal
  | [], _ => []
  | _ :: second :: third :: rest, selected :: selectedRest =>
      selected :: second :: third :: proofMergeThirdResult rest selectedRest
  | _ :: second :: [], selected :: _ => [selected, second]
  | _ :: [], selected :: _ => [selected]
  | original, [] => original

private def proofSortThirdOperational (values : SortValSeq) : SortValSeq :=
  let original := proofValSeqToList values
  let selected := proofSortBySourceOrder (proofEveryThirdValue original)
  proofValSeqOfList (proofMergeThirdResult original selected)

/- KORE symbol: LblsortThirdResult'LParUndsRParUnds'VERIFICATION'Unds'ValSeq'Unds'ValSeq; frozen source obligations: rule-684bef72ba46103ebf75024cdc1fa13051bb1bec81e5c3ebfd659638388ad8f2. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «sortThirdResult(_)_VERIFICATION_ValSeq_ValSeq»
    (values : SortValSeq) : SortValSeq :=
  proofSortThirdOperational values

/- KORE symbol: LblvalSeqConcat'LParUndsCommUndsRParUnds'MPY-LIST'Unds'ValSeq'Unds'ValSeq'Unds'ValSeq; frozen source obligations: rule-a1197a694d8ff7aa6e41e81faf447c740a45b12fc2bad596cbef040446551918, rule-d101e72bc8dee6c43ac06d55f47939cef9e5ae630efb965cc680c40d10bb36f9. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» :
    SortValSeq → SortValSeq → SortValSeq
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», suffix => suffix
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» value rest, suffix =>
      SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» value
        («valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» rest suffix)

/- KORE symbol: LblvsLen'LParUndsRParUnds'MPY-CORE'Unds'Int'Unds'ValSeq; frozen source obligations: rule-684bef72ba46103ebf75024cdc1fa13051bb1bec81e5c3ebfd659638388ad8f2. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «vsLen(_)_MPY-CORE_Int_ValSeq» (values : SortValSeq) : SortInt :=
  Int.ofNat (proofValSeqLength values)

private theorem proofConcatAssociative :
    ∀ (A B C : SortValSeq),
      «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»
          («valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» A B) C =
        «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» A
          («valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» B C)
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _, _ => rfl
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» value rest, B, C =>
      congrArg
        (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» value)
        (proofConcatAssociative rest B C)

private theorem proofConcatRightIdentity :
    ∀ (A : SortValSeq),
      «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»
          A SortValSeq.«.ValSeq_MPY-CORE_ValSeq» = A
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => rfl
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» value rest =>
      congrArg
        (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» value)
        (proofConcatRightIdentity rest)

private theorem proofSortThirdEmptyWhenLengthNonpositive :
    ∀ (VS : SortValSeq),
      «_<=Int_» («vsLen(_)_MPY-CORE_Int_ValSeq» VS) 0 = true →
        «sortThirdResult(_)_VERIFICATION_ValSeq_ValSeq» VS =
          SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _ => rfl
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _ rest, h => by
      have hle : Int.ofNat (Nat.succ (proofValSeqLength rest)) ≤ (0 : Int) :=
        of_decide_eq_true h
      have hpos : (0 : Int) < Int.ofNat (Nat.succ (proofValSeqLength rest)) :=
        Int.ofNat_succ_pos _
      exact (Int.not_lt_of_ge hle hpos).elim

theorem final :
    Klean33SortThird.Lemmas.targetStatement «_<=Int_» «sortThirdResult(_)_VERIFICATION_ValSeq_ValSeq» «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» «vsLen(_)_MPY-CORE_Int_ValSeq» := by
  exact
    ⟨proofSortThirdEmptyWhenLengthNonpositive,
     (fun C B A => proofConcatAssociative A B C),
     proofConcatRightIdentity⟩

end Proof
