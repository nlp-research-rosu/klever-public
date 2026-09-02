import Klean156IntToMiniRoman.Inj

axiom «.Map» : Option SortMap

axiom «tupleAt(_,_)_MINI-PYTHON_String_Strings_Int» (x0 : SortStrings) (x1 : SortInt) : Option SortString

axiom «_+String__STRING-COMMON_String_String_String» (x0 : SortString) (x1 : SortString) : Option SortString

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

noncomputable def _90142fe : SortInt → Option SortString
  | N => do
    let _Val0 <- «_/Int_» N 1000
    let _Val1 <- «tupleAt(_,_)_MINI-PYTHON_String_Strings_Int» (SortStrings.«_,__MINI-PYTHON-SYNTAX_Strings_String_Strings» "" (SortStrings.«_,__MINI-PYTHON-SYNTAX_Strings_String_Strings» "m" SortStrings.«.List{"_,__MINI-PYTHON-SYNTAX_Strings_String_Strings"}_Strings»)) _Val0
    let _Val2 <- _modInt_ N 1000
    let _Val3 <- «_/Int_» _Val2 100
    let _Val4 <- «tupleAt(_,_)_MINI-PYTHON_String_Strings_Int» (SortStrings.«_,__MINI-PYTHON-SYNTAX_Strings_String_Strings» "" (SortStrings.«_,__MINI-PYTHON-SYNTAX_Strings_String_Strings» "c" (SortStrings.«_,__MINI-PYTHON-SYNTAX_Strings_String_Strings» "cc" (SortStrings.«_,__MINI-PYTHON-SYNTAX_Strings_String_Strings» "ccc" (SortStrings.«_,__MINI-PYTHON-SYNTAX_Strings_String_Strings» "cd" (SortStrings.«_,__MINI-PYTHON-SYNTAX_Strings_String_Strings» "d" (SortStrings.«_,__MINI-PYTHON-SYNTAX_Strings_String_Strings» "dc" (SortStrings.«_,__MINI-PYTHON-SYNTAX_Strings_String_Strings» "dcc" (SortStrings.«_,__MINI-PYTHON-SYNTAX_Strings_String_Strings» "dccc" (SortStrings.«_,__MINI-PYTHON-SYNTAX_Strings_String_Strings» "cm" SortStrings.«.List{"_,__MINI-PYTHON-SYNTAX_Strings_String_Strings"}_Strings»)))))))))) _Val3
    let _Val5 <- «_+String__STRING-COMMON_String_String_String» _Val1 _Val4
    let _Val6 <- _modInt_ N 100
    let _Val7 <- «_/Int_» _Val6 10
    let _Val8 <- «tupleAt(_,_)_MINI-PYTHON_String_Strings_Int» (SortStrings.«_,__MINI-PYTHON-SYNTAX_Strings_String_Strings» "" (SortStrings.«_,__MINI-PYTHON-SYNTAX_Strings_String_Strings» "x" (SortStrings.«_,__MINI-PYTHON-SYNTAX_Strings_String_Strings» "xx" (SortStrings.«_,__MINI-PYTHON-SYNTAX_Strings_String_Strings» "xxx" (SortStrings.«_,__MINI-PYTHON-SYNTAX_Strings_String_Strings» "xl" (SortStrings.«_,__MINI-PYTHON-SYNTAX_Strings_String_Strings» "l" (SortStrings.«_,__MINI-PYTHON-SYNTAX_Strings_String_Strings» "lx" (SortStrings.«_,__MINI-PYTHON-SYNTAX_Strings_String_Strings» "lxx" (SortStrings.«_,__MINI-PYTHON-SYNTAX_Strings_String_Strings» "lxxx" (SortStrings.«_,__MINI-PYTHON-SYNTAX_Strings_String_Strings» "xc" SortStrings.«.List{"_,__MINI-PYTHON-SYNTAX_Strings_String_Strings"}_Strings»)))))))))) _Val7
    let _Val9 <- «_+String__STRING-COMMON_String_String_String» _Val5 _Val8
    let _Val10 <- _modInt_ N 10
    let _Val11 <- «tupleAt(_,_)_MINI-PYTHON_String_Strings_Int» (SortStrings.«_,__MINI-PYTHON-SYNTAX_Strings_String_Strings» "" (SortStrings.«_,__MINI-PYTHON-SYNTAX_Strings_String_Strings» "i" (SortStrings.«_,__MINI-PYTHON-SYNTAX_Strings_String_Strings» "ii" (SortStrings.«_,__MINI-PYTHON-SYNTAX_Strings_String_Strings» "iii" (SortStrings.«_,__MINI-PYTHON-SYNTAX_Strings_String_Strings» "iv" (SortStrings.«_,__MINI-PYTHON-SYNTAX_Strings_String_Strings» "v" (SortStrings.«_,__MINI-PYTHON-SYNTAX_Strings_String_Strings» "vi" (SortStrings.«_,__MINI-PYTHON-SYNTAX_Strings_String_Strings» "vii" (SortStrings.«_,__MINI-PYTHON-SYNTAX_Strings_String_Strings» "viii" (SortStrings.«_,__MINI-PYTHON-SYNTAX_Strings_String_Strings» "ix" SortStrings.«.List{"_,__MINI-PYTHON-SYNTAX_Strings_String_Strings"}_Strings»)))))))))) _Val10
    let _Val12 <- «_+String__STRING-COMMON_String_String_String» _Val9 _Val11
    return _Val12

noncomputable def «miniRoman(_)_ROMAN-VERIFICATION_String_Int» (x0 : SortInt) : Option SortString := _90142fe x0