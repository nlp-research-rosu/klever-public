requires "semantic.k"

// Mathematical reference layer used by the proof.  primeResult(N,D) is the
// trial-division definition of primality from candidate divisor D onward.
// For D = 2 and N >= 2 it is "YES" exactly when N is prime: if D*D > N no
// factor can remain; otherwise D is tested and the search advances.
module VERIFICATION
  imports MPY

  syntax Value ::= "primeResult" "(" Int "," Int ")" [function]
  rule primeResult(N, D) => strVal("YES")
       requires D *Int D >Int N
  rule primeResult(N, D) => strVal("NO")
       requires D *Int D <=Int N andBool N %Int D ==Int 0
  rule primeResult(N, D) => primeResult(N, D +Int 1)
       requires D *Int D <=Int N andBool N %Int D =/=Int 0

  syntax Value ::= "intersectionResult" "(" Int "," Int "," Int "," Int ")"
                   [function]
  rule intersectionResult(A, B, C, D) => strVal("NO")
       requires minInt(B, D) -Int maxInt(A, C) <Int 2
  rule intersectionResult(A, B, C, D)
       => primeResult(minInt(B, D) -Int maxInt(A, C), 2)
       requires minInt(B, D) -Int maxInt(A, C) >=Int 2

  syntax Value ::= "lengthResult" "(" Int ")" [function]
  rule lengthResult(N) => strVal("NO") requires N <Int 2
  rule lengthResult(N) => primeResult(N, 2) requires N >=Int 2

  // This is the exact constructor tree generated in solution.mpy.  Keeping it
  // as one named function makes the claims readable while still making their
  // subject syntactically precise.
  syntax Program ::= "solutionProgram" [function]
  rule solutionProgram =>
    Module(
      FuncDef("intersection", Params("interval1", "interval2"),
        Assign(Name("left"), Subscript(Name("interval1"), Int(0)))
        If(Compare(
          Subscript(Name("interval2"), Int(0)),
          CmpOp(">", Name("left"))),
          Assign(Name("left"), Subscript(Name("interval2"), Int(0))),
          .Stmts)
        Assign(Name("right"), Subscript(Name("interval1"), Int(1)))
        If(Compare(
          Subscript(Name("interval2"), Int(1)),
          CmpOp("<", Name("right"))),
          Assign(Name("right"), Subscript(Name("interval2"), Int(1))),
          .Stmts)
        Assign(Name("length"), BinOp("-", Name("right"), Name("left")))
        If(Compare(Name("length"), CmpOp("<", Int(2))),
          Return(Str("NO")),
          .Stmts)
        Assign(Name("divisor"), Int(2))
        While(Compare(
          BinOp("*", Name("divisor"), Name("divisor")),
          CmpOp("<=", Name("length"))),
          If(Compare(
            BinOp("%", Name("length"), Name("divisor")),
            CmpOp("==", Int(0))),
            Return(Str("NO")),
            .Stmts)
          Assign(Name("divisor"), BinOp("+", Name("divisor"), Int(1))))
        Return(Str("YES"))))
endmodule

// After LOOP-CORRECTNESS-SPEC proves this same reachability fact from the
// small-step rules, the whole-program proof imports it here as a proof lemma.
module VERIFICATION-WITH-LOOP-LEMMA
  imports VERIFICATION

  rule <k>
         While(Compare(
           BinOp("*", Name("divisor"), Name("divisor")),
           CmpOp("<=", Name("length"))),
           If(Compare(
             BinOp("%", Name("length"), Name("divisor")),
             CmpOp("==", Int(0))),
             Return(Str("NO")),
             .Stmts)
           Assign(Name("divisor"), BinOp("+", Name("divisor"), Int(1))))
         ~> (Return(Str("YES")) .Stmts)
         => primeResult(N, D)
       </k>
       <env>...
         "length" |-> intVal(N)
         "divisor" |-> intVal(D)
       ...</env>
       requires N >=Int 2 andBool D >=Int 2
       [priority(40)]
endmodule
