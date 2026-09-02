import Klean11StringXor.Inj

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _991a329 : SortBool → SortBool → Option SortBool
  | false, B => some B
  | _, _ => none

def _19e8fe3 : SortIntSeq → SortIntSeq → SortIntSeq → Option SortIntSeq
  | P, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 _Gen1, SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some P
  | _, _, _ => none

def _8a04e77 : SortIntSeq → SortIntSeq → SortIntSeq → Option SortIntSeq
  | P, SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _Gen0 => some P
  | _, _, _ => none

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _982236f : SortIntSeq → SortIntSeq → Option SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», T => some T
  | _, _ => none

def _7174452 : SortBool → SortBool → Option SortBool
  | true, _Gen0 => some true
  | _, _ => none

def _c4615f8 : SortIntSeq → SortIntSeq → SortIntSeq → Option SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _Gen0, Y => some Y
  | _, _, _ => none

axiom «.Map» : Option SortMap

axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList

axiom ListItem (x0 : SortKItem) : Option SortList

def _ba5ceea : SortIntSeq → SortIntSeq → SortIntSeq → Option SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _Gen0, X => some X
  | _, _, _ => none

def _1b832df : SortIntSeq → SortIntSeq → SortIntSeq → Option SortIntSeq
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 _Gen1, SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», Y => some Y
  | _, _, _ => none

def _9f873aa : SortIntSeq → SortIntSeq → SortIntSeq → Option SortIntSeq
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 _Gen1, SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», X => some X
  | _, _, _ => none

def _455c55f : SortIntSeq → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some true
  | _ => none

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

axiom «.List» : Option SortList

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

mutual
  def _1083b96 : SortIntSeq → SortIntSeq → SortIntSeq → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 AS, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» B BS, _Gen1 => do
      let _Val0 <- «xorLastY(_,_,_)_STRING-XOR-VERIFICATION_IntSeq_IntSeq_IntSeq_IntSeq» AS BS (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» B SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
      return _Val0
    | _, _, _ => none

  def «xorLastY(_,_,_)_STRING-XOR-VERIFICATION_IntSeq_IntSeq_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) (x2 : SortIntSeq) : Option SortIntSeq := (_1083b96 x0 x1 x2) <|> (_1b832df x0 x1 x2) <|> (_c4615f8 x0 x1 x2)
end

mutual
  def _13c9b37 : SortIntSeq → SortIntSeq → SortIntSeq → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» A AS, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 BS, _Gen1 => do
      let _Val0 <- «xorLastX(_,_,_)_STRING-XOR-VERIFICATION_IntSeq_IntSeq_IntSeq_IntSeq» AS BS (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» A SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
      return _Val0
    | _, _, _ => none

  def «xorLastX(_,_,_)_STRING-XOR-VERIFICATION_IntSeq_IntSeq_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) (x2 : SortIntSeq) : Option SortIntSeq := (_13c9b37 x0 x1 x2) <|> (_9f873aa x0 x1 x2) <|> (_ba5ceea x0 x1 x2)
end

def _4de6e05 : SortInt → SortInt → Option SortBool
  | I1, I2 => do
    let _Val0 <- «_==Int_» I1 I2
    let _Val1 <- notBool_ _Val0
    return _Val1

def _d5c840c : SortInt → Option SortBool
  | C => do
    let _Val0 <- «_==Int_» C 48
    let _Val1 <- «_==Int_» C 49
    let _Val2 <- _orBool_ _Val0 _Val1
    return _Val2

def «_=/=Int_» (x0 : SortInt) (x1 : SortInt) : Option SortBool := _4de6e05 x0 x1

def «binaryCode(_)_STRING-XOR-VERIFICATION_Bool_Int» (x0 : SortInt) : Option SortBool := _d5c840c x0

def _ee95f57 : SortInt → SortInt → Option SortInt
  | A, B => do
    let _Val0 <- «binaryCode(_)_STRING-XOR-VERIFICATION_Bool_Int» A
    let _Val1 <- «binaryCode(_)_STRING-XOR-VERIFICATION_Bool_Int» B
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- «_==Int_» A B
    let _Val4 <- _andBool_ _Val2 _Val3
    guard _Val4
    return 48

mutual
  def _327bf20 : SortIntSeq → Option SortBool
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C REST => do
      let _Val0 <- «binaryCode(_)_STRING-XOR-VERIFICATION_Bool_Int» C
      let _Val1 <- «binaryCodes(_)_STRING-XOR-VERIFICATION_Bool_IntSeq» REST
      let _Val2 <- _andBool_ _Val0 _Val1
      return _Val2
    | _ => none

  def «binaryCodes(_)_STRING-XOR-VERIFICATION_Bool_IntSeq» (x0 : SortIntSeq) : Option SortBool := (_327bf20 x0) <|> (_455c55f x0)
end

def _e7d4dc2 : SortInt → SortInt → Option SortInt
  | A, B => do
    let _Val0 <- «binaryCode(_)_STRING-XOR-VERIFICATION_Bool_Int» A
    let _Val1 <- «binaryCode(_)_STRING-XOR-VERIFICATION_Bool_Int» B
    let _Val2 <- _andBool_ _Val0 _Val1
    let _Val3 <- «_=/=Int_» A B
    let _Val4 <- _andBool_ _Val2 _Val3
    guard _Val4
    return 49

def «xorCode(_,_)_STRING-XOR-VERIFICATION_Int_Int_Int» (x0 : SortInt) (x1 : SortInt) : Option SortInt := (_e7d4dc2 x0 x1) <|> (_ee95f57 x0 x1)

mutual
  def «xorAcc(_,_,_)_STRING-XOR-VERIFICATION_IntSeq_IntSeq_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) (x2 : SortIntSeq) : Option SortIntSeq := (_19e8fe3 x0 x1 x2) <|> (_8a04e77 x0 x1 x2) <|> (_d67a843 x0 x1 x2)

  def _d67a843 : SortIntSeq → SortIntSeq → SortIntSeq → Option SortIntSeq
    | P, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» A AS, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» B BS => do
      let _Val0 <- «xorCode(_,_)_STRING-XOR-VERIFICATION_Int_Int_Int» A B
      let _Val1 <- «seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» P (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Val0 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
      let _Val2 <- «xorAcc(_,_,_)_STRING-XOR-VERIFICATION_IntSeq_IntSeq_IntSeq_IntSeq» _Val1 AS BS
      return _Val2
    | _, _, _ => none
end