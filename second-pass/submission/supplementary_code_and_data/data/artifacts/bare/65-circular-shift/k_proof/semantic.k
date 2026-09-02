module MPY-SYNTAX
  imports DOMAINS

  syntax Program ::= "Module" "(" Stmts ")" [symbol(Module)]
  syntax Stmts   ::= List{Stmt, ""}

  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")" [symbol(FuncDef)]
                | "Assign" "(" Expr "," Expr ")"                 [symbol(Assign)]
                | "If" "(" Expr "," Stmts "," Stmts ")"       [symbol(If)]
                | "Return" "(" Expr ")"                         [symbol(Return)]

  syntax Params     ::= "Params" "(" ParamNames ")" [symbol(Params)]
  syntax ParamNames ::= List{String, ","}

  syntax Expr ::= "Name" "(" String ")"                         [symbol(Name)]
                | "Int" "(" Int ")"                             [symbol(Int)]
                | "BinOp" "(" String "," Expr "," Expr ")"    [symbol(BinOp)]
                | "UnaryOp" "(" String "," Expr ")"            [symbol(UnaryOp)]
                | "Compare" "(" Expr "," CmpOp ")"             [symbol(Compare)]
                | "Call" "(" Expr "," Exprs ")"                [symbol(Call)]
                | "Subscript" "(" Expr "," Slice ")"           [symbol(Subscript)]

  syntax Exprs ::= List{Expr, ","}
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")" [symbol(CmpOp)]
  syntax Slice ::= "Slice" "(" Bound "," Bound "," Bound ")" [symbol(Slice)]
  syntax Bound ::= Expr | "NoBound"
endmodule

module MPY
  imports MPY-SYNTAX

  syntax Val ::= "VInt" "(" Int ")"
               | "VString" "(" String ")"
               | "VBool" "(" Bool ")"
               | "VNone"
  syntax Vals ::= List{Val, ","}

  configuration
    <mpy>
      <k> $PGM:Program </k>
      <entry> $ENTRY:String </entry>
      <args> $ARGS:Vals </args>
      <result> VNone </result>
    </mpy>

  rule <k> P:Program => .K </k>
       <entry> F:String </entry>
       <args> A:Vals </args>
       <result> _ => runProgram(P, F, A) </result>

  // Top-level definition lookup and positional parameter binding.
  syntax Val ::= runProgram(Program, String, Vals) [function]
  rule runProgram(Module(FuncDef(F, PS, BODY) _REST), F, ARGS)
    => resultOf(exec(BODY, bind(PS, ARGS)))
  rule runProgram(Module(FuncDef(F0, _, _) REST), F, ARGS)
    => runProgram(Module(REST), F, ARGS)
    requires F0 =/=String F

  syntax Map ::= bind(Params, Vals) [function]
  rule bind(Params(.ParamNames), .Vals) => .Map
  rule bind(Params((N:String, NS:ParamNames)), (V:Val, VS:Vals))
    => (N |-> V) bind(Params(NS), VS)

  // Statement execution returns early exactly when a Return is encountered.
  syntax ExecResult ::= returned(Val) | normal(Map)
  syntax ExecResult ::= exec(Stmts, Map) [function]
  syntax ExecResult ::= branch(Val, Stmts, Stmts, Stmts, Map) [function]
  syntax ExecResult ::= continue(ExecResult, Stmts) [function]
  syntax Val ::= resultOf(ExecResult) [function]

  rule exec(.Stmts, ENV) => normal(ENV)
  rule exec(Assign(Name(N), E) REST, ENV)
    => exec(REST, ENV [ N <- eval(E, ENV) ])
  rule exec(If(COND, THEN, ELSE) REST, ENV)
    => branch(eval(COND, ENV), THEN, ELSE, REST, ENV)
  rule exec(Return(E) _REST, ENV) => returned(eval(E, ENV))

  rule branch(VBool(B), THEN, _, REST, ENV)
    => continue(exec(THEN, ENV), REST)
    requires B
  rule branch(VBool(B), _, ELSE, REST, ENV)
    => continue(exec(ELSE, ENV), REST)
    requires notBool B
  rule continue(returned(V), _) => returned(V)
  rule continue(normal(ENV), REST) => exec(REST, ENV)
  rule resultOf(returned(V)) => V
  rule resultOf(normal(_)) => VNone

  // Expression semantics needed by solution.mpy.
  syntax Val ::= eval(Expr, Map) [function]
               | lookupVal(Map, String) [function]
               | pyStr(Val) [function]
               | pyLen(Val) [function]
               | unary(String, Val) [function]
               | binary(String, Val, Val) [function]
               | compare(String, Val, Val) [function]
               | sliceFrom(Val, Val) [function]
               | sliceTo(Val, Val) [function]
               | reverseValue(Val) [function]

  rule eval(Name(N), ENV) => lookupVal(ENV, N)
  rule lookupVal((N |-> V) _REST, N) => V
  rule eval(Int(I), _) => VInt(I)
  rule eval(UnaryOp(OP, E), ENV) => unary(OP, eval(E, ENV))
  rule eval(BinOp(OP, L, R), ENV) => binary(OP, eval(L, ENV), eval(R, ENV))
  rule eval(Compare(L, CmpOp(OP, R)), ENV)
    => compare(OP, eval(L, ENV), eval(R, ENV))
  rule eval(Call(Name("str"), E), ENV) => pyStr(eval(E, ENV))
  rule eval(Call(Name("len"), E), ENV) => pyLen(eval(E, ENV))
  rule eval(Subscript(E, Slice(NoBound, NoBound, UnaryOp("-", Int(1)))), ENV)
    => reverseValue(eval(E, ENV))
  rule eval(Subscript(E, Slice(LOWER:Expr, NoBound, NoBound)), ENV)
    => sliceFrom(eval(E, ENV), eval(LOWER, ENV))
  rule eval(Subscript(E, Slice(NoBound, UPPER:Expr, NoBound)), ENV)
    => sliceTo(eval(E, ENV), eval(UPPER, ENV))

  rule pyStr(VInt(I)) => VString(Int2String(I))
  rule pyLen(VString(S)) => VInt(lengthString(S))
  rule unary("-", VInt(I)) => VInt(0 -Int I)
  rule binary("-", VInt(I), VInt(J)) => VInt(I -Int J)
  rule binary("+", VString(S), VString(T)) => VString(S +String T)
  rule compare(">", VInt(I), VInt(J)) => VBool(I >Int J)

  // Python clamps ordinary slice endpoints into [0, length].
  syntax Int ::= clipIndex(Int, Int) [function, total]
  rule clipIndex(I, L) => 0 requires I <Int (0 -Int L)
  rule clipIndex(I, L) => I +Int L
    requires (0 -Int L) <=Int I andBool I <Int 0
  rule clipIndex(I, L) => I requires 0 <=Int I andBool I <=Int L
  rule clipIndex(I, L) => L requires L <Int I

  rule sliceFrom(VString(S), VInt(I))
    => VString(substrString(S, clipIndex(I, lengthString(S)), lengthString(S)))
  rule sliceTo(VString(S), VInt(I))
    => VString(substrString(S, 0, clipIndex(I, lengthString(S))))

  syntax String ::= reverseString(String) [function]
                  | reverseFrom(String, Int) [function]
  rule reverseValue(VString(S)) => VString(reverseString(S))
  rule reverseString(S) => reverseFrom(S, lengthString(S) -Int 1)
  rule reverseFrom(_, I) => "" requires I <Int 0
  rule reverseFrom(S, I)
    => substrString(S, I, I +Int 1) +String reverseFrom(S, I -Int 1)
    requires 0 <=Int I
endmodule
