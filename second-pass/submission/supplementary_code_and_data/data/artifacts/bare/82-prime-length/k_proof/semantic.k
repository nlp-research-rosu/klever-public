requires "domains.md"

module MPY-SYNTAX
  imports BOOL-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX

  syntax Program ::= "Module" "(" Stmts ")"

  syntax Stmts ::= List{Stmt, ""}
  syntax Stmt ::= "FuncDef" "(" String "," Params "," CellVars "," FreeVars "," Stmts ")"
                | "Assign" "(" Expr "," Expr ")"
                | "Return" "(" Expr ")"

  syntax Params   ::= "Params" "(" Strings ")"
  syntax CellVars ::= "CellVars" "(" Strings ")"
  syntax FreeVars ::= "FreeVars" "(" Strings ")"
  syntax Strings  ::= List{String, ","}

  syntax Expr ::= "Int" "(" Int ")"
                | "Bool" "(" Bool ")"
                | "Str" "(" String ")"
                | "Name" "(" String ")"
                | "Call" "(" Expr "," Exprs ")"
                | "BinOp" "(" String "," Expr "," Expr ")"
                | "BoolOp" "(" String "," Exprs ")"
                | "Compare" "(" Expr "," CmpOps ")"
                | "GenExp" "(" Expr "," CompFors ")"

  syntax Exprs ::= List{Expr, ","}
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"
  syntax CmpOps ::= List{CmpOp, ","}
  syntax CompFor ::= "CompFor" "(" Expr "," Expr "," Exprs ")"
  syntax CompFors ::= List{CompFor, ""}

  syntax Value ::= "VInt" "(" Int ")"
                 | "VBool" "(" Bool ")"
                 | "VStr" "(" String ")"

  syntax Result ::= "noResult" | Value
  syntax KItem ::= "run" "(" Program "," Value ")"
                 | "#exec" "(" Stmts ")"
endmodule

module SEMANTIC
  imports MPY-SYNTAX
  imports BOOL
  imports INT
  imports MAP
  imports STRING

  configuration
    <py>
      <k> run($PGM:Program, $ARG:Value) </k>
      <env> .Map </env>
      <return> noResult </return>
    </py>

  // Loading the translated module also performs the requested entry-point
  // call.  This task has one top-level function and one positional argument.
  rule <k> run(Module(FuncDef(F, Params(P, .Strings), _CV, _FV, BODY)), ARG)
           => #exec(BODY) ... </k>
       <env> .Map => P |-> ARG </env>
    requires F ==String "prime_length"

  rule <k> #exec(Assign(Name(X), E) SS) => #exec(SS) ... </k>
       <env> ENV => ENV [ X <- eval(E, ENV) ] </env>

  rule <k> #exec(Return(E) _SS) => .K ... </k>
       <env> ENV </env>
       <return> noResult => eval(E, ENV) </return>

  syntax Value ::= eval(Expr, Map) [function, total]
  rule eval(Int(I),       _ENV) => VInt(I)
  rule eval(Bool(B),      _ENV) => VBool(B)
  rule eval(Str(S),       _ENV) => VStr(S)
  rule eval(Name(X),       ENV) => {ENV[X]}:>Value
    requires X in_keys(ENV)

  rule eval(Call(Name("len"), E), ENV)
    => VInt(valueLength(eval(E, ENV)))

  syntax Int ::= valueLength(Value) [function, total]
  rule valueLength(VStr(S)) => lengthString(S)

  rule eval(BinOp("%", E1, E2), ENV)
    => VInt(asInt(eval(E1, ENV)) %Int asInt(eval(E2, ENV)))

  syntax Int ::= asInt(Value) [function, total]
  rule asInt(VInt(I)) => I

  rule eval(Compare(E1, CmpOp(">=", E2)), ENV)
    => VBool(asInt(eval(E1, ENV)) >=Int asInt(eval(E2, ENV)))
  rule eval(Compare(E1, CmpOp("!=", E2)), ENV)
    => VBool(asInt(eval(E1, ENV)) =/=Int asInt(eval(E2, ENV)))

  rule eval(BoolOp("and", E1, E2), ENV)
    => VBool(asBool(eval(E1, ENV)) andBool asBool(eval(E2, ENV)))

  // Expressions in this semantics are pure.  Eager evaluation therefore has
  // the same result as Python's short-circuiting `and` for the accepted AST.

  syntax Bool ::= asBool(Value) [function, total]
  rule asBool(VBool(B)) => B

  // `all(n % i != 0 for i in range(lo, hi))` denotes that every candidate
  // in the half-open integer range is a non-divisor.  The source AST is kept
  // intact by py2mpy; this semantic rule gives that AST its meaning.
  rule eval(
         Call(Name("all"),
           GenExp(
             Compare(BinOp("%", Name(NX), Name(IX)), CmpOp("!=", Int(0))),
             CompFor(Name(IX),
               Call(Name("range"), Int(LO), Name(HX)),
               Bool(true)))),
         ENV)
    => VBool(noDivisors(asInt({ENV[NX]}:>Value),
                        LO,
                        asInt({ENV[HX]}:>Value)))
    requires NX =/=String IX
     andBool NX in_keys(ENV)
     andBool HX in_keys(ENV)

  // Executable, ground definition of universal non-divisibility on [D, HI).
  // concrete(...) deliberately keeps the recursive range opaque during a
  // symbolic proof while evaluating it completely for every concrete run.
  syntax Bool ::= noDivisors(Int, Int, Int) [function, total]
  rule noDivisors(_N, D, HI) => true
    requires D >=Int HI
    [concrete(D, HI), simplification]
  rule noDivisors(N, D, HI) => false
    requires D <Int HI andBool N %Int D ==Int 0
    [concrete(N, D, HI), simplification]
  rule noDivisors(N, D, HI) => noDivisors(N, D +Int 1, HI)
    requires D <Int HI andBool N %Int D =/=Int 0
    [concrete(N, D, HI), simplification]
endmodule
