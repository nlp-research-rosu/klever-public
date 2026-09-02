import Klean50DecodeShift.Inj

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _587b402 : SortChars → Option SortChars
  | SortChars.nil_VERIFICATION_Chars => some SortChars.nil_VERIFICATION_Chars
  | _ => none

def _2625694 : SortChars → Option SortBool
  | SortChars.nil_VERIFICATION_Chars => some true
  | _ => none

def _715c7bb : SortChars → Option SortChars
  | SortChars.nil_VERIFICATION_Chars => some SortChars.nil_VERIFICATION_Chars
  | _ => none

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def _f2aa9b0 : SortInt → Option SortInt
  | C => do
    let _Val0 <- «_-Int_» C 5
    let _Val1 <- «_-Int_» _Val0 97
    let _Val2 <- _modInt_ _Val1 26
    let _Val3 <- «_+Int_» _Val2 97
    return _Val3

def _bb1b8a6 : SortInt → Option SortInt
  | C => do
    let _Val0 <- «_+Int_» C 5
    let _Val1 <- «_-Int_» _Val0 97
    let _Val2 <- _modInt_ _Val1 26
    let _Val3 <- «_+Int_» _Val2 97
    return _Val3

def _910950c : SortInt → Option SortBool
  | C => do
    let _Val0 <- «_<=Int_» 97 C
    let _Val1 <- «_<=Int_» C 122
    let _Val2 <- _andBool_ _Val0 _Val1
    return _Val2

def «decodeCode(_)_VERIFICATION_Int_Int» (x0 : SortInt) : Option SortInt := _f2aa9b0 x0

def «encodeCode(_)_VERIFICATION_Int_Int» (x0 : SortInt) : Option SortInt := _bb1b8a6 x0

def «isLowerCode(_)_VERIFICATION_Bool_Int» (x0 : SortInt) : Option SortBool := _910950c x0

mutual
  def _2c44f7c : SortChars → Option SortChars
    | SortChars.«cons(_,_)_VERIFICATION_Chars_Int_Chars» C CS => do
      let _Val0 <- «decodeCode(_)_VERIFICATION_Int_Int» C
      let _Val1 <- «decodeSpec(_)_VERIFICATION_Chars_Chars» CS
      return (SortChars.«cons(_,_)_VERIFICATION_Chars_Int_Chars» _Val0 _Val1)
    | _ => none

  def «decodeSpec(_)_VERIFICATION_Chars_Chars» (x0 : SortChars) : Option SortChars := (_2c44f7c x0) <|> (_715c7bb x0)
end

mutual
  def _4f67bdb : SortChars → Option SortChars
    | SortChars.«cons(_,_)_VERIFICATION_Chars_Int_Chars» C CS => do
      let _Val0 <- «encodeCode(_)_VERIFICATION_Int_Int» C
      let _Val1 <- «encodeSpec(_)_VERIFICATION_Chars_Chars» CS
      return (SortChars.«cons(_,_)_VERIFICATION_Chars_Int_Chars» _Val0 _Val1)
    | _ => none

  def «encodeSpec(_)_VERIFICATION_Chars_Chars» (x0 : SortChars) : Option SortChars := (_4f67bdb x0) <|> (_587b402 x0)
end

mutual
  def _931489b : SortChars → Option SortBool
    | SortChars.«cons(_,_)_VERIFICATION_Chars_Int_Chars» C CS => do
      let _Val0 <- «isLowerCode(_)_VERIFICATION_Bool_Int» C
      let _Val1 <- «allLower(_)_VERIFICATION_Bool_Chars» CS
      let _Val2 <- _andBool_ _Val0 _Val1
      return _Val2
    | _ => none

  def «allLower(_)_VERIFICATION_Bool_Chars» (x0 : SortChars) : Option SortBool := (_2625694 x0) <|> (_931489b x0)
end