requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // Exact constructor form generated from solution.py.  These are only
  // abbreviations, so symbolic execution still uses the supplied MPY rules.
  syntax Stmts ::= "primeLoopBody" [function]
  rule primeLoopBody
    => If(
         Compare(
           BinOp("%", Name("n"), Name("divisor")),
           CmpOp("==", Int(0))),
         Return(Bool(false)) .Stmts,
         .Stmts)
       AugAssign(Name("divisor"), "+", Int(1))
       .Stmts

  syntax Stmts ::= "primeBody" [function]
  rule primeBody
    => Assign(Name("n"), Call(Name("len"), (Name("string"), .Exprs)))
       If(
         Compare(Name("n"), CmpOp("<", Int(2))),
         Return(Bool(false)) .Stmts,
         .Stmts)
       Assign(Name("divisor"), Int(2))
       While(
         Compare(Name("divisor"), CmpOp("<", Name("n"))),
         primeLoopBody)
       Return(Bool(true))
       .Stmts

  syntax Val ::= "primeLengthClosure" [function]
  rule primeLengthClosure
    => closureVal(("string", .ParamNames), primeBody, 0)

  // Proof-only observation points used by the setup claim.  They stop at the
  // generated While statement and capture its live n and divisor values;
  // they do not summarize or execute the loop body.
  syntax KItem ::= #primeLoopEntry(Int, Int)
                 | "#capturePrimeLoopN"
                 | #capturePrimeLoopD(Int)
  rule <k>
         While(_C:Expr, _B:Stmts)
         =>
         Name("n") ~> #capturePrimeLoopN
         ...
       </k>
       [priority(1)]

  rule <k>
         N:Int ~> #capturePrimeLoopN ~> REST:K
         =>
         Name("divisor") ~> #capturePrimeLoopD(N) ~> REST
       </k>
       [priority(40)]

  rule
    <k>
      D:Int ~> #capturePrimeLoopD(N:Int) ~> _REST:K
      =>
      #primeLoopEntry(N, D)
    </k>
    <env> _ => 0 </env>
    <scopes> _ => .Map </scopes>
    <scopeLoc> _ => 0 </scopeLoc>
    <stack> _ => .List </stack>
    <ret> _ => noRet </ret>
    [priority(40)]

  // Mathematical result of testing the candidate divisors D, D + 1, ..., N - 1.
  // The equations deliberately mirror the Python loop.
  syntax Bool ::= noDivisorsFrom(Int, Int) [function]
  rule noDivisorsFrom(N:Int, D:Int) => true
    requires D >=Int N
  rule noDivisorsFrom(N:Int, D:Int) => false
    requires D <Int N andBool pyMod(N, D) ==Int 0
  rule noDivisorsFrom(N:Int, D:Int) => noDivisorsFrom(N, D +Int 1)
    requires D <Int N andBool pyMod(N, D) =/=Int 0

endmodule
