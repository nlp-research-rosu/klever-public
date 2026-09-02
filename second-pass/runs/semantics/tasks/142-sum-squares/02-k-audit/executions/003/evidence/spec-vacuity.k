requires "verification.k"

module SUM-SQUARES-SPEC-VACUITY
  imports SUM-SQUARES-VERIFICATION

  // Fresh auditor mutation of the main result: the real empty-list call
  // returns 0, but this deliberately false destination requires 1.
  claim [main-false-empty]:
    <k>
      Call(
        Name("sum_squares"),
        (list(intVals(.Ints)), .Exprs))
    =>
      1
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
