import Klean139SpecialFactorial.Inj

axiom «.List» : Option SortList

axiom «.Map» : Option SortMap

axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

axiom ListItem (x0 : SortKItem) : Option SortList

def _506e766 : SortInt → Option SortInt
  | N => do
    let _Val0 <- «_<=Int_» N 0
    guard _Val0
    return 1

def _74e4d5f : SortInt → Option SortInt
  | N => do
    let _Val0 <- «_<=Int_» N 0
    guard _Val0
    return 1

axiom «factorial(_)_VERIFICATION_Int_Int» (x0 : SortInt) : Option SortInt
axiom _fe27f40 : SortInt → Option SortInt

axiom _525148f : SortInt → Option SortInt
axiom «specialFactorial(_)_VERIFICATION_Int_Int» (x0 : SortInt) : Option SortInt