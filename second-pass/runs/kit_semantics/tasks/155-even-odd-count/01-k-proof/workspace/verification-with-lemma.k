requires "verification.k"

module VERIFICATION-WITH-LEMMA
  imports VERIFICATION

  // Operational use of the independently proved LOOP-PROOF.loop-tail theorem.
  // Its complete match context and state footprint are identical to that claim.
  rule
    <k> #while(Compare(Name("num"), CmpOp(">", Int(0))),
          Assign(Name("even"),
                 BinOp("-",
                   BinOp("+", Name("even"), Int(1)),
                   BinOp("%", Name("num"), Int(2))))
          Assign(Name("odd"),
                 BinOp("+", Name("odd"), BinOp("%", Name("num"), Int(2))))
          Assign(Name("num"), BinOp("//", Name("num"), Int(10)))
          .Stmts)
        ~> (Return(TupleExpr(Name("even"), Name("odd"))) .Stmts)
        ~> #endcall
        => tuple(vCons(E +Int evenPos(N),
                      vCons(O +Int oddPos(N), .ValSeq))) ~> CONT
    </k>
    <env> 1 => 0 </env>
    <scopes>
      -1 |-> B:Scope
       0 |-> scope("even_odd_count" |-> C:Val, parent(-1))
       1 |-> scope("num"  |-> N
                   "even" |-> E
                   "odd"  |-> O,
                   parent(0))
      =>
      -1 |-> B
       0 |-> scope("even_odd_count" |-> C, parent(-1))
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(CONT, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >=Int 0
    [priority(40)]
endmodule
