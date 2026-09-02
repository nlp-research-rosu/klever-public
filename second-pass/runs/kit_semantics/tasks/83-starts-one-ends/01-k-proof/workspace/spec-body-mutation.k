requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // Expected to fail: the program body uses 17 instead of 18, while the
  // claimed result remains the correct n=2 result.
  claim [changed-body-is-detected]:
    <k>
      Call(Name("starts_one_ends"), 2)
      =>
      18
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "starts_one_ends" |->
          closureVal(
            "n",
            Return(
              IfExp(
                Compare(Name("n"), CmpOp("==", Int(1))),
                Int(1),
                BinOp(
                  "*",
                  Int(17),
                  BinOp("**", Int(10), BinOp("-", Name("n"), Int(2)))
                )
              )
            ),
            0
          ),
        parent(-1)
      )
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
