requires "verification-body-mutated.k"

module BODY-SENSITIVITY-SPEC
  imports VERIFICATION

  // "1/5" * "5/1" is exactly 1.  The mutated simplifyBody executes a
  // For with .Stmts instead of simplifyLoopBody, so it cannot return true.
  claim [mutated-executed-body]:
    <k>
      #applyK(
        toCall(closureVal(("x", "n"), simplifyBody, 0)),
        (str(iCons(49, iCons(47, iCons(53, .IntSeq)))),
         str(iCons(53, iCons(47, iCons(49, .IntSeq)))),
         .Vals))
      =>
      true
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
endmodule
