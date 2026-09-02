requires "verification.k"

module AUDIT-GROUND-WITNESSES
  imports COUNT-UPPER-VERIFICATION

  // A fully concrete state satisfying the loop claim's precondition.
  // The initial count 7 becomes 8 because "aBCdEf" contributes one.
  claim
    <k>
      #loop(
        str(strToCodes("aBCdEf")),
        Name("ch"),
        AugAssign(
          Name("count"),
          "+",
          BoolOp(
            "and",
            Name("even"),
            Compare(Name("ch"), CmpOp("in", Str("AEIOU")))))
        Assign(Name("even"), UnaryOp("not", Name("even")))
        .Stmts)
      => .K
      ...
    </k>
    <env> 1 </env>
    <scopes>
      1 |-> scope(
        "s" |-> str(strToCodes("aBCdEf"))
        "count" |-> (7 => 8)
        "even" |-> (true => true)
        "ch" |-> (str(.IntSeq) => str(strToCodes("f"))),
        parent(0))
    </scopes>

  // A fully concrete state satisfying the end-to-end claim's precondition.
  claim
    <k>
      #loadAll(
        Module(
          FuncDef(
            "count_upper",
            Params("s"),
            Assign(Name("count"), Int(0))
            Assign(Name("even"), Bool(true))
            Assign(Name("ch"), Str(""))
            For(
              Name("ch"),
              Name("s"),
              AugAssign(
                Name("count"),
                "+",
                BoolOp(
                  "and",
                  Name("even"),
                  Compare(Name("ch"), CmpOp("in", Str("AEIOU")))))
              Assign(Name("even"), UnaryOp("not", Name("even")))
              .Stmts)
            Return(Name("count"))
            .Stmts)
          .Stmts))
      ~> Call(Name("count_upper"), str(strToCodes("aBCdEf")))
      => 1
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0 |-> scope(
        "count_upper" |->
          closureVal(
            ("s", .ParamNames),
            Assign(Name("count"), Int(0))
            Assign(Name("even"), Bool(true))
            Assign(Name("ch"), Str(""))
            For(
              Name("ch"),
              Name("s"),
              AugAssign(
                Name("count"),
                "+",
                BoolOp(
                  "and",
                  Name("even"),
                  Compare(Name("ch"), CmpOp("in", Str("AEIOU")))))
              Assign(Name("even"), UnaryOp("not", Name("even")))
              .Stmts)
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
