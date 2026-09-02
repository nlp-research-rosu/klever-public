requires "verification.k"

module AUDIT-FALSE-RESULT
  imports VERIFICATION

  // Satisfiable input, deliberately false result: count_upper("A") is 1.
  claim [false-A-is-zero]:
    <k>
      Call(Name("count_upper"), str(strToCodes("A")))
      => 0
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "count_upper" |->
          closureVal(
            ("s", .ParamNames),
            Assign(Name("count"), Int(0))
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
