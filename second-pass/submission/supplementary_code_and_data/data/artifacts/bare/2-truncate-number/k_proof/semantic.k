requires "domains.md"

module SEMANTIC-SYNTAX
  imports INT
  imports STRING
  imports MAP

  // The source fragment needed by solution.mpy.  These productions parse the
  // constructors emitted by py2mpy.py; no meaning is hidden in the front end.
  syntax Program ::= "Module" "(" Stmt ")"                     [symbol(Module)]
  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmt ")" [symbol(FuncDef)]
                | "Return" "(" Expr ")"                         [symbol(Return)]
  syntax Params ::= "Params" "(" String ")"                    [symbol(Params)]
  syntax Expr ::= "Name" "(" String ")"                        [symbol(Name)]
                | "BinOp" "(" String "," Expr "," Expr ")"    [symbol(BinOp)]
                | "Call" "(" Expr "," Expr ")"                 [symbol(Call)]

  // num(I,F,S) denotes the exact rational I + F/S.  Positive finite binary
  // Python floats are included because they are exact dyadic rationals.
  syntax Value ::= "num" "(" Int "," Int "," Int ")"         [symbol(num)]
                 | "intValue" "(" Int ")"                     [symbol(intValue)]
  syntax Result ::= "noResult" | Value

  syntax KItem ::= "invoke" "(" String "," Value ")"          [symbol(invoke)]
                 | "eval" "(" Expr ")"                        [symbol(eval)]
                 | "subtractLeft" "(" Expr ")"                [symbol(subtractLeft)]
                 | "subtractRight" "(" Value ")"              [symbol(subtractRight)]
                 | "applyInt"                                  [symbol(applyInt)]
                 | "finishReturn"                              [symbol(finishReturn)]
endmodule

module SEMANTIC
  imports SEMANTIC-SYNTAX

  configuration
    <python>
      <k> $PGM:Program ~> invoke("truncate_number", num($IPART:Int, $FRAC:Int, $SCALE:Int)) </k>
      <env> .Map </env>
      <result> noResult </result>
    </python>

  // Function entry binds the sole parameter.  The equality of F on the two
  // pending terms also checks that the requested function is the defined one.
  rule <k> Module(FuncDef(F, Params(P), BODY)) ~> invoke(F, V) => BODY </k>
       <env> .Map => P |-> V </env>

  rule <k> Return(E) => eval(E) ~> finishReturn ... </k>

  rule <k> eval(Name(X)) => V ... </k>
       <env>... X |-> V ...</env>

  rule <k> eval(BinOp("-", LEFT, RIGHT))
        => eval(LEFT) ~> subtractLeft(RIGHT) ... </k>
  rule <k> V:Value ~> subtractLeft(RIGHT)
        => eval(RIGHT) ~> subtractRight(V) ... </k>
  rule <k> intValue(J) ~> subtractRight(num(I, F, S))
        => num(I -Int J, F, S) ... </k>

  rule <k> eval(Call(Name("int"), ARG)) => eval(ARG) ~> applyInt ... </k>
  // The task's precondition is positive, so Python int truncation extracts I.
  rule <k> num(I, _F, _S) ~> applyInt => intValue(I) ... </k>

  rule <k> V:Value ~> finishReturn => .K </k>
       <result> noResult => V </result>
endmodule
