import Proof

namespace AuditOperationalBridge

def valNil : SortValSeq :=
  .«.ValSeq_MPY-CORE_ValSeq»

def valCons (head : SortVal) (tail : SortValSeq) : SortValSeq :=
  .«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» head tail

def intVal (value : Int) : SortVal :=
  .inj_SortInt value

def ofInts : List Int → SortValSeq
  | [] => valNil
  | head :: tail => valCons (intVal head) (ofInts tail)

def toInts : SortValSeq → List Int
  | .«.ValSeq_MPY-CORE_ValSeq» => []
  | .«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (.inj_SortInt head) tail =>
      head :: toInts tail
  | .«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _ tail =>
      toInts tail

#eval toInts (Proof.sortVS (ofInts [-3, -4, 5]))
#eval toInts (Proof.sortVS (ofInts [4, -4, 4]))
#eval toInts (Proof.sortVS (ofInts [3, 2, 1, 0, -1]))
#eval toInts (Proof.sortVS (ofInts [-7, -7, 0, 2, 2]))

example : toInts (Proof.sortVS (ofInts [-3, -4, 5])) = [-4, -3, 5] := rfl
example : toInts (Proof.sortVS (ofInts [4, -4, 4])) = [-4, 4, 4] := rfl
example : toInts (Proof.sortVS (ofInts [3, 2, 1, 0, -1])) = [-1, 0, 1, 2, 3] := rfl
example : toInts (Proof.sortVS (ofInts [-7, -7, 0, 2, 2])) = [-7, -7, 0, 2, 2] := rfl
example : toInts (Proof.sortVS (ofInts [2, 1])) = [1, 2] := rfl

example :
    Proof.«vsLen(_)_MPY-CORE_Int_ValSeq» (ofInts [8, 5, 3, 0, -9]) = 5 :=
  rfl

def badIdentitySort (input : SortValSeq) : SortValSeq :=
  input

def badConstantSort (_ : SortValSeq) : SortValSeq :=
  valNil

def badZeroLength (_ : SortValSeq) : SortInt :=
  0

theorem target_admits_identity :
    Klean120Maximum.Lemmas.targetStatement
      badIdentitySort
      Proof.«vsLen(_)_MPY-CORE_Int_ValSeq» := by
  intro input
  rfl

theorem target_admits_constants :
    Klean120Maximum.Lemmas.targetStatement badConstantSort badZeroLength := by
  intro input
  rfl

#print axioms AuditOperationalBridge.target_admits_identity
#print axioms AuditOperationalBridge.target_admits_constants

end AuditOperationalBridge
