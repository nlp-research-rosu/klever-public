import Klean26RemoveDuplicates.Inj

def _09cbcbb : SortValSeq → Option SortBool
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => some true
  | _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _ec93494 : SortVal → Option SortBool
  | SortVal.inj_SortInt _Gen0 => some true
  | _ => none

def _fbb3e9c : SortVal → Option SortBool
  | _Gen0 => some false

axiom «.List» : Option SortList

axiom «.Map» : Option SortMap

axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

axiom ListItem (x0 : SortKItem) : Option SortList

axiom «keepSinglesAcc(_,_,_)_REMOVE-DUPLICATES-VERIFICATION_ValSeq_ValSeq_ValSeq_ValSeq» (x0 : SortValSeq) (x1 : SortValSeq) (x2 : SortValSeq) : Option SortValSeq

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def «isIntV(_)_MPY-BUILTINS_Bool_Val» (x0 : SortVal) : Option SortBool := (_ec93494 x0) <|> (_fbb3e9c x0)

mutual
  def _0571d9e : SortValSeq → Option SortBool
    | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» V REST => do
      let _Val0 <- «isIntV(_)_MPY-BUILTINS_Bool_Val» V
      let _Val1 <- «allInts(_)_REMOVE-DUPLICATES-VERIFICATION_Bool_ValSeq» REST
      let _Val2 <- _andBool_ _Val0 _Val1
      return _Val2
    | _ => none

  def «allInts(_)_REMOVE-DUPLICATES-VERIFICATION_Bool_ValSeq» (x0 : SortValSeq) : Option SortBool := (_0571d9e x0) <|> (_09cbcbb x0)
end