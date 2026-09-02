module MPY-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX
  imports BOOL-SYNTAX

  syntax #Layout ::= r"[ \n\r\t]+"

  syntax Pgm ::= "Module" "(" Stmts ")"

  syntax Stmts ::= Stmt
                 | Stmt Stmts
  syntax Exprs ::= List{Expr, ","}

  syntax Params ::= "Params" "(" String ")"
  syntax CmpPart ::= "CmpOp" "(" String "," Expr ")"

  syntax Stmt ::= "ImportFrom" "(" String "," String ")"
                | "FuncDef" "(" String "," Params "," Stmts ")"
                | "Assign" "(" Expr "," Expr ")"
                | "For" "(" Expr "," Expr "," Stmts ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"
                | "Return" "(" Expr ")"

  syntax Expr ::= "Name" "(" String ")"
                | "Str" "(" String ")"
                | "Int" "(" Int ")"
                | "ListExpr" "(" Exprs ")"
                | "Attribute" "(" Expr "," String ")"
                | "Call" "(" Expr "," Exprs ")"
                | "Compare" "(" Expr "," CmpPart ")"
                | "BinOp" "(" String "," Expr "," Expr ")"
endmodule

module MPY
  imports MPY-SYNTAX
  imports INT
  imports STRING
  imports BOOL
  imports MAP
  imports LIST

  syntax PyValue ::= "pyInt" "(" Int ")"
                   | "pyStr" "(" String ")"
                   | "pyBool" "(" Bool ")"
                   | "pyList" "(" List ")"
                   | "noResult"

  syntax Function ::= "function" "(" String "," Stmts ")"

  syntax KItem ::= "invoke" "(" String "," PyValue ")"
                 | "store" "(" String ")"
                 | "finishReturn"
                 | "prepareMethod" "(" String "," Expr ")"
                 | "applyMethod" "(" String "," PyValue ")"
                 | "compareRight" "(" String "," Expr ")"
                 | "compareApply" "(" String "," PyValue ")"
                 | "binRight" "(" String "," Expr ")"
                 | "binApply" "(" String "," PyValue ")"
                 | "choose" "(" Stmts "," Stmts ")"
                 | "startFor" "(" String "," Stmts ")"
                 | "loop" "(" String "," List "," Stmts ")"
                 | "bind" "(" String "," PyValue ")"

  configuration
    <mpy>
      <k> $PGM:Pgm ~> invoke("parse_music", pyStr($INPUT:String)) </k>
      <functions> .Map </functions>
      <env> .Map </env>
      <result> noResult </result>
    </mpy>

  // Module loading. A juxtaposed source statement list becomes K sequencing.
  rule <k> Module(SS) => SS ... </k>
  rule <k> S:Stmt SS:Stmts => S ~> SS ... </k>

  rule <k> ImportFrom(_, _) => .K ... </k>
  rule <k> FuncDef(F, Params(P), BODY) => .K ... </k>
       <functions> FS => FS [ F <- function(P, BODY) ] </functions>

  rule <k> invoke(F, ARG) => BODY ... </k>
       <functions> ... F |-> function(P, BODY) ... </functions>
       <env> _ => P |-> ARG </env>

  // Statements used by solution.py.
  rule <k> Assign(Name(X), E) => E ~> store(X) ... </k>
  rule <k> V:PyValue ~> store(X) => .K ... </k>
       <env> ENV => ENV [ X <- V ] </env>

  rule <k> Return(E) => E ~> finishReturn ... </k>
  rule <k> V:PyValue ~> finishReturn => .K ... </k>
       <result> _ => V </result>

  rule <k> If(COND, THEN, ELSE) => COND ~> choose(THEN, ELSE) ... </k>
  rule <k> pyBool(true) ~> choose(THEN, _) => THEN ... </k>
  rule <k> pyBool(false) ~> choose(_, ELSE) => ELSE ... </k>

  rule <k> For(Name(X), ITER, BODY) => ITER ~> startFor(X, BODY) ... </k>
  rule <k> pyList(L) ~> startFor(X, BODY) => loop(X, L, BODY) ... </k>
  rule <k> loop(_, .List, _) => .K ... </k>
  rule <k> loop(X, ListItem(V:PyValue) REST, BODY)
        => bind(X, V) ~> BODY ~> loop(X, REST, BODY) ... </k>
  rule <k> bind(X, V) => .K ... </k>
       <env> ENV => ENV [ X <- V ] </env>

  // Literals, variables, and the only list literals needed by this program.
  rule <k> Int(I) => pyInt(I) ... </k>
  rule <k> Str(S) => pyStr(S) ... </k>
  rule <k> Name(X) => V ... </k>
       <env> ... X |-> V:PyValue ... </env>
  rule <k> ListExpr(.Exprs) => pyList(.List) ... </k>
  rule <k> ListExpr(Int(I)) => pyList(ListItem(pyInt(I))) ... </k>

  // Python's explicit-separator str.split(" "). This preserves empty fields,
  // exactly as CPython does for an explicit separator.
  syntax List ::= "splitWords" "(" String ")" [function]
  // Constructor-prefix equations make the behavior on each legal token
  // symbolic as well as concrete. They are instances of the general rules
  // below because the first separator is at the displayed position.
  rule splitWords("o " +String S) =>
       ListItem(pyStr("o")) splitWords(S) [simplification]
  rule splitWords("o| " +String S) =>
       ListItem(pyStr("o|")) splitWords(S) [simplification]
  rule splitWords(".| " +String S) =>
       ListItem(pyStr(".|")) splitWords(S) [simplification]
  rule splitWords(S) => ListItem(pyStr(S))
       requires findString(S, " ", 0) ==Int -1
  rule splitWords(S) =>
       ListItem(pyStr(substrString(S, 0, findString(S, " ", 0))))
       splitWords(substrString(S, findString(S, " ", 0) +Int 1,
                               lengthString(S)))
       requires findString(S, " ", 0) >=Int 0

  rule <k> Call(Attribute(E, "split"), ARG) =>
             E ~> prepareMethod("split", ARG) ... </k>
  rule <k> RECEIVER:PyValue ~> prepareMethod(METHOD, ARG) =>
             ARG ~> applyMethod(METHOD, RECEIVER) ... </k>
  rule <k> pyStr(" ") ~> applyMethod("split", pyStr(S)) =>
             pyList(splitWords(S)) ... </k>

  // Equality and list concatenation.
  rule <k> Compare(E1, CmpOp(OP, E2)) =>
             E1 ~> compareRight(OP, E2) ... </k>
  rule <k> LEFT:PyValue ~> compareRight(OP, E2) =>
             E2 ~> compareApply(OP, LEFT) ... </k>
  rule <k> pyStr(RIGHT) ~> compareApply("==", pyStr(LEFT)) =>
             pyBool(LEFT ==String RIGHT) ... </k>

  rule <k> BinOp(OP, E1, E2) => E1 ~> binRight(OP, E2) ... </k>
  rule <k> LEFT:PyValue ~> binRight(OP, E2) =>
             E2 ~> binApply(OP, LEFT) ... </k>
  rule <k> pyList(RIGHT) ~> binApply("+", pyList(LEFT)) =>
             pyList(LEFT RIGHT) ... </k>
endmodule

module MPY-PROGRAM-PARSING
  imports MPY-SYNTAX
  imports PROGRAM-LISTS
endmodule
