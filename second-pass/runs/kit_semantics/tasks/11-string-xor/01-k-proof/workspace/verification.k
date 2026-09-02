requires "reference-semantics/semantics.k"

module VERIFICATION-BASE
  imports MPY

  // Mathematical summary of the result accumulated by the source loop.
  // zip truncates at the shorter sequence; equal bits append '0', unequal
  // bits append '1'.
  syntax IntSeq ::= xorAcc(IntSeq, IntSeq, IntSeq) [function, total]
  rule xorAcc(ACC:IntSeq, .IntSeq, _:IntSeq) => ACC
    [simplification]
  rule xorAcc(ACC:IntSeq, iCons(_:Int, _:IntSeq), .IntSeq) => ACC
    [simplification]
  rule xorAcc(ACC:IntSeq,
              iCons(A:Int, AS:IntSeq),
              iCons(B:Int, BS:IntSeq))
    => xorAcc(seqConcat(ACC, iCons(48, .IntSeq)), AS, BS)
    requires A ==Int B
    [simplification]
  rule xorAcc(ACC:IntSeq,
              iCons(A:Int, AS:IntSeq),
              iCons(B:Int, BS:IntSeq))
    => xorAcc(seqConcat(ACC, iCons(49, .IntSeq)), AS, BS)
    requires A =/=Int B
    [simplification]

  // The HumanEval contract restricts inputs to strings of '0' and '1'.
  syntax Bool ::= bitString(IntSeq) [function, total]
  rule bitString(.IntSeq) => true
    [simplification]
  rule bitString(iCons(C:Int, CS:IntSeq))
    => (C ==Int 48 orBool C ==Int 49) andBool bitString(CS)
    [simplification]

  // Exact final values of the source loop targets.  They remain unchanged
  // when zip is empty and otherwise hold the last pair yielded by zip.
  syntax Val ::= lastX(Val, IntSeq, IntSeq) [function, total]
  rule lastX(X:Val, .IntSeq, _:IntSeq) => X
    [simplification]
  rule lastX(X:Val, iCons(_:Int, _:IntSeq), .IntSeq) => X
    [simplification]
  rule lastX(_:Val,
             iCons(A:Int, AS:IntSeq),
             iCons(_:Int, BS:IntSeq))
    => lastX(str(iCons(A, .IntSeq)), AS, BS)
    [simplification]

  syntax Val ::= lastY(Val, IntSeq, IntSeq) [function, total]
  rule lastY(Y:Val, .IntSeq, _:IntSeq) => Y
    [simplification]
  rule lastY(Y:Val, iCons(_:Int, _:IntSeq), .IntSeq) => Y
    [simplification]
  rule lastY(_:Val,
             iCons(_:Int, AS:IntSeq),
             iCons(B:Int, BS:IntSeq))
    => lastY(str(iCons(B, .IntSeq)), AS, BS)
    [simplification]
endmodule

module VERIFICATION
  imports VERIFICATION-BASE

  // Operational use of the independently proved LOOP-SPEC.loop-invariant
  // theorem.  The rule's complete match domain is identical to that claim:
  // exact loop, continuation, binding, frames, and cells.
  rule
    <k>
      #loop(
        zipObjS(A:IntSeq, B:IntSeq),
        TupleExpr(Name("x"), Name("y")),
        If(
          Compare(Name("x"), CmpOp("==", Name("y"))),
          AugAssign(Name("result"), "+", Str("0")),
          AugAssign(Name("result"), "+", Str("1"))
        )
      )
      =>
      .K
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      ...
      L |-> scope(
        "a"      |-> str(A0:IntSeq)
        "b"      |-> str(B0:IntSeq)
        "result" |-> (str(R:IntSeq) => str(xorAcc(R, A, B)))
        "x"      |-> (X0:Val => lastX(X0, A, B))
        "y"      |-> (Y0:Val => lastY(Y0, A, B)),
        P:Parent
      )
      ...
    </scopes>
    [priority(40)]
endmodule
