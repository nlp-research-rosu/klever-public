import Klean55Fib.Inj

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

axiom «.List» : Option SortList

axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList

axiom ListItem (x0 : SortKItem) : Option SortList

axiom «.Map» : Option SortMap

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

noncomputable def _788dd96 : SortInt → SortInt → SortInt → SortInt → Option SortInt
  | A, _Gen0, I, N => do
    let _Val0 <- «_>=Int_» I N
    guard _Val0
    return A

axiom _4906759 : SortInt → SortInt → SortInt → SortInt → Option SortInt
axiom «fibRun(_,_,_,_)_FIB-VERIFICATION_Int_Int_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) (x2 : SortInt) (x3 : SortInt) : Option SortInt

noncomputable def _161d5b5 : SortInt → Option SortInt
  | N => do
    let _Val0 <- «fibRun(_,_,_,_)_FIB-VERIFICATION_Int_Int_Int_Int_Int» 0 1 0 N
    return _Val0

noncomputable def «fibSpec(_)_FIB-VERIFICATION_Int_Int» (x0 : SortInt) : Option SortInt := _161d5b5 x0