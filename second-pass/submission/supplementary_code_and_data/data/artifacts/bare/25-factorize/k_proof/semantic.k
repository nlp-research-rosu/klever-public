module MPY-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX
  imports BOOL-SYNTAX

  syntax Module ::= "Module" "(" Stmts ")"

  syntax Stmts ::= List{Stmt, ""}
  syntax Stmt ::= "ImportFrom" "(" String "," Strings ")"
                | "FuncDef" "(" String "," Params "," Stmts ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"
                | "Return" "(" Expr ")"

  syntax Params ::= "Params" "(" Strings ")"
  syntax Strings ::= List{String, ","}

  syntax Exprs ::= List{Expr, ","}
  syntax Expr ::= "Int" "(" Int ")"
                | "Name" "(" String ")"
                | "BinOp" "(" String "," Expr "," Expr ")"
                | "Compare" "(" Expr "," CmpOps ")"
                | "ListExpr" "(" Exprs ")"
                | "Call" "(" Expr "," Exprs ")"

  syntax CmpOps ::= List{CmpOp, ","}
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"
endmodule

module SEMANTIC
  imports MPY-SYNTAX
  imports INT
  imports BOOL
  imports STRING
  imports MAP
  imports LIST

  syntax Val ::= IntVal(Int)
               | BoolVal(Bool)
               | ListVal(List)

  syntax Closure ::= Closure(Params, Stmts)

  syntax Frame ::= Frame(K, Map)

  syntax Result ::= "noResult"
                  | Val

  configuration
    <k> $PGM:Module </k>
    <input> $INPUT:Int </input>
    <result> noResult </result>

  syntax MachineState ::= Machine(K, Map, Map, List, Result) [function]
                        | Halted(Map, Map, List, Val)
  syntax ProofState ::= Run(MachineState)

  rule <k> Module(SS)
        => Machine(Invoke("factorize", ListItem(IntVal(N))) ~> Finish,
                   .Map, collect(SS), .List, noResult) </k>
       <input> N:Int </input>

  rule <k> Halted(_, _, _, V:Val) => .K </k>
       <result> noResult => V </result>

  // An explicit call machine is used for execution.  Capturing the caller's
  // continuation and environment in Frame gives Python calls local scope and
  // gives reachability proofs a sound induction point at recursive calls.
  syntax KItem ::= Invoke(String, List)
                 | Exec(Stmts)
                 | Eval(Expr)
                 | BinLeft(String, Expr)
                 | BinRight(String, Val)
                 | CompareLeft(String, Expr)
                 | CompareRight(String, Val)
                 | "MakeList"
                 | CallOne(String)
                 | CallTwoLeft(String, Expr)
                 | CallTwoRight(String, Val)
                 | Choose(Stmts, Stmts)
                 | "DoReturn"
                 | "Finish"

  rule Machine(Invoke(F, VS) ~> KREST,
               OLD, (F |-> Closure(PS, BODY)) FS, STACK, R)
    => Machine(Exec(BODY), bind(PS, VS),
               (F |-> Closure(PS, BODY)) FS,
               ListItem(Frame(KREST, OLD)) STACK, R)

  rule Machine(Exec(.Stmts) ~> KREST, ENV, FS, STACK, R)
    => Machine(KREST, ENV, FS, STACK, R)
  rule Machine(Exec(Return(E) _REST) ~> KREST, ENV, FS, STACK, R)
    => Machine(Eval(E) ~> DoReturn ~> KREST, ENV, FS, STACK, R)
  rule Machine(Exec(If(COND, THEN, ELSE) REST) ~> KREST,
               ENV, FS, STACK, R)
    => Machine(Eval(COND) ~> Choose(THEN, ELSE) ~> Exec(REST) ~> KREST,
               ENV, FS, STACK, R)

  rule Machine(BoolVal(B) ~> Choose(THEN, _) ~> KREST,
               ENV, FS, STACK, R)
    => Machine(Exec(THEN) ~> KREST, ENV, FS, STACK, R)
    requires B
  rule Machine(BoolVal(B) ~> Choose(_, ELSE) ~> KREST,
               ENV, FS, STACK, R)
    => Machine(Exec(ELSE) ~> KREST, ENV, FS, STACK, R)
    requires notBool B

  rule Machine(V:Val ~> DoReturn ~> _CURRENT,
               _, FS, ListItem(Frame(KREST, OLD)) STACK, R)
    => Machine(V ~> KREST, OLD, FS, STACK, R)

  rule Machine(V:Val ~> Finish, ENV, FS, STACK, noResult)
    => Halted(ENV, FS, STACK, V)

  rule Machine(Eval(Int(I)) ~> KREST, ENV, FS, STACK, R)
    => Machine(IntVal(I) ~> KREST, ENV, FS, STACK, R)
  rule Machine(Eval(Name(X)) ~> KREST,
               (X |-> V) ENV, FS, STACK, R)
    => Machine(V ~> KREST, (X |-> V) ENV, FS, STACK, R)

  rule Machine(Eval(ListExpr(.Exprs)) ~> KREST, ENV, FS, STACK, R)
    => Machine(ListVal(.List) ~> KREST, ENV, FS, STACK, R)
  rule Machine(Eval(ListExpr(E)) ~> KREST, ENV, FS, STACK, R)
    => Machine(Eval(E) ~> MakeList ~> KREST, ENV, FS, STACK, R)
  rule Machine(V:Val ~> MakeList ~> KREST, ENV, FS, STACK, R)
    => Machine(ListVal(ListItem(V)) ~> KREST, ENV, FS, STACK, R)

  rule Machine(Eval(BinOp(OP, LEFT, RIGHT)) ~> KREST,
               ENV, FS, STACK, R)
    => Machine(Eval(LEFT) ~> BinLeft(OP, RIGHT) ~> KREST,
               ENV, FS, STACK, R)
  rule Machine(V:Val ~> BinLeft(OP, RIGHT) ~> KREST,
               ENV, FS, STACK, R)
    => Machine(Eval(RIGHT) ~> BinRight(OP, V) ~> KREST,
               ENV, FS, STACK, R)
  rule Machine(V2:Val ~> BinRight(OP, V1) ~> KREST,
               ENV, FS, STACK, R)
    => Machine(evalBinOp(OP, V1, V2) ~> KREST, ENV, FS, STACK, R)

  rule Machine(Eval(Compare(LEFT, CmpOp(OP, RIGHT))) ~> KREST,
               ENV, FS, STACK, R)
    => Machine(Eval(LEFT) ~> CompareLeft(OP, RIGHT) ~> KREST,
               ENV, FS, STACK, R)
  rule Machine(V:Val ~> CompareLeft(OP, RIGHT) ~> KREST,
               ENV, FS, STACK, R)
    => Machine(Eval(RIGHT) ~> CompareRight(OP, V) ~> KREST,
               ENV, FS, STACK, R)
  rule Machine(V2:Val ~> CompareRight(OP, V1) ~> KREST,
               ENV, FS, STACK, R)
    => Machine(evalCompare(OP, V1, V2) ~> KREST, ENV, FS, STACK, R)

  rule Machine(Eval(Call(Name(F), E)) ~> KREST, ENV, FS, STACK, R)
    => Machine(Eval(E) ~> CallOne(F) ~> KREST, ENV, FS, STACK, R)
  rule Machine(V:Val ~> CallOne(F) ~> KREST, ENV, FS, STACK, R)
    => Machine(Invoke(F, ListItem(V)) ~> KREST, ENV, FS, STACK, R)
  rule Machine(Eval(Call(Name(F), E1, E2)) ~> KREST,
               ENV, FS, STACK, R)
    => Machine(Eval(E1) ~> CallTwoLeft(F, E2) ~> KREST,
               ENV, FS, STACK, R)
  rule Machine(V:Val ~> CallTwoLeft(F, E2) ~> KREST,
               ENV, FS, STACK, R)
    => Machine(Eval(E2) ~> CallTwoRight(F, V) ~> KREST,
               ENV, FS, STACK, R)
  rule Machine(V2:Val ~> CallTwoRight(F, V1) ~> KREST,
               ENV, FS, STACK, R)
    => Machine(Invoke(F, ListItem(V1) ListItem(V2)) ~> KREST,
               ENV, FS, STACK, R)

  syntax Map ::= collect(Stmts) [function]
  rule collect(.Stmts) => .Map
  rule collect(ImportFrom(_, _) REST) => collect(REST)
  rule collect(FuncDef(F, PS, BODY) REST)
    => collect(REST)[F <- Closure(PS, BODY)]

  syntax Map ::= bind(Params, List) [function]
  rule bind(Params(PS), VS) => bindLists(PS, VS)

  syntax Map ::= bindLists(Strings, List) [function]
  rule bindLists(.Strings, .List) => .Map
  rule bindLists(P, PS, ListItem(V) VS)
    => (P |-> V) bindLists(PS, VS)

  syntax Val ::= evalBinOp(String, Val, Val) [function]
  rule evalBinOp("+", IntVal(A), IntVal(B)) => IntVal(A +Int B)
  rule evalBinOp("*", IntVal(A), IntVal(B)) => IntVal(A *Int B)
  rule evalBinOp("+", ListVal(A), ListVal(B)) => ListVal(A B)
  rule evalBinOp("%", IntVal(A), IntVal(B)) => IntVal(A %Int B)
    requires B =/=Int 0
  rule evalBinOp("//", IntVal(A), IntVal(B)) => IntVal(A /Int B)
    requires B =/=Int 0

  syntax Val ::= evalCompare(String, Val, Val) [function]
  rule evalCompare("<", IntVal(A), IntVal(B)) => BoolVal(A <Int B)
  rule evalCompare(">", IntVal(A), IntVal(B)) => BoolVal(A >Int B)
  rule evalCompare("==", IntVal(A), IntVal(B)) => BoolVal(A ==Int B)
endmodule
