requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY
  imports INT
  imports BOOL

  // The next state of the four-state subsequence recognizer.
  syntax Int ::= nestedStep(Int, Int) [function, total]
  rule nestedStep(C, S) => S +Int 1
    requires S <Int 2 andBool C ==Int 91
  rule nestedStep(C, S) => S
    requires S <Int 2 andBool C =/=Int 91
  rule nestedStep(C, S) => S +Int 1
    requires S >=Int 2 andBool S <Int 4 andBool C ==Int 93
  rule nestedStep(C, S) => S
    requires S >=Int 2 andBool S <Int 4 andBool C =/=Int 93
  rule nestedStep(_C, S) => S
    requires S >=Int 4

  // Scan a code sequence starting in state S.
  syntax Int ::= nestedScan(IntSeq, Int) [function, total]
  rule nestedScan(.IntSeq, S) => S
  rule nestedScan(iCons(C, CS), S) =>
    nestedScan(CS, nestedStep(C, S))

  // The prompt's stated input domain: strings containing only square brackets.
  syntax Bool ::= bracketInput(IntSeq) [function, total]
  rule bracketInput(.IntSeq) => true
  rule bracketInput(iCons(C, CS)) =>
    (C ==Int 91 orBool C ==Int 93) andBool bracketInput(CS)

  // A completed state 4 means that [ [ ] ] occurred in order as a subsequence.
  syntax Bool ::= nestedResult(IntSeq) [function, total]
  rule nestedResult(CS) => nestedScan(CS, 0) ==Int 4
endmodule
