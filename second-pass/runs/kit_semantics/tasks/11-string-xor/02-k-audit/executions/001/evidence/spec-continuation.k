requires "verification.k"

module CONTINUATION-SPEC-BASE
  imports VERIFICATION-BASE

  claim [one-step-with-observable-suffix]:
    <k>
      #loop(
        zipObjS(iCons(48, .IntSeq), iCons(49, .IntSeq)),
        TupleExpr(Name("x"), Name("y")),
        If(
          Compare(Name("x"), CmpOp("==", Name("y"))),
          AugAssign(Name("result"), "+", Str("0")),
          AugAssign(Name("result"), "+", Str("1"))
        )
      )
      ~> Assign(Name("marker"), Str("M"))
      =>
      .K
    </k>
    <env> 1 </env>
    <scopes>
      1 |->
        ( scope(
            "a"      |-> str(iCons(48, .IntSeq))
            "b"      |-> str(iCons(49, .IntSeq))
            "result" |-> str(.IntSeq)
            "x"      |-> str(.IntSeq)
            "y"      |-> str(.IntSeq),
            parent(0)
          )
          =>
          scope(
            "a"      |-> str(iCons(48, .IntSeq))
            "b"      |-> str(iCons(49, .IntSeq))
            "result" |-> str(iCons(49, .IntSeq))
            "x"      |-> str(iCons(48, .IntSeq))
            "y"      |-> str(iCons(49, .IntSeq))
            "marker" |-> str(iCons(77, .IntSeq)),
            parent(0)
          )
        )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule

module CONTINUATION-SPEC-BRIDGE
  imports VERIFICATION

  claim [one-step-with-observable-suffix]:
    <k>
      #loop(
        zipObjS(iCons(48, .IntSeq), iCons(49, .IntSeq)),
        TupleExpr(Name("x"), Name("y")),
        If(
          Compare(Name("x"), CmpOp("==", Name("y"))),
          AugAssign(Name("result"), "+", Str("0")),
          AugAssign(Name("result"), "+", Str("1"))
        )
      )
      ~> Assign(Name("marker"), Str("M"))
      =>
      .K
    </k>
    <env> 1 </env>
    <scopes>
      1 |->
        ( scope(
            "a"      |-> str(iCons(48, .IntSeq))
            "b"      |-> str(iCons(49, .IntSeq))
            "result" |-> str(.IntSeq)
            "x"      |-> str(.IntSeq)
            "y"      |-> str(.IntSeq),
            parent(0)
          )
          =>
          scope(
            "a"      |-> str(iCons(48, .IntSeq))
            "b"      |-> str(iCons(49, .IntSeq))
            "result" |-> str(iCons(49, .IntSeq))
            "x"      |-> str(iCons(48, .IntSeq))
            "y"      |-> str(iCons(49, .IntSeq))
            "marker" |-> str(iCons(77, .IntSeq)),
            parent(0)
          )
        )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
