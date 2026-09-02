requires "verification-base.k"

module SPEC-REPRESENTATION-CONNECTION
  imports VERIFICATION-BASE

  claim
    <k> .K </k>
    <env> 0 </env>
    <scopes> .Map </scopes>
    <scopeLoc> 0 </scopeLoc>
    <heap>
      0 |-> list(
        vCons(2, snocVS(intsVS(iCons(4, iCons(3, .IntSeq))), 5)))
      =>
      0 |-> list(vCons(2, vCons(4, vCons(3, vCons(5, .ValSeq)))))
    </heap>
    <heapLoc> 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
