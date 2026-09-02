import Klean75IsMultiplyPrime.Inj

axiom «.Map» : Option SortMap

def _991a329 : SortBool → SortBool → Option SortBool
  | false, B => some B
  | _, _ => none

def _7174452 : SortBool → SortBool → Option SortBool
  | true, _Gen0 => some true
  | _, _ => none

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

def _orBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_7174452 x0 x1) <|> (_991a329 x0 x1)

def _4a3ddd1 : SortInt → Option SortBool
  | A => do
    let _Val0 <- «_==Int_» A 8
    let _Val1 <- «_==Int_» A 12
    let _Val2 <- _orBool_ _Val0 _Val1
    let _Val3 <- «_==Int_» A 18
    let _Val4 <- _orBool_ _Val2 _Val3
    let _Val5 <- «_==Int_» A 20
    let _Val6 <- _orBool_ _Val4 _Val5
    let _Val7 <- «_==Int_» A 27
    let _Val8 <- _orBool_ _Val6 _Val7
    let _Val9 <- «_==Int_» A 28
    let _Val10 <- _orBool_ _Val8 _Val9
    let _Val11 <- «_==Int_» A 30
    let _Val12 <- _orBool_ _Val10 _Val11
    let _Val13 <- «_==Int_» A 42
    let _Val14 <- _orBool_ _Val12 _Val13
    let _Val15 <- «_==Int_» A 44
    let _Val16 <- _orBool_ _Val14 _Val15
    let _Val17 <- «_==Int_» A 45
    let _Val18 <- _orBool_ _Val16 _Val17
    let _Val19 <- «_==Int_» A 50
    let _Val20 <- _orBool_ _Val18 _Val19
    let _Val21 <- «_==Int_» A 52
    let _Val22 <- _orBool_ _Val20 _Val21
    let _Val23 <- «_==Int_» A 63
    let _Val24 <- _orBool_ _Val22 _Val23
    let _Val25 <- «_==Int_» A 66
    let _Val26 <- _orBool_ _Val24 _Val25
    let _Val27 <- «_==Int_» A 68
    let _Val28 <- _orBool_ _Val26 _Val27
    let _Val29 <- «_==Int_» A 70
    let _Val30 <- _orBool_ _Val28 _Val29
    let _Val31 <- «_==Int_» A 75
    let _Val32 <- _orBool_ _Val30 _Val31
    let _Val33 <- «_==Int_» A 76
    let _Val34 <- _orBool_ _Val32 _Val33
    let _Val35 <- «_==Int_» A 78
    let _Val36 <- _orBool_ _Val34 _Val35
    let _Val37 <- «_==Int_» A 92
    let _Val38 <- _orBool_ _Val36 _Val37
    let _Val39 <- «_==Int_» A 98
    let _Val40 <- _orBool_ _Val38 _Val39
    let _Val41 <- «_==Int_» A 99
    let _Val42 <- _orBool_ _Val40 _Val41
    return _Val42

def «isThreePrimeProductBelow100(_)_VERIFICATION_Bool_Int» (x0 : SortInt) : Option SortBool := _4a3ddd1 x0