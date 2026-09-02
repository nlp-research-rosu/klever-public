requires "verification.k"

module AUDIT-SPEC-BODY-SLICE-MUTATION
  imports VERIFICATION

  // The actual executed closure body is changed from string[1:] to string[2:].
  // On ("aaaa", "aa") this changed body returns 2, so the original result 3
  // must be rejected.
  claim [changed-slice-body]:
    <k>
      Call(Name("how_many_times"), Str("aaaa"), Str("aa"))
      => 3
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "how_many_times" |->
          closureVal(
            ("string", "substring"),
            If(
              Compare(Name("substring"), CmpOp("==", Str(""))),
              Return(BinOp("+", Call(Name("len"), Name("string")), Int(1))),
              .Stmts)
            Assign(Name("count"), Int(0))
            While(
              Compare(Name("string"), CmpOp("!=", Str(""))),
              If(
                Call(Attribute(Name("string"), "startswith"), Name("substring")),
                AugAssign(Name("count"), "+", Int(1)),
                .Stmts)
              Assign(
                Name("string"),
                Subscript(Name("string"), Slice(Int(2), NoBound, NoBound))))
            Return(Name("count")),
            0),
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
