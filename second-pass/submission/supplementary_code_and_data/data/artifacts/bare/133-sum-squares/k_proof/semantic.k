module MPY-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX

  syntax PyModule ::= "Module" "(" PyStmts ")" [symbol(Module)]

  syntax PyStmts ::= List{PyStmt, ""}

  syntax PyStmt ::= "ImportFrom" "(" String "," String ")" [symbol(ImportFrom)]
                  | "FuncDef" "(" String "," "Params" "(" String ")" "," PyStmts ")" [symbol(FuncDef)]
                  | "Assign" "(" PyExpr "," PyExpr ")" [symbol(Assign)]
                  | "AugAssign" "(" PyExpr "," String "," PyExpr ")" [symbol(AugAssign)]
                  | "For" "(" PyExpr "," PyExpr "," PyStmts ")" [symbol(For)]
                  | "Return" "(" PyExpr ")" [symbol(Return)]

  syntax PyExpr ::= "Name" "(" String ")" [symbol(Name)]
                  | "Int" "(" Int ")" [symbol(IntExpr)]
                  | "Call" "(" PyExpr "," PyExpr ")" [symbol(Call)]
                  | "BinOp" "(" String "," PyExpr "," PyExpr ")" [symbol(BinOp)]
endmodule

module MPY-DOMAIN
  imports INT

  // Exact rationals model numeric inputs without relying on backend-specific
  // floating-point hooks.  PosNat makes every denominator positive.
  syntax PosNat ::= "one" [symbol(one)]
                  | "next" "(" PosNat ")" [symbol(next)]
                  | "ten" [symbol(ten)]

  syntax Int ::= posInt(PosNat) [function, total]

  rule posInt(one) => 1
  rule posInt(next(P)) => 1 +Int posInt(P)
  rule posInt(ten) => 10

  syntax NumValue ::= "intVal" "(" Int ")" [symbol(intVal)]
                    | "ratVal" "(" Int "," PosNat ")" [symbol(ratVal)]

  syntax PList ::= "nil" [symbol(nil)]
                 | "cons" "(" NumValue "," PList ")" [symbol(cons)]

  syntax PValue ::= NumValue
                  | "listVal" "(" PList ")" [symbol(listVal)]

  syntax Int ::= ceilInt(NumValue) [function]

  rule ceilInt(intVal(I)) => I
  rule ceilInt(ratVal(N, D))
    => 0 -Int ((0 -Int N) divInt posInt(D))
endmodule

module MPY
  imports MPY-SYNTAX
  imports MPY-DOMAIN
  imports MAP
  imports STRING

  syntax Function ::= "function" "(" String "," PyStmts ")" [symbol(function)]
  syntax Env ::= ".Env" [symbol(emptyEnv)]
               | "binding" "(" String "," PValue ")" Env [symbol(binding)]

  syntax PValue ::= evalExpr(PyExpr, Env) [function]
                  | lookupValue(Env, String) [function]
                  | ceilValue(PValue) [function]
                  | addValue(PValue, PValue) [function]
                  | mulValue(PValue, PValue) [function]

  rule evalExpr(Int(I), _) => intVal(I)
  rule lookupValue(binding(X, V) _, X) => V
  rule lookupValue(binding(Y, _) RHO, X) => lookupValue(RHO, X)
    requires X =/=String Y
  rule evalExpr(Name(X), RHO) => lookupValue(RHO, X)
  rule evalExpr(Call(Name("ceil"), E), RHO) => ceilValue(evalExpr(E, RHO))
  rule evalExpr(BinOp("*", E1, E2), RHO)
    => mulValue(evalExpr(E1, RHO), evalExpr(E2, RHO))
  rule evalExpr(BinOp("+", E1, E2), RHO)
    => addValue(evalExpr(E1, RHO), evalExpr(E2, RHO))

  rule ceilValue(V:NumValue) => intVal(ceilInt(V))
  rule addValue(intVal(I1), intVal(I2)) => intVal(I1 +Int I2)
  rule mulValue(intVal(I1), intVal(I2)) => intVal(I1 *Int I2)

  syntax KItem ::= load(PyStmts) [symbol(load)]
                 | loadStmt(PyStmt) [symbol(loadStmt)]
                 | callEntry(PValue) [symbol(callEntry)]
                 | exec(PyStmts) [symbol(exec)]
                 | loop(String, PValue, PyStmts) [symbol(loop)]
                 | bind(String, PValue) [symbol(bind)]

  configuration
    <python>
      <k> $PGM:PyModule ~> callEntry($ARGS:PValue) </k>
      <functions> .Map </functions>
      <env> .Env </env>
    </python>

  rule <k> Module(SS) => load(SS) ... </k>

  rule <k> load(.PyStmts) => .K ... </k>
  rule <k> load(S:PyStmt SS:PyStmts) => loadStmt(S) ~> load(SS) ... </k>

  rule <k> loadStmt(ImportFrom(_, _)) => .K ... </k>
  rule <k> loadStmt(FuncDef(F, Params(P), BODY)) => .K ... </k>
       <functions> FUNS => FUNS [ F <- function(P, BODY) ] </functions>

  rule <k> callEntry(V) => exec(BODY) ... </k>
       <functions> ... "sum_squares" |-> function(P, BODY) ... </functions>
       <env> _ => binding(P, V) .Env </env>

  rule <k> exec(.PyStmts) => .K ... </k>

  rule <k> exec(Assign(Name(X), E) SS) => exec(SS) ... </k>
       <env> RHO => binding(X, evalExpr(E, RHO)) RHO </env>

  rule <k> exec(AugAssign(Name(X), "+", E) SS) => exec(SS) ... </k>
       <env> RHO => binding(X, addValue(lookupValue(RHO, X), evalExpr(E, RHO))) RHO </env>

  rule <k> exec(For(Name(X), E, BODY) SS) => loop(X, evalExpr(E, RHO), BODY) ~> exec(SS) ... </k>
       <env> RHO </env>

  rule <k> exec(Return(E) _SS) => evalExpr(E, RHO) ... </k>
       <env> RHO </env>

  rule <k> loop(_, listVal(nil), _) => .K ... </k>
  rule <k> loop(X, listVal(cons(V, VS)), BODY)
        => bind(X, V) ~> exec(BODY) ~> loop(X, listVal(VS), BODY) ... </k>

  rule <k> bind(X, V) => .K ... </k>
       <env> RHO => binding(X, V) RHO </env>
endmodule
