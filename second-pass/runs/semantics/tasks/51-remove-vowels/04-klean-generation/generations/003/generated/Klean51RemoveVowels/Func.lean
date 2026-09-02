import Klean51RemoveVowels.Inj

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _982236f : SortIntSeq → SortIntSeq → Option SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», T => some T
  | _, _ => none

def _7174452 : SortBool → SortBool → Option SortBool
  | true, _Gen0 => some true
  | _, _ => none

def _991a329 : SortBool → SortBool → Option SortBool
  | false, B => some B
  | _, _ => none

def _df7826c : SortIntSeq → SortIntSeq → Option SortIntSeq
  | ACC, SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some ACC
  | _, _ => none

axiom «.List» : Option SortList

axiom «.Map» : Option SortMap

axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

axiom ListItem (x0 : SortKItem) : Option SortList

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

mutual
  def _6d95c8d : SortIntSeq → SortIntSeq → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» I S, T => do
      let _Val0 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» S T
      return (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» I _Val0)
    | _, _ => none

  def «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortIntSeq := (_6d95c8d x0 x1) <|> (_982236f x0 x1)
end

def _orBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_7174452 x0 x1) <|> (_991a329 x0 x1)

def _fdbc0d1 : SortInt → Option SortBool
  | C => do
    let _Val0 <- «_==Int_» C 65
    let _Val1 <- «_==Int_» C 69
    let _Val2 <- _orBool_ _Val0 _Val1
    let _Val3 <- «_==Int_» C 73
    let _Val4 <- _orBool_ _Val2 _Val3
    let _Val5 <- «_==Int_» C 79
    let _Val6 <- _orBool_ _Val4 _Val5
    let _Val7 <- «_==Int_» C 85
    let _Val8 <- _orBool_ _Val6 _Val7
    let _Val9 <- «_==Int_» C 97
    let _Val10 <- _orBool_ _Val8 _Val9
    let _Val11 <- «_==Int_» C 101
    let _Val12 <- _orBool_ _Val10 _Val11
    let _Val13 <- «_==Int_» C 105
    let _Val14 <- _orBool_ _Val12 _Val13
    let _Val15 <- «_==Int_» C 111
    let _Val16 <- _orBool_ _Val14 _Val15
    let _Val17 <- «_==Int_» C 117
    let _Val18 <- _orBool_ _Val16 _Val17
    return _Val18

def «isVowelCode(_)_VERIFICATION_Bool_Int» (x0 : SortInt) : Option SortBool := _fdbc0d1 x0

mutual
  def «removeVowelCodesAcc(_,_)_VERIFICATION_IntSeq_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortIntSeq := (_c8b63e6 x0 x1) <|> (_df7826c x0 x1) <|> (_e0881b0 x0 x1)

  def _c8b63e6 : SortIntSeq → SortIntSeq → Option SortIntSeq
    | ACC, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C REST => do
      let _Val0 <- «isVowelCode(_)_VERIFICATION_Bool_Int» C
      let _Val1 <- «removeVowelCodesAcc(_,_)_VERIFICATION_IntSeq_IntSeq_IntSeq» ACC REST
      guard _Val0
      return _Val1
    | _, _ => none

  def _e0881b0 : SortIntSeq → SortIntSeq → Option SortIntSeq
    | ACC, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C REST => do
      let _Val0 <- «isVowelCode(_)_VERIFICATION_Bool_Int» C
      let _Val1 <- notBool_ _Val0
      let _Val2 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» ACC (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
      let _Val3 <- «removeVowelCodesAcc(_,_)_VERIFICATION_IntSeq_IntSeq_IntSeq» _Val2 REST
      guard _Val1
      return _Val3
    | _, _ => none
end

def _78f9d87 : SortIntSeq → Option SortIntSeq
  | CODES => do
    let _Val0 <- «removeVowelCodesAcc(_,_)_VERIFICATION_IntSeq_IntSeq_IntSeq» SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» CODES
    return _Val0

def «removeVowelCodes(_)_VERIFICATION_IntSeq_IntSeq» (x0 : SortIntSeq) : Option SortIntSeq := _78f9d87 x0