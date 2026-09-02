module MPY-SYNTAX
  imports INT-SYNTAX
  imports BOOL-SYNTAX
  imports STRING-SYNTAX

  // The source constructors emitted by py2mpy.py for this program.
  syntax Program ::= "Module" "(" Stmts ")"
  syntax Stmts  ::= List{Stmt, ""}
  syntax Stmt   ::= "FuncDef" "(" String "," Params "," Stmts ")"
                  | "Assign" "(" Expr "," Expr ")"
                  | "Return" "(" Expr ")"
  syntax Params ::= "Params" "(" String ")"
  syntax Expr   ::= "Name" "(" String ")"
                  | "Int" "(" Int ")"
                  | "NoneVal"
                  | "Call" "(" Expr "," Expr ")"
                  | "Compare" "(" Expr "," CmpOp ")"
                  | "Subscript" "(" Expr "," Expr ")"
                  | "IfExp" "(" Expr "," Expr "," Expr ")"
  syntax CmpOp  ::= "CmpOp" "(" String "," Expr ")"

  // A first-order integer-list representation, convenient for both krun
  // inputs and universally quantified proof variables.
  syntax IntList ::= "nil"
                   | "cons" "(" Int "," IntList ")"
endmodule

module SEMANTIC-BASE
  imports MPY-SYNTAX
  imports INT
  imports BOOL

  syntax PyVal ::= Int
                 | Bool
                 | "none"
                 | "pyList" "(" IntList ")"
                 | "pySet" "(" IntList ")"
                 | "invalidIndex" "(" Int ")"
                 | "iteVal" "(" Bool "," PyVal "," PyVal ")"
  syntax PyVal ::= "itemAt" "(" IntList "," Int ")" [function, total]

  syntax Outcome ::= "noResult" | PyVal

  syntax KItem ::= "exec" "(" Stmts ")"
                 | "execStmt" "(" Stmt ")"
                 | "eval" "(" Expr ")"
                 | "assignDistinct"
                 | "returnValue"
                 | "setCall"
                 | "sortedCall"
                 | "lenCall"
                 | "cmpLeft" "(" String "," Expr ")"
                 | "cmpRight" "(" String "," PyVal ")"
                 | "subscriptLeft" "(" Expr ")"
                 | "subscriptRight" "(" IntList ")"
                 | "ifCondition" "(" Expr "," Expr ")"
                 | "ifThen" "(" Bool "," Expr ")"
                 | "ifElse" "(" Bool "," PyVal ")"

  configuration
    <mpy>
      <k> $PGM:Program </k>
      <input> $INPUT:IntList </input>
      <distinct> none </distinct>
      <result> noResult </result>
    </mpy>

  // A Module is run by invoking its required next_smallest entry point on
  // the integer list in <input>.  The parameter name is checked here.
  rule <k> Module(FuncDef("next_smallest", Params("lst"), BODY))
            => exec(BODY) ... </k>

  rule <k> exec(.Stmts) => .K ... </k>
  rule <k> exec(S SS) => execStmt(S) ~> exec(SS) ... </k>

  rule <k> execStmt(Assign(Name("distinct"), E))
            => eval(E) ~> assignDistinct ... </k>
  rule <k> V:PyVal ~> assignDistinct => .K ... </k>
       <distinct> _ => V </distinct>

  rule <k> execStmt(Return(E)) => eval(E) ~> returnValue ... </k>
  rule <k> V:PyVal ~> returnValue => .K ... </k>
       <result> noResult => V </result>

  rule <k> eval(Name("lst")) => pyList(L) ... </k>
       <input> L </input>
  rule <k> eval(Name("distinct")) => V ... </k>
       <distinct> V </distinct>
  rule <k> eval(Int(I)) => I ... </k>
  rule <k> eval(NoneVal) => none ... </k>

  rule <k> eval(Call(Name("set"), ARG)) => eval(ARG) ~> setCall ... </k>
  rule <k> pyList(L) ~> setCall => pySet(L) ... </k>
  rule <k> eval(Call(Name("sorted"), ARG))
            => eval(ARG) ~> sortedCall ... </k>
  rule <k> pySet(L) ~> sortedCall => pyList(uniqueSort(L)) ... </k>
  rule <k> eval(Call(Name("len"), ARG)) => eval(ARG) ~> lenCall ... </k>
  rule <k> pyList(L) ~> lenCall => lenInt(L) ... </k>

  rule <k> eval(Compare(LEFT, CmpOp(OP, RIGHT)))
            => eval(LEFT) ~> cmpLeft(OP, RIGHT) ... </k>
  rule <k> V:PyVal ~> cmpLeft(OP, RIGHT)
            => eval(RIGHT) ~> cmpRight(OP, V) ... </k>
  rule <k> I2:Int ~> cmpRight(">", I1:Int) => I1 >Int I2 ... </k>

  rule <k> eval(Subscript(BASE, INDEX))
            => eval(BASE) ~> subscriptLeft(INDEX) ... </k>
  rule <k> pyList(L) ~> subscriptLeft(INDEX)
            => eval(INDEX) ~> subscriptRight(L) ... </k>
  rule <k> I:Int ~> subscriptRight(L) => itemAt(L, I) ... </k>

  // If-expressions evaluate all three pure subexpressions and retain a
  // symbolic conditional when the input list is symbolic.  Concrete runs
  // reduce iteVal immediately.
  rule <k> eval(IfExp(COND, THEN, ELSE))
            => eval(COND) ~> ifCondition(THEN, ELSE) ... </k>
  rule <k> B:Bool ~> ifCondition(THEN, ELSE)
            => eval(THEN) ~> ifThen(B, ELSE) ... </k>
  rule <k> V:PyVal ~> ifThen(B, ELSE)
            => eval(ELSE) ~> ifElse(B, V) ... </k>
  rule <k> W:PyVal ~> ifElse(B, V) => iteVal(B, V, W) ... </k>

  // sorted(set(xs)): insertion sort with equality elimination.
  syntax IntList ::= "uniqueSort" "(" IntList ")" [function, total]
                   | "insertUnique" "(" Int "," IntList ")" [function, total]
  rule uniqueSort(nil) => nil [concrete]
  rule uniqueSort(cons(I, IS)) => insertUnique(I, uniqueSort(IS)) [concrete]
  rule insertUnique(I, nil) => cons(I, nil) [concrete]
  rule insertUnique(I, cons(J, JS)) => cons(I, cons(J, JS))
    requires I <Int J [concrete]
  rule insertUnique(I, cons(J, JS)) => cons(J, JS)
    requires I ==Int J [concrete]
  rule insertUnique(I, cons(J, JS)) => cons(J, insertUnique(I, JS))
    requires I >Int J [concrete]

  syntax Int ::= "lenInt" "(" IntList ")" [function, total]
  rule lenInt(nil) => 0 [concrete]
  rule lenInt(cons(_, IS)) => 1 +Int lenInt(IS) [concrete]

  rule itemAt(cons(I, _), 0) => I [concrete]
  rule itemAt(cons(_, IS), N) => itemAt(IS, N -Int 1)
    requires N >Int 0 [concrete]
  rule itemAt(nil, N) => invalidIndex(N) [concrete]
endmodule

// These equations are needed for concrete LLVM execution.  Omitting them
// from the Haskell definition prevents an unknown Bool from being split into
// speculative true/false branches; the symbolic iteVal is itself the value.
module ITE-CONCRETE [concrete]
  imports SEMANTIC-BASE

  rule iteVal(true,  V, _) => V
  rule iteVal(false, _, W) => W
endmodule

module SEMANTIC
  imports SEMANTIC-BASE
  imports ITE-CONCRETE
endmodule
