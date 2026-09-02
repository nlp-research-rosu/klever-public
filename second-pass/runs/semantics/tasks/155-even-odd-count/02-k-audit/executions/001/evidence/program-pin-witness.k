requires "verification.k"

// Exact submitted solution.mpy AST, after the trusted translator's byte check,
// loaded by the fixed semantics into the module scope used by the entry claim.
module PROGRAM-PIN-WITNESS
  imports EVEN-ODD-VERIFICATION

  claim
    <k>
      #loadAll(
        Module(
          FuncDef("even_odd_count", Params("num"),
            Expr(
              Str("Return the counts of even and odd decimal digits in num."))
            Assign(Name("even_count"), Int(0))
            Assign(Name("odd_count"), Int(0))
            Assign(Name("digit"), Int(0))
            For(Name("digit"), Call(Name("str"), Call(Name("abs"), Name("num"))),
              If(Compare(
                BinOp("%", Call(Name("ord"), Name("digit")), Int(2)),
                CmpOp("==", Int(0))),
                AugAssign(Name("even_count"), "+", Int(1)),
                AugAssign(Name("odd_count"), "+", Int(1))))
            Return(TupleExpr(Name("even_count"), Name("odd_count"))))))
    =>
      .K
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    =>
      0  |-> #evenOddModuleScope
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
