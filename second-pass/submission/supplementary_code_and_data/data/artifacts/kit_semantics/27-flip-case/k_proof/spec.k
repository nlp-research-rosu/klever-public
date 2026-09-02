requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [flip-case]:
    <k>
      #loadAll(Module(
        FuncDef("flip_case", Params("string"),
          Return(Call(Attribute(Name("string"), "swapcase"), .Exprs))
      ))) ~> Call(Name("flip_case"), str(CS:IntSeq))
      =>
      str(mapSwap(CS))
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0  |-> scope(
              "flip_case" |->
                closureVal(
                  ("string", .ParamNames),
                  Return(Call(Attribute(Name("string"), "swapcase"), .Exprs)) .Stmts,
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
