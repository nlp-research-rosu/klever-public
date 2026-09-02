import Klean133SumSquares.Inj

def _2e1d3f7 : SortVal → SortValSeq → Option SortVal
  | CURRENT, SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some CURRENT
  | _, _ => none

axiom «.Map» : Option SortMap

axiom ListItem (x0 : SortKItem) : Option SortList

axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList

axiom «_^Int_» (x0 : SortInt) (x1 : SortInt) : Option SortInt

def _e307d06 : SortInt → SortValSeq → Option SortInt
  | ACC, SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some ACC
  | _, _ => none

def _0f9305e : SortVal → Option SortInt
  | SortVal.inj_SortInt I => some I
  | _ => none

axiom «ceilFloat(_)_FLOAT_Float_Float» (x0 : SortFloat) : Option SortFloat

axiom «Float2Int(_)_FLOAT_Int_Float» (x0 : SortFloat) : Option SortInt

axiom «.List» : Option SortList

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

mutual
  def _88a3bd5 : SortVal → SortValSeq → Option SortVal
    | _Gen0, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V REST => do
      let _Val0 <- «lastFrom(_,_)_SUM-SQUARES-VERIFICATION-BASE_Val_Val_ValSeq» V REST
      return _Val0
    | _, _ => none

  def «lastFrom(_,_)_SUM-SQUARES-VERIFICATION-BASE_Val_Val_ValSeq» (x0 : SortVal) (x1 : SortValSeq) : Option SortVal := (_2e1d3f7 x0 x1) <|> (_88a3bd5 x0 x1)
end

noncomputable def _3836331 : SortVal → Option SortInt
  | SortVal.inj_SortFloat F => do
    let _Val0 <- «ceilFloat(_)_FLOAT_Float_Float» F
    let _Val1 <- «Float2Int(_)_FLOAT_Int_Float» _Val0
    return _Val1
  | _ => none

noncomputable def ceilF (x0 : SortVal) : Option SortInt := (_0f9305e x0) <|> (_3836331 x0)

mutual
  noncomputable def «sumSquaresFrom(_,_)_SUM-SQUARES-VERIFICATION-BASE_Int_Int_ValSeq» (x0 : SortInt) (x1 : SortValSeq) : Option SortInt := (_bbb0ffe x0 x1) <|> (_e307d06 x0 x1)

  noncomputable def _bbb0ffe : SortInt → SortValSeq → Option SortInt
    | ACC, SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V REST => do
      let _Val0 <- ceilF V
      let _Val1 <- «_^Int_» _Val0 2
      let _Val2 <- «_+Int_» ACC _Val1
      let _Val3 <- «sumSquaresFrom(_,_)_SUM-SQUARES-VERIFICATION-BASE_Int_Int_ValSeq» _Val2 REST
      return _Val3
    | _, _ => none
end