import Klean44ChangeBase.Inj

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

axiom «.Map» : Option SortMap

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

axiom «.List» : Option SortList

axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList

axiom ListItem (x0 : SortKItem) : Option SortList

axiom «baseDigits(_,_)_VERIFICATION_IntSeq_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortIntSeq

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

noncomputable def _be6edda : SortInt → SortMap → Option SortBool
  | _Gen0, _Pat0 => match (MapHook SortKItem SortKItem).size _Pat0.coll with
    | 0 => some true
    | _ => none

axiom _2e5365a : SortInt → SortMap → Option SortBool
axiom «freshScopes(_,_)_VERIFICATION_Bool_Int_Map» (x0 : SortInt) (x1 : SortMap) : Option SortBool