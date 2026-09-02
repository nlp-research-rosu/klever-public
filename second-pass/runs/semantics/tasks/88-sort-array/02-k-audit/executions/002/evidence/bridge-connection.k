requires "verification.k"

module BRIDGE-CONNECTION
  imports VERIFICATION

  // Exact symbolic domain used by the two general entry claims.
  claim [reachable-domain]:
    <k>
      Subscript(
        list(vCons(F:Int, snocVS(intsVS(MIDDLE:IntSeq), L:Int))),
        UnaryOp("-", Int(1)))
      => L
      ...
    </k>

  // Complete syntactic match domain admitted by the candidate bridge.
  claim [complete-match-domain]:
    <k>
      Subscript(
        list(vCons(F:Int, snocVS(MIDDLE:ValSeq, L:Int))),
        UnaryOp("-", Int(1)))
      => L
      ...
    </k>

  // Ground fixed-semantics executions using actual constructor lists.
  claim [fixed-ground-empty-middle]:
    <k>
      BinOp(
        "+",
        Subscript(
          list(vCons(2, vCons(5, .ValSeq))),
          UnaryOp("-", Int(1))),
        Int(10))
      => 15
      ...
    </k>

  claim [fixed-ground-one-middle]:
    <k>
      BinOp(
        "+",
        Subscript(
          list(vCons(2, vCons(4, vCons(5, .ValSeq)))),
          UnaryOp("-", Int(1))),
        Int(10))
      => 15
      ...
    </k>

  // Corresponding proof-representation executions admitted by the bridge.
  claim [bridge-ground-empty-middle]:
    <k>
      BinOp(
        "+",
        Subscript(
          list(vCons(2, snocVS(.ValSeq, 5))),
          UnaryOp("-", Int(1))),
        Int(10))
      => 15
      ...
    </k>

  claim [bridge-ground-one-middle]:
    <k>
      BinOp(
        "+",
        Subscript(
          list(vCons(2, snocVS(vCons(4, .ValSeq), 5))),
          UnaryOp("-", Int(1))),
        Int(10))
      => 15
      ...
    </k>
endmodule
