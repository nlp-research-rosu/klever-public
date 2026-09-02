import Klean138IsEqualToSumEven.Inj

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

axiom «_%Int_» (x0 : SortInt) (x1 : SortInt) : Option SortInt

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

noncomputable def _d99922d : SortInt → Option SortBool
  | N => do
    let _Val0 <- «_>=Int_» N 8
    let _Val1 <- «_%Int_» N 2
    let _Val2 <- «_==Int_» _Val1 0
    let _Val3 <- _andBool_ _Val0 _Val2
    return _Val3

noncomputable def _b3dd680 : SortInt → Option SortBool
  | N => do
    let _Val0 <- «_-Int_» N 6
    let _Val1 <- «_>Int_» _Val0 0
    let _Val2 <- «_-Int_» N 6
    let _Val3 <- «_%Int_» _Val2 2
    let _Val4 <- «_==Int_» _Val3 0
    let _Val5 <- _andBool_ _Val1 _Val4
    let _Val6 <- _andBool_ _Val5 true
    let _Val7 <- _andBool_ _Val6 true
    let _Val8 <- «_-Int_» N 6
    let _Val9 <- «_+Int_» _Val8 2
    let _Val10 <- «_+Int_» _Val9 2
    let _Val11 <- «_+Int_» _Val10 2
    let _Val12 <- «_==Int_» _Val11 N
    let _Val13 <- _andBool_ _Val7 _Val12
    return _Val13

noncomputable def «sumFourPositiveEvens(_)_VERIFICATION_Bool_Int» (x0 : SortInt) : Option SortBool := _d99922d x0

noncomputable def «canonicalWitnessesAreValid(_)_VERIFICATION_Bool_Int» (x0 : SortInt) : Option SortBool := _b3dd680 x0