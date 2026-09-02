requires "verification.k"

module MPY-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX
  imports BOOL-SYNTAX

  syntax Ids ::= List{String, ","}
  syntax Params ::= "Params" "(" Ids ")" [symbol(Params)]

  syntax Exprs ::= List{Expr, ","}
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")" [symbol(CmpOp)]
  syntax CmpOps ::= List{CmpOp, ","}

  syntax Expr ::= "Int" "(" Int ")" [symbol(IntExpr)]
                | "Str" "(" String ")" [symbol(StrExpr)]
                | "Name" "(" String ")" [symbol(Name)]
                | "BinOp" "(" String "," Expr "," Expr ")" [symbol(BinOp)]
                | "Compare" "(" Expr "," CmpOps ")" [symbol(Compare)]
                | "Call" "(" Expr "," Exprs ")" [symbol(Call)]

  syntax Stmts ::= List{Stmt, ""}
  syntax Stmt ::= "Module" "(" Stmts ")" [symbol(Module)]
                | "FuncDef" "(" String "," Params "," Stmts ")" [symbol(FuncDef)]
                | "Assign" "(" Expr "," Expr ")" [symbol(Assign)]
                | "If" "(" Expr "," Stmts "," Stmts ")" [symbol(If)]
                | "For" "(" Expr "," Expr "," Stmts ")" [symbol(For)]
                | "Return" "(" Expr ")" [symbol(Return)]

  syntax PyList ::= "Nil" [symbol(Nil)]
                  | "Cons" "(" Int "," PyList ")" [symbol(Cons)]
  syntax Val ::= Int | String | Bool | PyList
  syntax Result ::= "noResult" [symbol(noResult)] | Val
endmodule

module SEMANTIC
  imports VERIFICATION
  imports INT
  imports STRING
  imports BOOL
  imports MAP

  syntax KItem ::= "init" "(" Stmt "," PyList "," PyList ")" [symbol(init)]
                 | "exec" "(" Stmts ")" [symbol(exec)]
                 | "eval" "(" Expr ")" [symbol(eval)]
                 | "write" "(" String ")" [symbol(write)]
                 | "binRight" "(" String "," Expr ")" [symbol(binRight)]
                 | "applyBin" "(" String "," Val ")" [symbol(applyBin)]
                 | "cmpRight" "(" String "," Expr ")" [symbol(cmpRight)]
                 | "applyCmp" "(" String "," Val ")" [symbol(applyCmp)]
                 | "doLen" [symbol(doLen)]
                 | "branch" "(" Stmts "," Stmts ")" [symbol(branch)]
                 | "startFor" "(" String "," Stmts ")" [symbol(startFor)]
                 | "loop" "(" String "," PyList "," Stmts ")" [symbol(loop)]
                 | "finish" [symbol(finish)]

  syntax Int ::= length(PyList) [function, total]
  rule length(Nil) => 0
  rule length(Cons(_, REST)) => 1 +Int length(REST)

  configuration
    <exchange>
      <k> init($PGM:Stmt, $LST1:PyList, $LST2:PyList) </k>
      <env> .Map </env>
      <result> noResult </result>
    </exchange>

  rule <k> init(Module(FuncDef("exchange", Params("lst1", "lst2"), BODY)), L1, L2)
        => exec(BODY) ... </k>
       <env> .Map
        => "lst1" |-> L1
           "lst2" |-> L2
           "even" |-> 0
           "value" |-> 0
       </env>

  rule <k> exec(.Stmts) => .K ... </k>
  rule <k> exec(Assign(Name(X), E) REST)
        => eval(E) ~> write(X) ~> exec(REST) ... </k>
  rule <k> V:Val ~> write(X) => .K ... </k>
       <env> RHO => RHO [ X <- V ] </env>

  rule <k> exec(If(E, THEN, ELSE) REST)
        => eval(E) ~> branch(THEN, ELSE) ~> exec(REST) ... </k>
  rule <k> true  ~> branch(THEN, _) => exec(THEN) ... </k>
  rule <k> false ~> branch(_, ELSE) => exec(ELSE) ... </k>

  // A pure-statement rule for the translated parity-counting idiom.  It is
  // equivalent to the general If/evaluation rules below, while keeping the
  // symbolic loop invariant independent of a solver case split.
  rule <k> exec(
          If(Compare(BinOp("%", Name(X), Int(2)), CmpOp("==", Int(0))),
             Assign(Name(Y), BinOp("+", Name(Y), Int(1))),
             .Stmts)
          REST)
        => exec(REST) ... </k>
       <env> ... X |-> I:Int
                 Y |-> (N:Int => N +Int evenBit(I)) ... </env>
       [priority(40)]

  rule <k> exec(For(Name(X), E, BODY) REST)
        => eval(E) ~> startFor(X, BODY) ~> exec(REST) ... </k>
  rule <k> L:PyList ~> startFor(X, BODY)
        => loop(X, L, BODY) ... </k>
  rule <k> loop(_, Nil, _) => .K ... </k>
  rule <k> loop(X, Cons(I, REST), BODY)
        => I ~> write(X) ~> exec(BODY) ~> loop(X, REST, BODY) ... </k>

  rule <k> exec(Return(E) _REST)
        => eval(E) ~> finish ... </k>
  rule <k> V:Val ~> finish ~> _REST:K => .K </k>
       <result> noResult => V </result>

  rule <k> eval(Int(I)) => I ... </k>
  rule <k> eval(Str(S)) => S ... </k>
  rule <k> eval(Name(X)) => V ... </k>
       <env> ... X |-> V ... </env>

  rule <k> eval(BinOp(OP, LEFT, RIGHT))
        => eval(LEFT) ~> binRight(OP, RIGHT) ... </k>
  rule <k> LEFT:Val ~> binRight(OP, RIGHT)
        => eval(RIGHT) ~> applyBin(OP, LEFT) ... </k>
  rule <k> RIGHT:Int ~> applyBin("+", LEFT:Int)
        => LEFT +Int RIGHT ... </k>
  rule <k> RIGHT:Int ~> applyBin("%", LEFT:Int)
        => LEFT %Int RIGHT ... </k>

  rule <k> eval(Compare(LEFT, CmpOp(OP, RIGHT)))
        => eval(LEFT) ~> cmpRight(OP, RIGHT) ... </k>
  rule <k> LEFT:Val ~> cmpRight(OP, RIGHT)
        => eval(RIGHT) ~> applyCmp(OP, LEFT) ... </k>
  rule <k> RIGHT:Int ~> applyCmp("==", LEFT:Int)
        => LEFT ==Int RIGHT ... </k>
  rule <k> RIGHT:Int ~> applyCmp(">=", LEFT:Int)
        => LEFT >=Int RIGHT ... </k>

  rule <k> eval(Call(Name("len"), ARG))
        => eval(ARG) ~> doLen ... </k>
  rule <k> L:PyList ~> doLen => length(L) ... </k>
endmodule
