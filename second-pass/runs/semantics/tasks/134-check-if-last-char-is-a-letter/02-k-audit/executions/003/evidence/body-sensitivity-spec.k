requires "verification-body-mut.k"

module BODY-SENSITIVITY-SPEC
  imports VERIFICATION-BODY-MUT

  // The original long-true obligation is false for the mutated body.
  // Satisfying witness: PREFIX=.IntSeq, PREV=32, LAST=97, i.e. " a".
  claim
    <k>
      #checkIfLastCharMut(
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
