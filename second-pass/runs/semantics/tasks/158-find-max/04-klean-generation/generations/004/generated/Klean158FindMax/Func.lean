import Klean158FindMax.Inj

def _0092bdb : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 _Gen1, SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some false
  | _, _ => none

def _11995f1 : SortIntSeq → Option SortInt
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some 0
  | _ => none

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

def _28cc140 : SortIntSeq → SortIntSeq → Option SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», ACC => some ACC
  | _, _ => none

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def _5e2c753 : SortIntSeq → SortInt → Option SortIntSeq
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», C => some (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»)
  | _, _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _7174452 : SortBool → SortBool → Option SortBool
  | true, _Gen0 => some true
  | _, _ => none

def _80a1ae7 : SortInt → SortIntSeq → Option SortBool
  | _Gen0, SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some false
  | _, _ => none

def _8ec3df3 : SortWordSeq → SortIntSeq → SortInt → Option SortBestState
  | SortWordSeq.«.WordSeq_VERIFICATION_WordSeq», BEST, SCORE => some (SortBestState.«bestState(_,_)_VERIFICATION_BestState_IntSeq_Int» BEST SCORE)
  | _, _, _ => none

def _991a329 : SortBool → SortBool → Option SortBool
  | false, B => some B
  | _, _ => none

def _c71764f : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => some false
  | _, _ => none

def _f3f7875 : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq», SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 _Gen1 => some true
  | _, _ => none

def _9cc9039 : SortBestState → Option SortInt
  | SortBestState.«bestState(_,_)_VERIFICATION_BestState_IntSeq_Int» _Gen0 SCORE => some SCORE

axiom «.List» : Option SortList

axiom «.Map» : Option SortMap

axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

axiom ListItem (x0 : SortKItem) : Option SortList

def _a08019f : SortBestState → Option SortIntSeq
  | SortBestState.«bestState(_,_)_VERIFICATION_BestState_IntSeq_Int» WORD _Gen0 => some WORD

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

mutual
  def «snocCode(_,_)_MPY-SET_IntSeq_IntSeq_Int» (x0 : SortIntSeq) (x1 : SortInt) : Option SortIntSeq := (_5e2c753 x0 x1) <|> (_cd5036e x0 x1)

  def _cd5036e : SortIntSeq → SortInt → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» H T, C => do
      let _Val0 <- «snocCode(_,_)_MPY-SET_IntSeq_IntSeq_Int» T C
      return (SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» H _Val0)
    | _, _ => none
end

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def _orBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_7174452 x0 x1) <|> (_991a329 x0 x1)

def _cc09b1d : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» A As, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» B Bs => do
    let _Val0 <- «_>Int_» A B
    guard _Val0
    return false
  | _, _ => none

def _c875e09 : SortIntSeq → SortIntSeq → Option SortBool
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» A As, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» B Bs => do
    let _Val0 <- «_<Int_» A B
    guard _Val0
    return true
  | _, _ => none

mutual
  def _9b4a103 : SortIntSeq → Option SortInt
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» _Gen0 S => do
      let _Val0 <- «isLen(_)_MPY-CORE_Int_IntSeq» S
      let _Val1 <- «_+Int_» 1 _Val0
      return _Val1
    | _ => none

  def «isLen(_)_MPY-CORE_Int_IntSeq» (x0 : SortIntSeq) : Option SortInt := (_11995f1 x0) <|> (_9b4a103 x0)
end

def «bestScore(_)_VERIFICATION_Int_BestState» (x0 : SortBestState) : Option SortInt := _9cc9039 x0

def «bestWord(_)_VERIFICATION_IntSeq_BestState» (x0 : SortBestState) : Option SortIntSeq := _a08019f x0

mutual
  def «codeIn(_,_)_MPY-SET_Bool_Int_IntSeq» (x0 : SortInt) (x1 : SortIntSeq) : Option SortBool := (_80a1ae7 x0 x1) <|> (_c27c6a9 x0 x1)

  def _c27c6a9 : SortInt → SortIntSeq → Option SortBool
    | C, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» H T => do
      let _Val0 <- «_==Int_» C H
      let _Val1 <- «codeIn(_,_)_MPY-SET_Bool_Int_IntSeq» C T
      let _Val2 <- _orBool_ _Val0 _Val1
      return _Val2
    | _, _ => none
end

mutual
  def _6a28f31 : SortIntSeq → SortIntSeq → Option SortBool
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» A As, SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» B Bs => do
      let _Val0 <- «_==Int_» A B
      let _Val1 <- «strLt(_,_)_MPY-STR_Bool_IntSeq_IntSeq» As Bs
      guard _Val0
      return _Val1
    | _, _ => none

  def «strLt(_,_)_MPY-STR_Bool_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortBool := (_0092bdb x0 x1) <|> (_6a28f31 x0 x1) <|> (_c71764f x0 x1) <|> (_c875e09 x0 x1) <|> (_cc09b1d x0 x1) <|> (_f3f7875 x0 x1)
end

mutual
  def _37448bb : SortIntSeq → SortIntSeq → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C S, ACC => do
      let _Val0 <- «codeIn(_,_)_MPY-SET_Bool_Int_IntSeq» C ACC
      let _Val1 <- notBool_ _Val0
      let _Val2 <- «snocCode(_,_)_MPY-SET_IntSeq_IntSeq_Int» ACC C
      let _Val3 <- «dedupFrom(_,_)_MPY-SET_IntSeq_IntSeq_IntSeq» S _Val2
      guard _Val1
      return _Val3
    | _, _ => none

  def _5d1e314 : SortIntSeq → SortIntSeq → Option SortIntSeq
    | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» C S, ACC => do
      let _Val0 <- «codeIn(_,_)_MPY-SET_Bool_Int_IntSeq» C ACC
      let _Val1 <- «dedupFrom(_,_)_MPY-SET_IntSeq_IntSeq_IntSeq» S ACC
      guard _Val0
      return _Val1
    | _, _ => none

  def «dedupFrom(_,_)_MPY-SET_IntSeq_IntSeq_IntSeq» (x0 : SortIntSeq) (x1 : SortIntSeq) : Option SortIntSeq := (_28cc140 x0 x1) <|> (_37448bb x0 x1) <|> (_5d1e314 x0 x1)
end

def _a8c9961 : SortIntSeq → Option SortIntSeq
  | CS => do
    let _Val0 <- «dedupFrom(_,_)_MPY-SET_IntSeq_IntSeq_IntSeq» CS SortIntSeq.«.IntSeq_MPY-CORE_IntSeq»
    return _Val0

def «dedupCodes(_)_MPY-SET_IntSeq_IntSeq» (x0 : SortIntSeq) : Option SortIntSeq := _a8c9961 x0

mutual
  def _1aa6ab5 : SortWordSeq → SortIntSeq → SortInt → Option SortBestState
    | SortWordSeq.«wCons(_,_)_VERIFICATION_WordSeq_IntSeq_WordSeq» WORD REST, _BEST, SCORE => do
      let _Val0 <- «dedupCodes(_)_MPY-SET_IntSeq_IntSeq» WORD
      let _Val1 <- «isLen(_)_MPY-CORE_Int_IntSeq» _Val0
      let _Val2 <- «_>Int_» _Val1 SCORE
      let _Val3 <- «dedupCodes(_)_MPY-SET_IntSeq_IntSeq» WORD
      let _Val4 <- «isLen(_)_MPY-CORE_Int_IntSeq» _Val3
      let _Val5 <- «findMaxWords(_,_,_)_VERIFICATION_BestState_WordSeq_IntSeq_Int» REST WORD _Val4
      guard _Val2
      return _Val5
    | _, _, _ => none

  def _2e392cb : SortWordSeq → SortIntSeq → SortInt → Option SortBestState
    | SortWordSeq.«wCons(_,_)_VERIFICATION_WordSeq_IntSeq_WordSeq» WORD REST, BEST, SCORE => do
      let _Val0 <- «dedupCodes(_)_MPY-SET_IntSeq_IntSeq» WORD
      let _Val1 <- «isLen(_)_MPY-CORE_Int_IntSeq» _Val0
      let _Val2 <- «_==Int_» _Val1 SCORE
      let _Val3 <- «strLt(_,_)_MPY-STR_Bool_IntSeq_IntSeq» WORD BEST
      let _Val4 <- _andBool_ _Val2 _Val3
      let _Val5 <- «findMaxWords(_,_,_)_VERIFICATION_BestState_WordSeq_IntSeq_Int» REST WORD SCORE
      guard _Val4
      return _Val5
    | _, _, _ => none

  def _4ddaaa7 : SortWordSeq → SortIntSeq → SortInt → Option SortBestState
    | SortWordSeq.«wCons(_,_)_VERIFICATION_WordSeq_IntSeq_WordSeq» WORD REST, BEST, SCORE => do
      let _Val0 <- «dedupCodes(_)_MPY-SET_IntSeq_IntSeq» WORD
      let _Val1 <- «isLen(_)_MPY-CORE_Int_IntSeq» _Val0
      let _Val2 <- «_<Int_» _Val1 SCORE
      let _Val3 <- «findMaxWords(_,_,_)_VERIFICATION_BestState_WordSeq_IntSeq_Int» REST BEST SCORE
      guard _Val2
      return _Val3
    | _, _, _ => none

  def «findMaxWords(_,_,_)_VERIFICATION_BestState_WordSeq_IntSeq_Int» (x0 : SortWordSeq) (x1 : SortIntSeq) (x2 : SortInt) : Option SortBestState := (_1aa6ab5 x0 x1 x2) <|> (_2e392cb x0 x1 x2) <|> (_4ddaaa7 x0 x1 x2) <|> (_8ec3df3 x0 x1 x2) <|> (_b9a9e25 x0 x1 x2)

  def _b9a9e25 : SortWordSeq → SortIntSeq → SortInt → Option SortBestState
    | SortWordSeq.«wCons(_,_)_VERIFICATION_WordSeq_IntSeq_WordSeq» WORD REST, BEST, SCORE => do
      let _Val0 <- «dedupCodes(_)_MPY-SET_IntSeq_IntSeq» WORD
      let _Val1 <- «isLen(_)_MPY-CORE_Int_IntSeq» _Val0
      let _Val2 <- «_==Int_» _Val1 SCORE
      let _Val3 <- «strLt(_,_)_MPY-STR_Bool_IntSeq_IntSeq» WORD BEST
      let _Val4 <- notBool_ _Val3
      let _Val5 <- _andBool_ _Val2 _Val4
      let _Val6 <- «findMaxWords(_,_,_)_VERIFICATION_BestState_WordSeq_IntSeq_Int» REST BEST SCORE
      guard _Val5
      return _Val6
    | _, _, _ => none
end