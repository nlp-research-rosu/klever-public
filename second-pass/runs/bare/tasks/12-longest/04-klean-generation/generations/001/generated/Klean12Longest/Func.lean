import Klean12Longest.Inj

def _e4f8233 : SortString → SortStrings → Option SortString
  | BEST, SortStrings.«.List{"_,__MPY-SYNTAX_Strings_String_Strings"}_Strings» => some BEST
  | _, _ => none

axiom «lengthString(_)_STRING-COMMON_Int_String» (x0 : SortString) : Option SortInt

def _954c33a : SortStrings → Option SortValue
  | SortStrings.«.List{"_,__MPY-SYNTAX_Strings_String_Strings"}_Strings» => some SortValue.«noneVal_MPY-SEMANTICS_Value»
  | _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

axiom «stringAt(_,_)_VERIFICATION_String_String_Int» (x0 : SortString) (x1 : SortInt) : Option SortString

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

def _e744234 : SortStrings → Option SortValues
  | SortStrings.«.List{"_,__MPY-SYNTAX_Strings_String_Strings"}_Strings» => some SortValues.«.List{"_,__MPY-SEMANTICS_Values_Value_Values"}_Values»
  | _ => none

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

axiom «.Map» : Option SortMap

mutual
  noncomputable def «firstLongest(_,_)_VERIFICATION_String_String_Strings» (x0 : SortString) (x1 : SortStrings) : Option SortString := (_a40ac76 x0 x1) <|> (_ddee8e9 x0 x1) <|> (_e4f8233 x0 x1)

  noncomputable def _a40ac76 : SortString → SortStrings → Option SortString
    | BEST, SortStrings.«_,__MPY-SYNTAX_Strings_String_Strings» S SS => do
      let _Val0 <- «lengthString(_)_STRING-COMMON_Int_String» S
      let _Val1 <- «lengthString(_)_STRING-COMMON_Int_String» BEST
      let _Val2 <- «_<=Int_» _Val0 _Val1
      let _Val3 <- «firstLongest(_,_)_VERIFICATION_String_String_Strings» BEST SS
      guard _Val2
      return _Val3
    | _, _ => none

  noncomputable def _ddee8e9 : SortString → SortStrings → Option SortString
    | BEST, SortStrings.«_,__MPY-SYNTAX_Strings_String_Strings» S SS => do
      let _Val0 <- «lengthString(_)_STRING-COMMON_Int_String» S
      let _Val1 <- «lengthString(_)_STRING-COMMON_Int_String» BEST
      let _Val2 <- «_>Int_» _Val0 _Val1
      let _Val3 <- «firstLongest(_,_)_VERIFICATION_String_String_Strings» S SS
      guard _Val2
      return _Val3
    | _, _ => none
end

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def _3003411 : SortString → SortString → SortInt → SortInt → Option SortString
  | BEST, _ID, _I, N => do
    let _Val0 <- «_==Int_» N 0
    guard _Val0
    return BEST

mutual
  def _0a9f296 : SortStrings → Option SortValues
    | SortStrings.«_,__MPY-SYNTAX_Strings_String_Strings» S SS => do
      let _Val0 <- «stringValues(_)_VERIFICATION_Values_Strings» SS
      return (SortValues.«_,__MPY-SEMANTICS_Values_Value_Values» (SortValue.«strVal(_)_MPY-SEMANTICS_Value_String» S) _Val0)
    | _ => none

  def «stringValues(_)_VERIFICATION_Values_Strings» (x0 : SortStrings) : Option SortValues := (_0a9f296 x0) <|> (_e744234 x0)
end

noncomputable def _5bb79e3 : SortStrings → Option SortValue
  | SortStrings.«_,__MPY-SYNTAX_Strings_String_Strings» S SS => do
    let _Val0 <- «firstLongest(_,_)_VERIFICATION_String_String_Strings» S SS
    return (SortValue.«strVal(_)_MPY-SEMANTICS_Value_String» _Val0)
  | _ => none

axiom _7cce72c : SortString → SortString → SortInt → SortInt → Option SortString
axiom «firstInSeq(_,_,_,_)_VERIFICATION_String_String_String_Int_Int» (x0 : SortString) (x1 : SortString) (x2 : SortInt) (x3 : SortInt) : Option SortString
axiom _be8a39b : SortString → SortString → SortInt → SortInt → Option SortString

def _312168a : SortStrings → Option SortValue
  | SS => do
    let _Val0 <- «stringValues(_)_VERIFICATION_Values_Strings» SS
    return (SortValue.«listVal(_)_MPY-SEMANTICS_Value_Values» _Val0)

noncomputable def «expectedLongest(_)_VERIFICATION_Value_Strings» (x0 : SortStrings) : Option SortValue := (_5bb79e3 x0) <|> (_954c33a x0)

def «stringList(_)_VERIFICATION_Value_Strings» (x0 : SortStrings) : Option SortValue := _312168a x0