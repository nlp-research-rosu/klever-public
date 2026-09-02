requires "verification.k"

module MPY-SYNTAX
  imports BOOL-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX

  // The constructor language emitted by py2mpy.py (restricted here to the
  // nodes used by solution.mpy).
  syntax Module ::= "Module" "(" Stmts ")"                 [symbol]
  syntax Stmts ::= List{Stmt, ""}
  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")" [symbol]
                | "Assign" "(" Expr "," Expr ")"            [symbol]
                | "If" "(" Expr "," Stmts "," Stmts ")"     [symbol]
                | "Return" "(" Expr ")"                     [symbol]
  syntax Params ::= "Params" "(" ParamNames ")"             [symbol]
  syntax ParamNames ::= List{String, ","}

  syntax Expr ::= "Name" "(" String ")"                     [symbol]
                | "Str" "(" String ")"                      [symbol]
                | "Int" "(" Int ")"                         [symbol]
                | "Call" "(" Expr "," Exprs ")"            [symbol]
                | "Compare" "(" Expr "," CmpOps ")"        [symbol]
                | "CmpOp" "(" String "," Expr ")"          [symbol]
                | "UnaryOp" "(" String "," Expr ")"        [symbol]
                | "Subscript" "(" Expr "," Index ")"       [symbol]
  syntax Exprs ::= List{Expr, ","}
  syntax CmpOps ::= List{Expr, ","}
  syntax Index ::= Expr | Slice
  syntax Slice ::= "Slice" "(" Bound "," Bound "," Bound ")" [symbol]
  syntax Bound ::= Expr | "NoBound"                           [symbol]

  // Runtime values.  Chars is a snoc-list, making Python's negative string
  // indices and removal of the last character structural operations.
  syntax Vowel ::= "v_a" | "v_e" | "v_i" | "v_o" | "v_u"
                 | "v_A" | "v_E" | "v_I" | "v_O" | "v_U"
  syntax Char ::= "vow" "(" Vowel ")" | "con" "(" String ")"
  syntax Chars ::= ".Chars" | "snoc" "(" Chars "," Char ")"
  syntax Nat ::= "z" | "s" "(" Nat ")"
  syntax Val ::= "pyStr" "(" Chars ")"
               | "pyNat" "(" Nat ")"
               | "pyNeg" "(" Nat ")"
               | "pyBool" "(" Bool ")"
               | "vowelSet"
               | "word" "(" String ")"
endmodule

module MPY
  imports MPY-SYNTAX
  imports VERIFICATION
  imports BOOL
  imports INT
  imports STRING
  imports MAP

  configuration
    <T>
      <k> start($ARG:Val) </k>
      <program> $PGM:Module </program>
      <env> .Map </env>
      <stack> .Frames </stack>
    </T>

  syntax KItem ::= "start" "(" Val ")"
                 | "invoke" "(" String "," Val ")"
                 | "execMachine" "(" Stmts ")"
                 | "doStmt" "(" Stmt ")"
                 | "returning" "(" Expr ")"
                 | "branch" "(" Bool "," Stmts "," Stmts ")"
                 | "lenBranch" "(" Chars "," Stmts "," Stmts ")"
                 | "memberBranch" "(" String "," Val "," Stmts "," Stmts ")"
                 | "callResult" "(" Val ")"
                 | "tailReturn"
                 | "unwrap"
  syntax Frame ::= "frame" "(" K "," Map ")"
  syntax Frames ::= ".Frames" | "push" "(" Frame "," Frames ")"
  syntax KItem ::= Frame
  syntax ExecResult ::= "normal" "(" Map ")" | "returned" "(" Val ")"

  syntax Val ::= normalize(Val)                              [function]
  rule normalize(word(S)) => pyStr(litChars(S))
  rule normalize(V:Val) => V                                 [owise]

  rule <k> start(V) => invoke("get_closest_vowel", normalize(V)) ~> unwrap ... </k>

  // Explicit call states expose recursive calls to kprove.  A frame records
  // the caller continuation and environment; reaching a value restores both.
  rule <k> invoke(F, V) ~> K => execMachine(functionBody(M, F)) </k>
       <program> M </program>
       <env> ENV => functionEnv(M, F, V) </env>
       <stack> STACK => push(frame(K, ENV), STACK) </stack>

  rule <k> V:Val => callResult(V) ~> K </k>
       <env> _ENV => OLDENV </env>
       <stack> push(frame(K, OLDENV), REST) => REST </stack>
  rule callResult(V) ~> tailReturn => V
  rule callResult(V) ~> unwrap => V

  rule execMachine(.Stmts) => .K
  rule execMachine(S:Stmt REST:Stmts) => doStmt(S) ~> execMachine(REST)
  rule <k> doStmt(Assign(Name(X), E)) => .K ... </k>
       <program> M </program>
       <env> ENV => ENV [ X <- eval(E, ENV, M) ] </env>
  rule <k> doStmt(If(Compare(Call(Name("len"), Name(X), .Exprs),
                              CmpOp("<", Int(3)), .CmpOps), THEN, ELSE))
            => lenBranch(asChars(lookupVal(ENV, X)), THEN, ELSE) ... </k>
       <env> ENV </env>
  rule lenBranch(.Chars, THEN, ELSE) => execMachine(THEN)
  rule lenBranch(snoc(.Chars, A), THEN, ELSE) => execMachine(THEN)
  rule lenBranch(snoc(snoc(.Chars, A), B), THEN, ELSE) => execMachine(THEN)
  rule lenBranch(snoc(snoc(snoc(P, A), B), C), THEN, ELSE)
    => execMachine(ELSE)
  rule <k> doStmt(If(Compare(L, CmpOp(OP, Name("vowels")), .CmpOps),
                              THEN, ELSE))
            => memberBranch(OP, eval(L, ENV, M), THEN, ELSE) ... </k>
       <program> M </program>
       <env> ENV </env>
  rule memberBranch("in", pyStr(snoc(.Chars, vow(V:Vowel))), THEN, ELSE)
    => execMachine(THEN)
  rule memberBranch("in", pyStr(snoc(.Chars, con(S))), THEN, ELSE)
    => execMachine(ELSE)
  rule memberBranch("not in", pyStr(snoc(.Chars, vow(V:Vowel))), THEN, ELSE)
    => execMachine(ELSE)
  rule memberBranch("not in", pyStr(snoc(.Chars, con(S))), THEN, ELSE)
    => execMachine(THEN)
  rule <k> doStmt(If(COND, THEN, ELSE))
            => branch(asBool(eval(COND, ENV, M)), THEN, ELSE) ... </k>
       <program> M </program>
       <env> ENV </env> [owise]
  rule branch(true, THEN, ELSE) => execMachine(THEN)
  rule branch(false, THEN, ELSE) => execMachine(ELSE)
  rule <k> doStmt(Return(E)) ~> _REST => returning(E) </k>
  rule <k> returning(Call(Name(F), A:Expr, .Exprs))
            => invoke(F, eval(A, ENV, M)) ~> tailReturn ... </k>
       <program> M </program>
       <env> ENV </env>
  rule <k> returning(E) => eval(E, ENV, M) ... </k>
       <program> M </program>
       <env> ENV </env> [owise]

  // Big-step helpers give meaning to pure expressions and are also useful as
  // an executable reference layer.  Program calls in Return are handled by
  // the explicit machine rule above.
  syntax Val ::= call(Module, String, Val)                    [function]
  rule call(M:Module, F,
            V) => returnValue(exec(functionBody(M, F),
                                    functionEnv(M, F, V), M))

  syntax Stmts ::= functionBody(Module, String)               [function]
  rule functionBody(Module(FuncDef(F, Params(X:String, .ParamNames), BODY)), F)
    => BODY

  syntax Map ::= functionEnv(Module, String, Val)             [function]
  rule functionEnv(Module(FuncDef(F, Params(X:String, .ParamNames), BODY)), F, V)
    => X |-> V

  syntax Val ::= returnValue(ExecResult)                      [function]
  rule returnValue(returned(V)) => V

  syntax ExecResult ::= exec(Stmts, Map, Module)              [function]
                      | execRest(ExecResult, Stmts, Module)   [function]
                      | execStmt(Stmt, Map, Module)           [function]
                      | choose(Bool, Stmts, Stmts, Map, Module) [function]
  rule exec(.Stmts, ENV, M) => normal(ENV)
  rule exec(S:Stmt REST:Stmts, ENV, M)
    => execRest(execStmt(S, ENV, M), REST, M)
  rule execRest(normal(ENV), REST, M) => exec(REST, ENV, M)
  rule execRest(returned(V), REST, M) => returned(V)

  rule execStmt(Assign(Name(X), E), ENV, M)
    => normal(ENV [ X <- eval(E, ENV, M) ])
  rule execStmt(If(COND, THEN, ELSE), ENV, M)
    => choose(asBool(eval(COND, ENV, M)), THEN, ELSE, ENV, M)
  rule execStmt(Return(E), ENV, M) => returned(eval(E, ENV, M))
  rule choose(true,  THEN, ELSE, ENV, M) => exec(THEN, ENV, M)
  rule choose(false, THEN, ELSE, ENV, M) => exec(ELSE, ENV, M)

  // Expressions needed by the submitted Python program.
  syntax Val ::= eval(Expr, Map, Module)                       [function]
               | evalCompare(String, Val, Val)                [function]
               | evalUnary(String, Val)                       [function]
               | evalIndex(Val, Val)                          [function]
               | evalSliceLast(Val)                           [function]
  syntax Bool ::= asBool(Val)                                 [function]

  syntax Val ::= lookupVal(Map, String)                        [function]
  rule lookupVal((X |-> V:Val) REST, X) => V
  rule eval(Name(X), ENV, M) => lookupVal(ENV, X)
  rule eval(Str("aeiouAEIOU"), ENV, M) => vowelSet
  rule eval(Str(S), ENV, M) => pyStr(litChars(S))
    requires S =/=String "aeiouAEIOU"
  rule eval(Int(I), ENV, M) => pyNat(intNat(I)) requires I >=Int 0
  rule eval(Call(Name("len"), A:Expr, .Exprs), ENV, M)
    => pyNat(lenChars(asChars(eval(A, ENV, M))))
  rule eval(Call(Name(F), A:Expr, .Exprs), ENV, M)
    => call(M, F, eval(A, ENV, M)) requires F =/=String "len"
  rule eval(Compare(L, CmpOp(OP, R), .CmpOps), ENV, M)
    => evalCompare(OP, eval(L, ENV, M), eval(R, ENV, M))
  rule eval(UnaryOp(OP, E), ENV, M) => evalUnary(OP, eval(E, ENV, M))
  rule eval(Subscript(S, I:Expr), ENV, M)
    => evalIndex(eval(S, ENV, M), eval(I, ENV, M))
  rule eval(Subscript(S, Slice(NoBound, UnaryOp("-", Int(1)), NoBound)), ENV, M)
    => evalSliceLast(eval(S, ENV, M))

  rule evalCompare("<", pyNat(A), pyNat(B)) => pyBool(natLt(A, B))
  rule evalCompare("in", pyStr(snoc(.Chars, C)), vowelSet)
    => pyBool(isVowelChar(C))
  rule evalCompare("not in", pyStr(snoc(.Chars, C)), vowelSet)
    => pyBool(notBool isVowelChar(C))
  rule evalUnary("-", pyNat(N)) => pyNeg(N)
  rule evalIndex(pyStr(CS), pyNeg(N)) => fromEnd(CS, N)
  rule evalSliceLast(pyStr(snoc(CS, C))) => pyStr(CS)
  rule asBool(pyBool(B)) => B

  // Literal conversion is part of the semantics, not the Python-to-AST
  // translator.  Inputs supplied as word("...") use this same conversion.
  syntax Chars ::= litChars(String)                            [function]
  syntax Char ::= litChar(String)                             [function]
  rule litChars("") => .Chars
  rule litChars(S) => snoc(litChars(substrString(S, 0,
                                  lengthString(S) -Int 1)),
                            litChar(substrString(S, lengthString(S) -Int 1,
                                                   lengthString(S))))
    requires lengthString(S) >Int 0
  rule litChar("a") => vow(v_a)
  rule litChar("e") => vow(v_e)
  rule litChar("i") => vow(v_i)
  rule litChar("o") => vow(v_o)
  rule litChar("u") => vow(v_u)
  rule litChar("A") => vow(v_A)
  rule litChar("E") => vow(v_E)
  rule litChar("I") => vow(v_I)
  rule litChar("O") => vow(v_O)
  rule litChar("U") => vow(v_U)
  rule litChar(S) => con(S)                                  [owise]

  syntax Nat ::= intNat(Int)                                  [function]
  syntax Nat ::= lenChars(Chars)                              [function]
  rule intNat(0) => z
  rule intNat(1) => s(z)
  rule intNat(2) => s(s(z))
  rule intNat(3) => s(s(s(z)))
  rule intNat(I) => s(intNat(I -Int 1)) requires I >Int 0
  rule lenChars(.Chars) => z
  rule lenChars(snoc(CS, C)) => s(lenChars(CS))

  syntax Chars ::= asChars(Val)                               [function]
  rule asChars(pyStr(CS)) => CS

  syntax Bool ::= natLt(Nat, Nat)                             [function]
  rule natLt(A, z) => false
  rule natLt(z, s(B)) => true
  rule natLt(s(A), s(B)) => natLt(A, B)

  syntax Val ::= fromEnd(Chars, Nat)                          [function]
  rule fromEnd(snoc(CS, C), s(z)) => pyStr(snoc(.Chars, C))
  rule fromEnd(snoc(CS, C), s(s(N))) => fromEnd(CS, s(N))

  syntax Bool ::= isVowelChar(Char)                           [function]
  rule isVowelChar(vow(V:Vowel)) => true
  rule isVowelChar(con(S)) => false
endmodule
