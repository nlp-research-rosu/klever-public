requires "verification.k"

module MPY-SYNTAX
  imports INT-SYNTAX
  imports BOOL-SYNTAX
  imports STRING-SYNTAX

  syntax Module ::= "Module" "(" Stmt ")"

  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmt ")"
                | "Return" "(" Expr ")"

  syntax Params ::= "Params" "(" String ")"

  syntax Expr ::= "Name" "(" String ")"
                | "Int" "(" Int ")"
                | "Call" "(" Expr "," Expr ")"
                | "Call" "(" Expr "," Expr "," Expr ")"
                | "KwArg" "(" String "," Expr ")"
                | "BoolOp" "(" String "," Expr "," Expr ")"
                | "Compare" "(" Expr "," Expr ")"
                | "CmpOp" "(" String "," Expr ")"
                | "BinOp" "(" String "," Expr "," Expr ")"
                | "UnaryOp" "(" String "," Expr ")"
                | "Subscript" "(" Expr "," Expr ")"

  syntax IntList ::= "nil"
                   | "cons" "(" Int "," IntList ")"

  syntax Val ::= "ListVal" "(" IntList ")"
               | "IntVal" "(" Int ")"
               | "BoolVal" "(" Bool ")"
               | "NoneVal"
endmodule

module MPY
  imports MPY-SYNTAX
  imports INT
  imports BOOL
  imports STRING
  imports MAP

  syntax KItem ::= invoke(String, Val)
                 | execute(Stmt, Map)
                 | finish(Val)

  configuration
    <py>
      <k> $PGM:Module ~> invoke("sort_array", ListVal($INPUT:IntList)) </k>
      <input> ListVal($INPUT) </input>
      <result> NoneVal </result>
    </py>

  rule <k> Module(FuncDef(F, Params(P), BODY)) ~> invoke(F, V)
        => execute(BODY, P |-> V) ... </k>

  rule <k> execute(Return(E), ENV) => finish(eval(E, ENV)) ... </k>
  rule <k> finish(V) => .K </k> <result> _ => V </result>

  // Expression evaluation.  Calls to built-ins are explicit semantic rules;
  // py2mpy itself only preserves their AST shape.
  syntax Val ::= eval(Expr, Map) [function]
  rule eval(Name(X), (X |-> V) _REST) => V
  rule eval(Int(I), _) => IntVal(I)

  rule eval(Call(Name("len"), E), ENV)
    => lenVal(eval(E, ENV))

  rule eval(Call(Name("sorted"), E, KwArg("reverse", R)), ENV)
    => sortedVal(eval(E, ENV), eval(R, ENV))

  rule eval(BoolOp("and", E1, E2), ENV)
    => andVal(eval(E1, ENV), E2, ENV)

  // This source only observes len through `len(array) > 0`.  Matching the
  // list shape here also exposes the short-circuit fact to symbolic proofs.
  rule eval(Compare(Call(Name("len"), E), CmpOp(">", Int(0))), ENV)
    => nonemptyVal(eval(E, ENV))

  rule eval(Compare(E1, CmpOp("==", E2)), ENV)
    => compareVal("==", eval(E1, ENV), eval(E2, ENV))

  rule eval(BinOp(OP, E1, E2), ENV)
    => binVal(OP, eval(E1, ENV), eval(E2, ENV))

  rule eval(UnaryOp(OP, E), ENV)
    => unaryVal(OP, eval(E, ENV))

  rule eval(Subscript(E1, E2), ENV)
    => subscriptVal(eval(E1, ENV), eval(E2, ENV))

  syntax Val ::= lenVal(Val) [function]
               | sortedVal(Val, Val) [function]
               | andVal(Val, Expr, Map) [function]
               | nonemptyVal(Val) [function]
               | compareVal(String, Val, Val) [function]
               | binVal(String, Val, Val) [function]
               | unaryVal(String, Val) [function]
               | subscriptVal(Val, Val) [function]

  rule lenVal(ListVal(L)) => IntVal(ilen(L))

  rule sortedVal(ListVal(L), BoolVal(B)) => ListVal(sortFlag(L, B))

  rule andVal(BoolVal(false), _, _) => BoolVal(false)
  rule andVal(BoolVal(true), E, ENV) => eval(E, ENV)

  rule nonemptyVal(ListVal(nil)) => BoolVal(false)
  rule nonemptyVal(ListVal(cons(_, _))) => BoolVal(true)

  rule compareVal("==", IntVal(I), IntVal(J)) => BoolVal(I ==Int J)

  rule binVal("+", IntVal(I), IntVal(J)) => IntVal(I +Int J)
  rule binVal("%", IntVal(I), IntVal(J)) => IntVal(I %Int J)
  rule unaryVal("-", IntVal(I)) => IntVal(0 -Int I)

  rule subscriptVal(ListVal(cons(I, _IS)), IntVal(0)) => IntVal(I)
  rule subscriptVal(ListVal(cons(I, IS)), IntVal(-1))
    => IntVal(ilast(cons(I, IS)))

  syntax Int ::= ilen(IntList) [function, total]
               | ilast(IntList) [function]
  rule ilen(nil) => 0
  rule ilen(cons(_, IS)) => 1 +Int ilen(IS)
  rule ilast(cons(I, nil)) => I
  rule ilast(cons(_, cons(J, JS))) => ilast(cons(J, JS))

  // A mathematical insertion sort gives Python's sorted built-in its meaning.
  syntax IntList ::= sortAsc(IntList) [function, total]
                   | insertAsc(Int, IntList) [function, total]
                   | sortFlag(IntList, Bool) [function, total]
                   | reverse(IntList) [function, total]
                   | reverseAcc(IntList, IntList) [function, total]

  rule sortAsc(nil) => nil
  rule sortAsc(cons(I, IS)) => insertAsc(I, sortAsc(IS))

  rule insertAsc(I, nil) => cons(I, nil)
  rule insertAsc(I, cons(J, JS)) => cons(I, cons(J, JS)) requires I <=Int J
  rule insertAsc(I, cons(J, JS)) => cons(J, insertAsc(I, JS)) requires I >Int J

  rule sortFlag(L, false) => sortAsc(L)
  rule sortFlag(L, true)  => reverse(sortAsc(L))

  rule reverse(L) => reverseAcc(L, nil)
  rule reverseAcc(nil, ACC) => ACC
  rule reverseAcc(cons(I, IS), ACC) => reverseAcc(IS, cons(I, ACC))
endmodule
