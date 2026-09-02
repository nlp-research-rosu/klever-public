import Klean52BelowThreshold.Inj

def _37d95b8 : SortIntSeq → SortInt → Option SortBool
  | SortIntSeq.«nil_MPY-SYNTAX_IntSeq», _T => some true
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

mutual
  def _481a21e : SortIntSeq → SortInt → Option SortBool
    | SortIntSeq.«cons(_,_)_MPY-SYNTAX_IntSeq_Int_IntSeq» I XS, T => do
      let _Val0 <- «_<Int_» I T
      let _Val1 <- «allBelow(_,_)_VERIFICATION_Bool_IntSeq_Int» XS T
      let _Val2 <- _andBool_ _Val0 _Val1
      return _Val2
    | _, _ => none

  def «allBelow(_,_)_VERIFICATION_Bool_IntSeq_Int» (x0 : SortIntSeq) (x1 : SortInt) : Option SortBool := (_37d95b8 x0 x1) <|> (_481a21e x0 x1)
end