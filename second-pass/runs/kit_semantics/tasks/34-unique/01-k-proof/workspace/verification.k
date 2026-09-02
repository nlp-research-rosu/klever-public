requires "reference-semantics/semantics.k"

module VERIFICATION-BASE
  imports MPY

  // Exact mathematical summary of MPY-LIST's #memberAcc fold.
  syntax Bool ::= memberVS(Val, ValSeq) [function, total]
  rule memberVS(_:Val, .ValSeq) => false
  rule memberVS(V:Val, vCons(E:Val, R:ValSeq)) => memberVS(V, R)
    requires notBool (V ==K E)
    [simplification]
  rule memberVS(V:Val, vCons(E:Val, _:ValSeq)) => true
    requires V ==K E
    [simplification]

  // Append V precisely when it is not already present in ACC.
  syntax ValSeq ::= appendUnique(ValSeq, Val) [function, total]
  rule appendUnique(ACC:ValSeq, V:Val) => ACC
    requires memberVS(V, ACC)
  rule appendUnique(ACC:ValSeq, V:Val)
    => valSeqConcat(ACC, vCons(V, .ValSeq))
    requires notBool memberVS(V, ACC)

  // First-seen-order deduplication, parameterized by the current accumulator.
  syntax ValSeq ::= dedupFromVS(ValSeq, ValSeq) [function, total]
  rule dedupFromVS(.ValSeq, ACC:ValSeq) => ACC
  rule dedupFromVS(vCons(V:Val, R:ValSeq), ACC:ValSeq)
    => dedupFromVS(R, appendUnique(ACC, V))

  // Value left in the source for-loop target after consuming VS.
  syntax Val ::= lastFromVS(ValSeq, Val) [function, total]
  rule lastFromVS(.ValSeq, X:Val) => X
  rule lastFromVS(vCons(V:Val, R:ValSeq), _:Val) => lastFromVS(R, V)
endmodule

module VERIFICATION-MEMBER
  imports VERIFICATION-BASE

  // Operational bridge admitted only after MEMBER-SPEC proves the identical
  // arbitrary-continuation theorem using VERIFICATION-BASE (without this rule).
  rule <k> #memberAcc(V:Val, list(VS:ValSeq))
    => memberVS(V, VS) ... </k>
    [priority(40)]
endmodule

module VERIFICATION
  imports VERIFICATION-MEMBER

  // Operational bridge admitted only after LOOP-SPEC proves the identical
  // arbitrary-continuation loop theorem using VERIFICATION-MEMBER (without
  // this rule).  Return, sorted(), allocation, and frame-pop still execute.
  rule
    <k>
      #loop(
        list(VS:ValSeq),
        Name("x"),
        If(
          Compare(Name("x"), CmpOp("not in", Name("result"))),
          Expr(Call(Attribute(Name("result"), "append"), Name("x"))),
          .Stmts))
      => .K ...
    </k>
    <env> 1 </env>
    <scopes>
      ... 1 |-> scope(
        ("l" |-> ref(0))
        ("result" |-> ref(1))
        ("x" |-> (X:Val => lastFromVS(VS, X))),
        parent(0))
      ...
    </scopes>
    <heap>
      ... 1 |-> list(ACC:ValSeq => dedupFromVS(VS, ACC)) ...
    </heap>
    [priority(40)]
endmodule
