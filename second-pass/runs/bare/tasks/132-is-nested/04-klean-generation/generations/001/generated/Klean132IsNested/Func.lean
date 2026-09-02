import Klean132IsNested.Inj

def _476e6e0 : SortInt → SortBString → Option SortBool
  | 3, SortBString.«___MPY-SYNTAX_BString_Bracket_BString» SortBracket.«rbr_MPY-SYNTAX_Bracket» _Gen0 => some true
  | _, _ => none

def _429290f : SortInt → SortBString → Option SortBool
  | _Gen0, SortBString.«.BString_MPY-SYNTAX_BString» => some false
  | _, _ => none

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

axiom «.Map» : Option SortMap

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap

mutual
  def _2280b4a : SortInt → SortBString → Option SortBool
    | 3, SortBString.«___MPY-SYNTAX_BString_Bracket_BString» SortBracket.«lbr_MPY-SYNTAX_Bracket» BS => do
      let _Val0 <- «scan(_,_)_VERIFICATION_Bool_Int_BString» 3 BS
      return _Val0
    | _, _ => none

  def _4813405 : SortInt → SortBString → Option SortBool
    | 1, SortBString.«___MPY-SYNTAX_BString_Bracket_BString» SortBracket.«rbr_MPY-SYNTAX_Bracket» BS => do
      let _Val0 <- «scan(_,_)_VERIFICATION_Bool_Int_BString» 1 BS
      return _Val0
    | _, _ => none

  def _5ee52c5 : SortInt → SortBString → Option SortBool
    | 0, SortBString.«___MPY-SYNTAX_BString_Bracket_BString» SortBracket.«lbr_MPY-SYNTAX_Bracket» BS => do
      let _Val0 <- «scan(_,_)_VERIFICATION_Bool_Int_BString» 1 BS
      return _Val0
    | _, _ => none

  def _617f04c : SortInt → SortBString → Option SortBool
    | 2, SortBString.«___MPY-SYNTAX_BString_Bracket_BString» SortBracket.«lbr_MPY-SYNTAX_Bracket» BS => do
      let _Val0 <- «scan(_,_)_VERIFICATION_Bool_Int_BString» 2 BS
      return _Val0
    | _, _ => none

  def _68f3037 : SortInt → SortBString → Option SortBool
    | 1, SortBString.«___MPY-SYNTAX_BString_Bracket_BString» SortBracket.«lbr_MPY-SYNTAX_Bracket» BS => do
      let _Val0 <- «scan(_,_)_VERIFICATION_Bool_Int_BString» 2 BS
      return _Val0
    | _, _ => none

  def _83e6d58 : SortInt → SortBString → Option SortBool
    | 2, SortBString.«___MPY-SYNTAX_BString_Bracket_BString» SortBracket.«rbr_MPY-SYNTAX_Bracket» BS => do
      let _Val0 <- «scan(_,_)_VERIFICATION_Bool_Int_BString» 3 BS
      return _Val0
    | _, _ => none

  def «scan(_,_)_VERIFICATION_Bool_Int_BString» (x0 : SortInt) (x1 : SortBString) : Option SortBool := (_2280b4a x0 x1) <|> (_429290f x0 x1) <|> (_476e6e0 x0 x1) <|> (_4813405 x0 x1) <|> (_5ee52c5 x0 x1) <|> (_617f04c x0 x1) <|> (_68f3037 x0 x1) <|> (_83e6d58 x0 x1) <|> (_a212d13 x0 x1)

  def _a212d13 : SortInt → SortBString → Option SortBool
    | 0, SortBString.«___MPY-SYNTAX_BString_Bracket_BString» SortBracket.«rbr_MPY-SYNTAX_Bracket» BS => do
      let _Val0 <- «scan(_,_)_VERIFICATION_Bool_Int_BString» 0 BS
      return _Val0
    | _, _ => none
end