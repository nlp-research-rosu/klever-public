import Klean78HexKey.Inj

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

def _1ff8f4d {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, B1, _Gen0 => do
    guard C
    return B1

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _5a819d8 : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», _Gen0 => some true
  | _, _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _f69553d : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 _Gen1, SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some false
  | _, _ => none

def _e79b532 : SortIntSeq → Option SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some 0
  | _ => none

def _c61e7b1 : SortIntSeq → SortVal → Option SortVal
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», OLD => some OLD
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
  def _550853c : SortIntSeq → SortVal → Option SortVal
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C REST, _OLD => do
      let _Val0 <- «finalDigit(_,_)_HEX-KEY-VERIFICATION_Val_IntSeq_Val» REST ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)))
      return _Val0
    | _, _ => none

  def «finalDigit(_,_)_HEX-KEY-VERIFICATION_Val_IntSeq_Val» (x0 : SortIntSeq) (x1 : SortVal) : Option SortVal := (_550853c x0 x1) <|> (_c61e7b1 x0 x1)
end

def _2f3f58a {SortSort : Type} : SortBool → SortSort → SortSort → Option SortSort
  | C, _Gen0, B2 => do
    let _Val0 <- notBool_ C
    guard _Val0
    return B2

mutual
  def _3a4bf2f : SortIntSeq → SortIntSeq → Option SortBool
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» A As, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» B Bs => do
      let _Val0 <- «_==Int_» A B
      let _Val1 <- «strPrefix(_,_)_MPY-STR_Bool_IntSeq_IntSeq» As Bs
      let _Val2 <- _andBool_ _Val0 _Val1
      return _Val2
    | _, _ => none

  def «strPrefix(_,_)_MPY-STR_Bool_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortBool := (_3a4bf2f x0 x1) <|> (_5a819d8 x0 x1) <|> (_f69553d x0 x1)
end

def kite {SortSort : Type} (x0 : SortBool) (x1 : SortSort) (x2 : SortSort) : Option SortSort := (_1ff8f4d x0 x1 x2) <|> (_2f3f58a x0 x1 x2)

def _38142ad : SortIntSeq → SortIntSeq → Option SortBool
  | P, SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => do
    let _Val0 <- «strPrefix(_,_)_MPY-STR_Bool_IntSeq_IntSeq» P SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
    let _Val1 <- notBool_ _Val0
    guard _Val1
    return false
  | _, _ => none

def _56a27c9 : SortIntSeq → SortIntSeq → Option SortBool
  | P, X => do
    let _Val0 <- «strPrefix(_,_)_MPY-STR_Bool_IntSeq_IntSeq» P X
    guard _Val0
    return true

mutual
  def «strContains(_,_)_MPY-STR_Bool_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortBool := (_38142ad x0 x1) <|> (_56a27c9 x0 x1) <|> (_e133ba2 x0 x1)

  def _e133ba2 : SortIntSeq → SortIntSeq → Option SortBool
    | P, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C Xs => do
      let _Val0 <- «strPrefix(_,_)_MPY-STR_Bool_IntSeq_IntSeq» P (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C Xs)
      let _Val1 <- notBool_ _Val0
      let _Val2 <- «strContains(_,_)_MPY-STR_Bool_IntSeq_IntSeq» P Xs
      guard _Val1
      return _Val2
    | _, _ => none
end

def _47bbc9d : SortInt → Option SortBool
  | C => do
    let _Val0 <- «strContains(_,_)_MPY-STR_Bool_IntSeq_IntSeq» (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C SortIntSeq.«.IntSeq_MPY-CORE_IntSeq») (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 50 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 51 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 53 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 55 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 66 (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» 68 SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»))))))
    return _Val0

def «isPrimeHexCode(_)_HEX-KEY-VERIFICATION_Bool_Int» (x0 : SortInt) : Option SortBool := _47bbc9d x0

def _400f0a8 : SortInt → Option SortInt
  | C => do
    let _Val0 <- «isPrimeHexCode(_)_HEX-KEY-VERIFICATION_Bool_Int» C
    let _Val1 <- kite _Val0 1 0
    return _Val1

def «primeHexBit(_)_HEX-KEY-VERIFICATION_Int_Int» (x0 : SortInt) : Option SortInt := _400f0a8 x0

mutual
  def _50b4f17 : SortIntSeq → Option SortInt
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C REST => do
      let _Val0 <- «primeHexBit(_)_HEX-KEY-VERIFICATION_Int_Int» C
      let _Val1 <- «hexCount(_)_HEX-KEY-VERIFICATION_Int_IntSeq» REST
      let _Val2 <- «_+Int_» _Val0 _Val1
      return _Val2
    | _ => none

  def «hexCount(_)_HEX-KEY-VERIFICATION_Int_IntSeq» (x0 : SortIntSeq) : Option SortInt := (_50b4f17 x0) <|> (_e79b532 x0)
end