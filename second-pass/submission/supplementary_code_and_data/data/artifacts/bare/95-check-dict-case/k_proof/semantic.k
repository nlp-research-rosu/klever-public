// A small, task-oriented executable semantics for the exact constructor
// language emitted by py2mpy.py.  The semantics below is not a translation of
// the answer: it evaluates names, assignment, conditionals, for loops,
// returns, Boolean operations, calls, dictionaries, and Python's relevant
// string predicates.

module MPY-SYNTAX
  imports BOOL-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX

  syntax PyStmt  ::= "Module" "(" PyStmts ")"
                   | "FuncDef" "(" String "," Params "," PyStmts ")"
                   | "Assign" "(" PyExpr "," PyExpr ")"
                   | "If" "(" PyExpr "," PyStmts "," PyStmts ")"
                   | "If" "(" PyExpr "," PyStmts "," ")" [symbol(IfNoElse)]
                   | "For" "(" PyExpr "," PyExpr "," PyStmts ")"
                   | "Return" "(" PyExpr ")"
  syntax PyStmts ::= PyStmt
                   | PyStmt PyStmts

  syntax Params   ::= "Params" "(" Strings ")"
  syntax Strings  ::= NeList{String, ","}

  syntax PyExpr   ::= "Name" "(" String ")"
                   | "Bool" "(" Bool ")"
                   | "UnaryOp" "(" String "," PyExpr ")"
                   | "BoolOp" "(" String "," PyExprs ")"
                   | "Call" "(" PyExpr "," PyExprs ")"
                   | "Call" "(" PyExpr "," ")" [symbol(CallNoArgs)]
                   | "Attribute" "(" PyExpr "," String ")"
  syntax PyExprs  ::= NeList{PyExpr, ","}
endmodule

module MPY-VALUES
  imports BOOL
  imports INT
  imports STRING

  // DictVal records dictionary keys in iteration order.  Values are omitted
  // because this task never observes them.  Repeated keys are harmless for
  // the property, while a real Python dictionary presents only the last one.
  syntax Value  ::= "NoneVal"
                  | "BoolVal" "(" Bool ")"
                  | "StrVal" "(" String ")"
                  | "IntVal" "(" Int ")"
                  | "DictVal" "(" ")" [symbol(EmptyDictVal)]
                  | "DictVal" "(" Values ")"
  syntax Values ::= Value
                  | Value Values
endmodule

module MPY
  imports MPY-SYNTAX
  imports MPY-VALUES
  imports MAP

  configuration
    <task>
      <k> $PGM:PyStmt </k>
      <input> $INPUT:Value </input>
      <env> .Map </env>
      <result> NoneVal </result>
    </task>

  // Enter the requested top-level function with one fresh local frame.
  rule <k> Module(FuncDef("check_dict_case", Params("dict"), BODY))
        => BODY ...</k>
       <input> ARG </input>
       <env> .Map => "dict" |-> ARG </env>

  // Statement-list scheduling.
  rule <k> (S:PyStmt REST:PyStmts) => S ~> REST ...</k>

  syntax KItem ::= eval(PyExpr)
                 | assignTo(String)
                 | choose(PyStmts, PyStmts)
                 | chooseNoElse(PyStmts)
                 | startFor(String, PyStmts)
                 | loop(String, Values, PyStmts)
                 | bind(String, Value)
                 | "logicalNot"
                 | logicalOr(PyExpr)
                 | "returnValue"

  // Statements evaluate their subexpressions before applying effects.
  rule <k> Assign(Name(X), E) => eval(E) ~> assignTo(X) ...</k>
  rule <k> V:Value ~> assignTo(X) => .K ...</k>
       <env> ENV => ENV [ X <- V ] </env>

  rule <k> If(COND, THEN, ELSE) => eval(COND) ~> choose(THEN, ELSE) ...</k>
  rule <k> BoolVal(true)  ~> choose(THEN, _) => THEN ...</k>
  rule <k> BoolVal(false) ~> choose(_, ELSE) => ELSE ...</k>
  rule <k> If(COND, THEN, ) => eval(COND) ~> chooseNoElse(THEN) ...</k>
  rule <k> BoolVal(true)  ~> chooseNoElse(THEN) => THEN ...</k>
  rule <k> BoolVal(false) ~> chooseNoElse(_) => .K ...</k>

  rule <k> For(Name(X), ITER, BODY) => eval(ITER) ~> startFor(X, BODY) ...</k>
  rule <k> DictVal() ~> startFor(_, _) => .K ...</k>
  rule <k> DictVal(KEYS) ~> startFor(X, BODY) => loop(X, KEYS, BODY) ...</k>
  rule <k> loop(X, (V:Value VS:Values), BODY)
        => bind(X, V) ~> BODY ~> loop(X, VS, BODY) ...</k>
  rule <k> loop(X, V:Value, BODY) => bind(X, V) ~> BODY ...</k>
  rule <k> bind(X, V) => .K ...</k>
       <env> ENV => ENV [ X <- V ] </env>

  rule <k> Return(E) => eval(E) ~> returnValue ...</k>
  rule <k> V:Value ~> returnValue ~> _REST => .K </k>
       <env> _ => .Map </env>
       <result> _ => V </result>

  // Literal and local-name expression evaluation.
  rule <k> eval(Bool(B)) => BoolVal(B) ...</k>
  rule <k> eval(Name(X)) => V ...</k>
       <env>... X |-> V ...</env>

  // Python truthiness needed by `not dict`, plus ordinary Boolean negation.
  rule <k> eval(UnaryOp("not", E)) => eval(E) ~> logicalNot ...</k>
  rule <k> BoolVal(B) ~> logicalNot => BoolVal(notBool B) ...</k>
  rule <k> DictVal() ~> logicalNot => BoolVal(true) ...</k>
  rule <k> DictVal(_V:Value _VS:Values) ~> logicalNot => BoolVal(false) ...</k>
  rule <k> DictVal(_V:Value) ~> logicalNot => BoolVal(false) ...</k>

  // The solution has a two-operand `or`; this is short-circuit evaluation.
  rule <k> eval(BoolOp("or", E1, E2)) => eval(E1) ~> logicalOr(E2) ...</k>
  rule <k> BoolVal(true) ~> logicalOr(_) => BoolVal(true) ...</k>
  rule <k> BoolVal(false) ~> logicalOr(E) => eval(E) ...</k>

  // Built-in calls used by the source program.  Directly reading the receiver
  // from the environment preserves the evaluation behavior of these pure,
  // zero-argument string methods.
  rule <k> eval(Call(Name("isinstance"), Name(X), Name("str")))
        => BoolVal(pyIsString(V)) ...</k>
       <env>... X |-> V ...</env>

  rule <k> eval(Call(Attribute(Name(X), "islower"), ))
        => BoolVal(pyIsLower(V)) ...</k>
       <env>... X |-> V ...</env>
  rule <k> eval(Call(Attribute(Name(X), "isupper"), ))
        => BoolVal(pyIsUpper(V)) ...</k>
       <env>... X |-> V ...</env>

  syntax Bool ::= pyIsString(Value) [function, total]
  rule pyIsString(StrVal(_)) => true
  rule pyIsString(IntVal(_)) => false
  rule pyIsString(BoolVal(_)) => false
  rule pyIsString(DictVal(_)) => false
  rule pyIsString(DictVal()) => false
  rule pyIsString(NoneVal) => false

  // CPython's islower/isupper criterion is: at least one cased character and
  // every cased character has the requested case.  The proof model classifies
  // ASCII letters explicitly; all other code points are uncased.  This is the
  // relevant string domain for the HumanEval prompt and avoids K's deprecated
  // STRING.category hook, which is unavailable to the proof backend.
  syntax Bool ::= pyIsLower(Value) [function]
                | pyIsUpper(Value) [function]
                | lowerScan(String, Int, Bool) [function]
                | upperScan(String, Int, Bool) [function]

  rule pyIsLower(StrVal(S)) => lowerScan(S, 0, false)
  rule pyIsUpper(StrVal(S)) => upperScan(S, 0, false)

  rule lowerScan(S, I, SEEN) => SEEN
    requires I >=Int lengthString(S)
  rule lowerScan(S, I, _) => false
    requires I <Int lengthString(S)
     andBool ordChar(substrString(S, I, I +Int 1)) >=Int 65
     andBool ordChar(substrString(S, I, I +Int 1)) <=Int 90
  rule lowerScan(S, I, _) => lowerScan(S, I +Int 1, true)
    requires I <Int lengthString(S)
     andBool ordChar(substrString(S, I, I +Int 1)) >=Int 97
     andBool ordChar(substrString(S, I, I +Int 1)) <=Int 122
  rule lowerScan(S, I, SEEN) => lowerScan(S, I +Int 1, SEEN)
    requires I <Int lengthString(S)
     andBool (ordChar(substrString(S, I, I +Int 1)) <Int 65
       orBool ordChar(substrString(S, I, I +Int 1)) >Int 122
       orBool (ordChar(substrString(S, I, I +Int 1)) >Int 90
         andBool ordChar(substrString(S, I, I +Int 1)) <Int 97))

  rule upperScan(S, I, SEEN) => SEEN
    requires I >=Int lengthString(S)
  rule upperScan(S, I, _) => false
    requires I <Int lengthString(S)
     andBool ordChar(substrString(S, I, I +Int 1)) >=Int 97
     andBool ordChar(substrString(S, I, I +Int 1)) <=Int 122
  rule upperScan(S, I, _) => upperScan(S, I +Int 1, true)
    requires I <Int lengthString(S)
     andBool ordChar(substrString(S, I, I +Int 1)) >=Int 65
     andBool ordChar(substrString(S, I, I +Int 1)) <=Int 90
  rule upperScan(S, I, SEEN) => upperScan(S, I +Int 1, SEEN)
    requires I <Int lengthString(S)
     andBool (ordChar(substrString(S, I, I +Int 1)) <Int 65
       orBool ordChar(substrString(S, I, I +Int 1)) >Int 122
       orBool (ordChar(substrString(S, I, I +Int 1)) >Int 90
         andBool ordChar(substrString(S, I, I +Int 1)) <Int 97))
endmodule
