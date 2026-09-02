requires "verification.k"

module SPEC-VACUITY
  imports FACTORIZE-VERIFICATION-WITH-LOOP-LEMMA

  // False result mutation: the actual result for N is required to equal the
  // factorization of N+1. N=1 is a satisfying witness: [] is not [2].
  claim [factorize-wrong-successor-result]:
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
      => 0 |-> list(primeFactors(N +Int 1))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    requires N >=Int 1
endmodule
