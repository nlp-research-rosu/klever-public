import Klean8SumProduct.Inj

def _6b47af3 : SortInts → Option SortInt
  | SortInts.noInts => some 0
  | _ => none

def _30fd159 : SortInts → Option SortInt
  | SortInts.noInts => some 1
  | _ => none

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

axiom «.Map» : Option SortMap

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

mutual
  def «sumInts(_)_MPY_Int_Ints» (x0 : SortInts) : Option SortInt := (_6b47af3 x0) <|> (_f67990f x0)

  def _f67990f : SortInts → Option SortInt
    | SortInts.consInts I IS => do
      let _Val0 <- «sumInts(_)_MPY_Int_Ints» IS
      let _Val1 <- «_+Int_» I _Val0
      return _Val1
    | _ => none
end

mutual
  def _1522fc6 : SortInts → Option SortInt
    | SortInts.consInts I IS => do
      let _Val0 <- «productInts(_)_MPY_Int_Ints» IS
      let _Val1 <- «_*Int_» I _Val0
      return _Val1
    | _ => none

  def «productInts(_)_MPY_Int_Ints» (x0 : SortInts) : Option SortInt := (_1522fc6 x0) <|> (_30fd159 x0)
end

def _7eac054 : SortInts → Option SortPyVal
  | IS => do
    let _Val0 <- «sumInts(_)_MPY_Int_Ints» IS
    let _Val1 <- «productInts(_)_MPY_Int_Ints» IS
    return (SortPyVal.PyTuple (SortPyVal.PyInt _Val0) (SortPyVal.PyInt _Val1))

def «expectedSumProduct(_)_VERIFICATION_PyVal_Ints» (x0 : SortInts) : Option SortPyVal := _7eac054 x0