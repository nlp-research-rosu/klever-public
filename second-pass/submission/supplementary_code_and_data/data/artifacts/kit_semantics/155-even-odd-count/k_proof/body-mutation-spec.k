requires "verification-with-lemma.k"

module BODY-MUTATION-SPEC
  imports VERIFICATION-WITH-LEMMA

  claim [mutated-body-rejected]:
    <k> #loadAll(Module(
  FuncDef("even_odd_count", Params("num"),
    Expr(
      Str("Return the counts of even and odd decimal digits in num."))
    Assign(Name("num"), Call(Name("abs"), Name("num")))
    Assign(Name("even"), Int(0))
    Assign(Name("odd"), Int(0))
    If(Compare(Name("num"), CmpOp("==", Int(0))),
      Return(TupleExpr(Int(1), Int(0))), .Stmts)
    While(Compare(Name("num"), CmpOp(">", Int(0))),
      Assign(
        Name("even"),
        BinOp("+", Name("even"), BinOp("%", Name("num"), Int(2))))
      Assign(
        Name("odd"),
        BinOp("+", Name("odd"), BinOp("%", Name("num"), Int(2))))
      Assign(Name("num"), BinOp("//", Name("num"), Int(10))))
    Return(TupleExpr(Name("even"), Name("odd"))))))
         ~> Call(Name("even_odd_count"), Int(2))
         => tuple(vCons(1, vCons(0, .ValSeq)))
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(.Map => ?M:Map, parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule

