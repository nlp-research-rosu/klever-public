import Klean83StartsOneEnds.Inj

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

axiom «_^Int_» (x0 : SortInt) (x1 : SortInt) : Option SortInt

def _ce6228e : SortInt → Option SortInt
  | 1 => some 1
  | _ => none

axiom «.Map» : Option SortMap

noncomputable def _ca48972 : SortInt → Option SortInt
  | K => do
    let _Val0 <- «_>=Int_» K 0
    let _Val1 <- «_^Int_» 10 K
    guard _Val0
    return _Val1

noncomputable def «decimalMiddles(_)_VERIFICATION_Int_Int» (x0 : SortInt) : Option SortInt := _ca48972 x0

noncomputable def _4d8431a : SortInt → Option SortInt
  | N => do
    let _Val0 <- «_>Int_» N 1
    let _Val1 <- «_-Int_» N 2
    let _Val2 <- «decimalMiddles(_)_VERIFICATION_Int_Int» _Val1
    guard _Val0
    return _Val2

noncomputable def _29aa67c : SortInt → Option SortInt
  | N => do
    let _Val0 <- «_>Int_» N 1
    let _Val1 <- «_-Int_» N 2
    let _Val2 <- «decimalMiddles(_)_VERIFICATION_Int_Int» _Val1
    let _Val3 <- «_*Int_» 10 _Val2
    guard _Val0
    return _Val3

noncomputable def _8694cd6 : SortInt → Option SortInt
  | N => do
    let _Val0 <- «_>Int_» N 1
    let _Val1 <- «_-Int_» N 2
    let _Val2 <- «decimalMiddles(_)_VERIFICATION_Int_Int» _Val1
    let _Val3 <- «_*Int_» 9 _Val2
    guard _Val0
    return _Val3

noncomputable def «startsAndEndsWithOne(_)_VERIFICATION_Int_Int» (x0 : SortInt) : Option SortInt := _4d8431a x0

noncomputable def «startsWithOne(_)_VERIFICATION_Int_Int» (x0 : SortInt) : Option SortInt := _29aa67c x0

noncomputable def «endsWithOne(_)_VERIFICATION_Int_Int» (x0 : SortInt) : Option SortInt := _8694cd6 x0

noncomputable def _579350c : SortInt → Option SortInt
  | N => do
    let _Val0 <- «_>Int_» N 1
    let _Val1 <- «startsWithOne(_)_VERIFICATION_Int_Int» N
    let _Val2 <- «endsWithOne(_)_VERIFICATION_Int_Int» N
    let _Val3 <- «_+Int_» _Val1 _Val2
    let _Val4 <- «startsAndEndsWithOne(_)_VERIFICATION_Int_Int» N
    let _Val5 <- «_-Int_» _Val3 _Val4
    guard _Val0
    return _Val5

noncomputable def «qualifyingCount(_)_VERIFICATION_Int_Int» (x0 : SortInt) : Option SortInt := (_579350c x0) <|> (_ce6228e x0)