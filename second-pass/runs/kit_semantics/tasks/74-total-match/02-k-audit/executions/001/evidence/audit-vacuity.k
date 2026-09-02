requires "verification.k"

module AUDIT-VACUITY
  imports VERIFICATION

  // Fresh auditor mutation. Both inputs have total length 1, so the actual
  // function returns the first list ["a"]. The result obligation is
  // deliberately changed to the second, distinct list ["b"].
  claim [wrong-equality-result]:
    <k>
      #loadAll(Module(
        FuncDef("_total_length", Params("strings"),
          Assign(Name("total"), Int(0))
          Assign(Name("string"), NoneVal)
          For(Name("string"), Name("strings"),
            AugAssign(Name("total"), "+", Call(Name("len"), Name("string"))))
          Return(Name("total")))
        FuncDef("total_match", Params("lst1", "lst2"),
          If(Compare(
            Call(Name("_total_length"), Name("lst1")),
            CmpOp("<=", Call(Name("_total_length"), Name("lst2")))),
            Return(Name("lst1")),
            .Stmts)
          Return(Name("lst2")))
      ))
      ~> Call(
        Name("total_match"),
        list(vCons(str(iCons(97, .IntSeq)), .ValSeq)),
        list(vCons(str(iCons(98, .IntSeq)), .ValSeq))
      )
      => list(vCons(str(iCons(98, .IntSeq)), .ValSeq))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0 |-> scope(
        "_total_length" |-> closureVal(
          ("strings", .ParamNames),
          Assign(Name("total"), Int(0))
          Assign(Name("string"), NoneVal)
          For(Name("string"), Name("strings"),
            AugAssign(Name("total"), "+", Call(Name("len"), Name("string"))))
          Return(Name("total")),
          0
        )
        "total_match" |-> closureVal(
          ("lst1", "lst2", .ParamNames),
          If(Compare(
            Call(Name("_total_length"), Name("lst1")),
            CmpOp("<=", Call(Name("_total_length"), Name("lst2")))),
            Return(Name("lst1")),
            .Stmts)
          Return(Name("lst2")),
          0
        ),
        parent(-1)
      )
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
