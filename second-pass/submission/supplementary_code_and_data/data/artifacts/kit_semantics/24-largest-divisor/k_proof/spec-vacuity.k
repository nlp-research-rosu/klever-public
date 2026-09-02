requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: largest_divisor(15) is 5, not 6.
  claim [false-result]:
    <k> Call(Name("largest_divisor"), Int(15)) => 6 </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(
        "largest_divisor" |->
          closureVal(
            "n",
            Assign(
              Name("divisor"),
              BinOp("-", Name("n"), Int(1)))
            While(
              Compare(
                BinOp("%", Name("n"), Name("divisor")),
                CmpOp("!=", Int(0))),
              Assign(
                Name("divisor"),
                BinOp("-", Name("divisor"), Int(1))) .Stmts)
            Return(Name("divisor")) .Stmts,
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
