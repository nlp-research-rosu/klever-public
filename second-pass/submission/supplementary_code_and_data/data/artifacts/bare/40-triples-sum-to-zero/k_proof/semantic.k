requires "domains.md"

module MPY-SYNTAX
  imports BOOL-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX

  syntax Program ::= "Module" "(" Stmts ")"

  syntax Stmts ::= List{Stmt, ""}
  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"
                | "Return" "(" Expr ")"

  syntax Params ::= "Params" "(" Ids ")"
  syntax Ids ::= List{String, ","}

  syntax Exprs ::= List{Expr, ","}
  syntax CmpOps ::= List{CmpOp, ","}
  syntax Expr ::= "Bool" "(" Bool ")"
                | "Int" "(" Int ")"
                | "Name" "(" String ")"
                | "UnaryOp" "(" String "," Expr ")"
                | "BinOp" "(" String "," Expr "," Expr ")"
                | "Subscript" "(" Expr "," Expr ")"
                | "Slice" "(" Bound "," Bound "," Bound ")"
                | "Compare" "(" Expr "," CmpOps ")"
                | "Call" "(" Expr "," Exprs ")"
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"
  syntax Bound ::= Expr | "NoBound"
endmodule

module MPY
  imports MPY-SYNTAX
  imports BOOL
  imports INT
  imports STRING
  imports MAP
  imports LIST

  syntax Ints ::= ".Ints"
                | Int ";" Ints

  syntax PyVal ::= "VInt" "(" Int ")"
                 | "VBool" "(" Bool ")"
                 | "VList" "(" Ints ")"

  syntax Result ::= "noResult" | "result" "(" PyVal ")"
  syntax Fun ::= "function" "(" Params "," Stmts ")"

  syntax Expr ::= "Value" "(" PyVal ")"

  syntax KItem ::= "load" "(" Stmts ")"
                 | "start"
                 | "eval" "(" Expr "," Map ")"
                 | "unaryK" "(" String ")"
                 | "binLeftK" "(" String "," Expr "," Map ")"
                 | "binRightK" "(" String "," PyVal ")"
                 | "subscriptLeftK" "(" Expr "," Map ")"
                 | "subscriptRightK" "(" PyVal ")"
                 | "compareLeftK" "(" String "," Expr "," Map ")"
                 | "compareRightK" "(" String "," PyVal ")"
                 | "call1K" "(" String ")"
                 | "call2LeftK" "(" String "," Expr "," Map ")"
                 | "call2RightK" "(" String "," PyVal ")"
                 | "invoke1" "(" String "," PyVal ")"
                 | "invoke2" "(" String "," PyVal "," PyVal ")"
                 | "exec" "(" Stmts "," Map ")"
                 | "ifK" "(" Stmts "," Stmts "," Stmts "," Map ")"
                 | "finish"

  configuration
    <mpy>
      <k> $PGM:Program </k>
      <funs> .Map </funs>
      <env> .Map </env>
      <input> $INPUT:PyVal </input>
      <result> noResult </result>
    </mpy>

  rule <k> Module(SS) => load(SS) ... </k>

  rule <k> load(FuncDef(F, PS, BODY) REST) => load(REST) ... </k>
       <funs> FUNS => FUNS [ F <- function(PS, BODY) ] </funs>

  rule <k> load(.Stmts) => start ... </k>

  rule <k> start => eval(Call(Name("triples_sum_to_zero"), Value(V)), .Map)
                    ~> finish ... </k>
       <input> V </input>

  rule <k> V:PyVal ~> finish => .K </k>
       <result> noResult => result(V) </result>

  rule eval(Value(V), _) => V
  rule eval(Bool(B), _) => VBool(B)
  rule eval(Int(I), _) => VInt(I)
  rule eval(Name(X), RHO) => RHO [ X ]

  rule eval(UnaryOp(OP, E), RHO) => eval(E, RHO) ~> unaryK(OP)
  rule VList(.Ints) ~> unaryK("not") => VBool(true)
  rule VList(_ ; _) ~> unaryK("not") => VBool(false)
  rule VBool(B) ~> unaryK("not") => VBool(notBool B)

  rule eval(BinOp(OP, E1, E2), RHO)
    => eval(E1, RHO) ~> binLeftK(OP, E2, RHO)
  rule V1:PyVal ~> binLeftK(OP, E2, RHO)
    => eval(E2, RHO) ~> binRightK(OP, V1)
  rule VInt(I2) ~> binRightK("-", VInt(I1)) => VInt(I1 -Int I2)
  rule VInt(I2) ~> binRightK("+", VInt(I1)) => VInt(I1 +Int I2)

  rule eval(Subscript(BASE, INDEX), RHO)
    => eval(BASE, RHO) ~> subscriptLeftK(INDEX, RHO)
  rule V:PyVal ~> subscriptLeftK(INDEX, RHO)
    => eval(INDEX, RHO) ~> subscriptRightK(V)
  rule VInt(0) ~> subscriptRightK(VList(I ; _)) => VInt(I)
  rule eval(Slice(Int(1), NoBound, NoBound), _) => VInt(1)
  rule VInt(1) ~> subscriptRightK(VList(_ ; IS)) => VList(IS)

  rule eval(Compare(E1, CmpOp(OP, E2)), RHO)
    => eval(E1, RHO) ~> compareLeftK(OP, E2, RHO)
  rule V1:PyVal ~> compareLeftK(OP, E2, RHO)
    => eval(E2, RHO) ~> compareRightK(OP, V1)
  rule VList(IS) ~> compareRightK("in", VInt(I))
    => VBool(memberInt(I, IS))

  syntax Bool ::= memberInt(Int, Ints) [function, total]
  rule memberInt(_, .Ints) => false
  rule memberInt(I, J ; IS)
    => (I ==Int J) orBool memberInt(I, IS)

  rule eval(Call(Name(F), E), RHO)
    => eval(E, RHO) ~> call1K(F)
  rule V:PyVal ~> call1K(F) => invoke1(F, V)

  rule eval(Call(Name(F), E1, E2), RHO)
    => eval(E1, RHO) ~> call2LeftK(F, E2, RHO)
  rule V1:PyVal ~> call2LeftK(F, E2, RHO)
    => eval(E2, RHO) ~> call2RightK(F, V1)
  rule V2:PyVal ~> call2RightK(F, V1) => invoke2(F, V1, V2)

  rule <k> invoke1(F, V) => exec(BODY, X |-> V) ... </k>
       <funs> ... F |-> function(Params(X, .Ids), BODY) ... </funs>

  rule <k> invoke2(F, V1, V2)
            => exec(BODY, (X |-> V1) (Y |-> V2)) ... </k>
       <funs> ... F |-> function(Params(X, Y, .Ids), BODY) ... </funs>

  rule exec(Return(E) _, RHO) => eval(E, RHO)

  rule exec(If(E, THEN, ELSE) REST, RHO)
    => eval(E, RHO) ~> ifK(THEN, ELSE, REST, RHO)
  rule VBool(B) ~> ifK(Return(E) .Stmts, .Stmts, _REST:Stmts, RHO:Map)
    => eval(E, RHO)
    requires B
  rule VBool(B) ~> ifK(_THEN:Stmts, .Stmts, REST:Stmts, RHO:Map)
    => exec(REST, RHO)
    requires notBool B
  rule exec(.Stmts, _) => VBool(false)
endmodule
