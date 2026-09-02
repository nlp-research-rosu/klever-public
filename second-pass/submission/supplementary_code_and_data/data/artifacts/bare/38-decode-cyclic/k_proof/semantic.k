requires "domains.md"

module MPY-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX

  syntax Py ::= "Module" "(" Stmts ")"

  syntax Stmts ::= List{Stmt, ""}
  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "Assign" "(" Expr "," Expr ")"
                | "While" "(" Expr "," Stmts ")"
                | "Return" "(" Expr ")"

  syntax Params ::= "Params" "(" String ")"

  syntax Expr ::= "Name" "(" String ")"
                | "Str" "(" String ")"
                | "Int" "(" Int ")"
                | "BinOp" "(" String "," Expr "," Expr ")"
                | "Compare" "(" Expr "," CmpOp ")"
                | "Call" "(" Expr "," Expr ")"
                | "Subscript" "(" Expr "," Index ")"

  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"
  syntax Index ::= Expr | Slice
  syntax Slice ::= "Slice" "(" Bound "," Bound "," Bound ")"
  syntax Bound ::= Expr | "NoBound"
endmodule

module MPY
  imports MPY-SYNTAX
  imports INT
  imports STRING
  imports BOOL
  imports MAP

  syntax Val ::= pyInt(Int) | pyStr(String) | pyBool(Bool)
  syntax Result ::= "noResult" | Val

  syntax KItem ::= run(Py, String)
                 | exec(Stmts)
                 | eval(Expr)
                 | store(String)
                 | binRight(String, Expr)
                 | binApply(String, Val)
                 | cmpRight(String, Expr)
                 | cmpApply(String, Val)
                 | "builtinLen"
                 | indexRight(Expr)
                 | indexApply(Val)
                 | sliceLower(Expr, Expr)
                 | sliceUpper(Expr, Val)
                 | sliceApply(String, Val)
                 | tailLower(Expr)
                 | tailApply(String)
                 | whileLoop(Expr, Stmts)
                 | whileGuard(Expr, Stmts)
                 | "doReturn"

  configuration
    <k> run($PGM:Py, $S:String) </k>
    <env> .Map </env>
    <result> noResult </result>

  rule <k> run(Module(FuncDef("decode_cyclic", Params("s"), BODY)), S)
        => exec(BODY) ... </k>
       <env> _ => "s" |-> pyStr(S) </env>

  rule <k> exec(.Stmts) => .K ... </k>
  rule <k> exec((STMT:Stmt) REST:Stmts) => STMT ~> exec(REST) ... </k>

  rule <k> Assign(Name(X), E) => eval(E) ~> store(X) ... </k>
  rule <k> V:Val ~> store(X) => .K ... </k>
       <env> ENV => ENV [ X <- V ] </env>

  rule <k> While(TEST, BODY) => whileLoop(TEST, BODY) ... </k>
  rule <k> whileLoop(TEST, BODY) => eval(TEST) ~> whileGuard(TEST, BODY) ... </k>
  rule <k> pyBool(true) ~> whileGuard(TEST, BODY)
        => exec(BODY) ~> whileLoop(TEST, BODY) ... </k>
  rule <k> pyBool(false) ~> whileGuard(_, _) => .K ... </k>

  rule <k> Return(E) => eval(E) ~> doReturn ... </k>
  rule <k> V:Val ~> doReturn ~> _REST => .K </k>
       <env> _ => .Map </env>
       <result> _ => V </result>

  rule <k> eval(Str(S)) => pyStr(S) ... </k>
  rule <k> eval(Int(I)) => pyInt(I) ... </k>
  rule <k> eval(Name(X)) => V ... </k>
       <env> ... X |-> V:Val ... </env>

  rule <k> eval(BinOp(OP, L, R)) => eval(L) ~> binRight(OP, R) ... </k>
  rule <k> V:Val ~> binRight(OP, R) => eval(R) ~> binApply(OP, V) ... </k>
  rule <k> pyInt(B) ~> binApply("+", pyInt(A)) => pyInt(A +Int B) ... </k>
  rule <k> pyStr(B) ~> binApply("+", pyStr(A)) => pyStr(A +String B) ... </k>

  rule <k> eval(Compare(L, CmpOp(OP, R)))
        => eval(L) ~> cmpRight(OP, R) ... </k>
  rule <k> V:Val ~> cmpRight(OP, R) => eval(R) ~> cmpApply(OP, V) ... </k>
  rule <k> pyInt(B) ~> cmpApply("<", pyInt(A)) => pyBool(true) ... </k>
       requires A <Int B
  rule <k> pyInt(B) ~> cmpApply("<", pyInt(A)) => pyBool(false) ... </k>
       requires A >=Int B

  rule <k> eval(Call(Name("len"), E)) => eval(E) ~> builtinLen ... </k>
  rule <k> pyStr(S) ~> builtinLen => pyInt(lengthString(S)) ... </k>

  rule <k> eval(Subscript(BASE, IDX:Expr))
        => eval(BASE) ~> indexRight(IDX) ... </k>
  rule <k> V:Val ~> indexRight(IDX) => eval(IDX) ~> indexApply(V) ... </k>
  rule <k> pyInt(I) ~> indexApply(pyStr(S))
        => pyStr(substrString(S, I, I +Int 1)) ... </k>
        requires 0 <=Int I andBool I <Int lengthString(S)

  rule <k> eval(Subscript(BASE, Slice(L:Expr, U:Expr, NoBound)))
        => eval(BASE) ~> sliceLower(L, U) ... </k>
  rule <k> pyStr(S) ~> sliceLower(L, U) => eval(L) ~> sliceUpper(U, pyStr(S)) ... </k>
  rule <k> LV:Val ~> sliceUpper(U, pyStr(S)) => eval(U) ~> sliceApply(S, LV) ... </k>
  rule <k> pyInt(U) ~> sliceApply(S, pyInt(L))
        => pyStr(substrString(S, L, U)) ... </k>
        requires 0 <=Int L andBool L <=Int U andBool U <=Int lengthString(S)

  rule <k> eval(Subscript(BASE, Slice(L:Expr, NoBound, NoBound)))
        => eval(BASE) ~> tailLower(L) ... </k>
  rule <k> pyStr(S) ~> tailLower(L) => eval(L) ~> tailApply(S) ... </k>
  rule <k> pyInt(L) ~> tailApply(S)
        => pyStr(substrString(S, L, lengthString(S))) ... </k>
        requires 0 <=Int L andBool L <=Int lengthString(S)

  // Named terms used by the proof to state the exact translated program and
  // its loop invariant without duplicating a large AST in every claim.
  syntax Py ::= "solutionProgram" [function, total]
  rule solutionProgram =>
    Module(
      FuncDef("decode_cyclic", Params("s"),
        Assign(Name("result"), Str(""))
        Assign(Name("i"), Int(0))
        While(Compare(
          BinOp("+", Name("i"), Int(2)),
          CmpOp("<", Call(Name("len"), Name("s")))),
          Assign(
            Name("result"),
            BinOp(
              "+",
              BinOp(
                "+",
                Name("result"),
                Subscript(Name("s"), BinOp("+", Name("i"), Int(2)))),
              Subscript(
                Name("s"),
                Slice(Name("i"), BinOp("+", Name("i"), Int(2)), NoBound))))
          Assign(Name("i"), BinOp("+", Name("i"), Int(3))))
        Return(
          BinOp(
            "+",
            Name("result"),
            Subscript(Name("s"), Slice(Name("i"), NoBound, NoBound))))))

  // Independent accumulator specification: consume complete 3-character
  // blocks by rotating each block right; append a short suffix unchanged.
  syntax String ::= decodeFrom(String, Int, String) [function]
  rule decodeFrom(S, I, ACC) =>
       decodeFrom(
         S,
         I +Int 3,
         ACC
           +String substrString(S, I +Int 2, I +Int 3)
           +String substrString(S, I, I +Int 2))
       requires 0 <=Int I
        andBool I +Int 2 <Int lengthString(S)

  rule decodeFrom(S, I, ACC) =>
       ACC +String substrString(S, I, lengthString(S))
       requires 0 <=Int I
        andBool I <=Int lengthString(S)
        andBool I +Int 2 >=Int lengthString(S)

  syntax Stmts ::= "decodeBody" [function, total]
  rule decodeBody =>
    Assign(
      Name("result"),
      BinOp(
        "+",
        BinOp(
          "+",
          Name("result"),
          Subscript(Name("s"), BinOp("+", Name("i"), Int(2)))),
        Subscript(
          Name("s"),
          Slice(Name("i"), BinOp("+", Name("i"), Int(2)), NoBound))))
    Assign(Name("i"), BinOp("+", Name("i"), Int(3)))

  syntax Expr ::= "decodeTest" [function, total]
  rule decodeTest =>
    Compare(
      BinOp("+", Name("i"), Int(2)),
      CmpOp("<", Call(Name("len"), Name("s"))))

  syntax Stmts ::= "decodeReturn" [function, total]
  rule decodeReturn =>
    Return(
      BinOp(
        "+",
        Name("result"),
        Subscript(Name("s"), Slice(Name("i"), NoBound, NoBound))))
endmodule
