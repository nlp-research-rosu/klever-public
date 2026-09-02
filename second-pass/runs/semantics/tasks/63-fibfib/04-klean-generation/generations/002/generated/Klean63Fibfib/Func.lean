import Klean63Fibfib.Inj

axiom «.List» : Option SortList

axiom «.Map» : Option SortMap

axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

axiom ListItem (x0 : SortKItem) : Option SortList

def _c4644d5 : SortInt → SortInt → SortInt → SortInt → Option SortInt
  | A, _B, _C, N => do
    let _Val0 <- «_<=Int_» N 0
    guard _Val0
    return A

axiom _0c911c7 : SortInt → SortInt → SortInt → SortInt → Option SortInt
axiom «fibFrom(_,_,_,_)_FIBFIB-VERIFICATION_Int_Int_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) (x2 : SortInt) (x3 : SortInt) : Option SortInt