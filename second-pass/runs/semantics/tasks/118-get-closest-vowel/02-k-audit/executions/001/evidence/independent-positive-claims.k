requires "verification.k"

module AUDIT-CLAIM-EMPTY
  imports HUMAN-EVAL-118-VERIFICATION

  claim
    <k> Call(Name("get_closest_vowel"), str(.IntSeq))
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

module AUDIT-CLAIM-ONE
  imports HUMAN-EVAL-118-VERIFICATION

  claim
    <k> Call(Name("get_closest_vowel"), str(iCons(A:Int, .IntSeq)))
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

module AUDIT-CLAIM-TWO
  imports HUMAN-EVAL-118-VERIFICATION

  claim
    <k> Call(Name("get_closest_vowel"),
             str(iCons(A:Int, iCons(B:Int, .IntSeq))))
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

module AUDIT-CLAIM-THREE-PLUS
  imports HUMAN-EVAL-118-VERIFICATION

  claim
    <k> Call(Name("get_closest_vowel"),
             str(iCons(A:Int, iCons(B:Int, iCons(C:Int, R:IntSeq)))))
      => str(closestVowelSpec(
               iCons(A, iCons(B, iCons(C, R)))))
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
