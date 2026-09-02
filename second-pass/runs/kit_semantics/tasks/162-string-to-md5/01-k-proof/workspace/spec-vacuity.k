requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: the real empty-input branch returns noneV, not 0.
  claim [false-empty-result]:
    <k>
      #loadAll(Module(
        Import("hashlib")
        FuncDef("string_to_md5", Params("text"),
          If(Compare(Name("text"), CmpOp("==", Str(""))),
            Return(NoneVal),
            .Stmts)
          Return(
            Call(
              Attribute(
                Call(
                  Attribute(Name("hashlib"), "md5"),
                  Call(Attribute(Name("text"), "encode"), Str("utf-8"))),
                "hexdigest"),
              .Exprs)))
        Assign(
          Name("result"),
          Call(Name("string_to_md5"), str(.IntSeq)))
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
              Return(
                Call(
                  Attribute(
                    Call(
                      Attribute(Name("hashlib"), "md5"),
                      Call(Attribute(Name("text"), "encode"), Str("utf-8"))),
                    "hexdigest"),
                  .Exprs)),
              0)
          "result" |-> 0,
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
