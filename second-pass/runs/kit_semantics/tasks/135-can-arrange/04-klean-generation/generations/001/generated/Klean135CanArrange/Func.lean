import Klean135CanArrange.Inj

def _105572a : SortK → Option SortBool
  | K => some false

def _495da55 : SortK → Option SortBool
  | K => some false

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _613283e : SortK → Option SortBool
  | K => some false

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _7174452 : SortBool → SortBool → Option SortBool
  | true, _Gen0 => some true
  | _, _ => none

def _92664aa : SortK → Option SortBool
  | SortK.kseq (SortKItem.inj_SortInt Int) SortK.dotk => some true
  | _ => none

def _95cb29f : SortK → Option SortBool
  | SortK.kseq (SortKItem.inj_SortStr Str) SortK.dotk => some true
  | _ => none

def _991a329 : SortBool → SortBool → Option SortBool
  | false, B => some B
  | _, _ => none

def _d74a36c : SortK → Option SortBool
  | SortK.kseq (SortKItem.inj_SortFloat Float) SortK.dotk => some true
  | _ => none

def _dadad71 : SortK → Option SortBool
  | SortK.kseq (SortKItem.inj_SortBool Bool) SortK.dotk => some true
  | _ => none

def _e10ded0 : SortK → Option SortBool
  | K => some false

noncomputable local instance : DecidableEq SortKItem :=
  Classical.typeDecidableEq SortKItem

private noncomputable def kleanMapLookupModel
    (entries : List (SortKItem × SortKItem))
    (key : SortKItem) : Option SortKItem :=
  match entries with
  | [] => none
  | (candidate, value) :: rest =>
      if candidate = key then some value
      else kleanMapLookupModel rest key

private noncomputable def kleanMapContainsModel
    (entries : List (SortKItem × SortKItem))
    (key : SortKItem) : Bool :=
  match entries with
  | [] => false
  | (candidate, _) :: rest =>
      if candidate = key then true
      else kleanMapContainsModel rest key

private noncomputable def kleanMapDisjointModel
    (left right : List (SortKItem × SortKItem)) : Bool :=
  match right with
  | [] => true
  | (key, _) :: rest =>
      if kleanMapContainsModel left key then false
      else kleanMapDisjointModel left rest

private noncomputable def kleanMapDeleteModel
    (entries : List (SortKItem × SortKItem))
    (key : SortKItem) : List (SortKItem × SortKItem) :=
  match entries with
  | [] => []
  | (candidate, value) :: rest =>
      if candidate = key then kleanMapDeleteModel rest key
      else (candidate, value) :: kleanMapDeleteModel rest key

private noncomputable def kleanMapUpdateModel
    (entries : List (SortKItem × SortKItem))
    (key value : SortKItem) : List (SortKItem × SortKItem) :=
  match entries with
  | [] => [(key, value)]
  | (candidate, oldValue) :: rest =>
      if candidate = key then (key, value) :: rest
      else (candidate, oldValue) :: kleanMapUpdateModel rest key value

noncomputable def «.List» : Option SortList := some ⟨[]⟩

noncomputable def «.Map» : Option SortMap := some ⟨[]⟩

noncomputable def _List_ (x0 : SortList) (x1 : SortList) : Option SortList := some ⟨x0.coll ++ x1.coll⟩

noncomputable def _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap :=
  if kleanMapDisjointModel x0.coll x1.coll then
    some ⟨x0.coll ++ x1.coll⟩
  else none

noncomputable def «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap :=
  some ⟨[(x0, x1)]⟩

noncomputable def ListItem (x0 : SortKItem) : Option SortList :=
  some ⟨[x0]⟩

axiom «arrangeSeq(_,_,_,_)_VERIFICATION-BASE_Int_ValSeq_Int_Val_Int» (x0 : SortValSeq) (x1 : SortInt) (x2 : SortVal) (x3 : SortInt) : Option SortInt

axiom «orderGe(_,_)_VERIFICATION-BASE_Bool_Val_Val» (x0 : SortVal) (x1 : SortVal) : Option SortBool

axiom «scanDefined(_,_,_)_VERIFICATION-BASE_Bool_ValSeq_Int_Val» (x0 : SortValSeq) (x1 : SortInt) (x2 : SortVal) : Option SortBool

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def isInt (x0 : SortK) : Option SortBool := (_92664aa x0) <|> (_105572a x0)

def _orBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_7174452 x0 x1) <|> (_991a329 x0 x1)

def isFloat (x0 : SortK) : Option SortBool := (_d74a36c x0) <|> (_613283e x0)

def isBool (x0 : SortK) : Option SortBool := (_dadad71 x0) <|> (_495da55 x0)

def isStr (x0 : SortK) : Option SortBool := (_95cb29f x0) <|> (_e10ded0 x0)

def _5dde7dc : SortVal → Option SortBool
  | V => do
    let _Val0 <- isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
    let _Val1 <- isBool (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
    let _Val2 <- _orBool_ _Val0 _Val1
    let _Val3 <- isFloat (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
    let _Val4 <- _orBool_ _Val2 _Val3
    return _Val4

def «isNumericVal(_)_VERIFICATION-BASE_Bool_Val» (x0 : SortVal) : Option SortBool := _5dde7dc x0

def _1ec0a31 : SortVal → SortVal → Option SortBool
  | V, W => do
    let _Val0 <- «isNumericVal(_)_VERIFICATION-BASE_Bool_Val» V
    let _Val1 <- «isNumericVal(_)_VERIFICATION-BASE_Bool_Val» W
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- isStr (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
    let _Val4 <- isStr (SortK.kseq ((@inj SortVal SortKItem) W) SortK.dotk)
    let _Val5 <- _andBool_ _Val3 _Val4
    let _Val6 <- _orBool_ _Val2 _Val5
    return _Val6

def «orderablePair(_,_)_VERIFICATION-BASE_Bool_Val_Val» (x0 : SortVal) (x1 : SortVal) : Option SortBool := _1ec0a31 x0 x1