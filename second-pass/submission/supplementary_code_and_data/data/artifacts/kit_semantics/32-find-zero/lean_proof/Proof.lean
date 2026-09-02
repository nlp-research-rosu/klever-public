import Klean32FindZero.Lemmas

namespace Proof

/- KORE symbol: LblnumVals'LParUndsRParUnds'VERIFICATION-SYNTAX'Unds'ValSeq'Unds'NumSeq; frozen source obligations: rule-0dfb3ea463a2e10ce61e8445bcf95e2aa2d4748b432b47ccd1f9825f8cca2630, rule-f684bfbef1c0219f754e562f1888c8a1b7236498affdcf8c5681f52ef8e6175f, rule-4f3a4fc13d02a156f3a8d695f13fdac54badb56cceabf4cbe100c7ea4aca4d57, rule-f2662dddafe1054c19c3ddaf31b8c9e9a8971c2baafdf6d7f8bfb1785b1ff321. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «numVals(_)_VERIFICATION-SYNTAX_ValSeq_NumSeq» : SortNumSeq → SortValSeq
  | SortNumSeq.«.NumSeq_VERIFICATION-SYNTAX_NumSeq» =>
      SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
  | SortNumSeq.«nInt(_,_)_VERIFICATION-SYNTAX_NumSeq_Int_NumSeq» i rest =>
      SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
        (SortVal.inj_SortInt i)
        («numVals(_)_VERIFICATION-SYNTAX_ValSeq_NumSeq» rest)
  | SortNumSeq.«nFloat(_,_)_VERIFICATION-SYNTAX_NumSeq_Float_NumSeq» f rest =>
      SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
        (SortVal.inj_SortFloat f)
        («numVals(_)_VERIFICATION-SYNTAX_ValSeq_NumSeq» rest)

private def decodeNumVals : SortValSeq → Option SortNumSeq
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» =>
      some SortNumSeq.«.NumSeq_VERIFICATION-SYNTAX_NumSeq»
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
      (SortVal.inj_SortInt i) rest => do
        let decodedRest ← decodeNumVals rest
        pure
          (SortNumSeq.«nInt(_,_)_VERIFICATION-SYNTAX_NumSeq_Int_NumSeq»
            i decodedRest)
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
      (SortVal.inj_SortFloat f) rest => do
        let decodedRest ← decodeNumVals rest
        pure
          (SortNumSeq.«nFloat(_,_)_VERIFICATION-SYNTAX_NumSeq_Float_NumSeq»
            f decodedRest)
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _ _ => none

private theorem decode_numVals (ns : SortNumSeq) :
    decodeNumVals («numVals(_)_VERIFICATION-SYNTAX_ValSeq_NumSeq» ns) =
      some ns := by
  induction ns <;>
    simp_all
      [«numVals(_)_VERIFICATION-SYNTAX_ValSeq_NumSeq», decodeNumVals]

private theorem numVals_injective {left right : SortNumSeq}
    (equality :
      «numVals(_)_VERIFICATION-SYNTAX_ValSeq_NumSeq» left =
        «numVals(_)_VERIFICATION-SYNTAX_ValSeq_NumSeq» right) :
    left = right := by
  have decodedEquality := congrArg decodeNumVals equality
  simpa only [decode_numVals, Option.some.injEq] using decodedEquality

theorem final :
    Klean32FindZero.Lemmas.targetStatement «numVals(_)_VERIFICATION-SYNTAX_ValSeq_NumSeq» := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro ns
    constructor
    · intro equality
      apply numVals_injective
      simpa [«numVals(_)_VERIFICATION-SYNTAX_ValSeq_NumSeq»] using equality
    · intro equality
      cases equality
      rfl
  · intro ns₂ ns₁
    constructor
    · exact numVals_injective
    · intro equality
      cases equality
      rfl
  · intro rest i ns
    constructor
    · intro equality
      apply numVals_injective
      simpa [«numVals(_)_VERIFICATION-SYNTAX_ValSeq_NumSeq»] using equality
    · intro equality
      cases equality
      rfl
  · intro rest f ns
    constructor
    · intro equality
      apply numVals_injective
      simpa [«numVals(_)_VERIFICATION-SYNTAX_ValSeq_NumSeq»] using equality
    · intro equality
      cases equality
      rfl

end Proof
