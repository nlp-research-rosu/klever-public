import Klean41CarRaceCollision.Prelude

inductive SortParams : Type where
  | Params (x0 : SortString) : SortParams

inductive SortExpr : Type where
  | BinOp (x0 : SortString) (x1 : SortExpr) (x2 : SortExpr) : SortExpr
  | Int (x0 : SortInt) : SortExpr
  | Name (x0 : SortString) : SortExpr

structure SortResultCell : Type where
  val : SortInt

structure SortGeneratedCounterCell : Type where
  val : SortInt

inductive SortStmt : Type where
  | FuncDef (x0 : SortString) (x1 : SortParams) (x2 : SortStmt) : SortStmt
  | Return (x0 : SortExpr) : SortStmt

mutual
  structure SortEnvironmentCell : Type where
    val : SortMap

  structure SortFunctionsCell : Type where
    val : SortMap

  structure SortGeneratedTopCell : Type where
    state : SortStateCell
    generatedCounter : SortGeneratedCounterCell

  inductive SortK : Type where
    | dotk : SortK
    | kseq (x0 : SortKItem) (x1 : SortK) : SortK

  structure SortKCell : Type where
    val : SortK

  inductive SortKItem : Type where
    | inj_SortEnvironmentCell (x : SortEnvironmentCell) : SortKItem
    | inj_SortExpr (x : SortExpr) : SortKItem
    | inj_SortFunctionsCell (x : SortFunctionsCell) : SortKItem
    | inj_SortGeneratedCounterCell (x : SortGeneratedCounterCell) : SortKItem
    | inj_SortGeneratedTopCell (x : SortGeneratedTopCell) : SortKItem
    | inj_SortInt (x : SortInt) : SortKItem
    | inj_SortKCell (x : SortKCell) : SortKItem
    | inj_SortMap (x : SortMap) : SortKItem
    | inj_SortParams (x : SortParams) : SortKItem
    | inj_SortResultCell (x : SortResultCell) : SortKItem
    | inj_SortStateCell (x : SortStateCell) : SortKItem
    | inj_SortStmt (x : SortStmt) : SortKItem
    | inj_SortString (x : SortString) : SortKItem
    | definition (x0 : SortString) (x1 : SortStmt) : SortKItem
    | evaluate (x0 : SortExpr) : SortKItem
    | execute (x0 : SortStmt) : SortKItem
    | finishReturn : SortKItem
    | multiplyBy (x0 : SortInt) : SortKItem
    | multiplyRight (x0 : SortExpr) : SortKItem
    | run (x0 : SortString) (x1 : SortInt) : SortKItem

  structure SortMap : Type where
    coll : List (SortKItem × SortKItem)

  structure SortStateCell : Type where
    k : SortKCell
    functions : SortFunctionsCell
    environment : SortEnvironmentCell
    result : SortResultCell
end