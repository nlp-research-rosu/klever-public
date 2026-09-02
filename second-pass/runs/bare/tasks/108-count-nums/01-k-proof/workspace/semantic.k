requires "domains.md"

module MPY-SYNTAX
  imports INT-SYNTAX
  imports BOOL-SYNTAX
  imports STRING-SYNTAX

  syntax Program
  syntax Stmt
  syntax Stmts
  syntax Expr
  syntax Params
  syntax Cmp
  syntax Index
  syntax Bound

  syntax Program ::= "Module" "(" Stmts ")" [symbol(Module)]

  syntax Stmts ::= Stmt
                 | Stmt Stmts [symbol(StmtsCons)]

  syntax Params ::= "Params" "(" String ")" [symbol(Params)]

  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                  [symbol(FuncDef)]
                | "If" "(" Expr "," Stmts "," Stmts ")" [symbol(If)]
                | "Return" "(" Expr ")" [symbol(Return)]

  syntax Expr ::= "Int" "(" Int ")" [symbol(Int)]
                | "Name" "(" String ")" [symbol(Name)]
                | "ListExpr" "(" ")" [symbol(ListExpr)]
                | "UnaryOp" "(" String "," Expr ")" [symbol(UnaryOp)]
                | "BinOp" "(" String "," Expr "," Expr ")" [symbol(BinOp)]
                | "Compare" "(" Expr "," Cmp ")" [symbol(Compare)]
                | "Call" "(" Expr "," Expr ")" [symbol(Call)]
                | "Subscript" "(" Expr "," Index ")" [symbol(Subscript)]

  syntax Cmp ::= "CmpOp" "(" String "," Expr ")" [symbol(CmpOp)]
  syntax Index ::= Expr
                 | "Slice" "(" Bound "," Bound "," Bound ")" [symbol(Slice)]
  syntax Bound ::= Expr
                 | "NoBound" [symbol(NoBound)]

  syntax Value
  syntax VList
  syntax Value ::= "IntV" "(" Int ")" [symbol(IntV)]
                 | "BoolV" "(" Bool ")" [symbol(BoolV)]
                 | "ListV" "(" VList ")" [symbol(ListV)]
  syntax VList ::= "VNil" [symbol(VNil)]
                 | "VCons" "(" Int "," VList ")" [symbol(VCons)]

  syntax Value ::= "list" "(" ")" [macro]
                 | "list" "(" Int ")" [macro]
                 | "list" "(" Int "," Int ")" [macro]
                 | "list" "(" Int "," Int "," Int ")" [macro]
                 | "list" "(" Int "," Int "," Int "," Int ")" [macro]
                 | "list" "(" Int "," Int "," Int "," Int "," Int ")" [macro]

  rule list() => ListV(VNil)
  rule list(I1:Int) => ListV(VCons(I1, VNil))
  rule list(I1:Int, I2:Int) => ListV(VCons(I1, VCons(I2, VNil)))
  rule list(I1:Int, I2:Int, I3:Int)
    => ListV(VCons(I1, VCons(I2, VCons(I3, VNil))))
  rule list(I1:Int, I2:Int, I3:Int, I4:Int)
    => ListV(VCons(I1, VCons(I2, VCons(I3, VCons(I4, VNil)))))
  rule list(I1:Int, I2:Int, I3:Int, I4:Int, I5:Int)
    => ListV(VCons(I1, VCons(I2, VCons(I3, VCons(I4, VCons(I5, VNil))))))
endmodule

module MPY-SEMANTIC
  imports MPY-SYNTAX
  imports INT
  imports BOOL
  imports STRING
  imports MAP
  imports LIST

  syntax Function
  syntax Frame
  syntax Function ::= "function" "(" String "," Stmts ")" [symbol(function)]
  syntax Frame ::= "frame" "(" Map ")" [symbol(frame)]

  syntax KItem ::= "invoke" "(" String "," Value ")" [symbol(invoke)]
                 | "finishK" [symbol(finishK)]
                 | "callK" "(" String ")" [symbol(callK)]
                 | "returnK" [symbol(returnK)]
                 | "ifK" "(" Stmts "," Stmts ")" [symbol(ifK)]
                 | "unaryK" "(" String ")" [symbol(unaryK)]
                 | "binLeftK" "(" String "," Expr ")" [symbol(binLeftK)]
                 | "binRightK" "(" String "," Value ")" [symbol(binRightK)]
                 | "compareLeftK" "(" String "," Expr ")" [symbol(compareLeftK)]
                 | "compareRightK" "(" String "," Value ")" [symbol(compareRightK)]
                 | "subscriptK" "(" Index ")" [symbol(subscriptK)]
                 | "indexK" "(" VList ")" [symbol(indexK)]

  configuration
    <mpy>
      <k> $PGM:Program ~> invoke("count_nums", $ARG:Value) </k>
      <funs> .Map </funs>
      <env> .Map </env>
      <stack> .List </stack>
    </mpy>

  rule <k> Module(S1:Stmt S2:Stmt) => S1 ~> S2 ... </k>

  rule <k> FuncDef(F, Params(P), BODY) => .K ... </k>
       <funs> FUNS => FUNS [ F <- function(P, BODY) ] </funs>

  rule <k> invoke(F, V) => V ~> callK(F) ~> finishK ... </k>
  rule <k> V:Value ~> finishK => V ... </k>

  rule <k> V:Value ~> callK(F) => BODY ... </k>
       <funs> ... F |-> function(P, BODY) ... </funs>
       <env> CALLER => .Map [ P <- V ] </env>
       <stack> STACK => ListItem(frame(CALLER)) STACK </stack>

  rule <k> V:Value ~> returnK => V ... </k>
       <env> _ => CALLER </env>
       <stack> ListItem(frame(CALLER)) STACK => STACK </stack>

  rule <k> If(TEST, THEN, ELSE) => TEST ~> ifK(THEN, ELSE) ... </k>
  rule <k> BoolV(true) ~> ifK(THEN, _) => THEN ... </k>
  rule <k> BoolV(false) ~> ifK(_, ELSE) => ELSE ... </k>
  rule <k> Return(E) => E ~> returnK ... </k>

  rule <k> Int(I) => IntV(I) ... </k>
  rule <k> Name(X) => V ... </k>
       <env> ... X |-> V:Value ... </env>
  rule <k> ListExpr() => ListV(VNil) ... </k>

  rule <k> UnaryOp(OP, E) => E ~> unaryK(OP) ... </k>
  rule <k> IntV(I) ~> unaryK("-") => IntV(0 -Int I) ... </k>

  rule <k> BinOp(OP, L, R) => L ~> binLeftK(OP, R) ... </k>
  rule <k> V:Value ~> binLeftK(OP, R) => R ~> binRightK(OP, V) ... </k>
  rule <k> IntV(J) ~> binRightK("+", IntV(I)) => IntV(I +Int J) ... </k>
  rule <k> IntV(J) ~> binRightK("%", IntV(I)) => IntV(I %Int J) ... </k>
       requires J =/=Int 0
  rule <k> IntV(J) ~> binRightK("//", IntV(I)) => IntV(I /Int J) ... </k>
       requires J =/=Int 0

  rule <k> Compare(L, CmpOp(OP, R))
            => L ~> compareLeftK(OP, R) ... </k>
  rule <k> V:Value ~> compareLeftK(OP, R)
            => R ~> compareRightK(OP, V) ... </k>

  rule <k> IntV(J) ~> compareRightK("<", IntV(I)) => BoolV(true) ... </k>
       requires I <Int J
  rule <k> IntV(J) ~> compareRightK("<", IntV(I)) => BoolV(false) ... </k>
       requires I >=Int J
  rule <k> IntV(J) ~> compareRightK(">", IntV(I)) => BoolV(true) ... </k>
       requires I >Int J
  rule <k> IntV(J) ~> compareRightK(">", IntV(I)) => BoolV(false) ... </k>
       requires I <=Int J

  rule <k> ListV(VNil) ~> compareRightK("==", ListV(VNil))
            => BoolV(true) ... </k>
  rule <k> ListV(VNil) ~> compareRightK("==", ListV(VCons(_, _)))
            => BoolV(false) ... </k>

  rule <k> Call(Name(F), ARG) => ARG ~> callK(F) ... </k>

  rule <k> Subscript(BASE, IDX) => BASE ~> subscriptK(IDX) ... </k>
  rule <k> ListV(VALUES) ~> subscriptK(IDX:Expr)
            => IDX ~> indexK(VALUES) ... </k>
  rule <k> IntV(0) ~> indexK(VCons(I, _)) => IntV(I) ... </k>
  rule <k> ListV(VCons(_, REST))
            ~> subscriptK(Slice(Int(1), NoBound, NoBound))
            => ListV(REST) ... </k>
endmodule
