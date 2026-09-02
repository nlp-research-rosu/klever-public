requires "reference-semantics/semantics.k"

module VERIFICATION-BASE
  imports MPY

  // The generic Map update leaves a symbolic tombstone after a call frame is
  // popped.  This proof-only normalization states the corresponding concrete
  // map fact: removing a known binding reveals the disjoint remainder.
  rule (1 |-> _FRAME:Scope REST:Map) [1 <- undef] => REST
    requires notBool (1 in_keys(REST))

  // These are the exact statement lists emitted in solution.mpy.  Naming the
  // lists keeps the reachability claims readable; the equations below expand
  // to ordinary MPY syntax before execution.
  syntax Stmts ::= "intersectionBody" [function]
  rule intersectionBody =>
    Assign(Name("left"),
           Call(Name("max"),
                Subscript(Name("interval1"), Int(0)),
                Subscript(Name("interval2"), Int(0)),
                .Exprs))
    Assign(Name("right"),
           Call(Name("min"),
                Subscript(Name("interval1"), Int(1)),
                Subscript(Name("interval2"), Int(1)),
                .Exprs))
    Assign(Name("length"), BinOp("-", Name("right"), Name("left")))
    If(Compare(Name("length"), CmpOp("<=", Int(1))),
       Return(Str("NO")) .Stmts,
       .Stmts)
    Assign(Name("divisor"), Int(2))
    For(Name("divisor"), Call(Name("range"),
                              Int(2), Name("length"), .Exprs),
        divisorBody)
    Return(Str("YES")) .Stmts

  syntax Stmts ::= "divisorBody" [function]
  rule divisorBody =>
    If(Compare(BinOp("%", Name("length"), Name("divisor")),
               CmpOp("==", Int(0))),
       Return(Str("NO")) .Stmts,
       .Stmts)
    .Stmts

  // ASCII encodings of the two observable answers.
  syntax Val ::= "yesV" [function]
               | "noV"  [function]
  rule yesV => str(iCons(89, iCons(69, iCons(83, .IntSeq))))
  rule noV  => str(iCons(78, iCons(79, .IntSeq)))

  // A mathematical primality oracle by exhaustive divisor search.
  // primeFrom(N,D) checks exactly the candidate divisors D .. N-1.
  syntax Val ::= primeFrom(Int, Int) [function]
               | primeResult(Int)   [function]
  rule primeFrom(N:Int, D:Int) => yesV
    requires D >=Int N
  rule primeFrom(N:Int, D:Int) => noV
    requires D <Int N andBool pyMod(N, D) ==Int 0
  rule primeFrom(N:Int, D:Int) => primeFrom(N, D +Int 1)
    requires D <Int N andBool pyMod(N, D) =/=Int 0

  rule primeResult(N:Int) => noV
    requires N <=Int 1
  rule primeResult(N:Int) => primeFrom(N, 2)
    requires N >Int 1

  syntax Int ::= overlapLength(Int, Int, Int, Int) [function]
  rule overlapLength(A:Int, B:Int, C:Int, D:Int)
    => minInt(B, D) -Int maxInt(A, C)
endmodule

module VERIFICATION
  imports VERIFICATION-BASE

  // This is exactly the loop-correct claim in LOOP-SPEC.  The proof workflow
  // first proves that claim against VERIFICATION-BASE, then installs the
  // proved result here as a modular summary for the whole-function theorem.
  rule
    <k> #loop(rangeObj(DIVISOR:Int, LENGTH:Int, 1),
              Name("divisor"),
              If(Compare(BinOp("%", Name("length"), Name("divisor")),
                         CmpOp("==", Int(0))),
                 Return(Str("NO")) .Stmts,
                 .Stmts)
              .Stmts)
        ~> (Return(Str("YES")) .Stmts) ~> #endcall
      => primeFrom(LENGTH, DIVISOR) ~> KONT:K
    </k>
    <env> 1 => 0 </env>
    <scopes>
      SC:Map
      1 |-> scope(
        "interval1" |-> _INTERVAL1:Val
        "interval2" |-> _INTERVAL2:Val
        "left"      |-> _LEFT:Int
        "right"     |-> _RIGHT:Int
        "length"    |-> LENGTH
        "divisor"   |-> _OLD:Int,
        parent(0))
      => SC
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <stack> ListItem(frame(KONT, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    requires 2 <=Int DIVISOR andBool DIVISOR <=Int LENGTH
    [priority(40)]
endmodule
