import Proof

namespace OperationalAudit

def emptyIS : SortIntSeq :=
  SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»

def singleton7 : SortIntSeq :=
  SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 7 emptyIS

def sample : SortIntSeq :=
  SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 7
    (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» (-2)
      (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 5 emptyIS))

def expectedVals : SortValSeq :=
  SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (SortVal.inj_SortInt 7)
    (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (SortVal.inj_SortInt (-2))
      (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (SortVal.inj_SortInt 5)
        SortValSeq.«.ValSeq_MPY-CORE_ValSeq»))

-- Positive and adversarial boundary examples for every target parameter.
example : Proof._andBool_ true false = false := rfl
example : Proof._andBool_ true true = true := rfl
example : Proof._andBool_ false true = false := rfl
example : Proof._andBool_ false false = false := rfl
example : Proof.«_<Int_» 2 3 = true := rfl
example : Proof.«_<Int_» 3 2 = false := rfl
example : Proof.«_<Int_» (-5) 0 = true := rfl
example : Proof.«_<Int_» 3 3 = false := rfl
example : Proof.«_<=Int_» 3 3 = true := rfl
example : Proof.«_<=Int_» 4 3 = false := rfl
example : Proof.«_<=Int_» (-5) (-5) = true := rfl
example : Proof.«_<=Int_» 0 (-5) = false := rfl

example : Proof.«intAt(_,_)_VERIFICATION_Int_IntSeq_Int» emptyIS 42 = 0 := rfl
example : Proof.«intAt(_,_)_VERIFICATION_Int_IntSeq_Int» sample 0 = 7 := rfl
example : Proof.«intAt(_,_)_VERIFICATION_Int_IntSeq_Int» sample 1 = -2 := rfl
example : Proof.«intAt(_,_)_VERIFICATION_Int_IntSeq_Int» sample 2 = 5 := rfl
example : Proof.«intAt(_,_)_VERIFICATION_Int_IntSeq_Int» sample (-1) = 0 := rfl
example : Proof.«intAt(_,_)_VERIFICATION_Int_IntSeq_Int» sample 3 = 0 := rfl

example : Proof.«intVals(_)_VERIFICATION_ValSeq_IntSeq» sample = expectedVals := rfl
example : Proof.«isLen(_)_MPY-CORE_Int_IntSeq» emptyIS = 0 := rfl
example : Proof.«isLen(_)_MPY-CORE_Int_IntSeq» sample = 3 := rfl
example :
    Proof.«valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int» expectedVals 0 =
      SortVal.inj_SortInt 7 := rfl
example :
    Proof.«valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int» expectedVals 1 =
      SortVal.inj_SortInt (-2) := rfl
example :
    Proof.«valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int» expectedVals 2 =
      SortVal.inj_SortInt 5 := rfl
example :
    Proof.«valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int» expectedVals (-1) =
      SortVal.«noneV_MPY-CORE_Val» := rfl
example :
    Proof.«valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int» expectedVals 3 =
      SortVal.«noneV_MPY-CORE_Val» := rfl
example : Proof.«vsLen(_)_MPY-CORE_Int_ValSeq» expectedVals = 3 := rfl

-- Counterfactual implementations.
def alwaysFalseAnd (_ _ : SortBool) : SortBool := false
def zeroIntAt (_ : SortIntSeq) (_ : SortInt) : SortInt := 0
def emptyIntVals (_ : SortIntSeq) : SortValSeq :=
  SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
def zeroVsLen (_ : SortValSeq) : SortInt := 0

-- This dishonest Boolean bridge makes the guarded conjunct vacuous and still
-- satisfies the generated target. This is why the separate operational-bridge
-- audit is essential; the actual candidate does not use this mutation.
theorem alwaysFalseAnd_is_vacuously_accepted :
    Klean40TriplesSumToZero.Lemmas.targetStatement
      alwaysFalseAnd
      Proof.«_<Int_»
      Proof.«_<=Int_»
      Proof.«intAt(_,_)_VERIFICATION_Int_IntSeq_Int»
      Proof.«intVals(_)_VERIFICATION_ValSeq_IntSeq»
      Proof.«isLen(_)_MPY-CORE_Int_IntSeq»
      Proof.«valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int»
      Proof.«vsLen(_)_MPY-CORE_Int_ValSeq» := by
  unfold Klean40TriplesSumToZero.Lemmas.targetStatement
  constructor
  · exact Proof.final.1
  · intro index intSeq guarded
    simp [alwaysFalseAnd] at guarded

-- A constant length and an empty embedding are rejected by the first conjunct.
theorem zeroVsLen_is_rejected :
    ¬ Klean40TriplesSumToZero.Lemmas.targetStatement
      Proof._andBool_
      Proof.«_<Int_»
      Proof.«_<=Int_»
      Proof.«intAt(_,_)_VERIFICATION_Int_IntSeq_Int»
      Proof.«intVals(_)_VERIFICATION_ValSeq_IntSeq»
      Proof.«isLen(_)_MPY-CORE_Int_IntSeq»
      Proof.«valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int»
      zeroVsLen := by
  intro claimed
  have bad := claimed.1 singleton7
  simp [
    singleton7,
    emptyIS,
    zeroVsLen,
    Proof.«intVals(_)_VERIFICATION_ValSeq_IntSeq»,
    Proof.«isLen(_)_MPY-CORE_Int_IntSeq»
  ] at bad

theorem emptyIntVals_is_rejected :
    ¬ Klean40TriplesSumToZero.Lemmas.targetStatement
      Proof._andBool_
      Proof.«_<Int_»
      Proof.«_<=Int_»
      Proof.«intAt(_,_)_VERIFICATION_Int_IntSeq_Int»
      emptyIntVals
      Proof.«isLen(_)_MPY-CORE_Int_IntSeq»
      Proof.«valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int»
      Proof.«vsLen(_)_MPY-CORE_Int_ValSeq» := by
  intro claimed
  have bad := claimed.1 singleton7
  simp [
    singleton7,
    emptyIS,
    emptyIntVals,
    Proof.«isLen(_)_MPY-CORE_Int_IntSeq»,
    Proof.«vsLen(_)_MPY-CORE_Int_ValSeq»
  ] at bad

-- A constant element accessor is rejected by the guarded second conjunct.
theorem zeroIntAt_is_rejected :
    ¬ Klean40TriplesSumToZero.Lemmas.targetStatement
      Proof._andBool_
      Proof.«_<Int_»
      Proof.«_<=Int_»
      zeroIntAt
      Proof.«intVals(_)_VERIFICATION_ValSeq_IntSeq»
      Proof.«isLen(_)_MPY-CORE_Int_IntSeq»
      Proof.«valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int»
      Proof.«vsLen(_)_MPY-CORE_Int_ValSeq» := by
  intro claimed
  have bad := claimed.2 0 singleton7 (by rfl)
  simp [
    singleton7,
    emptyIS,
    zeroIntAt,
    Proof.«intVals(_)_VERIFICATION_ValSeq_IntSeq»,
    Proof.«valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int»
  ] at bad

end OperationalAudit
