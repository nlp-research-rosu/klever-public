module MPY-SYNTAX
  imports BOOL-SYNTAX
  imports FLOAT-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX

  // The CPython-AST constructors emitted by py2mpy.py that solution.mpy uses.
  syntax Module ::= "Module" "(" Stmts ")"
  syntax Stmts ::= List{Stmt, ""}
  syntax Strings ::= List{String, ","}
  syntax Params ::= "Params" "(" Strings ")"

  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "Return" "(" Expr ")"
                | "Assign" "(" Expr "," Expr ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"
                | "For" "(" Expr "," Expr "," Stmts ")"
                | "Expr" "(" Expr ")"

  syntax Exprs ::= List{Expr, ","}
  syntax Expr ::= "Name" "(" String ")"
                | "Str" "(" String ")"
                | "Float" "(" Float ")"
                | "ListExpr" "(" Exprs ")"
                | "Compare" "(" Expr "," CmpOps ")"
                | "Attribute" "(" Expr "," String ")"
                | "Call" "(" Expr "," Exprs ")"
  syntax CmpOps ::= List{CmpOp, ","}
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"

  // Runtime values. num(P,Q) denotes the exact rational P/Q; callers must
  // supply positive denominators. Vals is deliberately an ordinary free
  // datatype, making list order and every append step visible in proofs.
  syntax Value ::= "num" "(" Int "," Int ")"
                 | "str" "(" String ")"
                 | "bool" "(" Bool ")"
                 | "list" "(" Vals ")"
                 | "none"
  syntax Vals ::= ".Vals"
                | Value "::" Vals

  syntax Result ::= "noResult" | Value
endmodule

module MPY
  imports MPY-SYNTAX
  imports BOOL
  imports FLOAT
  imports INT
  imports MAP

  configuration
    <mpy>
      <k> $PGM:Module </k>
      <input> $INPUT:Vals </input>
      <env> .Map </env>
      <result> noResult </result>
    </mpy>

  syntax KItem ::= "exec" "(" Stmts ")"
                 | "eval" "(" Expr ")"
                 | "store" "(" String ")"
                 | "discard"
                 | "ifReady" "(" Stmts "," Stmts ")"
                 | "forReady" "(" Expr "," Stmts ")"
                 | "loop" "(" String "," Stmts "," Vals ")"
                 | "put" "(" String "," Value ")"
                 | "cmpRight" "(" String "," Expr ")"
                 | "applyCmp" "(" String "," Value ")"
                 | "appendTo" "(" String ")"
                 | "returnValue"

  syntax Vals ::= append(Vals, Value) [function, total]
  rule append(.Vals, V) => V :: .Vals
  rule append(V :: VS, W) => V :: append(VS, W)

  // Calling the required module-level function with the values in <input>.
  rule <k> Module(FuncDef("numerical_letter_grade", Params("grades"), BODY))
        => exec(BODY) ...</k>
       <input> INPUT </input>
       <env> .Map => "grades" |-> list(INPUT) </env>

  // Statement sequencing.
  rule <k> exec(.Stmts) => .K ...</k>
  rule <k> exec(S SS) => S ~> exec(SS) ...</k>

  rule <k> Expr(E) => eval(E) ~> discard ...</k>
  rule <k> _V:Value ~> discard => .K ...</k>

  rule <k> Assign(Name(X), E) => eval(E) ~> store(X) ...</k>
  rule <k> V:Value ~> store(X) => put(X, V) ...</k>

  rule <k> put(X, V) => .K ...</k>
       <env>... X |-> (_ => V) ...</env>
  rule <k> put(X, V) => .K ...</k>
       <env> ENV => ENV (X |-> V) </env>
    requires notBool (X in_keys(ENV))

  rule <k> If(TEST, THEN, ELSE) => eval(TEST) ~> ifReady(THEN, ELSE) ...</k>
  rule <k> bool(true)  ~> ifReady(THEN, _) => exec(THEN) ...</k>
  rule <k> bool(false) ~> ifReady(_, ELSE) => exec(ELSE) ...</k>

  rule <k> For(Name(X), ITER, BODY) => eval(ITER) ~> forReady(Name(X), BODY) ...</k>
  rule <k> list(VS) ~> forReady(Name(X), BODY) => loop(X, BODY, VS) ...</k>
  rule <k> loop(_, _, .Vals) => .K ...</k>
  rule <k> loop(X, BODY, V :: VS)
        => put(X, V) ~> exec(BODY) ~> loop(X, BODY, VS) ...</k>

  rule <k> Return(E) => eval(E) ~> returnValue ...</k>
  rule <k> V:Value ~> returnValue => .K ...</k>
       <result> _ => V </result>

  // Expressions.
  rule <k> eval(Name(X)) => V ...</k>
       <env>... X |-> V ...</env>
  rule <k> eval(Str(S)) => str(S) ...</k>
  rule <k> eval(ListExpr(.Exprs)) => list(.Vals) ...</k>

  // Exact decimal meanings of all float literals in solution.py.
  rule <k> eval(Float(4.0)) => num(4, 1) ...</k>
  rule <k> eval(Float(3.7)) => num(37, 10) ...</k>
  rule <k> eval(Float(3.3)) => num(33, 10) ...</k>
  rule <k> eval(Float(3.0)) => num(3, 1) ...</k>
  rule <k> eval(Float(2.7)) => num(27, 10) ...</k>
  rule <k> eval(Float(2.3)) => num(23, 10) ...</k>
  rule <k> eval(Float(2.0)) => num(2, 1) ...</k>
  rule <k> eval(Float(1.7)) => num(17, 10) ...</k>
  rule <k> eval(Float(1.3)) => num(13, 10) ...</k>
  rule <k> eval(Float(1.0)) => num(1, 1) ...</k>
  rule <k> eval(Float(0.7)) => num(7, 10) ...</k>
  rule <k> eval(Float(0.0)) => num(0, 1) ...</k>

  rule <k> eval(Compare(LEFT, CmpOp(OP, RIGHT)))
        => eval(LEFT) ~> cmpRight(OP, RIGHT) ...</k>
  rule <k> V:Value ~> cmpRight(OP, RIGHT)
        => eval(RIGHT) ~> applyCmp(OP, V) ...</k>
  rule <k> num(A, B) ~> applyCmp("==", num(P, Q))
        => bool((A *Int Q) ==Int (P *Int B)) ...</k>
  rule <k> num(A, B) ~> applyCmp(">", num(P, Q))
        => bool((P *Int B) >Int (A *Int Q)) ...</k>

  // The only method used by this task: list.append. It mutates the named
  // list and evaluates to Python's None value.
  rule <k> eval(Call(Attribute(Name(X), "append"), ARG))
        => eval(ARG) ~> appendTo(X) ...</k>
  rule <k> V:Value ~> appendTo(X) => none ...</k>
       <env>... X |-> (list(VS) => list(append(VS, V))) ...</env>
endmodule
