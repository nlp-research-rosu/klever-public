module MPY-SYNTAX
  imports STRING-SYNTAX

  syntax Program ::= "Module" "(" Stmt ")"
  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmt ")"
                | "Return" "(" Expr ")"
  syntax Params ::= "Params" "(" String ")"

  syntax Expr ::= "Name" "(" String ")"
                | "Str" "(" String ")"
                | "Attribute" "(" Expr "," String ")"
                | "Call" "(" Expr "," Expr "," Expr ")"
endmodule

module MPY
  imports MPY-SYNTAX
  imports STRING

  // A literal substring deletion primitive.  The concrete attribute keeps
  // K's replaceAll hook executable for krun while leaving symbolic strings
  // represented by deleteAll during proofs.
  syntax String ::= deleteAll(String, String) [function]
  rule deleteAll(S, NEEDLE) => replaceAll(S, NEEDLE, "")
    [concrete(S, NEEDLE), simplification]

  syntax Value ::= strVal(String)
  syntax Value ::= eval(Expr, String, String) [function]
  syntax Value ::= replaceValue(Value, String, String) [function]
  syntax Result ::= "noResult" | result(String)
  syntax KItem ::= "done"

  rule eval(Name(X), P, I) => strVal(I)
    requires X ==String P
  rule eval(Str(S), _, _) => strVal(S)
  rule eval(Call(Attribute(E, "replace"), Str(OLD), Str(NEW)), P, I)
    => replaceValue(eval(E, P, I), OLD, NEW)
  rule replaceValue(strVal(S), OLD, "") => strVal(deleteAll(S, OLD))

  configuration
    <mpy>
      <k> $PGM:K </k>
      <input> $INPUT:String </input>
      <result> noResult </result>
    </mpy>

  rule <k> Module(FuncDef(_, Params(P), Return(E)))
         => eval(E, P, I) ...</k>
       <input> I </input>

  rule <k> strVal(S) => done </k>
       <result> noResult => result(S) </result>
endmodule
