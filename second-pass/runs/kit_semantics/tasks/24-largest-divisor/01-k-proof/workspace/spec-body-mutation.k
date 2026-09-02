requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // Deliberately mutated return expression: the real body returns divisor,
  // while this body returns divisor - 1.  The original result must not prove.
  claim [mutated-body]:
    <k> Call(Name("largest_divisor"), Int(15)) => 5 </k>
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
            Return(
              BinOp("-", Name("divisor"), Int(1))) .Stmts,
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
