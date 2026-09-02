requires "spec.k"

module SPEC-VACUITY
  imports SPEC

  // Deliberately false on the realizable input CODES == .IntSeq.
  claim [digitSum-entry-off-by-one]:
    <k>
      Call(Name("digitSum"), str(CODES:IntSeq))
      => digitSumIS(CODES) +Int 1
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
              AugAssign(
                Name("total"),
                "+",
                Call(Name("ord"), Name("char"), .Exprs)
              ) .Stmts,
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
    requires CODES ==K .IntSeq
endmodule
