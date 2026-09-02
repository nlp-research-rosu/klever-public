requires "verification.k"

module BRIDGE-CONTEXT-BASE
  imports MPY-VERIFICATION-BASE

  claim
    <k>
      #loop(
        str(iCons(97, iCons(98, .IntSeq))),
        Name("character"),
        If(
          Compare(Name("character"), CmpOp("not in", Name("c"))),
          AugAssign(Name("result"), "+", Name("character"))
          Assign(
            Name("reversed_result"),
            BinOp("+", Name("character"), Name("reversed_result"))),
          .Stmts))
      ~> Assign(Name("after"), Str("x"))
      => .K
    </k>
    <env> 1 </env>
    <scopes>
      1 |->
        ( scope(
            ( "s" |-> str(iCons(97, iCons(98, .IntSeq)))
              "c" |-> str(.IntSeq)
              "result" |-> str(.IntSeq)
              "reversed_result" |-> str(.IntSeq)
              "character" |-> str(.IntSeq) ),
            parent(0))
        => scope(
            ( "s" |-> str(iCons(97, iCons(98, .IntSeq)))
              "c" |-> str(.IntSeq)
              "result" |-> str(iCons(97, iCons(98, .IntSeq)))
              "reversed_result" |-> str(iCons(98, iCons(97, .IntSeq)))
              "character" |-> str(iCons(98, .IntSeq))
              "after" |-> str(iCons(120, .IntSeq)) ),
            parent(0)) )
    </scopes>
endmodule

module BRIDGE-CONTEXT-ENABLED
  imports MPY-VERIFICATION

  claim
    <k>
      #loop(
        str(iCons(97, iCons(98, .IntSeq))),
        Name("character"),
        If(
          Compare(Name("character"), CmpOp("not in", Name("c"))),
          AugAssign(Name("result"), "+", Name("character"))
          Assign(
            Name("reversed_result"),
            BinOp("+", Name("character"), Name("reversed_result"))),
          .Stmts))
      ~> Assign(Name("after"), Str("x"))
      => .K
    </k>
    <env> 1 </env>
    <scopes>
      1 |->
        ( scope(
            ( "s" |-> str(iCons(97, iCons(98, .IntSeq)))
              "c" |-> str(.IntSeq)
              "result" |-> str(.IntSeq)
              "reversed_result" |-> str(.IntSeq)
              "character" |-> str(.IntSeq) ),
            parent(0))
        => scope(
            ( "s" |-> str(iCons(97, iCons(98, .IntSeq)))
              "c" |-> str(.IntSeq)
              "result" |-> str(iCons(97, iCons(98, .IntSeq)))
              "reversed_result" |-> str(iCons(98, iCons(97, .IntSeq)))
              "character" |-> str(iCons(98, .IntSeq))
              "after" |-> str(iCons(120, .IntSeq)) ),
            parent(0)) )
    </scopes>
endmodule
