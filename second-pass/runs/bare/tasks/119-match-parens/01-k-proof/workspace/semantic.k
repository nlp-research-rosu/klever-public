module MPY-SYNTAX
  imports INT-SYNTAX
  imports BOOL-SYNTAX
  imports STRING-SYNTAX

  syntax Pgm ::= "Module" "(" Stmts ")"

  syntax Stmts ::= List{Stmt, ""}
  syntax Strings ::= List{String, ","}
  syntax Params ::= "Params" "(" Strings ")"

  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"
                | "Return" "(" Expr ")"

  syntax Exprs ::= List{Expr, ","}
  syntax CmpOps ::= List{CmpOp, ","}
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"
  syntax Bound ::= Expr | "NoBound"
  syntax Slice ::= "Slice" "(" Bound "," Bound "," Bound ")"

  syntax Expr ::= "Name" "(" String ")"
                | "Int" "(" Int ")"
                | "Bool" "(" Bool ")"
                | "Str" "(" String ")"
                | "ListExpr" "(" Exprs ")"
                | "BinOp" "(" String "," Expr "," Expr ")"
                | "Compare" "(" Expr "," CmpOps ")"
                | "Subscript" "(" Expr "," Expr ")"
                | "Subscript" "(" Expr "," Slice ")"
                | "Call" "(" Expr "," Exprs ")"
endmodule

module MPY-RUNTIME-SYNTAX
  imports MPY-SYNTAX
  imports INT
  imports BOOL
  imports STRING
  imports MAP
  imports LIST

  // Parenthesis strings are inductive in the proof model.  Source String
  // tokens are converted to this representation by chars.
  syntax PString ::= ".PString"
                   | "lp" PString
                   | "rp" PString

  syntax PyString ::= "parens" "(" PString ")"
                    | "yesString"
                    | "noString"

  syntax Value ::= "intVal" "(" Int ")"
                 | "boolVal" "(" Bool ")"
                 | "strVal" "(" PyString ")"
                 | "listVal" "(" Values ")"
                 | "closure" "(" String "," Params "," Stmts ")"
  syntax Values ::= List{Value, ","}

  // PStr is a verification-only literal.  It lets a claim quantify over an
  // arbitrary inductive parenthesis string without changing py2mpy.py.
  syntax Expr ::= "PStr" "(" PString ")"

  syntax KItem ::= "exec" "(" Stmts ")"
                 | "eval" "(" Expr ")"
                 | "binRight" "(" String "," Expr ")"
                 | "binApply" "(" String "," Value ")"
                 | "compareRight" "(" String "," Expr ")"
                 | "compareApply" "(" String "," Value ")"
                 | "indexAt" "(" Int ")"
                 | "sliceTail"
                 | "listSecond" "(" Expr ")"
                 | "makeList2" "(" Value ")"
                 | "callOne" "(" Expr ")"
                 | "callOneApply" "(" Value ")"
                 | "callTwoFirst" "(" Expr "," Expr ")"
                 | "callTwoSecond" "(" Value "," Expr ")"
                 | "callTwoApply" "(" Value "," Value ")"
                 | "invoke" "(" Value "," Values ")"
                 | "choose" "(" Stmts "," Stmts ")"
                 | "returnFrom"
                 | "returned" "(" Value ")"
                 | "finishCall" "(" Map ")"
                 | "launch"
                 | "invokeEntry"

  syntax PString ::= "chars" "(" String ")" [function]
                   | "pconcat" "(" PString "," PString ")" [function]
                   | "ptail" "(" PString ")" [function]
  syntax PyString ::= "literalString" "(" String ")" [function]
                    | "stringPlus" "(" PyString "," PyString ")" [function]
                    | "stringHead" "(" PyString ")" [function]
                    | "stringTail" "(" PyString ")" [function]
  syntax Bool ::= "valueEq" "(" Value "," Value ")" [function]
                | "pstringEq" "(" PString "," PString ")" [function]

endmodule

module MPY-SEMANTICS
  imports MPY-RUNTIME-SYNTAX

  configuration
    <mpy>
      <k> $PGM:Pgm </k>
      <input> $INPUT:Expr </input>
      <env> .Map </env>
      <functions> .Map </functions>
      <result> noResult </result>
    </mpy>

  syntax Result ::= "noResult" | Value

  // Loading a module records its function definitions and then calls the
  // HumanEval entry point with the configured input expression.
  rule <k> Module(SS) => exec(SS) ~> launch ... </k>

  rule <k> exec(.Stmts) => .K ... </k>
  rule <k> exec(FuncDef(F, PS, BODY) REST)
        => exec(REST) ... </k>
       <functions> FS => FS [ F <- closure(F, PS, BODY) ] </functions>

  rule <k> exec(If(COND, THEN, ELSE) REST)
        => eval(COND) ~> choose(THEN, ELSE) ~> exec(REST) ... </k>
  rule <k> boolVal(true) ~> choose(THEN, _) => exec(THEN) ... </k>
  rule <k> boolVal(false) ~> choose(_, ELSE) => exec(ELSE) ... </k>

  rule <k> exec(Return(E) _REST) => eval(E) ~> returnFrom ... </k>
  rule <k> V:Value ~> returnFrom => returned(V) ... </k>
  // A return discards pending statement continuations in the current call.
  rule <k> returned(V) ~> exec(_) => returned(V) ... </k>

  // Expressions.
  rule <k> eval(Int(I)) => intVal(I) ... </k>
  rule <k> eval(Bool(B)) => boolVal(B) ... </k>
  rule <k> eval(Str(S)) => strVal(literalString(S)) ... </k>
  rule <k> eval(PStr(S)) => strVal(parens(S)) ... </k>
  rule <k> eval(Name(X)) => V ... </k> <env> ... X |-> V ... </env>
  rule <k> eval(Name(X)) => V ... </k> <functions> ... X |-> V ... </functions>

  rule <k> eval(BinOp(OP, L, R)) => eval(L) ~> binRight(OP, R) ... </k>
  rule <k> V:Value ~> binRight(OP, R) => eval(R) ~> binApply(OP, V) ... </k>
  rule <k> intVal(J) ~> binApply("+", intVal(I)) => intVal(I +Int J) ... </k>
  rule <k> intVal(J) ~> binApply("-", intVal(I)) => intVal(I -Int J) ... </k>
  rule <k> strVal(B) ~> binApply("+", strVal(A))
        => strVal(stringPlus(A, B)) ... </k>

  // The translated solution only uses one-link comparison chains.
  rule <k> eval(Compare(L, CmpOp(OP, R)))
        => eval(L) ~> compareRight(OP, R) ... </k>
  rule <k> V:Value ~> compareRight(OP, R)
        => eval(R) ~> compareApply(OP, V) ... </k>
  rule <k> V2:Value ~> compareApply("==", V1)
        => boolVal(valueEq(V1, V2)) ... </k>
  rule <k> intVal(J) ~> compareApply("<", intVal(I))
        => boolVal(I <Int J) ... </k>

  rule <k> eval(Subscript(E, Int(I))) => eval(E) ~> indexAt(I) ... </k>
  rule <k> listVal(V:Value, _VS:Values) ~> indexAt(0) => V ... </k>
  rule <k> listVal(_V:Value, VS:Values) ~> indexAt(I)
        => listVal(VS) ~> indexAt(I -Int 1) ... </k>
    requires I >Int 0
  rule <k> strVal(S) ~> indexAt(0) => strVal(stringHead(S)) ... </k>

  rule <k> eval(Subscript(E, Slice(Int(1), NoBound, NoBound)))
        => eval(E) ~> sliceTail ... </k>
  rule <k> strVal(S) ~> sliceTail => strVal(stringTail(S)) ... </k>

  rule <k> eval(ListExpr(E1:Expr, E2:Expr, .Exprs))
        => eval(E1) ~> listSecond(E2) ... </k>
  rule <k> V1:Value ~> listSecond(E2) => eval(E2) ~> makeList2(V1) ... </k>
  rule <k> V2:Value ~> makeList2(V1) => listVal(V1, V2, .Values) ... </k>

  rule <k> eval(Call(F, E1:Expr, .Exprs)) => eval(F) ~> callOne(E1) ... </k>
  rule <k> FV:Value ~> callOne(E1) => eval(E1) ~> callOneApply(FV) ... </k>
  rule <k> V1:Value ~> callOneApply(FV) => invoke(FV, V1) ... </k>
  rule <k> eval(Call(F, E1:Expr, E2:Expr, .Exprs))
        => eval(F) ~> callTwoFirst(E1, E2) ... </k>
  rule <k> FV:Value ~> callTwoFirst(E1, E2)
        => eval(E1) ~> callTwoSecond(FV, E2) ... </k>
  rule <k> V1:Value ~> callTwoSecond(FV, E2)
        => eval(E2) ~> callTwoApply(FV, V1) ... </k>
  rule <k> V2:Value ~> callTwoApply(FV, V1) => invoke(FV, V1, V2) ... </k>

  // The two arities needed by solution.py.  A call has a fresh local map;
  // finishCall restores the caller's map after normal or explicit return.
  rule <k> invoke(closure(_, Params(X:String, .Strings), BODY), V:Value, .Values)
        => exec(BODY) ~> finishCall(OLD) ... </k>
       <env> OLD => X |-> V </env>
  rule <k> invoke(closure(_, Params(X:String, Y:String, .Strings), BODY),
                  V1:Value, V2:Value, .Values)
        => exec(BODY) ~> finishCall(OLD) ... </k>
       <env> OLD => X |-> V1 Y |-> V2 </env>
  rule <k> returned(V) ~> finishCall(OLD) => V ... </k>
       <env> _ => OLD </env>

  rule <k> launch => eval(IN) ~> invokeEntry ... </k> <input> IN </input>
  rule <k> V:Value ~> invokeEntry => invoke(F, V) ... </k>
       <functions> ... "match_parens" |-> F ... </functions>
  rule <k> V:Value => .K </k> <result> noResult => V </result>

  // Concrete literal conversion.  chars is defined only for the input
  // alphabet promised by the HumanEval task.
  rule literalString("Yes") => yesString
  rule literalString("No") => noString
  rule literalString(S) => parens(chars(S))
    requires S =/=String "Yes" andBool S =/=String "No"

  rule chars("") => .PString
  rule chars(S) => lp chars(substrString(S, 1, lengthString(S)))
    requires lengthString(S) >Int 0
     andBool substrString(S, 0, 1) ==String "("
  rule chars(S) => rp chars(substrString(S, 1, lengthString(S)))
    requires lengthString(S) >Int 0
     andBool substrString(S, 0, 1) ==String ")"

  rule pconcat(.PString, T) => T
  rule pconcat(lp S, T) => lp pconcat(S, T)
  rule pconcat(rp S, T) => rp pconcat(S, T)
  rule stringPlus(parens(A), parens(B)) => parens(pconcat(A, B))

  rule stringHead(parens(lp _S)) => parens(lp .PString)
  rule stringHead(parens(rp _S)) => parens(rp .PString)
  rule stringTail(parens(lp S)) => parens(S)
  rule stringTail(parens(rp S)) => parens(S)

  rule valueEq(intVal(I), intVal(J)) => I ==Int J
  rule valueEq(boolVal(B), boolVal(C)) => B ==Bool C
  rule valueEq(strVal(parens(A)), strVal(parens(B))) => pstringEq(A, B)
  rule valueEq(strVal(yesString), strVal(yesString)) => true
  rule valueEq(strVal(noString), strVal(noString)) => true
  rule valueEq(strVal(yesString), strVal(noString)) => false
  rule valueEq(strVal(noString), strVal(yesString)) => false

  rule pstringEq(.PString, .PString) => true
  rule pstringEq(.PString, lp _) => false
  rule pstringEq(.PString, rp _) => false
  rule pstringEq(lp _, .PString) => false
  rule pstringEq(rp _, .PString) => false
  rule pstringEq(lp A, lp B) => pstringEq(A, B)
  rule pstringEq(rp A, rp B) => pstringEq(A, B)
  rule pstringEq(lp _, rp _) => false
  rule pstringEq(rp _, lp _) => false
endmodule

module SEMANTIC
  imports MPY-SEMANTICS
endmodule
