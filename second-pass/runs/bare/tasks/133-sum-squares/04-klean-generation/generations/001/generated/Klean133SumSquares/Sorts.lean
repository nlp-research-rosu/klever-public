import Klean133SumSquares.Prelude

inductive SortPosNat : Type where
  | next (x0 : SortPosNat) : SortPosNat
  | one : SortPosNat
  | ten : SortPosNat

structure SortGeneratedCounterCell : Type where
  val : SortInt

inductive SortNumValue : Type where
  | intVal (x0 : SortInt) : SortNumValue
  | ratVal (x0 : SortInt) (x1 : SortPosNat) : SortNumValue

inductive SortPyExpr : Type where
  | BinOp (x0 : SortString) (x1 : SortPyExpr) (x2 : SortPyExpr) : SortPyExpr
  | Call (x0 : SortPyExpr) (x1 : SortPyExpr) : SortPyExpr
  | IntExpr (x0 : SortInt) : SortPyExpr
  | Name (x0 : SortString) : SortPyExpr

inductive SortPList : Type where
  | cons (x0 : SortNumValue) (x1 : SortPList) : SortPList
  | nil : SortPList

mutual
  inductive SortPyStmt : Type where
    | Assign (x0 : SortPyExpr) (x1 : SortPyExpr) : SortPyStmt
    | AugAssign (x0 : SortPyExpr) (x1 : SortString) (x2 : SortPyExpr) : SortPyStmt
    | For (x0 : SortPyExpr) (x1 : SortPyExpr) (x2 : SortPyStmts) : SortPyStmt
    | FuncDef (x0 : SortString) (x1 : SortString) (x2 : SortPyStmts) : SortPyStmt
    | ImportFrom (x0 : SortString) (x1 : SortString) : SortPyStmt
    | Return (x0 : SortPyExpr) : SortPyStmt

  inductive SortPyStmts : Type where
    | «.List{"___MPY-SYNTAX_PyStmts_PyStmt_PyStmts"}_PyStmts» : SortPyStmts
    | «___MPY-SYNTAX_PyStmts_PyStmt_PyStmts» (x0 : SortPyStmt) (x1 : SortPyStmts) : SortPyStmts
end

inductive SortPValue : Type where
  | inj_SortNumValue (x : SortNumValue) : SortPValue
  | listVal (x0 : SortPList) : SortPValue

inductive SortEnv : Type where
  | binding (x0 : SortString) (x1 : SortPValue) (x2 : SortEnv) : SortEnv
  | emptyEnv : SortEnv

structure SortEnvCell : Type where
  val : SortEnv

mutual
  structure SortFunctionsCell : Type where
    val : SortMap

  structure SortGeneratedTopCell : Type where
    python : SortPythonCell
    generatedCounter : SortGeneratedCounterCell

  inductive SortK : Type where
    | dotk : SortK
    | kseq (x0 : SortKItem) (x1 : SortK) : SortK

  structure SortKCell : Type where
    val : SortK

  inductive SortKItem : Type where
    | inj_SortBool (x : SortBool) : SortKItem
    | inj_SortEnv (x : SortEnv) : SortKItem
    | inj_SortEnvCell (x : SortEnvCell) : SortKItem
    | inj_SortFunctionsCell (x : SortFunctionsCell) : SortKItem
    | inj_SortGeneratedCounterCell (x : SortGeneratedCounterCell) : SortKItem
    | inj_SortGeneratedTopCell (x : SortGeneratedTopCell) : SortKItem
    | inj_SortInt (x : SortInt) : SortKItem
    | inj_SortKCell (x : SortKCell) : SortKItem
    | inj_SortMap (x : SortMap) : SortKItem
    | inj_SortNumValue (x : SortNumValue) : SortKItem
    | inj_SortPList (x : SortPList) : SortKItem
    | inj_SortPValue (x : SortPValue) : SortKItem
    | inj_SortPosNat (x : SortPosNat) : SortKItem
    | inj_SortPyExpr (x : SortPyExpr) : SortKItem
    | inj_SortPyStmt (x : SortPyStmt) : SortKItem
    | inj_SortPyStmts (x : SortPyStmts) : SortKItem
    | inj_SortPythonCell (x : SortPythonCell) : SortKItem
    | inj_SortString (x : SortString) : SortKItem
    | «#kxExport0(_)_VERIFICATION-KLEAN-EXPORT_KItem_NumValue» (x0 : SortNumValue) : SortKItem
    | «#kxExport1(_)_VERIFICATION-KLEAN-EXPORT_KItem_PList» (x0 : SortPList) : SortKItem
    | «#kxExport2(_,_)_VERIFICATION-KLEAN-EXPORT_KItem_Int_PList» (x0 : SortInt) (x1 : SortPList) : SortKItem
    | bind (x0 : SortString) (x1 : SortPValue) : SortKItem
    | callEntry (x0 : SortPValue) : SortKItem
    | exec (x0 : SortPyStmts) : SortKItem
    | load (x0 : SortPyStmts) : SortKItem
    | loadStmt (x0 : SortPyStmt) : SortKItem
    | loop (x0 : SortString) (x1 : SortPValue) (x2 : SortPyStmts) : SortKItem

  structure SortMap : Type where
    coll : List (SortKItem × SortKItem)

  structure SortPythonCell : Type where
    k : SortKCell
    functions : SortFunctionsCell
    env : SortEnvCell
end