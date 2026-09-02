import Klean85Add.Lemmas

namespace Proof

/- KORE symbol: Lbl'Unds'Map'Unds'; frozen source obligations: rule-97c5ca34b9b50dc1f2c9ed9ae56ea870fa5fc9060599752a28635a1372be2589. Replace this stub with its honest total meaning from the frozen K semantics. -/
def _Map_ (left right : SortMap) : SortMap :=
  ⟨left.coll ++ right.coll⟩
/- KORE symbol: Lbl'UndsPipe'-'-GT-Unds'; frozen source obligations: rule-97c5ca34b9b50dc1f2c9ed9ae56ea870fa5fc9060599752a28635a1372be2589. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_|->_» (key value : SortKItem) : SortMap :=
  ⟨[(key, value)]⟩
/- KORE symbol: LbladdAccSpec'LParUndsCommUndsCommUndsRParUnds'VERIFICATION'Unds'Int'Unds'IntSeq'Unds'Bool'Unds'Int; frozen source obligations: rule-97c5ca34b9b50dc1f2c9ed9ae56ea870fa5fc9060599752a28635a1372be2589. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «addAccSpec(_,_,_)_VERIFICATION_Int_IntSeq_Bool_Int» :
    SortIntSeq → SortBool → SortInt → SortInt
  | .«.IntSeq_MPY-CORE_IntSeq», _, acc => acc
  | .«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _ rest, false, acc =>
      «addAccSpec(_,_,_)_VERIFICATION_Int_IntSeq_Bool_Int» rest true acc
  | .«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» value rest, true, acc =>
      «addAccSpec(_,_,_)_VERIFICATION_Int_IntSeq_Bool_Int»
        rest false (if value % 2 = 0 then acc + value else acc)

theorem final :
    Klean85Add.Lemmas.targetStatement _Map_ «_|->_» «addAccSpec(_,_,_)_VERIFICATION_Int_IntSeq_Bool_Int» := by
  sorry

end Proof
