module MPY-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX

  syntax Program ::= "Module" "(" Stmts ")"

  syntax Stmts ::= List{Stmt, ""}
  syntax Stmt ::= "ImportFrom" "(" String "," String ")"
                | "FuncDef" "(" String "," Params "," Stmts ")"
                | "Assign" "(" Expr "," Expr ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"
                | "Return" "(" Expr ")"

  syntax Params ::= "Params" "(" String ")"

  syntax Expr ::= "Name" "(" String ")"
                | "Int" "(" Int ")"
                | "Str" "(" String ")"
                | "Call" "(" Expr "," Expr ")"
                | "BinOp" "(" String "," Expr "," Expr ")"
                | "Compare" "(" Expr "," CmpOp ")"

  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"
endmodule

module MPY
  imports MPY-SYNTAX
  imports INT
  imports STRING
  imports BOOL
  imports MAP

  // Concrete Python values used by this task, plus rationalString(N,D), the
  // symbolic representation of a numeric input string whose exact value is
  // N/D.  The latter lets verification quantify over all exact decimal
  // values without asking an SMT solver to reason about string parsing.
  syntax Value ::= "pyInt" "(" Int ")"
                 | "pyStr" "(" String ")"
                 | "pyBool" "(" Bool ")"
                 | "exactNum" "(" Int "," Int ")"
                 | "rationalString" "(" Int "," Int ")"

  syntax Result ::= "noResult" | Value

  syntax KItem ::= "exec" "(" Stmts ")"
                 | "assignTo" "(" String ")"
                 | "toDecimal"
                 | "toInt"
                 | "ifControl" "(" Stmts "," Stmts ")"
                 | "binLeft" "(" String "," Expr ")"
                 | "binRight" "(" String "," Value ")"
                 | "compareLeft" "(" String "," Expr ")"
                 | "compareRight" "(" String "," Value ")"
                 | "returnControl"

  configuration
    <mpy>
      <k> $PGM:Program </k>
      <arg> $ARG:Value </arg>
      <env> .Map </env>
      <result> noResult </result>
    </mpy>

  // Load the single imported definition and invoke the requested entry point.
  rule <k> Module(ImportFrom("decimal", "Decimal")
                   FuncDef("closest_integer", Params(P), BODY))
        => exec(BODY) ... </k>
       <arg> V </arg>
       <env> .Map => P |-> V </env>

  // Statement sequencing and assignment.
  rule <k> exec(.Stmts) => .K ... </k>
  rule <k> exec(S SS) => S ~> exec(SS) ... </k>
  rule <k> Assign(Name(X), E) => E ~> assignTo(X) ... </k>
  rule <k> V:Value ~> assignTo(X) => .K ... </k>
       <env> ENV => ENV [ X <- V ] </env>

  // Literals and variable lookup.
  rule <k> Int(I) => pyInt(I) ... </k>
  rule <k> Str(S) => pyStr(S) ... </k>
  rule <k> Name(X) => V ... </k>
       <env> ... X |-> V ... </env>

  // The two builtins used by solution.py.
  rule <k> Call(Name("Decimal"), E) => E ~> toDecimal ... </k>
  rule <k> pyStr(S) ~> toDecimal => parseDecimal(S) ... </k>
  rule <k> rationalString(N, D) ~> toDecimal => exactNum(N, D) ... </k>
  rule <k> Call(Name("int"), E) => E ~> toInt ... </k>
  rule <k> pyInt(I) ~> toInt => pyInt(I) ... </k>
  rule <k> exactNum(N, D) ~> toInt => pyInt(N /Int D) ... </k>
    requires D >Int 0

  // Left-to-right expression evaluation.
  rule <k> BinOp(OP, E1, E2) => E1 ~> binLeft(OP, E2) ... </k>
  rule <k> V1:Value ~> binLeft(OP, E2) => E2 ~> binRight(OP, V1) ... </k>
  rule <k> exactNum(N2, D2) ~> binRight("+", exactNum(N1, D1))
        => exactNum((N1 *Int D2) +Int (N2 *Int D1), D1 *Int D2) ... </k>
    requires D1 >Int 0 andBool D2 >Int 0
  rule <k> exactNum(N2, D2) ~> binRight("-", exactNum(N1, D1))
        => exactNum((N1 *Int D2) -Int (N2 *Int D1), D1 *Int D2) ... </k>
    requires D1 >Int 0 andBool D2 >Int 0

  rule <k> Compare(E1, CmpOp(OP, E2))
        => E1 ~> compareLeft(OP, E2) ... </k>
  rule <k> V1:Value ~> compareLeft(OP, E2)
        => E2 ~> compareRight(OP, V1) ... </k>
  rule <k> pyInt(I2) ~> compareRight(">=", exactNum(N1, D1))
        => pyBool(N1 >=Int (I2 *Int D1)) ... </k>
    requires D1 >Int 0

  // Branching and function return.
  rule <k> If(E, THEN, ELSE) => E ~> ifControl(THEN, ELSE) ... </k>
  rule <k> pyBool(true) ~> ifControl(THEN, _ELSE) => exec(THEN) ... </k>
  rule <k> pyBool(false) ~> ifControl(_THEN, ELSE) => exec(ELSE) ... </k>
  rule <k> Return(E) => E ~> returnControl ... </k>
  rule <k> V:Value ~> returnControl ~> _REST:K => .K </k>
       <result> noResult => V </result>

  // Exact parser for the ordinary and scientific decimal notation accepted
  // by Decimal.  A positive denominator is preserved by every helper.
  syntax Int ::= exponentPosition(String) [function, total]
  rule exponentPosition(S) => findString(S, "e", 0)
    requires findString(S, "e", 0) >=Int 0
  rule exponentPosition(S) => findString(S, "E", 0)
    requires findString(S, "e", 0) <Int 0

  syntax Value ::= parseDecimal(String) [function]
                 | parseExponent(String, Int) [function]
                 | parseMantissa(String) [function]
                 | parseMantissaAt(String, Int) [function]
                 | scaleDecimal(Value, Int) [function]

  rule parseDecimal(S) => parseMantissa(S)
    requires exponentPosition(S) <Int 0
  rule parseDecimal(S) => parseExponent(S, exponentPosition(S))
    requires exponentPosition(S) >=Int 0
  rule parseExponent(S, P) =>
    scaleDecimal(parseMantissa(substrString(S, 0, P)),
                 String2Int(substrString(S, P +Int 1, lengthString(S))))
    requires P >=Int 0

  rule parseMantissa(S) => exactNum(String2Int(S), 1)
    requires findString(S, ".", 0) <Int 0
  rule parseMantissa(S) => parseMantissaAt(S, findString(S, ".", 0))
    requires findString(S, ".", 0) >=Int 0
  rule parseMantissaAt(S, P) =>
    exactNum(
      String2Int(substrString(S, 0, P)
                 +String substrString(S, P +Int 1, lengthString(S))),
      10 ^Int (lengthString(S) -Int P -Int 1))
    requires P >=Int 0

  rule scaleDecimal(exactNum(N, D), E) => exactNum(N *Int (10 ^Int E), D)
    requires E >=Int 0
  rule scaleDecimal(exactNum(N, D), E) => exactNum(N, D *Int (10 ^Int (0 -Int E)))
    requires E <Int 0
endmodule
