requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // The first comparison's return is deliberately mutated from a to b.
  // The expected result for (2, 1) remains 2, so this claim must fail.
  claim [changed-body]:
    <k>
      #loadAll(Module(
        FuncDef("compare_one", Params("a", "b"),
          If(Call(Name("isinstance"), Name("a"), Name("str")),
            Assign(Name("a_value"),
              Call(Name("float"),
                Call(Attribute(Name("a"), "replace"), Str(","), Str(".")))) .Stmts,
            Assign(Name("a_value"), Name("a")) .Stmts)
          If(Call(Name("isinstance"), Name("b"), Name("str")),
            Assign(Name("b_value"),
              Call(Name("float"),
                Call(Attribute(Name("b"), "replace"), Str(","), Str(".")))) .Stmts,
            Assign(Name("b_value"), Name("b")) .Stmts)
          If(Compare(Name("a_value"), CmpOp(">", Name("b_value"))),
            Return(Name("b")) .Stmts, .Stmts)
          If(Compare(Name("b_value"), CmpOp(">", Name("a_value"))),
            Return(Name("b")) .Stmts, .Stmts)
          Return(NoneVal) .Stmts))) ~>
      Call(Name("compare_one"), 2, 1)
      => 2
    </k>
    <env> 0 </env>
    <scopes> 0 |-> scope(.Map, parent(-1))
              -1 |-> builtinsScope => ?FINAL:Map </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
