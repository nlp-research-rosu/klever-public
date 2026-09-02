requires "verification.k"

module AUDIT-SPEC-VACUITY
  imports VERIFICATION

  // Fresh reviewer mutation. The actual result for ("ababa", "aba") is 2.
  // This deliberately false result-constraining target demands 3.
  claim [false-shifted-overlap]:
    <k>
      Call(
        Name("how_many_times"),
        Str("ababa"),
        Str("aba"))
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
