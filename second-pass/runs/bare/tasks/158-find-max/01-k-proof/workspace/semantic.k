module MPY-SYNTAX
  imports BOOL-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX

  // Constructor grammar emitted by py2mpy.py for the submitted program.
  syntax Pgm ::= AST
               | "runFindMax" "(" AST "," Words ")"

  syntax AST ::= "Module" "(" FuncDef ")"
  syntax FuncDef ::= "FuncDef" "(" String "," Params "," Stmts ")"
  syntax Params ::= "Params" "(" String ")"

  // The translator deliberately prints statement lists by juxtaposition.
  syntax Stmts ::= List{Stmt, ""}
  syntax Stmt ::= "Assign" "(" Expr "," Expr ")"
                | "For" "(" Expr "," Expr "," Stmts ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"
                | "Return" "(" Expr ")"

  syntax Expr ::= "Name" "(" String ")"
                | "Str" "(" String ")"
                | "Int" "(" Int ")"
                | "UnaryOp" "(" String "," Expr ")"
                | "Call" "(" Expr "," Expr ")"
                | "Compare" "(" Expr "," CmpOp ")"
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"

  // A transparent recursive word-list makes symbolic list induction explicit.
  syntax Words ::= "nil"
                 | "cons" "(" String "," Words ")"
endmodule

module SEMANTIC
  imports MPY-SYNTAX
  imports BOOL
  imports INT
  imports STRING

  syntax Value ::= "strVal" "(" String ")"
                 | "intVal" "(" Int ")"
                 | "boolVal" "(" Bool ")"
                 | "wordsVal" "(" Words ")"
  syntax Result ::= "noResult" | "result" "(" Value ")"

  syntax KItem ::= "exec" "(" Stmts ")"
                 | "eval" "(" Expr ")"
                 | "store" "(" String ")"
                 | "negate"
                 | "callArg" "(" String ")"
                 | "cmpLeft" "(" String "," Expr ")"
                 | "cmpRight" "(" String "," Value ")"
                 | "branch" "(" Stmts "," Stmts ")"
                 | "startFor" "(" String "," Stmts ")"
                 | "loop" "(" String "," Words "," Stmts ")"
                 | "finishReturn"

  configuration
    <mpy>
      <k> $PGM:Pgm </k>
      <words> $INPUT:Words </words>
      <best> "" </best>
      <bestCount> -1 </bestCount>
      <word> "" </word>
      <count> 0 </count>
      <result> noResult </result>
    </mpy>

  // Entry-point invocation.  The body is taken from the parsed AST itself.
  rule <k> Module(FuncDef("find_max", Params("words"), BODY))
          => exec(BODY) ... </k>
  rule <k> runFindMax(
             Module(FuncDef("find_max", Params("words"), BODY)), WORDS)
          => exec(BODY) ... </k>
       <words> _ => WORDS </words>

  // Statement sequencing.
  rule <k> exec(.Stmts) => .K ... </k>
  rule <k> exec(S REST) => S ~> exec(REST) ... </k>

  // Assignment and the five local variables used by find_max.
  rule <k> Assign(Name(X), E) => eval(E) ~> store(X) ... </k>
  rule <k> strVal(S) ~> store("best") => .K ... </k>
       <best> _ => S </best>
  rule <k> intVal(I) ~> store("best_count") => .K ... </k>
       <bestCount> _ => I </bestCount>
  rule <k> strVal(S) ~> store("word") => .K ... </k>
       <word> _ => S </word>
  rule <k> intVal(I) ~> store("count") => .K ... </k>
       <count> _ => I </count>

  // Name and literal evaluation.
  rule <k> eval(Str(S)) => strVal(S) ... </k>
  rule <k> eval(Int(I)) => intVal(I) ... </k>
  rule <k> eval(Name("words")) => wordsVal(WORDS) ... </k>
       <words> WORDS </words>
  rule <k> eval(Name("best")) => strVal(S) ... </k>
       <best> S </best>
  rule <k> eval(Name("best_count")) => intVal(I) ... </k>
       <bestCount> I </bestCount>
  rule <k> eval(Name("word")) => strVal(S) ... </k>
       <word> S </word>
  rule <k> eval(Name("count")) => intVal(I) ... </k>
       <count> I </count>

  // Unary minus.
  rule <k> eval(UnaryOp("-", E)) => eval(E) ~> negate ... </k>
  rule <k> intVal(I) ~> negate => intVal(0 -Int I) ... </k>

  // Function calls.  set(str) is represented extensionally by the source
  // string because the only observation made by this program is len(set(str)).
  syntax Value ::= "setVal" "(" String ")"
  rule <k> eval(Call(Name(F), ARG)) => eval(ARG) ~> callArg(F) ... </k>
  rule <k> strVal(S) ~> callArg("set") => setVal(S) ... </k>
  rule <k> setVal(S) ~> callArg("len") => intVal(distinctCount(S)) ... </k>

  // Comparisons used by the submitted implementation.
  rule <k> eval(Compare(L, CmpOp(OP, R)))
        => eval(L) ~> cmpLeft(OP, R) ... </k>
  rule <k> V:Value ~> cmpLeft(OP, R)
        => eval(R) ~> cmpRight(OP, V) ... </k>
  rule <k> intVal(J) ~> cmpRight(">", intVal(I))
        => boolVal(I >Int J) ... </k>
  rule <k> intVal(J) ~> cmpRight("==", intVal(I))
        => boolVal(I ==Int J) ... </k>
  rule <k> strVal(T) ~> cmpRight("<", strVal(S))
        => boolVal(S <String T) ... </k>

  // Conditionals branch on any Bool predicate, including symbolic ones.
  rule <k> If(COND, THEN, ELSE)
        => eval(COND) ~> branch(THEN, ELSE) ... </k>
  rule <k> boolVal(B) ~> branch(THEN, _)
        => exec(THEN) ... </k> requires B
  rule <k> boolVal(B) ~> branch(_, ELSE)
        => exec(ELSE) ... </k> requires notBool B

  // For loops snapshot the iterable and update the loop variable per element.
  rule <k> For(Name(X), ITER, BODY)
        => eval(ITER) ~> startFor(X, BODY) ... </k>
  rule <k> wordsVal(WORDS) ~> startFor(X, BODY)
        => loop(X, WORDS, BODY) ... </k>
  rule <k> loop(_, nil, _) => .K ... </k>
  rule <k> loop("word", cons(S, REST), BODY)
        => exec(BODY) ~> loop("word", REST, BODY) ... </k>
       <word> _ => S </word>

  // A return records the observable value and discards pending computation.
  rule <k> Return(E) => eval(E) ~> finishReturn ... </k>
  rule <k> V:Value ~> finishReturn ~> _ => .K </k>
       <result> noResult => result(V) </result>
  rule <k> V:Value ~> finishReturn => .K </k>
       <result> noResult => result(V) </result>

  // Concrete implementation of Python's len(set(s)): scan left-to-right and
  // count a character iff it does not occur in the already-scanned prefix.
  // The concrete attributes deliberately keep distinctCount(S) abstract for
  // symbolic strings in proofs.
  syntax Int ::= "distinctCount" "(" String ")" [function, total]
  syntax Int ::= "distinctCountFrom" "(" String "," Int ")" [function]
  rule distinctCount(S) => distinctCountFrom(S, 0)
    [concrete(S), simplification]
  rule distinctCountFrom(S, I) => 0
    requires I >=Int lengthString(S) [concrete(S, I), simplification]
  rule distinctCountFrom(S, I) => distinctCountFrom(S, I +Int 1)
    requires I <Int lengthString(S)
     andBool findString(
       substrString(S, 0, I), substrString(S, I, I +Int 1), 0) >=Int 0
    [concrete(S, I), simplification]
  rule distinctCountFrom(S, I) => 1 +Int distinctCountFrom(S, I +Int 1)
    requires I <Int lengthString(S)
     andBool findString(
       substrString(S, 0, I), substrString(S, I, I +Int 1), 0) <Int 0
    [concrete(S, I), simplification]

  // Useful symbolic facts about the two total comparison hooks.
  rule S:String <String S => false [simplification]
  rule distinctCount(_S) >=Int 0 => true [simplification]
endmodule
