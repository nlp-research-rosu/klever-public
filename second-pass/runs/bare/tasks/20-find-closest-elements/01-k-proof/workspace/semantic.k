requires "rat.md"

module MPY-SYNTAX
  imports BOOL-SYNTAX
  imports INT-SYNTAX
  imports RAT-SYNTAX
  imports STRING-SYNTAX

  // The constructor grammar emitted by py2mpy.py for solution.py.
  syntax Program ::= "Module" "(" Stmts ")"
  syntax Stmts ::= List{Stmt, ""}
  syntax Params ::= "Params" "(" String ")"
  syntax Strings ::= List{String, ","}

  syntax Stmt ::= "ImportFrom" "(" String "," Strings ")"
                | "FuncDef" "(" String "," Params "," Stmts ")"
                | "Assign" "(" Expr "," Expr ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"
                | "While" "(" Expr "," Stmts ")"
                | "Return" "(" Expr ")"

  syntax Expr ::= "Name" "(" String ")"
                | "Int" "(" Int ")"
                | "Subscript" "(" Expr "," Expr ")"
                | "BinOp" "(" String "," Expr "," Expr ")"
                | "Call" "(" Expr "," Expr ")"
                | "Compare" "(" Expr "," CmpOp ")"
                | "TupleExpr" "(" Expr "," Expr ")"
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"

  // Runtime values. Lists are explicit cons lists so that symbolic lookup and
  // length are defined by this semantics, rather than delegated to a host.
  syntax Value ::= "vint" "(" Int ")"
                 | "vnum" "(" Rat ")"
                 | "vbool" "(" Bool ")"
                 | "vnil"
                 | "vlist" "(" Value "," Value ")"
                 | "vtuple" "(" Value "," Value ")"

  syntax Input ::= Program
                 | "run" "(" Program "," Value ")"
endmodule

module MPY-SEMANTIC
  imports MPY-SYNTAX
  imports BOOL
  imports INT
  imports RAT
  imports MAP

  syntax Result ::= "noResult" | Value
  syntax Function ::= "function" "(" Params "," Stmts ")"

  configuration
    <mpy>
      <k> $PGM:Input </k>
      <env> .Map </env>
      <functions> .Map </functions>
      <result> noResult </result>
    </mpy>

  // Control items.
  syntax KItem ::= exec(Stmts)
                 | invoke(String, Value)
                 | bindAndExec(String, Stmts, Value)
                 | eval(Expr)
                 | assignTo(String)
                 | binLeft(String, Expr)
                 | binRight(String, Value)
                 | subscriptLeft(Expr)
                 | subscriptRight(Value)
                 | compareLeft(String, Expr)
                 | compareRight(String, Value)
                 | callOne(Value)
                 | tupleLeft(Expr)
                 | tupleRight(Value)
                 | choose(Stmts, Stmts)
                 | whileChoose(Expr, Stmts)
                 | "finishReturn"

  // Pure helpers implementing the relevant Python value operations.
  syntax Int ::= valueLength(Value) [function]
  rule valueLength(vnil) => 0
  rule valueLength(vlist(_, T)) => 1 +Int valueLength(T)

  syntax Value ::= valueAt(Value, Int) [function]
  rule valueAt(vlist(H, _), 0) => H
  rule valueAt(vlist(_, T), I) => valueAt(T, I -Int 1)
    requires I >Int 0

  syntax Value ::= valuePlus(Value, Value) [function]
                 | valueMinus(Value, Value) [function]
  rule valuePlus(vint(I), vint(J)) => vint(I +Int J)
  rule valuePlus(vnum(R), vnum(S)) => vnum(R +Rat S)
  rule valuePlus(vint(I), vnum(R)) => vnum(I +Rat R)
  rule valuePlus(vnum(R), vint(I)) => vnum(R +Rat I)
  rule valueMinus(vint(I), vint(J)) => vint(I -Int J)
  rule valueMinus(vnum(R), vnum(S)) => vnum(R -Rat S)
  rule valueMinus(vint(I), vnum(R)) => vnum(I -Rat R)
  rule valueMinus(vnum(R), vint(I)) => vnum(R -Rat I)

  syntax Bool ::= valueLess(Value, Value) [function]
  rule valueLess(vint(I), vint(J)) => I <Int J
  rule valueLess(vnum(R), vnum(S)) => R <Rat S
  rule valueLess(vint(I), vnum(R)) => I <Rat R
  rule valueLess(vnum(R), vint(I)) => R <Rat I

  // Load a module, then optionally invoke its entry point.
  rule <k> Module(SS) => exec(SS) ... </k>
  rule <k> run(Module(SS), ARG) => exec(SS) ~> invoke("find_closest_elements", ARG) ... </k>
  rule <k> exec(.Stmts) => .K ... </k>
  rule <k> exec(S SS) => S ~> exec(SS) ... </k>

  rule <k> ImportFrom(_, _) => .K ... </k>
  rule <k> FuncDef(F, P, BODY) => .K ... </k>
       <functions> FS => FS [ F <- function(P, BODY) ] </functions>

  rule <k> invoke(F, ARG) => bindAndExec(PNAME, BODY, ARG) ... </k>
       <functions> ... F |-> function(Params(PNAME), BODY) ... </functions>
  rule <k> bindAndExec(PNAME, BODY, ARG) => exec(BODY) ... </k>
       <env> _ => PNAME |-> ARG </env>

  // Statements.
  rule <k> Assign(Name(X), E) => eval(E) ~> assignTo(X) ... </k>
  rule <k> V:Value ~> assignTo(X) => .K ... </k>
       <env> RHO => RHO [ X <- V ] </env>

  rule <k> If(COND, YES, NO) => eval(COND) ~> choose(YES, NO) ... </k>
  rule <k> vbool(true) ~> choose(YES, _) => exec(YES) ... </k>
  rule <k> vbool(false) ~> choose(_, NO) => exec(NO) ... </k>

  rule <k> While(COND, BODY) => eval(COND) ~> whileChoose(COND, BODY) ... </k>
  rule <k> vbool(true) ~> whileChoose(COND, BODY)
        => exec(BODY) ~> While(COND, BODY) ... </k>
  rule <k> vbool(false) ~> whileChoose(_, _) => .K ... </k>

  rule <k> Return(E) => eval(E) ~> finishReturn ... </k>
  rule <k> V:Value ~> finishReturn ~> _:K => .K </k>
       <env> _ => .Map </env>
       <functions> _ => .Map </functions>
       <result> _ => V </result>

  // Expressions and their left-to-right evaluation contexts.
  rule <k> eval(Name(X)) => V ... </k>
       <env> ... X |-> V ... </env>
  rule <k> eval(Int(I)) => vint(I) ... </k>

  rule <k> eval(BinOp(OP, L, R)) => eval(L) ~> binLeft(OP, R) ... </k>
  rule <k> V:Value ~> binLeft(OP, R) => eval(R) ~> binRight(OP, V) ... </k>
  rule <k> W:Value ~> binRight("+", V) => valuePlus(V, W) ... </k>
  rule <k> W:Value ~> binRight("-", V) => valueMinus(V, W) ... </k>

  rule <k> eval(Subscript(L, I)) => eval(L) ~> subscriptLeft(I) ... </k>
  rule <k> V:Value ~> subscriptLeft(I) => eval(I) ~> subscriptRight(V) ... </k>
  rule <k> vint(I) ~> subscriptRight(V) => valueAt(V, I) ... </k>

  rule <k> eval(Compare(L, CmpOp(OP, R)))
        => eval(L) ~> compareLeft(OP, R) ... </k>
  rule <k> V:Value ~> compareLeft(OP, R)
        => eval(R) ~> compareRight(OP, V) ... </k>
  rule <k> W:Value ~> compareRight("<", V)
        => vbool(valueLess(V, W)) ... </k>

  // `len` is the only callable needed here. Keeping the callable as a value is
  // unnecessary, so recognize its AST name before normal name lookup.
  rule <k> eval(Call(Name("len"), ARG)) => eval(ARG) ~> callOne(vnil) ... </k>
  rule <k> V:Value ~> callOne(vnil) => vint(valueLength(V)) ... </k>

  rule <k> eval(TupleExpr(A, B)) => eval(A) ~> tupleLeft(B) ... </k>
  rule <k> V:Value ~> tupleLeft(B) => eval(B) ~> tupleRight(V) ... </k>
  rule <k> W:Value ~> tupleRight(V) => vtuple(V, W) ... </k>
endmodule

module MPY
  imports MPY-SEMANTIC
endmodule
