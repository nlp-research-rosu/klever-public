requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // Deliberately mutated body: returning 0 must not establish the original
  // max_element([1]) result.
  claim [mutated-body]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "max_element",
            Params("l"),
            Return(Int(0))
          )
        )
      )
      ~> Call(
           Name("max_element"),
           list(vCons(1, .ValSeq))
         )
      => 1
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        .Map
        =>
        "max_element" |->
          closureVal(
            ("l", .ParamNames),
            (Return(Int(0)) .Stmts),
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
