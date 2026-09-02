import Proof

private abbrev nil : SortValSeq :=
  SortValSeq.«.ValSeq_MPY-CORE_ValSeq»

private abbrev cons (v : SortVal) (vs : SortValSeq) : SortValSeq :=
  SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» v vs

private abbrev t : SortVal := SortVal.inj_SortBool true
private abbrev f : SortVal := SortVal.inj_SortBool false

private abbrev boolInput : SortValSeq :=
  cons t (cons t (cons f (cons f nil)))

private abbrev sourceExpected : SortValSeq :=
  cons f (cons t (cons f (cons t nil)))

example :
    Proof.«sortThirdResult(_)_VERIFICATION_ValSeq_ValSeq» boolInput = boolInput :=
  rfl

example :
    Proof.«sortThirdResult(_)_VERIFICATION_ValSeq_ValSeq» boolInput ≠ sourceExpected := by
  intro h
  cases h

#reduce Proof.«sortThirdResult(_)_VERIFICATION_ValSeq_ValSeq» boolInput
#reduce sourceExpected
