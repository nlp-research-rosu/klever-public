module MPY-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX

  syntax Module ::= "Module" "(" Stmts ")"
  syntax Stmts ::= List{Stmt, ""}
  syntax Params ::= "Params" "(" Strings ")"
  syntax Strings ::= List{String, ","}

  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "Assign" "(" Expr "," Expr ")"
                | "For" "(" Expr "," Expr "," Stmts ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"
                | "Return" "(" Expr ")"

  syntax Expr ::= "Int" "(" Int ")"
                | "Name" "(" String ")"
                | "UnaryOp" "(" String "," Expr ")"
                | "Attribute" "(" Expr "," String ")"
                | "Call" "(" Expr "," Exprs ")"
                | "Compare" "(" Expr "," CmpOps ")"
  syntax Exprs ::= List{Expr, ","}
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"
  syntax CmpOps ::= List{CmpOp, ","}
endmodule

module MPY
  imports MPY-SYNTAX
  imports INT
  imports BOOL
  imports MAP

  // Values used by this task's executable Mini-Python semantics.
  syntax IntSeq ::= ".Ints"
                  | "cons" "(" Int "," IntSeq ")"
  syntax Value ::= "VInt" "(" Int ")"
                 | "VBool" "(" Bool ")"
                 | "VList" "(" IntSeq ")"
  syntax Result ::= "noResult" | Value
  syntax KItem ::= "boot"

  configuration
    <mpy>
      <k> boot </k>
      <program> $PGM:Module </program>
      <input> $INPUT:Value </input>
      <env> .Map </env>
      <result> noResult </result>
    </mpy>

  // Pure expression evaluation.  The covered operations are exactly those
  // emitted for solution.py; unsupported Python constructs cannot silently run.
  syntax Value ::= eval(Expr, Map) [function]
  syntax Value ::= negate(Value) [function]
  syntax Int ::= asInt(Value) [function]
  syntax IntSeq ::= asInts(Value) [function]

  rule eval(Int(I), _) => VInt(I)
  rule eval(Name(X), RHO) => {RHO[X]}:>Value
    requires X in_keys(RHO)
  rule eval(UnaryOp("-", E), RHO) => negate(eval(E, RHO))
  rule eval(Call(Attribute(E, "count"), ARG), RHO)
    => VInt(count(asInt(eval(ARG, RHO)), asInts(eval(E, RHO))))
  rule eval(Compare(E1, CmpOp(">=", E2)), RHO)
    => VBool(asInt(eval(E1, RHO)) >=Int asInt(eval(E2, RHO)))
  rule eval(Compare(E1, CmpOp(">", E2)), RHO)
    => VBool(asInt(eval(E1, RHO)) >Int asInt(eval(E2, RHO)))

  rule negate(VInt(I)) => VInt(0 -Int I)
  rule asInt(VInt(I)) => I
  rule asInts(VList(IS)) => IS

  syntax Int ::= count(Int, IntSeq) [function, total]
  rule count(_, .Ints) => 0
  rule count(I, cons(I, IS)) => 1 +Int count(I, IS)
  rule count(I, cons(J, IS)) => count(I, IS)
    requires I =/=Int J

  // Small-step statement execution.
  syntax KItem ::= exec(Stmts)
                 | execStmt(Stmt)
                 | choose(Value, Stmts, Stmts)
                 | loop(String, IntSeq, Stmts)

  rule <k> boot => exec(S) </k>
       <program> Module(FuncDef("search", Params("lst"), S)) </program>
       <input> L </input>
       <env> .Map => "lst" |-> L </env>

  rule exec(.Stmts) => .K
  rule exec(S:Stmt SS:Stmts) => execStmt(S) ~> exec(SS)

  rule <k> execStmt(Assign(Name(X), E)) => .K ... </k>
       <env> RHO => RHO[X <- eval(E, RHO)] </env>

  rule <k> execStmt(If(E, THEN, ELSE)) => choose(eval(E, RHO), THEN, ELSE) ... </k>
       <env> RHO </env>
  rule choose(VBool(true), THEN, _) => exec(THEN)
  rule choose(VBool(false), _, ELSE) => exec(ELSE)

  rule <k> execStmt(For(Name(X), E, BODY)) => loop(X, asInts(eval(E, RHO)), BODY) ... </k>
       <env> RHO </env>
  rule loop(_, .Ints, _) => .K
  rule <k> loop(X, cons(I, IS), BODY) => exec(BODY) ~> loop(X, IS, BODY) ... </k>
       <env> RHO => RHO[X <- VInt(I)] </env>

  rule <k> execStmt(Return(E)) ~> _:K => .K </k>
       <env> RHO => .Map </env>
       <result> noResult => eval(E, RHO) </result>
endmodule

module SEMANTIC
  imports MPY
endmodule
