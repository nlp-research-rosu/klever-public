requires "verification.k"

module MPY-SYNTAX
  imports DOMAINS

  syntax Module ::= "Module" "(" Stmts ")" [symbol]
  syntax Stmts ::= List{Stmt, ""} [symbol]

  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")" [symbol]
                | "Return" "(" Expr ")" [symbol]
                | "If" "(" Expr "," Stmts "," Stmts ")" [symbol]

  syntax Params ::= "Params" "(" String ")" [symbol]

  syntax Expr ::= "Name" "(" String ")" [symbol]
                | "Str" "(" String ")" [symbol]
                | "Int" "(" Int ")" [symbol]
                | "UnaryOp" "(" String "," Expr ")" [symbol]
                | "BinOp" "(" String "," Expr "," Expr ")" [symbol]
                | "Compare" "(" Expr "," CmpOp ")" [symbol]
                | "Subscript" "(" Expr "," Expr ")" [symbol]
                | "Slice" "(" Bound "," Bound "," Bound ")" [symbol]
                | "Call" "(" Expr "," Expr ")" [symbol]

  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")" [symbol]
  syntax Bound ::= Expr | "NoBound" [symbol]
endmodule

module SOLUTION-AST
  imports MPY-SYNTAX

  // This is the parsed solution.mpy term used by proof claims.  The executable
  // krun commands still parse solution.mpy directly from disk.
  syntax Module ::= "#solution" [function]
  rule #solution =>
    Module(
      FuncDef("is_palindrome", Params("string"),
        Return(
          Compare(
            Name("string"),
            CmpOp("==",
              Subscript(
                Name("string"),
                Slice(NoBound, NoBound, UnaryOp("-", Int(1))))))))
      FuncDef("make_palindrome", Params("string"),
        If(Call(Name("is_palindrome"), Name("string")),
          Return(Name("string")),
          .Stmts)
        Return(
          BinOp("+",
            BinOp("+",
              Subscript(Name("string"), Int(0)),
              Call(
                Name("make_palindrome"),
                Subscript(
                  Name("string"),
                  Slice(Int(1), NoBound, NoBound)))),
            Subscript(Name("string"), Int(0))))))
endmodule

module MPY-SEMANTICS
  imports MPY-SYNTAX
  imports SOLUTION-AST
  imports BOOL
  imports INT
  imports STRING

  syntax Val ::= "strVal" "(" String ")" [symbol]
               | "boolVal" "(" Bool ")" [symbol]
               | "intVal" "(" Int ")" [symbol]

  syntax Env ::= "env" "(" String "," Val ")" [symbol]
  syntax Function ::= "function" "(" String "," Stmts ")" [symbol]
  syntax Outcome ::= "normal" [symbol]
                   | "returned" "(" Val ")" [symbol]

  syntax KItem ::= "#run" "(" Module "," String ")" [symbol]
                 | "#runFunction" "(" String "," Module "," String ")" [symbol]
  syntax Function ::= "#lookup" "(" String "," Stmts ")" [function]
  syntax Val ::= "#call" "(" String "," Val "," Module ")" [function]
               | "#apply" "(" Function "," Val "," Module ")" [function]
               | "#eval" "(" Expr "," Env "," Module ")" [function]
  syntax Outcome ::= "#exec" "(" Stmts "," Env "," Module ")" [function]
                   | "#resume" "(" Outcome "," Stmts "," Env "," Module ")" [function]
  syntax Stmts ::= "#branch" "(" Val "," Stmts "," Stmts ")" [function, total]
  syntax Bool ::= "#valueEq" "(" Val "," Val ")" [function]
  syntax String ::= "#reverse" "(" String ")" [function, total]

  configuration
    <mpy>
      <k> #run($PGM:Module, $INPUT:String) </k>
      <program> $PGM:Module </program>
      <input> $INPUT:String </input>
      <ast-match> $PGM:Module ==K #solution </ast-match>
      <result> .K </result>
    </mpy>

  rule <k> #run(P, S) => .K ... </k>
       <result> .K => #call("make_palindrome", strVal(S), P) </result>
  rule <k> #runFunction(F, P, S) => .K ... </k>
       <result> .K => #call(F, strVal(S), P) </result>

  rule #lookup(F, FuncDef(F, Params(X), BODY) REST)
    => function(X, BODY)
  rule #lookup(F, FuncDef(G, PARAMS, BODY) REST)
    => #lookup(F, REST)
    requires F =/=String G

  rule #call(F, V, Module(DEFS))
    => #apply(#lookup(F, DEFS), V, Module(DEFS))
  rule #apply(function(X, BODY), V, P)
    => #outcomeValue(#exec(BODY, env(X, V), P))

  syntax Val ::= "#outcomeValue" "(" Outcome ")" [function]
  rule #outcomeValue(returned(V)) => V

  rule #exec(.Stmts, ENV, P) => normal
  rule #exec(Return(E) REST, ENV, P) => returned(#eval(E, ENV, P))
  rule #exec(If(COND, THEN, ELSE) REST, ENV, P)
    => #resume(
         #exec(#branch(#eval(COND, ENV, P), THEN, ELSE), ENV, P),
         REST, ENV, P)
  rule #resume(returned(V), REST, ENV, P) => returned(V)
  rule #resume(normal, REST, ENV, P) => #exec(REST, ENV, P)

  rule #branch(boolVal(B), THEN, ELSE) => THEN
    requires B
  rule #branch(boolVal(B), THEN, ELSE) => ELSE
    requires notBool B

  rule #eval(Name(X), env(X, V), P) => V
  rule #eval(Str(S), ENV, P) => strVal(S)
  rule #eval(Int(I), ENV, P) => intVal(I)
  rule #eval(UnaryOp("-", E), ENV, P)
    => #negate(#eval(E, ENV, P))
  rule #eval(BinOp("+", LEFT, RIGHT), ENV, P)
    => #add(#eval(LEFT, ENV, P), #eval(RIGHT, ENV, P))
  rule #eval(Compare(LEFT, CmpOp("==", RIGHT)), ENV, P)
    => boolVal(#valueEq(#eval(LEFT, ENV, P), #eval(RIGHT, ENV, P)))
  rule #eval(Subscript(BASE, Int(0)), ENV, P)
    => #indexZero(#eval(BASE, ENV, P))
  rule #eval(Subscript(BASE, Slice(Int(1), NoBound, NoBound)), ENV, P)
    => #tail(#eval(BASE, ENV, P))
  rule #eval(Subscript(BASE, Slice(NoBound, NoBound,
                                  UnaryOp("-", Int(1)))), ENV, P)
    => #reversed(#eval(BASE, ENV, P))
  rule #eval(Call(Name(F), ARG), ENV, P)
    => #call(F, #eval(ARG, ENV, P), P)

  syntax Val ::= "#negate" "(" Val ")" [function]
               | "#add" "(" Val "," Val ")" [function]
               | "#indexZero" "(" Val ")" [function]
               | "#tail" "(" Val ")" [function]
               | "#reversed" "(" Val ")" [function]
  rule #negate(intVal(I)) => intVal(0 -Int I)
  rule #add(strVal(S1), strVal(S2)) => strVal(S1 +String S2)
  rule #indexZero(strVal(S)) => strVal(substrString(S, 0, 1))
    requires lengthString(S) >Int 0
  rule #tail(strVal(S)) => strVal(substrString(S, 1, lengthString(S)))
    requires lengthString(S) >Int 0
  rule #reversed(strVal(S)) => strVal(#reverse(S))

  rule #valueEq(strVal(S1), strVal(S2)) => S1 ==String S2

  rule #reverse("") => ""
  rule #reverse(S)
    => substrString(S, lengthString(S) -Int 1, lengthString(S))
       +String #reverse(substrString(S, 0, lengthString(S) -Int 1))
    requires lengthString(S) >Int 0
endmodule

module EXECUTION
  imports MPY-SEMANTICS
endmodule

module SEMANTIC
  imports MPY-SEMANTICS
  imports VERIFICATION
endmodule
