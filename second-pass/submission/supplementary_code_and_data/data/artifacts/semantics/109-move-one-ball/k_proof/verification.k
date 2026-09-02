requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // These constants are a literal transcription of solution.mpy.  Naming the
  // body here keeps the reachability claims readable without adding any
  // execution rule for move_one_ball.
  syntax Stmts ::= "MOVE-ONE-BALL-LOOP-BODY" [function]
  rule MOVE-ONE-BALL-LOOP-BODY
    => If(Compare(Name("current"), CmpOp("<", Name("previous"))),
          AugAssign(Name("drops"), "+", Int(1)),
          .Stmts)
       Assign(Name("previous"), Name("current"))

  syntax Stmts ::= "MOVE-ONE-BALL-BODY" [function]
  rule MOVE-ONE-BALL-BODY
    => If(Compare(Call(Name("len"), Name("arr")), CmpOp("==", Int(0))),
          Return(Bool(true)),
          .Stmts)
       Assign(Name("drops"), Int(0))
       Assign(Name("first"), Subscript(Name("arr"), Int(0)))
       Assign(Name("previous"), Name("first"))
       For(Name("current"), Name("arr"), MOVE-ONE-BALL-LOOP-BODY)
       If(Compare(Name("first"), CmpOp("<", Name("previous"))),
          AugAssign(Name("drops"), "+", Int(1)),
          .Stmts)
       Return(Compare(Name("drops"), CmpOp("<", Int(2))))

  syntax Val ::= "MOVE-ONE-BALL-CLOSURE" [function]
  rule MOVE-ONE-BALL-CLOSURE
    => closureVal("arr", MOVE-ONE-BALL-BODY, 0)

  // A typed, symbolic encoding of a finite Python list of integers.  The
  // wrapper stays visible so a circularity can match its IntSeq tail without
  // admitting non-integer Val elements.
  syntax ValSeq ::= intVals(IntSeq)

  // Constructor-exposure lemmas.  The generic list rules see only ValSeq and
  // cannot split an opaque symbolic IntSeq themselves, so these equivalent
  // typed cases expose exactly the two IntSeq constructors to symbolic
  // execution.  They add no behavior on concrete lists.
  rule <k> #iterNext(list(intVals(.IntSeq))) => #iterDone ... </k>
       [priority(40)]
  rule <k> #iterNext(list(intVals(iCons(I:Int, IS:IntSeq))))
        => #iterYield(I, list(intVals(IS))) ... </k>
       [priority(40)]

  rule <k> #applyK(toCall(builtinV("len")),
                   (list(intVals(.IntSeq)), .Vals))
        => 0 ... </k>
       [priority(40)]
  rule <k> #applyK(toCall(builtinV("len")),
                   (list(intVals(iCons(_I:Int, _IS:IntSeq))), .Vals))
        => 1 ... </k>
       [priority(40)]
  // The target observes len(arr) only through == 0, so 1 is the exact
  // zero/nonzero abstraction of every nonempty symbolic list.

  rule <k> Subscript(list(intVals(iCons(I:Int, _IS:IntSeq))), 0)
        => I ... </k>
       [priority(40)]

  // One descent is added precisely when the next item is below the previous
  // item.  scanDrops and scanLast are the pure mathematical fold used by the
  // postcondition.
  syntax Int ::= addDrop(Int, Int, Int) [function, total]
  rule addDrop(C:Int, P:Int, D:Int)
    => D +Int (#if C <Int P #then 1 #else 0 #fi)

  syntax Int ::= scanDrops(ValSeq, Int, Int) [function, total]
  rule scanDrops(.ValSeq, _P:Int, D:Int) => D
  rule scanDrops(vCons(C:Int, R:ValSeq), P:Int, D:Int)
    => scanDrops(R, C, addDrop(C, P, D))
  rule scanDrops(intVals(.IntSeq), _P:Int, D:Int) => D
  rule scanDrops(intVals(iCons(C:Int, IS:IntSeq)), P:Int, D:Int)
    => scanDrops(intVals(IS), C, addDrop(C, P, D))

  syntax Int ::= scanLast(ValSeq, Int) [function, total]
  rule scanLast(.ValSeq, P:Int) => P
  rule scanLast(vCons(C:Int, R:ValSeq), _P:Int)
    => scanLast(R, C)
  rule scanLast(intVals(.IntSeq), P:Int) => P
  rule scanLast(intVals(iCons(C:Int, IS:IntSeq)), _P:Int)
    => scanLast(intVals(IS), C)

  syntax Int ::= circularDrops(Int, ValSeq) [function, total]
  rule circularDrops(F:Int, VS:ValSeq)
    => addDrop(F, scanLast(VS, F), scanDrops(VS, F, 0))

  syntax Bool ::= moveOneBallSpec(ValSeq) [function, total]
  rule moveOneBallSpec(.ValSeq) => true
  rule moveOneBallSpec(vCons(F:Int, R:ValSeq))
    => circularDrops(F, vCons(F, R)) <Int 2
  rule moveOneBallSpec(intVals(.IntSeq)) => true
  rule moveOneBallSpec(intVals(iCons(F:Int, IS:IntSeq)))
    => circularDrops(F, intVals(iCons(F, IS))) <Int 2

endmodule
