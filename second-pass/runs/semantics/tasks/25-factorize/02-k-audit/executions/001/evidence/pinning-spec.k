requires "verification.k"

module FACTORIZE-PINNING-SPEC
  imports FACTORIZE-VERIFICATION

  // The literal term below is the complete submitted solution.mpy program.
  // Loading it must create exactly the closure used by the entry claim.
  claim [submitted-module-loads-entry-state]:
    <k>
      #loadAll(Module(
        ImportFrom("typing", "List")
        FuncDef("factorize", Params("n"),
          Assign(Name("factors"), ListExpr(.Exprs))
          Assign(Name("divisor"), Int(2))
          While(Compare(Name("n"), CmpOp(">", Int(1))),
            If(Compare(
              BinOp("%", Name("n"), Name("divisor")),
              CmpOp("==", Int(0))),
              Expr(
                Call(Attribute(Name("factors"), "append"),
                     Name("divisor")))
              Assign(Name("n"),
                     BinOp("//", Name("n"), Name("divisor"))),
              AugAssign(Name("divisor"), "+", Int(1))))
          Return(Name("factors")))))
      => .K
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      (0 |-> scope(
         "factorize" |-> closureVal("n", factorizeBody, 0),
         parent(-1))
       -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
endmodule
