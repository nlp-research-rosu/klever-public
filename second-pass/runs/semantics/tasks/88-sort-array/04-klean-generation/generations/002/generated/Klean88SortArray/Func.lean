import Klean88SortArray.Inj

def _6e2cc1e : SortIntSeq → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some true
  | _ => none

def _8dd04c0 : SortIntSeq → Option SortValSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
  | _ => none

axiom ListItem (x0 : SortKItem) : Option SortList

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

axiom «.List» : Option SortList

axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

axiom «.Map» : Option SortMap

mutual
  def _5355fed : SortIntSeq → Option SortValSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» I IS => do
      let _Val0 <- «intsVS(_)_VERIFICATION_ValSeq_IntSeq» IS
      return (SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» ((@inj SortInt SortVal) I) _Val0)
    | _ => none

  def «intsVS(_)_VERIFICATION_ValSeq_IntSeq» (x0 : SortIntSeq) : Option SortValSeq := (_5355fed x0) <|> (_8dd04c0 x0)
end

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

mutual
  def _60c5a68 : SortIntSeq → Option SortBool
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» I IS => do
      let _Val0 <- «_>=Int_» I 0
      let _Val1 <- «nonNegativeIS(_)_VERIFICATION_Bool_IntSeq» IS
      let _Val2 <- _andBool_ _Val0 _Val1
      return _Val2
    | _ => none

  def «nonNegativeIS(_)_VERIFICATION_Bool_IntSeq» (x0 : SortIntSeq) : Option SortBool := (_60c5a68 x0) <|> (_6e2cc1e x0)
end