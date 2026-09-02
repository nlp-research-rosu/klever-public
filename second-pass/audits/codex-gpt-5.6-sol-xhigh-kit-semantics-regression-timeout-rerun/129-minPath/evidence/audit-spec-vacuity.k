requires "verification.k"

module AUDIT-SPEC-VACUITY
  imports VERIFICATION

  // Fresh reviewer mutation: the last cell is deliberately changed from 1 to 2.
  claim [false-ground-result]:
    <k>
      #loadAll(Module(
        MinPathDefinition
        Assert(Compare(
          Call(Name("minPath"),
            ListExpr(
              ListExpr(Int(4), Int(3)),
              ListExpr(Int(2), Int(1))),
            Int(5)),
          CmpOp("==",
            ListExpr(Int(1), Int(2), Int(1), Int(2), Int(2)))))
      )) => .K
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope) => ?SCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?HEAP:Map </heap>
    <heapLoc> 0 => ?HEAPLOC:Int </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
