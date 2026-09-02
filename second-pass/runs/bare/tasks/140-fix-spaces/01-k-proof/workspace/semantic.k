requires "domains.md"

module MPY-SYNTAX
  imports BOOL-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX

  syntax Program ::= "Module" "(" Stmts ")"

  syntax Stmts ::= List{Stmt, ""}
  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "Return" "(" Expr ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"

  syntax Ids ::= List{String, ","}
  syntax Params ::= "Params" "(" Ids ")"

  syntax Exprs ::= List{Expr, ","}
  syntax Expr ::= "Name" "(" String ")"
                | "Str" "(" String ")"
                | "Int" "(" Int ")"
                | "BinOp" "(" String "," Expr "," Expr ")"
                | "Compare" "(" Expr "," CmpOps ")"
                | "Call" "(" Expr "," Exprs ")"
                | "Subscript" "(" Expr "," Index ")"

  syntax CmpOps ::= List{CmpOp, ","}
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"

  syntax Index ::= Expr | Slice
  syntax Bound ::= Expr | "NoBound"
  syntax Slice ::= "Slice" "(" Bound "," Bound "," Bound ")"
endmodule

module MPY-SEMANTIC
  imports MPY-SYNTAX
  imports BOOL
  imports INT
  imports STRING

  // A Python string is represented as a sequence of semantic characters.
  // Space has its own constructor; ch(S) represents a non-space character.
  syntax PString ::= ".PString"
                   | "sp" PString
                   | "ch" "(" String ")" PString

  syntax Val ::= pyStr(PString) | pyInt(Int) | pyBool(Bool)
  syntax Env ::= ".Env" | bind(String, Val, Env)
  syntax Funs ::= ".Funs" | fun(String, Params, Stmts, Funs)
  syntax Closure ::= closure(Params, Stmts)

  configuration
    <py>
      <k> $PGM:Program </k>
      <input> $INPUT:String </input>
      <env> .Env </env>
      <funs> .Funs </funs>
      <result> .K </result>
    </py>

  // Loading a translated module collects its definitions and invokes the
  // required HumanEval entry point on the command-line INPUT string.
  rule <k> Module(SS) => call("fix_spaces", pyStr(decode(INPUT))) </k>
       <input> INPUT </input>
       <funs> .Funs => collect(SS) </funs>

  rule <k> pyStr(S) => .K </k>
       <funs> _ => .Funs </funs>
       <result> .K => encode(S) </result>

  // Decode/encode connect concrete K String tokens to the structural string
  // model used by the semantics and by symbolic proofs.
  syntax PString ::= decode(String) [function]
  rule decode("") => .PString
  rule decode(S) => pconcat(decodeChar(substrString(S, 0, 1)), decode(substrString(S, 1, lengthString(S))))
    requires lengthString(S) >Int 0

  syntax PString ::= decodeChar(String) [function]
  rule decodeChar(" ") => sp .PString
  rule decodeChar(C) => ch(C) .PString [owise]

  syntax String ::= encode(PString) [function]
  rule encode(.PString) => ""
  rule encode(sp REST) => " " +String encode(REST)
  rule encode(ch(C) REST) => C +String encode(REST)

  // Definition collection and lexical lookup.
  syntax Funs ::= collect(Stmts) [function]
  rule collect(.Stmts) => .Funs
  rule collect(FuncDef(F, P, BODY) REST) => fun(F, P, BODY, collect(REST))

  syntax Closure ::= lookupFun(String, Funs) [function]
  rule lookupFun(F, fun(F, P, BODY, _REST)) => closure(P, BODY)
  rule lookupFun(F, fun(G, _P, _BODY, REST)) => lookupFun(F, REST)
    requires F =/=String G

  syntax Val ::= lookup(String, Env) [function]
  rule lookup(X, bind(X, V, _REST)) => V
  rule lookup(X, bind(Y, _V, REST)) => lookup(X, REST)
    requires X =/=String Y

  // Small-step evaluator.  Calls save the caller environment in a K
  // continuation, so recursive calls remain visible to circular proofs.
  syntax Val ::= pyLen(PString)
  syntax KItem ::= call(String, Val)
                 | enter(Closure, Val)
                 | finishCall(Env)
                 | exec(Stmts)
                 | choose(Stmts, Stmts, Stmts)
                 | eval(Expr)
                 | callArg(String)
                 | "lenResult"
                 | binRight(String, Expr)
                 | binApply(String, Val)
                 | cmpRight(String, Expr)
                 | cmpApply(String, Val)
                 | subApply(Index)
                 | decideEq(PString, PString)
                 | decideLonger(PString, Int)

  rule <k> call(F, V) => enter(lookupFun(F, FUNS), V) ...</k>
       <funs> FUNS </funs>
  rule <k> enter(closure(Params(X), BODY), V)
              => exec(BODY) ~> finishCall(OLD) ...</k>
       <env> OLD => bind(X, V, .Env) </env>
  rule <k> V:Val ~> finishCall(OLD) => V ...</k>
       <env> _ => OLD </env>

  syntax Stmts ::= sconcat(Stmts, Stmts) [function]
  rule sconcat(.Stmts, B) => B
  rule sconcat(S REST, B) => S sconcat(REST, B)

  rule <k> exec(Return(E) _REST) => eval(E) ...</k>
  rule <k> exec(If(COND, THEN, ELSE) REST)
              => eval(COND) ~> choose(THEN, ELSE, REST) ...</k>
  rule <k> pyBool(true) ~> choose(THEN, _ELSE, REST)
              => exec(sconcat(THEN, REST)) ...</k>
  rule <k> pyBool(false) ~> choose(_THEN, ELSE, REST)
              => exec(sconcat(ELSE, REST)) ...</k>

  // Expressions needed by solution.mpy.
  rule <k> eval(Name(X)) => lookup(X, ENV) ...</k> <env> ENV </env>
  rule <k> eval(Str(S)) => pyStr(decode(S)) ...</k>
  rule <k> eval(Int(I)) => pyInt(I) ...</k>

  rule <k> eval(BinOp(OP, L, R)) => eval(L) ~> binRight(OP, R) ...</k>
  rule <k> V:Val ~> binRight(OP, R) => eval(R) ~> binApply(OP, V) ...</k>
  rule <k> pyStr(B) ~> binApply("+", pyStr(A)) => pyStr(pconcat(A, B)) ...</k>

  rule <k> eval(Compare(L, CmpOp(OP, R)))
              => eval(L) ~> cmpRight(OP, R) ...</k>
  rule <k> V:Val ~> cmpRight(OP, R) => eval(R) ~> cmpApply(OP, V) ...</k>
  rule <k> pyStr(B) ~> cmpApply("==", pyStr(A)) => decideEq(A, B) ...</k>
  rule <k> pyInt(B) ~> cmpApply(">", pyInt(A)) => pyBool(A >Int B) ...</k>
  rule <k> pyInt(B) ~> cmpApply(">", pyLen(A)) => decideLonger(A, B) ...</k>

  rule <k> eval(Call(Name("len"), ARG)) => eval(ARG) ~> lenResult ...</k>
  rule <k> pyStr(S) ~> lenResult => pyLen(S) ...</k>
  rule <k> eval(Call(Name(F), ARG)) => eval(ARG) ~> callArg(F) ...</k>
    requires F =/=String "len"
  rule <k> V:Val ~> callArg(F) => call(F, V) ...</k>

  rule <k> eval(Subscript(BASE, INDEX)) => eval(BASE) ~> subApply(INDEX) ...</k>
  rule <k> pyStr(S) ~> subApply(Int(I)) => pyStr(pindex(S, I)) ...</k>
  rule <k> pyStr(S) ~> subApply(Slice(Int(L), NoBound, NoBound))
              => pyStr(pdrop(S, L)) ...</k>
  rule <k> pyStr(S) ~> subApply(Slice(Int(L), Int(U), NoBound))
              => pyStr(ptake(pdrop(S, L), U -Int L)) ...</k>

  // Equality and length comparison are machines rather than opaque functions.
  // Consequently the prover can split a symbolic PString by its constructors.
  rule <k> decideEq(.PString, .PString) => pyBool(true) ...</k>
  rule <k> decideEq(.PString, sp _B) => pyBool(false) ...</k>
  rule <k> decideEq(.PString, ch(_C) _B) => pyBool(false) ...</k>
  rule <k> decideEq(sp _A, .PString) => pyBool(false) ...</k>
  rule <k> decideEq(ch(_C) _A, .PString) => pyBool(false) ...</k>
  rule <k> decideEq(sp A, sp B) => decideEq(A, B) ...</k>
  rule <k> decideEq(sp _A, ch(_C) _B) => pyBool(false) ...</k>
  rule <k> decideEq(ch(_C) _A, sp _B) => pyBool(false) ...</k>
  rule <k> decideEq(ch(C) A, ch(C) B) => decideEq(A, B) ...</k>
  rule <k> decideEq(ch(C) _A, ch(D) _B) => pyBool(false) ...</k>
    requires C =/=String D

  rule <k> decideLonger(.PString, N) => pyBool(false) ...</k>
    requires N >=Int 0
  rule <k> decideLonger(sp _REST, 0) => pyBool(true) ...</k>
  rule <k> decideLonger(ch(_C) _REST, 0) => pyBool(true) ...</k>
  rule <k> decideLonger(sp REST, N) => decideLonger(REST, N -Int 1) ...</k>
    requires N >Int 0
  rule <k> decideLonger(ch(_C) REST, N) => decideLonger(REST, N -Int 1) ...</k>
    requires N >Int 0

  syntax PString ::= pconcat(PString, PString) [function]
  rule pconcat(.PString, B) => B
  rule pconcat(sp A, B) => sp pconcat(A, B)
  rule pconcat(ch(C) A, B) => ch(C) pconcat(A, B)

  syntax PString ::= pdrop(PString, Int) [function]
  rule pdrop(S, 0) => S
  rule pdrop(sp REST, N) => pdrop(REST, N -Int 1) requires N >Int 0
  rule pdrop(ch(_C) REST, N) => pdrop(REST, N -Int 1) requires N >Int 0

  syntax PString ::= ptake(PString, Int) [function]
  rule ptake(_S, 0) => .PString
  rule ptake(.PString, N) => .PString requires N >Int 0
  rule ptake(sp REST, N) => sp ptake(REST, N -Int 1) requires N >Int 0
  rule ptake(ch(C) REST, N) => ch(C) ptake(REST, N -Int 1) requires N >Int 0

  syntax PString ::= pindex(PString, Int) [function]
  rule pindex(sp _REST, 0) => sp .PString
  rule pindex(ch(C) _REST, 0) => ch(C) .PString
  rule pindex(sp REST, N) => pindex(REST, N -Int 1) requires N >Int 0
  rule pindex(ch(_C) REST, N) => pindex(REST, N -Int 1) requires N >Int 0
endmodule
