// A small, executable semantics for the py2mpy constructors used by
// solution.py.  The Python front end is purely syntactic; all evaluation
// (including String iteration and early return) is defined here.

module MPY-SYNTAX
  imports INT-SYNTAX
  imports BOOL-SYNTAX
  imports STRING-SYNTAX

  syntax Pgm ::= "Module" "(" Stmts ")"
               | "Run" "(" Pgm "," String "," String ")"

  syntax Stmts ::= List{Stmt, ""}
  syntax Params ::= "Params" "(" String ")"

  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "Assign" "(" Expr "," Expr ")"
                | "For" "(" Expr "," Expr "," Stmts ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"
                | "Return" "(" Expr ")"

  syntax Expr ::= "Name" "(" String ")"
                | "Int" "(" Int ")"
                | "Bool" "(" Bool ")"
                | "Str" "(" String ")"
                | "BinOp" "(" String "," Expr "," Expr ")"
                | "Compare" "(" Expr "," CmpOp ")"

  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"
endmodule

module MPY-SEMANTIC
  imports MPY-SYNTAX
  imports INT
  imports BOOL
  imports STRING
  imports MAP

  syntax Value ::= "intVal" "(" Int ")"
                 | "boolVal" "(" Bool ")"
                 | "strVal" "(" String ")"
  syntax Expr ::= Value

  syntax Function ::= "function" "(" Params "," Stmts ")"

  syntax KItem ::= "invoke" "(" String "," Value ")"
                 | "assignTo" "(" String ")"
                 | "ifBranch" "(" Stmts "," Stmts ")"
                 | "binLeft" "(" String "," Expr ")"
                 | "binRight" "(" String "," Value ")"
                 | "compareLeft" "(" CmpOp ")"
                 | "compareRight" "(" String "," Value ")"
                 | "forStart" "(" String "," Stmts ")"
                 | "forLoop" "(" String "," String "," Stmts ")"
                 | "returnNow"

  configuration
    <mpy>
      <k> $PGM:Pgm </k>
      <functions> .Map </functions>
      <env> .Map </env>
    </mpy>

  // Module loading and invocation of the one-argument HumanEval entry point.
  rule Run(Module(SS), F, INPUT)
    => Module(SS) ~> invoke(F, strVal(INPUT))
  rule Module(SS) => SS
  rule <k> .Stmts => .K ... </k>
  rule <k> (S:Stmt SS:Stmts) => S ~> SS ... </k>

  rule <k> FuncDef(F, PS, BODY) => .K ... </k>
       <functions> FS => FS [ F <- function(PS, BODY) ] </functions>

  rule <k> invoke(F, V) => BODY ... </k>
       <functions> ... F |-> function(Params(P), BODY) ... </functions>
       <env> _ => P |-> V </env>

  // Literals, variables, arithmetic, and the two equality cases needed here.
  rule Int(I) => intVal(I)
  rule Bool(B) => boolVal(B)
  rule Str(S) => strVal(S)
  rule <k> Name(X) => V ... </k>
       <env> ... X |-> V ... </env>

  rule BinOp(OP, L, R) => L ~> binLeft(OP, R)
  rule V:Value ~> binLeft(OP, R) => R ~> binRight(OP, V)
  rule intVal(J) ~> binRight("+", intVal(I)) => intVal(I +Int J)
  rule intVal(J) ~> binRight("-", intVal(I)) => intVal(I -Int J)

  rule Compare(L, C) => L ~> compareLeft(C)
  rule V:Value ~> compareLeft(CmpOp(OP, R))
    => R ~> compareRight(OP, V)
  rule intVal(J) ~> compareRight("==", intVal(I))
    => boolVal(I ==Int J)
  rule strVal(T) ~> compareRight("==", strVal(S))
    => boolVal(S ==String T)

  // Statements and early function return.
  rule Assign(Name(X), E) => E ~> assignTo(X)
  rule <k> V:Value ~> assignTo(X) => .K ... </k>
       <env> ... X |-> _ => X |-> V ... </env>
  rule <k> V:Value ~> assignTo(X) => .K ... </k>
       <env> ENV => X |-> V ENV </env>
    requires notBool (X in_keys(ENV))

  rule If(E, THEN, ELSE) => E ~> ifBranch(THEN, ELSE)
  rule boolVal(true)  ~> ifBranch(THEN, _) => THEN
  rule boolVal(false) ~> ifBranch(_, ELSE) => ELSE

  rule Return(E) => E ~> returnNow
  rule <k> V:Value ~> returnNow ~> _REST => V </k>

  // Python String iteration.  The loop variable receives one-character
  // strings and the original iterable binding is left untouched.
  rule For(Name(X), E, BODY) => E ~> forStart(X, BODY)
  rule <k> strVal(S) ~> forStart(X, BODY) => forLoop(X, S, BODY) ... </k>
       <env> ... X |-> _ => X |-> strVal("") ... </env>
  rule <k> strVal(S) ~> forStart(X, BODY) => forLoop(X, S, BODY) ... </k>
       <env> ENV => X |-> strVal("") ENV </env>
    requires notBool (X in_keys(ENV))
  rule forLoop(_, "", _) => .K
  rule <k> forLoop(X, S, BODY)
        => BODY
        ~> forLoop(X, substrString(S, 1, lengthString(S)), BODY) ... </k>
       <env> ... X |-> _
        => X |-> strVal(substrString(S, 0, 1)) ... </env>
    requires S =/=String ""
  rule <k> forLoop(X, S, BODY)
        => BODY
        ~> forLoop(X, substrString(S, 1, lengthString(S)), BODY) ... </k>
       <env> ENV
        => X |-> strVal(substrString(S, 0, 1)) ENV </env>
    requires S =/=String ""
     andBool notBool (X in_keys(ENV))
endmodule

module MPY
  imports MPY-SEMANTIC
endmodule
