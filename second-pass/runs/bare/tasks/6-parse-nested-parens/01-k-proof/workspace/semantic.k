module MPY-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX
  imports BOOL-SYNTAX

  syntax Program ::= "Module" "(" Stmts ")"

  syntax Stmts ::= List{Stmt, ""}
  syntax Strs ::= List{String, ","}
  syntax Exprs ::= List{Expr, ","}
  syntax CmpOps ::= List{CmpOp, ","}

  syntax Params ::= "Params" "(" Strs ")"

  syntax Stmt ::= "ImportFrom" "(" String "," Strs ")"
                | "FuncDef" "(" String "," Params "," Stmts ")"
                | "Assign" "(" Expr "," Expr ")"
                | "AugAssign" "(" Expr "," String "," Expr ")"
                | "For" "(" Expr "," Expr "," Stmts ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"
                | "Expr" "(" Expr ")"
                | "Return" "(" Expr ")"

  syntax Expr ::= "Name" "(" String ")"
                | "Int" "(" Int ")"
                | "Str" "(" String ")"
                | "ListExpr" "(" Exprs ")"
                | "Attribute" "(" Expr "," String ")"
                | "Call" "(" Expr "," Exprs ")"
                | "Compare" "(" Expr "," CmpOps ")"

  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"
endmodule

module MPY-SEMANTICS
  imports MPY-SYNTAX
  imports INT
  imports STRING
  imports BOOL
  imports MAP

  // Python values needed by this program.  Lists are immutable values in the
  // environment; append is modeled by replacing the binding with a new list.
  syntax PyVal ::= "pyInt" "(" Int ")"
                 | "pyStr" "(" String ")"
                 | "pyBool" "(" Bool ")"
                 | "pyList" "(" PyVals ")"
  syntax PyVals ::= ".PyVals" | PyVal "::" PyVals

  syntax Result ::= "noResult" | "result" "(" PyVal ")"
  syntax Function ::= "function" "(" Params "," Stmts ")"

  syntax KItem ::= "start"
                 | "invoke" "(" String "," PyVal ")"
                 | "forValues" "(" String "," PyVals "," Stmts ")"
                 | "choose" "(" PyVal "," Stmts "," Stmts ")"

  configuration
    <mpy>
      <k> $PGM:Program </k>
      <input> $INPUT:String </input>
      <env> .Map </env>
      <functions> .Map </functions>
      <result> noResult </result>
    </mpy>

  // Module loading registers functions before the requested entry point runs.
  rule <k> Module(SS) => SS ~> start ... </k>
  rule <k> (S:Stmt SS:Stmts) => S ~> SS ... </k>
  rule <k> .Stmts => .K ... </k>

  rule <k> ImportFrom(_, _) => .K ... </k>
  rule <k> FuncDef(F, PS, BODY) => .K ... </k>
       <functions> FS => FS [ F <- function(PS, BODY) ] </functions>

  rule <k> start => invoke("parse_nested_parens", pyStr(S)) ... </k>
       <input> S </input>

  rule <k> invoke(F, ARG) => BODY ... </k>
       <functions> ... F |-> function(Params(P:String), BODY) ... </functions>
       <env> _ => P |-> ARG </env>

  // Statement execution.
  rule <k> Assign(Name(X), E) => .K ... </k>
       <env> ENV => ENV [ X <- eval(E, ENV) ] </env>

  rule <k> AugAssign(Name(X), "+", E) => .K ... </k>
       <env> ENV => ENV [ X <- addPy(lookupPy(X, ENV), eval(E, ENV)) ] </env>

  rule <k> AugAssign(Name(X), "-", E) => .K ... </k>
       <env> ENV => ENV [ X <- subPy(lookupPy(X, ENV), eval(E, ENV)) ] </env>

  rule <k> If(E, THEN, ELSE) => choose(eval(E, ENV), THEN, ELSE) ... </k>
       <env> ENV </env>
  rule <k> choose(pyBool(true), THEN, _) => THEN ... </k>
  rule <k> choose(pyBool(false), _, ELSE) => ELSE ... </k>

  rule <k> For(Name(X), E, BODY) => forValues(X, iterable(eval(E, ENV)), BODY) ... </k>
       <env> ENV </env>
  rule <k> forValues(_, .PyVals, _) => .K ... </k>
  rule <k> forValues(X, V :: VS, BODY) => BODY ~> forValues(X, VS, BODY) ... </k>
       <env> ENV => ENV [ X <- V ] </env>

  rule <k> Expr(Call(Attribute(Name(X), "append"), E)) => .K ... </k>
       <env> ENV => ENV [ X <- appendPy(lookupPy(X, ENV), eval(E, ENV)) ] </env>

  rule <k> Return(E) ~> _ => .K </k>
       <env> ENV => .Map </env>
       <functions> _ => .Map </functions>
       <result> noResult => result(eval(E, ENV)) </result>

  // Pure expression evaluator.
  syntax PyVal ::= "eval" "(" Expr "," Map ")" [function]
  syntax PyVal ::= "lookupPy" "(" String "," Map ")" [function]
  rule lookupPy(X, (X |-> V:PyVal) _REST) => V

  rule eval(Int(I), _) => pyInt(I)
  rule eval(Str(S), _) => pyStr(S)
  rule eval(Name(X), ENV) => lookupPy(X, ENV)
  rule eval(ListExpr(.Exprs), _) => pyList(.PyVals)
  rule eval(Call(Attribute(E, "split"), Str(" ")), ENV)
    => pyList(splitSpaces(stringOf(eval(E, ENV))))
  rule eval(Compare(E1, CmpOp("==", E2)), ENV)
    => pyBool(eqPy(eval(E1, ENV), eval(E2, ENV)))
  rule eval(Compare(E1, CmpOp(">", E2)), ENV)
    => pyBool(gtPy(eval(E1, ENV), eval(E2, ENV)))

  syntax String ::= "stringOf" "(" PyVal ")" [function]
  rule stringOf(pyStr(S)) => S

  syntax Bool ::= "truth" "(" PyVal ")" [function]
  rule truth(pyBool(B)) => B

  syntax Bool ::= "eqPy" "(" PyVal "," PyVal ")" [function]
  rule eqPy(pyStr(A), pyStr(B)) => A ==String B
  rule eqPy(pyInt(A), pyInt(B)) => A ==Int B

  syntax Bool ::= "gtPy" "(" PyVal "," PyVal ")" [function]
  rule gtPy(pyInt(A), pyInt(B)) => A >Int B

  syntax PyVal ::= "addPy" "(" PyVal "," PyVal ")" [function]
  rule addPy(pyInt(A), pyInt(B)) => pyInt(A +Int B)

  syntax PyVal ::= "subPy" "(" PyVal "," PyVal ")" [function]
  rule subPy(pyInt(A), pyInt(B)) => pyInt(A -Int B)

  syntax PyVal ::= "appendPy" "(" PyVal "," PyVal ")" [function]
  rule appendPy(pyList(VS), V) => pyList(appendVals(VS, V))

  syntax PyVals ::= "appendVals" "(" PyVals "," PyVal ")" [function]
  rule appendVals(.PyVals, V) => V :: .PyVals
  rule appendVals(H :: T, V) => H :: appendVals(T, V)

  syntax PyVals ::= "iterable" "(" PyVal ")" [function]
  rule iterable(pyList(VS)) => VS
  rule iterable(pyStr(S)) => chars(S)

  syntax PyVals ::= "chars" "(" String ")" [function]
  rule chars("") => .PyVals
  rule chars(S) => pyStr(substrString(S, 0, 1))
                   :: chars(substrString(S, 1, lengthString(S)))
       requires lengthString(S) >Int 0

  // Python's explicit-separator split retains empty fields.
  syntax PyVals ::= "splitSpaces" "(" String ")" [function]
  rule splitSpaces(S) => pyStr(S) :: .PyVals
       requires findString(S, " ", 0) <Int 0
  rule splitSpaces(S) => pyStr(substrString(S, 0, findString(S, " ", 0)))
                         :: splitSpaces(substrString(S,
                              findString(S, " ", 0) +Int 1,
                              lengthString(S)))
       requires findString(S, " ", 0) >=Int 0
endmodule
