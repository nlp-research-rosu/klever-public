module MPY-SYNTAX
  imports DOMAINS

  syntax Ids    ::= List{String, ","}
  syntax Exprs  ::= List{Expr, ","}
  syntax Stmts  ::= List{Stmt, ""}

  syntax Params ::= "Params" "(" Ids ")"

  syntax Expr ::= "Name"      "(" String ")"
                | "Str"       "(" String ")"
                | "Int"       "(" Int ")"
                | "Attribute" "(" Expr "," String ")"
                | "Call"      "(" Expr "," Exprs ")"
                | "BinOp"     "(" String "," Expr "," Expr ")"

  syntax Stmt ::= "Return"  "(" Expr ")"
                | "FuncDef" "(" String "," Params "," Stmts ")"

  syntax Program ::= "Module" "(" Stmts ")"

  syntax Val ::= VStr(String) | VInt(Int)
  syntax KItem ::= invoke(String)
endmodule

module MPY
  imports MPY-SYNTAX

  configuration <k> $PGM:Program ~> invoke($ARG:String) </k>

  syntax Val ::= evalProgram(Program, String) [function]
  syntax Val ::= eval(Expr, String)            [function]
  syntax Val ::= addVals(Val, Val)             [function]
  syntax Val ::= multiplyVals(Val, Val)        [function]
  syntax Val ::= countVal(Val, String)         [function]
  syntax Val ::= stripVal(Val)                 [function]

  // This condition's Python subset only needs one top-level, one-argument
  // function whose body is a return.  Expressions below are compositional.
  rule evalProgram(
         Module(FuncDef("sort_numbers", Params("numbers"), Return(E))),
         S
       ) => eval(E, S)

  rule eval(Name("numbers"), S) => VStr(S)
  rule eval(Str(S), _)           => VStr(S)
  rule eval(Int(I), _)           => VInt(I)

  rule eval(BinOp("+", E1, E2), S)
    => addVals(eval(E1, S), eval(E2, S))
  rule eval(BinOp("*", E1, E2), S)
    => multiplyVals(eval(E1, S), eval(E2, S))

  rule eval(Call(Attribute(E, "count"), Str(Needle)), S)
    => countVal(eval(E, S), Needle)
  rule eval(Call(Attribute(E, "strip"), .Exprs), S)
    => stripVal(eval(E, S))

  rule addVals(VStr(S1), VStr(S2)) => VStr(S1 +String S2)
  rule multiplyVals(VStr(S), VInt(N)) => VStr(repeatString(S, N))
  rule countVal(VStr(S), Needle) => VInt(countAllOccurrences(S, Needle))
  rule stripVal(VStr(S)) => VStr(trimTrailingSpace(S))

  // Concrete helpers for the two Python string operations not directly
  // hooked by K.  The value passed to strip is produced by concatenating
  // zero or more "word " blocks, so removing its one trailing space is exact.
  syntax String ::= repeatString(String, Int) [function]
  rule repeatString(_, N) => ""
    requires N <=Int 0
    [concrete(N), simplification]
  rule repeatString(S, N) => S +String repeatString(S, N -Int 1)
    requires N >Int 0
    [concrete(N), simplification]

  syntax String ::= trimTrailingSpace(String) [function]
  rule trimTrailingSpace("") => ""
  rule trimTrailingSpace(S)
    => substrString(S, 0, lengthString(S) -Int 1)
    requires lengthString(S) >Int 0
    [concrete(S), simplification]

  rule <k> P:Program ~> invoke(S) => evalProgram(P, S) ... </k>
endmodule
