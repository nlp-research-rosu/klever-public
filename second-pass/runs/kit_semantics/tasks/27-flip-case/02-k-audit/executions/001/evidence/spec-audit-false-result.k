requires "verification.k"

module SPEC-AUDIT-FALSE-RESULT
  imports VERIFICATION

  // Fresh reviewer non-vacuity mutation: swapcase("A") is "a" (97), not "b" (98).
  claim [audit-wrong-result]:
    <k>
      #loadAll(Module(
        FuncDef("flip_case", Params("string"),
          Return(Call(Attribute(Name("string"), "swapcase"), .Exprs))
      ))) ~> Call(Name("flip_case"), str(iCons(65, .IntSeq)))
      =>
      str(iCons(98, .IntSeq))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0 |-> scope(
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
