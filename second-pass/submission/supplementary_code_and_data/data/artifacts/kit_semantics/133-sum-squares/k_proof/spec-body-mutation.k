requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // The implementation is materially mutated to add the ceiling instead of
  // its square.  On [2] it returns 2, so the correct result claim (4) fails.
  claim [changed-loop-update]:
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
                Name("rounded")))
            Return(Name("total")))))
      ~> Call(
           Name("sum_squares"),
           list(vCons(2, .ValSeq)))
      => 4
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
                 Name("rounded")))
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
