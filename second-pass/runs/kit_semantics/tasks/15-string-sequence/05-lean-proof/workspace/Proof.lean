import Klean15StringSequence.Lemmas

namespace Proof

private def intSeqOfChars : List Char → SortIntSeq
  | [] => SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
  | c :: cs =>
      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq»
        (Int.ofNat c.toNat)
        (intSeqOfChars cs)

private def seqConcatModel : SortIntSeq → SortIntSeq → SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», ys => ys
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» x xs, ys =>
      SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq»
        x
        (seqConcatModel xs ys)

private def appendRenderedInt (acc : SortIntSeq) (i : SortInt) : SortIntSeq :=
  seqConcatModel
    (seqConcatModel
      acc
      (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq»
        32
        SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»))
    (intSeqOfChars (toString i).toList)

private def sequenceAccGo : Nat → SortIntSeq → SortInt → SortIntSeq
  | 0, acc, _ => acc
  | fuel + 1, acc, i =>
      sequenceAccGo fuel (appendRenderedInt acc i) (i + 1)

/- KORE symbol: Lbl'Unds-LT-Eqls'Int'Unds'; frozen source obligations: rule-5cd1e3b5568df299d3f434281eb340a991725f175ade15ddce1a4febdab6d0fc. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_<=Int_» (x y : SortInt) : SortBool := decide (x ≤ y)
/- KORE symbol: Lbl'UndsPlus'Int'Unds'; frozen source obligations: rule-5cd1e3b5568df299d3f434281eb340a991725f175ade15ddce1a4febdab6d0fc. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_+Int_» (x y : SortInt) : SortInt := x + y
/- KORE symbol: LblInt2String'LParUndsRParUnds'STRING-COMMON'Unds'String'Unds'Int; frozen source obligations: rule-5cd1e3b5568df299d3f434281eb340a991725f175ade15ddce1a4febdab6d0fc. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «Int2String(_)_STRING-COMMON_String_Int»
    (x : SortInt) : SortString :=
  toString x
/- KORE symbol: LblseqConcat'LParUndsCommUndsRParUnds'MPY-STR'Unds'IntSeq'Unds'IntSeq'Unds'IntSeq; frozen source obligations: rule-5cd1e3b5568df299d3f434281eb340a991725f175ade15ddce1a4febdab6d0fc. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq»
    (xs ys : SortIntSeq) : SortIntSeq :=
  seqConcatModel xs ys
/- KORE symbol: LblsequenceAcc'LParUndsCommUndsCommUndsRParUnds'VERIFICATION'Unds'IntSeq'Unds'IntSeq'Unds'Int'Unds'Int; frozen source obligations: rule-5cd1e3b5568df299d3f434281eb340a991725f175ade15ddce1a4febdab6d0fc. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «sequenceAcc(_,_,_)_VERIFICATION_IntSeq_IntSeq_Int_Int»
    (acc : SortIntSeq) (i n : SortInt) : SortIntSeq :=
  sequenceAccGo (n - i + 1).toNat acc i
/- KORE symbol: LblstrToCodes'LParUndsRParUnds'MPY-STR'Unds'IntSeq'Unds'String; frozen source obligations: rule-5cd1e3b5568df299d3f434281eb340a991725f175ade15ddce1a4febdab6d0fc. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «strToCodes(_)_MPY-STR_IntSeq_String»
    (s : SortString) : SortIntSeq :=
  intSeqOfChars s.toList

theorem final :
    Klean15StringSequence.Lemmas.targetStatement «_<=Int_» «_+Int_» «Int2String(_)_STRING-COMMON_String_Int» «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» «sequenceAcc(_,_,_)_VERIFICATION_IntSeq_IntSeq_Int_Int» «strToCodes(_)_MPY-STR_IntSeq_String» := by
  intro N I ACC h
  have hle : I ≤ N := by
    simpa [«_<=Int_»] using h
  have hremaining : 0 ≤ N - I := Int.sub_nonneg_of_le hle
  have hshift : N - (I + 1) + 1 = N - I := by
    simp [Int.sub_eq_add_neg, Int.neg_add, Int.add_assoc]
  have hone : (0 : Int) ≤ 1 := by
    decide
  have hfuel :
      (N - I + 1).toNat = Nat.succ (N - (I + 1) + 1).toNat := by
    rw [hshift, Int.toNat_add hremaining hone]
    simp
  simp only [
    «sequenceAcc(_,_,_)_VERIFICATION_IntSeq_IntSeq_Int_Int»,
    «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq»,
    «strToCodes(_)_MPY-STR_IntSeq_String»,
    «Int2String(_)_STRING-COMMON_String_Int»,
    «_+Int_»
  ]
  rw [hfuel]
  rfl

end Proof
