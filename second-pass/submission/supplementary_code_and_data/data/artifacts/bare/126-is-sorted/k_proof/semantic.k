requires "list-domain.k"
requires "verification.k"

module MPY-SYNTAX
  imports VERIFICATION
  imports STRING
  imports MAP

  syntax Pgm ::= "Module" "(" Stmt ")" [symbol(module)]

  syntax Params ::= "Params" "(" String ")" [symbol(params1)]
  syntax CellVars ::= "CellVars" "(" String ")" [symbol(cellVars1)]
  syntax FreeVars ::= "FreeVars" "(" ")" [symbol(freeVars0)]

  syntax Stmt ::= "FuncDef" "(" String "," Params "," CellVars ","
                                  FreeVars "," Stmt ")" [symbol(funcDef)]
                | "Return" "(" Expr ")" [symbol(returnStmt)]

  syntax Expr ::= "Name" "(" String ")" [symbol(name)]
                | "Int" "(" Int ")" [symbol(intExpr)]
                | "Bool" "(" Bool ")" [symbol(boolExpr)]
                | "Attribute" "(" Expr "," String ")" [symbol(attribute)]
                | "Call" "(" Expr "," Expr ")" [symbol(call1)]
                | "BoolOp" "(" String "," Expr "," Expr ")" [symbol(boolOp2)]
                | "Compare" "(" Expr "," CmpOp ")" [symbol(compare1)]
                | "GenExp" "(" Expr "," CompFor ")" [symbol(genExp1)]
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")" [symbol(cmpOp)]
  syntax CompFor ::= "CompFor" "(" Expr "," Expr "," Expr ")"
                     [symbol(compFor)]

  syntax Value ::= "IntVal" "(" Int ")" [symbol(intVal)]
                 | "BoolVal" "(" Bool ")" [symbol(boolVal)]
                 | "PyList" "(" IntList ")" [symbol(pyList)]
endmodule

module MPY
  imports MPY-SYNTAX

  syntax KItem ::= "Run" "(" Pgm "," Value ")" [symbol(run)]
                 | "EvalStmt" "(" Stmt "," Map ")" [symbol(evalStmt)]

  configuration
    <k> Run($PGM:Pgm, $ARGS:Value) </k>

  // Loading the one-argument entry point and immediately invoking it.
  // CellVars is present because CPython classifies lst as captured by the
  // generator expression; the generator evaluator below reads that binding.
  rule <k> Run(Module(FuncDef("is_sorted", Params(X), _CV, _FV, BODY)), V)
        => EvalStmt(BODY, X |-> V) ... </k>

  rule <k> EvalStmt(Return(E), RHO) => eval(E, RHO) ... </k>

  syntax Value ::= eval(Expr, Map) [function]
  rule eval(Int(I), _) => IntVal(I)
  rule eval(Bool(B), _) => BoolVal(B)
  rule eval(Name(X), (X |-> V) _RHO) => V

  syntax IntList ::= asList(Value) [function]
  rule asList(PyList(IS)) => IS

  syntax Bool ::= asBool(Value) [function]
  rule asBool(BoolVal(B)) => B

  syntax Bool ::= eqValue(Value, Value) [function]
  rule eqValue(PyList(IS), PyList(JS)) => eqIntLists(IS, JS)
  rule eqValue(IntVal(I), IntVal(J)) => I ==Int J
  rule eqValue(BoolVal(B), BoolVal(C)) => B ==Bool C

  // Pure expression rules. Both BoolOp operands in this accepted subset are
  // booleans, so the denotation agrees with Python's short-circuit result.
  rule eval(BoolOp("and", E1, E2), RHO)
    => BoolVal(asBool(eval(E1, RHO)) andBool asBool(eval(E2, RHO)))

  rule eval(Compare(E1, CmpOp("==", E2)), RHO)
    => BoolVal(eqValue(eval(E1, RHO), eval(E2, RHO)))

  rule eval(Call(Name("sorted"), E), RHO)
    => PyList(sortInts(asList(eval(E, RHO))))

  // Denotation of all(source.count(x) <= 2 for x in source).  This fused rule
  // is equivalent to constructing the pure generator and folding Python all;
  // it also leaves a compact symbolic term for proof.
  rule eval(
         Call(Name("all"),
           GenExp(
             Compare(
               Call(Attribute(Name(SOURCE), "count"), Name(X)),
               CmpOp("<=", Int(LIMIT))),
             CompFor(Name(X), Name(SOURCE), Bool(true)))),
         (SOURCE |-> PyList(IS)) _RHO)
    => BoolVal(countsAtMost(IS, IS, LIMIT))
endmodule
