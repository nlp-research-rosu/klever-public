// A small, executable semantics for the exact Python subset used by solution.py.
// Numeric values are exact numerator/denominator pairs.  This gives an exact
// model of the arithmetic in this task (and avoids making the proof depend on
// a particular host floating-point printer).

module TINY-PYTHON-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX

  syntax PyVal ::= "PyNum" "(" Int "," Int ")"
  syntax KResult ::= PyVal

  syntax Exp ::= PyVal
               | "Int" "(" Int ")"
               | "Name" "(" String ")"
               | "BinOp" "(" String "," Exp "," Exp ")" [strict(2, 3)]

  syntax Params ::= "Params" "(" String "," String ")"
  syntax Stmt ::= "Return" "(" Exp ")" [strict]
                | "FuncDef" "(" String "," Params "," Stmt ")"
                | "Module" "(" Stmt ")"

  syntax Args ::= "Args" "(" Int "," Int ")"
  syntax Result ::= "noResult" | PyVal
endmodule

module TINY-PYTHON
  imports TINY-PYTHON-SYNTAX
  imports INT
  imports MAP

  configuration
    <triangle>
      <k> $PGM:Stmt </k>
      <args> $ARGS:Args </args>
      <env> .Map </env>
      <result> noResult </result>
    </triangle>

  // Loading this one-function module also invokes its entry point with the
  // two values supplied in <args>.  The body itself is interpreted normally.
  rule <k> Module(FuncDef(_F, Params(X, Y), BODY)) => BODY </k>
       <args> Args(A, H) </args>
       <env> .Map => (X |-> PyNum(A, 1)) (Y |-> PyNum(H, 1)) </env>

  rule <k> Int(I) => PyNum(I, 1) ... </k>
  rule <k> Name(X) => V ... </k>
       <env> ... X |-> V ... </env>

  rule <k> BinOp("*", PyNum(AN, AD), PyNum(BN, BD))
         => PyNum(AN *Int BN, AD *Int BD) ... </k>
  rule <k> BinOp("/", PyNum(AN, AD), PyNum(BN, BD))
         => PyNum(AN *Int BD, AD *Int BN) ... </k>
       requires BN =/=Int 0

  rule <k> Return(V:PyVal) => .K </k>
       <result> noResult => V </result>
endmodule
