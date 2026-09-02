module MPY-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX

  syntax Program ::= "Module" "(" Stmts ")" [symbol(Module)]

  syntax Stmts ::= Stmt
                 | Stmt Stmts [symbol(StmtSeq)]

  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")" [symbol(FuncDef)]
                | "Assign" "(" Expr "," Expr ")" [symbol(Assign)]
                | "Return" "(" Expr ")" [symbol(Return)]

  syntax Params ::= "Params" "(" String "," String ")" [symbol(Params)]

  syntax Expr ::= "Int" "(" Int ")" [symbol(IntLiteral)]
                | "Name" "(" String ")" [symbol(Name)]
                | "Attribute" "(" Expr "," String ")" [symbol(Attribute), strict(1)]
                | "Call" "(" Expr "," ")" [symbol(Call0), strict(1)]
                | "Call" "(" Expr "," Expr ")" [symbol(Call1), seqstrict(1,2)]
                | "Subscript" "(" Expr "," Expr ")" [symbol(Subscript), seqstrict(1,2)]
                | "BinOp" "(" String "," Expr "," Expr ")" [symbol(BinOp), seqstrict(2,3)]
endmodule

module MPY-SEMANTIC
  imports MPY-SYNTAX
  imports INT
  imports BOOL
  imports STRING
  imports MAP

  syntax PyValue ::= "VInt" "(" Int ")" [symbol(VInt)]
                   | "VStr" "(" String ")" [symbol(VStr)]
                   | "VNum" "(" Int ")" [symbol(VNum)]
                   | "VFruits" "(" Int "," Int ")" [symbol(VFruits)]
                   | "VWords" "(" PyValue "," PyValue "," PyValue "," PyValue "," PyValue ")" [symbol(VWords)]
                   | "VSplit" "(" PyValue ")" [symbol(VSplit)]
                   | "VBuiltinInt" [symbol(VBuiltinInt)]

  syntax Expr ::= PyValue
  syntax KResult ::= PyValue

  syntax Function ::= "function" "(" String "," String "," Stmts ")" [symbol(function)]

  syntax KItem ::= "exec" "(" Stmts ")" [symbol(exec)]
                 | "setVar" "(" String ")" [symbol(setVar)]
                 | "finishCall" [symbol(finishCall)]
                 | "invokeFruit" "(" Int "," Int "," Int ")" [symbol(invokeFruit)]
                 | "invokeString" "(" String "," Int ")" [symbol(invokeString)]

  configuration
    <py>
      <k> $PGM:K </k>
      <functions> .Map </functions>
      <env> .Map </env>
    </py>

  rule <k> Module(SS:Stmts) => exec(SS) ... </k>

  rule exec(S:Stmt SS:Stmts) => exec(S) ~> exec(SS)
  rule exec(S:Stmt) => S

  rule <k> FuncDef(F:String, Params(P1:String, P2:String), BODY:Stmts) => .K ... </k>
       <functions> FS => FS [ F <- function(P1, P2, BODY) ] </functions>

  rule <k> Assign(Name(X:String), E:Expr) => E ~> setVar(X) ... </k>
  rule <k> V:PyValue ~> setVar(X:String) => .K ... </k>
       <env> RHO => RHO [ X <- V ] </env>

  rule Return(E:Expr) => E

  rule <k> invokeFruit(A:Int, O:Int, N:Int) => exec(BODY) ~> finishCall ... </k>
       <functions> ... "fruit_distribution" |-> function(P1:String, P2:String, BODY:Stmts) ... </functions>
       <env> _ => P1 |-> VFruits(A, O) P2 |-> VInt(N) </env>

  rule <k> invokeString(S:String, N:Int) => exec(BODY) ~> finishCall ... </k>
       <functions> ... "fruit_distribution" |-> function(P1:String, P2:String, BODY:Stmts) ... </functions>
       <env> _ => P1 |-> VStr(S) P2 |-> VInt(N) </env>

  rule <k> V:PyValue ~> finishCall => V ... </k>
       <functions> _ => .Map </functions>
       <env> _ => .Map </env>

  rule <k> Name(X:String) => V ... </k>
       <env> ... X |-> V:PyValue ... </env>
  rule Name("int") => VBuiltinInt
  rule Int(I:Int) => VInt(I)

  rule Attribute(V:PyValue, "split") => VSplit(V)

  rule Call(VSplit(VFruits(A:Int, O:Int)), )
    => VWords(VNum(A), VStr("apples"), VStr("and"), VNum(O), VStr("oranges"))

  syntax Int ::= spaceAt(String, Int) [function]
               | nextSpace(String, Int) [function]
  rule spaceAt(S, 0) => findString(S, " ", 0)
  rule spaceAt(S, I) => nextSpace(S, spaceAt(S, I -Int 1) +Int 1)
    requires I >Int 0
  // This K distribution's findString result is relative to its start index.
  rule nextSpace(S, START) => START +Int findString(S, " ", START)

  rule Subscript(VWords(V0, _, _, _, _), VInt(0)) => V0
  rule Subscript(VWords(_, _, _, V3, _), VInt(3)) => V3

  rule Call(VBuiltinInt, VInt(I:Int)) => VInt(I)
  rule Call(VBuiltinInt, VNum(I:Int)) => VInt(I)
  rule Call(VBuiltinInt, VStr(S:String)) => VInt(String2Int(S))

  rule BinOp("-", VInt(I), VInt(J)) => VInt(I -Int J)
endmodule
