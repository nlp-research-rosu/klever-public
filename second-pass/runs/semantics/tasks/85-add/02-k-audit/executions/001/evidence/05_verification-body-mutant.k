requires "reference-semantics/semantics.k"

module VERIFICATION-BODY-MUTANT
  imports MPY

  syntax ValSeq ::= intValsMut(IntSeq)

  rule <k> #iterNext(list(intValsMut(.IntSeq))) => #iterDone ... </k>
       [priority(40)]
  rule <k> #iterNext(list(intValsMut(iCons(I:Int, REST:IntSeq))))
        => #iterYield(I, list(intValsMut(REST))) ... </k>
       [priority(40)]

  syntax Int ::= addAccSpecMut(IntSeq, Bool, Int) [function]
  rule addAccSpecMut(.IntSeq, _:Bool, ACC:Int) => ACC
  rule addAccSpecMut(iCons(_:Int, REST:IntSeq), false, ACC:Int)
    => addAccSpecMut(REST, true, ACC)
  rule addAccSpecMut(iCons(I:Int, REST:IntSeq), true, ACC:Int)
    => addAccSpecMut(REST, false, ACC +Int I)
    requires pyMod(I, 2) ==Int 0
  rule addAccSpecMut(iCons(I:Int, REST:IntSeq), true, ACC:Int)
    => addAccSpecMut(REST, false, ACC)
    requires pyMod(I, 2) =/=Int 0

  syntax Stmts ::= "mutatedLoopBody" [macro]
  rule mutatedLoopBody
    => If(Name("odd_index"),
         If(Compare(BinOp("%", Name("value"), Int(2)),
                    CmpOp("==", Int(1))),
            AugAssign(Name("total"), "+", Name("value")),
            .Stmts),
         .Stmts)
       Assign(Name("odd_index"), UnaryOp("not", Name("odd_index")))
endmodule
