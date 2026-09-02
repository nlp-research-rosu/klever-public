requires "verification.k"

module SPEC-VACUITY
  imports HUMAN-EVAL-118-VERIFICATION

  // Fresh false postcondition: the satisfying input "bab" returns "a", not "".
  claim
    <k> Call(Name("get_closest_vowel"),
             str(iCons(98, iCons(97, iCons(98, .IntSeq)))))
      => str(.IntSeq)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
             "get_closest_vowel"
               |-> closureVal("word", getClosestBody, 0),
             parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
