requires "verification.k"

module SPEC
  imports VERIFICATION

  claim
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
      ~> callEntry(listVal(
           cons(intVal(1), cons(intVal(2), cons(intVal(3), nil)))))
      => intVal(14)
    </k>
    <functions> .Map => ?FUNS:Map </functions>
    <env> .Env => ?ENV:Env </env>

  claim [all-numeric-lists]:
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
      => intVal(sumSquares(L))
    </k>
    <functions> .Map => ?FUNS:Map </functions>
    <env> .Env => ?ENV:Env </env>

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

  claim
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
      ~> callEntry(listVal(
           cons(ratVal(14, ten), cons(ratVal(42, ten), cons(intVal(0), nil)))))
      => intVal(29)
    </k>
    <functions> .Map => ?FUNS:Map </functions>
    <env> .Env => ?ENV:Env </env>

  claim
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
      ~> callEntry(listVal(
           cons(ratVal(-24, ten), cons(intVal(1), cons(intVal(1), nil)))))
      => intVal(6)
    </k>
    <functions> .Map => ?FUNS:Map </functions>
    <env> .Env => ?ENV:Env </env>
endmodule
