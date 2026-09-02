import Klean20FindClosestElements.Lemmas

namespace Proof

/- `valSeqAtTotal` implements the frozen `normIdx`/`valSeqAt` path used by
   `applyIndex` for lists and tuples.  The K definition leaves out-of-bounds
   total results abstract; `noneV` is the fixed representative for that
   otherwise unconstrained case. -/
private def valSeqLength : SortValSeq → Nat
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => 0
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _ rest =>
      valSeqLength rest + 1

private def valSeqAt? : SortValSeq → Nat → Option SortVal
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _ => none
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» value _, 0 =>
      some value
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _ rest, n + 1 =>
      valSeqAt? rest n

private def valSeqAtTotal (values : SortValSeq) (index : SortInt) : SortVal :=
  let length : SortInt := Int.ofNat (valSeqLength values)
  let normalized := if index < 0 then index + length else index
  if normalized < 0 then
    SortVal.«noneV_MPY-CORE_Val»
  else
    (valSeqAt? values normalized.toNat).getD SortVal.«noneV_MPY-CORE_Val»

private def canonicalItem (index : SortInt) (value : SortFloat) : SortVal :=
  SortVal.inj_SortIterable
    (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq»
      (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
        (SortVal.inj_SortInt index)
        (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
          (SortVal.inj_SortFloat value)
          SortValSeq.«.ValSeq_MPY-CORE_ValSeq»)))

private theorem valInjectionRetracts (value : SortVal) :
    (retr (inj value : SortKItem) : Option SortVal) = some value := by
  cases value <;> rfl

private theorem valInjectionInjective
    {left right : SortVal}
    (h : (inj left : SortKItem) = (inj right : SortKItem)) :
    left = right := by
  have h' := congrArg (fun item : SortKItem => (retr item : Option SortVal)) h
  have hs : some left = some right := by
    simpa only [valInjectionRetracts] using h'
  injection hs

private theorem canonicalValueOfKSeqEquality
    (value : SortVal) (index : SortInt) (float : SortFloat)
    (h :
      SortK.kseq (inj value : SortKItem) SortK.dotk =
      SortK.kseq (inj (canonicalItem index float) : SortKItem) SortK.dotk) :
    value = canonicalItem index float := by
  apply valInjectionInjective
  injection h

/- KORE symbol: LblallFloatItems'LParUndsRParUnds'VERIFICATION-BASE'Unds'Bool'Unds'ValSeq; frozen source obligations: rule-1be94e05a1b1440cd44a316053a753efc65fc522fcdf2fd8218e40d546231a89. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «allFloatItems(_)_VERIFICATION-BASE_Bool_ValSeq» : SortValSeq → SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => true
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
      (SortVal.inj_SortIterable
        (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq»
          (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
            (SortVal.inj_SortInt _)
            (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
              (SortVal.inj_SortFloat _)
              SortValSeq.«.ValSeq_MPY-CORE_ValSeq»))))
      rest =>
    «allFloatItems(_)_VERIFICATION-BASE_Bool_ValSeq» rest
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _ _ => false
/- KORE symbol: LblallFloatVS'LParUndsRParUnds'VERIFICATION-BASE'Unds'Bool'Unds'ValSeq; frozen source obligations: rule-1be94e05a1b1440cd44a316053a753efc65fc522fcdf2fd8218e40d546231a89. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «allFloatVS(_)_VERIFICATION-BASE_Bool_ValSeq» : SortValSeq → SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => true
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
      (SortVal.inj_SortFloat _) rest =>
    «allFloatVS(_)_VERIFICATION-BASE_Bool_ValSeq» rest
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _ _ => false
/- KORE symbol: LblapplyIndex'LParUndsCommUndsRParUnds'MPY-SUBSCRIPT'Unds'Val'Unds'Val'Unds'Int; frozen source obligations: rule-db9d3a3e81dee21bb05c9f3240b23092771092e55e7bb6f53dc9fdcfa44b3188, rule-c31085d90cc1a95717c3310bccb50623ab127a57e9e6010eb23e0aa2e4377dc7. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «applyIndex(_,_)_MPY-SUBSCRIPT_Val_Val_Int»
    (value : SortVal) (index : SortInt) : SortVal :=
  match value with
  | SortVal.inj_SortIterable
      (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» values) =>
    valSeqAtTotal values index
  | SortVal.inj_SortIterable
      (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq» values) =>
    valSeqAtTotal values index
  | _ => SortVal.«noneV_MPY-CORE_Val»
/- KORE symbol: LblenumVS'LParUndsCommUndsRParUnds'MPY-BUILTINS'Unds'ValSeq'Unds'ValSeq'Unds'Int; frozen source obligations: rule-1be94e05a1b1440cd44a316053a753efc65fc522fcdf2fd8218e40d546231a89. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «enumVS(_,_)_MPY-BUILTINS_ValSeq_ValSeq_Int» :
    SortValSeq → SortInt → SortValSeq
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _ =>
    SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» value rest, index =>
    SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
      (SortVal.inj_SortIterable
        (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq»
          (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
            (SortVal.inj_SortInt index)
            (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
              value
              SortValSeq.«.ValSeq_MPY-CORE_ValSeq»))))
      («enumVS(_,_)_MPY-BUILTINS_ValSeq_ValSeq_Int» rest (index + 1))
/- KORE symbol: LblitemFloat'LParUndsRParUnds'VERIFICATION-BASE'Unds'Float'Unds'Val; frozen source obligations: rule-db9d3a3e81dee21bb05c9f3240b23092771092e55e7bb6f53dc9fdcfa44b3188, rule-c31085d90cc1a95717c3310bccb50623ab127a57e9e6010eb23e0aa2e4377dc7. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «itemFloat(_)_VERIFICATION-BASE_Float_Val» : SortVal → SortFloat
  | SortVal.inj_SortIterable
      (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq»
        (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
          (SortVal.inj_SortInt _)
          (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
            (SortVal.inj_SortFloat value)
            SortValSeq.«.ValSeq_MPY-CORE_ValSeq»))) =>
    value
  | _ => 0.0
/- KORE symbol: LblitemIndex'LParUndsRParUnds'VERIFICATION-BASE'Unds'Int'Unds'Val; frozen source obligations: rule-db9d3a3e81dee21bb05c9f3240b23092771092e55e7bb6f53dc9fdcfa44b3188, rule-c31085d90cc1a95717c3310bccb50623ab127a57e9e6010eb23e0aa2e4377dc7. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «itemIndex(_)_VERIFICATION-BASE_Int_Val» : SortVal → SortInt
  | SortVal.inj_SortIterable
      (SortIterable.«tuple(_)_MPY-CORE_Iterable_ValSeq»
        (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
          (SortVal.inj_SortInt index)
          (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
            (SortVal.inj_SortFloat _)
            SortValSeq.«.ValSeq_MPY-CORE_ValSeq»))) =>
    index
  | _ => 0

private theorem enumerationPreservesFloatItems
    (index : SortInt) (values : SortValSeq)
    (h : «allFloatVS(_)_VERIFICATION-BASE_Bool_ValSeq» values = true) :
    «allFloatItems(_)_VERIFICATION-BASE_Bool_ValSeq»
      («enumVS(_,_)_MPY-BUILTINS_ValSeq_ValSeq_Int» values index) = true := by
  cases values with
  | «.ValSeq_MPY-CORE_ValSeq» =>
      rfl
  | «vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» value rest =>
      cases value <;>
        simp_all [«allFloatVS(_)_VERIFICATION-BASE_Bool_ValSeq»]
      case inj_SortFloat float =>
        simp only [«enumVS(_,_)_MPY-BUILTINS_ValSeq_ValSeq_Int»,
          «allFloatItems(_)_VERIFICATION-BASE_Bool_ValSeq»]
        exact enumerationPreservesFloatItems (index + 1) rest h
termination_by sizeOf values

theorem final :
    Klean20FindClosestElements.Lemmas.targetStatement «allFloatItems(_)_VERIFICATION-BASE_Bool_ValSeq» «allFloatVS(_)_VERIFICATION-BASE_Bool_ValSeq» «applyIndex(_,_)_MPY-SUBSCRIPT_Val_Val_Int» «enumVS(_,_)_MPY-BUILTINS_ValSeq_ValSeq_Int» «itemFloat(_)_VERIFICATION-BASE_Float_Val» «itemIndex(_)_VERIFICATION-BASE_Int_Val» := by
  constructor
  · intro V h
    have hv :
        V =
          canonicalItem
            («itemIndex(_)_VERIFICATION-BASE_Int_Val» V)
            («itemFloat(_)_VERIFICATION-BASE_Float_Val» V) := by
      apply canonicalValueOfKSeqEquality
      exact h
    rw [hv]
    rfl
  constructor
  · intro V h
    have hv :
        V =
          canonicalItem
            («itemIndex(_)_VERIFICATION-BASE_Int_Val» V)
            («itemFloat(_)_VERIFICATION-BASE_Float_Val» V) := by
      apply canonicalValueOfKSeqEquality
      exact h
    rw [hv]
    rfl
  · exact enumerationPreservesFloatItems

end Proof
