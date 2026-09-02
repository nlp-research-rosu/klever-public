import Proof

namespace WrongSliceMutation

def empty : SortValSeq := SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
def cons (head : SortVal) (tail : SortValSeq) : SortValSeq :=
  SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» head tail
def intVal (value : SortInt) : SortVal := SortVal.inj_SortInt value
def values : SortValSeq :=
  cons (intVal 3) (cons (intVal (-2)) (cons (intVal 7) empty))

def wrongDoSlice :
    SortVal → SortOptInt → SortOptInt → SortOptInt → SortVal
  | SortVal.inj_SortIterable
      (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» input),
      SortOptInt.«noB_MPY-SUBSCRIPT_OptInt»,
      SortOptInt.«noB_MPY-SUBSCRIPT_OptInt»,
      SortOptInt.«someB(_)_MPY-SUBSCRIPT_OptInt_Int» (-1) =>
      SortVal.inj_SortIterable
        (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» input)
  | _, _, _, _ => SortVal.«noneV_MPY-CORE_Val»

example :
    wrongDoSlice
        (SortVal.inj_SortIterable
          (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» values))
        SortOptInt.«noB_MPY-SUBSCRIPT_OptInt»
        SortOptInt.«noB_MPY-SUBSCRIPT_OptInt»
        (SortOptInt.«someB(_)_MPY-SUBSCRIPT_OptInt_Int» (-1)) =
      SortVal.inj_SortIterable
        (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq»
          (Proof.«reverseVS(_)_VERIFICATION_ValSeq_ValSeq» values)) := by
  rfl

end WrongSliceMutation
