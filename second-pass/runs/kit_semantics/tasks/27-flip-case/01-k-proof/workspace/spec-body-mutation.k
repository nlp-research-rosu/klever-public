requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // Deliberately mutated body: identity cannot satisfy the swapcase result.
  claim [identity-body]:
    <k>
      #loadAll(Module(
        FuncDef("flip_case", Params("string"),
          Return(Name("string"))
      ))) ~> Call(Name("flip_case"), str(iCons(65, .IntSeq)))
      =>
      str(iCons(97, .IntSeq))
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0  |-> scope(
              "flip_case" |->
                closureVal(
                  ("string", .ParamNames),
                  Return(Name("string")) .Stmts,
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
