requires "domains.md"

module MPY-SYNTAX
  imports INT-SYNTAX
  imports BOOL-SYNTAX
  imports STRING-SYNTAX

  // The prompt restricts inputs to square brackets.  BString is therefore a
  // complete, inductive representation of every input in the task's domain.
  syntax Bracket ::= "lbr" | "rbr"
  syntax BString ::= ".BString" | Bracket BString

  syntax Module ::= "Module" "(" Stmts ")"
  syntax Strings ::= List{String, ","}
  syntax Params ::= "Params" "(" Strings ")"

  syntax CmpOps ::= List{CmpOp, ","}
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"

  syntax Expr ::= "Name" "(" String ")"
                | "Int" "(" Int ")"
                | "Bool" "(" Bool ")"
                | "Str" "(" String ")"
                | "BinOp" "(" String "," Expr "," Expr ")"
                | "Compare" "(" Expr "," CmpOps ")"

  syntax Stmts ::= List{Stmt, ""}
  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "Assign" "(" Expr "," Expr ")"
                | "For" "(" Expr "," Expr "," Stmts ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"
                | "Return" "(" Expr ")"
endmodule

module SEMANTIC
  imports MPY-SYNTAX
  imports INT
  imports BOOL
  imports MAP

  syntax Val ::= "intVal" "(" Int ")"
               | "boolVal" "(" Bool ")"
               | "strVal" "(" BString ")"
  syntax Result ::= "noResult" | Val
  syntax Function ::= "function" "(" Params "," Stmts ")"

  syntax KItem ::= "start" "(" BString ")"
                 | "iterate" "(" String "," BString "," Stmts ")"

  configuration
    <py>
      <k> $PGM:Module ~> start($INPUT:BString) </k>
      <functions> .Map </functions>
      <env> .Map </env>
      <result> noResult </result>
    </py>

  // Module loading and the one-argument call used by this task.
  rule <k> Module(SS) => SS ... </k>
  rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k>
  rule <k> .Stmts => .K ... </k>

  rule <k> FuncDef(F, PS, BODY) => .K ... </k>
       <functions> FS => FS [ F <- function(PS, BODY) ] </functions>

  rule <k> start(BS) => BODY ... </k>
       <functions>
         ... "is_nested" |-> function(Params("string"), BODY) ...
       </functions>
       <env> _ => "string" |-> strVal(BS) </env>

  // Expressions in the implementation are pure, so a mathematical evaluator
  // keeps the operational statement rules small and proof-friendly.
  syntax Val ::= eval(Expr, Map) [function]
  syntax Val ::= add(Val, Val) [function]
  syntax Val ::= compare(String, Val, Val) [function]
  syntax Val ::= getVal(KItem) [function]

  rule eval(Name(X), ENV) => getVal(ENV [ X ])
  rule getVal(V:Val) => V
  rule eval(Int(I), _) => intVal(I)
  rule eval(Bool(B), _) => boolVal(B)
  rule eval(Str("["), _) => strVal(lbr .BString)
  rule eval(Str("]"), _) => strVal(rbr .BString)
  rule eval(BinOp("+", E1, E2), ENV) => add(eval(E1, ENV), eval(E2, ENV))
  rule eval(Compare(E1, CmpOp(OP, E2), .CmpOps), ENV)
    => compare(OP, eval(E1, ENV), eval(E2, ENV))

  rule add(intVal(I), intVal(J)) => intVal(I +Int J)

  rule compare("==", intVal(I), intVal(J)) => boolVal(I ==Int J)
  rule compare("<",  intVal(I), intVal(J)) => boolVal(I <Int J)
  rule compare("==", strVal(lbr .BString), strVal(lbr .BString))
    => boolVal(true)
  rule compare("==", strVal(lbr .BString), strVal(rbr .BString))
    => boolVal(false)
  rule compare("==", strVal(rbr .BString), strVal(lbr .BString))
    => boolVal(false)
  rule compare("==", strVal(rbr .BString), strVal(rbr .BString))
    => boolVal(true)

  syntax Stmts ::= choose(Val, Stmts, Stmts) [function]
  rule choose(boolVal(true),  THEN, _) => THEN
  rule choose(boolVal(false), _, ELSE) => ELSE

  // Assignment and branching.
  rule <k> Assign(Name(X), E) => .K ... </k>
       <env> ENV => ENV [ X <- eval(E, ENV) ] </env>

  rule <k> (If(E, THEN, ELSE)):KItem
        => (choose(eval(E, ENV), THEN, ELSE)):KItem ... </k>
       <env> ENV </env>

  // Python's iteration over a bracket string, one one-character string at a
  // time.  The continuation makes early Return discard the unvisited suffix.
  rule <k> For(Name(X), E, BODY)
        => iterate(X, getString(eval(E, ENV)), BODY) ... </k>
       <env> ENV => ENV [ X <- strVal(.BString) ] </env>

  syntax BString ::= getString(Val) [function]
  rule getString(strVal(BS)) => BS

  rule <k> iterate(_, .BString, _) => .K ... </k>
  rule <k> iterate(X, lbr BS:BString, BODY)
        => BODY ~> iterate(X, BS, BODY) ... </k>
       <env> ENV => ENV [ X <- strVal(lbr .BString) ] </env>
  rule <k> iterate(X, rbr BS:BString, BODY)
        => BODY ~> iterate(X, BS, BODY) ... </k>
       <env> ENV => ENV [ X <- strVal(rbr .BString) ] </env>

  // This task runs one function.  Clearing the K cell faithfully implements
  // the non-local control effect of a Python return from inside the loop.
  rule <k> Return(E) ~> _REST:K => .K </k>
       <functions> _ => .Map </functions>
       <env> ENV => .Map </env>
       <result> _ => eval(E, ENV) </result>
endmodule
