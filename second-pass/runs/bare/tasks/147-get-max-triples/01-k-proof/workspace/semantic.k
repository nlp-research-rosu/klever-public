// A deliberately small semantics for the exact Python subset used by solution.py.
// The surface constructors are those emitted, without desugaring, by py2mpy.py.
module MPY-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX

  syntax Pgm
  syntax Params
  syntax Stmt
  syntax Expr
  syntax Value

  syntax Pgm ::= "Module" "(" Stmt ")"
  syntax Params ::= "Params" "(" String ")"
  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmt ")"
                | "Return" "(" Expr ")" [strict]
  syntax Value ::= "Int" "(" Int ")"
  syntax Expr ::= Value
                | "Name" "(" String ")"
                | "BinOp" "(" String "," Expr "," Expr ")" [seqstrict(2,3)]
endmodule

module MPY
  imports MPY-SYNTAX
  imports INT
  imports STRING
  imports MAP

  syntax KResult ::= Value

  syntax Result ::= "noResult" | "result" "(" Int ")"

  configuration
    <mpy>
      <k> $PGM:Pgm </k>
      <input> $N:Int </input>
      <env> .Map </env>
      <result> noResult </result>
    </mpy>

  // Loading the sole top-level definition also invokes it on the configured
  // integer input. This is the entry-point convention of this semantics.
  rule <k> Module(FuncDef(_FN, Params(X), BODY)) => BODY </k>
       <input> N </input>
       <env> .Map => X |-> N </env>

  rule <k> Name(X) => Int(I) ...</k>
       <env>... X |-> I ...</env>

  rule BinOp("+",  Int(I), Int(J)) => Int(I +Int J)
  rule BinOp("-",  Int(I), Int(J)) => Int(I -Int J)
  rule BinOp("*",  Int(I), Int(J)) => Int(I *Int J)
  rule BinOp("//", Int(I), Int(J)) => Int(I divInt J)
    requires J =/=Int 0

  rule <k> Return(Int(I)) => .K </k>
       <result> noResult => result(I) </result>
endmodule
