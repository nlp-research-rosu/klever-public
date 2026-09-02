requires "verification.k"

module MPY-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX
  imports MAP

  // The concrete constructor grammar emitted by py2mpy.py for solution.py.
  syntax Program ::= "Module" "(" Stmt ")" [symbol(moduleProgram)]
  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmt ")"
                  [symbol(functionDefinition)]
                | "Return" "(" Expr ")" [symbol(returnStatement)]
  syntax Params ::= "Params" "(" String ")" [symbol(parameters)]

  syntax Expr ::= "Int" "(" Int ")" [symbol(integerExpression)]
                | "Str" "(" String ")" [symbol(stringExpression)]
                | "Name" "(" String ")" [symbol(nameExpression)]
                | "ListExpr" "(" Expr ")" [symbol(listExpression)]
                | "Attribute" "(" Expr "," String ")"
                  [symbol(attributeExpression)]
                | "Call" "(" Expr "," Expr ")" [symbol(callExpression)]
                | "BinOp" "(" String "," Expr "," Expr ")"
                  [symbol(binaryExpression)]

  // Python values used by this task.  PyVals is deliberately explicit rather
  // than K's builtin List so symbolic list tails remain easy to quantify over.
  syntax Value ::= Int | String | PyList
  syntax PyList ::= "pyList" "(" PyVals ")" [symbol(pyList)]
  syntax PyVals ::= ".PyVals" [symbol(emptyPyVals)]
                  | Value "::" PyVals [symbol(consPyVals)]
endmodule

module MPY-SEMANTICS
  imports MPY-SYNTAX
  imports INT
  imports BOOL

  configuration
    <mpy>
      <k> init($PGM) </k>
      <program> $PGM:Program </program>
      <input> $INPUT:PyList </input>
      <result> noResult </result>
    </mpy>

  syntax KItem ::= "init" "(" Program ")" [symbol(initProgram)]
                 | "noResult" [symbol(noResult)]

  // Calling the one module-level function binds its sole parameter and
  // evaluates the return expression.  The function name is not special here.
  rule <k> init(Module(FuncDef(_F, Params(X), Return(E)))) => .K </k>
       <input> V </input>
       <result> noResult => #eval(E, X |-> V) </result>

  syntax Value ::= "#eval" "(" Expr "," Map ")" [function]
  rule #eval(Int(I), _ENV) => I
  rule #eval(Str(S), _ENV) => S
  rule #eval(Name(X), X |-> V) => V
  rule #eval(ListExpr(E), ENV) => pyList(#eval(E, ENV) :: .PyVals)
  rule #eval(BinOp("+", L, R), ENV)
    => #add(#eval(L, ENV), #eval(R, ENV))
  rule #eval(BinOp("*", L, R), ENV)
    => #multiply(#eval(L, ENV), #eval(R, ENV))
  rule #eval(Call(Attribute(BASE, "count"), ARG), ENV)
    => #count(#eval(BASE, ENV), #eval(ARG, ENV))

  syntax Value ::= "#add" "(" Value "," Value ")" [function]
                 | "#multiply" "(" Value "," Value ")" [function]
  syntax Int ::= "#count" "(" Value "," Value ")" [function]
  syntax PyVals ::= "#appendVals" "(" PyVals "," PyVals ")" [function]
                  | "#repeatVals" "(" PyVals "," Int ")" [function]

  rule #add(pyList(XS), pyList(YS)) => pyList(#appendVals(XS, YS))
  rule #appendVals(.PyVals, YS) => YS
  rule #appendVals(X :: XS, YS) => X :: #appendVals(XS, YS)

  rule #multiply(pyList(XS), N:Int) => pyList(#repeatVals(XS, N))
  rule #repeatVals(_XS, N) => .PyVals requires N <=Int 0
  rule #repeatVals(XS, N) => #appendVals(XS, #repeatVals(XS, N -Int 1))
    requires N >Int 0

  rule #count(pyList(.PyVals), _N:Int) => 0
  rule #count(pyList(I:Int :: XS), N:Int)
    => 1 +Int (#count(pyList(XS), N))
    requires I ==Int N
  rule #count(pyList(I:Int :: XS), N:Int)
    => #count(pyList(XS), N)
    requires I =/=Int N
endmodule

// Compilation root: retain the executable semantics and its verification
// vocabulary in the compiled definition used by both krun and kprove.
module MPY-COMPILED
  imports MPY-SEMANTICS
  imports MPY-VERIFICATION
endmodule
