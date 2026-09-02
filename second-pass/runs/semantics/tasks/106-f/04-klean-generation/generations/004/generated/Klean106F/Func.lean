import Klean106F.Inj

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

axiom «_%Int_» (x0 : SortInt) (x1 : SortInt) : Option SortInt

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

axiom «.Map» : Option SortMap

axiom ListItem (x0 : SortKItem) : Option SortList

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList

axiom «.List» : Option SortList

def _4e0cfa9 : SortValSeq → SortInt → SortInt → SortInt → SortInt → Option SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», I, N, _F, _T => do
    let _Val0 <- «_>Int_» I N
    guard _Val0
    return true
  | _, _, _, _, _ => none

noncomputable def _2d78aae : SortInt → SortInt → Option SortInt
  | I1, I2 => do
    let _Val0 <- «_%Int_» I1 I2
    let _Val1 <- «_+Int_» _Val0 I2
    let _Val2 <- «_%Int_» _Val1 I2
    return _Val2

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

noncomputable def «pyMod(_,_)_MPY-INT_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := _2d78aae x0 x1

mutual
  noncomputable def _39e3697 : SortValSeq → SortInt → SortInt → SortInt → SortInt → Option SortBool
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (SortVal.inj_SortInt V) REST, I, N, F, T => do
      let _Val0 <- «_<=Int_» I N
      let _Val1 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» I 2
      let _Val2 <- «_==Int_» _Val1 0
      let _Val3 <- notBool_ _Val2
      let _Val4 <- _andBool_ _Val0 _Val3
      let _Val5 <- «_+Int_» T I
      let _Val6 <- «_==Int_» V _Val5
      let _Val7 <- _andBool_ _Val4 _Val6
      let _Val8 <- «_+Int_» I 1
      let _Val9 <- «_*Int_» F I
      let _Val10 <- «_+Int_» T I
      let _Val11 <- «outputOK(_,_,_,_,_)_VERIFICATION_Bool_ValSeq_Int_Int_Int_Int» REST _Val8 N _Val9 _Val10
      guard _Val7
      return _Val11
    | _, _, _, _, _ => none

  noncomputable def _42c32f9 : SortValSeq → SortInt → SortInt → SortInt → SortInt → Option SortBool
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» (SortVal.inj_SortInt V) REST, I, N, F, T => do
      let _Val0 <- «_<=Int_» I N
      let _Val1 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» I 2
      let _Val2 <- «_==Int_» _Val1 0
      let _Val3 <- _andBool_ _Val0 _Val2
      let _Val4 <- «_*Int_» F I
      let _Val5 <- «_==Int_» V _Val4
      let _Val6 <- _andBool_ _Val3 _Val5
      let _Val7 <- «_+Int_» I 1
      let _Val8 <- «_*Int_» F I
      let _Val9 <- «_+Int_» T I
      let _Val10 <- «outputOK(_,_,_,_,_)_VERIFICATION_Bool_ValSeq_Int_Int_Int_Int» REST _Val7 N _Val8 _Val9
      guard _Val6
      return _Val10
    | _, _, _, _, _ => none

  noncomputable def «outputOK(_,_,_,_,_)_VERIFICATION_Bool_ValSeq_Int_Int_Int_Int» (x0 : SortValSeq) (x1 : SortInt) (x2 : SortInt) (x3 : SortInt) (x4 : SortInt) : Option SortBool := (_39e3697 x0 x1 x2 x3 x4) <|> (_42c32f9 x0 x1 x2 x3 x4) <|> (_4e0cfa9 x0 x1 x2 x3 x4)
end