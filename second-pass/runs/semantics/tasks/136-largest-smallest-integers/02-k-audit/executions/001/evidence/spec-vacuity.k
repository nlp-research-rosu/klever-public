requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Fresh auditor mutation: the empty loop falsely increments the negative
  // accumulator.  VS=.ValSeq, A=0, B=0, OLD=0 satisfies the precondition,
  // but executing the loop leaves largest_negative at 0, not 1.
  claim [scan-loop-wrong-negative]:
    <k> #loop(list(VS:ValSeq), Name("value"), scanBody)
        => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> scope(
        ("lst"                 |-> INPUT:Val)
        ("largest_negative"    |-> (A:Int => negFold(VS, A) +Int 1))
        ("smallest_positive"   |-> (B:Int => posFold(VS, B)))
        ("value"               |-> (OLD:Int => finalValue(VS, OLD))),
        parent(0))
      ...
    </scopes>
    requires allInts(VS)
     andBool A <=Int 0
     andBool B >=Int 0
endmodule
