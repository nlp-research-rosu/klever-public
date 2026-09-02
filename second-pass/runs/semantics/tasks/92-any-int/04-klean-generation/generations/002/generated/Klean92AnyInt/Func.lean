import Klean92AnyInt.Inj

def _7174452 : SortBool → SortBool → Option SortBool
  | true, _Gen0 => some true
  | _, _ => none

def _991a329 : SortBool → SortBool → Option SortBool
  | false, B => some B
  | _, _ => none

axiom «.List» : Option SortList

axiom «.Map» : Option SortMap

axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

axiom ListItem (x0 : SortKItem) : Option SortList

def _orBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_7174452 x0 x1) <|> (_991a329 x0 x1)

def _f82a43a : SortInt → SortInt → SortInt → Option SortBool
  | X, Y, Z => do
    let _Val0 <- «_+Int_» X Y
    let _Val1 <- «_==Int_» _Val0 Z
    let _Val2 <- «_+Int_» X Z
    let _Val3 <- «_==Int_» _Val2 Y
    let _Val4 <- _orBool_ _Val1 _Val3
    let _Val5 <- «_+Int_» Y Z
    let _Val6 <- «_==Int_» _Val5 X
    let _Val7 <- _orBool_ _Val4 _Val6
    return _Val7

def «sumCondition(_,_,_)_ANY-INT-VERIFICATION_Bool_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) (x2 : SortInt) : Option SortBool := _f82a43a x0 x1 x2