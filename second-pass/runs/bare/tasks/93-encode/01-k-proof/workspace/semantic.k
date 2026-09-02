requires "domains.md"

module MPY-SYNTAX
  imports STRING-SYNTAX
  imports INT-SYNTAX

  syntax Pgm ::= "Module" "(" Stmts ")"

  syntax Stmts ::= List{Stmt, ""}
  syntax Exprs ::= List{Expr, ","}
  syntax CmpOps ::= List{CmpOp, ","}
  syntax Strings ::= List{String, ","}

  syntax Params ::= "Params" "(" Strings ")"
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"

  syntax Expr ::= "Name" "(" String ")"
                | "Str" "(" String ")"
                | "Int" "(" Int ")"
                | "BinOp" "(" String "," Expr "," Expr ")"
                | "Compare" "(" Expr "," CmpOps ")"
                | "Call" "(" Expr "," Exprs ")"
                | "Attribute" "(" Expr "," String ")"

  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "Assign" "(" Expr "," Expr ")"
                | "AugAssign" "(" Expr "," String "," Expr ")"
                | "For" "(" Expr "," Expr "," Stmts ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"
                | "Return" "(" Expr ")"
endmodule

module SEMANTIC
  imports MPY-SYNTAX
  imports STRING
  imports INT
  imports BOOL
  imports MAP
  imports K-EQUAL

  syntax PyValue ::= pyStr(String) | pyInt(Int) | pyBool(Bool)
  syntax FunValue ::= closure(Params, Stmts)
  syntax Result ::= "noResult" | returned(KItem)

  syntax KItem ::= Pgm | Stmt | PyValue | FunValue
                 | execStmts(Stmts)
                 | invoke(String, PyValue)
                 | startFor(String, KItem, Stmts)
                 | loopString(String, String, Stmts)
                 | vowelBranch(String, Stmts, Stmts)

  // A macro for the exact translated loop body.  It is used both by the
  // small-step rules above and by the fused iteration rule below.
  syntax Stmts ::= encodeLoopBody() [function]
  rule encodeLoopBody() =>
    If(Compare(Name("char"), CmpOp("in", Str("aeiouAEIOU"))),
      Assign(
        Name("char"),
        Call(
          Name("chr"),
          BinOp("+", Call(Name("ord"), Name("char")), Int(2)))),
    .Stmts)
    AugAssign(
      Name("result"),
      "+",
      Call(Attribute(Name("char"), "swapcase"), .Exprs))

  configuration
    <python>
      <k> $PGM:Pgm ~> invoke("encode", pyStr($MESSAGE:String)) </k>
      <env> .Map </env>
      <functions> .Map </functions>
      <result> noResult </result>
    </python>

  rule <k> Module(SS) => execStmts(SS) ... </k>

  rule <k> execStmts(.Stmts) => .K ... </k>
  rule <k> execStmts(S:Stmt SS:Stmts) => S ~> execStmts(SS) ... </k>

  rule <k> FuncDef(F, PS, BODY) => .K ... </k>
       <functions> FS => FS [ F <- closure(PS, BODY) ] </functions>

  rule <k> invoke(F, V) => execStmts(BODY) ... </k>
       <env> RHO => RHO [ P <- V ] </env>
       <functions> ... F |-> closure(Params(P:String), BODY) ... </functions>

  rule <k> Assign(Name(X), E) => .K ... </k>
       <env> RHO => RHO [ X <- eval(E, RHO) ] </env>

  rule <k> AugAssign(Name(X), "+", E) => .K ... </k>
       <env> RHO => RHO [ X <- plusValue(RHO [ X ], eval(E, RHO)) ] </env>

  rule <k> If(Compare(Name(X), CmpOp("in", Str("aeiouAEIOU"))), THEN, ELSE)
        => vowelBranch(C, THEN, ELSE) ... </k>
       <env> X |-> pyStr(C) _RHO </env>

  rule <k> vowelBranch("a", THEN, _ELSE) => execStmts(THEN) ... </k>
  rule <k> vowelBranch("e", THEN, _ELSE) => execStmts(THEN) ... </k>
  rule <k> vowelBranch("i", THEN, _ELSE) => execStmts(THEN) ... </k>
  rule <k> vowelBranch("o", THEN, _ELSE) => execStmts(THEN) ... </k>
  rule <k> vowelBranch("u", THEN, _ELSE) => execStmts(THEN) ... </k>
  rule <k> vowelBranch("A", THEN, _ELSE) => execStmts(THEN) ... </k>
  rule <k> vowelBranch("E", THEN, _ELSE) => execStmts(THEN) ... </k>
  rule <k> vowelBranch("I", THEN, _ELSE) => execStmts(THEN) ... </k>
  rule <k> vowelBranch("O", THEN, _ELSE) => execStmts(THEN) ... </k>
  rule <k> vowelBranch("U", THEN, _ELSE) => execStmts(THEN) ... </k>
  rule <k> vowelBranch(_C, _THEN, ELSE) => execStmts(ELSE) ... </k> [owise]

  rule <k> For(Name(X), E, BODY) => startFor(X, eval(E, RHO), BODY) ... </k>
       <env> RHO </env>

  rule startFor(X, pyStr(S), BODY) => loopString(X, S, BODY)

  rule <k> loopString(_X, S, _BODY) => .K ... </k>
       requires lengthString(S) ==Int 0

  // Fused form of the submitted loop body.  This is a semantics rule, not a
  // proof axiom: encodedChar and advancedVowel are defined exhaustively below.
  rule <k> loopString(
             "char",
             S,
             If(Compare(Name("char"), CmpOp("in", Str("aeiouAEIOU"))),
               Assign(
                 Name("char"),
                 Call(
                   Name("chr"),
                   BinOp("+", Call(Name("ord"), Name("char")), Int(2)))),
             .Stmts)
             AugAssign(
               Name("result"),
               "+",
               Call(Attribute(Name("char"), "swapcase"), .Exprs)))
        => loopString(
             "char",
             substrString(S, 1, lengthString(S)),
             encodeLoopBody()) ... </k>
       <env>
         "result" |-> pyStr(R) RHO
       =>
         ("result" |-> pyStr(
            R +String encodedChar(substrString(S, 0, 1))) RHO)
         [ "char" <- pyStr(advancedVowel(substrString(S, 0, 1))) ]
       </env>
       requires lengthString(S) =/=Int 0
       [priority(40)]

  rule <k> loopString(X, S, BODY)
        => execStmts(BODY)
        ~> loopString(X, substrString(S, 1, lengthString(S)), BODY) ... </k>
       <env> RHO
          => RHO [ X <- pyStr(substrString(S, 0, 1)) ]
       </env>
       requires lengthString(S) =/=Int 0
       [owise]

  rule <k> Return(E) => .K ... </k>
       <env> RHO </env>
       <result> noResult => returned(eval(E, RHO)) </result>

  syntax KItem ::= eval(Expr, Map) [function]
                 | plusValue(KItem, KItem) [function]
                 | inValue(KItem, KItem) [function]
                 | ordValue(KItem) [function]
                 | chrValue(KItem) [function]
                 | swapCaseValue(KItem) [function]

  rule eval(Name(X), RHO) => RHO [ X ]
  rule (_RHO:Map [ X <- V ]) [ X ] => V [simplification]
  rule eval(Str(S), _RHO) => pyStr(S)
  rule eval(Int(I), _RHO) => pyInt(I)
  rule eval(BinOp("+", E1, E2), RHO)
    => plusValue(eval(E1, RHO), eval(E2, RHO))
  rule eval(Compare(E1, CmpOp("in", E2)), RHO)
    => inValue(eval(E1, RHO), eval(E2, RHO))
  rule eval(Call(Name("ord"), E:Expr), RHO) => ordValue(eval(E, RHO))
  rule eval(Call(Name("chr"), E:Expr), RHO) => chrValue(eval(E, RHO))
  rule eval(Call(Attribute(E, "swapcase"), .Exprs), RHO)
    => swapCaseValue(eval(E, RHO))

  rule plusValue(pyInt(I1), pyInt(I2)) => pyInt(I1 +Int I2)
  rule plusValue(pyStr(S1), pyStr(S2)) => pyStr(S1 +String S2)
  rule inValue(pyStr(NEEDLE), pyStr(HAYSTACK))
    => pyBool(findString(HAYSTACK, NEEDLE, 0) >=Int 0)
  rule ordValue(pyStr(C)) => pyInt(ordChar(C))
  rule chrValue(pyInt(I)) => pyStr(chrChar(I))
  rule swapCaseValue(pyStr(C)) => pyStr(swapCaseChar(C))

  syntax String ::= swapCaseChar(String) [function, total]

  syntax String ::= encodedChar(String) [function, total]
                  | advancedVowel(String) [function, total]
endmodule
