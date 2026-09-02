module MPY-SYNTAX
  imports INT
  imports STRING

  syntax Pgm ::= "Module" "(" Stmts ")"

  syntax Stmts ::= List{Stmt, ""}
  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"
                | "Return" "(" Expr ")"

  syntax Params ::= "Params" "(" String ")"

  syntax Expr ::= "Name" "(" String ")"
                | "Str" "(" String ")"
                | "Int" "(" Int ")"
                | "BinOp" "(" String "," Expr "," Expr ")"
                | "Call" "(" Expr "," Expr ")"
                | "Subscript" "(" Expr "," Expr ")"
                | "Slice" "(" Bound "," Bound "," Bound ")"
                | "Compare" "(" Expr "," CmpOp ")"
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"
  syntax Bound ::= Expr | "NoBound"
endmodule

module MPY-SEMANTIC
  imports MPY-SYNTAX
  imports MAP
  imports LIST
  imports BOOL

  syntax Result ::= "noResult" | String
  syntax Val ::= Int | String | Bool | "PyBool" "(" Bool ")"

  syntax KItem ::= "start" "(" String ")"
                 | "eval" "(" Expr ")"
                 | "exec" "(" Stmts ")"
                 | "binLeft" "(" String "," Expr ")"
                 | "binRight" "(" String "," Val ")"
                 | "cmpLeft" "(" String "," Expr ")"
                 | "cmpRight" "(" String "," Val ")"
                 | "subBase" "(" Expr ")"
                 | "applyFun" "(" String ")"
                 | "choose" "(" Stmts "," Stmts "," Stmts ")"
                 | "endCall"
                 | "finish"

  syntax Stmts ::= "appendStmts" "(" Stmts "," Stmts ")" [function, total]
  rule appendStmts(.Stmts, SS) => SS
  rule appendStmts(S:Stmt REST:Stmts, SS) => S appendStmts(REST, SS)

  configuration
    <mpy>
      <k> $PGM:Pgm ~> start($INPUT:String) </k>
      <function>
        <funName> "" </funName>
        <parameter> "" </parameter>
        <body> .Stmts </body>
      </function>
      <env> .Map </env>
      <stack> .List </stack>
      <result> noResult </result>
    </mpy>

  rule <k> Module(FuncDef(F, Params(P), BODY)) ~> start(S)
         => eval(Call(Name(F), Str(S))) ~> finish ... </k>
       <funName> _ => F </funName>
       <parameter> _ => P </parameter>
       <body> _ => BODY </body>

  rule <k> eval(Str(S)) => S ... </k>
  rule <k> eval(Int(I)) => I ... </k>
  rule <k> eval(Name(X)) => V ... </k>
       <env>... X |-> V:Val ...</env>

  rule <k> eval(BinOp(OP, A, B)) => eval(A) ~> binLeft(OP, B) ... </k>
  rule <k> V:Val ~> binLeft(OP, B) => eval(B) ~> binRight(OP, V) ... </k>
  rule <k> I2:Int ~> binRight("+", I1:Int) => I1 +Int I2 ... </k>
  rule <k> S2:String ~> binRight("+", S1:String) => S1 +String S2 ... </k>
  rule <k> I2:Int ~> binRight("-", I1:Int) => I1 -Int I2 ... </k>
  rule <k> I2:Int ~> binRight("%", I1:Int) => I1 modInt I2 ... </k>

  rule <k> eval(Compare(A, CmpOp(OP, B)))
         => eval(A) ~> cmpLeft(OP, B) ... </k>
  rule <k> V:Val ~> cmpLeft(OP, B)
         => eval(B) ~> cmpRight(OP, V) ... </k>
  rule <k> S2:String ~> cmpRight("==", S1:String)
         => PyBool(S1 ==String S2) ... </k>

  rule <k> eval(Subscript(A, INDEX)) => eval(A) ~> subBase(INDEX) ... </k>
  rule <k> S:String ~> subBase(Int(I))
         => substrString(S, I, I +Int 1) ... </k>
  rule <k> S:String ~> subBase(Slice(Int(I), NoBound, NoBound))
         => substrString(S, I, lengthString(S)) ... </k>

  rule <k> eval(Call(Name(F), ARG))
         => eval(ARG) ~> applyFun(F) ... </k>
  rule <k> I:Int ~> applyFun("chr") => chrChar(I) ... </k>
  rule <k> S:String ~> applyFun("ord") => ordChar(S) ... </k>

  rule <k> S:String ~> applyFun(F) => exec(BODY) ... </k>
       <funName> F </funName>
       <parameter> P </parameter>
       <body> BODY </body>
       <env> ENV => P |-> S </env>
       <stack> STACK => ListItem(ENV) STACK </stack>

  rule <k> exec(If(COND, THEN, ELSE) REST)
         => eval(COND) ~> choose(THEN, ELSE, REST) ... </k>
  rule <k> PyBool(true) ~> choose(THEN:Stmts, _:Stmts, REST:Stmts)
         => exec(appendStmts(THEN, REST)) ... </k>
  rule <k> PyBool(false) ~> choose(_:Stmts, ELSE:Stmts, REST:Stmts)
         => exec(appendStmts(ELSE, REST)) ... </k>
  rule <k> exec(Return(E) _REST) => eval(E) ~> endCall ... </k>

  rule <k> V:Val ~> endCall => V ... </k>
       <env> _ => SAVED </env>
       <stack> ListItem(SAVED:Map) REST => REST </stack>

  rule <k> S:String ~> finish => .K </k>
       <result> _ => S </result>
endmodule

module MPY
  imports MPY-SEMANTIC
endmodule
