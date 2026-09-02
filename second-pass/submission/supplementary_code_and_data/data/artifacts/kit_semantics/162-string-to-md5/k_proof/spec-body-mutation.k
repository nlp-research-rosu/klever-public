requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // Deliberately false: the mutated second return yields None for "a".
  claim [reject-mutated-body]:
    <k>
      #loadAll(Module(
        Import("hashlib")
        FuncDef("string_to_md5", Params("text"),
          If(Compare(Name("text"), CmpOp("==", Str(""))),
            Return(NoneVal),
            .Stmts)
          Return(NoneVal))
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
              Return(NoneVal),
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
