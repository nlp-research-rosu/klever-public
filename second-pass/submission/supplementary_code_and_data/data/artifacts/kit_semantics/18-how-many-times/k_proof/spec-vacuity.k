requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: the real result for ("aaaa", "aa") is 3, not 4.
  claim [false-result]:
    <k>
      Call(Name("how_many_times"), Str("aaaa"), Str("aa"))
      => 4
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
                Subscript(Name("string"), Slice(Int(1), NoBound, NoBound))))
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
