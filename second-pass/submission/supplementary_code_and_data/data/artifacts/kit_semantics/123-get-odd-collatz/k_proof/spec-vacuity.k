requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false postcondition for the realizable input n = 1:
  // the returned heap list is mutated from [1] to [2].
  claim [false-result]:
    <k>
      FuncDef("get_odd_collatz", Params("n"),
        Assign(Name("odds"), ListExpr(.Exprs))
        Assign(Name("start"), Name("n"))
        Assign(Name("trace"), ListExpr(Name("start")))
        While(Compare(Name("n"), CmpOp(">", Int(1))),
          If(Compare(BinOp("%", Name("n"), Int(2)), CmpOp("==", Int(0))),
            Assign(Name("n"), BinOp("//", Name("n"), Int(2))),
            Expr(Call(Attribute(Name("odds"), "append"), Name("n")))
            Assign(
              Name("n"),
              BinOp("+", BinOp("*", Int(3), Name("n")), Int(1))))
          Expr(Call(Attribute(Name("trace"), "append"), Name("n"))))
        Expr(Call(Attribute(Name("odds"), "append"), Int(1)))
        Expr(Call(Attribute(Name("odds"), "sort"), .Exprs))
        Return(Name("odds")))
      ~> Call(Name("get_odd_collatz"), (1, .Exprs))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      ?SC:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(sortVS(vCons(2, .ValSeq)))
      1 |-> list(vCons(1, .ValSeq))
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
