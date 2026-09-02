requires "verification.k"

module AUDIT-FALSE-RESULT
  imports VERIFICATION

  // Reviewer-authored mutation. The satisfying input [3, -4, 2] returns -4;
  // this deliberately changes only the result obligation to the false value -3.
  claim [fresh-off-by-one]:
    <k>
      Call(
        Name("minSubArraySum"),
        list(vCons(3, vCons(-4, vCons(2, .ValSeq)))))
      => -3
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
                      Call(
                        Name("min"),
                        Name("value"),
                        BinOp(
                          "+",
                          Name("current"),
                          Name("value"))))
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
