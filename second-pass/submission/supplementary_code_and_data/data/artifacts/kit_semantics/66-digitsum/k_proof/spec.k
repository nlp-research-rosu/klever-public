requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [digitSum-loop]:
    <k>
      #loop(
        str(CODES:IntSeq),
        Name("char"),
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
      ~> (Return(Name("total")) .Stmts)
      ~> #endcall
      => TOTAL:Int +Int digitSumIS(CODES)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      (
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
        1 |-> scope(
          "total" |-> TOTAL
          "s" |-> str(INPUT:IntSeq)
          "char" |-> CHAR:Val,
          parent(0)
        )
      )
      =>
      (
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
      )
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [digitSum-entry]:
    <k>
      Call(Name("digitSum"), str(CODES:IntSeq))
      => digitSumIS(CODES)
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
endmodule
