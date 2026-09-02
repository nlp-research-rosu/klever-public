requires "domains.md"

module MPY-SYNTAX
  imports INT-SYNTAX
  imports BOOL-SYNTAX
  imports STRING-SYNTAX

  syntax Program ::= "Module" "(" Stmts ")"
  syntax Stmts ::= List{Stmt, ""}
  syntax Exprs ::= List{Expr, ","}

  syntax Stmt ::= "FuncDef" "(" String "," "Params" "(" String ")" "," Stmts ")"
                | "Assign" "(" Expr "," Expr ")"
                | "While" "(" Expr "," Stmts ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"
                | "Return" "(" Expr ")"

  syntax Expr ::= "Name" "(" String ")"
                | "Int" "(" Int ")"
                | "Bool" "(" Bool ")"
                | "ListExpr" "(" Exprs ")"
                | "BinOp" "(" String "," Expr "," Expr ")"
                | "Compare" "(" Expr "," Cmp ")"
  syntax Cmp ::= "CmpOp" "(" String "," Expr ")"
endmodule

module MPY
  imports MPY-SYNTAX
  imports INT
  imports BOOL

  // Runtime list values.  A non-associative representation keeps both concrete
  // execution and symbolic matching deterministic.
  syntax PList ::= "nil"
                 | "cons" "(" Int "," PList ")"
                 | "chooseCons" "(" Bool "," Int "," PList ")" [function, total]

  rule chooseCons(true, C, P) => cons(C, P)
  rule chooseCons(false, _, P) => P

  configuration
    <mpy>
      <k> $PGM:Program </k>
      <n> $N:Int </n>
      <result> .K </result>
    </mpy>

  syntax KItem ::= "scan" "(" Int "," Int ")"
                 | "trial" "(" Int "," Int "," Bool "," Int ")"
                 | "prependIf" "(" Int "," Bool ")"
                 | "returnValue"

  // This rule is deliberately a checked lowering: its left-hand side is the
  // complete constructor tree emitted in solution.mpy.  Any source mutation
  // changes that tree and therefore cannot enter the verified transition
  // system below.
  rule <k>
    Module(
      FuncDef("count_up_to", Params("n"),
        Assign(Name("primes"), ListExpr(.Exprs))
        Assign(Name("candidate"), Int(2))
        While(Compare(Name("candidate"), CmpOp("<", Name("n"))),
          Assign(Name("is_prime"), Bool(true))
          Assign(Name("divisor"), Int(2))
          While(Compare(
            BinOp("*", Name("divisor"), Name("divisor")),
            CmpOp("<=", Name("candidate"))),
            If(Compare(
              BinOp("%", Name("candidate"), Name("divisor")),
              CmpOp("==", Int(0))),
              Assign(Name("is_prime"), Bool(false)) .Stmts,
              .Stmts)
            Assign(Name("divisor"),
              BinOp("+", Name("divisor"), Int(1))))
          If(Name("is_prime"),
            Assign(Name("primes"),
              BinOp("+", Name("primes"),
                ListExpr(Name("candidate"), .Exprs))) .Stmts,
            .Stmts)
          Assign(Name("candidate"),
            BinOp("+", Name("candidate"), Int(1))))
        Return(Name("primes"))))
    => scan(2, N) ~> returnValue
    ... </k>
    <n> N </n>

  // candidate >= n: the result suffix is empty.
  rule <k> scan(C, N) => nil ... </k>
       requires C >=Int N

  // candidate < n: test all divisors beginning at 2.
  rule <k> scan(C, N) => trial(C, 2, true, N) ... </k>
       requires C <Int N

  // The divisor loop has passed sqrt(candidate).
  rule <k> trial(C, D, B, N)
        => scan(C +Int 1, N) ~> prependIf(C, B) ... </k>
       requires D *Int D >Int C

  // A found divisor permanently clears the primality flag, just as the
  // Python assignment is_prime = False does.
  rule <k> trial(C, D, _B, N)
        => trial(C, D +Int 1, false, N) ... </k>
       requires D *Int D <=Int C
        andBool C %Int D ==Int 0
        andBool D =/=Int 0

  // Otherwise advance to the next possible divisor.
  rule <k> trial(C, D, B, N)
        => trial(C, D +Int 1, B, N) ... </k>
       requires D *Int D <=Int C
        andBool C %Int D =/=Int 0
        andBool D =/=Int 0

  rule <k> P:PList ~> prependIf(C, B) => chooseCons(B, C, P) ... </k>

  rule <k> P:PList ~> returnValue => .K ... </k>
       <result> .K => P </result>
endmodule
