import Klean121Solution.Inj

def _105572a : SortK → Option SortBool
  | K => some false

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _92664aa : SortK → Option SortBool
  | SortK.kseq (SortKItem.inj_SortInt Int) SortK.dotk => some true
  | _ => none

def _d0a8392 : SortValSeq → Option SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some true
  | _ => none

def _5b64aff : SortVal → Option SortInt
  | SortVal.inj_SortInt I => some I
  | _ => none

axiom «_%Int_» (x0 : SortInt) (x1 : SortInt) : Option SortInt

def _b28ee4f : SortValSeq → SortBool → SortInt → Option SortInt
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq», _Gen0, ACC => some ACC
  | _, _, _ => none

axiom «.List» : Option SortList

axiom «.Map» : Option SortMap

axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

axiom ListItem (x0 : SortKItem) : Option SortList

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def isInt (x0 : SortK) : Option SortBool := (_92664aa x0) <|> (_105572a x0)

def «intProjection(_)_VERIFICATION_Int_Val» (x0 : SortVal) : Option SortInt := _5b64aff x0

noncomputable def _2d78aae : SortInt → SortInt → Option SortInt
  | I1, I2 => do
    let _Val0 <- «_%Int_» I1 I2
    let _Val1 <- «_+Int_» _Val0 I2
    let _Val2 <- «_%Int_» _Val1 I2
    return _Val2

mutual
  def _01539d8 : SortValSeq → Option SortBool
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V R => do
      let _Val0 <- isInt (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)
      let _Val1 <- «allInts(_)_VERIFICATION_Bool_ValSeq» R
      let _Val2 <- _andBool_ _Val0 _Val1
      return _Val2
    | _ => none

  def «allInts(_)_VERIFICATION_Bool_ValSeq» (x0 : SortValSeq) : Option SortBool := (_01539d8 x0) <|> (_d0a8392 x0)
end

noncomputable def «pyMod(_,_)_MPY-INT_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := _2d78aae x0 x1

mutual
  noncomputable def _294fd4d : SortValSeq → SortBool → SortInt → Option SortInt
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _Gen0 R, false, ACC => do
      let _Val0 <- «oddAtEvenAcc(_,_,_)_VERIFICATION_Int_ValSeq_Bool_Int» R true ACC
      return _Val0
    | _, _, _ => none

  noncomputable def _5a00258 : SortValSeq → SortBool → SortInt → Option SortInt
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V R, true, ACC => do
      let _Val0 <- «intProjection(_)_VERIFICATION_Int_Val» V
      let _Val1 <- «intProjection(_)_VERIFICATION_Int_Val» V
      let _Val2 <- «pyMod(_,_)_MPY-INT_Int_Int_Int» _Val1 2
      let _Val3 <- «_*Int_» _Val0 _Val2
      let _Val4 <- «_+Int_» ACC _Val3
      let _Val5 <- «oddAtEvenAcc(_,_,_)_VERIFICATION_Int_ValSeq_Bool_Int» R false _Val4
      return _Val5
    | _, _, _ => none

  noncomputable def «oddAtEvenAcc(_,_,_)_VERIFICATION_Int_ValSeq_Bool_Int» (x0 : SortValSeq) (x1 : SortBool) (x2 : SortInt) : Option SortInt := (_294fd4d x0 x1 x2) <|> (_5a00258 x0 x1 x2) <|> (_b28ee4f x0 x1 x2)
end

noncomputable def _1438213 : SortValSeq → SortBool → Option SortInt
  | VS, B => do
    let _Val0 <- «oddAtEvenAcc(_,_,_)_VERIFICATION_Int_ValSeq_Bool_Int» VS B 0
    return _Val0

noncomputable def «oddAtEvenPositions(_,_)_VERIFICATION_Int_ValSeq_Bool» (x0 : SortValSeq) (x1 : SortBool) : Option SortInt := _1438213 x0 x1