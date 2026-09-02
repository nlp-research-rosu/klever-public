requires "domains.md"

module MPY-SYNTAX
  imports INT-SYNTAX
  imports BOOL-SYNTAX
  imports STRING-SYNTAX

  // The task-specific fragment emitted by py2mpy.py.  These are AST nodes,
  // not Python surface syntax; all of their meaning is defined below.
  syntax Program ::= "Module" "(" Stmts ")" [symbol(Module)]
  syntax Stmts   ::= List{Stmt, ""}

  syntax Params ::= "Params" "(" String "," String ")" [symbol(Params)]

  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                  [symbol(FuncDef)]
                | "If" "(" Expr "," Stmts "," Stmts ")" [symbol(If)]
                | "Assign" "(" Expr "," Expr ")" [symbol(Assign)]
                | "Return" "(" Expr ")" [symbol(Return)]

  syntax Expr ::= "Int" "(" Int ")" [symbol(IntLiteral)]
                | "Name" "(" String ")" [symbol(Name)]
                | "UnaryOp" "(" String "," Expr ")" [symbol(UnaryOp)]
                | "BinOp" "(" String "," Expr "," Expr ")" [symbol(BinOp)]
                | "Compare" "(" Expr "," CmpOp ")" [symbol(Compare)]

  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")" [symbol(CmpOp)]
endmodule

module SEMANTIC
  imports MPY-SYNTAX
  imports INT
  imports BOOL
  imports MAP

  syntax Function ::= "function" "(" String "," String "," Stmts ")"
                      [symbol(function)]
  syntax Result ::= "noResult" [symbol(noResult)] | Int

  syntax KItem ::= "#invoke" "(" String "," Int "," Int ")"
                   [symbol(#invoke)]
                 | "#if" "(" Expr "," Stmts "," Stmts ")"
                   [symbol(#if), strict(1)]
                 | "#assign" "(" String "," Expr ")"
                   [symbol(#assign), strict(2)]
                 | "#return" "(" Expr ")" [symbol(#return), strict(1)]
                 | "#lessThan" "(" Expr "," Expr ")"
                   [symbol(#lessThan), strict]

  syntax KResult ::= Int | Bool
  syntax Expr ::= Int | Bool

  configuration
    <task>
      <k> $PGM:Program ~> #invoke("multiply", $A:Int, $B:Int) </k>
      <env> .Map </env>
      <functions> .Map </functions>
      <result> noResult </result>
    </task>

  // Statement-list scheduling.
  rule Module(SS) => SS
  rule <k> (S:Stmt SS:Stmts) => S ~> SS ... </k>
  rule .Stmts => .K

  // Loading a definition records its formal parameters and untranslated body.
  rule <k> FuncDef(F, Params(P1, P2), BODY) => .K ... </k>
       <functions> FUNS => FUNS [ F <- function(P1, P2, BODY) ] </functions>

  // The harness invokes the named, loaded function with two integer values.
  rule <k> #invoke(F, A, B) => BODY ... </k>
       <functions> ... F |-> function(P1, P2, BODY) ... </functions>
       <env> _ => (P1 |-> A) (P2 |-> B) </env>

  // Expressions.
  rule Int(I) => I
  rule <k> Name(X) => I ... </k>
       <env> ... X |-> I:Int ... </env>

  rule UnaryOp("-", E) => #unaryMinus(E)
  syntax KItem ::= "#unaryMinus" "(" Expr ")"
                   [symbol(#unaryMinus), strict(1)]
  rule #unaryMinus(I:Int) => 0 -Int I

  rule BinOp("%", E1, E2) => #modulo(E1, E2)
  rule BinOp("*", E1, E2) => #multiply(E1, E2)
  syntax KItem ::= "#modulo" "(" Expr "," Expr ")"
                   [symbol(#modulo), strict]
                 | "#multiply" "(" Expr "," Expr ")"
                   [symbol(#multiply), strict]
  rule #modulo(I1:Int, I2:Int) => I1 %Int I2
    requires I2 =/=Int 0
  rule #multiply(I1:Int, I2:Int) => I1 *Int I2

  rule Compare(E1, CmpOp("<", E2)) => #lessThan(E1, E2)
  rule #lessThan(I1:Int, I2:Int) => I1 <Int I2

  // Statements.  Empty branches are genuine empty statement lists.
  rule If(E, THEN, ELSE) => #if(E, THEN, ELSE)
  rule #if(true,  THEN, _) => THEN
  rule #if(false, _, ELSE) => ELSE

  rule Assign(Name(X), E) => #assign(X, E)
  rule <k> #assign(X, I:Int) => .K ... </k>
       <env> ENV => ENV [ X <- I ] </env>

  // This task has no caller frame: return terminates the entry invocation and
  // publishes its integer value in the result cell.
  rule <k> #return(I:Int) ~> _REST => .K </k>
       <result> _ => I </result>
  rule Return(E) => #return(E)
endmodule
