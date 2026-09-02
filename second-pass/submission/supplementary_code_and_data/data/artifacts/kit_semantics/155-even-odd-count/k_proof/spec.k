requires "verification.k"
requires "verification-with-lemma.k"

module LOOP-PROOF
  imports VERIFICATION

  // Loop-tail invariant: from nonnegative remaining magnitude N and current
  // counters E/O, the exact loop and return suffix add the digit summaries.
  claim [loop-tail]:
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
        => tuple(vCons(?ER:Int, vCons(?OR:Int, .ValSeq))) ~> CONT
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
    ensures ?ER ==Int E +Int evenPos(N)
     andBool ?OR ==Int O +Int oddPos(N)
endmodule

module SPEC
  imports VERIFICATION-WITH-LEMMA

  // Whole function call from an exact module binding, for every mathematical
  // integer accepted by the HumanEval signature.
  claim [even-odd-count]:
    <k> Call(Name("even_odd_count"), N:Int)
        => tuple(vCons(?ER:Int, vCons(?OR:Int, .ValSeq)))
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope("even_odd_count" |-> evenOddClosure, parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    ensures ?ER ==Int decEven(N)
     andBool ?OR ==Int decOdd(N)
endmodule
