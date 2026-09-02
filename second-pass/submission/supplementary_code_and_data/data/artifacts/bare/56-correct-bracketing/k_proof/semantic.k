requires "verification.k"

module MPY-SYNTAX
  imports INT-SYNTAX
  imports BOOL-SYNTAX
  imports STRING-SYNTAX

  syntax Pgm ::= "Module" "(" Stmts ")"
               | correctProgram()

  syntax Stmts ::= List{Stmt, ""}
                   | targetLoopBody() [function, total]
                   | targetTail() [function, total]
  syntax Strings ::= List{String, ","}

  syntax Params ::= "Params" "(" Strings ")"

  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "Assign" "(" Expr "," Expr ")"
                | "For" "(" Expr "," Expr "," Stmts ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"
                | "Return" "(" Expr ")"

  syntax Expr ::= "Name" "(" String ")"
                | "Int" "(" Int ")"
                | "Bool" "(" Bool ")"
                | "Str" "(" String ")"
                | "BinOp" "(" String "," Expr "," Expr ")"
                | "Compare" "(" Expr "," CmpOp ")"

  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"
endmodule

module MPY
  imports MPY-SYNTAX
  imports MAP
  imports INT
  imports BOOL
  imports STRING
  imports VERIFICATION

  syntax Value ::= IVal(Int) | BVal(Bool) | SVal(String) | SeqVal(BracketSeq)
  syntax Function ::= function(Params, Stmts)
  syntax Store ::= emptyStore() | bind(String, Value, Store)
  syntax Value ::= lookup(String, Store) [function]

  rule lookup(X, bind(X, V, _)) => V
  rule lookup(X, bind(Y, _, REST)) => lookup(X, REST)
    requires X =/=String Y

  syntax KItem ::= invoke(String, Value)
                 | functionBoundary()
                 | assignName(String)
                 | binopLeft(String, Expr)
                 | binopRight(String, Value)
                 | compareLeft(CmpOp)
                 | compareRight(String, Value)
                 | ifKont(Stmts, Stmts)
                 | forStart(Expr, Stmts)
                 | forString(String, String, Stmts)
                 | forBracketSeq(BracketSeq, String, Stmts)
                 | returnKont()
                 | finish()

  configuration
    <py>
      <k> $PGM:Pgm ~> invoke("correct_bracketing", SVal($INPUT:String)) </k>
      <functions> .Map </functions>
      <env> emptyStore() </env>
      <result> noResult() </result>
    </py>

  syntax Result ::= noResult() | result(Value)

  rule <k> Module(SS) => SS ... </k>
  rule targetLoopBody() =>
    If(Compare(Name("bracket"), CmpOp("==", Str("<"))),
      Assign(Name("depth"), BinOp("+", Name("depth"), Int(1))),
      Assign(Name("depth"), BinOp("-", Name("depth"), Int(1))))
    If(Compare(Name("depth"), CmpOp("<", Int(0))),
      Return(Bool(false)),
      .Stmts)
  rule targetTail() =>
    Return(Compare(Name("depth"), CmpOp("==", Int(0))))

  // This is exactly the tree in solution.mpy, named so that proof claims stay
  // readable.  krun still parses and executes solution.mpy itself.
  rule correctProgram() =>
    Module(
      FuncDef("correct_bracketing", Params("brackets"),
        Assign(Name("depth"), Int(0))
        For(Name("bracket"), Name("brackets"),
          targetLoopBody())
        targetTail()))
  rule <k> (S:Stmt REST:Stmts) => S ~> REST ... </k>
  rule <k> .Stmts => .K ... </k>

  rule <k> FuncDef(F, PS, BODY) => .K ... </k>
       <functions> M => M [ F <- function(PS, BODY) ] </functions>

  rule <k> invoke(F, V) => BODY ~> functionBoundary() ... </k>
       <functions> ... F |-> function(Params(P, .Strings), BODY) ... </functions>
       <env> _ => bind(P, V, emptyStore()) </env>

  rule <k> Int(I) => IVal(I) ... </k>
  rule <k> Bool(B) => BVal(B) ... </k>
  rule <k> Str(S) => SVal(S) ... </k>
  rule <k> Name(X) => lookup(X, STORE) ... </k>
       <env> STORE </env>

  rule <k> Assign(Name(X), E) => E ~> assignName(X) ... </k>
  rule <k> V:Value ~> assignName(X) => .K ... </k>
       <env> STORE => bind(X, V, STORE) </env>

  rule <k> BinOp(OP, L, R) => L ~> binopLeft(OP, R) ... </k>
  rule <k> V:Value ~> binopLeft(OP, R) => R ~> binopRight(OP, V) ... </k>
  rule <k> IVal(J) ~> binopRight("+", IVal(I)) => IVal(I +Int J) ... </k>
  rule <k> IVal(J) ~> binopRight("-", IVal(I)) => IVal(I -Int J) ... </k>

  rule <k> Compare(L, C) => L ~> compareLeft(C) ... </k>
  rule <k> V:Value ~> compareLeft(CmpOp(OP, R))
        => R ~> compareRight(OP, V) ... </k>
  rule <k> SVal(R) ~> compareRight("==", SVal(L))
        => BVal(L ==String R) ... </k>
  rule <k> IVal(R) ~> compareRight("==", IVal(L))
        => BVal(L ==Int R) ... </k>
  rule <k> IVal(R) ~> compareRight("<", IVal(L))
        => BVal(L <Int R) ... </k>

  rule <k> If(E, THEN, ELSE) => E ~> ifKont(THEN, ELSE) ... </k>
  rule <k> BVal(true) ~> ifKont(THEN, _) => THEN ... </k>
  rule <k> BVal(false) ~> ifKont(_, ELSE) => ELSE ... </k>

  rule <k> For(TARGET, ITERABLE, BODY)
        => ITERABLE ~> forStart(TARGET, BODY) ... </k>
  rule <k> SVal(S) ~> forStart(Name(X), BODY)
        => forString(S, X, BODY) ... </k>
  rule <k> SeqVal(BS) ~> forStart(Name(X), BODY)
        => forBracketSeq(BS, X, BODY) ... </k>
  rule <k> forString(S, _, _) => .K ... </k>
    requires S ==String ""
  rule <k> forString(S, X, BODY)
        => BODY ~> forString(substrString(S, 1, lengthString(S)), X, BODY) ... </k>
       <env> STORE => bind(X, SVal(substrString(S, 0, 1)), STORE) </env>
    requires S =/=String ""
  rule <k> forBracketSeq(noBrackets(), _, _) => .K ... </k>
  rule <k> forBracketSeq(openBracket(BS), X, BODY)
        => BODY ~> forBracketSeq(BS, X, BODY) ... </k>
       <env> STORE => bind(X, SVal("<"), STORE) </env>
  rule <k> forBracketSeq(closeBracket(BS), X, BODY)
        => BODY ~> forBracketSeq(BS, X, BODY) ... </k>
       <env> STORE => bind(X, SVal(">"), STORE) </env>

  rule <k> Return(E) => E ~> returnKont() ... </k>
  rule <k> V:Value ~> returnKont() ~> _REST:K
        => V ~> finish() </k>
  rule <k> V:Value ~> finish() => .K </k>
       <result> _ => result(V) </result>
endmodule
