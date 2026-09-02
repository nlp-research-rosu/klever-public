requires "spec.k"

module BRIDGE-CONTEXT-SPEC
  imports LOOP-SPEC

  // The observable assignment immediately after the summarized loop must be
  // preserved. This claim uses the same universal loop state as LOOP-SPEC and
  // requires "after" to become "z" after the loop.
  claim
    <k>
      #loop(
        str(S:IntSeq),
        Name("character"),
        If(
          Compare(Name("character"), CmpOp("not in", Name("c"))),
          AugAssign(Name("result"), "+", Name("character"))
          Assign(
            Name("reversed_result"),
            BinOp("+", Name("character"), Name("reversed_result"))),
          .Stmts))
      ~> Assign(Name("after"), Str("z"))
      => .K
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      ...
      L |->
        ( scope(
            ( "s" |-> str(ORIG:IntSeq)
              "c" |-> str(C:IntSeq)
              "result" |-> str(A:IntSeq)
              "reversed_result" |-> str(RA:IntSeq)
              "character" |-> V:Val
              "after" |-> str(iCons(120, .IntSeq)) ),
            P:Parent)
        => scope(
            ( "s" |-> str(ORIG)
              "c" |-> str(C)
              "result" |-> str(keptAcc(S, C, A))
              "reversed_result" |-> str(reversedKeptAcc(S, C, RA))
              "character" |-> lastCharacter(S, V)
              "after" |-> str(iCons(122, .IntSeq)) ),
            P) )
      ...
    </scopes>
endmodule
