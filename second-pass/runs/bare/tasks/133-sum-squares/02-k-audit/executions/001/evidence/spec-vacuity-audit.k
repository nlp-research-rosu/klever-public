requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Deliberately false: for L=nil the real program returns 0, not 1.
  claim [false-all-numeric-lists]:
    <k>
      Module(
        ImportFrom("math", "ceil")
        FuncDef("sum_squares", Params("lst"),
          Assign(Name("total"), Int(0))
          For(Name("number"), Name("lst"),
            Assign(Name("rounded"), Call(Name("ceil"), Name("number")))
            AugAssign(Name("total"), "+",
              BinOp("*", Name("rounded"), Name("rounded"))))
          Return(Name("total")))
        .PyStmts)
      ~> callEntry(listVal(L:PList))
      => intVal(sumSquares(L) +Int 1)
    </k>
    <functions> .Map => ?FUNS:Map </functions>
    <env> .Env => ?ENV:Env </env>

  // Exact dependency of the genuine universal claim.
  claim [loop-invariant]:
    <k>
      loop("number", listVal(L:PList),
        Assign(Name("rounded"), Call(Name("ceil"), Name("number")))
        AugAssign(Name("total"), "+",
          BinOp("*", Name("rounded"), Name("rounded")))
        .PyStmts)
      ~> exec(Return(Name("total")) .PyStmts)
      => intVal(sumSquaresFrom(A:Int, L))
    </k>
    <functions> FUNS:Map </functions>
    <env>
      (binding("total", intVal(A)) REST:Env) => ?ENV:Env
    </env>
endmodule
