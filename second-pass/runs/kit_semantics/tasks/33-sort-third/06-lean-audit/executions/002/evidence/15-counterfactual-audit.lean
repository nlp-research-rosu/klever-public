import Proof

def identitySortThirdResult (values : SortValSeq) : SortValSeq := values

def operationalVsLen : SortValSeq → SortInt
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => 0
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _ rest =>
      operationalVsLen rest + 1

private theorem operationalVsLenNonnegative :
    ∀ values, (0 : Int) ≤ operationalVsLen values
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => by simp [operationalVsLen]
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _ rest => by
      simp only [operationalVsLen]
      have ih := operationalVsLenNonnegative rest
      omega

theorem identityBridgeAlsoPasses :
    Klean33SortThird.Lemmas.targetStatement
      Proof.«_<=Int_»
      identitySortThirdResult
      Proof.«valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»
      operationalVsLen := by
  rcases Proof.final with ⟨_, assoc, rightIdentity⟩
  refine ⟨?_, assoc, rightIdentity⟩
  intro VS h
  cases VS with
  | «.ValSeq_MPY-CORE_ValSeq» => rfl
  | «vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» value rest =>
      simp [Proof.«_<=Int_», operationalVsLen] at h
      have nonnegative := operationalVsLenNonnegative rest
      have positive : (0 : Int) < operationalVsLen rest + 1 := by omega
      exact (Int.not_le_of_gt positive h).elim
