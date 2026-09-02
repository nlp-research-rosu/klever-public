requires "reference-semantics/semantics.k"

module AUDIT-ITERATOR-MUTANT
  imports MPY

  // Structural embedding of every finite integer sequence into a ValSeq.
  syntax ValSeq ::= intVals(IntSeq)
  rule intVals(.IntSeq) => .ValSeq
  rule intVals(iCons(V:Int, VS:IntSeq))
    => vCons(V, intVals(VS))

  // Proof-local exposure of the two fixed list-iterator cases after intVals
  // unfolds once. No binding, state, or control behavior is skipped.
  rule <k> #iterNext(list(intVals(.IntSeq)))
        => #iterDone ... </k>
       [priority(40)]
  rule <k> #iterNext(list(intVals(iCons(V:Int, VS:IntSeq))))
        => #iterYield(0, list(intVals(VS))) ... </k>
       [priority(40)]

  // The contribution of the element at zero-based index I.
  syntax Int ::= squareContribution(Int, Int) [function, total]
  rule squareContribution(V:Int, I:Int)
    => V *Int V
    requires pyMod(I, 3) ==Int 0
  rule squareContribution(V:Int, I:Int)
    => V *Int V *Int V
    requires pyMod(I, 3) =/=Int 0
     andBool pyMod(I, 4) ==Int 0
  rule squareContribution(V:Int, I:Int)
    => V
    requires pyMod(I, 3) =/=Int 0
     andBool pyMod(I, 4) =/=Int 0

  // Exact left fold for a remaining suffix beginning at index I.
  syntax Int ::= sumSquaresFrom(IntSeq, Int, Int) [function, total]
  rule sumSquaresFrom(.IntSeq, _I:Int, A:Int) => A
  rule sumSquaresFrom(iCons(V:Int, VS:IntSeq), I:Int, A:Int)
    => sumSquaresFrom(
         VS,
         I +Int 1,
         A +Int squareContribution(V, I))
endmodule

module AUDIT-ITERATOR-FULL
  imports AUDIT-ITERATOR-MUTANT

  // Operational bridge justified by LOOP-SPEC.loop under
  // VERIFICATION-BASE. Its complete match context is identical to that
  // reachability theorem.
  rule
    <k>
      #loop(
        list(intVals(IS:IntSeq)),
        Name("value"),
        If(
          Compare(
            BinOp("%", Name("index"), Int(3)),
            CmpOp("==", Int(0))),
          Assign(
            Name("total"),
            BinOp(
              "+",
              Name("total"),
              BinOp("*", Name("value"), Name("value"))))
          .Stmts,
          If(
            Compare(
              BinOp("%", Name("index"), Int(4)),
              CmpOp("==", Int(0))),
            Assign(
              Name("total"),
              BinOp(
                "+",
                Name("total"),
                BinOp(
                  "*",
                  BinOp("*", Name("value"), Name("value")),
                  Name("value"))))
            .Stmts,
            Assign(
              Name("total"),
              BinOp("+", Name("total"), Name("value")))
            .Stmts)
          .Stmts)
        Assign(
          Name("index"),
          BinOp("+", Name("index"), Int(1)))
        .Stmts)
      ~> Return(Name("total")) .Stmts
      ~> #endcall
      =>
      sumSquaresFrom(IS, I:Int, A:Int)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      ( -1 |-> BUILTINS:Scope
         0 |-> scope(MODULE:Map, parent(-1))
         1 |-> scope(
                "lst" |-> list(INPUT:ValSeq)
                "index" |-> I
                "total" |-> A
                "value" |-> OLD:Val,
                parent(0)) )
      =>
      ( -1 |-> BUILTINS
         0 |-> scope(MODULE, parent(-1)) )
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack>
      ListItem(frame(.K, 0, 1))
      =>
      .List
    </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [priority(30)]
endmodule
