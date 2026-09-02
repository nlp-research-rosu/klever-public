requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // Deliberately mutated body: returning arr removes both sorted() calls.
  // The original target postcondition must therefore be rejected.
  claim [return-input-mutant]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "sort_array",
            Params("arr", .ParamNames),
            Return(Name("arr"))
            .Stmts)))
      ~> Call(Name("sort_array"), ref(0), .Exprs)
      =>
      ref(2)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      ?SCOPES:Map
    </scopes>
    <scopeLoc> 1 => ?SCOPELOC:Int </scopeLoc>
    <heap>
      0 |-> list(vCons(3, vCons(4, .ValSeq)))
      =>
      ?HEAP:Map
    </heap>
    <heapLoc> 1 => ?HEAPLOC:Int </heapLoc>
    <stack> .List => ?STACK:List </stack>
    <ret> noRet => ?RET:RetState </ret>
    <exc> NoExc => ?EXC:Exc </exc>
    <exit-code> 0 => ?EXIT:Int </exit-code>
endmodule
