import Proof

namespace WrongSumMutation

def empty : SortValSeq := SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
def cons (head : SortVal) (tail : SortValSeq) : SortValSeq :=
  SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» head tail
def intVal (value : SortInt) : SortVal := SortVal.inj_SortInt value
def values : SortValSeq :=
  cons (intVal 3) (cons (intVal (-2)) (cons (intVal 7) empty))

def wrongSum (_ : SortValSeq) : SortInt := 0

example : wrongSum values = 8 := by
  rfl

end WrongSumMutation
