requires "domains.md"

module MPY-SYNTAX
  imports INT-SYNTAX
  imports BOOL-SYNTAX
  imports STRING-SYNTAX
  imports MAP
  imports LIST

  syntax Pgm ::= "Module" "(" Stmts ")"

  syntax Stmts ::= List{Stmt, ""}
  syntax Params ::= "Params" "(" Strings ")"
  syntax Strings ::= List{String, ","}
  syntax Exps ::= List{Exp, ","}
  syntax CmpOps ::= List{CmpOp, ","}

  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "Return" "(" Exp ")"
                | "Assign" "(" Exp "," Exp ")"
                | "If" "(" Exp "," Stmts "," Stmts ")"

  syntax Exp ::= "Int" "(" Int ")"
               | "Name" "(" String ")"
               | "Call" "(" Exp "," Exps ")"
               | "Compare" "(" Exp "," CmpOps ")"
               | "Subscript" "(" Exp "," Exp ")"
               | "Slice" "(" Bound "," Bound "," Bound ")"
               | "BinOp" "(" String "," Exp "," Exp ")"
               | "UnaryOp" "(" String "," Exp ")"

  syntax Bound ::= Exp | "NoBound"
  syntax CmpOp ::= "CmpOp" "(" String "," Exp ")"

  // Concrete arrays use seq(...).  An array value is a view into an Arr:
  // offset O and length N.  Keeping slicing as a view makes recursive calls
  // symbolic without copying or assuming a fixed input length.
  syntax Ints ::= List{Int, ","}
  syntax Arr ::= "seq" "(" Ints ")"
  syntax Val ::= "intVal" "(" Int ")"
               | "boolVal" "(" Bool ")"
               | "arrayVal" "(" Arr "," Int "," Int ")"

  syntax Function ::= "function" "(" Params "," Stmts ")"

endmodule

module MPY
  imports MPY-SYNTAX
  imports INT
  imports BOOL
  imports STRING
  imports MAP
  imports LIST

  syntax KItem ::= "invokeEntry" "(" Val ")"
                 | "load" "(" Stmts ")"
                 | "install" "(" String "," Params "," Stmts ")"
                 | "invoke" "(" String "," Val ")"
                 | "exec" "(" Stmts ")"
                 | "eval" "(" Exp ")"
                 | "value" "(" Val ")"
                 | "assignTo" "(" String ")"
                 | "branch" "(" Stmts "," Stmts "," Stmts ")"
                 | "callValue" "(" String ")"
                 | "applyLen"
                 | "sliceFromOne"
                 | "indexAt" "(" Int ")"
                 | "unaryMinus"
                 | "binLeft" "(" String "," Exp ")"
                 | "binRight" "(" String "," Val ")"
                 | "cmpLeft" "(" String "," Exp ")"
                 | "cmpRight" "(" String "," Val ")"
                 | "doReturn"
                 | "noReturn"

  syntax Stmts ::= "appendStmts" "(" Stmts "," Stmts ")" [function, total]
  rule appendStmts(.Stmts, MORE) => MORE
  rule appendStmts(S REST, MORE) => S appendStmts(REST, MORE)

  configuration
    <mpy>
      <k> $PGM:Pgm ~> invokeEntry($ARGS:Val) </k>
      <env> .Map </env>
      <defs> .Map </defs>
      <stack> .List </stack>
    </mpy>

  // Module loading. Function definitions are data in the definitions cell;
  // calls below interpret their parameter and statement constructors.
  rule <k> Module(SS) => load(SS) ... </k>
  rule <k> load(.Stmts) => .K ... </k>
  rule <k> load(FuncDef(F, PS, BODY) REST)
        => install(F, PS, BODY) ~> load(REST) ... </k>
  rule <k> install(F, PS, BODY) => .K ... </k>
       <defs> DEFS => DEFS [ F <- function(PS, BODY) ] </defs>
  rule <k> invokeEntry(V) => invoke("can_arrange", V) ... </k>

  // A call saves the caller environment.  The K continuation itself holds
  // the expression/statement continuation, so recursive calls remain visible
  // to reachability logic and can be discharged inductively.
  rule <k> invoke(F, V) => exec(BODY) ~> noReturn ... </k>
       <env> CALLER => P |-> V </env>
       <defs> ... F |-> function(Params(P, .Strings), BODY) ... </defs>
       <stack> FRAMES => ListItem(CALLER) FRAMES </stack>

  rule <k> exec(.Stmts) => .K ... </k>
  rule <k> exec(Assign(Name(X), E) REST)
        => eval(E) ~> assignTo(X) ~> exec(REST) ... </k>
  rule <k> value(V) ~> assignTo(X) => .K ... </k>
       <env> ENV => ENV [ X <- V ] </env>

  rule <k> exec(If(COND, THEN, ELSE) REST)
        => eval(COND) ~> branch(THEN, ELSE, REST) ... </k>
  rule <k> value(boolVal(true)) ~> branch(THEN, _ELSE, REST)
        => exec(appendStmts(THEN, REST)) ... </k>
  rule <k> value(boolVal(false)) ~> branch(_THEN, ELSE, REST)
        => exec(appendStmts(ELSE, REST)) ... </k>

  rule <k> exec(Return(E) REST) => eval(E) ~> doReturn ... </k>
  rule <k> value(V) ~> doReturn ~> noReturn => value(V) ... </k>
       <env> _ => CALLER </env>
       <stack> ListItem(CALLER) FRAMES => FRAMES </stack>

  // Expressions needed by the emitted solution AST.
  rule <k> eval(Int(I)) => value(intVal(I)) ... </k>
  rule <k> eval(Name(X)) => value(V) ... </k>
       <env> ... X |-> V ... </env>

  rule <k> eval(UnaryOp("-", E)) => eval(E) ~> unaryMinus ... </k>
  rule <k> value(intVal(I)) ~> unaryMinus => value(intVal(0 -Int I)) ... </k>

  rule <k> eval(Call(Name("len"), E, .Exps)) => eval(E) ~> applyLen ... </k>
  rule <k> value(arrayVal(A, O, N)) ~> applyLen => value(intVal(N)) ... </k>

  rule <k> eval(Call(Name(F), E, .Exps)) => eval(E) ~> callValue(F) ... </k>
       requires F =/=String "len"
  rule <k> value(V) ~> callValue(F) => invoke(F, V) ... </k>

  rule <k> eval(Subscript(E, Slice(Int(1), NoBound, NoBound)))
        => eval(E) ~> sliceFromOne ... </k>
  rule <k> value(arrayVal(A, O, N)) ~> sliceFromOne
        => value(arrayVal(A, O +Int 1, N -Int 1)) ... </k>

  rule <k> eval(Subscript(E, Int(I))) => eval(E) ~> indexAt(I) ... </k>
  rule <k> value(arrayVal(A, O, N)) ~> indexAt(I)
        => value(intVal(get(A, O +Int I))) ... </k>

  rule <k> eval(BinOp(OP, LEFT, RIGHT))
        => eval(LEFT) ~> binLeft(OP, RIGHT) ... </k>
  rule <k> value(V) ~> binLeft(OP, RIGHT)
        => eval(RIGHT) ~> binRight(OP, V) ... </k>
  rule <k> value(intVal(J)) ~> binRight("+", intVal(I))
        => value(intVal(I +Int J)) ... </k>

  rule <k> eval(Compare(LEFT, CmpOp(OP, RIGHT), .CmpOps))
        => eval(LEFT) ~> cmpLeft(OP, RIGHT) ... </k>
  rule <k> value(V) ~> cmpLeft(OP, RIGHT)
        => eval(RIGHT) ~> cmpRight(OP, V) ... </k>
  rule <k> value(intVal(J)) ~> cmpRight("<=", intVal(I))
        => value(boolVal(I <=Int J)) ... </k>
  rule <k> value(intVal(J)) ~> cmpRight("!=", intVal(I))
        => value(boolVal(I =/=Int J)) ... </k>
  rule <k> value(intVal(J)) ~> cmpRight("<", intVal(I))
        => value(boolVal(I <Int J)) ... </k>

  // Total symbolic array selection, plus executable equations for concrete
  // seq(...) arrays. Proof claims only access indices known to be in bounds.
  syntax Int ::= "get" "(" Arr "," Int ")" [function, total]
               | "arrSize" "(" Arr ")" [function, total]
               | "intsSize" "(" Ints ")" [function, total]
  rule arrSize(seq(IS)) => intsSize(IS)
  rule intsSize(.Ints) => 0
  rule intsSize(I, REST) => 1 +Int intsSize(REST)
  rule get(seq(I, REST), 0) => I
  rule get(seq(I, REST), N) => get(seq(REST), N -Int 1)
       requires N >Int 0

endmodule
