module MPY-SYNTAX
  imports INT
  imports STRING

  syntax Pgm ::= "Module" "(" Stmts ")" [symbol(moduleAst)]

  syntax Stmts ::= List{Stmt, ""}
  syntax Exprs ::= List{Expr, ","}
  syntax Ids ::= List{String, ","}
  syntax CmpOps ::= List{CmpOp, ","}

  syntax Stmt ::= "FuncDef" "(" String "," "Params" "(" Ids ")" "," Stmts ")"
                [symbol(functionDefinitionAst)]
                | "Assign" "(" Expr "," Expr ")" [symbol(assignAst)]
                | "If" "(" Expr "," Stmts "," Stmts ")" [symbol(ifAst)]
                | "While" "(" Expr "," Stmts ")" [symbol(whileAst)]
                | "Return" "(" Expr ")" [symbol(returnAst)]

  syntax Expr ::= "Int" "(" Int ")" [symbol(intAst)]
                | "Name" "(" String ")" [symbol(nameAst)]
                | "ListExpr" "(" Exprs ")" [symbol(listAst)]
                | "BinOp" "(" String "," Expr "," Expr ")" [symbol(binOpAst)]
                | "Compare" "(" Expr "," CmpOps ")" [symbol(compareAst)]
                | "Call" "(" Expr "," Exprs ")" [symbol(callAst)]

  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")" [symbol(cmpOpAst)]
endmodule

module SEMANTIC
  imports MPY-SYNTAX
  imports BOOL
  imports MAP

  // Runtime values.  Ints is deliberately an explicit, immutable list so
  // that collection and sorting remain visible in rewrite traces.
  syntax Ints ::= ".Ints" [constructor, symbol(emptyInts)]
                | Int "::" Ints [constructor, symbol(consInts)]
  syntax Value ::= "vi" "(" Int ")" [constructor, symbol(intValue)]
                 | "vb" "(" Bool ")" [constructor, symbol(boolValue)]
                 | "vl" "(" Ints ")" [constructor, symbol(listValue)]
  syntax Function ::= "function" "(" String "," Stmts ")"
                      [constructor, symbol(functionValue)]
  syntax Result ::= "noResult" [constructor]
                  | "result" "(" Value ")" [constructor]

  syntax KItem ::= "run" "(" Pgm ")"
                 | "load" "(" Stmts ")"
                 | "start"
                 | "exec" "(" Stmts ")"
                 | "eval" "(" Expr ")"
                 | "assignTo" "(" String ")"
                 | "singleton"
                 | "binLeft" "(" String "," Expr ")"
                 | "binRight" "(" String "," Value ")"
                 | "cmpLeft" "(" String "," Expr ")"
                 | "cmpRight" "(" String "," Value ")"
                 | "whileDecide" "(" Expr "," Stmts "," Stmts ")"
                 | "ifDecide" "(" Stmts "," Stmts "," Stmts ")"
                 | "sortResult"
                 | "finish"

  configuration
    <python>
      <k> run($PGM:Pgm) </k>
      <input> $N:Int </input>
      <functions> .Map </functions>
      <env> .Map </env>
      <result> noResult </result>
    </python>

  rule <k> run(Module(S)) => load(S) ~> start </k>

  rule <k> load(FuncDef(F, Params(P, .Ids), BODY) REST) => load(REST) ... </k>
       <functions> FS => FS [ F <- function(P, BODY) ] </functions>
  rule <k> load(.Stmts) => .K ... </k>

  rule <k> start => exec(BODY) </k>
       <input> N </input>
       <functions> ... "get_odd_collatz" |-> function(P, BODY) ... </functions>
       <env> _ => P |-> vi(N) </env>

  // Statement execution uses explicit continuations in the K cell.
  rule <k> exec(Assign(Name(X), E) REST)
        => eval(E) ~> assignTo(X) ~> exec(REST) ... </k>
  rule <k> V:Value ~> assignTo(X) => .K ... </k>
       <env> ENV => ENV [ X <- V ] </env>

  rule <k> exec(If(TEST, THEN, ELSE) REST)
        => eval(TEST) ~> ifDecide(THEN, ELSE, REST) ... </k>
  rule <k> vb(true) ~> ifDecide(THEN, _, REST)
        => exec(THEN) ~> exec(REST) ... </k>
  rule <k> vb(false) ~> ifDecide(_, ELSE, REST)
        => exec(ELSE) ~> exec(REST) ... </k>

  rule <k> exec(While(TEST, BODY) REST)
        => eval(TEST) ~> whileDecide(TEST, BODY, REST) ... </k>
  rule <k> vb(true) ~> whileDecide(TEST, BODY, REST)
        => exec(BODY) ~> exec(While(TEST, BODY) REST) ... </k>
  rule <k> vb(false) ~> whileDecide(_, _, REST)
        => exec(REST) ... </k>

  rule <k> exec(Return(E) _REST) => eval(E) ~> finish ... </k>
  rule <k> V:Value ~> finish => .K </k>
       <functions> _ => .Map </functions>
       <env> _ => .Map </env>
       <result> noResult => result(V) </result>
  rule <k> exec(.Stmts) => .K ... </k>

  // Expression evaluation is left-to-right, as in Python.
  rule <k> eval(Int(I)) => vi(I) ... </k>
  rule <k> eval(Name(X)) => V ... </k>
       <env> ... X |-> V ... </env>

  rule <k> eval(ListExpr(.Exprs)) => vl(.Ints) ... </k>
  rule <k> eval(ListExpr(E, .Exprs)) => eval(E) ~> singleton ... </k>
  rule <k> vi(I) ~> singleton => vl(I :: .Ints) ... </k>

  rule <k> eval(BinOp(OP, LEFT, RIGHT))
        => eval(LEFT) ~> binLeft(OP, RIGHT) ... </k>
  rule <k> LEFT:Value ~> binLeft(OP, RIGHT)
        => eval(RIGHT) ~> binRight(OP, LEFT) ... </k>
  rule <k> RIGHT:Value ~> binRight(OP, LEFT)
        => applyBin(OP, LEFT, RIGHT) ... </k>

  rule <k> eval(Compare(LEFT, CmpOp(OP, RIGHT), .CmpOps))
        => eval(LEFT) ~> cmpLeft(OP, RIGHT) ... </k>
  rule <k> LEFT:Value ~> cmpLeft(OP, RIGHT)
        => eval(RIGHT) ~> cmpRight(OP, LEFT) ... </k>
  rule <k> RIGHT:Value ~> cmpRight(OP, LEFT)
        => applyCmp(OP, LEFT, RIGHT) ... </k>

  rule <k> eval(Call(Name("sorted"), E, .Exprs))
        => eval(E) ~> sortResult ... </k>
  rule <k> vl(IS) ~> sortResult => vl(sortInts(IS)) ... </k>

  syntax Value ::= applyBin(String, Value, Value) [function]
  rule applyBin("+",  vi(A), vi(B)) => vi(A +Int B)
  rule applyBin("*",  vi(A), vi(B)) => vi(A *Int B)
  rule applyBin("%",  vi(A), vi(B)) => vi(A %Int B) requires B =/=Int 0
  rule applyBin("//", vi(A), vi(B)) => vi(A /Int B) requires B >Int 0 andBool A >=Int 0
  rule applyBin("+", vl(AS), vl(BS)) => vl(appendInts(AS, BS))

  syntax Value ::= applyCmp(String, Value, Value) [function]
  rule applyCmp("==", vi(A), vi(B)) => vb(true)  requires A ==Int B
  rule applyCmp("==", vi(A), vi(B)) => vb(false) requires A =/=Int B
  rule applyCmp("!=", vi(A), vi(B)) => vb(true)  requires A =/=Int B
  rule applyCmp("!=", vi(A), vi(B)) => vb(false) requires A ==Int B

  syntax Ints ::= appendInts(Ints, Ints) [function, total]
  rule appendInts(.Ints, BS) => BS
  rule appendInts(I :: IS, BS) => I :: appendInts(IS, BS)

  // Executable insertion sort used to model Python's sorted on integer lists.
  syntax Ints ::= insertInt(Int, Ints) [function, total]
  rule insertInt(I, .Ints) => I :: .Ints
  rule insertInt(I, J :: JS) => I :: J :: JS requires I <=Int J
  rule insertInt(I, J :: JS) => J :: insertInt(I, JS) requires I >Int J

  syntax Ints ::= sortInts(Ints) [function, total]
  rule sortInts(.Ints) => .Ints
  rule sortInts(I :: IS) => insertInt(I, sortInts(IS))
endmodule
