module MPY-SYNTAX
  imports INT
  imports BOOL
  imports STRING

  // The source language is the constructor language emitted by py2mpy.py.
  syntax ModuleAst ::= "Module" "(" Stmts ")"
  syntax Stmts    ::= List{Stmt, ""}
  syntax Strings  ::= List{String, ","}
  syntax Exprs    ::= List{Expr, ","}
  syntax CompFors ::= List{CompFor, ""}

  syntax Params   ::= "Params"   "(" Strings ")"
  syntax CellVars ::= "CellVars" "(" Strings ")"
  syntax FreeVars ::= "FreeVars" "(" Strings ")"

  syntax Stmt ::= "ImportFrom" "(" String "," Strings ")"
                | "FuncDef" "(" String "," Params "," Stmts ")"
                | "FuncDef" "(" String "," Params "," CellVars "," FreeVars "," Stmts ")"
                | "Assign" "(" Expr "," Expr ")"
                | "Return" "(" Expr ")"

  syntax Expr ::= "Name"     "(" String ")"
                | "Int"      "(" Int ")"
                | "Float"    "(" Float ")"
                | "Bool"     "(" Bool ")"
                | "BinOp"    "(" String "," Expr "," Expr ")"
                | "Call"     "(" Expr "," Exprs ")"
                | "ListComp" "(" Expr "," CompFors ")"

  syntax CompFor ::= "CompFor" "(" Expr "," Expr "," Exprs ")"
endmodule

module SEMANTIC
  imports MPY-SYNTAX

  // Exact rational numbers keep both execution and proof independent of
  // host floating-point rounding.  Runtime inputs use nums(rat(...), ...).
  syntax Num  ::= "rat" "(" Int "," Int ")"
                | "addNum"   "(" Num "," Num ")" [function]
                | "subNum"   "(" Num "," Num ")" [function]
                | "divNum"   "(" Num "," Num ")" [function]
                | "absNum"   "(" Num ")" [function]
                | "sumNums"  "(" Nums ")" [function]
                | "countNums" "(" Nums ")" [function]
                | "sumAbs"   "(" Nums "," Num ")" [function]
                | "asNum"    "(" Value ")" [function]
  syntax Nums ::= List{Num, ","}

  syntax Value ::= Num
                 | "nums" "(" Nums ")"
                 | "comprehension" "(" Expr "," String "," Nums "," Env ")"

  syntax Env ::= "emptyEnv"
               | "bind" "(" String "," Value "," Env ")"
  syntax Value ::= "lookup" "(" String "," Env ")" [function]

  syntax Value ::= "eval" "(" Expr "," Env ")" [function]
                 | "sumValue" "(" Value ")" [function]
                 | "lenValue" "(" Value ")" [function]
                 | "absValue" "(" Value ")" [function]
                 | "subValue" "(" Value "," Value ")" [function]
                 | "divValue" "(" Value "," Value ")" [function]
                 | "makeComp" "(" Expr "," String "," Value "," Env ")" [function]

  syntax Result ::= "noResult" | "result" "(" Value ")"

  configuration
    <mad>
      <k> init($PGM:ModuleAst, $ARGS:Value) </k>
      <env> emptyEnv </env>
      <result> noResult </result>
    </mad>

  syntax KItem ::= "init" "(" ModuleAst "," Value ")"
                 | "seekTarget" "(" Stmts "," Value ")"
                 | "exec" "(" Stmts ")"
                 | "setVar" "(" String "," Value ")"
                 | "finish" "(" Value ")"

  // Module loading ignores imports and locates the requested unary function.
  rule <k> init(Module(SS), ARGS) => seekTarget(SS, ARGS) ... </k>
  rule <k> seekTarget(ImportFrom(_, _) REST, ARGS)
        => seekTarget(REST, ARGS) ... </k>
  rule <k> seekTarget(FuncDef("mean_absolute_deviation", Params("numbers"),
                              _, _, BODY) _REST, ARGS)
        => exec(BODY) ... </k>
       <env> _ => bind("numbers", ARGS, emptyEnv) </env>
  rule <k> seekTarget(FuncDef(_, _, _) REST, ARGS)
        => seekTarget(REST, ARGS) ... </k>
  rule <k> seekTarget(FuncDef(F, _, _, _, _) REST, ARGS)
        => seekTarget(REST, ARGS) ... </k>
    requires F =/=String "mean_absolute_deviation"

  // The statement fragment needed by the submitted implementation.
  rule <k> exec(.Stmts) => .K ... </k>
  rule <k> exec(Assign(Name(X), E) REST)
        => setVar(X, eval(E, ENV)) ~> exec(REST) ... </k>
       <env> ENV </env>
  rule <k> setVar(X, V) => .K ... </k>
       <env> ENV => bind(X, V, ENV) </env>
  rule <k> exec(Return(E) _REST) => finish(eval(E, ENV)) ... </k>
       <env> ENV </env>
  rule <k> finish(V) => .K ... </k>
       <result> noResult => result(V) </result>

  // Lexical environments; the newest binding shadows older bindings.
  rule lookup(X, bind(X, V, _)) => V
  rule lookup(X, bind(Y, _, ENV)) => lookup(X, ENV)
    requires X =/=String Y

  // Denotational expression rules.  Comprehensions retain their lexical
  // environment until consumed by sum.
  rule eval(Name(X), ENV) => lookup(X, ENV)
  rule eval(Int(I), _) => rat(I, 1)
  rule eval(BinOp("-", A, B), ENV)
    => subValue(eval(A, ENV), eval(B, ENV))
  rule eval(BinOp("/", A, B), ENV)
    => divValue(eval(A, ENV), eval(B, ENV))
  rule eval(Call(Name("sum"), E), ENV) => sumValue(eval(E, ENV))
  rule eval(Call(Name("len"), E), ENV) => lenValue(eval(E, ENV))
  rule eval(Call(Name("abs"), E), ENV) => absValue(eval(E, ENV))
  rule eval(ListComp(E, CompFor(Name(X), ITER, Bool(true))), ENV)
    => makeComp(E, X, eval(ITER, ENV), ENV)

  rule makeComp(E, X, nums(NS), ENV) => comprehension(E, X, NS, ENV)
  rule sumValue(nums(NS)) => sumNums(NS)
  rule lenValue(nums(NS)) => countNums(NS)
  rule absValue(N:Num) => absNum(N)
  rule subValue(A:Num, B:Num) => subNum(A, B)
  rule divValue(A:Num, B:Num) => divNum(A, B)

  // Fusion for sum(abs(x - center) for x in numbers).  This is the usual
  // fold semantics of the list comprehension, retained symbolically for
  // arbitrary lists and unfolded for concrete lists below.
  rule sumValue(comprehension(
          Call(Name("abs"), BinOp("-", Name(X), Name(M))), X, NS, ENV))
    => sumAbs(NS, asNum(lookup(M, ENV)))

  rule asNum(N:Num) => N

  // Exact rational arithmetic.
  rule addNum(rat(A, B), rat(C, D))
    => rat(A *Int D +Int C *Int B, B *Int D)
  rule subNum(rat(A, B), rat(C, D))
    => rat(A *Int D -Int C *Int B, B *Int D)
  rule divNum(rat(A, B), rat(C, D))
    => rat(A *Int D, B *Int C)
  rule absNum(rat(A, B)) => rat(0 -Int A, B)
    requires A <Int 0
  rule absNum(rat(A, B)) => rat(A, B)
    requires A >=Int 0

  rule sumNums(.Nums) => rat(0, 1)
  rule sumNums(N, NS) => addNum(N, sumNums(NS))
  rule countNums(.Nums) => rat(0, 1)
  rule countNums(_N, NS) => addNum(rat(1, 1), countNums(NS))
  rule sumAbs(.Nums, _MEAN) => rat(0, 1)
  rule sumAbs(N, NS, MEAN) => addNum(absNum(subNum(N, MEAN)), sumAbs(NS, MEAN))

endmodule
