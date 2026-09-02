requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false for the realizable empty-list input: the real result is
  // 0, while this claim demands 1.
  claim [false-result]:
    <k>
      #loadAll(
        Module(
          Import("math")
          FuncDef(
            "sum_squares",
            Params("lst"),
            Assign(Name("total"), Int(0))
            Assign(Name("number"), Int(0))
            Assign(Name("rounded"), Int(0))
            For(
              Name("number"),
              Name("lst"),
              Assign(
                Name("rounded"),
                Call(Attribute(Name("math"), "ceil"), Name("number")))
              AugAssign(
                Name("total"),
                "+",
                BinOp("*", Name("rounded"), Name("rounded"))))
            Return(Name("total")))))
      ~> Call(Name("sum_squares"), list(.ValSeq))
      => 1
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      (0 |-> scope(
         "sum_squares" |->
           closureVal(
             ("lst", .ParamNames),
             Assign(Name("total"), Int(0))
             Assign(Name("number"), Int(0))
             Assign(Name("rounded"), Int(0))
             For(
               Name("number"),
               Name("lst"),
               Assign(
                 Name("rounded"),
                 Call(Attribute(Name("math"), "ceil"), Name("number")))
               AugAssign(
                 Name("total"),
                 "+",
                 BinOp("*", Name("rounded"), Name("rounded"))))
             Return(Name("total"))
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
