requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  claim [false-postcondition]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "car_race_collision",
            Params("n"),
            Return(BinOp("*", Name("n"), Name("n")))
          )
        )
      )
      ~> Call(Name("car_race_collision"), Int(N:Int))
      => (N *Int N) +Int 1
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0  |-> scope(
               "car_race_collision"
                 |-> closureVal(
                       ("n", .ParamNames),
                       (Return(BinOp("*", Name("n"), Name("n"))) .Stmts),
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
