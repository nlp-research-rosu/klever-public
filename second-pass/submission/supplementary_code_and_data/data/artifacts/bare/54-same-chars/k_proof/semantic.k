requires "domains.md"

module MPY-SYNTAX
  imports STRING-SYNTAX

  syntax Program ::= "Module" "(" Function ")"
  syntax Function ::= "FuncDef" "(" String "," Params "," Statement ")"
  syntax Params ::= "Params" "(" String "," String ")"

  syntax Statement ::= "Return" "(" Expr ")"

  syntax Expr ::= "Name" "(" String ")"
                | "Call" "(" Expr "," Expr ")"
                | "Compare" "(" Expr "," CmpOp ")"
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"
endmodule

module MPY
  imports MPY-SYNTAX
  imports BOOL
  imports INT
  imports K-EQUAL
  imports MAP
  imports SET
  imports STRING

  syntax Value ::= "stringValue" "(" String ")"
                 | "setValue" "(" Set ")"
                 | "boolValue" "(" Bool ")"
  syntax Result ::= "noResult" | "result" "(" Value ")"

  syntax Set ::= "charSet" "(" String ")" [function]
  rule charSet("") => .Set [concrete]
  rule charSet(S) => SetItem(substrString(S, 0, 1))
                     |Set charSet(substrString(S, 1, lengthString(S)))
    requires S =/=String ""
    [concrete]

  syntax KItem ::= "eval" "(" Expr ")"
                 | "makeSet"
                 | "compareRight" "(" Expr ")"
                 | "compareValues" "(" Value ")"
                 | "finishReturn"

  configuration
    <mpy>
      <k> $PGM:Program </k>
      <s0> $S0:String </s0>
      <s1> $S1:String </s1>
      <env> .Map </env>
      <result> noResult </result>
    </mpy>

  rule <k> Module(FuncDef(_F, Params(P0, P1), BODY)) => BODY ...</k>
       <s0> S0 </s0>
       <s1> S1 </s1>
       <env> .Map => (P0 |-> stringValue(S0)) (P1 |-> stringValue(S1)) </env>

  rule <k> Return(E) => eval(E) ~> finishReturn ...</k>

  rule <k> eval(Name(N)) => V ...</k>
       <env>... N |-> V ...</env>

  rule <k> eval(Call(Name("set"), E)) => eval(E) ~> makeSet ...</k>
  rule <k> stringValue(S) ~> makeSet => setValue(charSet(S)) ...</k>

  rule <k> eval(Compare(E0, CmpOp("==", E1)))
        => eval(E0) ~> compareRight(E1) ...</k>
  rule <k> V0:Value ~> compareRight(E1)
        => eval(E1) ~> compareValues(V0) ...</k>
  rule <k> setValue(CHARS1) ~> compareValues(setValue(CHARS0))
        => boolValue(CHARS0 ==K CHARS1) ...</k>

  rule <k> V:Value ~> finishReturn => .K </k>
       <result> noResult => result(V) </result>
endmodule
