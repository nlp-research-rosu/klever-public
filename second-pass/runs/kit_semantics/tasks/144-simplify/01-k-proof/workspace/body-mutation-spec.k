requires "verification.k"

module BODY-MUTATION-SPEC
  imports VERIFICATION-BASE

  claim [empty-loop-body-must-fail]:
    <k>
      #loop(str(iCons(49, .IntSeq)), Name("ch"), .Stmts)
      ~> (simplifyReturn .Stmts)
      ~> #endcall
      =>
      true
    </k>
    <env> 1 => 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       1 |-> simplifyScope(
         str(iCons(49, iCons(47, iCons(49, .IntSeq)))),
         str(iCons(49, iCons(47, iCons(49, .IntSeq)))),
         3,
         1,
         1,
         1,
         0,
         str(.IntSeq))
       -1 |-> builtinsScope)
      =>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack>
      ListItem(frame(.K, 0, 1))
      =>
      .List
    </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
endmodule
