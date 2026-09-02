requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // The source body is materially changed to accumulate instead of restarting
  // at the current element. For [2, -5, 3] it returns -3, not the target -5.
  claim [mutated-body]:
    <k>
      Call(
        Name("minSubArraySum"),
        list(vCons(2, vCons(-5, vCons(3, .ValSeq)))))
      => -5
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(
              "minSubArraySum" |->
                closureVal(
                  "nums", .ParamNames,
                  Assign(Name("current"), Int(0))
                  Assign(
                    Name("minimum"),
                    Subscript(Name("nums"), Int(0)))
                  For(
                    Name("value"),
                    Name("nums"),
                    Assign(
                      Name("current"),
                      BinOp(
                        "+",
                        Name("current"),
                        Name("value")))
                    Assign(
                      Name("minimum"),
                      Call(
                        Name("min"),
                        Name("minimum"),
                        Name("current"))))
                  Return(Name("minimum"))
                  .Stmts,
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
