// A small, executable semantics for the py2mpy fragment used by solution.py.
// Digit strings retain precisely the information observable by odd_count:
// whether each character is odd or even.  Text concatenation remains
// structural, so symbolic decimal conversion does not depend on a host hook.

module MPY-SYNTAX
  imports INT-SYNTAX
  imports BOOL-SYNTAX
  imports STRING-SYNTAX

  syntax Module ::= "Module" "(" Stmts ")"
  syntax Stmts ::= List{Stmt, ""}

  syntax Params ::= "Params" "(" String ")"
  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "Assign" "(" Expr "," Expr ")"
                | "For" "(" Expr "," Expr "," Stmts ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"
                | "Return" "(" Expr ")"

  syntax Expr ::= "Name" "(" String ")"
                | "Int" "(" Int ")"
                | "Str" "(" String ")"
                | "ListExpr" "(" ")"
                | "ListExpr" "(" Expr ")"
                | "BinOp" "(" String "," Expr "," Expr ")"
                | "Compare" "(" Expr "," CmpOp ")"
                | "Call" "(" Expr "," Expr ")"
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"

  // Valid input strings contain only digits.  This quotient records exactly
  // their parity, the only property this task observes.
  syntax Digit ::= "evenDigit" | "oddDigit"
  syntax Digits ::= "noDigits"
                  | "digit" "(" Digit "," Digits ")"

  // Text is a denotation of a Python string.  concat and number denote exact
  // string concatenation and decimal rendering, respectively.
  syntax Text ::= "literal" "(" String ")"
                | "inputDigits" "(" Digits ")"
                | "oneDigit" "(" Digit ")"
                | "number" "(" Int ")"
                | "concat" "(" Text "," Text ")"

  syntax Values ::= "noValues"
                  | "value" "(" Value "," Values ")"
  syntax Value ::= "noValue"
                 | "pyInt" "(" Int ")"
                 | "pyBool" "(" Bool ")"
                 | "pyString" "(" Text ")"
                 | "pyList" "(" Values ")"

  // A newest-binding-first environment.  Assignment adds a shadowing entry;
  // this avoids imposing any host-map reasoning on symbolic proofs.
  syntax Env ::= "emptyEnv"
               | "store" "(" String "," Value "," Env ")"

  syntax ExecResult ::= "normal" "(" Env ")"
                      | "returned" "(" Value ")"
endmodule

module MPY-SEMANTICS
  imports MPY-SYNTAX
  imports INT
  imports BOOL
  imports STRING

  configuration
    <py>
      <k> $PGM:Module </k>
      <input> $INPUT:Value </input>
      <output> noValue </output>
    </py>

  syntax Value ::= evaluate ( Expr , Env ) [function]
                 | lookup ( String , Env ) [function]
  syntax Value ::= addValue ( Value , Value ) [function]
                 | containsValue ( Value , Value ) [function]
                 | builtinStr ( Value ) [function]
  syntax Values ::= appendValues ( Values , Values ) [function]
                  | iterableValues ( Value ) [function]
                  | digitValues ( Digits ) [function]

  rule evaluate(Name(X), ENV) => lookup(X, ENV)
  rule lookup(X, store(X, V, _ENV)) => V
  rule lookup(X, store(Y, _V, ENV)) => lookup(X, ENV)
    requires X =/=String Y
  rule evaluate(Int(I), _) => pyInt(I)
  rule evaluate(Str(S), _) => pyString(literal(S))
  rule evaluate(ListExpr(), _) => pyList(noValues)
  rule evaluate(ListExpr(E), ENV) => pyList(value(evaluate(E, ENV), noValues))
  rule evaluate(BinOp("+", LEFT, RIGHT), ENV)
    => addValue(evaluate(LEFT, ENV), evaluate(RIGHT, ENV))
  rule evaluate(Compare(LEFT, CmpOp("in", RIGHT)), ENV)
    => containsValue(evaluate(LEFT, ENV), evaluate(RIGHT, ENV))
  rule evaluate(Call(Name("str"), ARG), ENV)
    => builtinStr(evaluate(ARG, ENV))

  rule addValue(pyInt(I), pyInt(J)) => pyInt(I +Int J)
  rule addValue(pyString(A), pyString(B)) => pyString(concat(A, B))
  rule addValue(pyList(A), pyList(B)) => pyList(appendValues(A, B))

  rule appendValues(noValues, B) => B
  rule appendValues(value(V, VS), B) => value(V, appendValues(VS, B))

  rule builtinStr(pyInt(I)) => pyString(number(I))

  rule containsValue(pyString(oneDigit(oddDigit)),
                     pyString(literal("13579"))) => pyBool(true)
  rule containsValue(pyString(oneDigit(evenDigit)),
                     pyString(literal("13579"))) => pyBool(false)

  rule iterableValues(pyList(VS)) => VS
  rule iterableValues(pyString(inputDigits(DS))) => digitValues(DS)
  rule digitValues(noDigits) => noValues
  rule digitValues(digit(D, DS))
    => value(pyString(oneDigit(D)), digitValues(DS))

  syntax ExecResult ::= execute ( Stmts , Env ) [function]
                      | afterBlock ( ExecResult , Stmts ) [function]
                      | executeFor ( Values , String , Stmts , Stmts , Env ) [function]
                      | afterIteration ( ExecResult , Values , String , Stmts , Stmts ) [function]

  rule execute(.Stmts, ENV) => normal(ENV)

  rule execute(Assign(Name(X), E) REST, ENV)
    => execute(REST, store(X, evaluate(E, ENV), ENV))

  rule execute(If(COND, YES, NO) REST, ENV)
    => executeIf(evaluate(COND, ENV), YES, NO, REST, ENV)

  syntax ExecResult ::= executeIf ( Value , Stmts , Stmts , Stmts , Env ) [function]
  rule executeIf(pyBool(true), YES, _, REST, ENV)
    => afterBlock(execute(YES, ENV), REST)
  rule executeIf(pyBool(false), _, NO, REST, ENV)
    => afterBlock(execute(NO, ENV), REST)

  rule afterBlock(normal(ENV), REST) => execute(REST, ENV)
  rule afterBlock(returned(V), _) => returned(V)

  rule execute(For(Name(X), ITER, BODY) REST, ENV)
    => executeFor(iterableValues(evaluate(ITER, ENV)), X, BODY, REST, ENV)

  rule executeFor(noValues, _, _, REST, ENV) => execute(REST, ENV)
  rule executeFor(value(V, VS), X, BODY, REST, ENV)
    => afterIteration(execute(BODY, store(X, V, ENV)), VS, X, BODY, REST)

  rule afterIteration(normal(ENV), VS, X, BODY, REST)
    => executeFor(VS, X, BODY, REST, ENV)
  rule afterIteration(returned(V), _, _, _, _) => returned(V)

  rule execute(Return(E) _REST, ENV) => returned(evaluate(E, ENV))

  syntax Value ::= resultValue ( ExecResult ) [function]
  rule resultValue(returned(V)) => V

  rule <k> Module(FuncDef("odd_count", Params("lst"), BODY))
        => .K ...</k>
       <input> IN </input>
       <output> noValue => resultValue(execute(BODY, store("lst", IN, emptyEnv))) </output>
endmodule

module MPY
  imports MPY-SEMANTICS
endmodule
