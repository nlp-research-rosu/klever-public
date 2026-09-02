module MPY-SYNTAX
  imports BOOL
  imports INT
  imports STRING

  syntax Program ::= "Module" "(" Stmts ")"
  syntax Stmts ::= List{Stmt, ""}
  syntax Params ::= "Params" "(" Strings ")"
  syntax Strings ::= List{String, ","}

  syntax Stmt ::= "ImportFrom" "(" String "," Strings ")"
                | "FuncDef" "(" String "," Params "," Stmts ")"
                | "Assign" "(" Expr "," Expr ")"
                | "AugAssign" "(" Expr "," String "," Expr ")"
                | "For" "(" Expr "," Expr "," Stmts ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"
                | "Return" "(" Expr ")"

  syntax Expr ::= "Name" "(" String ")"
                | "Int" "(" Int ")"
                | "Bool" "(" Bool ")"
                | "Compare" "(" Expr "," CmpOps ")"
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"
  syntax CmpOps ::= List{CmpOp, ","}

  syntax IntList ::= ".IntList"
                   | "cons" "(" Int "," IntList ")"
  syntax PyVal ::= "IntV" "(" Int ")"
                 | "BoolV" "(" Bool ")"
                 | "ListV" "(" IntList ")"
  syntax Result ::= "NoResult" | PyVal
endmodule

module SEMANTIC
  imports MPY-SYNTAX

  configuration
    <mpy>
      <k> $PGM:Program </k>
      <input> $OPERATIONS:IntList </input>
      <balance> 0 </balance>
      <current> 0 </current>
      <result> NoResult </result>
    </mpy>

  syntax KItem ::= "execStmts" "(" Stmts ")"
                 | "setBalance"
                 | "branch" "(" Stmts "," Stmts ")"
                 | "loop" "(" Stmts ")"
                 | "doReturn"

  rule <k> Module(SS) => execStmts(SS) ... </k>

  rule <k> execStmts(.Stmts) => .K ... </k>
  rule <k> execStmts(S SS) => S ~> execStmts(SS) ... </k>

  // Imports and annotations have no run-time effect in this subset.
  rule <k> ImportFrom(_, _) => .K ... </k>

  // The module is run as a call to the required entry point.  Its sole
  // argument is supplied by the <input> cell.
  rule <k> FuncDef("below_zero", Params("operations"), BODY)
        => execStmts(BODY) ... </k>

  rule <k> Assign(Name("balance"), E) => E ~> setBalance ... </k>
  rule <k> IntV(I) ~> setBalance => .K ... </k>
       <balance> _ => I </balance>

  rule <k> AugAssign(Name("balance"), "+", Name("operation")) => .K ... </k>
       <balance> B => B +Int I </balance>
       <current> I </current>

  rule <k> For(Name("operation"), E, BODY) => E ~> loop(BODY) ... </k>
  rule <k> ListV(.IntList) ~> loop(_) => .K ... </k>
  rule <k> ListV(cons(I, IS)) ~> loop(BODY)
        => execStmts(BODY) ~> ListV(IS) ~> loop(BODY) ... </k>
       <current> _ => I </current>

  rule <k> If(E, THEN, ELSE) => E ~> branch(THEN, ELSE) ... </k>
  rule <k> BoolV(true) ~> branch(THEN, _) => execStmts(THEN) ... </k>
  rule <k> BoolV(false) ~> branch(_, ELSE) => execStmts(ELSE) ... </k>

  rule <k> Return(E) => E ~> doReturn ... </k>
  rule <k> V:PyVal ~> doReturn ~> _ => .K </k>
       <balance> _ => 0 </balance>
       <current> _ => 0 </current>
       <result> NoResult => V </result>

  rule <k> Int(I) => IntV(I) ... </k>
  rule <k> Bool(B) => BoolV(B) ... </k>
  rule <k> Name("operations") => ListV(IS) ... </k>
       <input> IS </input>
  rule <k> Name("operation") => IntV(I) ... </k>
       <current> I </current>
  rule <k> Name("balance") => IntV(B) ... </k>
       <balance> B </balance>

  // Comparisons remain chains in the transliterated syntax.  This task uses
  // the one-link integer case, whose meaning is Python integer comparison.
  rule <k> Compare(Name("balance"), CmpOp("<", Int(0)))
        => BoolV(B <Int 0) ... </k>
       <balance> B </balance>
endmodule
