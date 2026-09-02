import Klean152Compare.Inj

def _a2aeb1f : SortValues → Option SortBool
  | SortValues.VCons _Gen0 _Gen1 => some false
  | _ => none

def _ab3408a : SortValues → Option SortValues
  | SortValues.VNil => some SortValues.VNil
  | _ => none

def _61fbef3 : SortBool → SortBool → Option SortBool
  | false, _Gen0 => some false
  | _, _ => none

def _54ec590 : SortValues → Option SortValues
  | SortValues.VCons _Gen0 VS => some VS
  | _ => none

def _1975853 : SortValue → Option SortInt
  | SortValue.VList _Gen0 => some 0
  | _ => none

def _9f73d9a : SortValue → Option SortInt
  | SortValue.VInt I => some I
  | _ => none

def _0177a0b : SortValues → Option SortBool
  | SortValues.VNil => some true
  | _ => none

def _cdf8b86 : SortValue → Option SortInt
  | SortValue.VBool _Gen0 => some 0
  | _ => none

def _17ebc68 : SortBool → Option SortBool
  | false => some true
  | _ => none

def _283a4a1 : SortValues → Option SortValue
  | SortValues.VNil => some (SortValue.VInt 0)
  | _ => none

def _de926b7 : SortValues → Option SortValue
  | SortValues.VCons V _Gen0 => some V
  | _ => none

def _53fc758 : SortBool → Option SortBool
  | true => some false
  | _ => none

def _5b9db8d : SortBool → SortBool → Option SortBool
  | true, B => some B
  | _, _ => none

def tailValues (x0 : SortValues) : Option SortValues := (_54ec590 x0) <|> (_ab3408a x0)

def isEmptyValues (x0 : SortValues) : Option SortBool := (_0177a0b x0) <|> (_a2aeb1f x0)

def valueAsInt (x0 : SortValue) : Option SortInt := (_1975853 x0) <|> (_9f73d9a x0) <|> (_cdf8b86 x0)

def headValue (x0 : SortValues) : Option SortValue := (_283a4a1 x0) <|> (_de926b7 x0)

def notBool_ (x0 : SortBool) : Option SortBool := (_17ebc68 x0) <|> (_53fc758 x0)

def _andBool_ (x0 : SortBool) (x1 : SortBool) : Option SortBool := (_5b9db8d x0 x1) <|> (_61fbef3 x0 x1)

def _5d22630 : SortValues → SortValues → Option SortValues
  | GS, _Gen0 => do
    let _Val0 <- isEmptyValues GS
    guard _Val0
    return SortValues.VNil

axiom _1b79171 : SortValues → SortValues → Option SortValues
axiom expected (x0 : SortValues) (x1 : SortValues) : Option SortValues
axiom _a6327c9 : SortValues → SortValues → Option SortValues