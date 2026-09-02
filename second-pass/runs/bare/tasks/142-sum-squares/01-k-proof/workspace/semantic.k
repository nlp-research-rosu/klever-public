module MPY-SYNTAX
  imports INT-SYNTAX
  imports BOOL-SYNTAX
  imports STRING-SYNTAX

  syntax Pgm ::= "Module" "(" Stmts ")"

  syntax Stmts ::= List{Stmt, ""}
  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "Return" "(" Expr ")"
                | "Assign" "(" Expr "," Expr ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"

  syntax Params ::= "Params" "(" Strings ")"
  syntax Strings ::= List{String, ","}

  syntax Exprs ::= List{Expr, ","}
  syntax Expr ::= "Int" "(" Int ")"
                | "Name" "(" String ")"
                | "ListExpr" "(" Exprs ")"
                | "BinOp" "(" String "," Expr "," Expr ")"
                | "UnaryOp" "(" String "," Expr ")"
                | "Compare" "(" Expr "," CmpOps ")"
                | "Call" "(" Expr "," Exprs ")"
                | "Subscript" "(" Expr "," Index ")"
  syntax CmpOps ::= List{CmpOp, ","}
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"
  syntax Index ::= Expr
                 | "Slice" "(" Bound "," Bound "," Bound ")"
  syntax Bound ::= Expr | "NoBound"

  // Runtime values.  The task contract only requires lists whose elements
  // are mathematical integers, so lists have a deliberately narrow sort.
  // A snoc-oriented sequence gives the semantics a direct structural view of
  // Python's last element and all-but-last slice.  Surface order is unchanged:
  // ListVal(1, 2, 3) denotes the ordinary list [1, 2, 3].
  syntax Ints ::= ".Ints"
  syntax Ints ::= Int
  syntax Ints ::= Ints "," Int
  syntax Value ::= "VInt" "(" Int ")"
                 | "VBool" "(" Bool ")"
                 | "ListVal" "(" Ints ")"
                 | "NoneVal"
endmodule

module MPY-SEMANTICS
  imports MPY-SYNTAX
  imports INT
  imports BOOL
  imports STRING
  imports MAP
  imports K-EQUAL

  configuration
    <k> $PGM:Pgm ~> run($ARGS:Value) </k>
    <functions> .Map </functions>
    <env> .Map </env>

  syntax Function ::= "function1" "(" String "," Stmts ")"

  syntax Outcome ::= "normal" | "returned" "(" Value ")"

  syntax KItem ::= "load" "(" Stmts ")"
                 | "run" "(" Value ")"
                 | "exec" "(" Stmts ")"
                 | "eval" "(" Expr ")"
                 | "invoke1" "(" String "," Value ")"
                 | "finishCall"
                 | "restoreEnv" "(" Map ")"
                 | "assignTo" "(" String "," Stmts ")"
                 | "choose" "(" Stmts "," Stmts "," Stmts ")"
                 | "afterBranch" "(" Stmts ")"
                 | "binLeft" "(" String "," Expr ")"
                 | "binRight" "(" String "," Value ")"
                 | "compareLeft" "(" String "," Expr ")"
                 | "compareRight" "(" String "," Value ")"
                 | "callOne" "(" String ")"
                 | "lengthResult"
                 | "lastResult"
                 | "initResult"

  // Module loading is separate from statement execution.  Function
  // definitions are immutable entries in the function table.
  rule <k> Module(SS) => load(SS) ... </k>
  rule <k> load(.Stmts) => .K ... </k>
  rule <k> load(FuncDef(F, Params(P), BODY) REST)
        => load(REST) ... </k>
       <functions> FS => FS [ F <- function1(P, BODY) ] </functions>

  rule <k> run(ARG) => invoke1("sum_squares", ARG) ... </k>

  // A call gets a fresh local environment and restores the caller's map on
  // both ordinary and recursive returns.
  rule <k> invoke1(F, V) => exec(BODY) ~> finishCall ~> restoreEnv(OLD) ... </k>
       <functions> ... F |-> function1(P, BODY) ... </functions>
       <env> OLD => P |-> V </env>
  rule <k> normal ~> finishCall => NoneVal ... </k>
  rule <k> returned(V) ~> finishCall => V ... </k>
  rule <k> V:Value ~> restoreEnv(OLD) => V ... </k>
       <env> _ => OLD </env>

  // Statement lists yield an explicit outcome.  This makes Return discard
  // the unexecuted tail without any control-stack side conditions.
  rule <k> exec(.Stmts) => normal ... </k>
  rule <k> exec(Return(E) _REST) => eval(E) ~> makeReturned ... </k>
  rule <k> exec(Assign(Name(X), E) REST)
        => eval(E) ~> assignTo(X, REST) ... </k>
  rule <k> V:Value ~> assignTo(X, REST) => exec(REST) ... </k>
       <env> ENV => ENV [ X <- V ] </env>
  rule <k> exec(If(COND, THEN, ELSE) REST)
        => eval(COND) ~> choose(THEN, ELSE, REST) ... </k>
  rule <k> VBool(true) ~> choose(THEN:Stmts, _ELSE:Stmts, REST:Stmts)
        => exec(THEN) ~> afterBranch(REST) ... </k>
  rule <k> VBool(false) ~> choose(_THEN:Stmts, ELSE:Stmts, REST:Stmts)
        => exec(ELSE) ~> afterBranch(REST) ... </k>
  rule <k> normal ~> afterBranch(REST) => exec(REST) ... </k>
  rule <k> returned(V) ~> afterBranch(_) => returned(V) ... </k>

  syntax KItem ::= "makeReturned"
  rule <k> V:Value ~> makeReturned => returned(V) ... </k>

  // Expression evaluation and its left-to-right continuations.
  rule <k> eval(Int(N)) => VInt(N) ... </k>
  rule <k> eval(Name(X)) => V ... </k>
       <env> ... X |-> V:Value ... </env>
  rule <k> eval(ListExpr(.Exprs)) => ListVal(.Ints) ... </k>

  rule <k> eval(BinOp(OP, LEFT, RIGHT))
        => eval(LEFT) ~> binLeft(OP, RIGHT) ... </k>
  rule <k> V:Value ~> binLeft(OP, RIGHT)
        => eval(RIGHT) ~> binRight(OP, V) ... </k>
  rule <k> V2:Value ~> binRight(OP, V1)
        => binResult(OP, V1, V2) ... </k>

  rule <k> eval(UnaryOp("-", E)) => eval(E) ~> negateResult ... </k>
  syntax KItem ::= "negateResult"
  rule <k> VInt(N) ~> negateResult => VInt(0 -Int N) ... </k>

  rule <k> eval(Compare(LEFT, CmpOp(OP, RIGHT)))
        => eval(LEFT) ~> compareLeft(OP, RIGHT) ... </k>
  rule <k> V:Value ~> compareLeft(OP, RIGHT)
        => eval(RIGHT) ~> compareRight(OP, V) ... </k>
  rule <k> V2:Value ~> compareRight(OP, V1)
        => compareResult(OP, V1, V2) ... </k>

  rule <k> eval(Call(Name("len"), E)) => eval(E) ~> lengthResult ... </k>
  rule <k> ListVal(IS) ~> lengthResult => VInt(lengthInts(IS)) ... </k>
  rule <k> eval(Call(Name(F), E)) => eval(E) ~> callOne(F) ... </k>
       requires F =/=String "len"
  rule <k> V:Value ~> callOne(F) => invoke1(F, V) ... </k>

  // These two index forms are exactly Python's last element and all-but-last
  // slice.  Both are defined below for every nonempty integer list.
  rule <k> eval(Subscript(E, UnaryOp("-", Int(1))))
        => eval(E) ~> lastResult ... </k>
  rule <k> ListVal(IS) ~> lastResult => VInt(lastInt(IS)) ... </k>
  rule <k> eval(Subscript(E, Slice(NoBound, UnaryOp("-", Int(1)), NoBound)))
        => eval(E) ~> initResult ... </k>
  rule <k> ListVal(IS) ~> initResult => ListVal(initInts(IS)) ... </k>

  syntax Value ::= "binResult" "(" String "," Value "," Value ")" [function]
  rule binResult("+", VInt(A), VInt(B)) => VInt(A +Int B)
  rule binResult("-", VInt(A), VInt(B)) => VInt(A -Int B)
  rule binResult("*", VInt(A), VInt(B)) => VInt(A *Int B)
  rule binResult("%", VInt(A), VInt(B)) => VInt(A %Int B)

  syntax Value ::= "compareResult" "(" String "," Value "," Value ")" [function]
  rule compareResult("==", VInt(A), VInt(B)) => VBool(A ==Int B)
  rule compareResult("==", ListVal(IS), ListVal(.Ints))
    => VBool(IS ==K .Ints)

  syntax Int ::= "lengthInts" "(" Ints ")" [function]
  rule lengthInts(.Ints) => 0
  rule lengthInts(_:Int) => 1
  rule lengthInts(PREFIX:Ints, _:Int) => lengthInts(PREFIX) +Int 1

  syntax Int ::= "lastInt" "(" Ints ")" [function]
  rule lastInt(N:Int) => N
  rule lastInt(_PREFIX:Ints, N:Int) => N

  syntax Ints ::= "initInts" "(" Ints ")" [function]
  rule initInts(_:Int) => .Ints
  rule initInts(PREFIX:Ints, _N:Int) => PREFIX
endmodule
