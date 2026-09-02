requires "domains.md"

module MPY-SYNTAX
  imports DOMAINS

  syntax Program ::= "Module" "(" Stmts ")"

  syntax Stmts ::= List{Stmt, ""}
  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "Return" "(" Expr ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"

  syntax Params ::= "Params" "(" String ")"

  syntax Expr ::= "Name" "(" String ")"
                | "Int" "(" Int ")"
                | "Str" "(" String ")"
                | "Call" "(" Expr "," Expr ")"
                | "Compare" "(" Expr "," CmpOp ")"
                | "Subscript" "(" Expr "," Index ")"
                | "BinOp" "(" String "," Expr "," Expr ")"

  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"
  syntax Index ::= Expr
                 | "Slice" "(" Bound "," Bound "," Bound ")"
  syntax Bound ::= Expr | "NoBound"

endmodule

module MPY-SEMANTIC
  imports MPY-SYNTAX

  syntax Value ::= intVal(Int)
                 | strVal(String)
                 | boolVal(Bool)
                 | vowelVal(String)

  syntax Outcome ::= "normal"
                   | returned(Value)

  syntax KItem ::= "run" "(" Program "," String ")"

  configuration
    <mpy>
      <k> run($PGM:Program, $INPUT:String) </k>
    </mpy>

  // A small-step evaluator for exactly the source-language forms used by
  // solution.mpy. The translator remains purely syntactic; all meaning below
  // is supplied here. Explicit continuation items preserve Python's
  // left-to-right evaluation order and expose symbolic branches to kprove.
  syntax KItem ::= exec(Stmts, String, Program)
                 | eval(Expr, String, Program)
                 | "programResult"
                 | "makeReturned"
                 | branch(Stmts, Stmts, Stmts, String, Program)
                 | continueWith(Stmts, String, Program)
                 | "lenResult"
                 | callResult(Program)
                 | compareLeft(String, Expr, String, Program)
                 | compareRight(String, Value)
                 | indexResult(Int)
                 | sliceResult(Int)
                 | binLeft(String, Expr, String, Program)
                 | binRight(String, Value)

  rule <k> run(
               Module(FuncDef("count_upper", Params("s"), BODY)) #as P,
               S
             )
          => exec(BODY, S, P) ~> programResult ... </k>

  rule <k> exec(.Stmts, _, _) => normal ... </k>
  rule <k> exec(Return(E) _REST, S, P)
          => eval(E, S, P) ~> makeReturned ... </k>
  rule <k> exec(If(COND, THEN, ELSE) REST, S, P)
          => eval(COND, S, P)
             ~> branch(THEN, ELSE, REST, S, P) ... </k>

  rule <k> boolVal(B)
             ~> branch(THEN, _, REST, S, P)
          => exec(THEN, S, P)
             ~> continueWith(REST, S, P) ... </k>
    requires B
  rule <k> boolVal(B)
             ~> branch(_, ELSE, REST, S, P)
          => exec(ELSE, S, P)
             ~> continueWith(REST, S, P) ... </k>
    requires notBool B
  rule <k> vowelVal("A") ~> branch(THEN, _, REST, S, P)
          => exec(THEN, S, P) ~> continueWith(REST, S, P) ... </k>
  rule <k> vowelVal("E") ~> branch(THEN, _, REST, S, P)
          => exec(THEN, S, P) ~> continueWith(REST, S, P) ... </k>
  rule <k> vowelVal("I") ~> branch(THEN, _, REST, S, P)
          => exec(THEN, S, P) ~> continueWith(REST, S, P) ... </k>
  rule <k> vowelVal("O") ~> branch(THEN, _, REST, S, P)
          => exec(THEN, S, P) ~> continueWith(REST, S, P) ... </k>
  rule <k> vowelVal("U") ~> branch(THEN, _, REST, S, P)
          => exec(THEN, S, P) ~> continueWith(REST, S, P) ... </k>
  rule <k> vowelVal(C) ~> branch(_, ELSE, REST, S, P)
          => exec(ELSE, S, P) ~> continueWith(REST, S, P) ... </k>
    requires C =/=String "A"
     andBool C =/=String "E"
     andBool C =/=String "I"
     andBool C =/=String "O"
     andBool C =/=String "U"

  rule <k> returned(V) ~> continueWith(_, _, _) => returned(V) ... </k>
  rule <k> normal ~> continueWith(REST, S, P)
          => exec(REST, S, P) ... </k>
  rule <k> V:Value ~> makeReturned => returned(V) ... </k>
  rule <k> returned(V) ~> programResult => V ... </k>

  rule <k> eval(Name("s"), S, _) => strVal(S) ... </k>
  rule <k> eval(Int(I), _, _) => intVal(I) ... </k>
  rule <k> eval(Str(S), _, _) => strVal(S) ... </k>

  rule <k> eval(Call(Name("len"), ARG), S, P)
          => eval(ARG, S, P) ~> lenResult ... </k>
  rule <k> strVal(S) ~> lenResult
          => intVal(lengthString(S)) ... </k>

  rule <k> eval(Call(Name("count_upper"), ARG), S, P)
          => eval(ARG, S, P) ~> callResult(P) ... </k>
  rule <k> strVal(S) ~> callResult(P)
          => run(P, S) ... </k>

  rule <k> eval(Compare(LEFT, CmpOp(OP, RIGHT)), S, P)
          => eval(LEFT, S, P)
             ~> compareLeft(OP, RIGHT, S, P) ... </k>
  rule <k> LEFT:Value ~> compareLeft(OP, RIGHT, S, P)
          => eval(RIGHT, S, P)
             ~> compareRight(OP, LEFT) ... </k>
  rule <k> intVal(J) ~> compareRight("==", intVal(I))
          => boolVal(I ==Int J) ... </k>
  rule <k> strVal("AEIOU") ~> compareRight("in", strVal(NEEDLE))
          => vowelVal(NEEDLE) ... </k>

  rule <k> eval(Subscript(BASE, Int(I)), S, P)
          => eval(BASE, S, P) ~> indexResult(I) ... </k>
  rule <k> strVal(S) ~> indexResult(I)
          => strVal(substrString(S, I, I +Int 1)) ... </k>

  rule <k> eval(
               Subscript(BASE, Slice(Int(I), NoBound, NoBound)),
               S,
               P
             )
          => eval(BASE, S, P) ~> sliceResult(I) ... </k>
  // Python clamps a positive lower slice bound to the string length.
  rule <k> strVal(S) ~> sliceResult(I)
          => strVal(
               substrString(
                 S,
                 minInt(maxInt(I, 0), lengthString(S)),
                 lengthString(S)
               )
             ) ... </k>

  rule <k> eval(BinOp(OP, LEFT, RIGHT), S, P)
          => eval(LEFT, S, P)
             ~> binLeft(OP, RIGHT, S, P) ... </k>
  rule <k> LEFT:Value ~> binLeft(OP, RIGHT, S, P)
          => eval(RIGHT, S, P) ~> binRight(OP, LEFT) ... </k>
  rule <k> intVal(J) ~> binRight("+", intVal(I))
          => intVal(I +Int J) ... </k>

endmodule
