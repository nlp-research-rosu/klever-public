requires "verification.k"

module AUDIT-BODY-MUTATION
  imports VERIFICATION

  // Operational-sensitivity check: this changes the actual FuncDef body
  // executed by the claim to `return True`, while retaining the empty-input
  // result obligation `false`.  A body-insensitive theorem would close.
  claim [changed-body-does-not-return-false]:
    <k>
      #loadAll(Module(
        FuncDef(
          "check_dict_case",
          Params("dict"),
          Return(Bool(true)) .Stmts)
        Assign(
          Name("result"),
          Call(
            Name("check_dict_case"),
            dictV(.ValSeq, .ValSeq)))))
      =>
      .K
    </k>
    <env> 0 </env>
    <scopes>
      ( 0 |-> scope(.Map, parent(-1))
        -1 |-> builtinsScope)
      =>
      ( 0 |-> scope(
          "check_dict_case" |->
            closureVal(
              ("dict", .ParamNames),
              Return(Bool(true)) .Stmts,
              0)
          "result" |-> false,
          parent(-1))
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
