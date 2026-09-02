requires "verification.k"

module AUDIT-GROUND
  imports VERIFICATION

  claim [ground-empty]:
    <k> Call(Name("count_upper"), str(.IntSeq)) => 0 </k>
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

  claim [ground-example]:
    <k>
      Call(Name("count_upper"), str(strToCodes("aBCdEf")))
      => 1
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

  claim [ground-three]:
    <k>
      Call(Name("count_upper"), str(strToCodes("AEIOU")))
      => 3
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
