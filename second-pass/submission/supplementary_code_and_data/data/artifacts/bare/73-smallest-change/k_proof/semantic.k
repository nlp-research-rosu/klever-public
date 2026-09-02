requires "domains.md"

module MPY-SYNTAX
  imports INT-SYNTAX
  imports BOOL-SYNTAX
  imports STRING-SYNTAX
  imports LIST

  // The concrete syntax is deliberately the constructor syntax emitted by
  // py2mpy.py.  Statement and expression lists use the same separators as the
  // transliterator (juxtaposition and comma, respectively).
  syntax Program ::= "Module" "(" Stmts ")" [symbol(Module)]

  syntax Stmts ::= List{Stmt, ""}
  syntax Exprs ::= List{Expr, ","}
  syntax Strings ::= List{String, ","}
  syntax CmpOps ::= List{CmpOp, ","}

  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")" [symbol(FuncDef)]
                | "If" "(" Expr "," Stmts "," Stmts ")"       [symbol(If)]
                | "Return" "(" Expr ")"                         [symbol(Return)]

  syntax Params ::= "Params" "(" Strings ")" [symbol(Params)]
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")" [symbol(CmpOp)]

  syntax Expr ::= "Int" "(" Int ")"                              [symbol(IntExpr)]
                | "Name" "(" String ")"                          [symbol(Name)]
                | "Call" "(" Expr "," Exprs ")"                 [symbol(Call)]
                | "Compare" "(" Expr "," CmpOps ")"             [symbol(Compare)]
                | "Subscript" "(" Expr "," Expr ")"             [symbol(Subscript)]
                | "Slice" "(" Expr "," Expr "," Expr ")"       [symbol(Slice)]
                | "UnaryOp" "(" String "," Expr ")"             [symbol(UnaryOp)]
                | "BinOp" "(" String "," Expr "," Expr ")"     [symbol(BinOp)]
                | "NoBound"                                       [symbol(NoBound)]
endmodule

module SEMANTIC
  imports MPY-SYNTAX
  imports INT
  imports BOOL
  imports LIST
  imports K-EQUAL

  configuration
    <mpy>
      <k> $PGM:Program </k>
      <input> $INPUT:List </input>
      <result> .K </result>
    </mpy>

  // Runtime helpers.  A function body is passed as the third argument so a
  // recursive call invokes the actual parsed body, not a built-in replacement.
  // `run` is operational (rather than a function) so symbolic side conditions
  // split proof paths. `addResult` is the return continuation for 1 + recurse.
  syntax KItem ::= run(Stmts, List, Stmts)
                 | recur(Stmts, List, Stmts)
                 | finish(Int)
                 | addResult(Int)
                 | eval(Expr, List, Stmts)  [function]
  syntax Bool ::= truth(Expr, List, Stmts)  [function]
  syntax Stmts ::= concatStmts(Stmts, Stmts) [function]

  rule concatStmts(.Stmts, S2) => S2
  rule concatStmts((S:Stmt) S1, S2) => S concatStmts(S1, S2)

  rule <k> Module(FuncDef("smallest_change", Params("arr"), BODY))
             => run(BODY, L, BODY) </k>
       <input> L </input>

  // Statements.  Returning discards the remaining statements.  An if-body
  // is prepended to the continuation exactly as Python executes it.
  rule <k> run(If(Compare(Call(Name("len"), Name("arr")),
                         CmpOp("<=", Int(1))), THEN, _ELSE) REST, L, BODY)
             => run(concatStmts(THEN, REST), L, BODY) ... </k>
    requires size(L) <=Int 1
  rule <k> run(If(Compare(Call(Name("len"), Name("arr")),
                         CmpOp("<=", Int(1))), _THEN, ELSE) REST, L, BODY)
             => run(concatStmts(ELSE, REST), L, BODY) ... </k>
    requires size(L) >Int 1
  rule <k> run(If(Compare(Subscript(Name("arr"), Int(0)),
                         CmpOp("==", Subscript(Name("arr"),
                                               UnaryOp("-", Int(1))))),
                    THEN, _ELSE) REST, L, BODY)
             => run(concatStmts(THEN, REST), L, BODY) ... </k>
    requires {L[0]}:>Int ==Int {L[-1]}:>Int
  rule <k> run(If(Compare(Subscript(Name("arr"), Int(0)),
                         CmpOp("==", Subscript(Name("arr"),
                                               UnaryOp("-", Int(1))))),
                    _THEN, ELSE) REST, L, BODY)
             => run(concatStmts(ELSE, REST), L, BODY) ... </k>
    requires notBool ({L[0]}:>Int ==Int {L[-1]}:>Int)

  rule <k> run(Return(Int(I)) _REST, _L, _BODY) => finish(I) ... </k>
  rule <k> run(Return(Call(Name("smallest_change"), ARG)) _REST, L, BODY)
             => recur(BODY, {eval(ARG, L, BODY)}:>List, BODY) ... </k>
  rule <k> run(Return(BinOp("+", Int(I),
                           Call(Name("smallest_change"), ARG))) _REST, L, BODY)
             => recur(BODY, {eval(ARG, L, BODY)}:>List, BODY)
                ~> addResult(I) ... </k>
  // Ground execution continues immediately.  Symbolic proofs stop at recur,
  // which is the induction cutpoint discharged by the recurrence claims.
  rule <k> recur(BODY, L, BODY) => run(BODY, L, BODY) ... </k> [concrete]
  rule <k> finish(I) ~> addResult(N) => finish(N +Int I) ... </k>
  rule <k> finish(I) => .K </k>
       <result> .K => I </result>

  // Integer and list expressions used by solution.py.
  rule eval(Int(I), _L, _BODY) => I
  rule eval(UnaryOp("-", E), L, BODY)
    => 0 -Int {eval(E, L, BODY)}:>Int
  rule eval(BinOp("+", E1, E2), L, BODY)
    => {eval(E1, L, BODY)}:>Int +Int {eval(E2, L, BODY)}:>Int
  rule eval(Call(Name("len"), Name("arr")), L, _BODY) => size(L)
  rule eval(Subscript(Name("arr"), INDEX), L, BODY)
    => L[{eval(INDEX, L, BODY)}:>Int]
  rule eval(Subscript(Name("arr"), Slice(LOW, HIGH, NoBound)), L, BODY)
    => range(L,
             {eval(LOW, L, BODY)}:>Int,
             0 -Int {eval(HIGH, L, BODY)}:>Int)
  // Comparisons are intentionally interpreted here rather than translated by
  // py2mpy.py.  List elements are constrained to Int by these projections.
  rule truth(Compare(E1, CmpOp("<=", E2)), L, BODY)
    => {eval(E1, L, BODY)}:>Int <=Int {eval(E2, L, BODY)}:>Int
  rule truth(Compare(E1, CmpOp("==", E2)), L, BODY)
    => {eval(E1, L, BODY)}:>Int ==Int {eval(E2, L, BODY)}:>Int
endmodule
