requires "/tmp/audit-work/27-flip-case/candidate/reference-semantics/semantics.k"

module DIRECT-PINNING
  imports MPY

  // The constructor tree is copied directly from the byte-validated
  // solution.mpy, with its empty Exprs made explicit.
  claim
    <k>
      #loadAll(
        Module(
          FuncDef(
            "flip_case",
            Params("string"),
            Return(Call(Attribute(Name("string"), "swapcase"), .Exprs)))))
      ~> Call(Name("flip_case"), str(S:IntSeq))
      =>
      str(mapSwap(S))
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
                     Return(
                       Call(
                         Attribute(Name("string"), "swapcase"),
                         .Exprs))
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
