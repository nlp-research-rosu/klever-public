requires "verification-base.k"

module SPEC-CONNECTION-GROUND
  imports VERIFICATION-BASE

  claim
    <k>
      Subscript(
        list(vCons(2, snocVS(intsVS(iCons(4, iCons(3, .IntSeq))), 5))),
        UnaryOp("-", Int(1)))
      => 5
    </k>
    <env> 0 </env>
    <scopes> .Map </scopes>
    <scopeLoc> 0 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
