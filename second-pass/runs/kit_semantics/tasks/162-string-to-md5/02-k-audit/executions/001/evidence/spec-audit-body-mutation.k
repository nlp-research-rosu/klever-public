requires "verification.k"

module SPEC-AUDIT-BODY-MUTATION
  imports VERIFICATION

  // Reviewer body-sensitivity probe: the executed nonempty return is changed
  // to "wrong", while the realizable input "a" retains the original result
  // obligation. A body-insensitive theorem would incorrectly close this.
  claim [reject-wrong-body]:
    <k>
      #loadAll(Module(
        Import("hashlib")
        FuncDef("string_to_md5", Params("text"),
          If(Compare(Name("text"), CmpOp("==", Str(""))),
            Return(NoneVal),
            .Stmts)
          Return(Str("wrong")))
        Assign(
          Name("result"),
          Call(
            Name("string_to_md5"),
            str(iCons(97, .IntSeq))))
      )) => .K
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        .Map =>
          "string_to_md5" |->
            closureVal(
              "text",
              If(Compare(Name("text"), CmpOp("==", Str(""))),
                Return(NoneVal),
                .Stmts)
              Return(Str("wrong")),
              0)
          "result" |->
            str(md5hexCodes(iCons(97, .IntSeq))),
        parent(-1))
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
