requires "verification.k"

module AUDIT-MUTANT-FALSE
  imports HUMAN-EVAL-118-VERIFICATION

  // False for the mutated body: fixed CPython and K execution return "X".
  claim
    <k> Call(Name("get_closest_vowel"),
             str(iCons(98, iCons(97, iCons(98, .IntSeq)))))
      => str(iCons(97, .IntSeq))
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
