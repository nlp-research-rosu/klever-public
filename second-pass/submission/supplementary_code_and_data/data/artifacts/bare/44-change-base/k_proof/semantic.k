requires "domains.md"

module MPY-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX

  syntax Program ::= "Module" "(" Stmts ")"
  syntax Stmts  ::= List{Stmt, ""}

  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"
                | "Return" "(" Expr ")"

  syntax Params ::= "Params" "(" String "," String ")"

  syntax Exprs ::= List{Expr, ","}
  syntax Expr  ::= "Name" "(" String ")"
                 | "Int" "(" Int ")"
                 | "BinOp" "(" String "," Expr "," Expr ")"
                 | "Compare" "(" Expr "," CmpOp ")"
                 | "Call" "(" Expr "," Exprs ")"
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"
endmodule

module MPY
  imports MPY-SYNTAX
  imports INT
  imports BOOL
  imports STRING
  imports MAP

  syntax Value ::= intVal(Int)
                 | strVal(String)
                 | boolVal(Bool)

  syntax Stmts ::= appendStmts(Stmts, Stmts) [function]
  rule appendStmts(.Stmts, SS) => SS
  rule appendStmts((S:Stmt SS:Stmts), TT) => S appendStmts(SS, TT)

  // The internal control terms below are deliberately separate from the
  // source AST.  They form a small-step semantics for exactly the Python
  // constructs used by solution.py.
  syntax KItem ::= call(Program, String, Value, Value)
                 | exec(Stmts, Map, Program)
                 | eval(Expr, Map, Program)
                 | branch(Stmts, Stmts, Stmts, Map, Program)
                 | cmpLeft(String, Expr, Map, Program)
                 | cmpRight(String, Value)
                 | binLeft(String, Expr, Map, Program)
                 | binRight(String, Value)
                 | toString()
                 | callArgLeft(String, Expr, Map, Program)
                 | callArgRight(String, Value, Program)

  configuration
    <k> call($PGM:Program, "change_base", intVal($X:Int), intVal($BASE:Int)) </k>

  // Function lookup, parameter binding, and statement execution.
  rule <k>
         call(Module(FuncDef(F, Params(X, B), BODY)), F, VX, VB)
      => exec(BODY,
              ((X |-> VX) (B |-> VB)),
              Module(FuncDef(F, Params(X, B), BODY)))
       ...
       </k>

  rule <k> exec(.Stmts, _RHO, _PGM) => strVal("") ... </k>

  // A return exits the whole current statement list.  This subset contains
  // no fall-through expression statements, so no extra completion value is
  // needed.
  rule <k> exec(Return(E) _REST, RHO, PGM) => eval(E, RHO, PGM) ... </k>

  rule <k>
         exec(If(COND, THEN, ELSE) REST, RHO, PGM)
      => eval(COND, RHO, PGM) ~> branch(THEN, ELSE, REST, RHO, PGM)
       ...
       </k>
  rule <k>
         boolVal(true) ~> branch(THEN:Stmts, _ELSE:Stmts, REST:Stmts, RHO, PGM)
      => exec(appendStmts(THEN, REST), RHO, PGM)
       ...
       </k>
  rule <k>
         boolVal(false) ~> branch(_THEN:Stmts, ELSE:Stmts, REST:Stmts, RHO, PGM)
      => exec(appendStmts(ELSE, REST), RHO, PGM)
       ...
       </k>

  // Literals and variables.
  rule <k> eval(Int(I), _RHO, _PGM) => intVal(I) ... </k>
  rule <k> eval(Name(X), RHO, _PGM) => RHO [ X ] ... </k>

  // Single comparisons (the only comparison shape used by the program).
  rule <k>
         eval(Compare(LEFT, CmpOp(OP, RIGHT)), RHO, PGM)
      => eval(LEFT, RHO, PGM) ~> cmpLeft(OP, RIGHT, RHO, PGM)
       ...
       </k>
  rule <k>
         V:Value ~> cmpLeft(OP, RIGHT, RHO, PGM)
      => eval(RIGHT, RHO, PGM) ~> cmpRight(OP, V)
       ...
       </k>
  rule <k> intVal(J) ~> cmpRight("<", intVal(I))
        => boolVal(I <Int J) ... </k>

  // Binary expressions evaluate left-to-right, as Python does.
  rule <k>
         eval(BinOp(OP, LEFT, RIGHT), RHO, PGM)
      => eval(LEFT, RHO, PGM) ~> binLeft(OP, RIGHT, RHO, PGM)
       ...
       </k>
  rule <k>
         V:Value ~> binLeft(OP, RIGHT, RHO, PGM)
      => eval(RIGHT, RHO, PGM) ~> binRight(OP, V)
       ...
       </k>
  rule <k> intVal(J) ~> binRight("//", intVal(I))
        => intVal(I /Int J) ... </k>
    requires J =/=Int 0
  rule <k> intVal(J) ~> binRight("%", intVal(I))
        => intVal(I %Int J) ... </k>
    requires J =/=Int 0
  rule <k> strVal(T) ~> binRight("+", strVal(S))
        => strVal(S +String T) ... </k>

  // Built-in str(int), plus ordinary two-argument function calls.
  rule <k>
         eval(Call(Name("str"), ARG), RHO, PGM)
      => eval(ARG, RHO, PGM) ~> toString()
       ...
       </k>
  rule <k> intVal(I) ~> toString() => strVal(Int2String(I)) ... </k>

  rule <k>
         eval(Call(Name(F), ARG1, ARG2), RHO, PGM)
      => eval(ARG1, RHO, PGM) ~> callArgLeft(F, ARG2, RHO, PGM)
       ...
       </k>
  rule <k>
         V1:Value ~> callArgLeft(F, ARG2, RHO, PGM)
      => eval(ARG2, RHO, PGM) ~> callArgRight(F, V1, PGM)
       ...
       </k>
  rule <k>
         V2:Value ~> callArgRight(F, V1, PGM)
      => call(PGM, F, V1, V2)
       ...
       </k>
endmodule
