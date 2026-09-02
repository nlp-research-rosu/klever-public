requires "domains.md"

module MPY-SYNTAX
  imports STRING-SYNTAX
  imports INT-SYNTAX

  syntax Module ::= "Module" "(" Stmts ")"

  syntax Stmts ::= List{Stmt, ""}
  syntax Strings ::= List{String, ","}
  syntax Params ::= "Params" "(" Strings ")"

  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "Assign" "(" Expr "," Expr ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"
                | "Return" "(" Expr ")"

  syntax Exprs ::= List{Expr, ","}
  syntax CmpOps ::= List{CmpOp, ","}

  syntax Expr ::= "Name" "(" String ")"
                | "Str" "(" String ")"
                | "Int" "(" Int ")"
                | "Attribute" "(" Expr "," String ")"
                | "Call" "(" Expr "," Exprs ")"
                | "Compare" "(" Expr "," CmpOps ")"
                | "BinOp" "(" String "," Expr "," Expr ")"

  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"
endmodule

module MPY-SEMANTIC
  imports MPY-SYNTAX
  imports DOMAINS

  // Runtime values. Lists contain Value elements wrapped with ListItem.
  syntax Value ::= "VStr" "(" String ")"
                 | "VInt" "(" Int ")"
                 | "VBool" "(" Bool ")"
                 | "VList" "(" List ")"
                 | "VAttr" "(" Value "," String ")"
  syntax Value ::= "iteValue" "(" Bool "," Value "," Value ")" [function]

  syntax Value ::= "eval" "(" Expr "," Map ")" [function]
  syntax Value ::= "call" "(" Value "," List ")" [function]
  syntax Value ::= "add" "(" Value "," Value ")" [function]
  syntax Value ::= "compare" "(" Value "," String "," Value ")" [function]
  syntax Bool  ::= "asBool" "(" Value ")" [function]

  rule eval(Name(X), (X |-> V:Value) _REST:Map) => V
  rule eval(Str(S), _) => VStr(S)
  rule eval(Int(I), _) => VInt(I)
  rule eval(Attribute(E, A), ENV) => VAttr(eval(E, ENV), A)
  rule eval(Call(F, .Exprs), ENV) => call(eval(F, ENV), .List)
  rule eval(Call(F, A:Expr), ENV) => call(eval(F, ENV), ListItem(eval(A, ENV)))
  rule eval(BinOp("+", L, R), ENV) => add(eval(L, ENV), eval(R, ENV))
  rule eval(Compare(L, CmpOp(OP, R)), ENV)
    => compare(eval(L, ENV), OP, eval(R, ENV))

  rule call(VAttr(VStr(S), "split"), .List) => VList(pySplitWhitespace(S))
  rule call(VAttr(VStr(S), "split"), ListItem(VStr(SEP)))
    => VList(pySplitOn(S, SEP))
  rule call(VAttr(VStr(SEP), "join"), ListItem(VList(VS)))
    => VStr(joinValues(SEP, VS))
  rule call(VAttr(VStr(S), "count"), ListItem(VStr(NEEDLE)))
    => VInt(countAllOccurrences(S, NEEDLE))

  rule add(VInt(I), VInt(J)) => VInt(I +Int J)
  rule compare(VStr(A), "!=", VStr(B)) => VBool(A =/=String B)
  rule compare(VStr(A), "in", VStr(B))
    => VBool(findString(B, A, 0) >=Int 0)
  rule asBool(VBool(B)) => B
  rule iteValue(true, THEN, _) => THEN
  rule iteValue(false, _, ELSE) => ELSE

  // Big-step statement execution with explicit return propagation.
  syntax Outcome ::= "normal" "(" Map ")"
                   | "returned" "(" Value ")"
  syntax Outcome ::= "iteOutcome" "(" Bool "," Outcome "," Outcome ")"
  syntax Outcome ::= "exec" "(" Stmts "," Map ")" [function]
                   | "execStmt" "(" Stmt "," Map ")" [function]
                   | "execRest" "(" Outcome "," Stmts ")" [function]

  rule exec(.Stmts, ENV) => normal(ENV)
  rule exec(S:Stmt SS:Stmts, ENV) => execRest(execStmt(S, ENV), SS)

  rule execRest(normal(ENV), SS) => exec(SS, ENV)
  rule execRest(returned(V), _) => returned(V)
  rule execRest(iteOutcome(B, THEN, ELSE), SS)
    => iteOutcome(B, execRest(THEN, SS), execRest(ELSE, SS))

  rule execStmt(Assign(Name(X), E), ENV) => normal(ENV [ X <- eval(E, ENV) ])
  rule execStmt(Return(E), ENV) => returned(eval(E, ENV))
  rule execStmt(If(COND, THEN, ELSE), ENV)
    => iteOutcome(
         asBool(eval(COND, ENV)), exec(THEN, ENV), exec(ELSE, ENV))

  // Python str.split() with no separator: collapse whitespace runs and omit
  // empty fields. This is the whitespace set recognized by CPython isspace().
  syntax Bool ::= "isWhitespace" "(" String ")" [function, total]
  rule isWhitespace(C)
    => findString(
         " \t\n\r\f\x0b\x1c\x1d\x1e\x1f\x85\xa0\u1680\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200a\u2028\u2029\u202f\u205f\u3000",
         C, 0) >=Int 0

  syntax List ::= "pySplitWhitespace" "(" String ")" [function]
                | "splitWhitespaceAt" "(" String "," Int "," String "," List ")" [function]
  rule pySplitWhitespace(S) => splitWhitespaceAt(S, 0, "", .List)
  rule splitWhitespaceAt(S, I, "", OUT) => OUT
    requires I >=Int lengthString(S)
  rule splitWhitespaceAt(S, I, WORD, OUT) => OUT ListItem(VStr(WORD))
    requires I >=Int lengthString(S) andBool WORD =/=String ""
  rule splitWhitespaceAt(S, I, "", OUT)
    => splitWhitespaceAt(S, I +Int 1, "", OUT)
    requires I <Int lengthString(S)
      andBool isWhitespace(substrString(S, I, I +Int 1))
  rule splitWhitespaceAt(S, I, WORD, OUT)
    => splitWhitespaceAt(S, I +Int 1, "", OUT ListItem(VStr(WORD)))
    requires I <Int lengthString(S)
      andBool WORD =/=String ""
      andBool isWhitespace(substrString(S, I, I +Int 1))
  rule splitWhitespaceAt(S, I, WORD, OUT)
    => splitWhitespaceAt(
         S, I +Int 1,
         WORD +String substrString(S, I, I +Int 1), OUT)
    requires I <Int lengthString(S)
      andBool notBool isWhitespace(substrString(S, I, I +Int 1))

  syntax String ::= "joinValues" "(" String "," List ")" [function]
                  | "joinValuesTail" "(" String "," List ")" [function]
  rule joinValues(_, .List) => ""
  rule joinValues(SEP, ListItem(VStr(S)) REST:List)
    => S +String joinValuesTail(SEP, REST)
  rule joinValuesTail(_, .List) => ""
  rule joinValuesTail(SEP, ListItem(VStr(S)) REST:List)
    => SEP +String S +String joinValuesTail(SEP, REST)

  // Python str.split(separator), including leading, trailing, and repeated
  // separators. The program calls this only with the nonempty string ",".
  syntax List ::= "pySplitOn" "(" String "," String ")" [function]
  rule pySplitOn(S, SEP) => ListItem(VStr(S))
    requires findString(S, SEP, 0) <Int 0
  rule pySplitOn(S, SEP)
    => ListItem(VStr(substrString(S, 0, findString(S, SEP, 0))))
       pySplitOn(
         substrString(
           S,
           findString(S, SEP, 0) +Int lengthString(SEP),
           lengthString(S)),
         SEP)
    requires findString(S, SEP, 0) >=Int 0
      andBool lengthString(SEP) >Int 0
endmodule
