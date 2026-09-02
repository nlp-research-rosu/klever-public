requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false for the satisfiable singleton input [5].
  claim [false-result]:
    <k>
      Call(
        Name("minSubArraySum"),
        list(vCons(5, .ValSeq)))
      => 6
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
