requires "verification.k"

module SPEC-FALSE-RESULT-AUDIT
  imports VERIFICATION

  // Fresh A5 mutation: the real program returns 2 for "abcde", not 3.
  claim [fresh-wrong-result]:
    <k>
      #loadAll(Module(
        FuncDef(
          "vowels_count",
          Params("s"),
          Assign(Name("count"), Int(0))
          Assign(Name("last"), Str(""))
          Assign(Name("char"), Str(""))
          For(
            Name("char"),
            Name("s"),
            AugAssign(
              Name("count"),
              "+",
              Compare(Name("char"), CmpOp("in", Str("aeiouAEIOU"))))
            Assign(Name("last"), Name("char"))
            .Stmts)
          AugAssign(
            Name("count"),
            "+",
            Compare(Name("last"), CmpOp("==", Str("y"))))
          AugAssign(
            Name("count"),
            "+",
            Compare(Name("last"), CmpOp("==", Str("Y"))))
          Return(Name("count"))
          .Stmts)
        .Stmts))
      ~> Call(Name("vowels_count"), (Str("abcde"), .Exprs))
      =>
      3
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      (0 |-> scope(
         "vowels_count" |-> closureVal(
           ("s", .ParamNames),
           Assign(Name("count"), Int(0))
           Assign(Name("last"), Str(""))
           Assign(Name("char"), Str(""))
           For(
             Name("char"),
             Name("s"),
             AugAssign(
               Name("count"),
               "+",
               Compare(Name("char"), CmpOp("in", Str("aeiouAEIOU"))))
             Assign(Name("last"), Name("char"))
             .Stmts)
           AugAssign(
             Name("count"),
             "+",
             Compare(Name("last"), CmpOp("==", Str("y"))))
           AugAssign(
             Name("count"),
             "+",
             Compare(Name("last"), CmpOp("==", Str("Y"))))
           Return(Name("count"))
           .Stmts,
           0),
         parent(-1))
       -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
