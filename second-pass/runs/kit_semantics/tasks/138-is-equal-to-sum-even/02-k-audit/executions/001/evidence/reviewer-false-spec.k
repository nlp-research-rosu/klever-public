requires "verification.k"

module REVIEWER-FALSE-SPEC
  imports VERIFICATION

  // Fresh audit mutation: the real body returns true at the satisfying input 8,
  // but this destination deliberately requires false.
  claim [false-result-at-eight]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "is_equal_to_sum_even",
            Params("n"),
            Return(
              BoolOp(
                "and",
                Compare(Name("n"), CmpOp(">=", Int(8))),
                Compare(
                  BinOp("%", Name("n"), Int(2)),
                  CmpOp("==", Int(0))
                )
              )
            )
          )
        )
      )
      ~> Call(Name("is_equal_to_sum_even"), Int(8))
      => false
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      (0 |-> scope(
              "is_equal_to_sum_even"
                |-> closureVal(
                      "n",
                      Return(
                        BoolOp(
                          "and",
                          Compare(Name("n"), CmpOp(">=", Int(8))),
                          Compare(
                            BinOp("%", Name("n"), Int(2)),
                            CmpOp("==", Int(0))
                          )
                        )
                      )
                      .Stmts,
                      0
                    ),
              parent(-1)
            )
       -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
