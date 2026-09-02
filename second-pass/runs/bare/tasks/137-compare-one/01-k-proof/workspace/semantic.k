requires "domains.md"

module MPY-SYNTAX
  imports INT-SYNTAX
  imports BOOL-SYNTAX
  imports STRING-SYNTAX

  syntax FloatLiteral ::= r"[\\+\\-]?[0-9]+\\.[0-9]+" [token]

  syntax Pgm ::= "Module" "(" Stmts ")"

  syntax Stmts ::= List{Stmt, ""}
  syntax Names ::= List{String, ","}
  syntax Params ::= "Params" "(" Names ")"
  syntax Exprs ::= List{Expr, ","}
  syntax CmpOps ::= List{CmpOp, ","}

  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "Assign" "(" Expr "," Expr ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"
                | "Return" "(" Expr ")"

  syntax Expr ::= "Name" "(" String ")"
                | "Int" "(" Int ")"
                | "Float" "(" FloatLiteral ")"
                | "Str" "(" String ")"
                | "NoneVal"
                | "Call" "(" Expr "," Exprs ")"
                | "Attribute" "(" Expr "," String ")"
                | "Compare" "(" Expr "," CmpOps ")"

  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"

  syntax PyVal ::= pyInt(Int)
                 | pyFloat(Int, Int)
                 | pyStr(String)
                 | pyBool(Bool)
                 | pyType(String)
                 | "pyNone"
endmodule

module MPY-SEMANTIC
  imports MPY-SYNTAX
  imports BOOL
  imports INT
  imports STRING
  imports MAP
  imports K-EQUAL

  configuration
    <mpy>
      <k> $PGM:Pgm ~> invoke($A:PyVal, $B:PyVal) </k>
      <functions> .Map </functions>
      <env> .Map </env>
      <result> pyNone </result>
    </mpy>

  syntax Function ::= function(Params, Stmts)
  syntax KItem ::= execute(Stmts)
                 | invoke(PyVal, PyVal)

  rule <k> Module(SS) => execute(SS) ... </k>
  rule <k> execute(.Stmts) => .K ... </k>
  rule <k> execute(S:Stmt REST:Stmts) => S ~> execute(REST) ... </k>

  rule <k> FuncDef(NAME, PS, BODY) => .K ... </k>
       <functions> FS => FS [ NAME <- function(PS, BODY) ] </functions>

  rule <k> invoke(A, B) => execute(BODY) ... </k>
       <functions> ... "compare_one" |-> function(Params(ANAME, BNAME, .Names), BODY) ... </functions>
       <env> _ => (ANAME |-> A) (BNAME |-> B) </env>

  rule <k> Assign(Name(X), E) => .K ... </k>
       <env> ENV => ENV [ X <- eval(E, ENV) ] </env>

  rule <k> If(E, THEN, _ELSE) => execute(THEN) ... </k>
       <env> ENV </env>
    requires eval(E, ENV) ==K pyBool(true)
  rule <k> If(E, _THEN, ELSE) => execute(ELSE) ... </k>
       <env> ENV </env>
    requires eval(E, ENV) ==K pyBool(false)

  rule <k> Return(E) ~> _ => .K </k>
       <env> ENV </env>
       <result> _ => eval(E, ENV) </result>

  syntax PyVal ::= eval(Expr, Map) [function]
  syntax PyVal ::= typeOf(PyVal) [function, total]
  syntax PyVal ::= pyFloatOf(PyVal) [function]
  syntax PyVal ::= pyReplace(PyVal, PyVal, PyVal) [function]
  syntax PyVal ::= pyCompare(String, PyVal, PyVal) [function]

  rule eval(Name(X), ENV) => {ENV[X]}:>PyVal requires X in_keys(ENV)
  rule eval(Name("str"), _ENV) => pyType("str")
  rule eval(Int(I), _ENV) => pyInt(I)
  rule eval(Str(S), _ENV) => pyStr(S)
  rule eval(NoneVal, _ENV) => pyNone

  rule eval(Call(Name("type"), E), ENV) => typeOf(eval(E, ENV))
  rule eval(Call(Name("float"), E), ENV) => pyFloatOf(eval(E, ENV))
  rule eval(Call(Attribute(E, "replace"), OLD, NEW), ENV)
    => pyReplace(eval(E, ENV), eval(OLD, ENV), eval(NEW, ENV))
  rule eval(Compare(L, CmpOp(OP, R)), ENV)
    => pyCompare(OP, eval(L, ENV), eval(R, ENV))

  rule typeOf(pyInt(_)) => pyType("int")
  rule typeOf(pyFloat(_, _)) => pyType("float")
  rule typeOf(pyStr(_)) => pyType("str")
  rule typeOf(pyBool(_)) => pyType("bool")
  rule typeOf(pyNone) => pyType("NoneType")
  rule typeOf(pyType(_)) => pyType("type")

  rule pyFloatOf(pyInt(I)) => pyFloat(I, 1)
  rule pyFloatOf(pyFloat(N, D)) => pyFloat(N, D)
  rule pyFloatOf(pyStr(S)) => parseDecimal(S)

  rule pyReplace(pyStr(S), pyStr(OLD), pyStr(NEW))
    => pyStr(replaceAll(S, OLD, NEW))

  rule pyCompare("==", pyType(T1), pyType(T2))
    => pyBool(T1 ==String T2)
  rule pyCompare("==", pyFloat(N1, D1), pyFloat(N2, D2))
    => pyBool((N1 *Int D2) ==Int (N2 *Int D1))
  rule pyCompare(">", pyFloat(N1, D1), pyFloat(N2, D2))
    => pyBool((N1 *Int D2) >Int (N2 *Int D1))

  syntax PyVal ::= parseDecimal(String) [function]
  syntax PyVal ::= parseUnsignedDecimal(String, Int) [function]
  syntax Int ::= decimalDigits(String) [function]

  rule parseDecimal(S)
    => parseUnsignedDecimal(substrString(S, 1, lengthString(S)), -1)
    requires lengthString(S) >Int 0
     andBool substrString(S, 0, 1) ==String "-"
  rule parseDecimal(S) => parseUnsignedDecimal(S, 1)
    requires lengthString(S) ==Int 0
      orBool substrString(S, 0, 1) =/=String "-"

  rule parseUnsignedDecimal(S, SIGN)
    => pyFloat(SIGN *Int decimalDigits(S), 1)
    requires findString(S, ".", 0) ==Int -1
  rule parseUnsignedDecimal(S, SIGN)
    => pyFloat(
         SIGN *Int
           (decimalDigits(substrString(S, 0, findString(S, ".", 0)))
              *Int (10 ^Int lengthString(substrString(S, findString(S, ".", 0) +Int 1, lengthString(S))))
            +Int decimalDigits(substrString(S, findString(S, ".", 0) +Int 1, lengthString(S)))),
         10 ^Int lengthString(substrString(S, findString(S, ".", 0) +Int 1, lengthString(S))))
    requires findString(S, ".", 0) >=Int 0

  rule decimalDigits("") => 0
  rule decimalDigits(S) => String2Int(S) requires S =/=String ""
endmodule

module MPY
  imports MPY-SEMANTIC
endmodule
