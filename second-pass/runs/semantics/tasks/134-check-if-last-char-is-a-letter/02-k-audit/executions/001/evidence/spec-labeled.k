requires "verification.k"

module SPEC
  imports VERIFICATION

  // Empty string.
  claim [audit-empty]:
    <k> #checkIfLastChar(str(.IntSeq)) => false </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  // One-character strings.
  claim [audit-one-alpha]:
    <k> #checkIfLastChar(str(iCons(C:Int, .IntSeq))) => true </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires isAlphaC(C)

  claim [audit-one-nonalpha]:
    <k> #checkIfLastChar(str(iCons(C:Int, .IntSeq))) => false </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires notBool isAlphaC(C)

  // Strings of length at least two: PREV is the character immediately before
  // LAST.  PREFIX remains completely symbolic.
  claim [audit-long-true]:
    <k>
      #checkIfLastChar(
        str(seqConcat(PREFIX:IntSeq,
                      iCons(PREV:Int, iCons(LAST:Int, .IntSeq)))))
      => true
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires isLen(PREFIX) >=Int 0
         andBool isAlphaC(LAST)
         andBool PREV ==Int 32

  claim [audit-long-last-nonalpha]:
    <k>
      #checkIfLastChar(
        str(seqConcat(PREFIX:IntSeq,
                      iCons(PREV:Int, iCons(LAST:Int, .IntSeq)))))
      => false
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires isLen(PREFIX) >=Int 0
         andBool notBool isAlphaC(LAST)

  claim [audit-long-prev-nonspace]:
    <k>
      #checkIfLastChar(
        str(seqConcat(PREFIX:IntSeq,
                      iCons(PREV:Int, iCons(LAST:Int, .IntSeq)))))
      => false
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires isLen(PREFIX) >=Int 0
         andBool isAlphaC(LAST)
         andBool PREV =/=Int 32
endmodule
