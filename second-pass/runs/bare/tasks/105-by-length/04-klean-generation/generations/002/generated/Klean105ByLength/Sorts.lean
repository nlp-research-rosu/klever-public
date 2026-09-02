import Klean105ByLength.Prelude

structure SortGeneratedCounterCell : Type where
  val : SortInt

inductive SortExpr : Type where
  | attributeExpression (x0 : SortExpr) (x1 : SortString) : SortExpr
  | binaryExpression (x0 : SortString) (x1 : SortExpr) (x2 : SortExpr) : SortExpr
  | callExpression (x0 : SortExpr) (x1 : SortExpr) : SortExpr
  | integerExpression (x0 : SortInt) : SortExpr
  | listExpression (x0 : SortExpr) : SortExpr
  | nameExpression (x0 : SortString) : SortExpr
  | stringExpression (x0 : SortString) : SortExpr

mutual
  inductive SortPyList : Type where
    | pyList (x0 : SortPyVals) : SortPyList

  inductive SortPyVals : Type where
    | consPyVals (x0 : SortValue) (x1 : SortPyVals) : SortPyVals
    | emptyPyVals : SortPyVals

  inductive SortValue : Type where
    | inj_SortInt (x : SortInt) : SortValue
    | inj_SortPyList (x : SortPyList) : SortValue
    | inj_SortString (x : SortString) : SortValue
end

inductive SortParams : Type where
  | parameters (x0 : SortString) : SortParams

structure SortInputCell : Type where
  val : SortPyList

inductive SortStmt : Type where
  | functionDefinition (x0 : SortString) (x1 : SortParams) (x2 : SortStmt) : SortStmt
  | returnStatement (x0 : SortExpr) : SortStmt

inductive SortProgram : Type where
  | moduleProgram (x0 : SortStmt) : SortProgram

structure SortProgramCell : Type where
  val : SortProgram

mutual
  structure SortGeneratedTopCell : Type where
    mpy : SortMpyCell
    generatedCounter : SortGeneratedCounterCell

  inductive SortK : Type where
    | dotk : SortK
    | kseq (x0 : SortKItem) (x1 : SortK) : SortK

  structure SortKCell : Type where
    val : SortK

  inductive SortKItem : Type where
    | inj_SortExpr (x : SortExpr) : SortKItem
    | inj_SortGeneratedCounterCell (x : SortGeneratedCounterCell) : SortKItem
    | inj_SortGeneratedTopCell (x : SortGeneratedTopCell) : SortKItem
    | inj_SortInputCell (x : SortInputCell) : SortKItem
    | inj_SortInt (x : SortInt) : SortKItem
    | inj_SortKCell (x : SortKCell) : SortKItem
    | inj_SortMpyCell (x : SortMpyCell) : SortKItem
    | inj_SortParams (x : SortParams) : SortKItem
    | inj_SortProgram (x : SortProgram) : SortKItem
    | inj_SortProgramCell (x : SortProgramCell) : SortKItem
    | inj_SortPyList (x : SortPyList) : SortKItem
    | inj_SortPyVals (x : SortPyVals) : SortKItem
    | inj_SortResultCell (x : SortResultCell) : SortKItem
    | inj_SortStmt (x : SortStmt) : SortKItem
    | inj_SortString (x : SortString) : SortKItem
    | inj_SortValue (x : SortValue) : SortKItem
    | initProgram (x0 : SortProgram) : SortKItem
    | noResult : SortKItem

  structure SortMpyCell : Type where
    k : SortKCell
    program : SortProgramCell
    input : SortInputCell
    result : SortResultCell

  structure SortResultCell : Type where
    val : SortKItem
end