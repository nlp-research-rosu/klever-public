requires "verification.k"

module IDENTITY-SPEC
  imports VERIFICATION

  claim [translated-program-identity]:
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
        BinOp(
          "-",
          BinOp("+", Name("even"), Int(1)),
          BinOp("%", Name("num"), Int(2))))
      Assign(
        Name("odd"),
        BinOp("+", Name("odd"), BinOp("%", Name("num"), Int(2))))
      Assign(Name("num"), BinOp("//", Name("num"), Int(10))))
    Return(TupleExpr(Name("even"), Name("odd")))))) => .K </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(.Map => "even_odd_count" |-> evenOddClosure, parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule

