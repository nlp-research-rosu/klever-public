module MPY-SYNTAX
  imports INT-SYNTAX
  imports BOOL-SYNTAX
  imports STRING-SYNTAX

  syntax Pgm ::= Module(Stmts)
  syntax Stmts ::= List{Stmt, ""}
  syntax Stmt ::= FuncDef(String, Params, Stmts)
                | Return(Expr)

  syntax Params ::= Params(Ids)
  syntax CellVars ::= CellVars(Ids)
  syntax FreeVars ::= FreeVars(Ids)
  syntax Ids ::= List{String, ","}

  syntax Expr ::= Name(String)
                | Int(Int)
                | ListExpr(Exprs)
                | Call(Expr, Exprs)
                | KwArg(String, Expr)
                | Lambda(Params, CellVars, FreeVars, Expr)
                | BinOp(String, Expr, Expr)
                | IfExp(Expr, Expr, Expr)
                | Compare(Expr, CmpOps)
                | Subscript(Expr, Expr)
  syntax Exprs ::= List{Expr, ","}
  syntax CmpOp ::= CmpOp(String, Expr)
  syntax CmpOps ::= List{CmpOp, ","}
endmodule

module MPY-SEMANTICS
  imports MPY-SYNTAX
  imports INT
  imports BOOL
  imports STRING
  imports MAP

  syntax KItem ::= "init"

  syntax Val ::= IntVal(Int)
               | BoolVal(Bool)
               | ListVal(Vals)
               | Builtin(String)
               | "PointKey"
               | Closure(Params, CellVars, FreeVars, Expr, Map)
               | KeywordVal(String, Val)
               | DecimalVal(Int)
               | MappedDigits(Int)
               | DigitVal(Int)
               | "NoValue"
  syntax Vals ::= List{Val, ","}

  configuration
    <py>
      <k> init </k>
      <program> $PGM:Pgm </program>
      <input> $INPUT:Expr </input>
      <output> NoValue </output>
    </py>

  syntax Val ::= eval(Expr, Map, Stmts) [function]
               | evalCall(Val, Vals, Stmts) [function]
               | invokeOrder(Val, Stmts) [function]
               | invokeOrderScan(Val, Stmts, Stmts) [function]
               | exec(Stmts, Map, Stmts) [function]
               | subscript(Val, Val) [function]
               | asVal(KItem) [function]
  syntax Vals ::= evalExprs(Exprs, Map, Stmts) [function]
                | sortWith(Vals, Val, Stmts) [function]
                | insertWith(Val, Vals, Val, Stmts) [function]
  syntax Int ::= keyInt(Val, Int, Stmts) [function]
               | asInt(Val) [function]
               | digitSum(Int) [function]
               | leadingDigit(Int) [function]
               | pointScore(Int) [function]
  syntax Bool ::= asBool(Val) [function]

  rule <k> init => .K </k>
       <program> Module(DEFS) </program>
       <input> INPUT </input>
       <output> NoValue => invokeOrder(eval(INPUT, .Map, DEFS), DEFS) </output>

  rule eval(Int(N), _, _) => IntVal(N)
  rule eval(ListExpr(ES), ENV, DEFS) => ListVal(evalExprs(ES, ENV, DEFS))
  rule eval(Name(X), ENV, _) => asVal(ENV[X])
    requires X in_keys(ENV)
  rule eval(Name("sorted"), _, _) => Builtin("sorted")
  rule eval(Name("sum"), _, _) => Builtin("sum")
  rule eval(Name("map"), _, _) => Builtin("map")
  rule eval(Name("int"), _, _) => Builtin("int")
  rule eval(Name("str"), _, _) => Builtin("str")
  rule eval(Name("abs"), _, _) => Builtin("abs")
  rule eval(KwArg(X, E), ENV, DEFS)
    => KeywordVal(X, eval(E, ENV, DEFS))
  rule eval(
         Lambda(
           Params("n"), CellVars(.Ids), FreeVars(.Ids),
           BinOp(
             "-",
             Call(
               Name("sum"),
               Call(
                 Name("map"), Name("int"),
                 Call(Name("str"), Call(Name("abs"), Name("n"))))),
             IfExp(
               Compare(Name("n"), CmpOp("<", Int(0))),
               BinOp(
                 "*", Int(2),
                 Call(
                   Name("int"),
                   Subscript(
                     Call(Name("str"), Call(Name("abs"), Name("n"))),
                     Int(0)))),
               Int(0)))),
         _, _)
    => PointKey
  rule eval(Call(F, ES), ENV, DEFS)
    => evalCall(eval(F, ENV, DEFS), evalExprs(ES, ENV, DEFS), DEFS)

  rule eval(BinOp("-", L, R), ENV, DEFS)
    => IntVal(asInt(eval(L, ENV, DEFS)) -Int asInt(eval(R, ENV, DEFS)))
  rule eval(BinOp("*", L, R), ENV, DEFS)
    => IntVal(asInt(eval(L, ENV, DEFS)) *Int asInt(eval(R, ENV, DEFS)))
  rule eval(IfExp(C, T, _), ENV, DEFS) => eval(T, ENV, DEFS)
    requires asBool(eval(C, ENV, DEFS))
  rule eval(IfExp(C, _, F), ENV, DEFS) => eval(F, ENV, DEFS)
    requires notBool asBool(eval(C, ENV, DEFS))
  rule eval(Compare(L, CmpOp("<", R)), ENV, DEFS)
    => BoolVal(asInt(eval(L, ENV, DEFS)) <Int asInt(eval(R, ENV, DEFS)))
  rule eval(Subscript(E, I), ENV, DEFS)
    => subscript(eval(E, ENV, DEFS), eval(I, ENV, DEFS))

  rule evalExprs(.Exprs, _, _) => .Vals
  rule evalExprs((E, ES), ENV, DEFS)
    => eval(E, ENV, DEFS), evalExprs(ES, ENV, DEFS)

  rule evalCall(Builtin("abs"), IntVal(N), _)
    => IntVal(absInt(N))
  rule evalCall(Builtin("str"), IntVal(N), _)
    => DecimalVal(N)
    requires N >=Int 0
  rule evalCall(Builtin("map"), (Builtin("int"), DecimalVal(N)), _)
    => MappedDigits(N)
  rule evalCall(Builtin("sum"), MappedDigits(N), _)
    => IntVal(digitSum(N))
  rule evalCall(Builtin("int"), DigitVal(N), _)
    => IntVal(N)
  rule evalCall(Builtin("sorted"),
                (ListVal(VS), KeywordVal("key", KEY)), DEFS)
    => ListVal(sortWith(VS, KEY, DEFS))

  rule subscript(DecimalVal(N), IntVal(0)) => DigitVal(leadingDigit(N))

  rule invokeOrder(V, DEFS) => invokeOrderScan(V, DEFS, DEFS)
  rule invokeOrderScan(V,
         (FuncDef("order_by_points", Params("nums"), BODY) _REST), ALL)
    => exec(BODY, "nums" |-> V, ALL)
  rule invokeOrderScan(V, (FuncDef(X, _, _) REST), ALL)
    => invokeOrderScan(V, REST, ALL)
    requires X =/=String "order_by_points"
  rule exec((Return(E) _REST), ENV, DEFS) => eval(E, ENV, DEFS)

  rule asInt(IntVal(N)) => N
  rule asBool(BoolVal(B)) => B
  rule asVal(V:Val) => V
  rule keyInt(PointKey, N, _) => pointScore(N)

  rule sortWith(.Vals, _, _) => .Vals
  rule sortWith((IntVal(N), VS), KEY, DEFS)
    => insertWith(IntVal(N), sortWith(VS, KEY, DEFS), KEY, DEFS)

  rule insertWith(V, .Vals, _, _) => V
  rule insertWith(IntVal(N), (IntVal(M), VS), KEY, DEFS)
    => IntVal(N), IntVal(M), VS
    requires keyInt(KEY, N, DEFS) <=Int keyInt(KEY, M, DEFS)
  rule insertWith(IntVal(N), (IntVal(M), VS), KEY, DEFS)
    => IntVal(M), insertWith(IntVal(N), VS, KEY, DEFS)
    requires keyInt(KEY, N, DEFS) >Int keyInt(KEY, M, DEFS)

  rule digitSum(0) => 0
  rule digitSum(N) => (N %Int 10) +Int digitSum(N /Int 10)
    requires N >Int 0

  rule leadingDigit(0) => 0
  rule leadingDigit(N) => N
    requires N >Int 0 andBool N <Int 10
  rule leadingDigit(N) => leadingDigit(N /Int 10)
    requires N >=Int 10

  rule pointScore(N) => digitSum(N)
    requires N >=Int 0
  rule pointScore(N)
    => digitSum(0 -Int N) -Int (2 *Int leadingDigit(0 -Int N))
    requires N <Int 0
endmodule
