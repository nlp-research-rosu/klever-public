requires "verification.k"

module AUDIT-CONCRETE-SUBSTITUTIONS
  imports FACTORIZE-VERIFICATION-WITH-LOOP-LEMMA

  claim [factorize-one]:
    <k> Call(Name("factorize"), Int(1)) => ref(0) </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope("factorize" |-> closureVal("n", factorizeBody, 0), parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 => 1 </scopeLoc>
    <heap> .Map => 0 |-> list(.ValSeq) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>

  claim [factorize-eight]:
    <k> Call(Name("factorize"), Int(8)) => ref(0) </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope("factorize" |-> closureVal("n", factorizeBody, 0), parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 => 1 </scopeLoc>
    <heap>
      .Map => 0 |-> list(vCons(2, vCons(2, vCons(2, .ValSeq))))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>

  claim [factorize-seventy]:
    <k> Call(Name("factorize"), Int(70)) => ref(0) </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope("factorize" |-> closureVal("n", factorizeBody, 0), parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 => 1 </scopeLoc>
    <heap>
      .Map => 0 |-> list(vCons(2, vCons(5, vCons(7, .ValSeq))))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
endmodule
