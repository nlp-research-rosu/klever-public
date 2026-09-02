import Klean28Concatenate.Inj

def _621d42f : SortString → SortStrList → Option SortString
  | ACC, SortStrList.«.StrList_MPY-SYNTAX_StrList» => some ACC
  | _, _ => none

axiom «_+String__STRING-COMMON_String_String_String» (x0 : SortString) (x1 : SortString) : Option SortString

mutual
  noncomputable def «concatAcc(_,_)_VERIFICATION_String_String_StrList» (x0 : SortString) (x1 : SortStrList) : Option SortString := (_621d42f x0 x1) <|> (_d4bf759 x0 x1)

  noncomputable def _d4bf759 : SortString → SortStrList → Option SortString
    | ACC, SortStrList.«_::__MPY-SYNTAX_StrList_String_StrList» S REST => do
      let _Val0 <- «_+String__STRING-COMMON_String_String_String» ACC S
      let _Val1 <- «concatAcc(_,_)_VERIFICATION_String_String_StrList» _Val0 REST
      return _Val1
    | _, _ => none
end