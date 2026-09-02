import Klean152Compare.Prelude

structure SortGeneratedCounterCell : Type where
  val : SortInt

mutual
  inductive SortBound : Type where
    | inj_SortExpr (x : SortExpr) : SortBound
    | NoBound : SortBound

  inductive SortCmpOp : Type where
    | CmpOp (x0 : SortString) (x1 : SortExpr) : SortCmpOp

  inductive SortCmpOps : Type where
    | «.List{"cmpOps"}» : SortCmpOps
    | cmpOps (x0 : SortCmpOp) (x1 : SortCmpOps) : SortCmpOps

  inductive SortExpr : Type where
    | BinOp (x0 : SortString) (x1 : SortExpr) (x2 : SortExpr) : SortExpr
    | Call (x0 : SortExpr) (x1 : SortExprs) : SortExpr
    | Compare (x0 : SortExpr) (x1 : SortCmpOps) : SortExpr
    | IntExpr (x0 : SortInt) : SortExpr
    | ListExpr (x0 : SortExprs) : SortExpr
    | Name (x0 : SortString) : SortExpr
    | Subscript (x0 : SortExpr) (x1 : SortIndex) : SortExpr
    | UnaryOp (x0 : SortString) (x1 : SortExpr) : SortExpr

  inductive SortExprs : Type where
    | «.List{"exprs"}» : SortExprs
    | exprs (x0 : SortExpr) (x1 : SortExprs) : SortExprs

  inductive SortIndex : Type where
    | inj_SortExpr (x : SortExpr) : SortIndex
    | Slice (x0 : SortBound) (x1 : SortBound) (x2 : SortBound) : SortIndex
end

inductive SortStrings : Type where
  | «.List{"strings"}» : SortStrings
  | strings (x0 : SortString) (x1 : SortStrings) : SortStrings

mutual
  inductive SortValue : Type where
    | VBool (x0 : SortBool) : SortValue
    | VInt (x0 : SortInt) : SortValue
    | VList (x0 : SortValues) : SortValue

  inductive SortValues : Type where
    | VCons (x0 : SortValue) (x1 : SortValues) : SortValues
    | VNil : SortValues
end

inductive SortParams : Type where
  | Params (x0 : SortStrings) : SortParams

inductive SortEnv : Type where
  | Bind (x0 : SortString) (x1 : SortValue) (x2 : SortEnv) : SortEnv
  | EmptyEnv : SortEnv

mutual
  inductive SortStmt : Type where
    | Assign (x0 : SortExpr) (x1 : SortExpr) : SortStmt
    | FuncDef (x0 : SortString) (x1 : SortParams) (x2 : SortStmts) : SortStmt
    | If (x0 : SortExpr) (x1 : SortStmts) (x2 : SortStmts) : SortStmt
    | Return (x0 : SortExpr) : SortStmt

  inductive SortStmts : Type where
    | «.List{"stmts"}» : SortStmts
    | stmts (x0 : SortStmt) (x1 : SortStmts) : SortStmts
end

inductive SortPgm : Type where
  | Module (x0 : SortStmts) : SortPgm

mutual
  structure SortGeneratedTopCell : Type where
    k : SortKCell
    generatedCounter : SortGeneratedCounterCell

  inductive SortK : Type where
    | dotk : SortK
    | kseq (x0 : SortKItem) (x1 : SortK) : SortK

  structure SortKCell : Type where
    val : SortK

  inductive SortKItem : Type where
    | inj_SortBool (x : SortBool) : SortKItem
    | inj_SortBound (x : SortBound) : SortKItem
    | inj_SortCmpOp (x : SortCmpOp) : SortKItem
    | inj_SortCmpOps (x : SortCmpOps) : SortKItem
    | inj_SortEnv (x : SortEnv) : SortKItem
    | inj_SortExpr (x : SortExpr) : SortKItem
    | inj_SortExprs (x : SortExprs) : SortKItem
    | inj_SortGeneratedCounterCell (x : SortGeneratedCounterCell) : SortKItem
    | inj_SortGeneratedTopCell (x : SortGeneratedTopCell) : SortKItem
    | inj_SortIndex (x : SortIndex) : SortKItem
    | inj_SortInt (x : SortInt) : SortKItem
    | inj_SortKCell (x : SortKCell) : SortKItem
    | inj_SortParams (x : SortParams) : SortKItem
    | inj_SortPgm (x : SortPgm) : SortKItem
    | inj_SortStmt (x : SortStmt) : SortKItem
    | inj_SortStmts (x : SortStmts) : SortKItem
    | inj_SortString (x : SortString) : SortKItem
    | inj_SortStrings (x : SortStrings) : SortKItem
    | inj_SortValue (x : SortValue) : SortKItem
    | inj_SortValues (x : SortValues) : SortKItem
    | «#kxExport0(_,_)_VERIFICATION-KLEAN-EXPORT_KItem_Values_Values» (x0 : SortValues) (x1 : SortValues) : SortKItem
    | assignK (x0 : SortString) (x1 : SortStmts) (x2 : SortEnv) (x3 : SortPgm) : SortKItem
    | binLeftK (x0 : SortString) (x1 : SortExpr) (x2 : SortEnv) (x3 : SortPgm) : SortKItem
    | binRightK (x0 : SortString) (x1 : SortValue) : SortKItem
    | callArgK (x0 : SortExpr) (x1 : SortEnv) (x2 : SortPgm) : SortKItem
    | callInvokeK (x0 : SortValue) (x1 : SortPgm) : SortKItem
    | compareLeftK (x0 : SortString) (x1 : SortExpr) (x2 : SortEnv) (x3 : SortPgm) : SortKItem
    | compareRightK (x0 : SortString) (x1 : SortValue) : SortKItem
    | continueK (x0 : SortStmts) (x1 : SortPgm) : SortKItem
    | evalExprsK (x0 : SortExprs) (x1 : SortEnv) (x2 : SortPgm) : SortKItem
    | evalK (x0 : SortExpr) (x1 : SortEnv) (x2 : SortPgm) : SortKItem
    | execK (x0 : SortStmts) (x1 : SortEnv) (x2 : SortPgm) : SortKItem
    | execute (x0 : SortPgm) (x1 : SortValue) (x2 : SortValue) : SortKItem
    | extractReturned : SortKItem
    | ifK (x0 : SortStmts) (x1 : SortStmts) (x2 : SortStmts) (x3 : SortEnv) (x4 : SortPgm) : SortKItem
    | invokeK (x0 : SortPgm) (x1 : SortValue) (x2 : SortValue) : SortKItem
    | listHeadK (x0 : SortExprs) (x1 : SortEnv) (x2 : SortPgm) : SortKItem
    | listTailK (x0 : SortValue) : SortKItem
    | makeReturned : SortKItem
    | subscriptK (x0 : SortIndex) : SortKItem
    | unaryK (x0 : SortString) : SortKItem
end