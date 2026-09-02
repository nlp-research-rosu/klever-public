requires "/tmp/audit-work/142-sum-squares-audit/spec.k"

module SUM-SQUARES-SPEC-VACUITY
  imports SUM-SQUARES-SPEC

  // Fresh reviewer mutation: the actual result is required to be one larger
  // than the recursively defined contract result.  The empty-list witness
  // satisfies the entry pattern and returns 0, while this destination is 1.
  claim [false-main]:
    <k>
      Call(
        Name("sum_squares"),
        (list(intVals(IS:Ints)), .Exprs))
    =>
      sumSquares(IS, 0, 0) +Int 1
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
