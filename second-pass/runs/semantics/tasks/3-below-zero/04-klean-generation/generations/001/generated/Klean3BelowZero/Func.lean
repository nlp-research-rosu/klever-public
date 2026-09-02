import Klean3BelowZero.Inj

def _1ff8f4d {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, B1, _Gen0 => do
    guard C
    return B1

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

def _cb69d61 : SortInt → SortIntVals → Option SortBool
  | _Gen0, SortIntVals.«.IntVals_BELOW-ZERO-COMMON_IntVals» => some false
  | _, _ => none

axiom «.List» : Option SortList

axiom ListItem (x0 : SortKItem) : Option SortList

axiom «.Map» : Option SortMap

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def _2f3f58a {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, _Gen0, B2 => do
    let _Val0 <- notBool_ C
    guard _Val0
    return B2

def kite {SortSort : Type} (x0 : SortBool) (x1 : SortSort) (x2 : SortSort) : Option SortSort := (_1ff8f4d x0 x1 x2) <|> (_2f3f58a x0 x1 x2)

mutual
  def _95b59b0 : SortInt → SortIntVals → Option SortBool
    | B, SortIntVals.«intCons(_,_)_BELOW-ZERO-COMMON_IntVals_Int_IntVals» I IS => do
      let _Val0 <- «_+Int_» B I
      let _Val1 <- «_<Int_» _Val0 0
      let _Val2 <- «_+Int_» B I
      let _Val3 <- «prefixBelow(_,_)_BELOW-ZERO-COMMON_Bool_Int_IntVals» _Val2 IS
      let _Val4 <- kite _Val1 true _Val3
      return _Val4
    | _, _ => none

  def «prefixBelow(_,_)_BELOW-ZERO-COMMON_Bool_Int_IntVals» (x0 : SortInt) (x1 : SortIntVals) : Option SortBool := (_95b59b0 x0 x1) <|> (_cb69d61 x0 x1)
end