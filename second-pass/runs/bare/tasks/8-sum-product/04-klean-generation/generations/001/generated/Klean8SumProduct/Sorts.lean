import Klean8SumProduct.Prelude

inductive SortInts : Type where
  | consInts (x0 : SortInt) (x1 : SortInts) : SortInts
  | noInts : SortInts

structure SortGeneratedCounterCell : Type where
  val : SortInt

inductive SortExpr : Type where
  | Call (x0 : SortExpr) (x1 : SortExpr) : SortExpr
  | Name (x0 : SortString) : SortExpr
  | TupleExpr (x0 : SortExpr) (x1 : SortExpr) : SortExpr

inductive SortStrings : Type where
  | «.List{"Strings"}» : SortStrings
  | Strings (x0 : SortString) (x1 : SortStrings) : SortStrings

inductive SortParams : Type where
  | Params (x0 : SortString) : SortParams

inductive SortPyVal : Type where
  | PyInt (x0 : SortInt) : SortPyVal
  | PyList (x0 : SortInts) : SortPyVal
  | PyTuple (x0 : SortPyVal) (x1 : SortPyVal) : SortPyVal

mutual
  inductive SortStmt : Type where
    | FuncDef (x0 : SortString) (x1 : SortParams) (x2 : SortStmts) : SortStmt
    | ImportFrom (x0 : SortString) (x1 : SortStrings) : SortStmt
    | Return (x0 : SortExpr) : SortStmt

  inductive SortStmts : Type where
    | «.List{"Stmts"}» : SortStmts
    | Stmts (x0 : SortStmt) (x1 : SortStmts) : SortStmts
end

structure SortInputCell : Type where
  val : SortPyVal

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
    | inj_SortExpr (x : SortExpr) : SortKItem
    | inj_SortFunctionsCell (x : SortFunctionsCell) : SortKItem
    | inj_SortGeneratedCounterCell (x : SortGeneratedCounterCell) : SortKItem
    | inj_SortGeneratedTopCell (x : SortGeneratedTopCell) : SortKItem
    | inj_SortInputCell (x : SortInputCell) : SortKItem
    | inj_SortInt (x : SortInt) : SortKItem
    | inj_SortInts (x : SortInts) : SortKItem
    | inj_SortKCell (x : SortKCell) : SortKItem
    | inj_SortMap (x : SortMap) : SortKItem
    | inj_SortParams (x : SortParams) : SortKItem
    | inj_SortPyVal (x : SortPyVal) : SortKItem
    | inj_SortPythonCell (x : SortPythonCell) : SortKItem
    | inj_SortResultCell (x : SortResultCell) : SortKItem
    | inj_SortStmt (x : SortStmt) : SortKItem
    | inj_SortStmts (x : SortStmts) : SortKItem
    | inj_SortString (x : SortString) : SortKItem
    | inj_SortStrings (x : SortStrings) : SortKItem
    | «#kxExport0(_)_VERIFICATION-KLEAN-EXPORT_KItem_Ints» (x0 : SortInts) : SortKItem
    | execStmts (x0 : SortStmts) : SortKItem
    | invoke (x0 : SortString) (x1 : SortPyVal) : SortKItem

  structure SortMap : Type where
    coll : List (SortKItem × SortKItem)

  structure SortPythonCell : Type where
    k : SortKCell
    input : SortInputCell
    functions : SortFunctionsCell
    result : SortResultCell

  structure SortResultCell : Type where
    val : SortK
end