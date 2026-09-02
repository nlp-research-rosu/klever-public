requires "baseline-verification.k"

module LEMMA-LEN-CONNECTION
  imports BASELINE-VERIFICATION
  claim
    <k>
      isLen(seqConcat(P:IntSeq, iCons(A:Int, iCons(B:Int, .IntSeq))))
      =>
      isLen(P) +Int 2
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
endmodule

module LEMMA-AT-FIRST-CONNECTION
  imports BASELINE-VERIFICATION
  claim
    <k>
      intSeqAt(
        seqConcat(P:IntSeq, iCons(A:Int, iCons(B:Int, .IntSeq))),
        isLen(P))
      =>
      A
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
endmodule

module LEMMA-AT-SECOND-CONNECTION
  imports BASELINE-VERIFICATION
  claim
    <k>
      intSeqAt(
        seqConcat(P:IntSeq, iCons(A:Int, iCons(B:Int, .IntSeq))),
        isLen(P) +Int 1)
      =>
      B
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
endmodule
