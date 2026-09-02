requires "verification-no-bridges.k"

module SIMPLIFY-SPEC-NO-BRIDGES
  imports SIMPLIFY-VERIFICATION-NO-BRIDGES

  claim
    <k> runSimplify(
          str(fractionCodes(A:Int, B:Int)),
          str(fractionCodes(C:Int, D:Int)))
      => pyMod(A *Int C, B *Int D) ==Int 0
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(
             vCons(str(numCodes(A)),
             vCons(str(numCodes(B)), .ValSeq)))
      1 |-> list(
             vCons(str(numCodes(C)),
             vCons(str(numCodes(D)), .ValSeq)))
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires A >Int 0 andBool B >Int 0
     andBool C >Int 0 andBool D >Int 0
endmodule
