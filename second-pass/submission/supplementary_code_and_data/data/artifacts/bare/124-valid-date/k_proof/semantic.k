requires "domains.md"

module MPY-SYNTAX
  imports INT-SYNTAX
  imports BOOL-SYNTAX
  imports STRING-SYNTAX

  // The constructor grammar is the portion of py2mpy.py used by solution.mpy.
  syntax Program ::= "Module" "(" Stmts ")"
  syntax Stmts  ::= List{Stmt, ""}

  syntax Stmt ::= "FuncDef" "(" String "," "Params" "(" String ")" "," Stmts ")"
                | "Return" "(" Expr ")"
                | "Assign" "(" Expr "," Expr ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"

  syntax Expr ::= "Int" "(" Int ")"
                | "Bool" "(" Bool ")"
                | "Str" "(" String ")"
                | "Name" "(" String ")"
                | "UnaryOp" "(" String "," Expr ")"
                | "BoolOp" "(" String "," Expr "," Expr ")"
                | "BoolOp" "(" String "," Expr "," Expr "," Expr ")"
                | "BoolOp" "(" String "," Expr "," Expr "," Expr "," Expr ")"
                | "Compare" "(" Expr "," CmpOp ")"
                | "Subscript" "(" Expr "," Expr ")"
                | "Subscript" "(" Expr "," SliceExpr ")"
                | "Attribute" "(" Expr "," String ")"
                | "Call" "(" Expr "," ")"
                | "Call" "(" Expr "," Expr ")"

  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"
  syntax SliceExpr ::= "Slice" "(" Expr "," Expr "," "NoBound" ")"
endmodule

module MPY-SEMANTIC
  imports MPY-SYNTAX
  imports INT
  imports BOOL
  imports STRING

  syntax Val ::= intVal(Int) | boolVal(Bool) | strVal(String)
  syntax Vals ::= vals(Val)

  syntax Env ::= ".Env" | bind(String, Val, Env)
  syntax ExecResult ::= normal(Env) | returned(Val)

  syntax Command ::= runProgram(Program, String, Vals)
  configuration <k> $PGM:Command </k>

  // A module is executable when it consists of the requested one-argument
  // function. This is precisely the top-level shape emitted for solution.py.
  rule <k> runProgram(
             Module(FuncDef(F, Params(P), BODY)),
             F,
             vals(V))
          => finish(exec(BODY, bind(P, V, .Env))) ... </k>

  syntax KItem ::= finish(ExecResult) [function]
  rule finish(returned(V)) => V
  rule finish(normal(_)) => boolVal(false)

  syntax ExecResult ::= exec(Stmts, Env) [function]
  rule exec(.Stmts, ENV) => normal(ENV)
  rule exec(Return(E) _REST, ENV) => returned(eval(E, ENV))
  rule exec(Assign(Name(N), E) REST, ENV)
    => exec(REST, bind(N, eval(E, ENV), ENV))
  rule exec(If(COND, THEN, ELSE) REST, ENV)
    => branch(eval(COND, ENV), THEN, ELSE, REST, ENV)

  syntax ExecResult ::= branch(Val, Stmts, Stmts, Stmts, Env) [function]
  rule branch(boolVal(true),  THEN, _, REST, ENV) => resume(exec(THEN, ENV), REST)
  rule branch(boolVal(false), _, ELSE, REST, ENV) => resume(exec(ELSE, ENV), REST)

  syntax ExecResult ::= resume(ExecResult, Stmts) [function]
  rule resume(returned(V), _) => returned(V)
  rule resume(normal(ENV), REST) => exec(REST, ENV)

  syntax Val ::= lookup(String, Env) [function]
  rule lookup(N, bind(N, V, _)) => V
  rule lookup(N, bind(M, _, REST)) => lookup(N, REST)
    requires N =/=String M

  syntax Val ::= eval(Expr, Env) [function]
  rule eval(Int(I), _) => intVal(I)
  rule eval(Bool(B), _) => boolVal(B)
  rule eval(Str(S), _) => strVal(S)
  rule eval(Name(N), ENV) => lookup(N, ENV)

  rule eval(UnaryOp("not", E), ENV) => pyNot(eval(E, ENV))

  rule eval(BoolOp("and", A, B), ENV)
    => boolVal(asBool(eval(A, ENV)) andBool asBool(eval(B, ENV)))
  rule eval(BoolOp("and", A, B, C), ENV)
    => boolVal(asBool(eval(A, ENV)) andBool asBool(eval(B, ENV))
               andBool asBool(eval(C, ENV)))
  rule eval(BoolOp("and", A, B, C, D), ENV)
    => boolVal(asBool(eval(A, ENV)) andBool asBool(eval(B, ENV))
               andBool asBool(eval(C, ENV)) andBool asBool(eval(D, ENV)))
  rule eval(BoolOp("or", A, B), ENV)
    => boolVal(asBool(eval(A, ENV)) orBool asBool(eval(B, ENV)))
  rule eval(BoolOp("or", A, B, C), ENV)
    => boolVal(asBool(eval(A, ENV)) orBool asBool(eval(B, ENV))
               orBool asBool(eval(C, ENV)))
  rule eval(BoolOp("or", A, B, C, D), ENV)
    => boolVal(asBool(eval(A, ENV)) orBool asBool(eval(B, ENV))
               orBool asBool(eval(C, ENV)) orBool asBool(eval(D, ENV)))

  rule eval(Compare(A, CmpOp(OP, B)), ENV)
    => compare(OP, eval(A, ENV), eval(B, ENV))

  rule eval(Subscript(E, Int(I)), ENV) => pyIndex(eval(E, ENV), I)
  rule eval(Subscript(E, Slice(Int(LO), Int(HI), NoBound)), ENV)
    => pySlice(eval(E, ENV), LO, HI)

  rule eval(Call(Name("len"), E), ENV) => pyLen(eval(E, ENV))
  rule eval(Call(Name("int"), E), ENV) => pyInt(eval(E, ENV))
  rule eval(Call(Attribute(E, "isdigit"), ), ENV) => pyIsDigit(eval(E, ENV))

  syntax Bool ::= asBool(Val) [function]
  rule asBool(boolVal(B)) => B

  syntax Val ::= pyNot(Val) [function]
  rule pyNot(boolVal(B)) => boolVal(notBool B)

  syntax Val ::= compare(String, Val, Val) [function]
  rule compare("==", intVal(A), intVal(B)) => boolVal(A ==Int B)
  rule compare("!=", intVal(A), intVal(B)) => boolVal(A =/=Int B)
  rule compare("<",  intVal(A), intVal(B)) => boolVal(A <Int B)
  rule compare("<=", intVal(A), intVal(B)) => boolVal(A <=Int B)
  rule compare(">",  intVal(A), intVal(B)) => boolVal(A >Int B)
  rule compare(">=", intVal(A), intVal(B)) => boolVal(A >=Int B)
  rule compare("==", strVal(A), strVal(B)) => boolVal(A ==String B)
  rule compare("!=", strVal(A), strVal(B)) => boolVal(A =/=String B)

  syntax Val ::= pyLen(Val) [function]
  rule pyLen(strVal(S)) => intVal(lengthString(S))

  syntax Val ::= pyIndex(Val, Int) [function]
  rule pyIndex(strVal(S), I) => strVal(substrString(S, I, I +Int 1))

  syntax Val ::= pySlice(Val, Int, Int) [function]
  rule pySlice(strVal(S), LO, HI) => strVal(substrString(S, LO, HI))

  syntax Val ::= pyInt(Val) [function]
  rule pyInt(strVal(S)) => intVal(String2Int(S))

  // Only ASCII decimal characters participate in the mm-dd-yyyy format.
  syntax Val ::= pyIsDigit(Val) [function]
  rule pyIsDigit(strVal(S)) => boolVal(isDigits(S))

  syntax Bool ::= isDigits(String) [function]
  rule isDigits(S) => false requires lengthString(S) ==Int 0
  rule isDigits(S) => isDigitsAt(S, 0) requires lengthString(S) >Int 0

  syntax Bool ::= isDigitsAt(String, Int) [function]
  rule isDigitsAt(S, I) => true requires I >=Int lengthString(S)
  rule isDigitsAt(S, I)
    => isDigitChar(substrString(S, I, I +Int 1))
       andBool isDigitsAt(S, I +Int 1)
    requires I <Int lengthString(S)

  syntax Bool ::= isDigitChar(String) [function]
  rule isDigitChar(C) => findString("0123456789", C, 0) >=Int 0
endmodule

module MPY
  imports MPY-SEMANTIC
endmodule
