import Proof

namespace AuditCounterfactual

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

def badIdentitySort (input : SortValSeq) : SortValSeq :=
  input

example : toInts (badIdentitySort (ofInts [2, 1])) = [1, 2] := rfl

end AuditCounterfactual
