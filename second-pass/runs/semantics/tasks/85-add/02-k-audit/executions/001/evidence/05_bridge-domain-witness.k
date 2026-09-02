requires "verification.k"

module BRIDGE-DOMAIN-WITNESS
  imports VERIFICATION

  // Concrete false fixed-semantics transition admitted by the candidate bridge.
  // The non-empty integer input [4,2] is in the intended domain. With no caller
  // frame, fixed execution performs the loop, changes the locals, and later
  // sticks at #pop. The candidate bridge can instead reach this target in one
  // step while retaining all initial locals.
  claim [overbroad-empty-stack-transition]:
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
