import Klean12Longest.Inj

axiom ListItem (x0 : SortKItem) : Option SortList

axiom «.Map» : Option SortMap

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

def _11995f1 : SortIntSeq → Option SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some 0
  | _ => none

def _3cdc03a : SortVal → SortStringSeq → Option SortVal
  | BEST, SortStringSeq.«.StringSeq_VERIFICATION_StringSeq» => some BEST
  | _, _ => none

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

axiom «.List» : Option SortList

axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList

mutual
  def _9b4a103 : SortIntSeq → Option SortInt
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 S => do
      let _Val0 <- «isLen(_)_MPY-CORE_Int_IntSeq» S
      let _Val1 <- «_+Int_» 1 _Val0
      return _Val1
    | _ => none

  def «isLen(_)_MPY-CORE_Int_IntSeq» (x0 : SortIntSeq) : Option SortInt := (_11995f1 x0) <|> (_9b4a103 x0)
end

mutual
  def _6a6c441 : SortVal → SortStringSeq → Option SortVal
    | SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» BEST), SortStringSeq.«sCons(_,_)_VERIFICATION_StringSeq_IntSeq_StringSeq» CS REST => do
      let _Val0 <- «isLen(_)_MPY-CORE_Int_IntSeq» CS
      let _Val1 <- «isLen(_)_MPY-CORE_Int_IntSeq» BEST
      let _Val2 <- «_>Int_» _Val0 _Val1
      let _Val3 <- «longestAcc(_,_)_VERIFICATION_Val_Val_StringSeq» ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» CS)) REST
      guard _Val2
      return _Val3
    | _, _ => none

  def _942fc51 : SortVal → SortStringSeq → Option SortVal
    | SortVal.inj_SortStr (SortStr.«str(_)_MPY-CORE_Str_IntSeq» BEST), SortStringSeq.«sCons(_,_)_VERIFICATION_StringSeq_IntSeq_StringSeq» CS REST => do
      let _Val0 <- «isLen(_)_MPY-CORE_Int_IntSeq» CS
      let _Val1 <- «isLen(_)_MPY-CORE_Int_IntSeq» BEST
      let _Val2 <- «_<=Int_» _Val0 _Val1
      let _Val3 <- «longestAcc(_,_)_VERIFICATION_Val_Val_StringSeq» ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» BEST)) REST
      guard _Val2
      return _Val3
    | _, _ => none

  def «longestAcc(_,_)_VERIFICATION_Val_Val_StringSeq» (x0 : SortVal) (x1 : SortStringSeq) : Option SortVal := (_3cdc03a x0 x1) <|> (_6a6c441 x0 x1) <|> (_942fc51 x0 x1) <|> (_a67df00 x0 x1)

  def _a67df00 : SortVal → SortStringSeq → Option SortVal
    | SortVal.«noneV_MPY-CORE_Val», SortStringSeq.«sCons(_,_)_VERIFICATION_StringSeq_IntSeq_StringSeq» CS REST => do
      let _Val0 <- «longestAcc(_,_)_VERIFICATION_Val_Val_StringSeq» ((@inj SortStr SortVal) (SortStr.«str(_)_MPY-CORE_Str_IntSeq» CS)) REST
      return _Val0
    | _, _ => none
end