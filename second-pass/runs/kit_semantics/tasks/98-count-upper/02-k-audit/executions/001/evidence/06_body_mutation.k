requires "verification.k"

module AUDIT-BODY-MUTATION
  imports VERIFICATION

  // The executed closure is materially changed to count = 1. The original
  // empty-input obligation 0 must therefore be rejected.
  claim [mutated-initial-count]:
    <k>
      Call(Name("count_upper"), str(.IntSeq))
      => 0
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "count_upper" |->
          closureVal(
            ("s", .ParamNames),
            Assign(Name("count"), Int(1))
            Assign(Name("remaining"), Name("s"))
            While(
              Name("remaining"),
              AugAssign(
                Name("count"),
                "+",
                Compare(
                  Subscript(Name("remaining"), Int(0)),
                  CmpOp("in", Str("AEIOU"))))
              Assign(
                Name("remaining"),
                Subscript(
                  Name("remaining"),
                  Slice(Int(2), NoBound, NoBound))))
            Return(Name("count"))
            .Stmts,
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
