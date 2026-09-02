requires "verification.k"

module SUM-SQUARES-BRIDGE-GROUND-SPEC
  imports SUM-SQUARES-VERIFICATION

  // Context preservation for a proof-local iterator step.
  claim [abstract-step-context]:
    <k>
      #iterNext(list(intVals(intCons(7, .Ints))))
      ~> Int(99)
    =>
      #iterYield(7, list(intVals(.Ints)))
      ~> Int(99)
    </k>

  // The corresponding fixed-representation iterator step.
  claim [concrete-step-context]:
    <k>
      #iterNext(list(vCons(7, .ValSeq)))
      ~> Int(99)
    =>
      #iterYield(7, list(.ValSeq))
      ~> Int(99)
    </k>

  claim [abstract-program-123]:
    <k>
      Call(
        Name("sum_squares"),
        (list(intVals(intCons(1, intCons(2, intCons(3, .Ints))))), .Exprs))
    =>
      6
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0  |-> scope(
        "sum_squares" |->
          closureVal(
            ("lst", .ParamNames),
            sumSquaresFunctionBody,
            0),
        parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [concrete-program-123]:
    <k>
      Call(
        Name("sum_squares"),
        (list(vCons(1, vCons(2, vCons(3, .ValSeq)))), .Exprs))
    =>
      6
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0  |-> scope(
        "sum_squares" |->
          closureVal(
            ("lst", .ParamNames),
            sumSquaresFunctionBody,
            0),
        parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
