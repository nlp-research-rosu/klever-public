module MPY-SYNTAX
  imports INT
  imports STRING

  syntax ParamList ::= List{String, ","}
  syntax Params ::= "Params" "(" ParamList ")"

  syntax Expr ::= "Name" "(" String ")"
                | "Int" "(" Int ")"
                | "Str" "(" String ")"
                | "Attribute" "(" Expr "," String ")"
                | "Call" "(" Expr "," Expr ")"
                | "Subscript" "(" Expr "," Expr ")"
                | "BinOp" "(" String "," Expr "," Expr ")"
                | "Compare" "(" Expr "," CmpOp ")"
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"

  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "Assign" "(" Expr "," Expr ")"
                | "Return" "(" Expr ")"
  syntax Stmts ::= List{Stmt, ""}
  syntax Module ::= "Module" "(" Stmts ")"

  syntax PyVal ::= "intVal" "(" Int ")"
                 | "boolVal" "(" Bool ")"
                 | "strVal" "(" String ")"
                 | "pairList" "(" PyVal "," PyVal ")"
                 | "builtinInt"
                 | "splitMethod" "(" PyVal ")"
                 | "slashSplit" "(" String ")" [function]
  syntax Int ::= "decimalValue" "(" String ")" [function]
  syntax Expr ::= PyVal
  syntax PyVals ::= List{PyVal, ","}

  syntax Function ::= "function" "(" Params "," Stmts ")"
  syntax Result ::= "noResult" | "result" "(" PyVal ")"
endmodule

module SEMANTIC
  imports MPY-SYNTAX
  imports BOOL
  imports MAP

  configuration
    <simplify>
      <k> $PGM:Module ~> invoke("simplify", $ARGS:PyVals) </k>
      <functions> .Map </functions>
      <env> .Map </env>
      <result> noResult </result>
    </simplify>

  syntax KItem ::= "exec" "(" Stmts ")"
                 | "invoke" "(" String "," PyVals ")"
                 | "bind" "(" String ")"
                 | "finishReturn"
                 | "getAttribute" "(" String ")"
                 | "callWith" "(" Expr ")"
                 | "apply" "(" PyVal ")"
                 | "indexWith" "(" Expr ")"
                 | "indexApply" "(" PyVal ")"
                 | "binRight" "(" String "," Expr ")"
                 | "binApply" "(" String "," PyVal ")"
                 | "compareRight" "(" String "," Expr ")"
                 | "compareApply" "(" String "," PyVal ")"

  rule <k> Module(SS) => exec(SS) ... </k>
  rule <k> exec(.Stmts) => .K ... </k>
  rule <k> exec(S SS) => S ~> exec(SS) ... </k>

  rule <k> FuncDef(F, PS, BODY) => .K ... </k>
       <functions> FS => FS [ F <- function(PS, BODY) ] </functions>

  rule <k> invoke(F, V1:PyVal, V2:PyVal) => exec(BODY) ... </k>
       <functions> ... F |-> function(Params(X:String, Y:String), BODY) ... </functions>
       <env> _ => (X |-> V1) (Y |-> V2) </env>

  rule <k> Assign(Name(X), E) => E ~> bind(X) ... </k>
  rule <k> V:PyVal ~> bind(X) => .K ... </k>
       <env> RHO => RHO [ X <- V ] </env>

  rule <k> Return(E) => E ~> finishReturn ... </k>
  rule <k> V:PyVal ~> finishReturn ~> _REST => .K </k>
       <result> _ => result(V) </result>

  rule <k> Int(I) => intVal(I) ... </k>
  rule <k> Str(S) => strVal(S) ... </k>
  rule <k> Name("int") => builtinInt ... </k>
  rule <k> Name(X) => V ... </k>
       <env> ... X |-> V:PyVal ... </env>

  rule <k> Attribute(E, A) => E ~> getAttribute(A) ... </k>
  rule <k> V:PyVal ~> getAttribute("split") => splitMethod(V) ... </k>

  rule <k> Call(F, E) => F ~> callWith(E) ... </k>
  rule <k> V:PyVal ~> callWith(E) => E ~> apply(V) ... </k>
  rule <k> strVal("/") ~> apply(splitMethod(strVal(S)))
        => slashSplit(S) ... </k>
  rule slashSplit(S) =>
         pairList(
           strVal(substrString(S, 0, findString(S, "/", 0))),
           strVal(substrString(S, findString(S, "/", 0) +Int 1, lengthString(S))))
       requires findString(S, "/", 0) >=Int 0
       [owise]
  rule <k> strVal(S) ~> apply(builtinInt) => intVal(decimalValue(S)) ... </k>
  rule decimalValue(S) => String2Int(S) [owise]

  rule <k> Subscript(BASE, INDEX) => BASE ~> indexWith(INDEX) ... </k>
  rule <k> V:PyVal ~> indexWith(INDEX) => INDEX ~> indexApply(V) ... </k>
  rule <k> intVal(0) ~> indexApply(pairList(V0, _)) => V0 ... </k>
  rule <k> intVal(1) ~> indexApply(pairList(_, V1)) => V1 ... </k>

  rule <k> BinOp(OP, L, R) => L ~> binRight(OP, R) ... </k>
  rule <k> V:PyVal ~> binRight(OP, R) => R ~> binApply(OP, V) ... </k>
  rule <k> intVal(B) ~> binApply("*", intVal(A)) => intVal(A *Int B) ... </k>
  rule <k> intVal(B) ~> binApply("%", intVal(A)) => intVal(A %Int B) ... </k>
       requires B =/=Int 0

  rule <k> Compare(L, CmpOp(OP, R)) => L ~> compareRight(OP, R) ... </k>
  rule <k> V:PyVal ~> compareRight(OP, R) => R ~> compareApply(OP, V) ... </k>
  rule <k> intVal(B) ~> compareApply("==", intVal(A))
        => boolVal(A ==Int B) ... </k>
endmodule
