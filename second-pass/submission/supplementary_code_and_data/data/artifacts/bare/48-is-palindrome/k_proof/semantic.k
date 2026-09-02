requires "domains.md"

module MPY-SYNTAX
  imports DOMAINS

  // The concrete grammar covers every constructor emitted for solution.mpy.
  syntax Program ::= "Module" "(" Stmt ")"

  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmt ")"
                | "Return" "(" Expr ")"

  syntax Params ::= "Params" "(" String ")"

  syntax Expr ::= "Name" "(" String ")"
                | "Int" "(" Int ")"
                | "Str" "(" String ")"
                | "UnaryOp" "(" String "," Expr ")"
                | "Subscript" "(" Expr "," Slice ")"
                | "Compare" "(" Expr "," CmpOp ")"
                | PyVal

  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"
  syntax Slice ::= "Slice" "(" Bound "," Bound "," Bound ")"
  syntax Bound ::= Expr | "NoBound"

  syntax PyVal ::= "PyString" "(" String ")"
                 | "PyInt" "(" Int ")"
                 | "PyBool" "(" Bool ")"
endmodule

module SEMANTIC
  imports MPY-SYNTAX
  imports MAP

  syntax Function ::= "#function" "(" String "," Stmt ")"

  syntax KItem ::= "#load" "(" Stmt ")"
                 | "#invoke" "(" String "," PyVal ")"
                 | "#return" | "#returnFrame" "(" Map ")"
                 | "#compareRight" "(" CmpOp ")"
                 | "#compareValues" "(" PyVal "," String ")"
                 | "#applySlice" "(" Slice ")"
                 | "#unaryMinus"

  configuration
    <py>
      <k> $PGM:Program ~> #invoke($FUNCTION:String, PyString($ARG:String)) </k>
      <functions> .Map </functions>
      <env> .Map </env>
    </py>

  // Loading and calling the one-function module emitted by the translator.
  rule <k> Module(FD) => #load(FD) ... </k>

  rule <k> #load(FuncDef(F, Params(P), BODY)) => .K ... </k>
       <functions> .Map => F |-> #function(P, BODY) </functions>

  rule <k> #invoke(F, V) => BODY ~> #returnFrame(OLD) ... </k>
       <functions> F |-> #function(P, BODY) </functions>
       <env> OLD => P |-> V </env>

  // Return is evaluated before its caller's environment is restored.
  rule <k> Return(E) => E ~> #return ... </k>
  rule <k> V:PyVal ~> #return ~> #returnFrame(OLD) => V ... </k>
       <env> _CURRENT => OLD </env>

  // Literal and variable evaluation.
  rule <k> Int(I) => PyInt(I) ... </k>
  rule <k> Str(S) => PyString(S) ... </k>
  rule <k> Name(X) => V ... </k>
       <env> X |-> V </env>

  rule <k> UnaryOp("-", E) => E ~> #unaryMinus ... </k>
  rule <k> PyInt(I) ~> #unaryMinus => PyInt(0 -Int I) ... </k>

  // Evaluation order for a single CPython Compare/CmpOp pair.
  rule <k> Compare(E, C) => E ~> #compareRight(C) ... </k>
  rule <k> LEFT:PyVal ~> #compareRight(CmpOp(OP, RIGHT))
        => RIGHT ~> #compareValues(LEFT, OP) ... </k>
  rule <k> PyString(RIGHT) ~> #compareValues(PyString(LEFT), "==")
        => PyBool(LEFT ==String RIGHT) ... </k>

  // Python's s[::-1] is the only slice form used by solution.mpy.
  rule <k> Subscript(E, SL) => E ~> #applySlice(SL) ... </k>
  rule <k> PyString(S) ~> #applySlice(
          Slice(NoBound, NoBound, UnaryOp("-", Int(1))))
        => PyString(reverseString(S)) ... </k>

  // Reverse by Unicode code point, matching Python str slicing rather than
  // reversing a UTF-8 byte representation.
  syntax String ::= reverseString(String) [function]
  syntax String ::= reverseStringN(String, Int) [function]

  rule reverseString(S) => reverseStringN(S, lengthString(S))
  rule reverseStringN(_S, 0) => ""
  rule reverseStringN(S, N)
    => substrString(S, N -Int 1, N) +String reverseStringN(S, N -Int 1)
    requires N >Int 0
endmodule
