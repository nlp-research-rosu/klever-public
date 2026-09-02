requires "verification-no-bridge.k"

module BRIDGE-DOMAIN-WITNESS-NO-BRIDGE
  imports VERIFICATION-NO-BRIDGE

  claim [fixed-semantics-rejects-transition]:
    <k>
      #loop(
        list(intVals(iCons(4, iCons(2, .IntSeq)))),
        Name("value"),
        addLoopBody)
      ~> (Return(Name("total")) .Stmts):Stmts
      ~> #endcall
      =>
      Return(addAccSpec(iCons(4, iCons(2, .IntSeq)), false, 0))
      ~> #endcall
    </k>
    <env> 1 </env>
    <scopes>
      (1 |-> scope(
        ("lst" |-> list(intVals(iCons(4, iCons(2, .IntSeq)))))
        ("total" |-> 0)
        ("odd_index" |-> false)
        ("value" |-> 0),
        parent(0)))
      (0 |-> scope(.Map, parent(-1)))
      (-1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
