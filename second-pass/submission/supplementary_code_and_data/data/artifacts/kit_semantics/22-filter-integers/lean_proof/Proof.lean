import Klean22FilterIntegers.Lemmas

namespace Proof

/- KORE symbol: Lbl'Unds'orBool'Unds'; frozen source obligations: rule-55b672e7a2348769766678767d4f1ec37801c590e4687ecb281112debaebe350. Replace this stub with its honest total meaning from the frozen K semantics. -/
def _orBool_ (left right : SortBool) : SortBool := left || right
/- KORE symbol: LblisBool; frozen source obligations: rule-55b672e7a2348769766678767d4f1ec37801c590e4687ecb281112debaebe350. Replace this stub with its honest total meaning from the frozen K semantics. -/
def isBool : SortK → SortBool
  | SortK.kseq (SortKItem.inj_SortBool _) SortK.dotk => true
  | _ => false
/- KORE symbol: LblisInt; frozen source obligations: rule-55b672e7a2348769766678767d4f1ec37801c590e4687ecb281112debaebe350. Replace this stub with its honest total meaning from the frozen K semantics. -/
def isInt : SortK → SortBool
  | SortK.kseq (SortKItem.inj_SortInt _) SortK.dotk => true
  | _ => false
/- KORE symbol: LblisIntV'LParUndsRParUnds'MPY-BUILTINS'Unds'Bool'Unds'Val; frozen source obligations: rule-55b672e7a2348769766678767d4f1ec37801c590e4687ecb281112debaebe350. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «isIntV(_)_MPY-BUILTINS_Bool_Val» : SortVal → SortBool
  | SortVal.inj_SortBool _ => true
  | SortVal.inj_SortInt _ => true
  | _ => false

theorem final :
    Klean22FilterIntegers.Lemmas.targetStatement _orBool_ isBool isInt «isIntV(_)_MPY-BUILTINS_Bool_Val» := by
  intro V
  cases V <;> rfl

end Proof
