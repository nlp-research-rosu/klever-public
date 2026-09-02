requires "verification.k"

module SPEC-EMPTY
  imports VERIFICATION
  claim
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
endmodule

module SPEC-ONE-ALPHA
  imports VERIFICATION
  claim
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
endmodule

module SPEC-ONE-NONALPHA
  imports VERIFICATION
  claim
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
endmodule

module SPEC-LONG-TRUE
  imports VERIFICATION
  claim
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
endmodule

module SPEC-LONG-LAST-NONALPHA
  imports VERIFICATION
  claim
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
endmodule

module SPEC-LONG-PREV-NOT-SPACE
  imports VERIFICATION
  claim
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
