module MPY-SYNTAX
  imports INT
  imports FLOAT
  imports BOOL
  imports STRING
  imports MAP

  // The constructor grammar used by the portion of py2mpy.py exercised by
  // solution.py.  The constructors retain the structure of the CPython AST.
  syntax Program ::= "Module" "(" Stmts ")"
  syntax Stmts  ::= Stmt
  syntax Stmt   ::= "FuncDef" "(" String "," Params "," Stmts ")"
                  | "Return" "(" Expr ")"
  syntax Params ::= "Params" "(" String "," String "," String ")"

  syntax Expr ::= "Name" "(" String ")"
                | "Int" "(" Int ")"
                | "Bool" "(" Bool ")"
                | "BinOp" "(" String "," Expr "," Expr ")"
                | "Call" "(" Expr "," Expr ")"
                | "Compare" "(" Expr "," CmpOp ")"
                | "BoolOp" "(" String "," Expr "," Expr "," Expr ")"
                | "BoolOp" "(" String "," Expr "," Expr "," Expr "," Expr ")"
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"

  // Runtime values distinguish Python integers from every modeled
  // non-integer number.  Bool is deliberately non-integer here because the
  // solution uses exact type(x) == int, not isinstance(x, int).
  syntax IntVal    ::= "intVal" "(" Int ")"
  syntax NonIntVal ::= "floatVal" "(" Float ")"
                     | "boolVal" "(" Bool ")"
                     | "otherNumberVal" "(" String ")"
  syntax Val ::= IntVal | NonIntVal
               | "typeVal" "(" String ")"

  syntax KItem ::= "Invoke" "(" Program "," Val "," Val "," Val ")"
endmodule

module MPY-SEMANTICS
  imports MPY-SYNTAX

  configuration
    <mpy>
      <k> $PGM:K </k>
      <env> .Map </env>
    </mpy>

  syntax KItem ::= "exec" "(" Stmts ")"
                 | "eval" "(" Expr ")"
                 | "finishCall"
                 | "typeOf"
                 | "binLeft" "(" String "," Expr ")"
                 | "binRight" "(" String "," Val ")"
                 | "compareLeft" "(" String "," Expr ")"
                 | "compareRight" "(" String "," Val ")"
                 | "andThen" "(" Expr ")"
                 | "orThen" "(" Expr ")"

  // Module/function entry and return.  The local environment is cleared when
  // the call finishes, making each invocation independent.
  rule <k> Invoke(Module(FuncDef(_F, Params(X, Y, Z), BODY)), V1, V2, V3)
           => exec(BODY) ~> finishCall ... </k>
       <env> .Map => X |-> V1 Y |-> V2 Z |-> V3 </env>
  rule <k> exec(Return(E)) => eval(E) ... </k>
  rule <k> V:Val ~> finishCall => V ... </k>
       <env> _ => .Map </env>

  // Literals, local names, and the built-in int type object.
  rule <k> eval(Int(I)) => intVal(I) ... </k>
  rule <k> eval(Bool(B)) => boolVal(B) ... </k>
  rule <k> eval(Name("int")) => typeVal("int") ... </k>
  rule <k> eval(Name(X)) => V ... </k>
       <env>... X |-> V ...</env>

  // The only built-in call emitted by solution.py: exact Python type.
  rule <k> eval(Call(Name("type"), E)) => eval(E) ~> typeOf ... </k>
  rule <k> _I:IntVal ~> typeOf => typeVal("int") ... </k>
  rule <k> _N:NonIntVal ~> typeOf => typeVal("non-int") ... </k>

  // Left-to-right integer addition.
  rule <k> eval(BinOp(OP, E1, E2)) => eval(E1) ~> binLeft(OP, E2) ... </k>
  rule <k> V1:Val ~> binLeft(OP, E2) => eval(E2) ~> binRight(OP, V1) ... </k>
  rule <k> intVal(I2) ~> binRight("+", intVal(I1))
           => intVal(I1 +Int I2) ... </k>

  // The target uses one-element comparison chains.  Both integer equality
  // and equality of type objects return a Python boolean value.
  rule <k> eval(Compare(E1, CmpOp(OP, E2)))
           => eval(E1) ~> compareLeft(OP, E2) ... </k>
  rule <k> V1:Val ~> compareLeft(OP, E2)
           => eval(E2) ~> compareRight(OP, V1) ... </k>
  rule <k> intVal(I2) ~> compareRight("==", intVal(I1))
           => boolVal(I1 ==Int I2) ... </k>
  rule <k> typeVal(T2) ~> compareRight("==", typeVal(T1))
           => boolVal(T1 ==String T2) ... </k>

  // Python's and/or are evaluated left-to-right and short circuit.  The
  // continuation rules skip, rather than evaluate, remaining operands once
  // their result is determined.
  rule <k> eval(BoolOp("and", E1, E2, E3))
           => eval(E1) ~> andThen(E2) ~> andThen(E3) ... </k>
  rule <k> eval(BoolOp("and", E1, E2, E3, E4))
           => eval(E1) ~> andThen(E2) ~> andThen(E3) ~> andThen(E4) ... </k>
  rule <k> boolVal(true) ~> andThen(E) => eval(E) ... </k>
  rule <k> boolVal(false) ~> andThen(_E) => boolVal(false) ... </k>

  rule <k> eval(BoolOp("or", E1, E2, E3))
           => eval(E1) ~> orThen(E2) ~> orThen(E3) ... </k>
  rule <k> boolVal(false) ~> orThen(E) => eval(E) ... </k>
  rule <k> boolVal(true) ~> orThen(_E) => boolVal(true) ... </k>
endmodule
