requires "verification-with-lemma.k"

module AUDIT-FRESH-VACUITY-SPEC
  imports VERIFICATION-WITH-LEMMA

  // Deliberately false at the satisfiable entry state N = 0:
  // the real and summarized result is (1, 0), not (2, 0).
  claim [zero-has-two-even-digits]:
    <k> Call(Name("even_odd_count"), Int(0))
        => tuple(vCons(2, vCons(0, .ValSeq)))
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope("even_odd_count" |-> evenOddClosure, parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
