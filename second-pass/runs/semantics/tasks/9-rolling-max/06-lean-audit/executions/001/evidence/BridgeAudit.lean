import Proof
import Klean9RollingMax.Func

open Klean9RollingMax

private def empty : SortIntSeq :=
  SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»

private def one : SortIntSeq :=
  SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 7 empty

private def two : SortIntSeq :=
  SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» (-3) one

example : Proof.«firstAfter(_,_)_VERIFICATION_Bool_IntSeq_Bool» empty true = true := rfl
example : Proof.«firstAfter(_,_)_VERIFICATION_Bool_IntSeq_Bool» empty false = false := rfl
example : Proof.«firstAfter(_,_)_VERIFICATION_Bool_IntSeq_Bool» one true = false := rfl
example : Proof.«firstAfter(_,_)_VERIFICATION_Bool_IntSeq_Bool» one false = false := rfl
example : Proof.«firstAfter(_,_)_VERIFICATION_Bool_IntSeq_Bool» two true = false := rfl

theorem candidate_agrees_with_generated_k_function
    (input : SortIntSeq) (flag : SortBool) :
    _root_.«firstAfter(_,_)_VERIFICATION_Bool_IntSeq_Bool» input flag =
      some (Proof.«firstAfter(_,_)_VERIFICATION_Bool_IntSeq_Bool» input flag) := by
  cases input <;> cases flag <;> rfl

private def constantFalse : SortIntSeq → SortBool → SortBool :=
  fun _ _ => false

theorem constantFalse_can_prove_target :
    Klean9RollingMax.Lemmas.targetStatement constantFalse := by
  intro input
  rfl

example : constantFalse empty true ≠
    Proof.«firstAfter(_,_)_VERIFICATION_Bool_IntSeq_Bool» empty true := by
  decide

private def identityFlag : SortIntSeq → SortBool → SortBool :=
  fun _ flag => flag

theorem identityFlag_can_prove_target :
    Klean9RollingMax.Lemmas.targetStatement identityFlag := by
  intro input
  rfl

example : identityFlag one true ≠
    Proof.«firstAfter(_,_)_VERIFICATION_Bool_IntSeq_Bool» one true := by
  decide

example :
    Klean9RollingMax.Lemmas.targetStatement
      Proof.«firstAfter(_,_)_VERIFICATION_Bool_IntSeq_Bool» :=
  Proof.final
