import Proof
import Klean32FindZero.Func

namespace Stage5Audit

private abbrev emptyNumSeq : SortNumSeq :=
  SortNumSeq.«.NumSeq_VERIFICATION-SYNTAX_NumSeq»

private abbrev emptyValSeq : SortValSeq :=
  SortValSeq.«.ValSeq_MPY-CORE_ValSeq»

/- Universal operational connection to the generated total K function. -/
theorem candidate_matches_generated_k_function :
    (ns : SortNumSeq) →
      _root_.«numVals(_)_VERIFICATION-SYNTAX_ValSeq_NumSeq» ns =
        some (Proof.«numVals(_)_VERIFICATION-SYNTAX_ValSeq_NumSeq» ns)
  | SortNumSeq.«.NumSeq_VERIFICATION-SYNTAX_NumSeq» => by
      simp
        [_root_.«numVals(_)_VERIFICATION-SYNTAX_ValSeq_NumSeq»,
         _ef0f289, _f5e2fa2, _fe2b4c3,
         Proof.«numVals(_)_VERIFICATION-SYNTAX_ValSeq_NumSeq»]
  | SortNumSeq.«nFloat(_,_)_VERIFICATION-SYNTAX_NumSeq_Float_NumSeq» f rest => by
      simp
        [_root_.«numVals(_)_VERIFICATION-SYNTAX_ValSeq_NumSeq»,
         _ef0f289, _f5e2fa2, _fe2b4c3, inj,
         Proof.«numVals(_)_VERIFICATION-SYNTAX_ValSeq_NumSeq»,
         candidate_matches_generated_k_function rest]
      rfl
  | SortNumSeq.«nInt(_,_)_VERIFICATION-SYNTAX_NumSeq_Int_NumSeq» i rest => by
      simp
        [_root_.«numVals(_)_VERIFICATION-SYNTAX_ValSeq_NumSeq»,
         _ef0f289, _f5e2fa2, _fe2b4c3, inj,
         Proof.«numVals(_)_VERIFICATION-SYNTAX_ValSeq_NumSeq»,
         candidate_matches_generated_k_function rest]
      rfl

/- Boundary and mixed-constructor witnesses preserve order, payload, and sort. -/
example :
    Proof.«numVals(_)_VERIFICATION-SYNTAX_ValSeq_NumSeq» emptyNumSeq =
      emptyValSeq := rfl

example :
    Proof.«numVals(_)_VERIFICATION-SYNTAX_ValSeq_NumSeq»
        (SortNumSeq.«nInt(_,_)_VERIFICATION-SYNTAX_NumSeq_Int_NumSeq»
          7
          (SortNumSeq.«nFloat(_,_)_VERIFICATION-SYNTAX_NumSeq_Float_NumSeq»
            2.5 emptyNumSeq)) =
      SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
        (SortVal.inj_SortInt 7)
        (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
          (SortVal.inj_SortFloat 2.5)
          emptyValSeq) := rfl

/- Counterfactual 1: a constant bridge collapses distinct source sequences. -/
private def constantBridge (_ : SortNumSeq) : SortValSeq := emptyValSeq

theorem constant_bridge_rejected :
    ¬ Klean32FindZero.Lemmas.targetStatement constantBridge := by
  intro alleged
  have injectivity := alleged.2.1
  have impossible :=
    (injectivity
      emptyNumSeq
      (SortNumSeq.«nInt(_,_)_VERIFICATION-SYNTAX_NumSeq_Int_NumSeq»
        1 emptyNumSeq)).mp rfl
  simp at impossible

/- Counterfactual 2: retaining only the head loses the operational tail. -/
private def tailDroppingBridge : SortNumSeq → SortValSeq
  | SortNumSeq.«.NumSeq_VERIFICATION-SYNTAX_NumSeq» => emptyValSeq
  | SortNumSeq.«nInt(_,_)_VERIFICATION-SYNTAX_NumSeq_Int_NumSeq» i _ =>
      SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
        (SortVal.inj_SortInt i) emptyValSeq
  | SortNumSeq.«nFloat(_,_)_VERIFICATION-SYNTAX_NumSeq_Float_NumSeq» f _ =>
      SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
        (SortVal.inj_SortFloat f) emptyValSeq

theorem tail_dropping_bridge_rejected :
    ¬ Klean32FindZero.Lemmas.targetStatement tailDroppingBridge := by
  intro alleged
  have injectivity := alleged.2.1
  have impossible :=
    (injectivity
      (SortNumSeq.«nInt(_,_)_VERIFICATION-SYNTAX_NumSeq_Int_NumSeq»
        1 emptyNumSeq)
      (SortNumSeq.«nInt(_,_)_VERIFICATION-SYNTAX_NumSeq_Int_NumSeq»
        1
        (SortNumSeq.«nInt(_,_)_VERIFICATION-SYNTAX_NumSeq_Int_NumSeq»
          2 emptyNumSeq))).mp rfl
  simp at impossible

/- Counterfactual 3: hard-coding integer payloads violates injectivity. -/
private def hardCodedIntBridge : SortNumSeq → SortValSeq
  | SortNumSeq.«.NumSeq_VERIFICATION-SYNTAX_NumSeq» => emptyValSeq
  | SortNumSeq.«nInt(_,_)_VERIFICATION-SYNTAX_NumSeq_Int_NumSeq» _ rest =>
      SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
        (SortVal.inj_SortInt 0)
        (hardCodedIntBridge rest)
  | SortNumSeq.«nFloat(_,_)_VERIFICATION-SYNTAX_NumSeq_Float_NumSeq» f rest =>
      SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
        (SortVal.inj_SortFloat f)
        (hardCodedIntBridge rest)

theorem hard_coded_bridge_rejected :
    ¬ Klean32FindZero.Lemmas.targetStatement hardCodedIntBridge := by
  intro alleged
  have injectivity := alleged.2.1
  have impossible :=
    (injectivity
      (SortNumSeq.«nInt(_,_)_VERIFICATION-SYNTAX_NumSeq_Int_NumSeq»
        1 emptyNumSeq)
      (SortNumSeq.«nInt(_,_)_VERIFICATION-SYNTAX_NumSeq_Int_NumSeq»
        2 emptyNumSeq)).mp rfl
  simp at impossible

end Stage5Audit
