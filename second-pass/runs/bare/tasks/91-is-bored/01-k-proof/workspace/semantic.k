module MPY-SYNTAX
  imports STRING-SYNTAX
  imports INT-SYNTAX
  imports BOOL-SYNTAX

  syntax Module ::= "Module" "(" Stmts ")"
  syntax Params ::= "Params" "(" String ")"
  syntax Stmts  ::= List{Stmt, ""}
  syntax Exprs  ::= List{Expr, ","}

  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "Assign" "(" Expr "," Expr ")"
                | "AugAssign" "(" Expr "," String "," Expr ")"
                | "For" "(" Expr "," Expr "," Stmts ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"
                | "Return" "(" Expr ")"

  syntax Expr ::= "Name" "(" String ")"
                | "Int" "(" Int ")"
                | "Str" "(" String ")"
                | "Attribute" "(" Expr "," String ")"
                | "Call" "(" Expr "," Exprs ")"
endmodule

module MPY
  imports MPY-SYNTAX
  imports STRING
  imports INT
  imports BOOL

  // Values and the three locals needed by this translated program.
  syntax Value  ::= "vStr" "(" String ")"
                  | "vInt" "(" Int ")"
                  | "vBool" "(" Bool ")"
                  | "vList" "(" Values ")"
  syntax Values ::= "nil"
                  | "cons" "(" Value "," Values ")"
  syntax State  ::= "state" "(" String "," Int "," String ")"

  syntax Outcome ::= "normal" "(" State ")"
                   | "returned" "(" Value ")"

  configuration
    <k> start </k>
    <program> $PGM:Module </program>
    <input> $INPUT:String </input>
    <result> 0 </result>

  syntax KItem ::= "start" | "done"

  rule <k> start => done </k>
       <program> Module(FuncDef("is_bored", Params("S"), BODY)) </program>
       <input> INPUT </input>
       <result> _ => runFunction(BODY, INPUT) </result>

  syntax Int ::= runFunction(Stmts, String) [function]
  rule runFunction(BODY, INPUT)
    => resultOf(evalStmts(BODY, state(INPUT, 0, "")))

  syntax Int ::= resultOf(Outcome) [function]
  rule resultOf(returned(vInt(N))) => N

  // Big-step statement semantics.
  syntax Outcome ::= evalStmts(Stmts, State) [function]
                   | evalStmt(Stmt, State) [function]
                   | evalRest(Outcome, Stmts) [function]

  rule evalStmts(.Stmts, ST) => normal(ST)
  rule evalStmts(S:Stmt SS:Stmts, ST) => evalRest(evalStmt(S, ST), SS)

  rule evalRest(returned(V), _) => returned(V)
  rule evalRest(normal(ST), SS) => evalStmts(SS, ST)

  rule evalStmt(Assign(Name("count"), E), ST)
    => normal(setCount(ST, asInt(eval(E, ST))))
  rule evalStmt(AugAssign(Name("count"), "+", E), ST)
    => normal(setCount(ST, getCount(ST) +Int asInt(eval(E, ST))))
  rule evalStmt(For(Name("sentence"), E, BODY), ST)
    => evalFor(asValues(eval(E, ST)), BODY, ST)
  rule evalStmt(If(E, THEN, ELSE), ST)
    => evalBranch(asBool(eval(E, ST)), THEN, ELSE, ST)
  rule evalStmt(Return(E), ST) => returned(eval(E, ST))

  syntax Outcome ::= evalBranch(Bool, Stmts, Stmts, State) [function]
  rule evalBranch(true, THEN, _, ST) => evalStmts(THEN, ST)
  rule evalBranch(false, _, ELSE, ST) => evalStmts(ELSE, ST)

  syntax Outcome ::= evalFor(Values, Stmts, State) [function]
                   | evalForRest(Outcome, Values, Stmts) [function]
  rule evalFor(nil, _, ST) => normal(ST)
  rule evalFor(cons(vStr(S), REST), BODY, ST)
    => evalForRest(evalStmts(BODY, setSentence(ST, S)), REST, BODY)
  rule evalForRest(returned(V), _, _) => returned(V)
  rule evalForRest(normal(ST), REST, BODY) => evalFor(REST, BODY, ST)

  // State access is deliberately explicit: no hidden host-language store.
  syntax Value ::= lookup(String, State) [function]
  rule lookup("S", state(S, _, _)) => vStr(S)
  rule lookup("count", state(_, N, _)) => vInt(N)
  rule lookup("sentence", state(_, _, S)) => vStr(S)

  syntax State ::= setCount(State, Int) [function]
                 | setSentence(State, String) [function]
  rule setCount(state(S, _, SENT), N) => state(S, N, SENT)
  rule setSentence(state(S, N, _), SENT) => state(S, N, SENT)

  syntax Int ::= getCount(State) [function]
  rule getCount(state(_, N, _)) => N

  // Expression and method-call semantics for the accepted program subset.
  syntax Value ::= eval(Expr, State) [function]
                 | replaceValue(Value, Value, Value) [function]
                 | splitValue(Value, Value) [function]
                 | stripValue(Value) [function]
                 | startswithValue(Value, Value) [function]
  rule eval(Name(X), ST) => lookup(X, ST)
  rule eval(Int(N), _) => vInt(N)
  rule eval(Str(S), _) => vStr(S)
  rule eval(Call(Attribute(E, "replace"), A, B), ST)
    => replaceValue(eval(E, ST), eval(A, ST), eval(B, ST))
  rule eval(Call(Attribute(E, "split"), SEP), ST)
    => splitValue(eval(E, ST), eval(SEP, ST))
  rule eval(Call(Attribute(E, "strip"), .Exprs), ST)
    => stripValue(eval(E, ST))
  rule eval(Call(Attribute(E, "startswith"), PREFIX), ST)
    => startswithValue(eval(E, ST), eval(PREFIX, ST))

  rule replaceValue(vStr(S), vStr(OLD), vStr(NEW))
    => vStr(replaceAll(S, OLD, NEW))
  rule splitValue(vStr(S), vStr(".")) => vList(splitDots(S))
  rule stripValue(vStr(S)) => vStr(strip(S))
  rule startswithValue(vStr(S), vStr(PREFIX)) => vBool(startsWith(S, PREFIX))

  syntax Int ::= asInt(Value) [function]
  syntax Bool ::= asBool(Value) [function]
  syntax Values ::= asValues(Value) [function]
  rule asInt(vInt(N)) => N
  rule asBool(vBool(B)) => B
  rule asValues(vList(VS)) => VS

  // Pure definitions of the three String methods used above.
  syntax Values ::= splitDots(String) [function]
                  | splitDotsAt(String, Int) [function]
  rule splitDots(S) => splitDotsAt(S, findString(S, ".", 0))
  rule splitDotsAt(S, -1) => cons(vStr(S), nil)
  rule splitDotsAt(S, I)
    => cons(vStr(substrString(S, 0, I)),
            splitDots(substrString(S, I +Int 1, lengthString(S))))
    requires I >=Int 0

  syntax Bool ::= whiteSpace(String) [function]
  rule whiteSpace(" ")  => true
  rule whiteSpace("\t") => true
  rule whiteSpace("\n") => true
  rule whiteSpace("\r") => true
  rule whiteSpace("\f") => true
  rule whiteSpace("\u000b") => true
  rule whiteSpace("\u001c") => true
  rule whiteSpace("\u001d") => true
  rule whiteSpace("\u001e") => true
  rule whiteSpace("\u001f") => true
  rule whiteSpace("\u0085") => true
  rule whiteSpace("\u00a0") => true
  rule whiteSpace("\u1680") => true
  rule whiteSpace("\u2000") => true
  rule whiteSpace("\u2001") => true
  rule whiteSpace("\u2002") => true
  rule whiteSpace("\u2003") => true
  rule whiteSpace("\u2004") => true
  rule whiteSpace("\u2005") => true
  rule whiteSpace("\u2006") => true
  rule whiteSpace("\u2007") => true
  rule whiteSpace("\u2008") => true
  rule whiteSpace("\u2009") => true
  rule whiteSpace("\u200a") => true
  rule whiteSpace("\u2028") => true
  rule whiteSpace("\u2029") => true
  rule whiteSpace("\u202f") => true
  rule whiteSpace("\u205f") => true
  rule whiteSpace("\u3000") => true
  rule whiteSpace(_) => false [owise]

  syntax String ::= strip(String) [function]
                  | stripLeft(String) [function]
                  | stripRight(String) [function]
  rule strip(S) => stripRight(stripLeft(S))
  rule stripLeft("") => ""
  rule stripLeft(S) => stripLeft(substrString(S, 1, lengthString(S)))
    requires whiteSpace(substrString(S, 0, 1))
  rule stripLeft(S) => S
    requires notBool whiteSpace(substrString(S, 0, 1))
  rule stripRight("") => ""
  rule stripRight(S) => stripRight(substrString(S, 0, lengthString(S) -Int 1))
    requires whiteSpace(substrString(S, lengthString(S) -Int 1, lengthString(S)))
  rule stripRight(S) => S
    requires notBool whiteSpace(substrString(S, lengthString(S) -Int 1, lengthString(S)))

  syntax Bool ::= startsWith(String, String) [function]
  rule startsWith(S, PREFIX)
    => (lengthString(S) >=Int lengthString(PREFIX))
       andBool (substrString(S, 0, lengthString(PREFIX)) ==String PREFIX)
endmodule
