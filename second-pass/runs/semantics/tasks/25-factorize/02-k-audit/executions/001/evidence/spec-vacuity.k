requires "verification.k"

module FACTORIZE-SPEC-VACUITY
  imports FACTORIZE-VERIFICATION-WITH-LOOP-LEMMA

  // Deliberately false: appends a spurious factor 2 to every required result.
  // Witness N=1 satisfies the precondition; the real and summarized result is
  // empty, while this postcondition requires [2].
  claim [factorize-false-extra-factor]:
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
      => 0 |-> list(
           valSeqConcat(
             primeFactors(N),
             vCons(2, .ValSeq)))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    requires N >=Int 1
endmodule
