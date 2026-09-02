requires "verification.k"

module MPY-SYNTAX
  imports STRING

  syntax Pgm ::= PyProgram

  syntax PyProgram ::= "Module" "(" PyStmts ")"
  syntax PyStmts ::= List{PyStmt, ""}

  syntax Params ::= "Params" "(" String ")"

  syntax PyStmt ::= "ImportFrom" "(" String "," String ")"
                  | "FuncDef" "(" String "," Params "," PyStmts ")"
                  | "Assign" "(" PyExpr "," PyExpr ")"
                  | "For" "(" PyExpr "," PyExpr "," PyStmts ")"
                  | "Return" "(" PyExpr ")"

  syntax PyExpr ::= "Name" "(" String ")"
                  | "Str" "(" String ")"
                  | "BinOp" "(" String "," PyExpr "," PyExpr ")"

  syntax StrList ::= ".StrList"
                   | String "::" StrList
  syntax PyVal ::= "sVal" "(" String ")"
                 | "lVal" "(" StrList ")"

  syntax Function ::= "noFunction"
                    | "function" "(" String "," String "," PyStmts ")"
  syntax Result ::= "noResult" | PyVal

  syntax KItem ::= "load" "(" PyProgram ")"
                 | "moduleLoaded"
                 | "invoke" "(" String "," PyVal ")"
                 | "assignTo" "(" String ")"
                 | "addLeft" "(" PyExpr ")"
                 | "addRight" "(" PyVal ")"
                 | "startFor" "(" String "," PyStmts ")"
                 | "loop" "(" String "," StrList "," PyStmts ")"
                 | "bindLoop" "(" String "," PyVal ")"
                 | "finishReturn"
                 | "cleanup"
endmodule

module MPY-SEMANTICS
  imports MPY-SYNTAX
  imports VERIFICATION

  configuration
    <py>
      <k> load($PGM:PyProgram) ~> invoke("concatenate", $ARG:PyVal) </k>
      <function> noFunction </function>
      <argument> lVal(.StrList) </argument>
      <accumulator> sVal("") </accumulator>
      <iterationItem> sVal("") </iterationItem>
      <result> noResult </result>
    </py>

  // Module loading.
  rule <k> load(Module(STMTS)) => STMTS ~> moduleLoaded ... </k>
  rule <k> .PyStmts => .K ... </k>
  rule <k> (S:PyStmt REST:PyStmts) => S ~> REST ... </k>
  rule <k> ImportFrom(_, _) => .K ... </k>
  rule <k> FuncDef(F, Params(P), BODY) => .K ... </k>
       <function> _ => function(F, P, BODY) </function>
  rule <k> moduleLoaded => .K ... </k>

  // The sole call frame needed by this first-order task.
  rule <k> invoke(F, ARG) => BODY ~> cleanup ... </k>
       <function> function(F, "strings", BODY) </function>
       <argument> _ => ARG </argument>

  // Expressions and assignment.
  rule <k> Str(S) => sVal(S) ... </k>
  rule <k> Name("strings") => V ... </k>
       <argument> V </argument>
  rule <k> Name("result") => V ... </k>
       <accumulator> V </accumulator>
  rule <k> Name("string") => V ... </k>
       <iterationItem> V </iterationItem>
  rule <k> Assign(Name(X), E) => E ~> assignTo(X) ... </k>
  rule <k> V:PyVal ~> assignTo("result") => .K ... </k>
       <accumulator> _ => V </accumulator>
  rule <k> BinOp("+", LEFT, RIGHT) => LEFT ~> addLeft(RIGHT) ... </k>
  rule <k> V:PyVal ~> addLeft(RIGHT) => RIGHT ~> addRight(V) ... </k>
  rule <k> sVal(S2) ~> addRight(sVal(S1)) => sVal(S1 +String S2) ... </k>

  // For loops consume the list from left to right and execute their body once
  // for each element.
  rule <k> For(Name(X), ITER, BODY) => ITER ~> startFor(X, BODY) ... </k>
  rule <k> lVal(ITEMS) ~> startFor(X, BODY) => loop(X, ITEMS, BODY) ... </k>
  rule <k> loop(_, .StrList, _) => .K ... </k>
  rule <k> loop(X, S :: REST, BODY)
        => bindLoop(X, sVal(S)) ~> BODY ~> loop(X, REST, BODY) ... </k>
  rule <k> bindLoop("string", V) => .K ... </k>
       <iterationItem> _ => V </iterationItem>

  // Return publishes a value; cleanup restores the call-local cells so that
  // claims can state a closed final configuration.
  rule <k> Return(E) => E ~> finishReturn ... </k>
  rule <k> V:PyVal ~> finishReturn => .K ... </k>
       <result> _ => V </result>
  rule <k> cleanup => .K ... </k>
       <function> _ => noFunction </function>
       <argument> _ => lVal(.StrList) </argument>
       <accumulator> _ => sVal("") </accumulator>
       <iterationItem> _ => sVal("") </iterationItem>
endmodule
