requires "verification.k"

module REVIEWER-BODY-MUTATION
  imports VERIFICATION

  // The claim-executed closure body is materially changed from 18 to 19.
  // At n=3 that body returns 190, so the original correct target 180 must fail.
  claim [fresh-executed-body-mutation]:
    <k>
      Call(Name("starts_one_ends"), 3)
      =>
      180
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
                  Int(19),
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
