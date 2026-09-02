module MPY-SYNTAX
  imports INT-SYNTAX
  imports BOOL-SYNTAX
  imports STRING-SYNTAX

  // Concrete syntax emitted by the fixed py2mpy.py translator.  This task
  // uses only the constructors below; unsupported Python constructs cannot
  // silently acquire a meaning in this semantics.
  syntax Module ::= "Module" "(" Stmts ")"
  syntax Stmts ::= List{Stmt, ""}
  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"
                | "Return" "(" Expr ")"

  syntax Params ::= "Params" "(" Strings ")"
  syntax Strings ::= List{String, ","}

  syntax Expr ::= "Int" "(" Int ")"
                | "Name" "(" String ")"
                | "UnaryOp" "(" String "," Expr ")"
                | "BinOp" "(" String "," Expr "," Expr ")"
                | "Compare" "(" Expr "," CmpOps ")"
                | "Call" "(" Expr "," Exprs ")"
  syntax Exprs ::= List{Expr, ","}
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"
  syntax CmpOps ::= List{CmpOp, ","}
endmodule

module SEMANTIC
  imports MPY-SYNTAX
  imports INT
  imports BOOL
  imports STRING
  imports MAP

  // A binVal(I) is the canonical semantic representation of the Python
  // string bin(I).  Keeping its integer payload preserves exact symbolic
  // equality while VERIFICATION supplies a concrete string observer.
  syntax PyVal ::= "intVal" "(" Int ")"
                 | "boolVal" "(" Bool ")"
                 | "ratVal" "(" Int "," Int ")"
                 | "binVal" "(" Int ")"
  syntax Result ::= "noResult" | "result" "(" PyVal ")"

  syntax KItem ::= "boot" "(" Module "," Int "," Int ")"
                 | "exec" "(" Stmts ")"
                 | "execStmt" "(" Stmt ")"
                 | "choose" "(" Stmts "," Stmts ")"
                 | "doReturn"

  syntax PyVal ::= "eval" "(" Expr "," Map ")" [function]
                 | "unary" "(" String "," PyVal ")" [function]
                 | "binary" "(" String "," PyVal "," PyVal ")" [function]
                 | "compare" "(" String "," PyVal "," PyVal ")" [function]
                 | "callBuiltin" "(" String "," PyVal ")" [function]
                 | "roundValue" "(" PyVal ")" [function]

  configuration
    <py>
      <k> boot($PGM:Module, $N:Int, $M:Int) </k>
      <env> .Map </env>
      <result> noResult </result>
    </py>

  // Loading the one public, two-argument function binds its formal names to
  // the two concrete/symbolic inputs and starts its body.
  rule <k> boot(Module(FuncDef("rounded_avg", Params(X:String, Y:String), BODY)), N, M)
        => exec(BODY) ... </k>
       <env> .Map => (X |-> intVal(N)) (Y |-> intVal(M)) </env>

  rule exec(.Stmts) => .K
  rule exec(S REST) => execStmt(S) ~> exec(REST)

  rule <k> execStmt(If(COND, THEN, ELSE))
        => eval(COND, ENV) ~> choose(THEN, ELSE) ... </k>
       <env> ENV </env>
  rule boolVal(true)  ~> choose(THEN, _) => exec(THEN)
  rule boolVal(false) ~> choose(_, ELSE) => exec(ELSE)

  rule <k> execStmt(Return(E)) => eval(E, ENV) ~> doReturn ... </k>
       <env> ENV </env>
  rule <k> V:PyVal ~> doReturn ~> _REST => .K </k>
       <result> noResult => result(V) </result>

  rule eval(Int(I), _) => intVal(I)
  rule eval(Name(X), (X |-> V) _REST) => V
  rule eval(UnaryOp(OP, E), ENV) => unary(OP, eval(E, ENV))
  rule eval(BinOp(OP, L, R), ENV)
    => binary(OP, eval(L, ENV), eval(R, ENV))
  rule eval(Compare(L, CmpOp(OP, R)), ENV)
    => compare(OP, eval(L, ENV), eval(R, ENV))
  rule eval(Call(Name(F), E), ENV) => callBuiltin(F, eval(E, ENV))

  rule unary("-", intVal(I)) => intVal(0 -Int I)
  rule binary("+", intVal(I), intVal(J)) => intVal(I +Int J)
  rule binary("/", intVal(I), intVal(J)) => ratVal(I, J)
    requires J =/=Int 0
  rule compare(">", intVal(I), intVal(J)) => boolVal(I >Int J)
  rule callBuiltin("round", V) => roundValue(V)
  rule callBuiltin("bin", intVal(I)) => binVal(I)

  // Python 3 round on an exact rational: nearest integer, ties to even.
  // The task reaches these rules with a positive numerator and denominator 2.
  rule roundValue(ratVal(I, D)) => intVal(I /Int D)
    requires D >Int 0 andBool 2 *Int (I %Int D) <Int D
  rule roundValue(ratVal(I, D)) => intVal((I /Int D) +Int 1)
    requires D >Int 0 andBool 2 *Int (I %Int D) >Int D
  rule roundValue(ratVal(I, D)) => intVal(I /Int D)
    requires D >Int 0
     andBool 2 *Int (I %Int D) ==Int D
     andBool (I /Int D) %Int 2 ==Int 0
  rule roundValue(ratVal(I, D)) => intVal((I /Int D) +Int 1)
    requires D >Int 0
     andBool 2 *Int (I %Int D) ==Int D
     andBool (I /Int D) %Int 2 =/=Int 0
endmodule
