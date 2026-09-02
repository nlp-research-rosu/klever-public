import Klean3BelowZero.Inj

def _1ff8f4d {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, B1, _Gen0 => do
    guard C
    return B1

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _51abe17 : SortInt → SortIntList → Option SortBool
  | _Gen0, SortIntList.«.IntList_MPY-SYNTAX_IntList» => some false
  | _, _ => none

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def _2f3f58a {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, _Gen0, B2 => do
    let _Val0 <- notBool_ C
    guard _Val0
    return B2

def kite {SortSort : Type} (x0 : SortBool) (x1 : SortSort) (x2 : SortSort) : Option SortSort := (_1ff8f4d x0 x1 x2) <|> (_2f3f58a x0 x1 x2)

mutual
  def _5bb6a09 : SortInt → SortIntList → Option SortBool
    | B, SortIntList.«cons(_,_)_MPY-SYNTAX_IntList_Int_IntList» I IS => do
      let _Val0 <- «_+Int_» B I
      let _Val1 <- «_<Int_» _Val0 0
      let _Val2 <- «_+Int_» B I
      let _Val3 <- «belowZeroFrom(_,_)_VERIFICATION_Bool_Int_IntList» _Val2 IS
      let _Val4 <- kite _Val1 true _Val3
      return _Val4
    | _, _ => none

  def «belowZeroFrom(_,_)_VERIFICATION_Bool_Int_IntList» (x0 : SortInt) (x1 : SortIntList) : Option SortBool := (_51abe17 x0 x1) <|> (_5bb6a09 x0 x1)
end