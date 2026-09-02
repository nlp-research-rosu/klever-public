import Klean124ValidDate.Inj

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

def _1ff8f4d {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, B1, _Gen0 => do
    guard C
    return B1

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

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

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def _3d3398a : SortInt → SortInt → Option SortInt
  | T, O => do
    let _Val0 <- «_-Int_» T 48
    let _Val1 <- «_*Int_» _Val0 10
    let _Val2 <- «_+Int_» _Val1 O
    let _Val3 <- «_-Int_» _Val2 48
    return _Val3

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def _orBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_7174452 x0 x1) <|> (_991a329 x0 x1)

def _2f3f58a {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, _Gen0, B2 => do
    let _Val0 <- notBool_ C
    guard _Val0
    return B2

def «dateNumber(_,_)_VALID-DATE-VERIFICATION_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := _3d3398a x0 x1

def _61e9db7 : SortInt → Option SortBool
  | C => do
    let _Val0 <- «_<=Int_» 48 C
    let _Val1 <- «_<=Int_» C 57
    let _Val2 <- _andBool_ _Val0 _Val1
    return _Val2

def kite {SortSort : Type} (x0 : SortBool) (x1 : SortSort) (x2 : SortSort) : Option SortSort := (_1ff8f4d x0 x1 x2) <|> (_2f3f58a x0 x1 x2)

def «digitCode(_)_VALID-DATE-VERIFICATION_Bool_Int» (x0 : SortInt) : Option SortBool := _61e9db7 x0

def _7c45515 : SortInt → Option SortInt
  | M => do
    let _Val0 <- «_==Int_» M 2
    let _Val1 <- «_==Int_» M 4
    let _Val2 <- «_==Int_» M 6
    let _Val3 <- _orBool_ _Val1 _Val2
    let _Val4 <- «_==Int_» M 9
    let _Val5 <- _orBool_ _Val3 _Val4
    let _Val6 <- «_==Int_» M 11
    let _Val7 <- _orBool_ _Val5 _Val6
    let _Val8 <- kite _Val7 30 31
    let _Val9 <- kite _Val0 29 _Val8
    return _Val9

def «dateLimit(_)_VALID-DATE-VERIFICATION_Int_Int» (x0 : SortInt) : Option SortInt := _7c45515 x0

def _fae6be7 : SortInt → SortInt → SortInt → SortInt → SortInt → SortInt → SortInt → SortInt → SortInt → SortInt → Option SortBool
  | M0, M1, SEP1, D0, D1, SEP2, Y0, Y1, Y2, Y3 => do
    let _Val0 <- «_==Int_» SEP1 45
    let _Val1 <- «_==Int_» SEP2 45
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- «digitCode(_)_VALID-DATE-VERIFICATION_Bool_Int» M0
    let _Val4 <- _andBool_ _Val2 _Val3
    let _Val5 <- «digitCode(_)_VALID-DATE-VERIFICATION_Bool_Int» M1
    let _Val6 <- _andBool_ _Val4 _Val5
    let _Val7 <- «digitCode(_)_VALID-DATE-VERIFICATION_Bool_Int» D0
    let _Val8 <- _andBool_ _Val6 _Val7
    let _Val9 <- «digitCode(_)_VALID-DATE-VERIFICATION_Bool_Int» D1
    let _Val10 <- _andBool_ _Val8 _Val9
    let _Val11 <- «digitCode(_)_VALID-DATE-VERIFICATION_Bool_Int» Y0
    let _Val12 <- _andBool_ _Val10 _Val11
    let _Val13 <- «digitCode(_)_VALID-DATE-VERIFICATION_Bool_Int» Y1
    let _Val14 <- _andBool_ _Val12 _Val13
    let _Val15 <- «digitCode(_)_VALID-DATE-VERIFICATION_Bool_Int» Y2
    let _Val16 <- _andBool_ _Val14 _Val15
    let _Val17 <- «digitCode(_)_VALID-DATE-VERIFICATION_Bool_Int» Y3
    let _Val18 <- _andBool_ _Val16 _Val17
    let _Val19 <- «dateNumber(_,_)_VALID-DATE-VERIFICATION_Int_Int_Int» M0 M1
    let _Val20 <- «_<=Int_» 1 _Val19
    let _Val21 <- _andBool_ _Val18 _Val20
    let _Val22 <- «dateNumber(_,_)_VALID-DATE-VERIFICATION_Int_Int_Int» M0 M1
    let _Val23 <- «_<=Int_» _Val22 12
    let _Val24 <- _andBool_ _Val21 _Val23
    let _Val25 <- «dateNumber(_,_)_VALID-DATE-VERIFICATION_Int_Int_Int» D0 D1
    let _Val26 <- «_<=Int_» 1 _Val25
    let _Val27 <- _andBool_ _Val24 _Val26
    let _Val28 <- «dateNumber(_,_)_VALID-DATE-VERIFICATION_Int_Int_Int» D0 D1
    let _Val29 <- «dateNumber(_,_)_VALID-DATE-VERIFICATION_Int_Int_Int» M0 M1
    let _Val30 <- «dateLimit(_)_VALID-DATE-VERIFICATION_Int_Int» _Val29
    let _Val31 <- «_<=Int_» _Val28 _Val30
    let _Val32 <- _andBool_ _Val27 _Val31
    return _Val32

def «validDate10(_,_,_,_,_,_,_,_,_,_)_VALID-DATE-VERIFICATION_Bool_Int_Int_Int_Int_Int_Int_Int_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) (x2 : SortInt) (x3 : SortInt) (x4 : SortInt) (x5 : SortInt) (x6 : SortInt) (x7 : SortInt) (x8 : SortInt) (x9 : SortInt) : Option SortBool := _fae6be7 x0 x1 x2 x3 x4 x5 x6 x7 x8 x9