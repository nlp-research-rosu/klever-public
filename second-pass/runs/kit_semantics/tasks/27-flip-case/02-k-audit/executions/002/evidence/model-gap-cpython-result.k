requires "verification.k"

module MODEL-GAP-CPYTHON-RESULT
  imports VERIFICATION

  // CPython maps U+00E9 to U+00C9, but the fixed ASCII-only model does not.
  claim [u00e9-would-be-u00c9]:
    <k>
      #loadAll(Module(
        FuncDef("flip_case", Params("string"),
          Return(Call(Attribute(Name("string"), "swapcase"), .Exprs))
      ))) ~> Call(Name("flip_case"), str(iCons(233, .IntSeq)))
      =>
      str(iCons(201, .IntSeq))
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
