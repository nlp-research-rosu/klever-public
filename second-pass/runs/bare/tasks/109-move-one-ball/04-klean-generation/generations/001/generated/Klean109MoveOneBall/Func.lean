import Klean109MoveOneBall.Inj

def _edd22d4 : SortIList → Option SortInt
  | SortIList.«_::__HUMAN-EVAL-SYNTAX_IList_Int_IList» I SortIList.«.IList_HUMAN-EVAL-SYNTAX_IList» => some I
  | _ => none

def _725427b : SortInt → SortIList → Option SortInt
  | _PREVIOUS, SortIList.«.IList_HUMAN-EVAL-SYNTAX_IList» => some 0
  | _, _ => none

def _2e6fee5 : SortIList → Option SortInt
  | SortIList.«.IList_HUMAN-EVAL-SYNTAX_IList» => some 0
  | _ => none

def _2289f6a : SortIList → Option SortInt
  | SortIList.«.IList_HUMAN-EVAL-SYNTAX_IList» => some 0
  | _ => none

mutual
  def _7d53305 : SortIList → Option SortInt
    | SortIList.«_::__HUMAN-EVAL-SYNTAX_IList_Int_IList» _I (SortIList.«_::__HUMAN-EVAL-SYNTAX_IList_Int_IList» J IS) => do
      let _Val0 <- «last(_)_HUMAN-EVAL-VERIFICATION_Int_IList» (SortIList.«_::__HUMAN-EVAL-SYNTAX_IList_Int_IList» J IS)
      return _Val0
    | _ => none

  def «last(_)_HUMAN-EVAL-VERIFICATION_Int_IList» (x0 : SortIList) : Option SortInt := (_7d53305 x0) <|> (_edd22d4 x0)
end

def _7252351 : SortInt → SortInt → Option SortInt
  | I, J => do
    let _Val0 <- «_>Int_» I J
    guard _Val0
    return 1

def _3808e3f : SortInt → SortInt → Option SortInt
  | I, J => do
    let _Val0 <- «_<=Int_» I J
    guard _Val0
    return 0

mutual
  def _1de452d : SortIList → Option SortInt
    | SortIList.«_::__HUMAN-EVAL-SYNTAX_IList_Int_IList» _I IS => do
      let _Val0 <- «length(_)_HUMAN-EVAL-VERIFICATION_Int_IList» IS
      let _Val1 <- «_+Int_» 1 _Val0
      return _Val1
    | _ => none

  def «length(_)_HUMAN-EVAL-VERIFICATION_Int_IList» (x0 : SortIList) : Option SortInt := (_1de452d x0) <|> (_2e6fee5 x0)
end

def «dropBit(_,_)_HUMAN-EVAL-VERIFICATION_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := (_3808e3f x0 x1) <|> (_7252351 x0 x1)

mutual
  def _6ff344a : SortInt → SortIList → Option SortInt
    | PREVIOUS, SortIList.«_::__HUMAN-EVAL-SYNTAX_IList_Int_IList» I IS => do
      let _Val0 <- «dropBit(_,_)_HUMAN-EVAL-VERIFICATION_Int_Int_Int» PREVIOUS I
      let _Val1 <- «dropsFrom(_,_)_HUMAN-EVAL-VERIFICATION_Int_Int_IList» I IS
      let _Val2 <- «_+Int_» _Val0 _Val1
      return _Val2
    | _, _ => none

  def «dropsFrom(_,_)_HUMAN-EVAL-VERIFICATION_Int_Int_IList» (x0 : SortInt) (x1 : SortIList) : Option SortInt := (_6ff344a x0 x1) <|> (_725427b x0 x1)
end

def _524a687 : SortIList → Option SortInt
  | SortIList.«_::__HUMAN-EVAL-SYNTAX_IList_Int_IList» I IS => do
    let _Val0 <- «last(_)_HUMAN-EVAL-VERIFICATION_Int_IList» (SortIList.«_::__HUMAN-EVAL-SYNTAX_IList_Int_IList» I IS)
    let _Val1 <- «dropsFrom(_,_)_HUMAN-EVAL-VERIFICATION_Int_Int_IList» _Val0 (SortIList.«_::__HUMAN-EVAL-SYNTAX_IList_Int_IList» I IS)
    return _Val1
  | _ => none

def «cyclicDrops(_)_HUMAN-EVAL-VERIFICATION_Int_IList» (x0 : SortIList) : Option SortInt := (_2289f6a x0) <|> (_524a687 x0)

def _28ab6ac : SortIList → Option SortBool
  | L => do
    let _Val0 <- «cyclicDrops(_)_HUMAN-EVAL-VERIFICATION_Int_IList» L
    let _Val1 <- «_<=Int_» _Val0 1
    return _Val1

def «rotationSortable(_)_HUMAN-EVAL-VERIFICATION_Bool_IList» (x0 : SortIList) : Option SortBool := _28ab6ac x0