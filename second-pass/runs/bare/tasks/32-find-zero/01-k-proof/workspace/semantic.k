requires "domains.md"

module SEMANTIC-SYNTAX
  imports INT-SYNTAX
  imports BOOL-SYNTAX
  imports STRING-SYNTAX
  imports MAP
  imports LIST

  syntax Strings ::= List{String, ","}
  syntax Params ::= "Params" "(" Strings ")"

  syntax Exprs ::= List{Expr, ","}
  syntax Expr ::= "Int" "(" Int ")"
                | "Name" "(" String ")"
                | "UnaryOp" "(" String "," Expr ")"
                | "BinOp" "(" String "," Expr "," Expr ")"
                | "Compare" "(" Expr "," CmpOp ")"
                | "Call" "(" Expr "," Expr ")"
                | "Call" "(" Expr "," Expr "," Expr ")"
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"

  syntax Stmts ::= List{Stmt, ""}
  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "Assign" "(" Expr "," Expr ")" [strict(2)]
                | "Return" "(" Expr ")" [strict]
                | "For" "(" Expr "," Expr "," Stmts ")"
                | "While" "(" Expr "," Stmts ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"

  syntax Program ::= "Module" "(" Stmts ")"
                   | Program ";;" Expr

  // Values are exact rationals.  All rules maintain a positive denominator.
  syntax Val ::= "rat" "(" Int "," Int ")"
               | "bool" "(" Bool ")"
               | "list" "(" List ")"
  syntax Expr ::= Val
  syntax KResult ::= Val

  // A convenient external entry point used by runners and specifications.
  syntax Expr ::= "Invoke" "(" String "," Val ")"
endmodule

module SEMANTIC
  imports SEMANTIC-SYNTAX
  imports INT
  imports BOOL
  imports STRING
  imports MAP
  imports LIST

  configuration
    <T>
      <k> $PGM:Program </k>
      <env> .Map </env>
      <functions> .Map </functions>
      <stack> .List </stack>
    </T>

  // Runtime data kept outside the translated language.
  syntax Fun ::= function1(String, Stmts)
               | function2(String, String, Stmts)
  syntax Frame ::= frame(K, Map)

  syntax KItem ::= exec(Stmts)
                 | "cleanup"
                 | forStart(String, Stmts)
                 | forLoop(String, List, Stmts)
                 | whileTest(Expr, Stmts)
                 | ifTest(Stmts, Stmts)
                 | compareLeft(String, Expr)
                 | compareRight(String, Val)
                 | call1(String)
                 | callArg1(String, Expr)
                 | callArg2(String, Val)
                 | invoke1(String, Val)
                 | invoke2(String, Val, Val)

  // Rational helpers reduce after every operation to keep execution compact.
  syntax Int ::= gcdInt(Int, Int) [function, total]
  rule gcdInt(A, 0) => absInt(A) [simplification]
  rule gcdInt(A, B) => gcdInt(B, A modInt B)
    requires B =/=Int 0 [simplification]

  syntax Val ::= makeRat(Int, Int) [function, total]
               | addRat(Val, Val) [function, total]
               | subRat(Val, Val) [function, total]
               | mulRat(Val, Val) [function, total]
               | divRat(Val, Val) [function, total]
               | negRat(Val) [function, total]

  rule makeRat(0, D) => rat(0, 1)
    requires D =/=Int 0 [simplification]
  rule makeRat(N, D) => makeRat(0 -Int N, 0 -Int D)
    requires D <Int 0 [simplification]
  rule makeRat(N, D)
    => rat(N divInt gcdInt(absInt(N), D), D divInt gcdInt(absInt(N), D))
    requires N =/=Int 0 andBool D >Int 0 [simplification]

  rule addRat(rat(A, B), rat(C, D))
    => makeRat(A *Int D +Int C *Int B, B *Int D) [simplification]
  rule subRat(rat(A, B), rat(C, D))
    => makeRat(A *Int D -Int C *Int B, B *Int D) [simplification]
  rule mulRat(rat(A, B), rat(C, D))
    => makeRat(A *Int C, B *Int D) [simplification]
  rule divRat(rat(A, B), rat(C, D))
    => makeRat(A *Int D, B *Int C)
    requires C =/=Int 0 [simplification]
  rule negRat(rat(A, B)) => rat(0 -Int A, B) [simplification]

  // Module loading, execution of statement lists, and cleanup.
  rule <k> Module(SS) ;; E => exec(SS) ~> E ~> cleanup ...</k>
  rule exec(.Stmts) => .K
  rule exec(S SS) => S ~> exec(SS)

  rule <k> V:Val ~> cleanup => V ...</k>
       <env> _ => .Map </env>
       <functions> _ => .Map </functions>
       <stack> .List </stack>

  // Function definitions are immutable for this translated program.
  rule <k> FuncDef(F, Params(P), BODY) => .K ...</k>
       <functions> M => M [ F <- function1(P, BODY) ] </functions>
  rule <k> FuncDef(F, Params(P1, P2), BODY) => .K ...</k>
       <functions> M => M [ F <- function2(P1, P2, BODY) ] </functions>

  // Variables and primitive expressions.
  rule <k> Int(I) => rat(I, 1) ...</k>
  rule <k> Name(X) => V ...</k>
       <env>... X |-> V:Val ...</env>

  rule UnaryOp("-", V:Val) => negRat(V)
  rule BinOp("+", A:Val, B:Val) => addRat(A, B)
  rule BinOp("-", A:Val, B:Val) => subRat(A, B)
  rule BinOp("*", A:Val, B:Val) => mulRat(A, B)
  rule BinOp("/", A:Val, B:Val) => divRat(A, B)

  context UnaryOp(_, HOLE)
  context BinOp(_, HOLE, _)
  context BinOp(_, _V:Val, HOLE)

  // The generated program uses single comparisons, kept faithful to the AST.
  rule Compare(E, CmpOp(OP, R)) => E ~> compareLeft(OP, R)
  rule V:Val ~> compareLeft(OP, R) => R ~> compareRight(OP, V)
  rule rat(B, DB) ~> compareRight(">", rat(A, DA))
    => bool(A *Int DB >Int B *Int DA)

  // Assignment and structured control flow.
  rule <k> Assign(Name(X), V:Val) => .K ...</k>
       <env> RHO => RHO [ X <- V ] </env>

  rule For(Name(X), E, BODY) => E ~> forStart(X, BODY)
  rule list(L) ~> forStart(X, BODY) => forLoop(X, L, BODY)
  rule forLoop(_X, .List, _BODY) => .K
  rule forLoop(X, ListItem(V:Val) REST, BODY)
    => Assign(Name(X), V) ~> exec(BODY) ~> forLoop(X, REST, BODY)

  rule While(COND, BODY) => COND ~> whileTest(COND, BODY)
  rule bool(true) ~> whileTest(COND, BODY)
    => exec(BODY) ~> While(COND, BODY)
  rule bool(false) ~> whileTest(_COND, _BODY) => .K

  rule If(COND, YES, NO) => COND ~> ifTest(YES, NO)
  rule bool(true) ~> ifTest(YES, _NO) => exec(YES)
  rule bool(false) ~> ifTest(_YES, NO) => exec(NO)

  // Evaluate call arguments left-to-right before changing the local frame.
  rule Call(Name(F), E) => E ~> call1(F)
  rule V:Val ~> call1(F) => invoke1(F, V)
  rule Call(Name(F), E1, E2) => E1 ~> callArg1(F, E2)
  rule V:Val ~> callArg1(F, E2) => E2 ~> callArg2(F, V)
  rule V2:Val ~> callArg2(F, V1) => invoke2(F, V1, V2)
  rule Invoke(F, V) => invoke1(F, V)

  rule <k> invoke1(F, V) ~> CALLER => exec(BODY) </k>
       <env> RHO => P |-> V </env>
       <functions>... F |-> function1(P, BODY) ...</functions>
       <stack> S => ListItem(frame(CALLER, RHO)) S </stack>

  rule <k> invoke2(F, V1, V2) ~> CALLER => exec(BODY) </k>
       <env> RHO => P1 |-> V1 P2 |-> V2 </env>
       <functions>... F |-> function2(P1, P2, BODY) ...</functions>
       <stack> S => ListItem(frame(CALLER, RHO)) S </stack>

  // Return abandons the rest of the callee and resumes its saved continuation.
  rule <k> Return(V:Val) ~> _CURRENT => V ~> CALLER </k>
       <env> _ => RHO </env>
       <stack> ListItem(frame(CALLER, RHO)) S => S </stack>
endmodule
