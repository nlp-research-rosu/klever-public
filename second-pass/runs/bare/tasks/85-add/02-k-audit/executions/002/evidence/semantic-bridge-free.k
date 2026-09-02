module MPY-SYNTAX
  imports INT-SYNTAX
  imports BOOL-SYNTAX
  imports STRING-SYNTAX

  syntax Module ::= "Module" "(" Stmts ")" [symbol]
  syntax Stmts ::= List{Stmt, ""}
  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")" [symbol]
                | "Return" "(" Expr ")"                         [symbol]
  syntax Params ::= "Params" "(" String ")" [symbol]

  syntax Expr ::= "Int" "(" Int ")"                                  [symbol]
                | "Name" "(" String ")"                              [symbol]
                | "BinOp" "(" String "," Expr "," Expr ")"        [symbol]
                | "Compare" "(" Expr "," CmpOp ")"                 [symbol]
                | "Subscript" "(" Expr "," Index ")"               [symbol]
                | "Call" "(" Expr "," Expr ")"                     [symbol]
                | "IfExp" "(" Expr "," Expr "," Expr ")"         [symbol]
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")" [symbol]
  syntax Index ::= Expr
                 | "Slice" "(" Bound "," Bound "," Bound ")" [symbol]
  syntax Bound ::= Expr | "NoBound" [symbol]

  // Runtime values use a deliberately small inductive integer sequence.  It
  // is enough for this task, concrete execution, and structural proof.
  syntax ISeq ::= "nil" [symbol]
                | "cons" "(" Int "," ISeq ")" [symbol]
  syntax PyVal ::= "pyInt" "(" Int ")"   [symbol]
                 | "pyBool" "(" Bool ")" [symbol]
                 | "pyList" "(" ISeq ")" [symbol]
endmodule

module MPY
  imports MPY-SYNTAX
  imports INT
  imports BOOL
  imports STRING
  imports MAP
  imports LIST

  syntax FuncInfo ::= "function" "(" String "," Expr ")" [symbol]

  syntax KItem ::= "start"
                 | "done"
                 | "eval" "(" Expr ")"
                 | "select" "(" Expr "," Expr ")"
                 | "binRight" "(" String "," Expr ")"
                 | "binApply" "(" String "," PyVal ")"
                 | "cmpRight" "(" String "," Expr ")"
                 | "cmpApply" "(" String "," PyVal ")"
                 | "isShortList"
                 | "keepIfEven"
                 | "indexAt" "(" Int ")"
                 | "sliceFrom" "(" Int ")"
                 | "builtInLen"
                 | "userCall" "(" String ")"
                 | "restoreCaller"

  configuration
    <mpy>
      <k> $PGM:Module ~> start </k>
      <input> $INPUT:PyVal </input>
      <functions> .Map </functions>
      <env> .Map </env>
      <callStack> .List </callStack>
    </mpy>

  // A module is loaded before its designated entry point is invoked.  The
  // accepted function body is a return expression, which is all solution.py
  // uses; expression evaluation below is otherwise compositional.
  rule <k> Module(FuncDef(F, Params(P), Return(E)) REST) => Module(REST) ... </k>
       <functions> FS => (F |-> function(P, E)) FS </functions>

  rule <k> Module(.Stmts) ~> start => INPUT ~> userCall("add") ~> done ... </k>
       <input> INPUT </input>

  rule <k> V:PyVal ~> done => V ... </k>

  rule <k> eval(Int(I)) => pyInt(I) ... </k>
  rule <k> eval(Name(X)) => V ... </k>
       <env>... X |-> V ...</env>

  rule <k> eval(IfExp(COND, THEN, ELSE))
        => eval(COND) ~> select(THEN, ELSE) ... </k>
  rule <k> pyBool(true)  ~> select(THEN, _) => eval(THEN) ... </k>
  rule <k> pyBool(false) ~> select(_, ELSE) => eval(ELSE) ... </k>

  rule <k> eval(BinOp(OP, LEFT, RIGHT))
        => eval(LEFT) ~> binRight(OP, RIGHT) ... </k>
  rule <k> LEFT:PyVal ~> binRight(OP, RIGHT)
        => eval(RIGHT) ~> binApply(OP, LEFT) ... </k>
  rule <k> pyInt(R) ~> binApply("+", pyInt(L)) => pyInt(L +Int R) ... </k>
  rule <k> pyInt(R) ~> binApply("%", pyInt(L)) => pyInt(L %Int R) ... </k>

  rule <k> eval(Compare(LEFT, CmpOp(OP, RIGHT)))
        => eval(LEFT) ~> cmpRight(OP, RIGHT) ... </k>
  rule <k> LEFT:PyVal ~> cmpRight(OP, RIGHT)
        => eval(RIGHT) ~> cmpApply(OP, LEFT) ... </k>
  rule <k> pyInt(R) ~> cmpApply("<",  pyInt(L)) => pyBool(L <Int R) ... </k>
  rule <k> pyInt(R) ~> cmpApply("==", pyInt(L)) => pyBool(L ==Int R) ... </k>

  rule <k> eval(Subscript(BASE, Int(I)))
        => eval(BASE) ~> indexAt(I) ... </k>
  rule <k> pyList(VALUES) ~> indexAt(I)
        => pyInt(at(VALUES, I)) ... </k>
  rule <k> eval(Subscript(BASE, Slice(Int(I), NoBound, NoBound)))
        => eval(BASE) ~> sliceFrom(I) ... </k>
  rule <k> pyList(VALUES) ~> sliceFrom(I)
        => pyList(drop(VALUES, I)) ... </k>

  rule <k> eval(Call(Name("len"), ARG))
        => eval(ARG) ~> builtInLen ... </k>
  rule <k> pyList(VALUES) ~> builtInLen
        => pyInt(size(VALUES)) ... </k>

  rule <k> eval(Call(Name(F), ARG))
        => eval(ARG) ~> userCall(F) ... </k>
    requires F =/=String "len"

  // The remainder of the K sequence is itself the expression continuation;
  // only the lexical environment therefore needs an explicit call stack.
  rule <k> ARG:PyVal ~> userCall(F)
        => eval(BODY) ~> restoreCaller ... </k>
       <functions>... F |-> function(P, BODY) ...</functions>
       <env> OLD => P |-> ARG </env>
       <callStack> STACK => ListItem(OLD) STACK </callStack>

  rule <k> RESULT:PyVal ~> restoreCaller => RESULT ... </k>
       <env> _ => OLD </env>
       <callStack> ListItem(OLD) STACK => STACK </callStack>

  syntax Int ::= size(ISeq) [function, total]
  rule size(nil) => 0
  rule size(cons(_, REST)) => 1 +Int size(REST)

  syntax Int ::= at(ISeq, Int) [function]
  rule at(cons(HEAD, _), 0) => HEAD
  rule at(cons(_, REST), I) => at(REST, I -Int 1)
    requires I >Int 0

  syntax ISeq ::= drop(ISeq, Int) [function]
  rule drop(VALUES, 0) => VALUES
  rule drop(cons(_, REST), I) => drop(REST, I -Int 1)
    requires I >Int 0

  syntax Int ::= evenPart(Int) [function]
  rule evenPart(I) => I
    requires I %Int 2 ==Int 0
    [concrete]
  rule evenPart(I) => 0
    requires I %Int 2 =/=Int 0
    [concrete]
endmodule
