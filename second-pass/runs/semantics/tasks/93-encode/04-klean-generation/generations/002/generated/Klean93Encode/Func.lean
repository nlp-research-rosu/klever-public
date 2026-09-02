import Klean93Encode.Inj

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

def _3dabce1 : SortInt → Option SortInt
  | C => some C

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _5b8d770 : SortIntSeq → SortIntSeq → Option SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», ACC => some ACC
  | _, _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _7174452 : SortBool → SortBool → Option SortBool
  | true, _Gen0 => some true
  | _, _ => none

def _982236f : SortIntSeq → SortIntSeq → Option SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», T => some T
  | _, _ => none

def _991a329 : SortBool → SortBool → Option SortBool
  | false, B => some B
  | _, _ => none

axiom «.List» : Option SortList

axiom «.Map» : Option SortMap

axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

axiom ListItem (x0 : SortKItem) : Option SortList

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

mutual
  def _6d95c8d : SortIntSeq → SortIntSeq → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» I S, T => do
      let _Val0 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» S T
      return (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» I _Val0)
    | _, _ => none

  def «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortIntSeq := (_6d95c8d x0 x1) <|> (_982236f x0 x1)
end

def _orBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_7174452 x0 x1) <|> (_991a329 x0 x1)

def _1f3d8f0 : SortInt → Option SortBool
  | C => do
    let _Val0 <- «_>=Int_» C 97
    let _Val1 <- «_<=Int_» C 122
    let _Val2 <- _andBool_ _Val0 _Val1
    return _Val2

def _b6acdbd : SortInt → Option SortBool
  | C => do
    let _Val0 <- «_>=Int_» C 65
    let _Val1 <- «_<=Int_» C 90
    let _Val2 <- _andBool_ _Val0 _Val1
    return _Val2

def _64a720c : SortInt → Option SortBool
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

def «isLowerC(_)_MPY-METHODS_Bool_Int» (x0 : SortInt) : Option SortBool := _1f3d8f0 x0

def «isUpperC(_)_MPY-METHODS_Bool_Int» (x0 : SortInt) : Option SortBool := _b6acdbd x0

def «isVowelCode(_)_ENCODE-VERIFICATION_Bool_Int» (x0 : SortInt) : Option SortBool := _64a720c x0

def _756c9a9 : SortInt → Option SortInt
  | C => do
    let _Val0 <- «isLowerC(_)_MPY-METHODS_Bool_Int» C
    let _Val1 <- «_-Int_» C 32
    guard _Val0
    return _Val1

def _19d844e : SortInt → Option SortInt
  | C => do
    let _Val0 <- «isUpperC(_)_MPY-METHODS_Bool_Int» C
    let _Val1 <- «_+Int_» C 32
    guard _Val0
    return _Val1

def «swapC(_)_MPY-METHODS_Int_Int» (x0 : SortInt) : Option SortInt := (_19d844e x0) <|> (_756c9a9 x0) <|> (_3dabce1 x0)

def _799fc17 : SortInt → Option SortInt
  | C => do
    let _Val0 <- «swapC(_)_MPY-METHODS_Int_Int» C
    let _Val1 <- «isVowelCode(_)_ENCODE-VERIFICATION_Bool_Int» _Val0
    let _Val2 <- «swapC(_)_MPY-METHODS_Int_Int» C
    let _Val3 <- «_+Int_» _Val2 2
    guard _Val1
    return _Val3

def _983f424 : SortInt → Option SortInt
  | C => do
    let _Val0 <- «swapC(_)_MPY-METHODS_Int_Int» C
    let _Val1 <- «isVowelCode(_)_ENCODE-VERIFICATION_Bool_Int» _Val0
    let _Val2 <- notBool_ _Val1
    let _Val3 <- «swapC(_)_MPY-METHODS_Int_Int» C
    guard _Val2
    return _Val3

def «encodeCode(_)_ENCODE-VERIFICATION_Int_Int» (x0 : SortInt) : Option SortInt := (_799fc17 x0) <|> (_983f424 x0)

mutual
  def _75cb017 : SortIntSeq → SortIntSeq → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C REST, ACC => do
      let _Val0 <- «encodeCode(_)_ENCODE-VERIFICATION_Int_Int» C
      let _Val1 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» ACC (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Val0 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
      let _Val2 <- «encodeAcc(_,_)_ENCODE-VERIFICATION_IntSeq_IntSeq_IntSeq» REST _Val1
      return _Val2
    | _, _ => none

  def «encodeAcc(_,_)_ENCODE-VERIFICATION_IntSeq_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortIntSeq := (_5b8d770 x0 x1) <|> (_75cb017 x0 x1)
end

def _153912e : SortIntSeq → Option SortIntSeq
  | INPUT => do
    let _Val0 <- «encodeAcc(_,_)_ENCODE-VERIFICATION_IntSeq_IntSeq_IntSeq» INPUT SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
    return _Val0

def «encodeCodes(_)_ENCODE-VERIFICATION_IntSeq_IntSeq» (x0 : SortIntSeq) : Option SortIntSeq := _153912e x0