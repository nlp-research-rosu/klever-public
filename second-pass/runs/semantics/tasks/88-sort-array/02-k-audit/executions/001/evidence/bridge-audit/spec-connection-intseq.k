requires "verification-base.k"

module SPEC-CONNECTION-INTSEQ
  imports VERIFICATION-BASE

  claim
    <k>
      Subscript(
        list(vCons(F:Int, snocVS(intsVS(IS:IntSeq), L:Int))),
        UnaryOp("-", Int(1)))
      => L
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
