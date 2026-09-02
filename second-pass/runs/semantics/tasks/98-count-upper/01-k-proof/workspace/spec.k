requires "verification.k"

module COUNT-UPPER-SPEC
  imports COUNT-UPPER-VERIFICATION

  // Loop invariant.  ACC is the number already seen and countUpperFrom is the
  // contribution of the unconsumed suffix.  The remaining local bindings are
  // existential in the post-state because the function returns only count.
  claim
    <k>
      #loop(
        str(S:IntSeq),
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
    <env> L:Int </env>
    <scopes>
      SC:Map
      L |-> scope(
        "s" |-> INPUT:Val
        "count" |-> (ACC:Int => ACC +Int countUpperFrom(S, EVEN))
        "even" |-> (EVEN:Bool => ?FINAL_EVEN:Bool)
        "ch" |-> (OLD_CH:Val => ?FINAL_CH:Val),
        P:Parent)
    </scopes>

  // End-to-end claim: load the exact translated definition, call it with an
  // arbitrary semantic string, and obtain the mathematical result.
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
      ~> Call(Name("count_upper"), str(S:IntSeq))
      => countUpperFrom(S, true)
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
