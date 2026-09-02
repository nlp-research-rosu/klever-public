requires "domains.md"

module MPY-SYNTAX
  imports BOOL-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX

  syntax Program ::= "Module" "(" Stmt ")"

  syntax Params ::= "Params" "(" String "," String ")"

  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmt ")"
                | "Return" "(" Expr ")"

  syntax Expr ::= "Name" "(" String ")"
                | "Call" "(" Expr "," Expr ")"
                | "Call" "(" Expr "," Expr "," Expr ")"
                | "IfExp" "(" Expr "," Expr "," Expr ")"
                | "Compare" "(" Expr "," CmpOp ")"

  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"
endmodule

module SEMANTIC
  imports MPY-SYNTAX
  imports BOOL
  imports INT
  imports STRING

  // Runtime values for the Python subset used by solution.py.
  syntax PyString ::= "pyStr" "(" String ")"
  syntax StrVals ::= ".StrVals"
                   | PyString "::" StrVals
  syntax IntVals ::= ".IntVals"
                   | IntVal "::" IntVals
  syntax IntVal ::= "pyInt" "(" Int ")"
  syntax Value ::= PyString
                 | IntVal
                 | "pyList" "(" StrVals ")"
                 | "pyInts" "(" IntVals ")"
                 | "pyBool" "(" Bool ")"
                 | "builtin" "(" String ")"

  syntax Args ::= "args" "(" Value "," Value ")"
  syntax Env ::= "env" "(" Value "," Value ")"

  // Pure evaluator functions.  The source program has no side effects, so
  // its expression semantics can be given compositionally.
  syntax Value ::= eval(Expr, Env) [function]
                 | apply1(Value, Value) [function]
                 | apply2(Value, Value, Value) [function]
                 | lessEqual(Value, Value) [function]
                 | ifValue(Value, Value, Value) [function]
  syntax IntVals ::= mapLengths(StrVals) [function]
  syntax Int ::= sumInts(IntVals) [function]

  rule eval(Name("lst1"), env(V1, _V2)) => V1
  rule eval(Name("lst2"), env(_V1, V2)) => V2
  rule eval(Name("len"),  _ENV) => builtin("len")
  rule eval(Name("map"),  _ENV) => builtin("map")
  rule eval(Name("sum"),  _ENV) => builtin("sum")

  rule eval(Call(F, A), ENV)
    => apply1(eval(F, ENV), eval(A, ENV))
  rule eval(Call(F, A, B), ENV)
    => apply2(eval(F, ENV), eval(A, ENV), eval(B, ENV))
  rule eval(Compare(L, CmpOp("<=", R)), ENV)
    => lessEqual(eval(L, ENV), eval(R, ENV))
  rule eval(IfExp(COND, THEN, ELSE), ENV)
    => ifValue(eval(COND, ENV), eval(THEN, ENV), eval(ELSE, ENV))

  rule apply1(builtin("len"), pyStr(S)) => pyInt(lengthString(S))
  rule apply1(builtin("sum"), pyInts(IS)) => pyInt(sumInts(IS))
  rule apply2(builtin("map"), builtin("len"), pyList(SS))
    => pyInts(mapLengths(SS))

  rule mapLengths(.StrVals) => .IntVals
  rule mapLengths(pyStr(S) :: REST)
    => pyInt(lengthString(S)) :: mapLengths(REST)

  rule sumInts(.IntVals) => 0
  rule sumInts(pyInt(I) :: REST) => I +Int sumInts(REST)

  rule lessEqual(pyInt(I), pyInt(J)) => pyBool(true)
    requires I <=Int J
  rule lessEqual(pyInt(I), pyInt(J)) => pyBool(true)
    requires I ==Int J
  rule lessEqual(pyInt(I), pyInt(J)) => pyBool(false)
    requires I >Int J
  rule ifValue(pyBool(true),  THEN, _ELSE) => THEN
  rule ifValue(pyBool(false), _THEN, ELSE) => ELSE

  // A module is executed by invoking its translated two-argument function.
  syntax KItem ::= run(Program, Args)
  rule run(
         Module(FuncDef("total_match", Params("lst1", "lst2"), Return(BODY))),
         args(V1, V2))
    => eval(BODY, env(V1, V2))

  configuration <k> run($PGM:Program, $ARGS:Args) </k>
endmodule

module SEMANTIC-SYNTAX
  imports MPY-SYNTAX
  imports SEMANTIC
endmodule
