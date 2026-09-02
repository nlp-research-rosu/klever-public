import Klean72WillItFly.Lemmas

namespace Proof

/- KORE symbol: LblallInts'LParUndsRParUnds'VERIFICATION'Unds'Bool'Unds'ValSeq; frozen source obligations: rule-8c6fd5f43e6635bfa3e7668c921b0d8e3f46d6d1de6484989e3107ed21ffcc0c. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «allInts(_)_VERIFICATION_Bool_ValSeq» : SortValSeq → SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => true
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
      (SortVal.inj_SortInt _) rest =>
      «allInts(_)_VERIFICATION_Bool_ValSeq» rest
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _ _ => false

private def snocVS : SortValSeq → SortVal → SortValSeq
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», value =>
      SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
        value SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» head tail, value =>
      SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
        head (snocVS tail value)

/- KORE symbol: LblreverseVS'LParUndsRParUnds'VERIFICATION'Unds'ValSeq'Unds'ValSeq; frozen source obligations: rule-e8f739bf08317e883904eb65ce494f7a330c76031451acc8eea4e8073068f5e0. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «reverseVS(_)_VERIFICATION_ValSeq_ValSeq» : SortValSeq → SortValSeq
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» =>
      SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» head tail =>
      snocVS («reverseVS(_)_VERIFICATION_ValSeq_ValSeq» tail) head

/- KORE symbol: LbldoSlice'LParUndsCommUndsCommUndsCommUndsRParUnds'MPY-SUBSCRIPT'Unds'Val'Unds'Val'Unds'OptInt'Unds'OptInt'Unds'OptInt; frozen source obligations: rule-e8f739bf08317e883904eb65ce494f7a330c76031451acc8eea4e8073068f5e0. Replace this stub with its honest total meaning from the frozen K semantics. -/
noncomputable def «doSlice(_,_,_,_)_MPY-SUBSCRIPT_Val_Val_OptInt_OptInt_OptInt» :
    SortVal → SortOptInt → SortOptInt → SortOptInt → SortVal
  -- The first branch is exactly frozen rule e8f739... at priority 40.
  | SortVal.inj_SortIterable
      (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» values),
      SortOptInt.«noB_MPY-SUBSCRIPT_OptInt»,
      SortOptInt.«noB_MPY-SUBSCRIPT_OptInt»,
      SortOptInt.«someB(_)_MPY-SUBSCRIPT_OptInt_Int» (-1) =>
      SortVal.inj_SortIterable
        (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq»
          («reverseVS(_)_VERIFICATION_ValSeq_ValSeq» values))
  -- Other inputs retain the generated MPY-SUBSCRIPT implementation. `noneV`
  -- totalizes only inputs for which that partial generated function has no rule.
  | value, lo, hi, step =>
      (_root_.«doSlice(_,_,_,_)_MPY-SUBSCRIPT_Val_Val_OptInt_OptInt_OptInt»
        value lo hi step).getD SortVal.«noneV_MPY-CORE_Val»

/- KORE symbol: LblsumIntVS'LParUndsRParUnds'VERIFICATION'Unds'Int'Unds'ValSeq; frozen source obligations: rule-8c6fd5f43e6635bfa3e7668c921b0d8e3f46d6d1de6484989e3107ed21ffcc0c. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «sumIntVS(_)_VERIFICATION_Int_ValSeq» : SortValSeq → SortInt
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => 0
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
      (SortVal.inj_SortInt value) rest =>
      value + «sumIntVS(_)_VERIFICATION_Int_ValSeq» rest
  -- Frozen sumIntVS equations have no non-integer case; all theorem uses are
  -- guarded by allInts, so this totalization is unreachable in the proof.
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _ _ => 0

private def config
    (item : SortKItem)
    (kont : SortK)
    (gen9 : SortGeneratedCounterCell)
    (gen8 : SortExitCodeCell)
    (gen7 : SortExcCell)
    (gen6 : SortRetCell)
    (gen5 : SortStackCell)
    (gen4 : SortHeapLocCell)
    (gen3 : SortHeapCell)
    (gen2 : SortScopeLocCell)
    (gen1 : SortScopesCell)
    (gen0 : SortEnvCell) : SortGeneratedTopCell :=
  { k := { val := SortK.kseq item kont }
    env := gen0
    scopes := gen1
    scopeLoc := gen2
    heap := gen3
    heapLoc := gen4
    stack := gen5
    ret := gen6
    exc := gen7
    exitCode := gen8
    generatedCounter := gen9 }

private theorem allInts_cons
    {head : SortVal} {tail : SortValSeq}
    (h : «allInts(_)_VERIFICATION_Bool_ValSeq»
      (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» head tail) = true) :
    ∃ value : SortInt,
      head = SortVal.inj_SortInt value ∧
      «allInts(_)_VERIFICATION_Bool_ValSeq» tail = true := by
  cases head <;> simp_all [«allInts(_)_VERIFICATION_Bool_ValSeq»]

private theorem sumAcc_correct
    (gen9 : SortGeneratedCounterCell)
    (gen8 : SortExitCodeCell)
    (gen7 : SortExcCell)
    (gen6 : SortRetCell)
    (gen5 : SortStackCell)
    (gen4 : SortHeapLocCell)
    (gen3 : SortHeapCell)
    (gen2 : SortScopeLocCell)
    (gen1 : SortScopesCell)
    (gen0 : SortEnvCell)
    (kont : SortK)
    (values : SortValSeq)
    (acc : SortInt)
    (h : «allInts(_)_VERIFICATION_Bool_ValSeq» values = true) :
    Rewrites
      (config
        (SortKItem.«#sumAcc(_,_)_MPY-BUILTINS_KItem_Iterable_Int»
          (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» values) acc)
        kont gen9 gen8 gen7 gen6 gen5 gen4 gen3 gen2 gen1 gen0)
      (config
        (SortKItem.inj_SortInt
          (acc + «sumIntVS(_)_VERIFICATION_Int_ValSeq» values))
        kont gen9 gen8 gen7 gen6 gen5 gen4 gen3 gen2 gen1 gen0) := by
  cases values with
  | «.ValSeq_MPY-CORE_ValSeq» =>
      simp only [«sumIntVS(_)_VERIFICATION_Int_ValSeq», Int.add_zero]
      apply Rewrites.tran Rewrites._268b33b
      apply Rewrites.tran Rewrites._5d4a96e
      exact Rewrites._91416c0
  | «vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» head tail =>
      obtain ⟨value, rfl, htail⟩ := allInts_cons h
      apply Rewrites.tran Rewrites._268b33b
      apply Rewrites.tran Rewrites._3b733db
      apply Rewrites.tran
      · exact Rewrites._38833f2
          (defn_Val0 := by rfl)
          (defn_Val1 := by rfl)
          (defn_Val2 := by rfl)
          (defn_Val3 := by rfl)
          (defn_Val4 := by rfl)
          (req := by rfl)
      · simpa only
          [«sumIntVS(_)_VERIFICATION_Int_ValSeq», Int.add_assoc]
          using sumAcc_correct gen9 gen8 gen7 gen6 gen5 gen4 gen3 gen2
            gen1 gen0 kont tail (acc + value) htail
termination_by sizeOf values
decreasing_by
  simp_all
  exact Nat.add_pos_left (by decide) _

theorem final :
    Klean72WillItFly.Lemmas.targetStatement «allInts(_)_VERIFICATION_Bool_ValSeq» «doSlice(_,_,_,_)_MPY-SUBSCRIPT_Val_Val_OptInt_OptInt_OptInt» «reverseVS(_)_VERIFICATION_ValSeq_ValSeq» «sumIntVS(_)_VERIFICATION_Int_ValSeq» := by
  unfold Klean72WillItFly.Lemmas.targetStatement
  constructor
  · intro values
    rfl
  · intro gen9 gen8 gen7 gen6 gen5 gen4 gen3 gen2 gen1 gen0 kont values h
    simpa only [Int.zero_add, config] using
      sumAcc_correct gen9 gen8 gen7 gen6 gen5 gen4 gen3 gen2 gen1 gen0
        kont values 0 h

end Proof
