module MPY-SYNTAX
  imports INT-SYNTAX
  imports BOOL-SYNTAX
  imports STRING-SYNTAX

  syntax Pgm ::= "Module" "(" Stmts ")"

  syntax Stmts ::= List{Stmt, ""}
  syntax Exprs ::= List{Expr, ","}
  syntax CmpOps ::= List{CmpOp, ","}
  syntax Strings ::= List{String, ","}
  syntax Ints ::= List{Int, ","}

  syntax Params ::= "Params" "(" Strings ")"

  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "Return" "(" Expr ")"
                | "Assign" "(" Expr "," Expr ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"
                | "For" "(" Expr "," Expr "," Stmts ")"

  syntax Expr ::= "Name" "(" String ")"
                | "Int" "(" Int ")"
                | "ListExpr" "(" Exprs ")"
                | "BinOp" "(" String "," Expr "," Expr ")"
                | "UnaryOp" "(" String "," Expr ")"
                | "Compare" "(" Expr "," CmpOps ")"
                | "NoneVal"

  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"

  // Values deliberately use a different list constructor from the source AST.
  syntax Value ::= Int | Bool | "none" | "listVal" "(" Ints ")"
  syntax Input ::= "input" "(" Ints ")"
endmodule

module SEMANTIC
  imports MPY-SYNTAX
  imports INT
  imports BOOL
  imports STRING
  imports MAP

  syntax Function ::= ".Function" | "function" "(" String "," Stmts ")"
  syntax Result ::= "noResult" | "result" "(" Value ")"

  configuration
    <mpy>
      <k> boot($PGM:Pgm) </k>
      <input> $ARGS:Input </input>
      <function> .Function </function>
      <env> .Map </env>
      <result> noResult </result>
    </mpy>

  syntax KItem ::= "boot" "(" Pgm ")"
                 | "exec" "(" Stmts ")"
                 | "start"
                 | "eval" "(" Expr ")"
                 | "store" "(" String ")"
                 | "bind" "(" String "," Value ")"
                 | "branch" "(" Stmts "," Stmts ")"
                 | "binLeft" "(" String "," Expr ")"
                 | "binRight" "(" String "," Value ")"
                 | "cmpLeft" "(" CmpOps ")"
                 | "cmpRight" "(" String "," Value ")"
                 | "forStart" "(" String "," Stmts ")"
                 | "loop" "(" String "," Ints "," Stmts ")"
                 | "returnK"

  rule boot(Module(SS)) => exec(SS) ~> start

  rule exec(.Stmts) => .K
  rule exec(S:Stmt SS:Stmts) => S ~> exec(SS)

  rule <k> FuncDef("prod_signs", Params(P), BODY) => .K ...</k>
       <function> .Function => function(P, BODY) </function>

  rule <k> start => exec(BODY) ...</k>
       <input> input(IS) </input>
       <function> function(P, BODY) </function>
       <env> _ => P |-> listVal(IS) </env>

  rule Assign(Name(X), E) => eval(E) ~> store(X)
  rule <k> V:Value ~> store(X) => .K ...</k>
       <env>... X |-> (_ => V) ...</env>
  rule <k> V:Value ~> store(X) => .K ...</k>
       <env> RHO => RHO X |-> V </env>
    requires notBool (X in_keys(RHO))

  rule <k> bind(X, V) => .K ...</k>
       <env>... X |-> (_ => V) ...</env>
  rule <k> bind(X, V) => .K ...</k>
       <env> RHO => RHO X |-> V </env>
    requires notBool (X in_keys(RHO))

  rule If(E, THEN, ELSE) => eval(E) ~> branch(THEN, ELSE)
  rule true  ~> branch(THEN, _) => exec(THEN)
  rule false ~> branch(_, ELSE) => exec(ELSE)

  rule For(Name(X), E, BODY) => eval(E) ~> forStart(X, BODY)
  rule listVal(IS) ~> forStart(X, BODY) => loop(X, IS, BODY)
  rule loop(_, .Ints, _) => .K
  rule loop(X, I, IS, BODY) => bind(X, I) ~> exec(BODY) ~> loop(X, IS, BODY)

  rule Return(E) => eval(E) ~> returnK
  rule <k> V:Value ~> returnK ~> _REST => .K </k>
       <result> noResult => result(V) </result>

  rule eval(Int(I)) => I
  rule eval(NoneVal) => none
  rule eval(ListExpr(.Exprs)) => listVal(.Ints)
  rule <k> eval(Name(X)) => V ...</k>
       <env> ... X |-> V ...</env>

  rule eval(UnaryOp(OP, E)) => eval(E) ~> binRight(OP, 0)
  rule eval(BinOp(OP, E1, E2)) => eval(E1) ~> binLeft(OP, E2)
  rule V:Value ~> binLeft(OP, E2) => eval(E2) ~> binRight(OP, V)

  rule I2:Int ~> binRight("+", I1:Int) => I1 +Int I2
  rule I2:Int ~> binRight("-", I1:Int) => I1 -Int I2
  rule I2:Int ~> binRight("*", I1:Int) => I1 *Int I2
  rule I:Int  ~> binRight("-", 0)      => 0 -Int I

  rule eval(Compare(E, OPS)) => eval(E) ~> cmpLeft(OPS)
  rule V:Value ~> cmpLeft(CmpOp(OP, E), .CmpOps)
    => eval(E) ~> cmpRight(OP, V)

  rule I2:Int ~> cmpRight("<",  I1:Int) => I1 <Int I2
  rule I2:Int ~> cmpRight("==", I1:Int) => I1 ==Int I2
  rule listVal(.Ints) ~> cmpRight("==", listVal(.Ints)) => true
  rule listVal(.Ints) ~> cmpRight("==", listVal(_I, _IS)) => false
endmodule
