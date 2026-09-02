requires "reference-semantics/semantics.k"

module SAME-CHARS-ACTUAL-PROGRAM-CONNECTION
  imports MPY

  // Bridge-free connection: load the exact submitted solution.mpy AST, then
  // resolve and call the function through the module binding.
  claim
    <k>
      #loadAll(
        Module(
          FuncDef(
            "same_chars",
            Params("s0", "s1"),
            Return(
              Compare(
                Call(Name("set"), (Name("s0"), .Exprs)),
                CmpOp("==",
                  Call(Name("set"), (Name("s1"), .Exprs)))))
            .Stmts)
          .Stmts))
      ~> Call(Name("same_chars"), (str(S0:IntSeq), str(S1:IntSeq), .Exprs))
      =>
      sameSet(dedupCodes(S0), dedupCodes(S1))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        .Map [
          "same_chars" <-
            closureVal(
              ("s0", "s1", .ParamNames),
              (Return(
                Compare(
                  Call(Name("set"), (Name("s0"), .Exprs)),
                  CmpOp("==",
                    Call(Name("set"), (Name("s1"), .Exprs)))))
               .Stmts),
              0)
        ],
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
