import Klean127Intersection.Lemmas

namespace Proof

/- KORE symbol: Lbl'Unds'Map'Unds'; frozen source obligations: rule-5cdc3db730891902bebfc52c9ef2d3ed5f0ac955c8c9731b0522f080198846d0. Replace this stub with its honest total meaning from the frozen K semantics. -/
def _Map_ (left right : SortMap) : SortMap :=
  ⟨left.coll ++ right.coll⟩

private noncomputable def sameKItem (left right : SortKItem) : Bool := by
  classical
  exact if left = right then true else false

/- KORE symbol: Lbl'Unds'in'Unds'keys'LParUndsRParUnds'MAP'Unds'Bool'Unds'KItem'Unds'Map; frozen source obligations: rule-5cdc3db730891902bebfc52c9ef2d3ed5f0ac955c8c9731b0522f080198846d0. Replace this stub with its honest total meaning from the frozen K semantics. -/
noncomputable def «_in_keys(_)_MAP_Bool_KItem_Map»
    (key : SortKItem) (map : SortMap) : SortBool :=
  map.coll.any fun entry => sameKItem key entry.1

/- KORE symbol: Lbl'UndsLSqBUnds-LT-'-undef'RSqB'; frozen source obligations: rule-5cdc3db730891902bebfc52c9ef2d3ed5f0ac955c8c9731b0522f080198846d0. Replace this stub with its honest total meaning from the frozen K semantics. -/
noncomputable def «_[_<-undef]» (map : SortMap) (key : SortKItem) : SortMap :=
  ⟨map.coll.filter fun entry => !sameKItem key entry.1⟩

/- KORE symbol: Lbl'UndsPipe'-'-GT-Unds'; frozen source obligations: rule-5cdc3db730891902bebfc52c9ef2d3ed5f0ac955c8c9731b0522f080198846d0. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_|->_» (key value : SortKItem) : SortMap :=
  ⟨[(key, value)]⟩

/- KORE symbol: LblnotBool'Unds'; frozen source obligations: rule-5cdc3db730891902bebfc52c9ef2d3ed5f0ac955c8c9731b0522f080198846d0. Replace this stub with its honest total meaning from the frozen K semantics. -/
def notBool_ (value : SortBool) : SortBool :=
  !value

theorem final :
    Klean127Intersection.Lemmas.targetStatement _Map_ «_in_keys(_)_MAP_Bool_KItem_Map» «_[_<-undef]» «_|->_» notBool_ := by
  intro _REST frame
  exact nomatch frame

end Proof
