requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // Body-sensitivity probe: the odd branch appends 2 instead of the current n.
  // On n = 3 this mutated function returns [1, 2, 2], so the original [1, 3, 5]
  // postcondition must be rejected.
  claim [mutated-body]:
    <k>
      FuncDef("get_odd_collatz", Params("n"),
        Assign(Name("odds"), ListExpr(.Exprs))
        Assign(Name("start"), Name("n"))
        Assign(Name("trace"), ListExpr(Name("start")))
        While(Compare(Name("n"), CmpOp(">", Int(1))),
          If(Compare(BinOp("%", Name("n"), Int(2)), CmpOp("==", Int(0))),
            Assign(Name("n"), BinOp("//", Name("n"), Int(2))),
            Expr(Call(Attribute(Name("odds"), "append"), Int(2)))
            Assign(
              Name("n"),
              BinOp("+", BinOp("*", Int(3), Name("n")), Int(1))))
          Expr(Call(Attribute(Name("trace"), "append"), Name("n"))))
        Expr(Call(Attribute(Name("odds"), "append"), Int(1)))
        Expr(Call(Attribute(Name("odds"), "sort"), .Exprs))
        Return(Name("odds")))
      ~> Call(Name("get_odd_collatz"), (3, .Exprs))
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
      0 |-> list(
        sortVS(vCons(1, vCons(3, vCons(5, .ValSeq)))))
      1 |-> list(?TV:ValSeq)
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
