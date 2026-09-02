requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // The real body is materially changed: an uppercase character contributes 0.
  // The unchanged expected result for "A" is 65, so this claim must fail.
  claim [digitSum-mutated-body]:
    <k>
      Call(
        Name("digitSum"),
        str(iCons(65, .IntSeq))
      )
      => digitSumIS(iCons(65, .IntSeq))
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(
        "digitSum" |-> closureVal(
          ("s", .ParamNames),
          Assign(Name("total"), Int(0))
          Assign(Name("char"), Str(""))
          For(
            Name("char"),
            Name("s"),
            If(
              Call(Attribute(Name("char"), "isupper"), .Exprs),
              AugAssign(Name("total"), "+", Int(0)) .Stmts,
              .Stmts
            ) .Stmts
          )
          Return(Name("total"))
          .Stmts,
          0
        ),
        parent(-1)
      )
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
