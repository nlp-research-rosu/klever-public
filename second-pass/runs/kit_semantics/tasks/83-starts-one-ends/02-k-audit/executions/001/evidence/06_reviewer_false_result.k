requires "verification.k"

module REVIEWER-FALSE-RESULT
  imports VERIFICATION

  // Reviewer-authored fresh mutation: n=3 satisfies the multi-digit domain.
  // The real body returns 180, so the result-constraining target 181 is false.
  claim [fresh-false-result-at-three]:
    <k>
      Call(Name("starts_one_ends"), 3)
      =>
      181
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
                  Int(18),
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
