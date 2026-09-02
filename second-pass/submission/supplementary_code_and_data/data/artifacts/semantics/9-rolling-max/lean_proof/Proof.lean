import Klean9RollingMax.Lemmas

namespace Proof

/- KORE symbol: LblfirstAfter'LParUndsCommUndsRParUnds'VERIFICATION'Unds'Bool'Unds'IntSeq'Unds'Bool; frozen source obligations: rule-49d35612d63bf56fdd624a16c30b97a62ddbf196c0acb5a07976bc8b31be1a41. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «firstAfter(_,_)_VERIFICATION_Bool_IntSeq_Bool» :
    SortIntSeq → SortBool → SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», flag => flag
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ _, _ => false

theorem final :
    Klean9RollingMax.Lemmas.targetStatement «firstAfter(_,_)_VERIFICATION_Bool_IntSeq_Bool» := by
  intro input
  cases input <;> rfl

end Proof
