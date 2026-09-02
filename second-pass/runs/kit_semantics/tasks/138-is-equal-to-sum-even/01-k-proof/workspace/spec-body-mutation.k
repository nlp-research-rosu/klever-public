requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // The body is materially changed to return False; the original N = 8
  // postcondition must therefore be rejected.
  claim [mutated-body]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "is_equal_to_sum_even",
            Params("n"),
            Return(Bool(false))
          )
        )
      )
      ~> Call(Name("is_equal_to_sum_even"), Int(N))
      => true
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
                      Return(Bool(false)) .Stmts,
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
    requires N ==Int 8
endmodule
