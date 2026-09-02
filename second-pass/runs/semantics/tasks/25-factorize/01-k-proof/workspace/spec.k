requires "verification.k"

module FACTORIZE-LOOP-SPEC
  imports FACTORIZE-VERIFICATION

  // Loop invariant and summary.  It is proved first, then made available as a
  // proved lemma for the entry-point theorem by prove.sh.
  claim [factorize-loop]:
    <k>
      #while(Compare(Name("n"), CmpOp(">", Int(1))), factorizeStep)
      ~> KONT
      => KONT
    </k>
    <env> L </env>
    <scopes>
      (L |-> scope(
        ("n" |-> N
         "divisor" |-> D
         "factors" |-> ref(H)),
        parent(0)))
      SC
      =>
      (L |-> scope(
        ("n" |-> 1
         "divisor" |-> factorDivisor(N, D)
         "factors" |-> ref(H)),
        parent(0)))
      SC
    </scopes>
    <heap>
      (H |-> list(VS)) HP
      => (H |-> list(factorLoop(N, D, VS))) HP
    </heap>
    requires N >=Int 1 andBool D >=Int 2

endmodule

module FACTORIZE-SPEC
  imports FACTORIZE-VERIFICATION-WITH-LOOP-LEMMA

  // Public theorem: for every positive input, factorize returns the canonical
  // ordered prime-factor sequence (the empty sequence for 1).
  claim [factorize-correct]:
    <k>
      Call(Name("factorize"), Int(N))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "factorize" |-> closureVal("n", factorizeBody, 0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 => 1 </scopeLoc>
    <heap>
      .Map
      => 0 |-> list(primeFactors(N))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    requires N >=Int 1
endmodule
