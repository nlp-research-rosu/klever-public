requires "mpy-syntax.k"
requires "verification.k"

module HUMAN-EVAL
  imports HUMAN-EVAL-SYNTAX
  imports HUMAN-EVAL-VERIFICATION
  imports MAP

  syntax Value ::= iVal(Int) | bVal(Bool) | listVal(IList)

  syntax KItem ::= exec(Stmts) | execStmt(Stmt) | eval(Expr)
                 | branch(Stmts, Stmts)
                 | assignTo(String)
                 | addRight(Expr) | addValues(Int)
                 | compareRight(String, Expr) | compareValues(String, Value)
                 | "getLength" | "getLast" | "isEmpty"
                 | startFor(String, Stmts)
                 | loop(String, IList, Stmts)
                 | bind(String, Value)
                 | "doReturn"

  configuration
    <k> $PGM:Pgm </k>
    <input> $INPUT:IList </input>
    <env> .Map </env>

  // A module with one unary definition is run by calling that definition on INPUT.
  rule <k> Module(FuncDef(_F, Params(X), BODY)) => exec(BODY) </k>
       <input> INPUT </input>
       <env> .Map => X |-> listVal(INPUT) </env>

  rule <k> exec(.Stmts) => .K ... </k>
  rule <k> exec(S:Stmt SS:Stmts) => execStmt(S) ~> exec(SS) ... </k>

  rule <k> execStmt(Assign(Name(X), E)) => eval(E) ~> assignTo(X) ... </k>
  rule <k> V:Value ~> assignTo(X) => .K ... </k>
       <env> ENV => ENV [ X <- V ] </env>

  rule <k> execStmt(If(E, THEN, ELSE)) => eval(E) ~> branch(THEN, ELSE) ... </k>
  rule <k> bVal(true)  ~> branch(THEN, _ELSE) => exec(THEN) ... </k>
  rule <k> bVal(false) ~> branch(_THEN, ELSE) => exec(ELSE) ... </k>

  rule <k> execStmt(For(Name(X), E, BODY))
        => eval(E) ~> startFor(X, BODY) ... </k>
  rule <k> listVal(L) ~> startFor(X, BODY) => loop(X, L, BODY) ... </k>
  rule <k> loop(_X, .IList, _BODY) => .K ... </k>

  // Reviewer bridge-free variant: all loops use ordinary concrete iteration.
  rule <k> loop(X, I :: IS, BODY)
        => bind(X, iVal(I)) ~> exec(BODY) ~> loop(X, IS, BODY) ... </k>
       [owise]
  rule <k> bind(X, V) => .K ... </k>
       <env> ENV => ENV [ X <- V ] </env>

  rule <k> execStmt(Return(E)) => eval(E) ~> doReturn ... </k>
  rule <k> V:Value ~> doReturn ~> _REST => V </k>
  rule <k> V:Value ~> doReturn => V </k>

  rule <k> eval(Int(I)) => iVal(I) ... </k>
  rule <k> eval(Bool(B)) => bVal(B) ... </k>
  rule <k> eval(Name(X)) => V ... </k>
       <env> ... X |-> V ... </env>

  rule <k> eval(UnaryOp("-", Int(I))) => iVal(0 -Int I) ... </k>

  rule <k> eval(BinOp("+", LEFT, RIGHT))
        => eval(LEFT) ~> addRight(RIGHT) ... </k>
  rule <k> iVal(I) ~> addRight(RIGHT) => eval(RIGHT) ~> addValues(I) ... </k>
  rule <k> iVal(J) ~> addValues(I) => iVal(I +Int J) ... </k>

  rule <k> eval(Compare(LEFT, CmpOp(OP, RIGHT)))
        => eval(LEFT) ~> compareRight(OP, RIGHT) ... </k>
  rule <k> V:Value ~> compareRight(OP, RIGHT)
        => eval(RIGHT) ~> compareValues(OP, V) ... </k>
  rule <k> iVal(J) ~> compareValues("==", iVal(I)) => bVal(I ==Int J) ... </k>
  rule <k> iVal(J) ~> compareValues(">",  iVal(I)) => bVal(I >Int J) ... </k>
  rule <k> iVal(J) ~> compareValues("<=", iVal(I)) => bVal(I <=Int J) ... </k>

  // Constructor-sensitive form of len(arr) == 0, needed for symbolic lists.
  rule <k> eval(Compare(Call(Name("len"), E), CmpOp("==", Int(0))))
        => eval(E) ~> isEmpty ... </k>
       [priority(40)]
  rule <k> listVal(.IList) ~> isEmpty => bVal(true) ... </k>
  rule <k> listVal(_I :: _IS) ~> isEmpty => bVal(false) ... </k>

  rule <k> eval(Call(Name("len"), E)) => eval(E) ~> getLength ... </k>
  rule <k> listVal(L) ~> getLength => iVal(length(L)) ... </k>

  rule <k> eval(Subscript(E, UnaryOp("-", Int(1)))) => eval(E) ~> getLast ... </k>
  rule <k> listVal(L) ~> getLast => iVal(last(L)) ... </k>
endmodule
