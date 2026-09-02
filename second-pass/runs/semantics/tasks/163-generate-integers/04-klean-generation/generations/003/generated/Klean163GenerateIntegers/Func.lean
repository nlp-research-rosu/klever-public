import Klean163GenerateIntegers.Inj

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

def _d3d9190 : SortBool → SortInt → SortValSeq → Option SortValSeq
  | false, _Gen0, REST => some REST
  | _, _, _ => none

def _e47590f : SortBool → SortInt → SortValSeq → Option SortValSeq
  | true, D, REST => some (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortInt SortVal) D) REST)
  | _, _, _ => none

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def _orBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_7174452 x0 x1) <|> (_991a329 x0 x1)

def «keepDigit(_,_,_)_VERIFICATION_ValSeq_Bool_Int_ValSeq» (x0 : SortBool) (x1 : SortInt) (x2 : SortValSeq) : Option SortValSeq := (_d3d9190 x0 x1 x2) <|> (_e47590f x0 x1 x2)

def _fbc13b2 : SortInt → SortInt → SortInt → Option SortBool
  | A, B, D => do
    let _Val0 <- «_<=Int_» A D
    let _Val1 <- «_<=Int_» D B
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- «_<=Int_» B D
    let _Val4 <- «_<=Int_» D A
    let _Val5 <- _andBool_ _Val3 _Val4
    let _Val6 <- _orBool_ _Val2 _Val5
    return _Val6

def «betweenEndpoints(_,_,_)_VERIFICATION_Bool_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) (x2 : SortInt) : Option SortBool := _fbc13b2 x0 x1 x2

def _fd73f04 : SortInt → SortInt → Option SortValSeq
  | A, B => do
    let _Val0 <- «betweenEndpoints(_,_,_)_VERIFICATION_Bool_Int_Int_Int» A B 2
    let _Val1 <- «betweenEndpoints(_,_,_)_VERIFICATION_Bool_Int_Int_Int» A B 4
    let _Val2 <- «betweenEndpoints(_,_,_)_VERIFICATION_Bool_Int_Int_Int» A B 6
    let _Val3 <- «betweenEndpoints(_,_,_)_VERIFICATION_Bool_Int_Int_Int» A B 8
    let _Val4 <- «keepDigit(_,_,_)_VERIFICATION_ValSeq_Bool_Int_ValSeq» _Val3 8 SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
    let _Val5 <- «keepDigit(_,_,_)_VERIFICATION_ValSeq_Bool_Int_ValSeq» _Val2 6 _Val4
    let _Val6 <- «keepDigit(_,_,_)_VERIFICATION_ValSeq_Bool_Int_ValSeq» _Val1 4 _Val5
    let _Val7 <- «keepDigit(_,_,_)_VERIFICATION_ValSeq_Bool_Int_ValSeq» _Val0 2 _Val6
    return _Val7

def «evenDigits(_,_)_VERIFICATION_ValSeq_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortValSeq := _fd73f04 x0 x1