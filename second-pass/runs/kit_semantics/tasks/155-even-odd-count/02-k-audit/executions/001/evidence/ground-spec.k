requires "verification-with-lemma.k"

module AUDIT-GROUND-SPEC
  imports VERIFICATION-WITH-LEMMA

  claim [zero]:
    <k> Call(Name("even_odd_count"), Int(0))
        => tuple(vCons(1, vCons(0, .ValSeq)))
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

  claim [negative-twelve]:
    <k> Call(Name("even_odd_count"), Int(-12))
        => tuple(vCons(1, vCons(1, .ValSeq)))
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

  claim [one-two-three]:
    <k> Call(Name("even_odd_count"), Int(123))
        => tuple(vCons(1, vCons(2, .ValSeq)))
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
