import Klean114Minsubarraysum.Inj

def _4082f88 : SortIntSeq → SortInt → Option SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», LAST => some LAST
  | _, _ => none

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

def _72cfa46 : SortIntSeq → SortInt → SortInt → Option SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _C, B => some B
  | _, _, _ => none

axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList

def _c7787dc : SortIntSeq → SortInt → Option SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», C => some C
  | _, _ => none

def _a66427b : SortValSeq → SortInt → Option SortVal
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V _Gen0, 0 => some V
  | _, _ => none

axiom «.Map» : Option SortMap

axiom «.List» : Option SortList

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

axiom ListItem (x0 : SortKItem) : Option SortList

mutual
  def «lastFrom(_,_)_VERIFICATION-BASE_Int_IntSeq_Int» (x0 : SortIntSeq) (x1 : SortInt) : Option SortInt := (_4082f88 x0 x1) <|> (_dd02ce3 x0 x1)

  def _dd02ce3 : SortIntSeq → SortInt → Option SortInt
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» I R, _LAST => do
      let _Val0 <- «lastFrom(_,_)_VERIFICATION-BASE_Int_IntSeq_Int» R I
      return _Val0
    | _, _ => none
end

def _a12317b : SortInt → SortInt → Option SortInt
  | A, B => do
    let _Val0 <- «_<Int_» A B
    guard _Val0
    return A

def _43fa584 : SortInt → SortInt → Option SortInt
  | A, B => do
    let _Val0 <- «_>=Int_» A B
    guard _Val0
    return B

mutual
  def _86fc1c7 : SortValSeq → SortInt → Option SortVal
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» _Gen0 S, I => do
      let _Val0 <- «_>Int_» I 0
      let _Val1 <- «_-Int_» I 1
      let _Val2 <- «valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int» S _Val1
      guard _Val0
      return _Val2
    | _, _ => none

  def «valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int» (x0 : SortValSeq) (x1 : SortInt) : Option SortVal := (_86fc1c7 x0 x1) <|> (_a66427b x0 x1)
end

def «chooseSmaller(_,_)_VERIFICATION-BASE_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := (_43fa584 x0 x1) <|> (_a12317b x0 x1)

def _903225a : SortInt → SortInt → Option SortInt
  | I, C => do
    let _Val0 <- «_+Int_» C I
    let _Val1 <- «chooseSmaller(_,_)_VERIFICATION-BASE_Int_Int_Int» I _Val0
    return _Val1

def «nextCurrent(_,_)_VERIFICATION-BASE_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := _903225a x0 x1

mutual
  def «kadaneCurrent(_,_)_VERIFICATION-BASE_Int_IntSeq_Int» (x0 : SortIntSeq) (x1 : SortInt) : Option SortInt := (_c7787dc x0 x1) <|> (_f9462e3 x0 x1)

  def _f9462e3 : SortIntSeq → SortInt → Option SortInt
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» I R, C => do
      let _Val0 <- «nextCurrent(_,_)_VERIFICATION-BASE_Int_Int_Int» I C
      let _Val1 <- «kadaneCurrent(_,_)_VERIFICATION-BASE_Int_IntSeq_Int» R _Val0
      return _Val1
    | _, _ => none
end

mutual
  def «kadaneSmallest(_,_,_)_VERIFICATION-BASE_Int_IntSeq_Int_Int» (x0 : SortIntSeq) (x1 : SortInt) (x2 : SortInt) : Option SortInt := (_72cfa46 x0 x1 x2) <|> (_fc02d79 x0 x1 x2)

  def _fc02d79 : SortIntSeq → SortInt → SortInt → Option SortInt
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» I R, C, B => do
      let _Val0 <- «nextCurrent(_,_)_VERIFICATION-BASE_Int_Int_Int» I C
      let _Val1 <- «nextCurrent(_,_)_VERIFICATION-BASE_Int_Int_Int» I C
      let _Val2 <- «chooseSmaller(_,_)_VERIFICATION-BASE_Int_Int_Int» _Val1 B
      let _Val3 <- «kadaneSmallest(_,_,_)_VERIFICATION-BASE_Int_IntSeq_Int_Int» R _Val0 _Val2
      return _Val3
    | _, _, _ => none
end

def _133ca99 : SortIntSeq → Option SortInt
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» H T => do
    let _Val0 <- «kadaneSmallest(_,_,_)_VERIFICATION-BASE_Int_IntSeq_Int_Int» T H H
    return _Val0
  | _ => none

def «minSubArraySumSpec(_)_VERIFICATION-BASE_Int_IntSeq» (x0 : SortIntSeq) : Option SortInt := _133ca99 x0