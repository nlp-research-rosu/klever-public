import Klean63Fibfib.Inj

def _b32bb5f : SortInt → Option SortInt
  | 2 => some 1
  | _ => none

def _2e2f28f : SortInt → Option SortInt
  | N => do
    let _Val0 <- «_<=Int_» N 1
    guard _Val0
    return 0

axiom _009ee55 : SortInt → Option SortInt
axiom «fibfibMath(_)_FIBFIB-VERIFICATION_Int_Int» (x0 : SortInt) : Option SortInt