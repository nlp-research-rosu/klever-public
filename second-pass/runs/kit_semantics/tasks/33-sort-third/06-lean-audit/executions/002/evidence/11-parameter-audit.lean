import Proof

private abbrev nil : SortValSeq := SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
private abbrev iv (n : Int) : SortVal := SortVal.inj_SortInt n
private abbrev cons (v : SortVal) (vs : SortValSeq) : SortValSeq :=
  SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» v vs

private abbrev singleton (n : Int) := cons (iv n) nil

private abbrev input : SortValSeq :=
  cons (iv 5) (cons (iv 6) (cons (iv 3) (cons (iv 4)
    (cons (iv 8) (cons (iv 9) (cons (iv 2) nil))))))

private abbrev expected : SortValSeq :=
  cons (iv 2) (cons (iv 6) (cons (iv 3) (cons (iv 4)
    (cons (iv 8) (cons (iv 9) (cons (iv 5) nil))))))

example : Proof.«_<=Int_» (-1) 0 = true := rfl
example : Proof.«_<=Int_» 1 0 = false := rfl
example : Proof.«vsLen(_)_MPY-CORE_Int_ValSeq» input = 7 := rfl
example :
    Proof.«valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»
      (cons (iv 1) (singleton 2)) (singleton 3) =
      cons (iv 1) (cons (iv 2) (singleton 3)) := rfl
example : Proof.«sortThirdResult(_)_VERIFICATION_ValSeq_ValSeq» input = expected := rfl

#reduce Proof.«_<=Int_» (-1) 0
#reduce Proof.«_<=Int_» 1 0
#reduce Proof.«vsLen(_)_MPY-CORE_Int_ValSeq» input
#reduce Proof.«sortThirdResult(_)_VERIFICATION_ValSeq_ValSeq» input
